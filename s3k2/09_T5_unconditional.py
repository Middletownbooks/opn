#!/usr/bin/env python3
"""
|T| = 5 at k = 2 :  an UNCONDITIONAL two-sided fixed-support test.

SETTING (section 3, k = 2, sub-case |T| = 5).  3 is ordinary, 3^2 || N, and the
primes = 1 (mod 3) dividing N are exactly T = {a_1, a_2, p, n_1, n_2} with
a_1, a_2 ordinary, p special, n_1, n_2 notable.  Every other prime of N is an
ordinary prime = 2 (mod 3); call that set U.  Splitting sigma(N)/N = 2:

        PROD_T * PROD_U = 18/13,     PROD_U = prod_{x in U} (1 + 1/x + 1/x^2).

LOWER BOUND on PROD_T  (kills small T):
   ordinary exponent is exactly 2, notable q >= 4 even, special e >= 1 with
   p = 1 (mod 12); each sigma(t^e)/t^e increases with e, so minimise over the
   role assignment.  If that minimum exceeds 18/13 the set is impossible.

UPPER BOUND on PROD_T * PROD_U  (kills large T):
   PROD_T < g(T) = prod_{t in T} t/(t-1), and U is contained in
        Sm(T) = { x prime, x = 2 (mod 3), x^2+x+1 T-smooth }
   because every prime factor of x^2+x+1 is = 1 (mod 3) and divides N.
   So PROD_U <= h(T) = prod_{x in Sm(T), x>=5} (1 + 1/x + 1/x^2).
   If g(T) * h(T) <= 18/13 the set is impossible.

MAKING h(T) RIGOROUS.  Sm(T) is found exactly for x^2+x+1 <= Y by running over
all T-smooth M <= Y and testing whether 4M-3 is a square.  The remaining terms
are bounded unconditionally: if x^2+x+1 = M > Y then x > sqrt(M) - 1, distinct
x give distinct M, and for any 0 < eps < 1/2

   sum_{M T-smooth, M > Y} M^{-1/2} <= Y^{-eps} * prod_{t in T} 1/(1 - t^{eps-1/2})

since M > Y implies 1 <= (M/Y)^eps and the full sum factors as an Euler product.
With Y = 10^24 this tail is below 10^-6 for every T considered, so

   h(T) <= (head product) * exp(1.000001 * tail)

is a genuine upper bound.  No Thue-Mahler input, no completeness assumption.
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
        if s % 12 != 1: continue                 # special needs p = 1 (mod 12)
        rest = [T[j] for j in range(5) if j != i]
        for nb in combinations(range(4), 2):
            od = [rest[j] for j in range(4) if j not in nb]
            v = fs(s)*fn(rest[nb[0]])*fn(rest[nb[1]])*fo(od[0])*fo(od[1])
            if best is None or v < best: best = v
    return best

def smooth_x(T):
    """exact Sm(T) for x^2+x+1 <= Y, excluding x = 2 (N is odd)."""
    out = []
    L = list(T)
    def rec(i, m):
        if i == 5:
            d = 4*m - 3
            r = math.isqrt(d)
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
    """upper bound for sum_{x in Sm(T), x^2+x+1 > Y} 1/x."""
    best = None
    lnY = math.log(Y)
    for k in range(1, 100):
        eps = 0.5 * k / 100.0
        if eps >= 0.5: break
        v = -eps * lnY
        for t in T:
            v -= math.log(1.0 - t ** (eps - 0.5))
        if best is None or v < best: best = v
    return math.exp(best) / (1 - Y ** -0.5)

POOL = [p for p in range(7, TMAX) if isprime(p) and p % 3 == 1]
print(f"pool: primes = 1 (mod 3) in [7,{TMAX}) : {len(POOL)}  -> {POOL}")
print(f"exact smoothness search bound Y = 10^{len(str(Y))-1}  (x up to ~10^12)")
print()

dead_low = []; dead_up = 0; alive = []; margins = []
maxtail = 0.0
for rest in combinations([p for p in POOL if p != 13], 4):
    T = tuple(sorted((13,) + rest))
    m = min_prod_T(T)
    if m is None:
        dead_low.append((T, None)); continue
    if m > TARGET:
        dead_low.append((T, m)); continue
    S = smooth_x(T)
    tb = tail_bound(T); maxtail = max(maxtail, tb)
    g = 1.0
    for t in T: g *= t / (t - 1.0)
    h = 1.0
    for x in S: h *= 1.0 + 1.0/x + 1.0/x**2
    h *= math.exp(1.000001 * tb)
    gh = g * h
    if gh <= TF:
        dead_up += 1; margins.append((gh, T, S))
    else:
        alive.append((gh, T, S, g, h))

tot = len(dead_low) + dead_up + len(alive)
print("=" * 78)
print(f"5-subsets T of the pool with 13 in T : {tot}")
print(f"   dead by the LOWER bound (min PROD_T > 18/13)      : {len(dead_low)}")
print(f"   dead by the UPPER bound (g*h <= 18/13)            : {dead_up}")
print(f"   SURVIVING                                         : {len(alive)}")
print(f"   largest tail bound used anywhere                  : {maxtail:.3e}")
print("=" * 78)
print()
if dead_low:
    print("killed by the lower bound:")
    for T, m in dead_low:
        print(f"   T = {str(list(T)):26s} min PROD_T = "
              + ("no admissible special" if m is None else f"{float(m):.9f}"))
    print()
if alive:
    print("SURVIVING SETS (these need a different argument):")
    for gh, T, S, g, h in sorted(alive, reverse=True):
        print(f"   T = {str(list(T)):26s} g = {g:.6f}  h = {h:.6f}  g*h = {gh:.6f}")
        print(f"        Sm(T) = {S}")
else:
    print("NO SURVIVORS: every such T is impossible.")
print()
margins.sort(reverse=True)
print("closest calls among the sets killed by the upper bound:")
for gh, T, S in margins[:10]:
    print(f"   T = {str(list(T)):26s} g*h = {gh:.9f}  (needs > {TF:.9f})   Sm = {S}")
