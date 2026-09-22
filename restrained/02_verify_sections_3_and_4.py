#!/usr/bin/env python3
"""Recompute every abundancy bound in Ochem-Zelinsky sections 3 and 4.
Several sit within 3% of 2, so they are the load-bearing numbers."""
from decimal import Decimal as D, getcontext
getcontext().prec = 40

Ainf = D(1); k = 7
while k < 400:
    Ainf *= (D(1) + D(1)/(D(7)**(D(k)/D(2)) - D(2))) ** (k-1); k += 1

def sig(p, e):      # exact sigma(p^e)/p^e
    return sum(D(p)**i for i in range(e+1)) / D(p)**e
def cap(p):         # sup over e of sigma(p^e)/p^e
    return D(p)/D(p-1)

rows = [
 ("S3 ruling out 127", [sig(3,2), sig(7,2), cap(13), sig(19,2), cap(127)],
  (D(10)**-10, 2+14), "1.9592144484846309"),
 ("S3 ruling out 331", [sig(3,2), sig(13,2), sig(31,2), cap(61), cap(331)],
  (D(10)**-10, 2+14), "1.6675275884645719"),
 ("S3 ruling out 19",  [sig(3,2), sig(7,2), cap(13), cap(19)],
  (D(10)**-5, 4+14), "1.944420956068104"),
 ("S3 ruling out 31",  [sig(3,2), sig(13,2), cap(31), cap(61)],
  (D(10)**-3, 4+14), "1.69272709609736065"),
 ("S3 final argument", [sig(3,2), cap(7), cap(13), cap(61), cap(97), cap(193)],
  (D(10)**-3, 8+14), "1.9497723588476532"),
]
print(f"A_inf = {Ainf:.20f}")
print()
print(f"{'bound':<22} {'recomputed':>24} {'paper':>22} {'<2':>5} {'agrees':>7}")
for name, facs, (eps, cnt), stated in rows:
    v = D(1)
    for f in facs: v *= f
    v *= (D(1)+eps)**cnt
    v *= Ainf
    st = D(stated)
    agree = abs(v-st) < D("1e-6")
    print(f"{name:<22} {v:>24.16f} {stated:>22} {str(v<2):>5} {str(agree):>7}")

print()
print("="*74)
print("SECTION 4 final computation")
print("="*74)
z = D(216171986291); K = 43500000000
tail = (D(1) + 1/z) ** K
base = D("1.5") * (D(1) + D(1)/D(6000000))
print(f"  (1 + 1/z)^K with z = {z}, K = {K}   = {tail:.16f}")
print(f"  3/2 * (1 + 1/6000000)                                = {base:.16f}")
for label, A in [("1.076855990994 (as stated in the final product)", D("1.076855990994")),
                 ("1.088507187872 (the abundancy quoted for the sieve)", D("1.088507187872"))]:
    v = base * A * tail
    print(f"  with A = {label}")
    print(f"      product = {v:.20f}   < 2 ? {v < 2}")
print(f"  paper states     1.99209763359616948564")
print()
print("""NOTE.  Neither reading of the transcribed abundancy constant reproduces the
stated product 1.99209763359616948564.  The text quotes two different numbers
-- 1.088507187872 for what the sieve reached, and 1.076855990994 inside the
final product -- and neither gives the stated value.  The most likely
explanation is OCR damage in the transcription I was given, not an error in
the paper; I cannot distinguish without the PDF.

What matters for the argument is unaffected: EVERY candidate reading gives a
product below 2, which is all section 4 needs.  The conclusion q >= 23e9 does
not depend on which reading is correct.""")
