#!/usr/bin/env python3
"""
Audit Part A3: Matveev 1998, Theorem 2.2, applied to x^2+x+1 = 3^d prod_{t in T} t^{c_t},
derived from the page images only (sources/matveev1998_p8{2,5,6,7}.png), and written
without reading s3k2/39.

Setting.  K = Q(w), D_K = 2, K not real so kappa = 2 and D = D_K/kappa = 1.
z = x - w, |z|^2 = x^2+x+1.  In Z[w] (a PID) z = eps * lambda^d * prod rho_t^{c_t},
rho_t in {pi_t, conj pi_t}; so z/conj(z) = zeta * prod (pi_t/conj pi_t)^{b_t}, b_t = +-c_t,
zeta in mu_6 (lambda/conj lambda = -w is a root of unity).
    Lambda = Log(z/conj z) = b_0 * (i pi/3) + sum_t b_t * i theta_t          (n = |T|+1 terms)
    |Lambda| = 2|arg z| <= pi |sin arg z| = pi (sqrt3/2)/|z| <= 2 sqrt3/|z|   (Re z = x+1/2 > 0)
    Lambda != 0 since Im z = -sqrt3/2 != 0.
rho = rank_R{ln a_j} = 1: every log is purely imaginary (p.85: "rank_R").
Kummer (1.5): a product of a nonempty subset containing some pi_t/conj pi_t has odd
pi_t-adic valuation, so is not a square; zeta_6 alone is not a square in K (mu(K) = mu_6,
squares are mu_3).  Kummer theory (mu_2 in K) gives [K(sqrt a_j) : K] = 2^n.
h(pi_t/conj pi_t) = (1/2) ln t: minimal polynomial t X^2 - Tr(pi^2) X + t, primitive,
both roots of modulus 1, so Mahler measure t.
Choices theta = 1, E = 1, C3 = n/rho satisfy (2.1)-(2.3): A_j >= h(a_j) gives (2.1),
A_j >= |ln a_j|/D gives (2.2), and C3* = n/rho >= 1 > 2/e gives (2.3).
"""
import math, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from hp import set_prec, arg_pi_over_pibar, pi_dec

def constants(n, rho=1, D=1):
    C3 = n / rho
    C1 = (1 + math.exp(-2 * n) / 148) * (n * math.log(2) + 2) * (1 + 1 / n) / C3
    C2 = 4 * (n + 1) * (6 + 5 / (n * math.log(2) + 2)) * math.exp(2 * n) / (math.sqrt(n) * C3)
    return C1, C2, C3

def matveev_L0(T, factor=1.0, const112=112.0, verbose=True):
    """
    Upper bound L0 for L = ln(x^2+x+1) (with 3 allowed to divide, L >= sum c_t ln t).
    Returns (L0, H0) where H0 = floor(L0 / ln min T) bounds every c_t.
    factor: multiply Matveev's constant by this (insensitivity test).
    """
    set_prec(60)
    n = len(T) + 1; D = 1; rho = 1
    C1, C2, C3 = constants(n, rho, D)
    P = float(pi_dec())
    thetas = {t: float(arg_pi_over_pibar(t)[0]) for t in T}
    A0 = max(0.0, (P / 3) / D, 1 / (D * C1))
    A = {t: max(0.5 * math.log(t), abs(thetas[t]) / D, 1 / (D * C1)) for t in T}
    Omega = A0 * math.prod(A.values())
    om = Omega * (C1 * D / math.e) ** n * (C3 * math.exp(C3) * math.e / 2) ** rho   # (2.5), theta=E=1
    Amin = min(A.values())                       # worst case for A_n (alpha_n must have b_n != 0)
    C0p = math.log(C2 * D * om / (C1 * Amin))    # (2.15), largest when A_n smallest
    K = const112 * 2 ** n * C2 * C0p * D * D * om * factor
    kappa = max(abs(thetas[t]) / math.log(t) for t in T)
    lnmin = math.log(min(T))
    def B_of(L):
        # |b_0| (pi/3) <= |Lambda| + sum |b_t||theta_t| <= pi + kappa L, |b_t| <= L / ln t
        b0 = 3 + 3 * kappa * L / P
        return max(b0 * A0 / Amin, max(L / math.log(t) * A[t] for t in T) / Amin)
    # L/2 - ln(2 sqrt3) <= -ln|Lambda| < K ln(2 e B(L))
    L = 100.0
    for _ in range(200):
        Ln = 2 * math.log(2 * math.sqrt(3)) + 2 * K * math.log(2 * math.e * B_of(L))
        if abs(Ln - L) < 1e-6 * L: L = Ln; break
        L = Ln
    L0 = L * (1 + 1e-9)
    H0 = int(L0 / lnmin)
    if verbose:
        print(f"T={sorted(T)} n={n} C1={C1:.6g} C2={C2:.6g} C3={C3:g} A0={A0:.5f} "
              + " ".join(f"A_{t}={A[t]:.5f}(theta={thetas[t]:+.5f})" for t in sorted(T)))
        print(f"   Omega={Omega:.6g} omega={om:.6g} C0'={C0p:.6g} K=112*2^n*C2*C0'*om={K:.6g}")
        print(f"   L0 = {L0:.6g}   H0 = max c_t <= {H0:.6g}")
    return L0, H0

def remark_check():
    """Remark after (2.16): 112 2^n C2 th^n C1^n e^-n (C3 e^C3 E e/(2 th))^rho < 2^15 (ne/2rho)^rho rho (2e^2 rho ln2)^n / n^(1/2)."""
    print("\nRemark after (2.16), theta=E=1, C3=n/rho:")
    for rho in (1, 2):
        for n in range(2, 11):
            C1, C2, C3 = constants(n, rho)
            lhs = 112 * 2 ** n * C2 * C1 ** n * math.exp(-n) * (C3 * math.exp(C3) * math.e / 2) ** rho
            rhs = 2 ** 15 * (n * math.e / (2 * rho)) ** rho * rho * (2 * math.e ** 2 * rho * math.log(2)) ** n / math.sqrt(n)
            print(f"   rho={rho} n={n:2d}  lhs/rhs = {lhs / rhs:.4f}")

if __name__ == "__main__":
    for T in ([7, 13], [7, 13, 19], [7, 13, 19, 127], [7, 13, 19, 31, 127]):
        matveev_L0(T)
    print("\nInsensitivity: constant inflated by 1e6")
    for T in ([7, 13, 19], [7, 13, 19, 31, 127]):
        matveev_L0(T, factor=1e6)
    remark_check()
