#!/usr/bin/env python3
"""
Independent check of the eight single-exponent equations that s3k2/33 takes from
the Skolem solver (s3k2/32), using a4_solver (Matveev + exact LLL + Fincke-Pohst),
by solving the full multi-exponent problem and filtering the fixed exponents.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a4_solver import solve

def val(p, n):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k

REPO = {  # s3k2/32 table (NOTES 14b): x >= 1 solutions (c, x)
    "13^c": [(1, 3)], "3*13^c": [(0, 1), (2, 22)], "3*61^c": [(0, 1), (1, 13)], "39*61^c": [],
    "61^c": [], "13*61^c": [(0, 3)], "97^c": [], "61*97^c": [],
}
S13 = solve([13], allow3=True, verbose=False)
S1361 = solve([13, 61], allow3=True, verbose=False)
S6197 = solve([61, 97], allow3=True, verbose=False)
def pick(sols, D3, fixed, p):
    out = []
    for x in sols:
        if x < 1: continue
        n = x * x + x + 1
        if val(3, n) != D3: continue
        n //= 3 ** D3
        ok = all(val(q, n) == e for q, e in fixed)
        if not ok: continue
        for q, e in fixed: n //= q ** e
        c = val(p, n); n //= p ** c
        if n == 1: out.append((c, x))
    return sorted(out)
mine = {
    "13^c": pick(S13, 0, [], 13), "3*13^c": pick(S13, 1, [], 13),
    "3*61^c": pick(S1361, 1, [(13, 0)], 61), "39*61^c": pick(S1361, 1, [(13, 1)], 61),
    "61^c": pick(S1361, 0, [(13, 0)], 61), "13*61^c": pick(S1361, 0, [(13, 1)], 61),
    "97^c": pick(S6197, 0, [(61, 0)], 97), "61*97^c": pick(S6197, 0, [(61, 1)], 97),
}
ok = True
for k in REPO:
    print(f"x^2+x+1 = {k:8s}: mine {mine[k]}  repo {REPO[k]}  {'OK' if mine[k] == REPO[k] else 'MISMATCH'}")
    ok &= mine[k] == REPO[k]
print("ALL AGREE" if ok else "DISAGREE")
