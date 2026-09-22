#!/usr/bin/env python3
"""
|T| = 5 at k = 2 : the three tests, tallied separately by what they assume.

  TEST 1 (unconditional)   min PROD_T > 18/13.
  TEST 2 (unconditional)   g(T) * h(T) <= 18/13, with the rigorous tail bound.
  TEST 3 (conditional)     omega(N) >= 10 (Nielsen 2015) gives |U| >= 4; U is
                           contained in Sm(T) and PROD_U <= R(T) = (18/13)/min
                           PROD_T, so the four LARGEST members of Sm(T) must
                           already fit inside R(T).  This one assumes Sm(T) has
                           no member beyond the search bound Y, i.e. that the
                           Thue-Mahler equation x^2+x+1 = T-smooth has no large
                           solution.  Sm(T) is finite, but I have not proved the
                           search exhausts it -- so test 3 is flagged separate.

See 09_T5_unconditional.py for the derivations of the bounds.
"""
from fractions import Fraction as F
from itertools import combinations
import math, sys

def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
Y    = 10**24
TARGET = F(18, 13); TF = 18/13
fs = lambda t: F(t+1, t)
fo = lambda t: F(t*t+t+1, t*t)
fn = lambda t: F(t**4+t**3+t*t+t+1, t**4)

def min_prod_T(T):
    best = None
    for i, s in enumerate(T):
        if s % 12 != 1: continue
        rest = [T[j] for j in range(5) if j != i]
        for nb in combinations(range(4), 2):
            od = [rest[j] for j in range(4) if j not in nb]
            v = fs(s)*fn(rest[nb[0]])*fn(rest[nb[1]])*fo(od[0])*fo(od[1])
            if best is None or v < best: best = v
    return best

def smooth_x(T):
    out = []; L = list(T)
    def rec(i, m):
        if i == 5:
            d = 4*m - 3; r = math.isqrt(d)
            if r*r == d and r % 2 == 1:
                x = (r-1)//2
                if x >= 5 and x % 3 == 2 and isprime(x): out.append(x)
            return
        v = m
        while v <= Y:
            rec(i+1, v); v *= L[i]
    rec(0, 1)
    return sorted(set(out))

def tail_bound(T):
    best = None; lnY = math.log(Y)
    for k in range(1, 100):
        eps = 0.5*k/100.0
        if eps >= 0.5: break
        v = -eps*lnY
        for t in T: v -= math.log(1.0 - t**(eps-0.5))
        if best is None or v < best: best = v
    return math.exp(best)/(1 - Y**-0.5)

POOL = [p for p in range(7, TMAX) if isprime(p) and p % 3 == 1]
n1 = n2 = n3 = 0; alive = []
for rest in combinations([p for p in POOL if p != 13], 4):
    T = tuple(sorted((13,) + rest))
    m = min_prod_T(T)
    if m is None or m > TARGET: n1 += 1; continue
    S = smooth_x(T)
    g = 1.0
    for t in T: g *= t/(t-1.0)
    h = 1.0
    for x in S: h *= 1.0 + 1.0/x + 1.0/x**2
    h *= math.exp(1.000001*tail_bound(T))
    if g*h <= TF: n2 += 1; continue
    R = TARGET/m                                  # PROD_U <= R
    if len(S) < 4: n3 += 1; continue
    best4 = S[-4:]                                # the four cheapest members
    pr = F(1)
    for x in best4: pr *= fo(x)
    if pr > R: n3 += 1; continue
    alive.append((T, S, float(R), float(pr)))

tot = n1+n2+n3+len(alive)
print(f"pool = primes = 1 (mod 3) in [7,{TMAX}) : {len(POOL)}")
print(f"5-subsets T with 13 in T                : {tot}")
print()
print(f"  TEST 1  min PROD_T > 18/13          (unconditional) : {n1:6d}")
print(f"  TEST 2  g*h <= 18/13                (unconditional) : {n2:6d}")
print(f"          ------------------------------------------- ")
print(f"          eliminated with no unproved input           : {n1+n2:6d}"
      f"   ({100.0*(n1+n2)/tot:.1f}%)")
print()
print(f"  TEST 3  omega>=10 + Sm(T) complete  (CONDITIONAL)   : {n3:6d}")
print(f"          ------------------------------------------- ")
print(f"          still alive after all three tests           : {len(alive):6d}")
print()
if alive:
    for T, S, R, pr in alive[:30]:
        print(f"   T = {str(list(T)):26s} Sm = {str(S)[:40]:40s} R = {R:.6f} "
              f"four-largest product = {pr:.6f}")
else:
    print("   Every |T| = 5 set over this pool is eliminated.")
