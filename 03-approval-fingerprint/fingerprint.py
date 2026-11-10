"""fingerprint: tie an approval to the exact caption and image bytes, so a change after sign-off un-approves it.

    from fingerprint import fingerprint, still_approved
    approval = {"by": "legal", "sha": fingerprint(caption, ["hero.png"])}      # store this when they say yes
    if not still_approved(approval, caption, ["hero.png"]):                     # check it again before posting
        raise SystemExit("changed since it was approved: ask again")

One changed pixel, one swapped file or one edited comma changes the fingerprint. Standard library only."""
import hashlib
import os
import unicodedata


def fingerprint(caption, files=()):
    h = hashlib.sha256()
    text = unicodedata.normalize("NFC", caption or "").strip()
    h.update(b"caption\0" + text.encode("utf-8") + b"\0")
    for p in files:
        h.update(b"file\0" + os.path.basename(p).encode() + b"\0")
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest()


def still_approved(approval, caption, files=()):
    return bool(approval and approval.get("sha")) and approval["sha"] == fingerprint(caption, files)
