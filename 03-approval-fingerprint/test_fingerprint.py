import os
import tempfile
from fingerprint import fingerprint, still_approved

d = tempfile.mkdtemp()
img = os.path.join(d, "hero.png")
open(img, "wb").write(b"\x89PNG" + bytes(range(256)) * 40)
ok = {"by": "legal", "sha": fingerprint("Summer sale, 20% off", [img])}
assert still_approved(ok, "Summer sale, 20% off", [img])
assert still_approved(ok, "  Summer sale, 20% off \n", [img])          # outer whitespace is not a change
assert not still_approved(ok, "Summer sale, 25% off", [img])            # the words changed
b = bytearray(open(img, "rb").read()); b[100] ^= 1; open(img, "wb").write(b)
assert not still_approved(ok, "Summer sale, 20% off", [img])            # one bit of the image changed
assert not still_approved({}, "x", [])
print("ok fingerprint")
