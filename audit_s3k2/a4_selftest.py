#!/usr/bin/env python3
"""
Self-test of a4_solver's lattice step: force a round with a SMALL C so that
Lmin is below the L of known solutions, and check that every known solution
with Lmin <= L <= Lcur shows up among the enumerated vectors (a completeness
check of the ellipsoid and of the exact Fincke-Pohst enumeration).
"""
import math, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import a4_solver as S
from hp import set_prec, arg_pi_over_pibar, pi_dec
from decimal import Decimal as Dm

def one_round(T, Lcur, C):
    T = sorted(T); m = len(T); d = m + 1
    lnt = [math.log(t) for t in T]
    H = [int(Lcur / l) + 1 for l in lnt]
    g = [max(1, round(1000 * l)) for l in lnt]
    G = [g[i] * H[i] for i in range(m)]; Gmax = max(G)
    Lmin = 2 * math.log(S.K6 * C / Gmax)
    set_prec(len(str(C)) + 40); P = pi_dec()
    phi = [3 * arg_pi_over_pibar(t)[0] / P for t in T]
    psi = [int((Dm(C) * ph).to_integral_value()) for ph in phi]
    basis = []
    for i in range(m):
        r = [0] * d; r[i] = g[i]; r[m] = psi[i]; basis.append(r)
    r = [0] * d; r[m] = C; basis.append(r)
    Rl = int(C * S.K6 * math.exp(-Lmin / 2)) + 2 + sum(H)
    R2 = sum(x * x for x in G) + Rl * Rl
    vecs, nodes = S.enumerate_ball(S.lll(basis), R2)
    got = set()
    for v in vecs:
        cs = tuple(abs(v[i] // g[i]) for i in range(m))
        if all(cs[i] <= H[i] for i in range(m)):
            for x in S.check_exponents(T, cs, False): got.add(x)
    return Lmin, got, len(vecs)

ok = True
for T, Lcur, C in (([7, 13, 19], 14.0, 3 * 10 ** 5), ([7, 13, 19], 14.0, 10 ** 5), ([7, 13, 19], 14.0, 3 * 10 ** 4),
                   ([7, 13, 19, 127], 14.0, 10 ** 5), ([7, 13, 19, 127], 14.0, 2 * 10 ** 4)):
    known = S.brute(T, 10 ** 4)
    Lmin, got, nv = one_round(T, Lcur, C)
    need = {x for x in known if Lmin <= math.log(x * x + x + 1) <= Lcur}
    miss = need - got
    print(f"T={T} Lcur={Lcur} C={C}: Lmin={Lmin:.3f}, {nv} vectors; solutions with Lmin<=L<=Lcur: {sorted(need)}; found {sorted(got)}; missing {sorted(miss)}")
    ok &= not miss
print("SELFTEST", "PASS" if ok else "FAIL")
