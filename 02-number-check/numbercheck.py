"""numbercheck: refuse AI-written text that contains a number its source data does not.

    from numbercheck import unsourced_numbers
    bad = unsourced_numbers(ai_paragraph, source_data)
    if bad:
        raise ValueError(f"numbers not in the source: {bad}")

source_data is anything JSON-like (dict, list, numbers, strings); every number inside it counts as sourced. A number in
the text passes when it equals a source number, or is that number rounded the way people round (36.3 written as 36,
1,240 as 1.2k, 0.25 as 25%). Years and small counting words can be allowed with allow=. Standard library only."""
import re

NUM = re.compile(r"(?<![\w.])[$£€]?(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?\s*(k|m|bn|%|percent)?(?![\w])", re.I)
SCALE = {"k": 1e3, "m": 1e6, "bn": 1e9}


def numbers_in(text):
    """[(as written, value)] for every number in a piece of text."""
    out = []
    for m in NUM.finditer(text or ""):
        whole, frac, unit = m.group(1).replace(",", ""), m.group(2), (m.group(3) or "").lower()
        v = float(f"{whole}.{frac}" if frac else whole) * SCALE.get(unit, 1)
        out.append((m.group(0).strip(), v, unit in ("%", "percent"), len(frac or "")))
    return out


def source_numbers(data):
    found = []
    if isinstance(data, bool):
        return found
    if isinstance(data, (int, float)):
        return [float(data)]
    if isinstance(data, str):
        return [v for _, v, _, _ in numbers_in(data)]
    if isinstance(data, dict):
        data = list(data.values())
    if isinstance(data, (list, tuple)):
        for x in data:
            found += source_numbers(x)
    return found


def _matches(v, pct, places, src):
    for s in src:
        for cand in ((s, s * 100) if pct else (s,)):
            if abs(cand - v) < 1e-9:
                return True
            step = 10 ** -places                      # 36 matches 36.3; 36.3 does not match 36.35 at one place
            if abs(cand - v) <= step / 2 + 1e-9 and cand != 0:
                return True
            for scale in (1e3, 1e6, 1e9):             # 1.2k for 1,240
                if v >= scale and abs(cand - v) <= scale * step / 2 + 1e-9:
                    return True
    return False


def unsourced_numbers(text, source_data, allow=()):
    """The numbers in text that the source does not hold, as written. Empty list means the text is clean."""
    src = source_numbers(source_data) + [float(a) for a in allow]
    return [w for w, v, pct, places in numbers_in(text) if not _matches(v, pct, places, src)]
