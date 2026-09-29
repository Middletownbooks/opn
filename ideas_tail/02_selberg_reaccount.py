#!/usr/bin/env python3
"""
ideas_tail/02 -- the Selberg pilot of restrained/16c-16d, re-accounted.

Two bookkeeping changes, both sound (RESULT.md, Idea 3 and section 2):

 (i) WEIGHTED main term.  16d bounds sum_{r in S n (x,2x]} 1/r by (count bound)/x,
     i.e. by 1/G(xi) + E1^2/x.  Sieving with weights a_n = x/n on (x, rho*x] instead
     gives   sum 1/r <= ln(rho)/G(xi) + 2 (1 + E1(xi)^2)/x
     (the remainder per class is at most 2 max a_n = 2; RESULT.md, Lemma S).  For rho = 2 the main
     term drops by the factor ln 2 = 0.693.

 (ii) GREEDY FILL instead of q ~ K_max/2 (LEMMA G, RESULT.md).  With intervals
     I_j = (y_j, y_{j+1}], V_j >= sum over possible ordinary primes in I_j of
     ln(r/(r-1)), and w_j = ln(1 + 1/y_j):
        |O| >= |T| + sum_{j<J} V_j / w_j + (c - Lambda_0 - sum_{j<J} V_j) / w_J
     for every J with Lambda_0 + sum_{j<J} V_j <= c.

Input: restrained/runs/16c_selberg_tables_M2_1e8.txt (xi, G, W, E1), computed with the
exact M2 below 1e8.  Floating point: like 16d this is a PILOT, not a proof.
It also prints the same projection for a smaller base Lambda_0, to show how much a
look-ahead at the base (ideas_tail/04) would be worth.
Run:  python3 02_selberg_reaccount.py [rho]
"""
import sys, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
tab = [tuple(map(float, l.split())) for l in
       open(os.path.join(HERE, "..", "restrained", "runs", "16c_selberg_tables_M2_1e8.txt"))]
RHO = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
c = math.log(4 / 3) - math.log1p(1 / 6e6)
T, LNA0 = 2_670_032_132, 0.0503326399823567378172

def V(x, rho, weighted=True):
    """upper bound for sum of ln(r/(r-1)) over possible ordinary r in (x, rho x]"""
    if not weighted:                                       # 16d exactly as run: (x/G + E1^2)/x
        return min(1 / G + E1 * E1 / x for t, G, W, E1 in tab if t * t < x)
    best = min(math.log(rho) / G + 2 * (1 + E1 * E1) / x for t, G, W, E1 in tab if t < x)
    return best * (1 + 1 / x)                              # ln(r/(r-1)) <= (1/r)(1 + 1/(r-1))

def greedy(lna0, vfun, rho, y0=1e12):
    """best lower bound on |O| from LEMMA G, and the z where it is attained"""
    lam, y, acc, best = lna0, y0, float(T), (0.0, y0)
    while y < 1e300:
        w = math.log1p(1 / y)
        if lam <= c:
            cand = acc + (c - lam) / w
            if cand > best[0]: best = (cand, y)
        v = vfun(y, rho)
        if lam + v > c: break
        lam += v; acc += v / w; y *= rho
    return best

def old_style(lna0, vfun, rho, y0=1e12):
    """16d's count: q ~ K_max/2 = (c - ln A_up(z))/ln(1+1/z)/2, maximised over z"""
    lam, y, best = lna0, y0, (0.0, y0)
    while y < 1e300:
        lam += vfun(y, rho); y *= rho
        if lam >= c: break
        best = max(best, ((c - lam) / math.log1p(1 / y), y))
    return best

print(f"rho = {RHO};  c = {c:.6f}")
print("per-interval loss of the weighted bound vs the trivial prime sum ln(rho)/ln x:")
for e in (12, 14, 16, 18, 20):
    x = 10.0 ** e
    print(f"   x = 1e{e}:  V/trivial = {V(x, RHO) / (math.log(RHO) / math.log(x)):.3f}")
o16d = old_style(LNA0, lambda y, r: V(y, 2.0, weighted=False), 2.0)
print(f"\n16d as run (unweighted, K_max/2):   q ~ {o16d[0] / 2:.3e} at z ~ {o16d[1]:.2e}")
oW = old_style(LNA0, V, RHO)
print(f"weighted only (K_max/2):            q ~ {oW[0] / 2:.3e} at z ~ {oW[1]:.2e}")
g = greedy(LNA0, V, RHO)
print(f"weighted + greedy fill (Lemma G):   q ~ {g[0] / 2:.3e} at z ~ {g[1]:.2e}")
triv = greedy(LNA0, lambda y, r: math.log(math.log(r * y) / math.log(y)) + 1 / y, RHO)
print(f"no sieve at all, same Lemma G:      q ~ {triv[0] / 2:.3e} at z ~ {triv[1]:.2e}  (cf. 01: 2.25e13)")
print("\nsensitivity to the base Lambda_0 = ln A(1e12) (what a look-ahead at the base buys):")
for lna0 in (0.0503, 0.03, 0.02, 0.01, 0.005, 0.001):
    g = greedy(lna0, V, RHO)
    tv = greedy(lna0, lambda y, r: math.log(math.log(r * y) / math.log(y)) + 1 / y, RHO)
    print(f"   Lambda_0 = {lna0:.4f}:  Selberg q ~ {g[0] / 2:.2e} (z ~ {g[1]:.1e});  no-sieve q ~ {tv[0] / 2:.2e}")
