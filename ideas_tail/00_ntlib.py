#!/usr/bin/env python3
"""
ideas_tail/00_ntlib -- shared number-theory helpers (bare CPython).

is_prime, brent, the ECM routines and factor() are COPIED from
restrained/15_tree_pilot.py (lines 55-167; same code, own rho budget), so that the
ideas_tail scripts do not execute that script's module-level work.  is_prime is a
deterministic Miller-Rabin below 3.317e24 (first 13 prime bases; Sorenson-Webster)
and a strong probable-prime test with 20 bases above.
Load with:  importlib.util (the file name starts with a digit).
"""
import math, random
MRB = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
def is_prime(n):
    if n < 2: return False
    for p in MRB:
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    bases = MRB if n < 3317044064679887385961981 else MRB + (43, 47, 53, 59, 61, 67, 71)
    for a in bases:
        y = pow(a, d, n)
        if y in (1, n - 1): continue
        for _ in range(s - 1):
            y = y * y % n
            if y == n - 1: break
        else: return False
    return True

class Budget(Exception): pass
RHO_BUDGET = 2_000_000
def brent(n, budget=None):
    if n % 2 == 0: return 2
    rng = random.Random(n)
    for _ in range(20):
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g = r = q = 1; it = 0
        while g == 1:
            x = y
            for _ in range(r): y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n; q = q * abs(x - y) % n
                g = math.gcd(q, n); k += m
            r *= 2; it += r
            if it > (budget or RHO_BUDGET): raise Budget(n)
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n; g = math.gcd(abs(x - ys), n)
        if g != n: return g
    raise Budget(n)

# ---- ECM (Montgomery curves, Suyama parametrisation), the fallback after rho ----
def _add(P, Q, D, n):     # differential addition: P + Q with P - Q = D
    X1, Z1 = P; X2, Z2 = Q; X0, Z0 = D
    u = (X1 - Z1) * (X2 + Z2) % n; v = (X1 + Z1) * (X2 - Z2) % n
    return (Z0 * (u + v) ** 2 % n, X0 * (u - v) ** 2 % n)
def _dbl(P, a24, n):
    X, Z = P
    s, d = (X + Z) ** 2 % n, (X - Z) ** 2 % n
    t = s - d
    return (s * d % n, t * (d + a24 * t) % n)
def _mul(k, P, a24, n):   # Montgomery ladder
    R0, R1 = P, _dbl(P, a24, n)
    for bit in bin(k)[3:]:
        if bit == '1': R0, R1 = _add(R1, R0, P, n), _dbl(R1, a24, n)
        else: R0, R1 = _dbl(R0, a24, n), _add(R1, R0, P, n)
    return R0
_SP = None
def _primes_upto(m):
    s = bytearray([1]) * (m + 1); s[:2] = b"\0\0"
    for i in range(2, math.isqrt(m) + 1):
        if s[i]: s[i*i::i] = bytearray(len(range(i*i, m + 1, i)))
    return [i for i in range(m + 1) if s[i]]
def ecm_one(n, B1, B2, sigma):
    u, v = (sigma * sigma - 5) % n, 4 * sigma % n
    x0, z0 = pow(u, 3, n), pow(v, 3, n)
    den = 16 * x0 * v % n                         # a24 = (v-u)^3 (3u+v) / (16 u^3 v)
    g = math.gcd(den, n)
    if g != 1: return g if g != n else None
    a24 = pow(v - u, 3, n) * (3 * u + v) * pow(den, -1, n) % n
    Q = (x0, z0)
    for p in _primes_upto(B1):
        pk = p
        while pk * p <= B1: pk *= p
        Q = _mul(pk, Q, a24, n)
    g = math.gcd(Q[1], n)
    if 1 < g < n: return g
    if g == n: return None
    # stage 2: primes q = k*D +- d in (B1, B2]
    D = 2310
    baby = {}
    Q2 = _dbl(Q, a24, n); prev, cur = Q, _add(Q2, Q, Q, n)   # [1]Q, [3]Q
    baby[1] = Q
    for d in range(3, D // 2, 2):
        if math.gcd(d, D) == 1: baby[d] = cur
        prev, cur = cur, _add(cur, Q2, prev, n)
    QD = _mul(D, Q, a24, n)
    k = B1 // D
    Gk_prev = _mul(max(k - 1, 1), QD, a24, n) if k > 1 else None
    Gk = _mul(k, QD, a24, n) if k >= 1 else QD
    if k == 0: k = 1
    if Gk_prev is None: Gk_prev = _mul(k - 1, QD, a24, n) if k > 1 else (Q[0], Q[1])
    acc = 1
    PR2 = set(p for p in _primes_upto(B2) if p > B1)
    while k * D - D // 2 <= B2:
        X, Z = Gk
        for d, (xd, zd) in baby.items():
            if (k * D + d) in PR2 or (k * D - d) in PR2:
                acc = acc * (X * zd - xd * Z) % n
        k += 1
        if k == 2 and Gk_prev == (Q[0], Q[1]): Gk_prev, Gk = Gk, _dbl(QD, a24, n)
        else: Gk_prev, Gk = Gk, _add(Gk, QD, Gk_prev, n)
    g = math.gcd(acc, n)
    return g if 1 < g < n else None
def ecm(n, rng):
    for B1, curves in ((2000, 25), (11000, 90), (50000, 300), (250000, 700)):
        B2 = 100 * B1
        for _ in range(curves):
            g = ecm_one(n, B1, B2, rng.randrange(6, n - 1))
            if g: return g
    return None


def factor(n, rho_budget=None, use_ecm=True):
    """(sorted prime factors with multiplicity, complete?)  complete=False means a
    composite part could not be split within budget; it is returned as ('C', v)."""
    out, stack, rest = [], [n], []
    while stack:
        v = stack.pop()
        if v == 1: continue
        if is_prime(v): out.append(v); continue
        try:
            d = brent(v, rho_budget)
        except Budget:
            d = ecm(v, random.Random(v)) if use_ecm else None
            if d is None: rest.append(v); continue
        stack += [d, v // d]
    return sorted(out), rest

def prod_tree(xs):
    xs = list(xs) or [1]
    while len(xs) > 1:
        xs = [xs[i] * xs[i+1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]

def cube_root(q):
    e = (q - 1) // 3
    for g in range(2, q):
        x = pow(g, e, q)
        if x != 1: return x
