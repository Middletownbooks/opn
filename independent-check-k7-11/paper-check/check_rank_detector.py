#!/usr/bin/env python3
"""Numerical check of Lemma 4.1 / 4.2 of the OpenAI paper (rank detector Phi).

For n = 2s+1 and distinct nodes x_1..x_n:
  B_pq = (x_p - x_q) / (F'(x_p) F'(x_q)) * h_pq h_pq^T,  h_pq = (x_p^a x_q^b)_{0<=a,b<s}
  Phi(H) = sum_pq H(p,q) B_pq.
Checks: (i) Phi kills additive and diagonal matrices; (ii) rank B_pq = 1 (p != q);
(iii) Phi(S_order) invertible for every strict linear order (all orders for n <= 7,
random orders for n = 9).  Exact rational arithmetic (fractions) throughout.
"""
import itertools, random, sys
from fractions import Fraction as Fr

def det(M):
    # exact Gaussian elimination
    M = [row[:] for row in M]; n = len(M); d = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f: M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return d

def rank(M):
    M = [row[:] for row in M]; r = 0; rows = len(M); cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def build(n, x):
    s = (n - 1) // 2
    Fp = [Fr(1)] * n
    for p in range(n):
        for q in range(n):
            if q != p: Fp[p] *= (x[p] - x[q])
    B = {}
    for p in range(n):
        for q in range(n):
            h = [x[p] ** a * x[q] ** b for a in range(s) for b in range(s)]
            w = (x[p] - x[q]) / (Fp[p] * Fp[q])
            B[p, q] = [[w * hi * hj for hj in h] for hi in h]
    return s, B

def phi(H, B, n, d):
    out = [[Fr(0)] * d for _ in range(d)]
    for p in range(n):
        for q in range(n):
            if H[p][q]:
                Bq = B[p, q]
                for i in range(d):
                    for j in range(d):
                        out[i][j] += H[p][q] * Bq[i][j]
    return out

def S_of(order, n):
    pos = {v: i for i, v in enumerate(order)}
    return [[Fr(0) if p == q else (Fr(1, 2) if pos[p] < pos[q] else Fr(-1, 2)) for q in range(n)] for p in range(n)]

random.seed(1)
for n, sample in ((3, None), (5, None), (7, None), (9, 300)):
    x = [Fr(random.randint(-40, 40)) + Fr(p, 7) for p in range(n)]
    assert len(set(x)) == n
    s, B = build(n, x); d = s * s
    # (i) additive and diagonal matrices
    ok_add = all(all(v == 0 for row in phi([[Fr(random.randint(-5, 5)) * (p == q) + rr + cc for q, cc in enumerate(c)] for p, rr in enumerate(r)], B, n, d) for v in row)
                 for r, c in [([Fr(random.randint(-9, 9)) for _ in range(n)], [Fr(random.randint(-9, 9)) for _ in range(n)]) for _ in range(5)])
    # (ii) rank one off the diagonal, zero on it
    ok_r1 = all(rank(B[p, q]) == (0 if p == q else 1) for p in range(n) for q in range(n))
    # (iii) invertibility for orders
    orders = list(itertools.permutations(range(n))) if sample is None else [random.sample(range(n), n) for _ in range(sample)]
    bad = sum(1 for o in orders if det(phi(S_of(o, n), B, n, d)) == 0)
    print(f"n={n} (s={s}, d={d}): kills additive+diagonal: {ok_add}; rank-one entries: {ok_r1}; "
          f"orders tested {len(orders)}{' (all)' if sample is None else ' (random)'}; singular images: {bad}")
