#!/usr/bin/env python3
"""
PILOT: can an upper-bound (Selberg) sieve push the section-4 bound of Ochem-Zelinsky
far beyond what brute force reaches?  (NOTES_RESTRAINED.md 4g.)

THE IDEA.  The section-4 count needs only an UPPER bound on
    ln A(z) = sum over Algorithm-1 survivors 3e6 < r <= z of ln(r/(r-1)).
Every survivor avoids M2 at its time, and M2 contains the initial set
    S = { primes q = 1 (mod 3), 7 <= q < 3e6 },
so every survivor lies in the STATIC set
    T = { primes r : no q in S divides r^2 + r + 1 }.
Hence  ln A(z) <= ln A(z0) + sum_{r in T, z0 < r <= z} 1/(r-1).
Here ln A(z0) is an upper bound from an actual run: the superset run to z0 = 1e12
(restrained/runs/13_1e12_Q2e35_checkpoints.txt).  T is counted on dyadic intervals
(x, 2x] by the Selberg upper-bound sieve.

THE SIEVE.  A = the integers n in (x, 2x], so X = x.  Sieve by every prime p < xi:
  * omega(p) = 3 for p in S: the classes 0, rho and rho^2 mod p, with rho a cube root of 1;
  * omega(p) = 1 for all other p: the class 0.
A prime r in T with r > xi survives the sieve.  |A_d| = X omega(d)/d + R_d with
|R_d| <= omega(d), since there are omega(d) residue classes mod d, each contributing
X/d up to an error below 1.  Selberg's Lambda^2 bound (proof in NOTES_RESTRAINED 4g):
    #{sifted n} <= X / G(xi) + E(xi),
    G(xi) = sum over squarefree d < xi (all p | d below xi) of g(d),  g(p) = omega(p)/(p - omega(p)),
    E(xi) = (sum_{d < xi} mu^2(d) omega(d))^2 <= (xi (1 + ln xi)^2)^2,
the last because omega(d) <= tau_3(d) and sum_{d<y} tau_3(d) <= y (1 + ln y)^2.

A LOWER BOUND FOR G(xi) at any xi, without enumerating d < xi.  Write d = b a, with
b | prod(S) and (a, prod S) = 1.  For p outside S, g(p) = 1/(p-1) = 1/phi(p), so
    G(xi) = sum_b g(b) sum_{a < xi/b, (a, P_S) = 1} mu^2(a)/phi(a)
          >= sum_{b < B} g(b) * prod_{q in S} (1 - 1/q) * ln(xi/b).
This uses the lemma:  sum_{a<y, (a,m)=1} mu^2(a)/phi(a) >= (phi(m)/m) ln y  (proof in
4g).  Truncating at b < B only lowers the bound.

THIS IS A PILOT.  Floating point is used throughout; a final version would use outward
rounding.  Its outputs are:
  (1) sanity checks: exact G against the lower bound at small xi, and the sieve bound
      against a brute-force count on a small instance;
  (2) the bound against the TRUE count of T on (x, 2x] where it is known (static-set
      runs of 13_sieve.c with Q = 3e6);
  (3) a PROJECTION: the rigorous-in-principle ln A upper bound carried from z0 = 1e12,
      and the q bound it would give.

Run:  python3 16_selberg_pilot.py [static-run-output]
"""
import sys, math, os, bisect

D = 3_000_000
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[:2] = b"\0\0"
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = bytearray(len(range(i*i, n + 1, i)))
    return s
ISP = primes_upto(D)
SPEC = [q for q in range(7, D) if ISP[q] and q % 3 == 1]
LOG_PHI_RATIO = math.fsum(math.log1p(-1.0 / q) for q in SPEC)   # ln prod_S (1 - 1/q)
PHI_RATIO = math.exp(LOG_PHI_RATIO)

# ---- the b-sum: squarefree b < B made of S-primes, weight g(b) = prod 3/(q-3) ----
def b_terms(B):
    out = []                                   # (b, g(b))
    def rec(start, b, g):
        out.append((b, g))
        for i in range(start, len(SPEC)):
            q = SPEC[i]
            if b * q >= B: break
            rec(i + 1, b * q, g * 3.0 / (q - 3))
    rec(0, 1, 1.0)
    return out
BTERMS = None; BKEYS = None; PRE_G = None; PRE_GL = None
BTERMS_B = [0]
def G_low(xi, B=10**8):
    """PHI_RATIO * sum_{b < min(xi, B)} g(b) ln(xi/b), via prefix sums"""
    global BTERMS, BKEYS, PRE_G, PRE_GL
    if BTERMS is None:
        BTERMS = sorted(b_terms(B)); BTERMS_B[0] = B
        BKEYS = [b for b, _ in BTERMS]
        PRE_G, PRE_GL = [0.0], [0.0]
        for b, g in BTERMS:
            PRE_G.append(PRE_G[-1] + g); PRE_GL.append(PRE_GL[-1] + g * math.log(b))
    i = bisect.bisect_left(BKEYS, xi)
    return PHI_RATIO * (math.log(xi) * PRE_G[i] - PRE_GL[i])

def E_up(xi): return (xi * (1 + math.log(xi)) ** 2) ** 2

def omega(p): return 3 if (p in SPECSET) else 1
SPECSET = set(SPEC)

def G_exact(xi):
    """sum over squarefree d < xi of g(d), by a smallest-prime-factor sieve"""
    n = int(xi)
    spf = list(range(n))
    for i in range(2, math.isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n, i):
                if spf[j] == j: spf[j] = i
    g = [0.0] * n; g[1] = 1.0; tot = 1.0
    for d in range(2, n):
        p = spf[d]; m = d // p
        if m % p == 0: continue                # not squarefree: g = 0
        w = omega(p); g[d] = g[m] * w / (p - w); tot += g[d]
    return tot

def selberg_bound(x):
    """best of X/G_low(xi) + E_up(xi) over a grid of xi; returns (bound, xi)"""
    best = None
    lo = 10.0; hi = math.sqrt(x)
    t = lo
    while t <= hi:
        v = x / G_low(t) + E_up(t)
        if best is None or v < best[0]: best = (v, t)
        t *= 1.25
    return best

if __name__ == "__main__":
    print(f"|S| = {len(SPEC)} primes q = 1 (mod 3) in [7, 3e6);  prod_S (1-1/q) = {PHI_RATIO:.6f}")
    full = math.exp(math.fsum(math.log1p(3.0 / (q - 3)) for q in SPEC))
    asym = math.exp(math.fsum(math.log((q - 1) / (q - 3)) for q in SPEC))
    print(f"prod_S (1 + g(q)) = {full:.4f};  prod_S (q-1)/(q-3) = {asym:.4f}  "
          f"(the constant C in G(xi) ~ C ln xi)")

    print("\n(1a) exact G(xi) >= the lower bound G_low(xi):")
    for xi in (10**3, 10**4, 10**5, 10**6):
        ge, gl = G_exact(xi), G_low(xi)
        print(f"     xi = {xi:>8,d}:  G = {ge:10.4f}   G_low = {gl:10.4f}   ok = {ge >= gl}")
    covered = sum(g for b, g in BTERMS)
    print(f"     b-terms below B = {BTERMS_B[0]:.0e}: {len(BTERMS):,}; sum g(b) = {covered:.4f} "
          f"of the full product {full:.4f}")

    print("\n(1b) brute force on a small instance: n in (x, 2x], x = 2e6, sieving to xi")
    x = 2_000_000
    for xi in (50, 200, 1000):
        ps = [p for p in range(2, xi) if ISP[p]]
        roots = {}
        for p in ps:
            if p in SPECSET:
                rho = next(pow(g, (p - 1) // 3, p) for g in range(2, p) if pow(g, (p - 1) // 3, p) != 1)
                roots[p] = (0, rho, p - 1 - rho)
            else:
                roots[p] = (0,)
        cnt = sum(1 for n in range(x + 1, 2 * x + 1) if all(n % p not in roots[p] for p in ps))
        ge = G_exact(xi); tot_w = 0
        # exact error term: (sum_{d<xi} mu^2 omega(d))^2
        spf = list(range(xi));
        for i in range(2, math.isqrt(xi) + 1):
            if spf[i] == i:
                for j in range(i * i, xi, i):
                    if spf[j] == j: spf[j] = i
        w = [0] * xi; w[1] = 1; s = 1
        for d in range(2, xi):
            p = spf[d]; m = d // p
            if m % p == 0: continue
            w[d] = w[m] * omega(p); s += w[d]
        bound = x / ge + s * s
        print(f"     xi = {xi:5d}: sifted count {cnt:,}  <=  Selberg bound {bound:,.0f} ?  {cnt <= bound}")

    print("\n(2) bound versus the TRUE count of T on (x, 2x]")
    true = {}
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        for line in open(sys.argv[1]):
            if line.startswith("CP"):
                f = dict(kv.split("=") for kv in line.split()[1:])
                true[int(f["x"])] = int(f["k"])
    for x in (10**9, 2 * 10**9, 5 * 10**9, 10**10):
        if x in true and 2 * x in true:
            tc = true[2 * x] - true[x]
            b, xi = selberg_bound(x)
            print(f"     x = {x:.0e}: true {tc:,}   bound {b:,.0f} (xi = {xi:,.0f})   ratio {b / tc:.2f}")
    if not true: print("     (no static run supplied)")

    print("\n(3) PROJECTION from z0 = 1e12")
    lnA0 = 0.0503326399823567378172          # superset run, runs/13_1e12_Q2e35_checkpoints.txt
    c = math.log(2 / (1.5 * (1 + 1 / 6e6)))
    x = 1e12; lnA = lnA0; best = None
    print(f"     {'z':>10s} {'bound/x':>10s} {'ratio to ~2c/ln x':>18s} {'ln A_up(z)':>11s} {'K_max ~':>11s} {'q >= ~':>10s}")
    while True:
        b, xi = selberg_bound(x)
        inc = b / x
        lnA += inc; z = 2 * x
        if lnA >= c: break
        K = (c - lnA) / math.log1p(1 / z)
        q = K / 2
        if best is None or q > best[0]: best = (q, z, lnA)
        if math.log10(z) % 3 < math.log10(2):
            heur = 0.113 / math.log(x)           # heuristic: ~11.3% of the ~x/ln x primes in (x, 2x], each ~1/x
            print(f"     {z:10.2e} {inc:10.3e} {inc / heur:18.2f} {lnA:11.5f} {K:11.3e} {q:10.3e}")
        x = z
        if z > 1e80: break
    print(f"\n     best projected bound: q >= ~{best[0]:.3e} at z ~ {best[1]:.2e} (ln A_up = {best[2]:.4f}, c = {c:.4f})")
