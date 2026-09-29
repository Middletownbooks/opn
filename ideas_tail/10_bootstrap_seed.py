#!/usr/bin/env python3
"""
ideas_tail/10 -- pilot for Idea 4 (secondary question (c)): is there a SEED for a
bootstrap proving that M2 keeps a positive share of the primes = 1 (mod 3)?

Among primes = 1 (mod 3) in (x, 2x], M2 contains every prime that is neither a survivor
nor a special candidate.  So  share(M2) >= 1 - theta_S - theta_Sp,  where theta_S and
theta_Sp are upper bounds, relative to the prime count, for
  * survivors: Selberg count bound x/G(xi) + 2 E1^2 from restrained/16c's tables (M2 exact
    below 1e8); the class r = 1 (mod 3) halves main term and prime count alike;
  * special candidates: r = 1 (mod 12), r prime, (r+1)/2 free of primes in [5, 3e6).
    Selberg on n = 1 (mod 12) in (x, 2x]: omega(p) = 2 (n = 0, -1) for 5 <= p < 3e6,
    omega(p) = 1 otherwise; |R_d| <= omega(d); remainder <= (sum_{d<xi} omega(d))^2 (crude).
Compared with the prime count (x/2)/ln x of primes = 1 mod 3 (li is close enough for a pilot).
Floating point: a pilot, not a proof.  Run:  python3 10_bootstrap_seed.py
"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
tab = [tuple(map(float, l.split())) for l in
       open(os.path.join(HERE, "..", "restrained", "runs", "16c_selberg_tables_M2_1e8.txt"))]
XI = 2_000_000
spf = list(range(XI + 1))
for i in range(2, math.isqrt(XI) + 1):
    if spf[i] == i:
        for j in range(i * i, XI + 1, i):
            if spf[j] == j: spf[j] = i
g = [0.0] * (XI + 1); om = [0] * (XI + 1); g[1] = 1.0; om[1] = 1
for d in range(2, XI + 1):
    p = spf[d]; m = d // p
    if p < 5 or m % p == 0 or om[m] == 0: continue
    w = 2 if p < 3_000_000 else 1
    g[d] = g[m] * w / (p - w); om[d] = om[m] * w
G = [0.0] * (XI + 1); W = [0] * (XI + 1)
for d in range(1, XI + 1): G[d] = G[d - 1] + g[d]; W[d] = W[d - 1] + om[d]
h = [0.0] * (XI + 1); h[1] = 1.0                      # h(d) = prod (1 + g(p))
for d in range(2, XI + 1):
    p = spf[d]; m = d // p
    if om[d]: h[d] = h[m] * (1 + om[d] // om[m] / (p - om[d] // om[m]))
E1c = {}
def E1(xi):                                            # sum omega(d) min(1, h(d) G(xi/d)/G(xi))
    if xi not in E1c:
        E1c[xi] = sum(om[d] * min(1.0, h[d] * G[xi // d] / G[xi]) for d in range(1, xi) if om[d])
    return E1c[xi]
XIS = [int(10 ** (k / 10)) for k in range(30, 64)]
def sp_bound(x, sharp=True):
    X = x / 12
    return min(X / G[xi] + (E1(xi) if sharp else W[xi]) ** 2 for xi in XIS if xi <= XI)
def s_bound(x):
    return min(x / Gs + 2 * (1 + E1 * E1) for t, Gs, Ww, E1 in tab if t < x)
print("theta_Sp with the sharper weights |lambda_d| <= min(1, h(d) G(xi/d)/G(xi)):")
print(f"{'x':>8} {'theta_S':>8} {'theta_Sp':>9} {'M2 share >=':>12}")
for e in (10, 12, 14, 16, 18):
    x = 10.0 ** e; P = x / math.log(x)                # primes in (x, 2x], all classes
    tS = s_bound(x) / P; tSp = sp_bound(x) / (P / 2)
    print(f"{x:8.0e} {tS:8.3f} {tSp:9.3f} {1 - tS - tSp:12.3f}")
