#!/usr/bin/env python3
"""
Complete solution of  x^2 + x + 1 = 3^delta * prod_{t in T} t^{c_t}  (any |T|)
by Matveev's lower bound plus lattice reduction.  Standard library only.

This is the standard Baker-plus-reduction method, specialised to Y = 1, where
only ARCHIMEDEAN logarithms are needed (no p-adic linear forms).  Every
constant is taken from MATVEEV_1998.md, which transcribes Theorem 2.2 of
Matveev, Izv. RAN Ser. Mat. 62:4 (1998) from the user-supplied screenshots.

STEP 0 (the linear form).  K = Q(w), D = 1.  With z = x - w = eps*gamma*prod pi_t^{c_t},
  z/zbar = zeta6^j * prod alpha_t^{e_t},  alpha_t = pi_t/conj(pi_t),  e_t = +-c_t,
  Lambda = Log(z/zbar) = i*phi,  phi = sum e_t theta_t + b0 * pi/3,
where theta_t = Arg(alpha_t) in (-pi, pi] and b0 is an integer.  Lambda != 0, and
|Lambda| <= 2 sqrt(3)/|z| once |z| >= 2 sqrt(3), with |z|^2 = x^2+x+1.
Hypotheses of Theorem 2.2 (Kummer condition, heights, rho = 1): MATVEEV_1998.md.

STEP 1 (Matveev).  With n = |T|+1, H = max c_t and |b0| <= 3|T|H + 1,
  (1/2) L <= ln(2 sqrt 3) + max_j 112 * 2^n C2 C0'_j omega ln(2e B_j),
  L = ln(x^2+x+1) >= H ln(min T),
which gives an explicit bound H <= X0.  Floating-point constants are inflated
by 1% before use.

STEP 2 (reduction; de Weger's lattice argument, written out here).  Put
v = (e_1..e_k, b0), phi~(v) = sum e_t [C theta_t] + b0 [C pi/3] (rounded), and
let Gamma be the lattice of vectors (e_1, .., e_k, phi~(v)).  For v != 0,
  |M v|^2 = sum e_t^2 + phi~^2 >= l^2,   l = shortest nonzero length of Gamma,
  |C phi(v) - phi~(v)| <= T0 = (sum |e_t| + |b0|)/2,
so C|phi| >= sqrt(l^2 - S) - T0 with S = k X0^2.  If l^2 > S + T0^2, then
  L <= 2 ln( 2 sqrt 3 * C / (sqrt(l^2 - S) - T0) ).
For l we use min |b_i*| over the Gram-Schmidt vectors of the reduced basis.
That is a valid lower bound for ANY basis of Gamma.  The reduced basis is
checked to be a basis of Gamma (same |det|), so soundness does not depend on
the LLL routine being correct, only on it using unimodular operations.
Iterate with the new bound.

STEP 3 (search).  Enumerate every 3^delta * T-smooth M <= exp(L_final) and test
whether 4M - 3 is a square.  This is exhaustive below the proved bound.

Run:  python3 39_baker_lll.py validate
      python3 39_baker_lll.py residual
"""
import sys, math, os
from decimal import Decimal, getcontext
from fractions import Fraction
from math import isqrt

getcontext().prec = 600

# ------------------------------------------------------------ high precision
def d_atan_small(x):
    """arctan for |x| <= 1e-3, Taylor series."""
    eps = Decimal(10) ** (-(getcontext().prec - 10))
    s = Decimal(0); term = x; n = 1; x2 = x*x; sign = 1
    while abs(term) > eps:
        s += sign * term / n
        term *= x2; n += 2; sign = -sign
    return s
def d_atan(x):
    if x < 0: return -d_atan(-x)
    if x > 1: return d_pi()/2 - d_atan(1/x)
    k = 0
    while x > Decimal("1e-3"):
        x = x / (1 + (1 + x*x).sqrt()); k += 1
    return d_atan_small(x) * (2**k)
_PI = []
def d_pi():
    if not _PI:
        # Machin: pi = 16 atan(1/5) - 4 atan(1/239)
        def at_inv(m):
            eps = Decimal(10) ** (-(getcontext().prec - 10))
            s = Decimal(0); term = Decimal(1)/m; n = 1; sign = 1; m2 = m*m
            while term > eps:
                s += sign*term/n; term /= m2; n += 2; sign = -sign
            return s
        _PI.append(16*at_inv(5) - 4*at_inv(239))
    return _PI[0]
def d_atan2(y, x):
    pi = d_pi()
    if x > 0: return d_atan(y/x)
    if x < 0: return d_atan(y/x) + (pi if y >= 0 else -pi)
    return pi/2 if y > 0 else -pi/2
SQ3 = Decimal(3).sqrt()

# ------------------------------------------------------------ Eisenstein data
def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
def eis_prime(q):
    for b in range(1, isqrt(4*q//3) + 2):
        disc = 4*q - 3*b*b
        if disc < 0: break
        r = isqrt(disc)
        if r*r == disc and (b + r) % 2 == 0:
            a = (b + r)//2
            assert a*a - a*b + b*b == q
            return (a, b)
    raise ValueError(q)
def arg_eis(a, b):
    """Arg of a + b w, w = (-1 + sqrt(-3))/2."""
    return d_atan2(Decimal(b)*SQ3/2, Decimal(a) - Decimal(b)/2)
def reduce_pi(th):
    pi = d_pi()
    while th > pi: th -= 2*pi
    while th <= -pi: th += 2*pi
    return th
def theta(t):
    a, b = eis_prime(t)
    return reduce_pi(2*arg_eis(a, b))

# ------------------------------------------------------------ Matveev (Theorem 2.2)
def matveev_X0(T, delta):
    k = len(T); n = k + 1; D = 1; rho = 1
    C3 = n / rho
    C1 = (1 + math.exp(-2*n)/148) * (n*math.log(2) + 2) * (1 + 1/n) / C3
    C2 = 4*(n+1) * (6 + 5/(n*math.log(2) + 2)) * math.exp(2*n) / (math.sqrt(n)*C3)
    th = [float(abs(theta(t))) for t in T]
    A = [max(0.0, (math.pi/3)/D, 1/(D*C1))]                        # zeta6: h = 0
    A += [max(0.5*math.log(t), th[i]/D, 1/(D*C1)) for i, t in enumerate(T)]
    Omega = 1.0
    for a in A: Omega *= a
    omega = Omega * (C1*D*1/math.e)**n * (C3*math.exp(C3)*1*math.e/2)**rho
    Amax = max(A)
    def rhs(H):
        Bmax = 3*k*H + 1
        worst = 0.0
        for Aj in A:                       # every admissible choice of the last index
            C0p = math.log(C2*D*omega/(C1*Aj))
            val = 112 * 2**n * C2 * C0p * D*D * omega * math.log(2*math.e*Bmax*Amax/Aj)
            worst = max(worst, val)
        return math.log(2*math.sqrt(3)) + worst * 1.01            # 1% safety margin
    tmin = min(T)
    H = 1e40
    for _ in range(200):
        Hn = 2*rhs(H)/math.log(tmin)
        if abs(Hn - H) < 1e-6*H: H = Hn; break
        H = Hn
    return int(H * 1.01) + 1, dict(n=n, C1=C1, C2=C2, omega=omega, A=A)

# ------------------------------------------------------------ LLL (integral, Cohen 2.6.7 style)
def lll(B):
    """LLL-reduce the rows of integer matrix B (delta = 3/4).  Only unimodular
       row operations (b_k -= q b_l, swaps) are used, so the output is a basis
       of the same lattice whatever happens.  Correctness of the reduction is
       NOT relied upon for soundness."""
    b = [list(r) for r in B]; n = len(b)
    dot = lambda u, v: sum(x*y for x, y in zip(u, v))
    d = [0]*(n+1); lam = [[0]*n for _ in range(n)]
    d[0] = 1; d[1] = dot(b[0], b[0])
    k = 1; kmax = 0
    def redi(k, l):
        if 2*abs(lam[k][l]) > d[l+1]:
            q = (2*lam[k][l] + d[l+1]) // (2*d[l+1])
            b[k] = [x - q*y for x, y in zip(b[k], b[l])]
            lam[k][l] -= q*d[l+1]
            for i in range(l): lam[k][i] -= q*lam[l][i]
    def swapi(k):
        b[k], b[k-1] = b[k-1], b[k]
        for j in range(k-1): lam[k][j], lam[k-1][j] = lam[k-1][j], lam[k][j]
        l = lam[k][k-1]
        Bn = (d[k-1]*d[k+1] + l*l) // d[k]
        for i in range(k+1, kmax+1):
            t = lam[i][k]
            lam[i][k] = (d[k+1]*lam[i][k-1] - l*t) // d[k]
            lam[i][k-1] = (Bn*t + l*lam[i][k]) // d[k+1]
        d[k] = Bn
    while k < n:
        if k > kmax:
            kmax = k
            for j in range(k+1):
                u = dot(b[k], b[j])
                for i in range(j): u = (d[i+1]*u - lam[k][i]*lam[j][i]) // d[i]
                if j < k: lam[k][j] = u
                else:
                    d[k+1] = u
                    assert u != 0, "dependent vectors"
        redi(k, k-1)
        if 4*d[k+1]*d[k-1] < 3*d[k]*d[k] - 4*lam[k][k-1]**2:
            swapi(k); k = max(1, k-1)
        else:
            for l in range(k-2, -1, -1): redi(k, l)
            k += 1
    return b

def det_int(M):
    """exact determinant by fraction-free Bareiss elimination."""
    A = [list(r) for r in M]; n = len(A); sign = 1; prev = 1
    for i in range(n):
        if A[i][i] == 0:
            for r in range(i+1, n):
                if A[r][i] != 0: A[i], A[r] = A[r], A[i]; sign = -sign; break
            else: return 0
        for r in range(i+1, n):
            for c in range(i+1, n):
                A[r][c] = (A[r][c]*A[i][i] - A[r][i]*A[i][c]) // prev
        prev = A[i][i]
    return sign*A[n-1][n-1]

def min_gs_norm2(B):
    """min |b_i*|^2 over exact Gram-Schmidt; a lower bound for l(Gamma)^2."""
    Bs = []; out = None
    for v in B:
        w = [Fraction(x) for x in v]
        for u in Bs:
            uu = sum(x*x for x in u)
            mu = sum(x*y for x, y in zip(w, u)) / uu
            w = [x - mu*y for x, y in zip(w, u)]
        Bs.append(w)
        nn = sum(x*x for x in w)
        out = nn if out is None or nn < out else out
    return out

# ------------------------------------------------------------ reduction
def reduce_bound(T, delta, X0, log=print):
    k = len(T)
    ths = [theta(t) for t in T]; pi3 = d_pi()/3
    L = None; X = X0; rounds = 0
    while True:
        Xb = 3*k*X + 1
        S = k*X*X; T0 = Fraction(k*X + Xb, 2)
        # choose C so that l ~ C^{1/(k+1)} comfortably exceeds sqrt(S + T0^2)
        target = (S + T0*T0) * 10**6
        C = 10**(int((k+1)*(math.log10(float(target))/2)) + 4)
        Cd = Decimal(C)
        rowsphi = [int((Cd*th).to_integral_value()) for th in ths] + [int((Cd*pi3).to_integral_value())]
        # basis vectors (columns of M) written as rows: v = unit vector in coordinate i
        Bm = []
        for i in range(k+1):
            row = [1 if j == i else 0 for j in range(k)] + [rowsphi[i]]
            Bm.append(row)
        R = lll(Bm)
        assert abs(det_int(R)) == abs(det_int(Bm)), "LLL output is not a basis of Gamma"
        l2 = min_gs_norm2(R)
        if l2 <= S + T0*T0:
            log(f"      round {rounds}: l^2 not large enough (C = 10^{len(str(C))-1}); stopping")
            break
        rt = Decimal(l2.numerator)/Decimal(l2.denominator) - Decimal(S)
        denom = rt.sqrt() - Decimal(T0.numerator)/Decimal(T0.denominator)
        Lnew = 2*float((2*SQ3*Cd/denom).ln()) + 1e-9
        Xnew = int(Lnew / math.log(min(T))) + 1
        log(f"      round {rounds}: X = {X:.3e} -> ln(x^2+x+1) <= {Lnew:.2f}, H <= {Xnew}")
        rounds += 1
        if L is not None and Lnew >= L - 1e-6:
            L = min(L, Lnew); break
        L = Lnew
        if Xnew >= X: break
        X = Xnew
    return L

# ------------------------------------------------------------ search
def search(T, delta, L):
    """all integers x with x^2+x+1 = 3^delta * T-smooth, and x^2+x+1 <= exp(L)."""
    Ymax = int(math.exp(min(L, 5000))) + 1 if L < 700 else None
    lim = Decimal(L).exp()
    limI = int(lim) + 1
    out = set(); base = 3 if delta else 1; Tl = list(T)
    def rec(i, m):
        if i == len(Tl):
            N = base*m; dd = 4*N - 3; r = isqrt(dd)
            if r*r == dd:
                x = (r-1)//2; out.add(x); out.add(-1-x)
            return
        v = m
        while base*v <= limI: rec(i+1, v); v *= Tl[i]
    rec(0, 1)
    return sorted(out)

def solve_complete(T, delta, log=print):
    T = tuple(sorted(T))
    X0, info = matveev_X0(T, delta)
    log(f"   T = {list(T)}, delta = {delta}: Matveev gives H <= {X0:.3e} (omega = {info['omega']:.3e})")
    L = reduce_bound(T, delta, X0, log)
    if L is None: raise RuntimeError("reduction failed")
    L = max(L, math.log(12))           # below |z| = 2 sqrt 3 the bound on |Lambda| is not used
    sols = search(T, delta, L)
    log(f"      exhaustive search to x^2+x+1 <= e^{L:.1f}: {len(sols)//2} solution pairs")
    return sols, L

# ------------------------------------------------------------ validation and use
def identity_check(T, delta, x):
    """Lambda = Log(z/zbar) must equal sum e_t theta_t + b0 pi/3 for some signs."""
    N = x*x + x + 1
    c = []
    for t in T:
        e = 0
        while N % t == 0: N //= t; e += 1
        c.append(e)
    th_z = reduce_pi(2*d_atan2(-SQ3/2, Decimal(x) + Decimal(1)/2))   # z = x - w
    ths = [theta(t) for t in T]; pi3 = d_pi()/3
    best = None
    for mask in range(2**len(T)):
        s = sum(((-1 if mask >> i & 1 else 1)*c[i])*ths[i] for i in range(len(T)))
        b0 = ((th_z - s)/pi3).to_integral_value()
        res = abs(th_z - s - b0*pi3)
        best = res if best is None or res < best else best
    return best

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if mode == "validate":
        print("V1. Identity Lambda = sum e_t theta_t + b0 pi/3 on known solutions (residual):")
        for T, x in [((7,), 18), ((7,), 2), ((7, 13, 19), 653), ((7, 13, 19, 31), 191),
                     ((7, 19, 31), 11), ((13,), 3)]:
            r = identity_check(T, 0, x)
            print(f"   T = {T}, x = {x}: residual {float(r):.1e}")
            assert r < Decimal("1e-400")
        print("V2. Rank one against the Skolem solver of script 32 (independent method):")
        import importlib.util
        spec = importlib.util.spec_from_file_location("sk", os.path.join(os.path.dirname(os.path.abspath(__file__)), "32_skolem.py"))
        sk = importlib.util.module_from_spec(spec); spec.loader.exec_module(sk)
        for p in (7, 13, 19, 31, 43, 61, 73, 97):
            for delta in (0, 1):
                sols, L = solve_complete((p,), delta, log=lambda *a: None)
                ref, st = sk.solve([3] if delta else [], p)
                refx = sorted({x for c, x in ref})
                print(f"   p = {p:>3}, delta = {delta}: Baker+LLL {[x for x in sols if x >= 0]}   Skolem {[x for x in refx if x >= 0]}")
                assert sols == refx, "DISAGREE"
        print("   all agree.")
        print("V3. Multi-prime sets against a direct search to 10^150:")
        for T in ((7, 13), (7, 13, 19), (7, 13, 19, 31)):
            sols, L = solve_complete(T, 0)
            direct = search(T, 0, 150*math.log(10))
            print(f"      direct search to 10^150: {[x for x in direct if x >= 0]}")
            print(f"      Baker+LLL (complete):   {[x for x in sols if x >= 0]}")
            assert set(direct) <= set(sols) and (L > 150*math.log(10) or set(sols) == set(direct))
        print("VALIDATION PASSED")
    elif mode == "residual":
        from itertools import chain
        named = [(7,13,19,37,67), (7,13,19,37,127), (7,13,19,43,127), (7,13,19,127,409),
                 (7,13,19,127,1723), (7,13,19,31,127), (7,13,19,31,331),
                 (7,13), (13,61,151), (13,61,157), (7,13,19), (13,61,157,8269), (7,13,19,127)]
        caseB = [(7,13), (13,61,151), (13,61,157), (13,61,28057), (7,13,19)]
        print("NAMED SETS: complete Sm(T) = { x prime, x = 2 mod 3, x^2+x+1 T-smooth }")
        for T in named:
            sols, L = solve_complete(T, 0)
            sm = [x for x in sols if x >= 5 and x % 3 == 2 and isprime(x)]
            print(f"      Sm(T) complete = {sm}")
        print()
        print("CASE B: complete { t prime, t = 1 mod 3, (t^2+t+1)/3 S-smooth }")
        for S in caseB:
            sols, L = solve_complete(S, 1)
            tb = [x for x in sols if x > 1 and x % 3 == 1 and isprime(x)]
            print(f"      solutions t = {tb}")
