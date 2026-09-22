#!/usr/bin/env python3
"""
k = 2: does Ochem-Zelinsky's section 2 argument still close?

DEFINITIONS.  N odd perfect, N = p^e m^2, p = e = 1 (mod 4) the special prime.
McDaniel: at least one even exponent exceeds 2.  Call N k-RESTRAINED when
exactly k do; k = 1 is their 'restrained'.  For k = 2 write the two notable
components n_1^{q_1}, n_2^{q_2} with q_i >= 4 even.  'Ordinary' = exponent 2.

THEIR SECTION 2 (k = 1, assuming 3 does not divide N), rederived for k = 2:

  - every ordinary s is = 2 (mod 3), else 3 | sigma(s^2) = s^2+s+1 and 3 | N;
    with s odd that is s = 5 (mod 6);
  - every prime factor of s^2+s+1 other than 3 is = 1 (mod 3), hence is NOT
    ordinary, hence lies in {p, n_1, n_2}.  So every ordinary s is 'regular':
        sigma(s^2) = p^a * n_1^b * n_2^c.
  - each triple (a,b,c) determines at most one ordinary s, since s^2+s+1
    determines s.

So the k = 1 argument goes through verbatim with PAIRS replaced by TRIPLES.
The question is purely quantitative: does the resulting abundancy bound still
fall below 2?

THREE THINGS GET WORSE AT k = 2:
  (1) A_1 covers three non-ordinary components instead of two;
  (2) the number of classes with a+b+c = k grows QUADRATICALLY, (k+1)(k+2)/2 - 3,
      instead of linearly, k - 1;
  (3) in the case where a notable prime is = 2 (mod 3) the size floor drops
      from 7 to 5.
"""
from fractions import Fraction as F
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

print(__doc__)
print("="*74)
print("A_1 : supremum of the non-ordinary abundancy")
print("="*74)
print("p = 1 (mod 12) so p >= 13.  A notable prime = 1 (mod 3) is = 1 (mod 6),")
print("so >= 7; one = 2 (mod 3) is = 5 (mod 6), so >= 5.")
def cap(x): return F(x, x-1)
P=[x for x in range(13,200) if isprime(x) and x%12==1]
N1=[x for x in range(5,200) if isprime(x) and x%6==1]
N5=[x for x in range(5,200) if isprime(x) and x%6==5]
best_i=max((cap(p)*cap(a)*cap(b), (p,a,b))
           for p in P[:4] for a in N1[:4] for b in N1[:4]
           if len({p,a,b})==3 and a<b)
best_ii=max((cap(p)*cap(a)*cap(b), (p,a,b))
            for p in P[:4] for a in N1[:4] for b in N5[:4] if len({p,a,b})==3)
print(f"   k=1 (their value)                 A_1 = 91/72        = {float(F(91,72)):.6f}")
print(f"   k=2 case (i)  both notables 1 mod 3: {best_i[1]} -> {float(best_i[0]):.6f}")
print(f"   k=2 case (ii) one notable 2 mod 3 : {best_ii[1]} -> {float(best_ii[0]):.6f}")

print()
print("="*74)
print("A_inf : the tail over classes with a+b+c >= 7")
print("="*74)
print("""From sigma(s^2) = product of the notables/special to total degree k, each
factor at least B, we get (s+1)^2 > B^k so s >= B^{k/2} - 1, and the class
contributes at most 1 + 1/(B^{k/2} - 2).  Lemma 3 (Bennett-Levin) kills the
pure-power classes, leaving (k+1)(k+2)/2 - 3 triples of degree k (against
k - 1 pairs at k = 1).""")
def Ainf(B, classes, kmin=7, kmax=400):
    v=D(1)
    for k in range(kmin,kmax):
        cnt=classes(k)
        if cnt<=0: continue
        v *= (D(1)+D(1)/(D(B)**(D(k)/D(2))-D(2)))**cnt
    return v
a_k1 = Ainf(7, lambda k: k-1)
a_k2_7 = Ainf(7, lambda k: (k+1)*(k+2)//2-3)
a_k2_5 = Ainf(5, lambda k: (k+1)*(k+2)//2-3)
print(f"   k=1, pairs,   B=7 : A_inf = {a_k1:.12f}   (paper: 1.01178747704420359446)")
print(f"   k=2, triples, B=7 : A_inf = {a_k2_7:.12f}")
print(f"   k=2, triples, B=5 : A_inf = {a_k2_5:.12f}")

print()
print("="*74)
print("HOW MUCH ROOM IS LEFT for the low classes (a+b+c <= 6)?")
print("="*74)
A2_k1 = D(1)
for s in [5,29,59,863,1667,1733,2819,306419,1345913,3619619,68839637]:
    A2_k1 *= D(s)/D(s-1)
print(f"   At k=1 the 11 tabulated low classes contribute A_2 = {A2_k1:.12f}")
print(f"   and the total was {D(91)/D(72)*A2_k1*a_k1:.6f} < 2, with room to spare.")
print()
for label,A1,Ai in (("k=2 case (i)  B=7", D(best_i[0].numerator)/D(best_i[0].denominator), a_k2_7),
                    ("k=2 case (ii) B=5", D(best_ii[0].numerator)/D(best_ii[0].denominator), a_k2_5)):
    room = D(2)/(A1*Ai)
    print(f"   {label}:  A_1 = {A1:.6f}, A_inf = {Ai:.6f}")
    print(f"      room for ALL low classes = 2/(A_1*A_inf) = {room:.6f}")
    print(f"      but the k=1 low classes ALONE already consume {A2_k1:.6f}")
    if room > A2_k1:
        print(f"      -> {float(room/A2_k1):.6f} left over for the remaining low classes")
    else:
        print(f"      -> ALREADY EXCEEDED: the bound cannot reach below 2.")
    print()
lows=[(a,b,c) for a in range(7) for b in range(7) for c in range(7) if 1<=a+b+c<=6]
pure=[t for t in lows if sorted(t)[:2]==[0,0] and max(t)>1]
c0=[t for t in lows if t[2]==0]
print(f"   low classes with 1 <= a+b+c <= 6            : {len(lows)}")
print(f"   of which pure powers killed by Lemma 3      : {len(pure)}")
print(f"   of which have c = 0 (the k=1 classes)       : {len(c0)}")
print(f"   NEW classes introduced by the second notable: {len(lows)-len(c0)}")
