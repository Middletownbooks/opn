#!/usr/bin/env python3
"""
A lemma about the NOTABLE component 3^q of a restrained odd perfect number
that I do not find stated in Ochem-Zelinsky, plus its corollary.

Setting (their Theorem 1): N restrained odd perfect, notable prime n = 3,
notable exponent q >= 4.  q is EVEN (it is one of the even exponents), so q+1
is ODD.  p is the special prime, e the special exponent, e = 1 mod 4.
Ordinary primes are those with exponent exactly 2.

LEMMA A.  Every prime r > 3 dividing sigma(3^q) satisfies r = +-1 (mod 12).

PROOF.  r | sigma(3^q) = (3^{q+1}-1)/2 gives 3^{q+1} = 1 (mod r), so
ord_r(3) | q+1, which is odd; hence ord_r(3) is odd.  Write r-1 = 2^a m with m
odd and a >= 1.  Then ord_r(3) | gcd(m, r-1) = m, and m | (r-1)/2 because
a >= 1.  So 3^{(r-1)/2} = 1 (mod r): 3 is a quadratic residue mod r.  By
quadratic reciprocity (3/r) = 1 exactly when r = +-1 (mod 12).   QED

COROLLARY B.  In such an N, every ordinary prime s = 5 (mod 12) satisfies
v_s(sigma(p^e)) = 2; that is, s^2 divides the special component's divisor sum.

PROOF.  s = 5 mod 12 gives s = 2 mod 3, so s^2+s+1 = 1 mod 3 -- more to the
point, every prime factor of t^2+t+1 is 3 or = 1 (mod 3), so a prime = 2 mod 3
can never be produced by an ordinary component.  (Ochem-Zelinsky use exactly
this step in section 3: "Since 107 = 2 (mod 3), 107 cannot be produced by an
ordinary component.")  By Lemma A it cannot be produced by the notable
component either, since 5 is not +-1 mod 12.  The only remaining component is
the special one, and s is ordinary so e_s = 2 copies are needed.   QED

In particular, if 5 is ordinary then 25 | sigma(p^e); if 17 is ordinary then
17^2 | sigma(p^e); and so on for 29, 41, 53, 89, 101, ...
"""
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
import random,math
def rho(n):
    if n%2==0: return 2
    while True:
        x=random.randrange(2,n); y=x; c=random.randrange(1,n); d=1
        while d==1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n
            d=math.gcd(abs(x-y),n)
        if d!=n: return d
def factor(n,out=None):
    if out is None: out={}
    if n==1: return out
    if isprime(n): out[n]=out.get(n,0)+1; return out
    d=rho(n); factor(d,out); factor(n//d,out); return out

print(__doc__)
print("VERIFICATION of Lemma A: factor sigma(3^q) for even q and check r = +-1 mod 12")
print(f"{'q':>4} {'sigma(3^q)':>22} {'prime factorisation':>44} {'all +-1 mod 12?':>16}")
allok=True
for q in range(4,33,2):
    s=(3**(q+1)-1)//2
    f=factor(s)
    ok=all(r%12 in (1,11) for r in f if r>3)
    allok &= ok
    fs='*'.join(f"{r}^{k}" if k>1 else str(r) for r,k in sorted(f.items()))
    print(f"{q:>4} {s:>22} {fs:>44} {str(ok):>16}")
print(f"\nLemma A holds in every case tested: {allok}")
print()
print("CONTROL -- the evenness of q is essential.  For ODD q, q+1 is even and")
print("the order argument fails.  Factorisations of sigma(3^q) for odd q:")
for q in (1,3,5,7,9):
    s=(3**(q+1)-1)//2
    f=factor(s)
    bad=[r for r in f if r>3 and r%12 not in (1,11)]
    fs='*'.join(f"{r}^{k}" if k>1 else str(r) for r,k in sorted(f.items()))
    print(f"   q={q}: sigma(3^q) = {fs:<40} factors NOT +-1 mod 12: {bad}")
