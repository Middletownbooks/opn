#!/usr/bin/env python3
"""
q = 3: what survives, and a replacement constraint.

SETTING.  N odd perfect, N = pi^alpha m^2 with pi = alpha = 1 (mod 4).  Since
3 = 3 (mod 4), 3 is never the Euler prime, so e_3 is EVEN whenever 3 | N.
Write n_p = e_p + 1; n_p is odd for every non-Euler p, and n_pi = 2 (mod 4).

WHAT DIES AT q = 3.  Lower-prime avoidance (the engine of the whole
minimal-prime programme) says: for every odd prime l < q and every p | N,
v_l(sigma(p^{e_p})) = 0.  For q = 3 the set of odd primes below q is EMPTY, so
the hypothesis is vacuous and every downstream tool built on it dies:
Corollary 2e (exponent floors), Lemma OC (order collision), the forbidden-set
machinery, and the residue restrictions on pi.  This is exactly why the branch
is structurally different, and it is not a gap in anyone's argument.

WHAT SURVIVES.  Everything that needs only Euler's form and valuation balance:
  - the valuation-balance identity;
  - the cyclotomic input condition;
  - Theorem 1' (input classification at every prime divisor), since its proof
    never used minimality;
  - Proposition E, since 3 is a Fermat prime (3 - 1 = 2, so mu(3) = 1).

Below: three constraints that do NOT need lower primes, so they are available
at q = 3, with verification.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def primes(a,b): return [p for p in range(a,b) if isprime(p)]
def order(a,m):
    a%=m; x,k=a,1
    while x!=1: x=(x*a)%m; k+=1
    return k
def legendre(a,p): 
    r=pow(a%p,(p-1)//2,p)
    return -1 if r==p-1 else r
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def sigma(p,e): return sum(p**i for i in range(e+1))

print(__doc__)
print("="*74)
print("LEMMA QR.  Let p be a NON-EULER prime factor of N and r a prime dividing")
print("sigma(p^{e_p}).  Then p is a quadratic residue mod r.")
print("="*74)
print("""PROOF.  p non-Euler => e_p even => n_p odd.  r | sigma(p^{e_p}) => p^{n_p} = 1
(mod r) => ord_r(p) | n_p, so ord_r(p) is odd.  Writing r-1 = 2^a m with m odd
and a >= 1, ord_r(p) | m | (r-1)/2, so p^{(r-1)/2} = 1 (mod r).   QED

Sharpness: when r = 3 (mod 4) we have v_2(r-1) = 1, so oddpart(r-1) = (r-1)/2
and 'ord_r(p) odd' is EQUIVALENT to (p/r) = 1 -- nothing is lost.  For
r = 1 (mod 4) the order condition is strictly stronger than the QR one.""")
bad=0; tested=0
for p in primes(3,60):
    for e in (2,4,6,8):
        s=sigma(p,e)
        for r in primes(3,400):
            if r==p or s%r: continue
            tested+=1
            if legendre(p,r)!=1: bad+=1; print("   FAIL",p,e,r)
print(f"   checked {tested} (p,e,r) instances with e even: {bad} failures")

print()
print("="*74)
print("LEMMA 3MOD12.  If 3 | N then every prime r > 3 dividing sigma(3^{e_3})")
print("satisfies r = +-1 (mod 12).   [needs no 'restrained' hypothesis]")
print("="*74)
print("""PROOF.  3 is never the Euler prime, so e_3 is even and n_3 is odd.  By
Lemma QR, 3 is a quadratic residue mod r, and (3/r) = 1 exactly when
r = +-1 (mod 12).   QED

COROLLARY.  The component 3^{e_3} can never produce a prime = 5 or 7 (mod 12).""")
bad=0
for e in range(2,34,2):
    s=sigma(3,e)
    for r in primes(5,10**5):
        if s%r==0 and r%12 not in (1,11): bad+=1; print("   FAIL e=",e,"r=",r)
print(f"   all prime factors < 1e5 of sigma(3^e) for even e <= 32: {bad} violations")

print()
print("="*74)
print("LEMMA NO2CYCLE.  Let p, s be distinct NON-EULER prime factors of N with")
print("p = s = 3 (mod 4).  Then p and s cannot each produce the other.")
print("="*74)
print("""PROOF.  If s | sigma(p^{e_p}) then (p/s) = 1 by Lemma QR; if p | sigma(s^{e_s})
then (s/p) = 1.  But p = s = 3 (mod 4) makes (p-1)/2 and (s-1)/2 both odd, so
quadratic reciprocity gives (p/s)(s/p) = -1.  Contradiction.   QED

This is a constraint on the PRODUCTION DIGRAPH that survives at q = 3: among
the prime factors congruent to 3 mod 4, production is 2-cycle-free.""")
print()
print("Verification: search for a mutual pair among primes = 3 mod 4 (even")
print("exponents up to 12 on both sides).")
P=[p for p in primes(3,200) if p%4==3]
found=[]
for i,p in enumerate(P):
    for s in P[i+1:]:
        a=any(sigma(p,e)%s==0 for e in range(2,13,2))
        b=any(sigma(s,f)%p==0 for f in range(2,13,2))
        if a and b: found.append((p,s))
print(f"   pairs from {len(P)} primes = 3 mod 4 below 200 : mutual pairs found = {len(found)}")
print(f"   (reciprocity predicts 0)   {found if found else ''}")
print()
print("   worked instance: p=7, s=11, both 3 mod 4.")
print(f"      ord_11(7) = {order(7,11)} (even) -> 11 never divides sigma(7^even); "
      f"(7/11) = {legendre(7,11)}")
print(f"      ord_7(11) = {order(11,7)} (odd)  -> 7 | sigma(11^2) = {sigma(11,2)} = 7*19; "
      f"(11/7) = {legendre(11,7)}")
print(f"      product of Legendre symbols = {legendre(7,11)*legendre(11,7)} = -1, as reciprocity requires.")
