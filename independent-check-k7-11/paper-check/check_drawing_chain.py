#!/usr/bin/env python3
"""End-to-end check of the OpenAI paper's lower-bound chain on concrete
straight-line drawings of K_{m,n} (n odd), in exact arithmetic.

For each drawing: build J exactly as in (3.1) (signed crossings with the
stated orientation convention, half comparison signs of the counterclockwise
spoke order read from a fixed gap, sigma = +1 out of a_i, -1 into b_p); test
Lemma 3.2 (J_ik - J_i1 - J_1k + J_11 is row-plus-column); apply Phi
(Lemma 4.2); test R_ik = X_i - Y_k, rank R_ii = d, rank R_ik <= c_ik, and
sum_{i != k} rank R_ik >= 2 d_m d_n (Corollary 2.3), hence c(D) >= d_m d_n.
On the Zarankiewicz axis drawing every inequality must be tight.
"""
import random, sys
from fractions import Fraction as Fr
sys.path.insert(0, __import__("os").path.dirname(__file__))
from check_rank_detector import build, phi, rank

def zr(r): return (r // 2) * ((r - 1) // 2)

def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def seg_cross(p1, p2, p3, p4):
    """+1/-1 if open segments p1p2 and p3p4 cross properly (sign = orientation of
    (dir1, dir2)), 0 if they do not meet.  Assumes general position."""
    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        v1 = (p2[0]-p1[0], p2[1]-p1[1]); v2 = (p4[0]-p3[0], p4[1]-p3[1])
        c = v1[0]*v2[1] - v1[1]*v2[0]
        return 1 if c > 0 else -1
    return 0

def ccw_key(v):
    # counterclockwise angle order starting just after the +x direction (the gap)
    x, y = v
    half = 0 if (y > 0 or (y == 0 and x < 0)) else 1
    return (half, Fr(-x, 1) / (abs(x) + abs(y)) if half == 0 else Fr(x, 1) / (abs(x) + abs(y)))

def order_index(center, others):
    vecs = [(o[0]-center[0], o[1]-center[1]) for o in others]
    assert all(not (v[1] == 0 and v[0] > 0) for v in vecs), "spoke on the gap"
    idx = sorted(range(len(others)), key=lambda t: ccw_key(vecs[t]))
    pos = [0] * len(others)
    for r, t in enumerate(idx): pos[t] = r
    return pos

def check(A, Bp, label, expect_tight=False, flip=False):
    m, n = len(A), len(Bp); s = (n - 1) // 2; d = s * s
    # signed crossings between edges (i,p) = a_i -> b_p
    I = {}
    for i in range(m):
        for p in range(n):
            for k in range(m):
                for q in range(n):
                    if i != k and p != q:
                        v = seg_cross(A[i], Bp[p], A[k], Bp[q])
                        I[i, p, k, q] = -v if flip else v
    posA = [order_index(A[i], Bp) for i in range(m)]           # spoke order at a_i over p
    posB = [order_index(Bp[p], A) for p in range(n)]           # spoke order at b_p over i
    T = lambda pos, u, w: 0 if u == w else (1 if pos[u] < pos[w] else -1)
    def J(i, p, k, q):
        val = Fr(I.get((i, p, k, q), 0))
        if i == k and p != q: val += Fr(1, 2) * T(posA[i], p, q)          # sigma = +1 * +1
        if p == q and i != k: val += Fr(1, 2) * T(posB[p], i, k)          # sigma = -1 * -1
        return val
    blk = {(i, k): [[J(i, p, k, q) for q in range(n)] for p in range(n)] for i in range(m) for k in range(m)}
    # Lemma 3.2: rectangular differences of H vanish
    lem32 = True
    for i in range(m):
        for k in range(m):
            H = [[blk[i, k][p][q] - blk[i, 0][p][q] - blk[0, k][p][q] + blk[0, 0][p][q] for q in range(n)] for p in range(n)]
            lem32 &= all(H[p][q] - H[p][0] - H[0][q] + H[0][0] == 0 for p in range(n) for q in range(n))
    xs = [Fr(3 * p + 1, 2) for p in range(n)]
    _, Bm = build(n, xs)
    R = {key: phi(M, Bm, n, d) for key, M in blk.items()}
    diff_ok = all(R[i, k] == [[R[i, 0][a][b] - (R[0, 0][a][b] - R[0, k][a][b]) for b in range(d)] for a in range(d)]
                  for i in range(m) for k in range(m))
    diag_full = all(rank(R[i, i]) == d for i in range(m))
    c = {(i, k): sum(1 for p in range(n) for q in range(n) if p != q and I[i, p, k, q] != 0) for i in range(m) for k in range(m) if i != k}
    ranks = {(i, k): rank(R[i, k]) for i in range(m) for k in range(m) if i != k}
    rank_le_c = all(ranks[key] <= c[key] for key in ranks)
    total_rank = sum(ranks.values()); cD = sum(c.values()) // 2
    bound = 2 * zr(m) * d
    msg = (f"{label:28s} m={m} n={n}: Lemma3.2 {lem32}; R_ik=X_i-Y_k {diff_ok}; rank R_ii=d {diag_full}; "
           f"rank R_ik<=c_ik {rank_le_c}; sum rank {total_rank} >= {bound}: {total_rank >= bound}; c(D)={cD} >= d_m d_n={zr(m)*zr(n)}")
    if expect_tight:
        msg += f"; TIGHT: c(D)==d_m d_n {cD == zr(m)*zr(n)}, sum rank==2c {total_rank == 2*cD}, every rank==c_ik {all(ranks[k_]==c[k_] for k_ in ranks)}"
    print(msg)
    return lem32

def generic(r):
    return [(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6)) for _ in range(r)]

def axis(m, n):
    ys = random.sample(range(1, 10**6), m); xs_ = random.sample(range(1, 10**6), n)
    A = [(0, ys[i] if i < m // 2 else -ys[i]) for i in range(m)]
    Bp = [(xs_[p] if p < n // 2 else -xs_[p], 0) for p in range(n)]
    return A, Bp

random.seed(7)
for (m, n) in ((3, 3), (4, 5), (5, 5), (6, 5), (5, 7), (7, 7)):
    for t in range(3):
        check(generic(m), generic(n), f"random drawing #{t}")
    check(*axis(m, n), "Zarankiewicz axis drawing", expect_tight=True)
print("control: same drawings with the crossing-sign convention flipped (Lemma 3.2 should then fail):")
random.seed(7)
check(generic(5), generic(5), "flipped signs", flip=True)
