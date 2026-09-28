#!/usr/bin/env python3
"""Exact Algorithm-1 M2 membership for q < Y, as a byte map, using the same logic as restrained/12.
Used by 16c_selberg_tables.c.  Run: python3 16b_m2_dump.py Y out.bin  (Y = 1e8 takes about 20 s)."""

import sys, math
Y = int(sys.argv[1]); out = sys.argv[2]; LO = 3_000_000
isp = bytearray([1]) * (Y + 1); isp[:2] = b"\0\0"
for i in range(2, math.isqrt(Y) + 1):
    if isp[i]: isp[i*i::i] = bytearray(len(range(i*i, Y + 1, i)))
hit = bytearray(Y + 1); m2 = bytearray(Y + 1); surv = bytearray(Y // 2 + 2)
def add(q):
    m2[q] = 1
    e = (q - 1) // 3
    rho = next(r for r in (pow(g, e, q) for g in range(2, q)) if r != 1)
    for c in (rho, q - 1 - rho):
        t = c + q
        if t <= Y: hit[t::q] = b"\1" * len(range(t, Y + 1, q))
for q in range(7, LO):
    if isp[q] and q % 3 == 1: add(q)
for r in range(LO + 1, Y + 1):
    if not isp[r]: continue
    if not hit[r]:
        if r <= Y // 2 + 1: surv[r] = 1
    elif r % 3 == 1 and (r % 4 == 3 or not surv[(r + 1) // 2]): add(r)
open(out, "wb").write(bytes(m2))
print("M2 primes below", Y, ":", sum(m2))
