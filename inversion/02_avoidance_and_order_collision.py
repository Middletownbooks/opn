#!/usr/bin/env python3
"""
Sharp lower-prime avoidance, and the order-collision lemma driving the
inversion.  Section 0 re-verifies the paper's Lemma 3.2 by brute force, since
everything below rests on it.
"""
def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True
def primes(lo, hi):
    return [p for p in range(lo, hi) if isprime(p)]
def vp(n, p):
    v = 0
    while n % p == 0: n //= p; v += 1
    return v
def order(p, l):
    """ord_l(p) for l prime, l does not divide p"""
    x, k = p % l, 1
    while x != 1:
        x = (x*p) % l; k += 1
    return k
def sigma_pe(p, e):
    return sum(p**i for i in range(e+1))
def oddpart(n):
    while n % 2 == 0: n //= 2
    return n
def divisors(n):
    return sorted(d for d in range(1, n+1) if n % d == 0)

print("=== 0. Brute-force check of the paper's Lemma 3.2 (cyclotomic input condition) ===")
print("Claim: for odd prime l, p != l, n = e+1:  v_l(sigma(p^e)) > 0  iff")
print("       (ord_l(p) > 1 and ord_l(p) | n)  or  (ord_l(p) = 1 and l | n).")
bad = 0; tested = 0
for l in primes(3, 30):
    for p in primes(3, 60):
        if p == l: continue
        d = order(p, l)
        for e in range(1, 40):
            n = e + 1
            lhs = vp(sigma_pe(p, e), l) > 0
            rhs = (d > 1 and n % d == 0) or (d == 1 and n % l == 0)
            tested += 1
            if lhs != rhs:
                bad += 1
                if bad < 5: print(f"   MISMATCH l={l} p={p} e={e}")
print(f"   {tested} cases tested, {bad} mismatches -> Lemma 3.2 confirmed as stated.")

print()
print("=== 1. THEOREM 2 (sharp lower-prime avoidance) ===")
print("""Let N be odd perfect, q = min S, and let l < q be an odd prime.  For every
p in S with n_p = e_p + 1 and d_l = ord_l(p):
   d_l = 1  (p = 1 mod l)  ==>  l  does not divide n_p
   d_l > 1                 ==>  d_l does not divide n_p
For NON-EULER p, n_p is odd, so the second condition is vacuous unless d_l is
odd, i.e. unless d_l divides mu_l := oddpart(l-1).
For the EULER prime pi, n_pi = 2 mod 4, so the second condition is vacuous
unless v_2(d_l) <= 1, i.e. unless d_l divides 2*mu_l.""")
print()
print("COROLLARY 2a (Euler residue restriction).  For every odd prime l < q,")
print("     pi  !=  -1  (mod l).")
print("Proof: pi = -1 mod l gives ord_l(pi) = 2 (l odd > 2), and 2 | n_pi since")
print("n_pi = 2 mod 4, so ord_l(pi) | n_pi: pi is an l-input, contradicting")
print("avoidance.  QED   [generalises the paper's Proposition 9.2, proved there")
print("only for q = 5, l = 3]")
print()
print("Density of Euler residue classes surviving Corollary 2a, by branch:")
from fractions import Fraction
for q in primes(5, 32):
    ls = primes(3, q)
    dens = Fraction(1)
    for l in ls: dens *= Fraction(l-2, l-1)
    mod = 1
    for l in ls: mod *= l
    print(f"   q={q:>3}: l<q = {str(ls):<24} surviving fraction = {dens} "
          f"= {float(dens):.4f}  (mod {mod})")

print()
print("=== 2. LEMMA OC (order collision) ===")
print("""Let p in S and let d divide n_p.  Then for every odd prime l < q:
   (a) if p = 1 mod l  then  l does not divide d;
   (b) if d_l = ord_l(p) > 1  then  d_l does not divide d.
Proof: if l | d then l | n_p, contradicting Theorem 2; if d_l | d then
d_l | n_p, likewise.  QED

Why this is the engine.  Every r in S must be PRODUCED: e_r > 0 and the
r-adic balance e_r = sum_{p != r} v_r(sigma(p^{e_p})) forces some p in S with
ord_r(p) | n_p (order-one convention: r | n_p).  Writing d = ord_r(p), the
production order d must divide r-1 AND divide n_p, so Lemma OC restricts it.
Production is thus a covering problem constrained by avoidance -- the opposite
direction from an upper abundancy envelope, which Proposition A of the audit
showed can never close anything.""")

print()
print("=== 3. Forced-prime endpoints L(q) for the order-one child, all q ===")
print("In the child N_1 (or E_1) the witness x satisfies x = 1 mod q and q | n_x,")
print("so Phi_q(x) | sigma(x^{e_x}); LTE gives v_q(Phi_q(x)) = 1; and every prime")
print("r | Phi_q(x)/q has ord_r(x) = q, hence r = 1 mod q and r > q.  So the")
print("forced support prime is at least L(q) := least prime r > q with r = 1 mod q.")
print()
print(f"{'q':>4} {'L(q)':>7} {'candidates r=1 mod q in (q,L(q)) -- ALL of them':>52}")
for q in primes(5, 60):
    r = q + 1            # k=1 counts: q+1 > q and q+1 = 1 mod q
    cands = []
    while not isprime(r):
        cands.append(r); r += q
    print(f"{q:>4} {r:>7} {str(cands):>52}")
print()
print("The k=1 candidate r = q+1 is always EVEN (q odd), hence never prime, so")
print("omitting it can never change L(q).  That explains -- and mathematically")
print("excuses -- the release certificate's and Table 6's candidate list")
print("[35,52,69,86] for q=17, which drops 18.  The claim L(17)=103 is correct.")
print("The audit point stands unchanged: the verifier hardcodes that list and")
print("performs no completeness check, so it would equally accept a list that")
print("dropped a candidate whose omission did matter.")
