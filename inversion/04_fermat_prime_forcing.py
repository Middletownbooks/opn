#!/usr/bin/env python3
"""
PROPOSITION E (Fermat-prime forcing) -- free of the minimal-prime hypothesis.

Let N be odd perfect with Euler prime pi and Euler exponent alpha, and let
F | N be a Fermat prime, F in {3,5,17,257,65537}, so F - 1 = 2^s.  Then at
least one of:
  (a) some non-Euler p | N has p = 1 mod F and F | e_p + 1;
  (b) pi = 1 mod F and F | alpha + 1;
  (c) pi = -1 mod F.

PROOF.  F in S, so e_F > 0 and the F-adic valuation balance
e_F = sum_{p != F} v_F(sigma(p^{e_p})) forces an F-input witness p, i.e.
ord_F(p) | n_p (order-one convention: F | n_p).  Now ord_F(p) | F - 1 = 2^s,
so ord_F(p) is a power of 2.
 - p non-Euler: n_p = e_p + 1 is odd (Euler form), so the only power of 2
   dividing it is 1; hence ord_F(p) = 1, giving p = 1 mod F and F | n_p: case (a).
 - p = pi: n_pi = alpha + 1 = 2 mod 4, so v_2(n_pi) = 1 and ord_F(pi) is 1 or 2.
   ord = 1 gives case (b); ord = 2 gives pi = -1 mod F, case (c).   QED

CONSEQUENCE OF CASE (a).  p = 1 mod F and F | n_p give Phi_F(p) | sigma(p^{e_p}),
and LTE gives v_F(Phi_F(p)) = 1.  Any prime r | Phi_F(p)/F has ord_r(p) = F,
so r = 1 mod F and r > F.  Hence N acquires a support prime >= L(F), and
e_p >= F - 1 contributes F - 1 to Omega(N).

This is the paper's q = 5 and q = 17 forced-or-pure mechanism, but with the
hypothesis 'F is the SMALLEST prime factor' removed.  It applies to any
Fermat prime dividing N.  That the paper's two three-child branches are
exactly q = 5 and q = 17 is not a coincidence: 5 and 17 are the only Fermat
primes in {5,7,11,13,17}, and a branch has exactly 3 first-input children iff
q - 1 is a power of 2 (Theorem 1 with mu = 1).
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def L(F):
    r=F+1
    while not isprime(r): r+=F
    return r
print(__doc__)
print("Fermat primes and their forced endpoints L(F) = least prime r > F, r = 1 mod F:")
for F in (3,5,17,257,65537):
    lf=L(F)
    print(f"   F={F:>6}   L(F) = {lf:<8} (= {(lf-1)//F}*F + 1)   case (a) forces "
          f"e_p >= {F-1}, so Omega(N) >= {F-1}")
print()
print("So, unconditionally on the minimal prime:")
print("   257   | N  =>  pi = +-1 mod 257 (with the stated exponent condition),")
print("                  or Omega(N) >= 256 and N has a prime factor >= %d." % L(257))
print("   65537 | N  =>  pi = +-1 mod 65537 (likewise),")
print("                  or Omega(N) >= 65536 and N has a prime factor >= %d." % L(65537))
print()
print("Sanity check of the LTE step v_F(Phi_F(p)) = 1 for p = 1 mod F:")
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
bad=0
for F in (3,5,17):
    for p in range(3,4000):
        if not isprime(p) or p%F!=1: continue
        Phi=sum(p**i for i in range(F))        # Phi_F(p) for F prime
        if vp(Phi,F)!=1: bad+=1; print("   FAIL",F,p)
print(f"   checked all primes p = 1 mod F up to 4000 for F = 3,5,17: {bad} failures")
