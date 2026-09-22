#!/usr/bin/env python3
"""How much abundancy room section 3 has at k = 2, as a function of |T|."""
from fractions import Fraction as Fr
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
P1=[p for p in range(5,200) if isprime(p) and p%3==1]
print("T = the primes = 1 (mod 3) dividing N.  13 is always in T (sigma(3^2)=13).")
print("|T| <= 2 (ordinary, by the 3-budget) + (k+1) (special + k notables).")
print("   k = 1: |T| <= 4      k = 2: |T| <= 5")
print()
print("The component 3^2 contributes sigma(9)/9 = 13/9 exactly.  Bounding the")
print("T-primes by t/(t-1) and taking the smallest admissible T:")
print()
print(f"{'|T|':>4} {'smallest T':>28} {'13/9 * prod t/(t-1)':>22} {'room left to 2':>16}")
for n in (3,4,5,6):
    T=P1[:n]
    if 13 not in T: T=sorted(set(T[:n-1])|{13})[:n]
    v=Fr(13,9)
    for t in T: v*=Fr(t,t-1)
    room = Fr(2)/v
    flag = "  <-- k=1 ceiling" if n==4 else ("  <-- k=2 ceiling" if n==5 else "")
    print(f"{n:>4} {str(T):>28} {float(v):>22.6f} {float(room):>16.6f}{flag}")
print()
print("""READING.

  |T| = 4 (the k = 1 ceiling): the bound is 1.9912, leaving a factor 1.0044 for
  every ordinary prime = 2 (mod 3).  Tight, but nonzero -- which is why their
  section 3 could be finished once the factor tree had pinned T down.

  |T| = 5 (only possible at k >= 2): the bound is already 2.0466 > 2 BEFORE a
  single ordinary prime = 2 (mod 3) is counted.  No abundancy argument of this
  shape can work in that sub-case.

So section 3 at k = 2 splits cleanly:
  * |T| <= 4  -- the k = 1 situation, plausibly reachable by the fixed-support
                 machinery that closed section 2, now over quartets;
  * |T| = 5   -- all of p, n_1, n_2 congruent to 1 mod 3 AND two ordinary
                 primes = 1 mod 3.  Abundancy is exhausted; a different
                 obstruction is required.""")
