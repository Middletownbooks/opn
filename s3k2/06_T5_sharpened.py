#!/usr/bin/env python3
"""
Sharpening the |T| = 5 abundancy test with the congruence conditions.

Extra constraints, all forced in the sub-case |T| = 5 (so p, n_1, n_2 = 1 mod 3):

  * the SPECIAL prime obeys p = 1 (mod 4) as well, hence  p = 1 (mod 12).
  * the 3-budget is fully spent by the two ordinary primes of T, so
        v_3(sigma(p^e)) = v_3(e+1) = 0   ->  e = 1 (mod 4),  e != 2 (mod 3)
        v_3(sigma(n^q)) = v_3(q+1) = 0   ->  q even >= 4,    q != 2 (mod 3)
    i.e. q = 0 or 4 (mod 6).  The minimising exponents e = 1 and q = 4 are
    both still admissible, so the role minima are unchanged -- but the SPECIAL
    role can no longer be given to a prime that is 7 (mod 12).

Role minima (each decreasing in t, minimum at the smallest legal exponent):
    special  e >= 1 :  1 + 1/t
    ordinary e  = 2 :  1 + 1/t + 1/t^2
    notable  q >= 4 :  1 + 1/t + 1/t^2 + 1/t^3 + 1/t^4
"""
from fractions import Fraction as F
from itertools import combinations

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

gs = lambda t: 1.0 + 1.0/t
go = lambda t: 1.0 + 1.0/t + 1.0/t**2
gn = lambda t: 1.0 + 1.0/t + 1.0/t**2 + 1.0/t**3 + 1.0/t**4
fs = lambda t: F(t+1, t)
fo = lambda t: F(t*t+t+1, t*t)
fn = lambda t: F(t**4+t**3+t*t+t+1, t**4)

def min_prod_T(T, exact=False):
    """min over: 1 special (= 1 mod 12), 2 notable, 2 ordinary.  None if no special."""
    S, O, Nn = (fs, fo, fn) if exact else (gs, go, gn)
    best = None
    for i, s in enumerate(T):
        if s % 12 != 1: continue
        rest = [T[j] for j in range(5) if j != i]
        for nb in combinations(range(4), 2):
            od = [rest[j] for j in range(4) if j not in nb]
            v = S(s) * Nn(rest[nb[0]]) * Nn(rest[nb[1]]) * O(od[0]) * O(od[1])
            if best is None or v < best: best = v
    return best

TARGET = F(18, 13); TF = 18/13
P1 = [p for p in range(7, 2000) if isprime(p) and p % 3 == 1]

print("=" * 74)
print("SHARPENED TEST.  |T| = 5, PROD_T * PROD_U = 18/13, PROD_U >= 1.")
print("A set T dies if it admits no role assignment, or if min PROD_T > 18/13.")
print("=" * 74)
print()

POOL = [p for p in P1 if p < 700]
print(f"pool = primes = 1 (mod 3) in [7,700) : {len(POOL)} primes")
no_role = []; killed = []; nsurv = 0; surv_small = []
for rest in combinations([p for p in POOL if p != 13], 4):
    T = tuple(sorted((13,) + rest))
    m = min_prod_T(T)
    if m is None: no_role.append(T); continue
    if m > TF * (1 - 1e-12):                      # near or above: re-test exactly
        me = min_prod_T(T, exact=True)
        if me > TARGET: killed.append((T, me)); continue
        m = float(me)
    nsurv += 1
    if len(surv_small) < 25: surv_small.append((T, m))

n = len(no_role) + len(killed) + nsurv
print(f"5-subsets containing 13                               : {n}")
print(f"   dead: no prime = 1 (mod 12) for the special role   : {len(no_role)}")
print(f"   dead: min PROD_T > 18/13                           : {len(killed)}")
print(f"   surviving                                          : {nsurv}")
print()
print("Killed by abundancy (complete list):")
for T, m in sorted(killed):
    print(f"   T = {str(list(T)):30s} min PROD_T = {float(m):.9f}")
print()
print(f"No-special sets (complete list has {len(no_role)}; first 10):")
for T in sorted(no_role)[:10]:
    print(f"   T = {list(T)}")
print()
print("Smallest surviving sets and the abundancy window left for U:")
print(f"   {'T':30s} {'min PROD_T':>12} {'PROD_U <=':>11} {'every x in U >':>15}")
for T, m in surv_small:
    room = TARGET / min_prod_T(T, exact=True)
    x = 5
    while F(x*x + x + 1, x*x) > room: x += 1
    print(f"   {str(list(T)):30s} {m:>12.9f} {float(room):>11.6f} {x-1:>15}")
