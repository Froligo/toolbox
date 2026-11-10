from numbercheck import numbers_in, unsourced_numbers

src = {"revenue": 18240.55, "orders": 412, "conversion": 0.031, "note": "up from 23.7% in 2019"}
assert unsourced_numbers("Revenue was $18,240.55 from 412 orders.", src) == []
assert unsourced_numbers("Revenue was about $18,241 and 18.2k overall.", src) == []      # rounding people do
assert unsourced_numbers("Conversion was 3.1%, up from 23.7% in 2019.", src) == []
assert unsourced_numbers("Revenue rose 40% to $19,000 on 412 orders.", src) == ["40%", "$19,000"]
assert unsourced_numbers("We had 3 big days.", src) == ["3"]
assert unsourced_numbers("We had 3 big days.", src, allow=[3]) == []
assert [w for w, *_ in numbers_in("v2.0 shipped, 1,240 users, 5m views")] == ["1,240", "5m"]
print("ok numbercheck")
