#!/usr/bin/env python3
"""
Run the independent solver (a4_solver.py) on EVERY statement that s3k2/39's
`residual` mode settles, and compare with 39's printed answers (copied from
its output, logs/39_residual.log).  Also re-derive, independently of 35/36,
the narrowing step for the four alpha=2 named sets whose Sm(T) has >= 4 members.
"""
import sys, math
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a4_solver import solve
from hp import is_square
from fractions import Fraction as F

def isprime(n):
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True

REPO_SM = {   # s3k2/39 residual, "Sm(T) complete = ..."
    (7,13,19,37,67): [11,29,653], (7,13,19,37,127): [11,107,653], (7,13,19,43,127): [11,107,653],
    (7,13,19,127,409): [11,53,107,653], (7,13,19,127,1723): [11,41,107,653],
    (7,13,19,31,127): [5,11,107,191,653], (7,13,19,31,331): [5,11,191,653],
    (7,13): [], (13,61,151): [], (13,61,157): [], (7,13,19): [11,653],
    (13,61,157,8269): [], (7,13,19,127): [11,107,653]}
REPO_CASEB = {(7,13): [], (13,61,151): [13], (13,61,157): [13], (13,61,28057): [13], (7,13,19): [7]}

ok = True
mine_sm = {}
for T, rep in REPO_SM.items():
    sols = solve(list(T), allow3=False, verbose=False)
    sm = [x for x in sols if x >= 5 and x % 3 == 2 and isprime(x)]
    mine_sm[T] = sm
    print(f"Sm{list(T)}: mine {sm}  repo {rep}  {'OK' if sm == rep else 'MISMATCH'}", flush=True)
    ok &= sm == rep
for S, rep in REPO_CASEB.items():
    sols = solve(list(S), allow3=True, verbose=False)
    # (t^2+t+1)/3 S-smooth  <=>  t^2+t+1 = 3 * S-smooth
    tb = []
    for t in sols:
        if t > 1 and t % 3 == 1 and isprime(t):
            n = (t * t + t + 1) // 3
            for s in S:
                while n % s == 0: n //= s
            if n == 1 and (t * t + t + 1) % 9 != 0: tb.append(t)
    print(f"CaseB{list(S)}: mine {tb}  repo {rep}  {'OK' if tb == rep else 'MISMATCH'}", flush=True)
    ok &= tb == rep

# ---- narrowing for the alpha = 2, |W| = 0 named sets with |Sm| >= 4
def Fset(t):
    n = t * t + t + 1; out = set(); d = 2
    while d * d <= n:
        while n % d == 0: out.add(d); n //= d
        d += 1
    if n > 1: out.add(n)
    return {p for p in out if p % 3 == 1}
def geom(t, k): return F(sum(t**i for i in range(k + 1)), t**k)
def sig(t, k): return sum(t**i for i in range(k + 1))
def forced_ok(t, k, MIN):  # no prime = 1 mod 3 below MIN divides sigma(t^k)
    return all(sig(t, k) % q for q in (7,) if q < MIN and q != t)
def v3(n):
    c = 0
    while n % 3 == 0: n //= 3; c += 1
    return c
from itertools import combinations
TARGET = F(18, 13)
for T in [(7,13,19,127,409), (7,13,19,127,1723), (7,13,19,31,127), (7,13,19,31,331)]:
    MIN = T[0]; los = []
    for O in combinations(T, 2):
        if not all(Fset(a) <= set(T) and forced_ok(a, 2, MIN) for a in O): continue
        rest = [t for t in T if t not in O]
        for s in rest:
            if s % 12 != 1: continue
            # alpha = 2 spends the whole 3-budget: v3(e+1) = v3(q+1) = 0
            es = [e for e in range(1, 400, 4) if v3(e + 1) == 0 and forced_ok(s, e, MIN)]
            if not es: continue
            ns = [n for n in rest if n != s]
            qs = [[q for q in range(4, 400, 2) if v3(q + 1) == 0 and forced_ok(n, q, MIN)] for n in ns]
            if not all(qs): continue
            lo = geom(O[0], 2) * geom(O[1], 2) * geom(s, es[0])
            for n, q in zip(ns, qs): lo *= geom(n, q[0])
            los.append((lo, O, s, ns))
    LO = min(l[0] for l in los); R = TARGET / LO
    adm = [x for x in mine_sm[T] if geom(x, 2) <= R]
    print(f"{list(T)}: assignments {[(list(O), s, ns) for _, O, s, ns in los]}  LO_raw {float(LO):.6f}  R {float(R):.6f}"
          f"  admissible {adm}  need 4 -> {'DEAD' if len(adm) < 4 else 'ALIVE?'}")
    ok &= len(adm) < 4
print("ALL AGREE" if ok else "SOMETHING DISAGREES")
