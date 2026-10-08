#!/usr/bin/env python3
"""What the K_{m,n} theorem alone gives for K_N, by counting.

A crossing of K_N involves two edges uv, wx on four distinct vertices.  For a
split V = A u B with |A| = a, it is a crossing of the K_{a,N-a} subdrawing
iff both pairs are split; that happens for 4*C(N-4, a-2) of the C(N, a)
splits.  Since every K_{a,N-a} subdrawing has >= Z(a) Z(N-a) crossings:
    cr(K_N) >= C(N,a) Z(a) Z(N-a) / (4 C(N-4, a-2))   for every a.
Compare with H(N) = Z(N) Z(N-1) / 4... = (1/4) fl(N/2) fl((N-1)/2) fl((N-2)/2) fl((N-3)/2).
"""
from math import comb, ceil
from fractions import Fraction as Fr

def Z(r): return (r // 2) * ((r - 1) // 2)
def H(N): return (N // 2) * ((N - 1) // 2) * ((N - 2) // 2) * ((N - 3) // 2) // 4

print(f"{'N':>5} {'H(N)':>12} {'counting bound':>15} {'ratio':>7}")
for N in [6, 8, 10, 11, 12, 13, 14, 16, 20, 30, 50, 100, 200, 400, 1000]:
    best = max(Fr(comb(N, a) * Z(a) * Z(N - a), 4 * comb(N - 4, a - 2)) for a in range(2, N - 1))
    lb = ceil(best)
    print(f"{N:>5} {H(N):>12} {lb:>15} {float(Fr(lb, H(N))):>7.4f}")
