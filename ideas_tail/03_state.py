#!/usr/bin/env python3
"""
ideas_tail/03 -- exact Algorithm-1 state below Y, saved as one byte map for reuse.

status[n] for 0 <= n <= Y:
   0  not a prime >= 5 (or not examined)
   1  prime < 3e6 (in M1, and in M2 if = 1 mod 3)
   2  survivor ("can be ordinary")
   3  non-survivor, in M1 but NOT in M2 (= 2 mod 3, or a special candidate)
   4  non-survivor, in M2 (= 1 mod 3, cannot divide N)
So:  M2 = {status 4} u {status 1 and = 1 mod 3};   M1 = {1, 3, 4};   D = allowed
primes = 1 mod 3 with status 2 or 3.
Logic identical to restrained/12 (the exact Python reference).  The checkpoint
k and ln A at 1e8 are printed so they can be compared with restrained/13.
Run:  python3 03_state.py Y OUT        (Y = 1e8: about 3 minutes, 0.2 GB)
"""
import sys, math
Y = int(float(sys.argv[1])); OUT = sys.argv[2]; LO = 3_000_000
isp = bytearray([1]) * (Y + 1); isp[:2] = b"\0\0"
for i in range(2, math.isqrt(Y) + 1):
    if isp[i]: isp[i*i::i] = bytearray(len(range(i*i, Y + 1, i)))
hit = bytearray(Y + 1); st = bytearray(Y + 1)
def cube_root(q):
    e = (q - 1) // 3
    for g in range(2, q):
        x = pow(g, e, q)
        if x != 1: return x
def add(q):
    rho = cube_root(q)
    for c in (rho, q - 1 - rho):
        t = c + q
        if t <= Y: hit[t::q] = b"\1" * len(range(t, Y + 1, q))
for q in range(5, LO):
    if isp[q]:
        st[q] = 1
        if q % 3 == 1: add(q)
k = 0; acc = []
for r in range(LO + 1, Y + 1):
    if not isp[r]: continue
    if not hit[r]:
        st[r] = 2; k += 1; acc.append(math.log1p(1.0 / (r - 1)))
    elif r % 3 == 1 and (r % 4 == 3 or st[(r + 1) // 2] != 2):
        st[r] = 4; add(r)
    else:
        st[r] = 3
open(OUT, "wb").write(bytes(st))
print(f"Y={Y} k={k} lnA={math.fsum(acc):.15f} "
      f"M2={sum(1 for n in range(7, Y + 1) if (st[n] == 4 or (st[n] == 1 and n % 3 == 1)))} "
      f"special_candidates={sum(1 for n in range(LO, Y + 1) if st[n] == 3 and n % 3 == 1)}")
