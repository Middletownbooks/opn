#!/usr/bin/env python3
"""End-to-end checks of "The crossing number of complete graphs" (OpenAI 2026),
exact arithmetic modulo the prime 2^61-1, on concrete drawings of K_n.

  * Lemma 4.1: sum J([ip],[kq]) w_i w_p w_k w_q H(t_i,t_p,t_k,t_q) = 0 for monomials
    H of separate degree <= n-2 (random polyline drawings, adjacent edges may cross).
  * Lemma 4.2: E : S -> R^T injective (rank = C(s,2)^2).
  * Prop 4.3:  E^T diag(a) E = 0 (image totally isotropic), |T|/2 >= dim S, c(D) >= |T|/2.
  * Section 5: the two-page drawing has exactly Z(n) crossings, and there the chain
    is tight: |T| = 2 Z(n) = 2 dim E(S).
Negative controls must FAIL Lemma 4.1: shuffled spoke orders, no half terms, flipped signs.
"""
import random, itertools, sys
from fractions import Fraction as Fr
P = (1 << 61) - 1
def inv(a): return pow(a % P, P - 2, P)

def Zn(n): return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4

# ---------------- drawings: return (I, order) ----------------
# I[(i,p,k,q)] = signed crossing count of oriented edges i->p and k->q (all pairs, incl. adjacent)
# order[v] = list of the other vertices in counterclockwise spoke order from the gap
def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
def proper(p1, p2, p3, p4):
    d1, d2, d3, d4 = cross(p3, p4, p1), cross(p3, p4, p2), cross(p1, p2, p3), cross(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        v1 = (p2[0]-p1[0], p2[1]-p1[1]); v2 = (p4[0]-p3[0], p4[1]-p3[1])
        return 1 if v1[0]*v2[1] - v1[1]*v2[0] > 0 else -1
    if not ({p1, p2} & {p3, p4}) and 0 in (d1, d2, d3, d4):
        if min(p1[0], p2[0]) <= max(p3[0], p4[0]) and min(p3[0], p4[0]) <= max(p1[0], p2[0]) and \
           min(p1[1], p2[1]) <= max(p3[1], p4[1]) and min(p3[1], p4[1]) <= max(p1[1], p2[1]):
            raise ValueError("degenerate")
    return 0
def ccw_key(v):
    x, y = v; half = 0 if (y > 0 or (y == 0 and x < 0)) else 1
    return (half, Fr(-x, abs(x) + abs(y)) if half == 0 else Fr(x, abs(x) + abs(y)))

def polyline_drawing(n, bends, R=10**4):
    V = [(random.randint(-R, R), random.randint(-R, R)) for _ in range(n)]
    path = {}
    for i, p in itertools.combinations(range(n), 2):
        path[i, p] = [V[i]] + [(random.randint(-R, R), random.randint(-R, R)) for _ in range(bends)] + [V[p]]
        path[p, i] = path[i, p][::-1]
    segs = lambda pt: list(zip(pt[:-1], pt[1:]))
    for e in itertools.combinations(range(n), 2):
        s = segs(path[e])
        for a in range(len(s)):
            for b in range(a + 2, len(s)):
                if proper(*s[a], *s[b]): raise ValueError("self-crossing edge")
    I, pts = {}, 0
    for (i, p), (k, q) in itertools.combinations(list(itertools.combinations(range(n), 2)), 2):
        tot = 0
        for (a, b) in segs(path[i, p]):
            for (c, d) in segs(path[k, q]):
                v = proper(a, b, c, d); tot += v; pts += (v != 0)
        for (x, y, sx) in (((i, p), (k, q), 1), ((p, i), (k, q), -1), ((i, p), (q, k), -1), ((p, i), (q, k), 1)):
            I[x + y] = sx * tot; I[y + x] = -sx * tot
    order = []
    for v in range(n):
        others = [w for w in range(n) if w != v]
        vec = {w: (path[v, w][1][0] - V[v][0], path[v, w][1][1] - V[v][1]) for w in others}
        assert all(not (vec[w][1] == 0 and vec[w][0] > 0) for w in others)
        order.append(sorted(others, key=lambda w: ccw_key(vec[w])))
    return I, order, pts

def two_page_drawing(n):
    """Section 5: vertices on the spine, edge {i,j} on the upper page iff (i+j) mod n < floor(n/2)."""
    m = n // 2
    a = [1000 * i + random.randint(-200, 200) for i in range(n)]     # generic, increasing
    up = lambda i, j: (i + j) % n < m
    I, pts = {}, 0
    def tangent(i, p, x, y):
        c = (a[i] + a[p]) / 2
        inc = (-y, x - c)                       # direction of increasing polar angle
        leftright = a[i] < a[p]
        decreasing = (up(i, p) and leftright) or (not up(i, p) and not leftright)
        return (-inc[0], -inc[1]) if decreasing else inc
    E = list(itertools.combinations(range(n), 2))
    for (i, p), (k, q) in itertools.combinations(E, 2):
        tot = 0
        if len({i, p, k, q}) == 4 and up(i, p) == up(k, q):
            lo1, hi1 = sorted((a[i], a[p])); lo2, hi2 = sorted((a[k], a[q]))
            alternating = (lo1 < lo2 < hi1 < hi2) or (lo2 < lo1 < hi2 < hi1)
            if alternating:
                c1, r1 = (lo1 + hi1) / 2, (hi1 - lo1) / 2; c2, r2 = (lo2 + hi2) / 2, (hi2 - lo2) / 2
                x = (r1 * r1 - r2 * r2 + c2 * c2 - c1 * c1) / (2 * (c2 - c1))
                y = (r1 * r1 - (x - c1) ** 2) ** 0.5 * (1 if up(i, p) else -1)
                t1, t2 = tangent(i, p, x, y), tangent(k, q, x, y)
                cr = t1[0] * t2[1] - t1[1] * t2[0]
                assert abs(cr) > 1e-6
                tot = 1 if cr > 0 else -1; pts += 1
        for (x_, y_, sx) in (((i, p), (k, q), 1), ((p, i), (k, q), -1), ((i, p), (q, k), -1), ((p, i), (q, k), 1)):
            I[x_ + y_] = sx * tot; I[y_ + x_] = -sx * tot
    order = []
    for v in range(n):
        def key(w):
            r = Fr(abs(a[w] - a[v]), 2); right = a[w] > a[v]
            if up(v, w): return (0, (-1 if right else 1) * (1 / (2 * r)))      # angles near pi/2
            return (1, (-1 if not right else 1) * (1 / (2 * r)))               # angles near 3pi/2
        order.append(sorted([w for w in range(n) if w != v], key=key))
    return I, order, pts

def straight_drawing(n, R=10**6):
    pts_ = [(random.randint(-R, R), random.randint(-R, R)) for _ in range(n)]
    I, c = {}, 0
    E = list(itertools.combinations(range(n), 2))
    for (i, p), (k, q) in itertools.combinations(E, 2):
        tot = proper(pts_[i], pts_[p], pts_[k], pts_[q]) if len({i, p, k, q}) == 4 else 0
        c += (tot != 0)
        for (x, y, sx) in (((i, p), (k, q), 1), ((p, i), (k, q), -1), ((i, p), (q, k), -1), ((p, i), (q, k), 1)):
            I[x + y] = sx * tot; I[y + x] = -sx * tot
    order = [sorted([w for w in range(n) if w != v], key=lambda w: ccw_key((pts_[w][0]-pts_[v][0], pts_[w][1]-pts_[v][1]))) for v in range(n)]
    return I, order, c

# ---------------- J and the checks ----------------
def J2(I, order, n, half=True, flip=False):
    """2*J([ip],[kq]) for oriented edges i->p, k->q (integers)."""
    pos = [{w: r for r, w in enumerate(order[v])} for v in range(n)]
    def T(v, a, b): return 0 if a == b else (1 if pos[v][a] < pos[v][b] else -1)
    J = {}
    for i, p in itertools.permutations(range(n), 2):
        for k, q in itertools.permutations(range(n), 2):
            if {i, p} == {k, q}: J[i, p, k, q] = 0; continue
            val = 2 * I[i, p, k, q] * (-1 if flip else 1)
            if half:
                for w in {i, p} & {k, q}:
                    se = 1 if w == i else -1; sf = 1 if w == k else -1
                    oe = p if w == i else i; of = q if w == k else k
                    val += se * sf * T(w, oe, of)
            J[i, p, k, q] = val
    return J

def lemma41(J, n, t, w, trials=12):
    ok = True
    for _ in range(trials):
        a, b, c, h = (random.randint(0, n - 2) for _ in range(4))
        tot = 0
        for (i, p, k, q), v in J.items():
            if v:
                tot += v * w[i] * w[p] * w[k] * w[q] * pow(t[i], a, P) * pow(t[p], b, P) * pow(t[k], c, P) * pow(t[q], h, P)
        ok &= tot % P == 0
    return ok

def rank_mod(rows, ncols):
    M = [r[:] for r in rows]; r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] % P), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; iv = inv(M[r][c])
        M[r] = [x * iv % P for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % P:
                f = M[i][c]; M[i] = [(x - f * y) % P for x, y in zip(M[i], M[r])]
        r += 1
    return r

def full_check(name, I, order, n, cpts, expect_tight=False):
    s = (n - 1) // 2
    t = [i + 2 for i in range(n)]
    w = [inv(eval_prod := 1) for _ in range(n)]
    for i in range(n):
        d = 1
        for j in range(n):
            if j != i: d = d * (t[i] - t[j]) % P
        w[i] = inv(d)
    J = J2(I, order, n)
    l41 = lemma41(J, n, t, w)
    # T: ordered pairs of undirected independent edges with nonzero J
    E = list(itertools.combinations(range(n), 2))
    Tset = [(e, f) for e in E for f in E if len(set(e) | set(f)) == 4 and J[e + f] != 0]
    # basis of S
    sym = [(a, b) for a in range(s - 1) for b in range(a, s - 1)]
    def m(ab, x, u): a, b = ab; return (pow(x, a, P) * pow(u, b, P) + (pow(x, b, P) * pow(u, a, P) if a != b else 0)) % P
    basis = [(A, B) for A in sym for B in sym]
    Erows = [[m(A, t[e[0]], t[e[1]]) * m(B, t[f[0]], t[f[1]]) % P for (A, B) in basis] for (e, f) in Tset]
    rk = rank_mod(Erows, len(basis)) if Erows else 0
    # isotropy: E^T diag(a) E == 0
    def Delta(x, u, y, v): return (x-u)*(y-v)*(x-y)*(x-v)*(u-y)*(u-v) % P
    a = [J[e + f] * w[e[0]] * w[e[1]] * w[f[0]] * w[f[1]] % P * Delta(t[e[0]], t[e[1]], t[f[0]], t[f[1]]) % P for (e, f) in Tset]
    iso = True
    nb = len(basis)
    for c1 in range(nb):
        for c2 in range(c1, nb):
            if sum(a[r] * Erows[r][c1] % P * Erows[r][c2] for r in range(len(Tset))) % P:
                iso = False; break
        if not iso: break
    dimS = (s * (s - 1) // 2) ** 2
    msg = (f"{name:22s} n={n}: Lemma4.1 {l41}; dim S {dimS}; rank E {rk} (injective {rk == dimS}); "
           f"isotropic {iso}; |T|/2 = {len(Tset)//2} >= {dimS}: {len(Tset)//2 >= dimS}; c(D) = {cpts} >= |T|/2: {cpts >= len(Tset)//2}")
    if expect_tight:
        msg += f"; TIGHT: c(D)==Z(n) {cpts == Zn(n)}, |T|==2Z(n) {len(Tset) == 2*Zn(n)}, rank E==|T|/2 {rk == len(Tset)//2}"
    print(msg); sys.stdout.flush()
    return l41

random.seed(5)
print("== two-page construction (Section 5): crossing count vs Z(n)")
print("   ", [(n, two_page_drawing(n)[2], Zn(n)) for n in range(5, 21)])
print("== random straight-line drawings")
for n in (5, 7, 9, 11):
    I, order, c = straight_drawing(n); full_check("straight-line", I, order, n, c)
print("== two-page optimal drawings (tightness)")
for n in (5, 7, 9, 11, 13):
    I, order, c = two_page_drawing(n); full_check("two-page", I, order, n, c, expect_tight=True)
print("== random polyline drawings (repeated + adjacent crossings): Lemma 4.1 only")
cnt = 0
while cnt < 6:
    n = random.choice((5, 7))
    try: I, order, c = polyline_drawing(n, bends=random.choice((1, 2)))
    except (ValueError, AssertionError): continue
    cnt += 1
    t = [i + 2 for i in range(n)]; w = []
    for i in range(n):
        d = 1
        for j in range(n):
            if j != i: d = d * (t[i] - t[j]) % P
        w.append(inv(d))
    print(f"   polyline n={n}: {c} crossing points; Lemma 4.1 {lemma41(J2(I, order, n), n, t, w)}")
print("== negative controls on one polyline drawing (each should be False)")
while True:
    try: I, order, c = polyline_drawing(7, bends=1); break
    except (ValueError, AssertionError): continue
n = 7; t = [i + 2 for i in range(n)]; w = []
for i in range(n):
    d = 1
    for j in range(n):
        if j != i: d = d * (t[i] - t[j]) % P
    w.append(inv(d))
shuffled = [random.sample(o, len(o)) for o in order]
print("   shuffled spoke orders:", lemma41(J2(I, shuffled, n), n, t, w))
print("   no half terms:        ", lemma41(J2(I, order, n, half=False), n, t, w))
print("   flipped crossing signs:", lemma41(J2(I, order, n, flip=True), n, t, w))
