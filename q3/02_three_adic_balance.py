#!/usr/bin/env python3
"""
q = 3, second pass: the exact 3-adic balance, a parity constraint on the
3-component, and how much abundancy is left once 3 is present.
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
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def sigma(p,e): return sum(p**i for i in range(e+1))
from fractions import Fraction

print("="*74)
print("1.  v_3 of a component, exactly")
print("="*74)
print("""For p != 3 and n_p = e_p + 1:
  p = 1 (mod 3):  v_3(sigma(p^{e_p})) = v_3(n_p)                    [LTE]
  p = 2 (mod 3):  sigma(p^{e_p}) = sum of n_p terms alternating +-1 mod 3,
                  so v_3 > 0 iff n_p is EVEN, i.e. iff e_p is odd, i.e. iff
                  p is the Euler prime; and then
                  v_3 = v_3(p+1) + v_3(n_p / 2).""")
bad=0; n=0
for p in primes(5,80):
    for e in range(1,26):
        s=sigma(p,e); nn=e+1; got=vp(s,3)
        if p%3==1: pred=vp(nn,3)
        else: pred=(vp(p+1,3)+vp(nn//2,3)) if nn%2==0 else 0
        n+=1
        if got!=pred: bad+=1; print("   FAIL",p,e,got,pred)
print(f"   {n} components checked, {bad} failures -> formulas confirmed")

print()
print("="*74)
print("2.  THE EXACT 3-ADIC BALANCE  (any odd perfect N with 3 | N)")
print("="*74)
print("""      e_3  =  SUM over non-Euler p = 1 (mod 3) of v_3(e_p + 1)   +   E

with  E = v_3(alpha+1)                       if pi = 1 (mod 3),
      E = v_3(pi+1) + v_3((alpha+1)/2)       if pi = 2 (mod 3).

Every non-Euler p = 2 (mod 3) contributes NOTHING.  So the entire 3-adic
supply comes from primes = 1 (mod 3) whose exponent satisfies 3 | e_p + 1,
together with the single Euler component.  This is the q=3 analogue of the
identity q = o_1 + v_3(e+1) proved for the restrained case, without the
'ordinary' hypothesis that made every term there equal to 1.""")

print()
print("="*74)
print("3.  PARITY CONSTRAINT ON THE 3-COMPONENT")
print("="*74)
print("""3^{e+1} = 3 (mod 24) for odd e+1, so sigma(3^e) = (3^{e+1}-1)/2 = 1 (mod 12).
By Lemma 3MOD12 every prime factor is = +-1 (mod 12).  A product of such primes
is = 1 (mod 12) exactly when the number of factors = -1 (mod 12), counted with
multiplicity, is EVEN.  Hence:

   sigma(3^{e_3}) has an EVEN number of prime factors = 11 (mod 12),
   counted with multiplicity.""")
bad=0
for e in range(2,40,2):
    s=sigma(3,e)
    assert s%12==1, e
    m=s; cnt=0; d=5
    while d*d<=m:
        while m%d==0:
            if d%12==11: cnt+=1
            m//=d
        d+=2
    if m>1 and m%12==11: cnt+=1
    if cnt%2: bad+=1; print("   FAIL e=",e)
print(f"   sigma(3^e) = 1 mod 12 and the 11-mod-12 multiplicity is even, for all even e <= 38: {bad} failures")

print()
print("="*74)
print("4.  HOW MUCH ABUNDANCY IS LEFT  (why the q=5..17 method has no analogue)")
print("="*74)
print("The 3-component alone supplies most of the required abundancy of 2:")
for e in (2,4,6,8,100):
    v=Fraction(sigma(3,e),3**e)
    print(f"   e_3 = {e:>3}:  sigma(3^e)/3^e = {float(v):.6f},  leaving "
          f"{float(2/v):.6f} for every other component combined")
print()
P=primes(5,200); v=Fraction(1); k=0
while v<=Fraction(4,3):
    v*=Fraction(P[k],P[k]-1); k+=1
print(f"   prod p/(p-1) over the smallest primes >= 5 exceeds 4/3 after only "
      f"k = {k} primes ({P[:k]})")
print("""
   So the abundancy floor k0(3) = 3 is essentially vacuous.  At q = 5..17 the
   floor grew fast (7, 15, 27, 41, 62) and was the instrument that refuted
   M = 18.  At q = 3 it gives nothing, because 3 itself supplies ~3/2 of the
   factor 2.  Abundancy and lower-prime avoidance BOTH fail here, which is the
   precise sense in which the branch is different.""")
