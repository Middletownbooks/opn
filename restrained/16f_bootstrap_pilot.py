#!/usr/bin/env python3
"""
Bootstrap pilot (NOTES_RESTRAINED.md 4h): can an upper-bound sieve bound the
survivors' tail within the factor (about 3.1) that 16e says a full proof needs?

In the exactly known range (true survivors below 3.44e10, exact M2 below 1e8), it
compares the best Selberg bound from the 16c tables with the TRUE survivor counts on
dyadic ranges.  A bootstrap cannot do better than this, because here M2 is known
exactly rather than bounded.  It also prints an IDEALISED bound x/G(sqrt x), with the
error term ignored and the maximal level; no valid Selberg bound beats it.  It prints
the asymptotic Selberg constant 2^k Gamma(k+1), and the overshoot that would be
allowed if brute force reached z0 (from 16e's heuristic tail).
Run:  python3 16f_bootstrap_pilot.py
"""
import math, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
cp = {}
for l in open(os.path.join(HERE, "runs", "13_z_Q2e35_checkpoints.txt")):
    m = re.match(r"CP x=(\d+) k=(\d+) lnA=(\S+)", l)
    if m: cp[int(m[1])] = (int(m[2]), float(m[3]))
tab = [tuple(map(float, l.split())) for l in open(os.path.join(HERE, "runs", "16c_selberg_tables_M2_1e8.txt"))]
def bound(x): return min((x / G + E1 * E1, t) for t, G, W, E1 in tab if t * t < x)
def G_at(y): return max((t, G) for t, G, W, E1 in tab if t <= y)[1]
print(f"{'range':>24} {'true':>12} {'bound':>13} {'bound/true':>11} {'ideal/true':>11}")
for a in (1_000_000_000, 2_000_000_000, 4_000_000_000, 8_000_000_000, 16_000_000_000):
    t = cp[2 * a][0] - cp[a][0]; B, _ = bound(float(a))
    print(f"({a:.1e}, {2*a:.1e}] {t:12,d} {B:13,.0f} {B / t:11.2f} {a / G_at(math.sqrt(2 * a)) / t:11.2f}")
for k in (1.0, 1.9): print(f"Selberg asymptotic constant 2^k Gamma(k+1), k = {k}: {2 ** k * math.gamma(k + 1):.2f}")
C, al, c = 1.051, 0.86, math.log(2 / (1.5 * (1 + 1 / 6e6)))
for z0 in (3.4e10, 1e12, 1e15, 1e20, 1e28):
    u = math.log(z0); tail = C * u ** (-al) / al
    la = 0.0412 + (C / al) * (math.log(3.4e10) ** (-al) - u ** (-al))
    print(f"brute force to z0 = {z0:.0e}: heuristic tail {tail:.4f}, allowed overshoot {(c - la) / tail:.2f}")
