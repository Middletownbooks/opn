#!/usr/bin/env python3
"""Lemma 3.2 (and hence the cycle pairing of Lemma 3.1 on 4-cycles) on random
POLYLINE drawings of K_{m,n}: edges bend, independent and adjacent pairs may
cross several times, signed crossings may cancel.  Exact integer geometry;
drawings with self-intersecting edges, crossings at bends, or crossings
through vertices are rejected (not admissible drawings).
"""
import random, itertools
from fractions import Fraction as Fr

def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def proper(p1, p2, p3, p4):
    d1, d2, d3, d4 = cross(p3, p4, p1), cross(p3, p4, p2), cross(p1, p2, p3), cross(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        v1 = (p2[0]-p1[0], p2[1]-p1[1]); v2 = (p4[0]-p3[0], p4[1]-p3[1])
        return 1 if v1[0]*v2[1] - v1[1]*v2[0] > 0 else -1
    if (d1 == 0 or d2 == 0 or d3 == 0 or d4 == 0) and not ({p1, p2} & {p3, p4}):
        # touching / collinear contact not at a shared endpoint -> degenerate, reject
        if min(p1[0], p2[0]) <= max(p3[0], p4[0]) and min(p3[0], p4[0]) <= max(p1[0], p2[0]) and \
           min(p1[1], p2[1]) <= max(p3[1], p4[1]) and min(p3[1], p4[1]) <= max(p1[1], p2[1]):
            raise ValueError("degenerate")
    return 0

def segs(path): return list(zip(path[:-1], path[1:]))

def signed(path_e, path_f, adjacent):
    tot, cnt = 0, 0
    for (a, b) in segs(path_e):
        for (c, d) in segs(path_f):
            v = proper(a, b, c, d)
            tot += v; cnt += (v != 0)
    return tot, cnt

def ccw_key(v):
    x, y = v
    half = 0 if (y > 0 or (y == 0 and x < 0)) else 1
    return (half, Fr(-x, abs(x) + abs(y)) if half == 0 else Fr(x, abs(x) + abs(y)))

def order_pos(vecs):
    assert all(not (v[1] == 0 and v[0] > 0) for v in vecs)
    idx = sorted(range(len(vecs)), key=lambda t: ccw_key(vecs[t]))
    pos = [0] * len(vecs)
    for r, t in enumerate(idx): pos[t] = r
    return pos

def trial(m, n, bends, R=10**4):
    A = [(random.randint(-R, R), random.randint(-R, R)) for _ in range(m)]
    B = [(random.randint(-R, R), random.randint(-R, R)) for _ in range(n)]
    P = {(i, p): [A[i]] + [(random.randint(-R, R), random.randint(-R, R)) for _ in range(bends)] + [B[p]]
         for i in range(m) for p in range(n)}
    E = list(P)
    for e in E:  # simple edges, avoiding other vertices
        s = segs(P[e])
        for x in range(len(s)):
            for y in range(x + 2, len(s)):
                if proper(*s[x], *s[y]) != 0: raise ValueError("self-intersecting edge")
    I, raw_pts, nonzero = {}, 0, 0
    for e, f in itertools.combinations(E, 2):
        adj = e[0] == f[0] or e[1] == f[1]
        t, c = signed(P[e], P[f], adj)
        I[e, f] = t
        I[f, e] = -t      # swapping the order of the two directions flips the sign
        raw_pts += c; nonzero += (t != 0)
    posA = [order_pos([(P[i, p][1][0]-A[i][0], P[i, p][1][1]-A[i][1]) for p in range(n)]) for i in range(m)]
    posB = [order_pos([(P[i, p][-2][0]-B[p][0], P[i, p][-2][1]-B[p][1]) for i in range(m)]) for p in range(n)]
    T = lambda pos, u, w: 0 if u == w else (1 if pos[u] < pos[w] else -1)
    def J(i, p, k, q):
        if (i, p) == (k, q): return Fr(0)
        v = Fr(I[(i, p), (k, q)])
        if i == k: v += Fr(1, 2) * T(posA[i], p, q)
        if p == q: v += Fr(1, 2) * T(posB[p], i, k)
        return v
    ok = True
    for i in range(m):
        for k in range(m):
            H = [[J(i, p, k, q) - J(i, p, 0, q) - J(0, p, k, q) + J(0, p, 0, q) for q in range(n)] for p in range(n)]
            ok &= all(H[p][q] - H[p][0] - H[0][q] + H[0][0] == 0 for p in range(n) for q in range(n))
    multi = sum(1 for (e, f) in itertools.combinations(E, 2) if signed(P[e], P[f], False)[1] >= 2)
    cancel = sum(1 for (e, f) in itertools.combinations(E, 2) if signed(P[e], P[f], False)[1] >= 2 and I[e, f] == 0)
    adjx = sum(1 for (e, f) in itertools.combinations(E, 2) if (e[0] == f[0] or e[1] == f[1]) and signed(P[e], P[f], True)[1] > 0)
    return ok, raw_pts, multi, cancel, adjx

random.seed(11)
done = 0; allok = True; tot = [0, 0, 0, 0]
while done < 40:
    m, n = random.choice([(3, 3), (3, 5), (4, 5), (5, 5)])
    try:
        ok, pts, multi, cancel, adjx = trial(m, n, bends=random.choice([1, 2]))
    except (ValueError, AssertionError):
        continue
    done += 1; allok &= ok
    tot = [tot[0] + pts, tot[1] + multi, tot[2] + cancel, tot[3] + adjx]
    if not ok: print("FAIL on a drawing with", m, n)
print(f"40 admissible random polyline drawings: Lemma 3.2 held on all: {allok}")
print(f"  crossing points {tot[0]}, edge pairs crossing >= 2 times {tot[1]}, of which signed sum 0 (cancelling) {tot[2]}, adjacent pairs that cross {tot[3]}")
