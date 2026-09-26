#!/usr/bin/env python3
"""
Exact solution of  x^2 + x + 1 = D * p^c  (one unknown exponent), for ALL c.

Several search bounds of section 13d are single-exponent equations of this
shape.  They are rank-one S-unit equations in Z[w] (w = primitive cube root of
unity), and Skolem's p-adic method settles them completely with integer
arithmetic.  No Baker bound and no lattice reduction are needed; those enter
only when two or more exponents are free.

REDUCTION.  N(x - w) = x^2 + x + 1, where N(a + b w) = a^2 - ab + b^2, and Z[w] is
a UFD with units +-1, +-w, +-w^2.  For a split prime q = pi * conj(pi), pi and
conj(pi) cannot both divide x - w, since then q | x - w, but the w-coefficient
is -1.  And v_3(x^2+x+1) <= 1, the 3-part being (1 - w).  So

        x - w  =  eps * gamma * pi^c,

where eps is one of 6 units, gamma is the product of the fixed primes over D
(each with a choice of conjugate), and pi is one of the two primes over p.
Writing z_c = eps*gamma*pi^c = A_c + B_c w, the equation is  B_c = -1,  with
x = A_c.  Multiplication by pi is an integer 2x2 matrix M (det M = p), so
B_c is an integer linear recurrence and the problem is: for which c >= 0 is
B_c = -1?  Finitely many forms (eps, conjugate choices), each handled below.

SKOLEM / STRASSMANN.  Let l >= 5 be a prime, l != p, and L the order of M mod l,
so X := M^L - I = 0 (mod l).  For t in Z_l, M^(Lt) = exp(t*Lam), Lam = log(I+X),
and on the class c = c0 + L t

        f(t) := B_{c0+Lt} + 1 = sum_k  e2^T Lam^k z_{c0} t^k / k!    (+1 in k=0).

  k = 0 coefficient: B_{c0} + 1.
  k = 1 coefficient: e2^T Lam z_{c0} = B_{c0+L} - B_{c0}  (mod l^2), because
          X^k/k = 0 (mod l^2) for k >= 2 (l >= 5), so Lam = X (mod l^2).
  k >= 2: valuation >= k - v_l(k!) > k - (k-1)/(l-1) >= 3/2, hence >= 2.

Strassmann's theorem (the number of zeros in Z_l of a convergent power series is
at most the largest index attaining the minimum coefficient valuation) gives:
  * B_{c0}+1 not = 0 (mod l)                         -> NO c in the class   (EMPTY)
  * B_{c0}+1 = 0 (mod l), B_{c0+L}-B_{c0} exactly div. by l^1 -> AT MOST ONE (ONE)
  * otherwise                                         -> this l says nothing

A class c = r (mod Mod), Mod a common multiple of the L's used, is SETTLED when
some l makes its l-class EMPTY, or makes it ONE and a known solution s lies in
that l-class: then s is the only solution in the l-class, so the r-class holds
{s} or nothing.  If every r (mod Mod) is settled, the solution list found by
direct search is COMPLETE, for all c.  If any class is not settled, the script
says so and claims nothing.

VALIDATION.  Script 26 searched x^2+x+1 = p^c for every prime p = 1 (mod 3) below
200 and c <= 1200 and found only c = 1, plus (18, c=3) for p = 7.  This script
must reproduce exactly that list, and now for all c, before being trusted on the
new equations.
"""
import sys
from math import gcd, isqrt

# --------------------------------------------------------- Eisenstein integers
def emul(z1, z2):
    a, b = z1; c, d = z2
    return (a*c - b*d, a*d + b*c - b*d)
def econj(z):
    a, b = z
    return (a - b, -b)
def enorm(z):
    a, b = z
    return a*a - a*b + b*b
UNITS = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]   # 1,-1,w,-w,w^2,-w^2
ONE_MINUS_W = (1, -1)
assert all(enorm(u) == 1 for u in UNITS) and enorm(ONE_MINUS_W) == 3

def eis_prime(q):
    """pi with N(pi) = q, for a prime q = 1 (mod 3)."""
    for b in range(1, isqrt(4*q//3) + 2):
        # a^2 - a b + b^2 = q  ->  a = (b + sqrt(4q - 3b^2)) / 2
        disc = 4*q - 3*b*b
        if disc < 0: break
        r = isqrt(disc)
        if r*r == disc and (b + r) % 2 == 0:
            z = ((b + r)//2, b)
            assert enorm(z) == q
            return z
    raise ValueError(q)

def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for b in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(b, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

# --------------------------------------------------------- the forms
def forms(Dfactors, p):
    """All starting values z_0 = eps*gamma and multipliers pi for
       x^2+x+1 = (prod of norms of Dfactors) * p^c.
       Dfactors: list of rational primes in D (3 or q = 1 mod 3, each to power 1)."""
    choices = [[(1, 0)]]
    for q in Dfactors:
        if q == 3: opts = [ONE_MINUS_W]
        else:
            g = eis_prime(q); opts = [g, econj(g)]
        choices = [c + [o] for c in choices for o in opts]
    pi = eis_prime(p)
    out = []
    for ch in choices:
        gamma = (1, 0)
        for f in ch: gamma = emul(gamma, f)
        for eps in UNITS:
            for P in (pi, econj(pi)):
                out.append((emul(eps, gamma), P))
    return out

def B_seq_mod(z0, P, n, m):
    """B_c mod m for c = 0..n-1"""
    a, b = z0[0] % m, z0[1] % m
    u, v = P
    out = []
    for _ in range(n):
        out.append(b)
        a, b = (a*u - b*v) % m, (a*v + b*u - b*v) % m
    return out

def mat_pow_mod(P, e, m):
    u, v = P
    R = ((1, 0), (0, 1)); A = ((u % m, (-v) % m), (v % m, (u - v) % m))
    def mm(X, Y):
        return tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(2)) % m
                           for j in range(2)) for i in range(2))
    while e:
        if e & 1: R = mm(R, A)
        A = mm(A, A); e >>= 1
    return R

def order_dividing(P, l, Mod):
    """order of M mod l if it divides Mod, else None"""
    I = ((1, 0), (0, 1))
    if mat_pow_mod(P, Mod, l) != I: return None
    L = Mod
    for q in prime_factors(Mod):
        while L % q == 0 and mat_pow_mod(P, L//q, l) == I: L //= q
    return L

def prime_factors(n):
    f = []; d = 2
    while d*d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: f.append(n)
    return f

# --------------------------------------------------------- one form, exactly
def known_solutions(z0, P, CKNOWN):
    z = z0; out = []
    for c in range(CKNOWN + 1):
        if z[1] == -1: out.append((c, z[0]))
        z = emul(z, P)
    return out

def classify(z0, P, l, L):
    """per class c0 mod L: 'E' empty, 'O' at most one, '?' inconclusive"""
    m = l*l
    B = B_seq_mod(z0, P, 2*L, m)
    cl = []
    for c0 in range(L):
        k0 = (B[c0] + 1) % m
        if k0 % l: cl.append('E'); continue
        k1 = (B[c0 + L] - B[c0]) % m
        cl.append('O' if (k1 % l == 0 and k1 % m != 0) else '?')
    return cl

def solve_form(z0, P, p, Mods, lmax=4000, CKNOWN=60):
    known = known_solutions(z0, P, CKNOWN)
    for Mod in Mods:
        info = []
        for l in range(5, lmax):
            if not isprime(l) or l == p: continue
            L = order_dividing(P, l, Mod)
            if L is None: continue
            info.append((l, L, classify(z0, P, l, L)))
        unsettled = []
        for r in range(Mod):
            ok = False
            for (l, L, cl) in info:
                s = cl[r % L]
                if s == 'E': ok = True; break
                if s == 'O' and any((c - r) % L == 0 for c, _ in known):
                    ok = True; break
            if not ok: unsettled.append(r)
        if not unsettled:
            return known, Mod, len(info)
    return known, None, unsettled

MODS = [720, 5040, 10080, 55440, 110880]

def solve(Dfactors, p, verbose=False):
    """complete list of x with x^2+x+1 = D p^c (all c >= 0), or raise."""
    D = 1
    for q in Dfactors: D *= q
    sols = set()
    for z0, P in forms(Dfactors, p):
        known, Mod, extra = solve_form(z0, P, p, MODS)
        if Mod is None:
            return None, f"UNSETTLED classes {extra[:10]}"
        for c, x in known:
            assert x*x + x + 1 == D * p**c
            sols.add((c, x))
    return sorted(sols), "complete"

if __name__ == "__main__":
    print("=" * 76)
    print("VALIDATION: reproduce script 26 (x^2+x+1 = p^c, p < 200), now for ALL c")
    print("=" * 76)
    ok = True
    for p in [q for q in range(7, 200) if q % 3 == 1 and isprime(q)]:
        sols, status = solve([], p)
        pos = sorted((c, x) for c, x in sols if x >= 2) if sols else None
        print(f"   p = {p:>3}: {status:9s} x >= 2 : {pos}")
        if sols is None: ok = False; continue
        expect_c1 = [(1, x) for x in range(2, 20) if x*x + x + 1 == p]
        expect = expect_c1 + ([(3, 18)] if p == 7 else [])
        if pos != expect: ok = False; print("      MISMATCH with script 26:", expect)
    print("   reproduction:", "EXACT" if ok else "FAILED")
    if not ok: sys.exit(1)

    print()
    print("=" * 76)
    print("THE EQUATIONS OF SECTION 13 WITH ONE FREE EXPONENT")
    print("=" * 76)
    todo = [
        ("x^2+x+1 = 13^c        (Sm({13}), section 11c)",        [],       13),
        ("x^2+x+1 = 3*13^c      (13a; uncoupled branch of 13b)", [3],      13),
        ("x^2+x+1 = 3*61^c      (13b, 13 ordinary, i = 0)",      [3],      61),
        ("x^2+x+1 = 39*61^c     (13b, 13 ordinary, i = 1)",      [3, 13],  61),
        ("x^2+x+1 = 61^c        (count for T = {13,61})",        [],       61),
        ("x^2+x+1 = 13*61^c     (count for T = {13,61})",        [13],     61),
        ("x^2+x+1 = 97^c        (count for T = {13,61,97})",     [],       97),
        ("x^2+x+1 = 61*97^c     (count for T = {13,61,97})",     [61],     97),
    ]
    for label, Df, p in todo:
        sols, status = solve(Df, p)
        print(f"   {label}")
        print(f"        {status}; all integer x (both x and -1-x): {sols}")

    print()
    print("CROSS-CHECK: each list above against a direct 4Dp^c - 3 = square search,")
    print("c <= 400 (independent of the p-adic argument).")
    for label, Df, p in todo:
        D = 1
        for q in Df: D *= q
        sols, _ = solve(Df, p)
        direct = []
        for c in range(401):
            d = 4*D*p**c - 3
            r = isqrt(d)
            if r*r == d: direct += [(c, (r-1)//2), (c, -(r+1)//2)]
        assert sorted(direct) == sols, (label, direct, sols)
    print("   all eight agree.")

    print()
    print("MUTATION TEST: hide the solution x = 18 (c = 3) of x^2+x+1 = 7^c by")
    print("capping the known-solution search at c <= 2.  The solver must NOT")
    print("report the truncated list as complete.")
    refused = 0
    for z0, P in forms([], 7):
        known, Mod, extra = solve_form(z0, P, 7, MODS, CKNOWN=2)
        full, _, _ = solve_form(z0, P, 7, MODS, CKNOWN=60)
        if any(c == 3 for c, _ in full):
            assert Mod is None, "solver accepted a list missing a solution"
            refused += 1
    print(f"   forms containing the hidden solution: {refused}; all refused -> sound")
    assert refused > 0
