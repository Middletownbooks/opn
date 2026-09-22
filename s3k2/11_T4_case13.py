#!/usr/bin/env python3
"""
Section 3 at k = 2, sub-case |T| = 4 with |A| = 1 :  the "one ordinary, three
big" split, in which W = {p,n_1,n_2} n {2 mod 3} is EMPTY.

Here T = {a, p, n_1, n_2} with a ordinary, so the prime divisors of N are again
exactly {3} u T u U and the same exact identity holds:

        PROD_T * PROD_U = 18/13 ,     U  contained in  Sm(T).

Only the role profile changes: one ordinary, one special, two notable, and the
3-budget now reads

        1 (from a) + v_3(e+1) + v_3(q_1+1) + v_3(q_2+1) = 2,

so EXACTLY ONE of the three big components carries one extra factor 3, and the
other two carry none.  That sharpens the exponent minima:

    carries the 3      special : e = 5 (mod 12)  -> e >= 5
                       notable : q = 2 (mod 3) even -> q >= 8
    carries none       special : e = 1 (mod 4), e != 2 (mod 3) -> e >= 1
                       notable : q even >= 4, q != 2 (mod 3)   -> q >= 4

and the special prime is = 1 (mod 12) when it carries none, = 5 (mod 12) when
it carries the 3 -- but every element of T is = 1 (mod 3), so the special is
always = 1 (mod 12) here and therefore CANNOT be the component carrying the 3
(e = 5 mod 12 forces p = 2 mod 3).  Hence the extra 3 sits on a notable:
one notable has q >= 8, the other q >= 4.

Tests and bounds are exactly those of 09/10; see that file for the tail lemma.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
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

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
Y    = 10**24
TARGET = F(18, 13); TF = 18/13

def geom(t, k):                 # 1 + 1/t + ... + 1/t^k
    return F(sum(t**i for i in range(k+1)), t**k)

f_spec1 = lambda t: geom(t, 1)      # special, e >= 1
f_ord   = lambda t: geom(t, 2)      # ordinary, exponent exactly 2
f_not4  = lambda t: geom(t, 4)      # notable, q >= 4
f_not8  = lambda t: geom(t, 8)      # notable carrying the extra 3, q >= 8

def min_prod_T(T):
    """one ordinary, one special (= 1 mod 12), two notable one of which has q>=8."""
    best = None
    for perm in permutations(range(4)):
        a, s, n1, n2 = (T[i] for i in perm)
        if s % 12 != 1: continue
        v = f_ord(a) * f_spec1(s) * f_not8(n1) * f_not4(n2)
        if best is None or v < best: best = v
    return best

def smooth_x(T):
    out = []; L = list(T)
    def rec(i, m):
        if i == len(L):
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
for rest in combinations([p for p in POOL if p != 13], 3):
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
    R = TARGET/m
    if len(S) < 4: n3 += 1; continue
    pr = F(1)
    for x in S[-4:]: pr *= f_ord(x)
    if pr > R: n3 += 1; continue
    alive.append((T, S, float(R), float(pr)))

tot = n1+n2+n3+len(alive)
print(f"|T| = 4, |A| = 1  (W empty).  pool = primes = 1 mod 3 in [7,{TMAX}): {len(POOL)}")
print(f"4-subsets T with 13 in T : {tot}")
print()
print(f"  TEST 1  min PROD_T > 18/13        (unconditional) : {n1:6d}")
print(f"  TEST 2  g*h <= 18/13              (unconditional) : {n2:6d}")
print(f"          eliminated with no unproved input         : {n1+n2:6d}"
      f"   ({100.0*(n1+n2)/tot:.1f}%)")
print(f"  TEST 3  omega>=10 + Sm(T) complete (CONDITIONAL)  : {n3:6d}")
print(f"          still alive                               : {len(alive):6d}")
print()
for T, S, R, pr in alive[:25]:
    print(f"   T = {str(list(T)):22s} Sm = {str(S)[:36]:36s} R = {R:.6f}  "
          f"four-largest = {pr:.6f}")
