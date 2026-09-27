#!/usr/bin/env python3
"""
Exact reference implementation of Ochem-Zelinsky's Algorithm 1
(sources/ochem_zelinsky_algorithm1.txt), in bare CPython, for small ranges.

It is the independent third leg for validating restrained/13_sieve.c and for
reading the released sources/loopless.cpp (which is exact for r < 2^32).

Algorithm 1, restated.  M1 starts as the primes 5 <= r < 3e6, and M2 as the primes
7 <= r < 3e6 with r = 1 (mod 3).  For each prime r > 3e6 in increasing order:
  * if no prime of M2 divides r^2+r+1, then r survives (k += 1, A *= r/(r-1));
  * else r joins M1; and if r = 1 (mod 3) and (r = 3 mod 4, or some prime factor
    of r+1 other than 2 and 3 lies in M1), then r joins M2.

Implementation (no factoring):
  * q in M2 divides r^2+r+1  <=>  r = rho or q-1-rho (mod q), where rho is a
    primitive cube root of unity mod q.  So each q, once in M2, marks its hits
    r > q in a byte array, and a prime r is tested by one lookup.
  * The M1 test for r = 1 (mod 12) reduces to a lookup.  Let s = (r+1)/2; it is
    = 1 (mod 6), so its prime factors are >= 5.  If s has a prime factor below 3e6,
    that factor is in M1.  Otherwise, since s < 9e12, s is itself a prime > 3e6,
    and s is in M1 iff s did not survive.  So:  r joins M2  <=>  s is not a survivor.
    (For r = 3 mod 4 the test is true outright.)

Output: the same progress lines as loopless.cpp ("k: .. | r: .. | A: ..", every
10000 survivors), then a summary line.

Run:  python3 12_algorithm1_reference.py R [Q]  (all primes r <= R; with Q, a prime
      q of M2 excludes r only if q < Q -- the restricted mode of 13_sieve.c)
"""
import sys, math

R = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
Q = int(sys.argv[2]) if len(sys.argv) > 2 else R + 1
LO = 3_000_000

isp = bytearray([1]) * (R + 1); isp[:2] = b"\0\0"
for i in range(2, math.isqrt(R) + 1):
    if isp[i]: isp[i*i::i] = bytearray(len(range(i*i, R + 1, i)))

hit = bytearray(R + 1)                 # hit[r] = 1: some q in M2, q < r, divides r^2+r+1
def cube_root(q):
    e = (q - 1) // 3
    for g in range(2, q):
        rho = pow(g, e, q)
        if rho != 1: return rho
def add_M2(q):
    if q >= Q: return
    rho = cube_root(q)
    for c in (rho, q - 1 - rho):
        t = c + q                      # the first hit above q
        if t <= R: hit[t::q] = b"\1" * len(range(t, R + 1, q))

for q in range(7, LO):
    if isp[q] and q % 3 == 1: add_M2(q)

surv = bytearray(R // 2 + 2)           # survivors, indexed by value
k = 0; lnA = []                        # lnA terms, summed with fsum at print time
acc = 0.0; comp = 0.0                  # Neumaier running sum of log1p(1/(r-1))
last = 0
for r in range(LO + 1, R + 1):
    if not isp[r]: continue
    if not hit[r]:
        k += 1
        term = math.log1p(1.0 / (r - 1))
        t = acc + term
        comp += (acc - t) + term if abs(acc) >= abs(term) else (term - t) + acc
        acc = t
        if r <= R // 2 + 1: surv[r] = 1
        if k % 10000 == 0:
            print(f"k: {k:<8d} | r: {r:<10d} | A: {math.exp(acc + comp):.12f}")
        last = r
    else:
        if r % 3 == 1:
            if r % 4 == 3 or not surv[(r + 1) // 2]:
                add_M2(r)
print(f"SUMMARY R={R} Q={Q} k={k} lnA={acc + comp:.17g} A={math.exp(acc + comp):.15f} last_survivor={last}")
