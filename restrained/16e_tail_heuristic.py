#!/usr/bin/env python3
"""
HEURISTIC (not a proof): does the survivors' total abundancy converge below the
section-4 threshold?  (NOTES_RESTRAINED.md 4g, addendum.)

It reads the exact Algorithm-1 checkpoints (exact below 2^35 ~ 3.44e10) and prints
the local survival rate on consecutive ranges.  It fits f(r) ~ C (ln r)^-alpha,
integrates the implied tail of sum 1/r over survivors beyond 3.4e10, and compares
ln A(infinity) with c = ln(4/3) - ln(1 + 1/6e6).  If a PROVEN upper bound on that tail
were within the printed factor of this estimate, then ln A(z) < c for every z.
K_max(z) would then grow without bound, so N would need infinitely many ordinary
primes: no restrained odd perfect number, given the rest of the paper's section 4.
Run:  python3 16e_tail_heuristic.py
"""
import math, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
cp = {}
for l in open(os.path.join(HERE, "runs", "13_z_Q2e35_checkpoints.txt")):
    m = re.match(r"CP x=(\d+) k=(\d+) lnA=(\S+)", l)
    if m: cp[int(m[1])] = (int(m[2]), float(m[3]))
def li(x):
    a, n = 2.0, 400000; la, lb = math.log(a), math.log(x); s = 0.0
    for i in range(n):
        t = la + (i + 0.5) * (lb - la) / n; s += math.exp(t) / t
    return s * (lb - la) / n
pts = [1_000_000_000, 4_000_000_000, 10_000_000_000, 20_000_000_000, 34_000_000_000]
print("local survival rate (survivors / primes), exact ranges:")
rates = []
for a, b in zip(pts, pts[1:]):
    f = (cp[b][0] - cp[a][0]) / (li(b) - li(a)); rates.append((math.log(math.sqrt(a * b)), f))
    print(f"   ({a:.1e}, {b:.1e}]: {100 * f:.2f}%")
(u1, f1), (u2, f2) = rates[0], rates[-1]
alpha = math.log(f1 / f2) / math.log(u2 / u1); C = f1 * u1 ** alpha
u0 = math.log(3.4e10); tail = C * u0 ** (-alpha) / alpha
lnA34 = cp[34_000_000_000][1]; c = math.log(2 / (1.5 * (1 + 1 / 6e6)))
print(f"fit f(r) ~ {C:.3f} (ln r)^-{alpha:.2f}")
print(f"exact ln A(3.4e10) = {lnA34:.4f}; heuristic tail = {tail:.4f}; heuristic ln A(inf) ~ {lnA34 + tail:.3f}; c = {c:.4f}")
print(f"a proof needs a tail bound within a factor {(c - lnA34) / tail:.2f} of the heuristic")
