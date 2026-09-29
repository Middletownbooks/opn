#!/usr/bin/env python3
"""
ideas_tail/01 -- the "greedy fill" count, and what it gives with NO sieve beyond 1e12.

The brief's count stops at a fixed z and uses q ~ K_max(z)/2, where
K_max(z) = (c - ln A(z)) / ln(1 + 1/z).  But the survivor set may be replaced by ANY
set of primes U containing every possible ordinary prime <= z, and then

  LEMMA G0 (proved in RESULT.md, Idea 1).  If U contains O n (3e6, z] and
  Lambda(U) = sum_{u in U} ln(u/(u-1)) < c, then  |O| >= |U| + K,
  K = (c - Lambda(U)) / ln(1 + 1/z) > 0.

Take U = T u {all primes in (1e12, z]}, where T is the Q = 2^35 superset run's
survivor set below 1e12 (|T| = 2,670,032,132, ln A <= 0.0503326399823567378172).
|U| + K is increasing in z while Lambda < c (d/dz = c - Lambda(z) > 0), so push z up
to where Lambda(z) reaches c.  No computation beyond the existing run is needed.

Rigour.  Explicit prime estimates, used as black boxes (see RESULT.md for sources and
my confidence in them):
  (RS-a) sum_{p<=x} 1/p <  lnln x + B + 1/(2 ln^2 x)   for x >= 286
  (RS-b) sum_{p<=x} 1/p >  lnln x + B - 1/(2 ln^2 x)   for x > 1
  (RS-c) pi(x) > x / ln x                                for x >= 17
  pi(1e12) = 37,607,912,018 (standard table value).
And sum_{p > 1e12} (ln(p/(p-1)) - 1/p) < sum_{n > 1e12} 1/(n(n-1)) = 1/1e12.
Everything below is done in Decimal with 50 digits; margins dwarf rounding.
Run:  python3 01_greedy_fill_trivial.py
"""
from decimal import Decimal as D, getcontext
getcontext().prec = 50

T_COUNT = 2_670_032_132
LNA0 = D("0.0503326399823567378172") + D("1e-15")          # padded, as in restrained/14
Z0 = D(10) ** 12
PI_Z0 = 37_607_912_018
c = (D(4) / D(3)).ln() - (1 + D(1) / D(6_000_000)).ln()      # the brief's c (conservative)

def lnln(x): return x.ln().ln()
def tail_upper(z):
    """upper bound for sum_{1e12 < p <= z} ln(p/(p-1))"""
    return (lnln(z) - lnln(Z0) + 1 / (2 * z.ln() ** 2) + 1 / (2 * Z0.ln() ** 2)
            + D(1) / Z0)

def bound_at(z):
    lam = LNA0 + tail_upper(z)
    if lam >= c: return None
    U = T_COUNT + int(z / z.ln()) - PI_Z0                   # |U| lower bound (RS-c)
    K = (c - lam) / (1 + 1 / z).ln()
    O = U + int(K)                                           # |O| > U + K, so |O| >= U + floor(K) + 1
    q = (O + 1 + 2) // 2 - 2                                 # q >= omega/2 - 2, omega = |O| + 2
    return lam, U, K, O + 1, q

print(f"c = {c:.12f};  ln A(1e12) <= {LNA0:.12f}")
print(f"{'z':>10} {'Lambda(z) <=':>14} {'|U| >=':>18} {'K >':>18} {'q >=':>18}")
best = None
z = Z0
while True:
    r = bound_at(z)
    if r is None: break
    lam, U, K, O, q = r
    print(f"{float(z):10.3e} {float(lam):14.6f} {U:18,d} {int(K):18,d} {q:18,d}")
    if best is None or q > best[1]: best = (z, q)
    z *= D(2)
# refine the optimum by bisection on ln z
lo, hi = best[0], best[0] * 2
for _ in range(200):
    mid = (lo * hi).sqrt()
    if bound_at(mid) is None: hi = mid
    else: lo = mid
r = bound_at(lo)
print(f"\noptimum z ~ {float(lo):.4e}: Lambda <= {float(r[0]):.9f} (< c), "
      f"|O| >= {r[3]:,d}, so q >= {r[4]:,d}")
# for comparison: the brief's count at z = 1e12, K_max/2 style
K12 = (c - LNA0) / (1 + 1 / Z0).ln()
print(f"brief-style at z = 1e12: k + K_max = {T_COUNT + int(K12):,d}, q >= ~{(T_COUNT + int(K12)) // 2:,d}")
