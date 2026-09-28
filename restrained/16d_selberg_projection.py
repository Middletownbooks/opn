#!/usr/bin/env python3
"""
Selberg pilot, final analysis (NOTES_RESTRAINED.md 4g).  It reads the tables of
16c_selberg_tables.c.  For each xi those give: G(xi); W(xi) = sum_{d<xi} omega(d);
and E1(xi) = sum_{d<xi} omega(d) * min(1, h(d) G(xi/d) / G(xi)).  Here omega(p) = 3
for p in M2 (exact, below 1e8), else 1.
  * Upper bound for the count of T' = {primes r in (x,2x] avoiding M2 below 1e8}:
        min over xi of  x/G(xi) + E1(xi)^2     ("sharper weights", |lambda_d| bounded)
        min over xi of  x/G(xi) + W(xi)^2      ("crude weights",  |lambda_d| <= 1)
  * "loss" = bound / (0.113 x / ln x).  0.113 x / ln x is the measured count of the
    static set with S = M2 below 3e6.  It is exact to 0.5% at 1e9 and 1e10 (static
    runs of 13_sieve.c with Q = 3e6).
  * Projection: ln A_up(z) = ln A(1e12) of the superset run + sum over dyadic (x, 2x]
    of bound/x, and q >= ~K_max/2 with K_max = (c - ln A_up)/ln(1 + 1/z).
  * Sensitivity: the same projection, if the bound were exactly L times 0.113 x/ln x.
Floating point throughout: a pilot, not a proof.
Run:  python3 16d_selberg_projection.py TABLES
"""
import sys, math
tab = [tuple(map(float, l.split())) for l in open(sys.argv[1])]
def bound(x, sharp):
    return min((x / G + (E1 if sharp else W) ** 2, t) for t, G, W, E1 in tab if t * t < x)
c = math.log(2 / (1.5 * (1 + 1 / 6e6))); LNA0 = 0.0503326399823567378172
print(f"{'x':>8} {'loss, crude':>12} {'loss, sharper':>14} {'xi':>10}")
for e in range(10, 21):
    x = 10.0 ** e; b0 = bound(x, 0)[0]; b1, t = bound(x, 1); h = 0.113 * x / math.log(x)
    print(f"{x:8.0e} {b0 / h:12.2f} {b1 / h:14.2f} {t:10.3g}")
def project(inc):
    lnA, x, best = LNA0, 1e12, (0.0, 0.0)
    while x < 1e300:
        lnA += inc(x); z = 2 * x
        if lnA >= c: break
        q = (c - lnA) / math.log1p(1 / z) / 2
        if q > best[0]: best = (q, z)
        x = z
    return best
for sharp in (0, 1):
    q, z = project(lambda x: bound(x, sharp)[0] / x)
    print(f"{'sharper' if sharp else 'crude'} weights: projected q >= ~{q:.2e} (best z ~ {z:.2e})")
print("sensitivity (bound = L * 0.113 x/ln x):")
for L in (10, 8, 6, 5, 4, 3, 2):
    q, z = project(lambda x: L * 0.113 / math.log(x))
    print(f"   L = {L:2d}: q >= ~{q:.2e}  (z ~ {z:.2e})")
