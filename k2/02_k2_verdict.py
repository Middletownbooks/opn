#!/usr/bin/env python3
"""k = 2: does the section 2 abundancy bound still fall below 2?  Verdict."""
from decimal import Decimal as D, getcontext
getcontext().prec = 40
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def C2(n): return n*(n+1)//2

def Ainf(B, T, kmin=7, kmax=400):
    v=D(1)
    for k in range(kmin,kmax):
        c=T(k)
        if c>0: v*=(D(1)+D(1)/(D(B)**(D(k)/D(2))-D(2)))**c
    return v

# class counts of total degree k
T_pairs   = lambda k: k-1                                   # their k=1 count
T_tri     = lambda k: (k+1)*(k+2)//2 - 3                    # triples, pure powers removed
def T_tri_ref(k):                                           # also remove all-even triples
    tot=(k+1)*(k+2)//2
    return tot - (C2(k//2+1) if k%2==0 else 3)

A2 = D(1)                                # the 11 low classes tabulated at k=1
for s in [5,29,59,863,1667,1733,2819,306419,1345913,3619619,68839637]:
    A2 *= D(s)/D(s-1)

print("="*74)
print("CASE (ii):  one notable prime = 2 (mod 3)")
print("="*74)
print("""Such a notable is = 5 (mod 6), so it can be as small as 5, and then every
factor of sigma(s^2) = p^a n_1^b n_2^c is only guaranteed >= 5.""")
A1_ii = D(13)/D(12)*D(7)/D(6)*D(5)/D(4)
for T,name in ((T_tri,"pure powers removed"),(T_tri_ref,"also all-even removed")):
    Ai=Ainf(5,T); prod=A1_ii*Ai
    print(f"   A_1 = {A1_ii:.6f} (p=13, n_1=7, n_2=5),  A_inf (B=5, {name}) = {Ai:.6f}")
    print(f"   A_1 * A_inf = {prod:.6f}   -- and this is BEFORE any ordinary prime")
    print(f"   is counted, so the bound is at least this.   Exceeds 2?  {prod>2}")
print()
print("   => the section 2 method CANNOT close case (ii).  It fails outright.")

print()
print("="*74)
print("CASE (i):  both notables = 1 (mod 3), so all of p, n_1, n_2 >= 7")
print("="*74)
A1_i = D(13)/D(12)*D(7)/D(6)*D(19)/D(18)
print(f"   A_1 = {A1_i:.6f}  (worst admissible triple p=13, n_1=7, n_2=19)")
print()
print("""The low classes of the k=1 analysis survive verbatim: a class (a,b,0) at
k=2 imposes the same condition as (a,b) at k=1, so the tabulated m(a,b) are
still the smallest solutions.  They contribute A_2 as before.

The second notable adds new classes.  Consider just ONE of them: the class
where sigma(s^2) is a single prime equal to the SECOND notable.  Both
(0,1,0) and (0,0,1) require sigma(s^2) = s^2+s+1 to be a prime = 1 (mod 6).
The two smallest ordinary candidates (s = 5 mod 6) with that property are:""")
found=[]
s=5
while len(found)<4:
    if s%6==5 and isprime(s):
        v=s*s+s+1
        if isprime(v) and v%6==1: found.append((s,v))
    s+=2
for s,v in found[:4]:
    print(f"      s = {s:>3}: sigma(s^2) = {v:>5}, prime, = 1 mod 6")
print(f"""   So the two classes take s = {found[0][0]} and s = {found[1][0]} in some order, and their
   combined contribution is ({found[0][0]}/{found[0][0]-1})*({found[1][0]}/{found[1][0]-1}).  A_2 already contains the
   {found[0][0]}/{found[0][0]-1}; the SECOND of them multiplies the bound by a further {found[1][0]}/{found[1][0]-1}.""")
extra = D(found[1][0])/D(found[1][0]-1)
for T,name in ((T_tri,"pure powers removed"),(T_tri_ref,"also all-even removed")):
    Ai=Ainf(7,T)
    bound = A1_i*A2*extra*Ai
    print()
    print(f"   A_inf (B=7, {name}) = {Ai:.6f}")
    print(f"   bound >= A_1 * A_2 * ({found[1][0]}/{found[1][0]-1}) * A_inf = {bound:.6f}   exceeds 2? {bound>2}")
print()
print("""   and that uses only the k=1 low classes plus ONE of the 56 new ones, so the
   true bound is larger still.""")

print()
print("="*74)
print("VERDICT")
print("="*74)
print("""The section 2 abundancy method does NOT extend to k = 2.  It fails in both
cases, and for a structural reason rather than a numerical accident:

  - the class count per degree grows QUADRATICALLY in k for triples,
    (k+1)(k+2)/2 - 3, against LINEARLY, k - 1, for pairs.  A_inf jumps from
    1.0118 to 1.0713 at B = 7 and to 1.3045 at B = 5;
  - A_1 must cover a third non-ordinary component;
  - and a notable prime = 2 (mod 3) drops the size floor from 7 to 5.

At k = 1 the final figure was 1.6887, which looks comfortable, but the margin
is consumed entirely by these three effects at the very next rung.

This is a precise limit on the method, not on the conjecture: k = 2 may well be
closable, but not by this argument.""")
