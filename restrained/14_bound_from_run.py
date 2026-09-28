#!/usr/bin/env python3
"""
Turn the checkpoint lines of restrained/13_sieve.c into the section-4 bound.

For each checkpoint x, with k = k(x) survivors and L = ln A(x):
    K_max(x) = the largest K with  3/2 * (1 + 1/6e6) * A * (1 + 1/x)^K < 2,
and the number of ordinary primes is then at least k + K_max + 1
(restrained/10, item 3).  So  omega(N) >= k + K_max + 3, and Lemma 8 gives
    q >= omega/2 - 2,  with q even.

The survivors are a SUPERSET of the possible ordinary primes below x (exact for
x <= Q; see 13_sieve.c), so every bound printed here is valid.  L is padded by
1e-15, which is far above the long-double summation error.

What this does NOT check: the rest of the paper's section 4 is taken as given.
That covers Lemma 8, the ruling-out of every prime 5..3e6 (tree.txt), p > 6e6,
and sigma_{-1}(3^q) < 3/2.  Only Algorithm 1 is recomputed.

Run:  python3 14_bound_from_run.py RUN_OUTPUT
"""
import sys, re
from decimal import Decimal as D, getcontext, ROUND_FLOOR
getcontext().prec = 60
BASE = D(3) / 2 * (1 + D(1) / 6000000)
SLACK = D("1e-15")
NEED = 46_000_000_000

def kmax(x, L):
    A = (L + SLACK).exp()
    Lx = (1 + 1 / D(x)).ln()
    K = int(((2 / (BASE * A)).ln() / Lx).to_integral_value(rounding=ROUND_FLOOR))
    while BASE * A * (1 + 1 / D(x)) ** K >= 2: K -= 1
    while BASE * A * (1 + 1 / D(x)) ** (K + 1) < 2: K += 1
    return K

rows = []
for line in open(sys.argv[1]):
    m = re.match(r"CP x=(\d+) k=(\d+) lnA=(\S+) m2=(\d+) m2big=(\d+)", line)
    if m: rows.append((int(m[1]), int(m[2]), D(m[3]), int(m[5])))
    if line.startswith("SUMMARY"): print(line.strip())
print(f"{'x':>16s} {'k(x)':>14s} {'A(x)':>16s} {'K_max':>16s} {'k+K_max':>16s} {'q >=':>16s}  M2 unused")
first = None
for x, k, L, big in rows:
    K = kmax(x, L); B = k + K
    # q >= omega/2 - 2 with omega >= B + 3, i.e. q >= (B-1)/2; the least integer
    # >= (B-1)/2 is B//2; then q is even.  (An earlier version rounded with
    # Decimal's //, which truncates toward zero, and so could come out 2 low.)
    q = B // 2; q += q % 2
    if first is None and B >= NEED: first = x
    print(f"{x:>16,d} {k:>14,d} {float(L.exp()):>16.12f} {K:>16,d} {B:>16,d} {q:>16,d}  {big:,d}")
print()
if first: print(f"k + K_max first reaches 46e9 (the paper's requirement for q >= 23e9) at checkpoint x = {first:,d}")
else: print("k + K_max never reaches 46e9 at these checkpoints")
