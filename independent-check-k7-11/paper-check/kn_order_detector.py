#!/usr/bin/env python3
"""Lemma 3.2/3.3 of "The crossing number of complete graphs" (OpenAI 2026):
for 2s distinct nodes and ANY linear order, the pairing
  M(A,B) = sum_{p,q} S(p,q) (u_p - u_q)/(G'(u_p) G'(u_q)) A(u_p,u_q) B(u_p,u_q)
is nonsingular on P_{s-1,s-2} x P_{s-2,s-1}.  Exact rational arithmetic.
Also checks Lemma 3.2 directly (evaluation on L_s is injective on both spaces)."""
import itertools, random
from fractions import Fraction as Fr

def det(M):
    M = [r[:] for r in M]; n = len(M); d = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f: M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return d

def pairing_matrix(u, order, s):
    N = len(u); pos = {v: i for i, v in enumerate(order)}
    Gp = [Fr(1)] * N
    for p in range(N):
        for q in range(N):
            if q != p: Gp[p] *= u[p] - u[q]
    monA = [(a, b) for a in range(s) for b in range(s - 1)]        # P_{s-1,s-2}
    monB = [(a, b) for a in range(s - 1) for b in range(s)]        # P_{s-2,s-1}
    W = {}
    for p in range(N):
        for q in range(N):
            if p != q:
                Spq = Fr(1, 2) if pos[p] < pos[q] else Fr(-1, 2)
                W[p, q] = Spq * (u[p] - u[q]) / (Gp[p] * Gp[q])
    return [[sum(W[p, q] * u[p] ** (a1 + a2) * u[q] ** (b1 + b2) for (p, q) in W) for (a2, b2) in monB] for (a1, b1) in monA]

def lemma32(u, s):
    L = [(p, q) for p in range(s) for q in range(p)] + [(p, q) for p in range(s, 2 * s) for q in range(p + 1, 2 * s)]
    ok = True
    for da, db in ((s - 1, s - 2), (s - 2, s - 1)):
        mons = [(a, b) for a in range(da + 1) for b in range(db + 1)]
        ok &= len(L) == len(mons) and det([[u[p] ** a * u[q] ** b for (a, b) in mons] for (p, q) in L]) != 0
    return ok

random.seed(3)
for s, nsample in ((2, None), (3, None), (4, 400), (5, 60)):
    N = 2 * s
    u = random.sample(range(-60, 61), N); u = [Fr(x, 3) for x in u]
    orders = list(itertools.permutations(range(N))) if nsample is None else [random.sample(range(N), N) for _ in range(nsample)]
    sing = sum(1 for o in orders if det(pairing_matrix(u, o, s)) == 0)
    print(f"s={s} ({N} nodes, pairing {s*(s-1)}x{s*(s-1)}): Lemma 3.2 injectivity {lemma32(u, s)}; "
          f"orders tested {len(orders)}{' (all)' if nsample is None else ' (random)'}; singular pairings: {sing}")
