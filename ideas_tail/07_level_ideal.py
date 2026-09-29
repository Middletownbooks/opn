#!/usr/bin/env python3
"""
ideas_tail/07 -- how much of the sieve loss is the LEVEL, and how much is sieving for
primality?  A pilot (floating point; ideal bounds with the error term ignored).

Sequence = the primes r in (x, 2x] (count X, from li).  Sift by the M2 primes q (here
q < 3e6, so every prime = 1 mod 3 in [7, xi)), each removing the two root classes of
r^2+r+1 among the phi(q) = q-1 classes: density f(q) = 2/(q-1), g(q) = f/(1-f) = 2/(q-3).
Selberg's upper bound with sifting limit xi and level D = xi^2 is X/G(xi) + (error).
The error term is IGNORED here, so each column is the best any Selberg bound with that
level could do if the primes had that level of distribution:
   * "BV level"  D = x^{1/2}  (Bombieri-Vinogradov strength), xi = x^{1/4};
   * "EH level"  D = x        (Elliott-Halberstam strength),   xi = x^{1/2}.
Compared with the TRUE Algorithm-1 survivor counts (exact, restrained/runs/13_z...).
The 16f column (restrained/16f: sieving integers for primality too, D = x) is 8.4-8.8.
Run:  python3 07_level_ideal.py
"""
import math, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
cp = {}
for l in open(os.path.join(HERE, "..", "restrained", "runs", "13_z_Q2e35_checkpoints.txt")):
    m = re.match(r"CP x=(\d+) k=(\d+) lnA=(\S+)", l)
    if m: cp[int(m[1])] = int(m[2])
def li(x):
    a, n = 2.0, 200000; la, lb = math.log(a), math.log(x); s = 0.0
    for i in range(n):
        t = la + (i + 0.5) * (lb - la) / n; s += math.exp(t) / t
    return s * (lb - la) / n
XI = 200_000
spf = list(range(XI + 1))
for i in range(2, math.isqrt(XI) + 1):
    if spf[i] == i:
        for j in range(i * i, XI + 1, i):
            if spf[j] == j: spf[j] = i
g = [0.0] * (XI + 1); g[1] = 1.0
for d in range(2, XI + 1):
    p = spf[d]; m = d // p
    if p % 3 != 1 or p < 7 or m % p == 0 or g[m] == 0.0: continue
    g[d] = g[m] * 2.0 / (p - 3)
Gc = [0.0] * (XI + 1)
for d in range(1, XI + 1): Gc[d] = Gc[d - 1] + g[d]
def G(xi): return Gc[min(int(xi), XI)]
print(f"{'range':>24} {'true':>11} {'BV-ideal':>9} {'EH-ideal':>9}   (bound / true)")
for a in (1_000_000_000, 2_000_000_000, 4_000_000_000, 8_000_000_000, 16_000_000_000):
    X = li(2 * a) - li(a); t = cp[2 * a] - cp[a]
    print(f"({a:.1e}, {2*a:.1e}] {t:11,d} {X / G(a ** 0.25) / t:9.2f} {X / G(a ** 0.5) / t:9.2f}")
