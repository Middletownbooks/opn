#!/usr/bin/env python3
"""
Audit Part A4: an independent complete solver for

        x^2 + x + 1 = prod_{t in T} t^{c_t}        (x >= 0; optionally a factor 3 allowed)

Written without reading s3k2/39.  The reduction differs from a "shortest-vector
lower bound" argument in three ways:

  * the unknown is L = ln(x^2+x+1) (weighted exponents), not max c_t;
  * the lattice is reduced by an EXACT rational LLL, and then every lattice
    vector in an ellipsoid that provably contains every solution with
    Lmin <= L <= Lcur is ENUMERATED (Fincke-Pohst, exact Fractions); each vector
    found is tested as a candidate exponent vector; no lemma about b*_i is used;
  * the last step enumerates every exponent vector with sum c_t ln t <= Lfinal
    and tests 4N-3 for squareness (no search in x).

Linear form (see a3_matveev_bound.py):  z = x - w,  Lambda = Log(z / conj z),
Lambda' = Lambda / (i pi/3) = b0 + sum_t b_t phi_t,  phi_t = 3 theta_t / pi,
|b_t| = c_t,  |Lambda'| <= (3/pi) * 2 sqrt3 / |z| = (6 sqrt3/pi) e^{-L/2}.
Lattice vector for (b, b0):  v = (g_t b_t)_t ++ (b0 C + sum_t b_t psi_t),
psi_t = round(C phi_t), |C phi_t - psi_t| <= 1/2 + 1e-20, so
|v_last| <= C (6 sqrt3/pi) e^{-L/2} + sum_t |b_t|.
"""
import math, sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from hp import set_prec, arg_pi_over_pibar, pi_dec, is_square
from decimal import Decimal as Dm
from a3_matveev_bound import matveev_L0

K6 = 6 * math.sqrt(3) / math.pi * (1 + 1e-12)       # (6 sqrt3/pi), rounded up

# ---------------------------------------------------------------- exact LLL
def lll(basis, delta=F(99, 100)):
    b = [list(r) for r in basis]; n = len(b)
    def dot(u, v): return sum(x * y for x, y in zip(u, v))
    def gs():
        bs = []; mu = [[F(0)] * n for _ in range(n)]; Bn = []
        for i in range(n):
            v = [F(x) for x in b[i]]
            for j in range(i):
                mu[i][j] = F(dot(b[i], bs[j])) / Bn[j] if Bn[j] else F(0)
                v = [a - mu[i][j] * c for a, c in zip(v, bs[j])]
            bs.append(v); Bn.append(dot(v, v))
        return mu, Bn, bs
    mu, Bn, bs = gs(); k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                b[k] = [a - q * c for a, c in zip(b[k], b[j])]
                mu, Bn, bs = gs()
        if Bn[k] >= (delta - mu[k][k - 1] ** 2) * Bn[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            mu, Bn, bs = gs(); k = max(k - 1, 1)
    return b

# ------------------------------------------------------ exact Fincke-Pohst
def enumerate_ball(basis, R2):
    """All integer combinations y with ||sum y_i basis_i||^2 <= R2 (exact). Yields vectors."""
    n = len(basis)
    def dot(u, v): return sum(x * y for x, y in zip(u, v))
    bs = []; mu = [[F(0)] * n for _ in range(n)]; Bn = []
    for i in range(n):
        v = [F(x) for x in basis[i]]
        for j in range(i):
            mu[i][j] = F(dot(basis[i], bs[j])) / Bn[j]
            v = [a - mu[i][j] * c for a, c in zip(v, bs[j])]
        bs.append(v); Bn.append(dot(v, v))
    R2 = F(R2); y = [0] * n; out = []; nodes = [0]
    def rec(i, rem):
        nodes[0] += 1
        c = -sum((mu[j][i] * y[j] for j in range(i + 1, n)), F(0))
        q = rem / Bn[i]
        s = math.isqrt(math.floor(q)) + 1
        lo = math.floor(c) - s; hi = math.ceil(c) + s
        for yi in range(lo, hi + 1):
            d = (yi - c) ** 2 * Bn[i]
            if d <= rem:
                y[i] = yi
                if i == 0:
                    out.append([sum(y[k] * basis[k][col] for k in range(n)) for col in range(len(basis[0]))])
                else:
                    rec(i - 1, rem - d)
        y[i] = 0
    rec(n - 1, R2)
    return out, nodes[0]

# ------------------------------------------------------------------ solver
def check_exponents(T, cs, allow3):
    N = 1
    for t, c in zip(T, cs): N *= t ** c
    sols = []
    for M in ([N, 3 * N] if allow3 else [N]):
        if is_square(4 * M - 3):
            r = math.isqrt(4 * M - 3); x = (r - 1) // 2
            if x >= 0: sols.append(x)
    return sols

def solve(T, allow3=False, factor=1.0, verbose=True):
    T = sorted(T); m = len(T)
    L0, _ = matveev_L0(T, factor=factor, verbose=False)
    if allow3: L0 += math.log(3)
    lnt = [math.log(t) for t in T]
    found = set()
    Lcur = L0
    if verbose: print(f"T={T} allow3={allow3} Matveev L0 = {L0:.4g}")
    rounds = 0
    while True:
        rounds += 1
        H = [int(Lcur / l) + 1 for l in lnt]                 # |b_t| <= H_t
        g = [max(1, round(1000 * l)) for l in lnt]            # weights ~ ln t
        G = [g[i] * H[i] for i in range(m)]
        Gmax = max(G); d = m + 1
        # choose C so that the ellipsoid holds O(1) lattice points
        logC = d * math.log(math.sqrt(d + 1) * Gmax) - sum(math.log(x) for x in g) + math.log(50)
        C = 10 ** (int(logC / math.log(10)) + 1)
        Lmin = 2 * math.log(K6 * C / Gmax)                   # then C*K6*e^{-Lmin/2} = Gmax
        if Lmin >= Lcur * 0.97 and rounds > 1: break
        digits = len(str(C)) + 40
        set_prec(digits)
        P = pi_dec()
        phi = [3 * arg_pi_over_pibar(t)[0] / P for t in T]
        psi = [int((Dm(C) * ph).to_integral_value()) for ph in phi]
        basis = []
        for i in range(m):
            r = [0] * d; r[i] = g[i]; r[m] = psi[i]; basis.append(r)
        r = [0] * d; r[m] = C; basis.append(r)
        Rl = int(C * K6 * math.exp(-Lmin / 2)) + 2 + sum(H)
        R2 = sum(x * x for x in G) + Rl * Rl
        t0 = time.time()
        red = lll(basis)
        vecs, nodes = enumerate_ball(red, R2)
        cand = 0
        for v in vecs:
            bs = [v[i] // g[i] for i in range(m)]
            assert all(bs[i] * g[i] == v[i] for i in range(m))
            cs = [abs(b) for b in bs]
            if any(cs[i] > H[i] for i in range(m)): continue
            cand += 1
            for x in check_exponents(T, cs, allow3): found.add(x)
        if verbose:
            print(f"  round {rounds}: Lcur={Lcur:.4g} C=10^{len(str(C))-1} -> Lmin={Lmin:.4f} "
                  f"(x < {math.exp(Lmin/2):.3g}); {len(vecs)} vectors in ellipsoid, {cand} in box, "
                  f"{nodes} nodes, {time.time()-t0:.1f}s")
        Lcur = Lmin
    # final: every exponent vector with sum c_t ln t <= Lcur (+ln3 margin handled by allow3 test)
    Lf = Lcur
    cnt = [0]
    def rec(i, cs, s):
        if i == m:
            cnt[0] += 1
            for x in check_exponents(T, cs, allow3): found.add(x)
            return
        c = 0
        while s + c * lnt[i] <= Lf + 1e-9:
            rec(i + 1, cs + [c], s + c * lnt[i]); c += 1
    rec(0, [], 0.0)
    if verbose:
        print(f"  final: {cnt[0]} exponent vectors with sum c_t ln t <= {Lf:.3f}")
        print(f"  COMPLETE LIST (x >= 0): {sorted(found)}")
    return sorted(found)

def brute(T, X, allow3=False):
    out = []
    for x in range(X):
        n = x * x + x + 1
        for t in T:
            while n % t == 0: n //= t
        if n == 1 or (allow3 and n == 3): out.append(x)
    return out

if __name__ == "__main__":
    sets = [[7, 13], [7, 13, 19], [7, 13, 19, 127], [7, 13, 19, 31, 127]]
    if len(sys.argv) > 1 and sys.argv[1] == "factor":
        for T in sets: solve(T, factor=1e6)
        sys.exit()
    allow3 = len(sys.argv) > 1 and sys.argv[1] == "allow3"
    for T in sets:
        sol = solve(T, allow3=allow3)
        b = brute(T, 10 ** 6, allow3)
        print(f"  brute force x < 10^6: {b}   agree on that range: {[x for x in sol if x < 10**6] == b}\n")
