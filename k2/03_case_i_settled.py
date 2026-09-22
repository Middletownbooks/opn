#!/usr/bin/env python3
"""Case (i) of k = 2, settled by identifying further new classes exactly."""
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
def factor(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def C2(n): return n*(n+1)//2
def Ainf(B,T,kmin=7,kmax=400):
    v=D(1)
    for k in range(kmin,kmax):
        c=T(k)
        if c>0: v*=(D(1)+D(1)/(D(B)**(D(k)/D(2))-D(2)))**c
    return v
def T_ref(k):
    tot=(k+1)*(k+2)//2
    return tot - (C2(k//2+1) if k%2==0 else 3)

A2=D(1)
for s in [5,29,59,863,1667,1733,2819,306419,1345913,3619619,68839637]:
    A2*=D(s)/D(s-1)
A1=D(13)/D(12)*D(7)/D(6)*D(19)/D(18)
Ai=Ainf(7,T_ref)

print("""Case (i): both notables = 1 (mod 3).  The 11 tabulated k=1 classes all have
c = 0, so they carry over unchanged and contribute A_2.  Now identify the
smallest ordinary prime in each of two NEW classes exactly.

An ordinary prime is s = 5 (mod 6).  p = 1 (mod 12); a notable = 1 (mod 6).
Note s = 5 (mod 12) gives sigma(s^2) = 7 (mod 12) and s = 11 (mod 12) gives
sigma(s^2) = 1 (mod 12) -- which is why m(1,0) = 59 in their table.
""")
# class (0,0,1): sigma(s^2) is a single prime = 1 mod 6, the SECOND notable
c001=[]
s=5
while len(c001)<3:
    if s%6==5 and isprime(s):
        v=s*s+s+1
        if isprime(v) and v%6==1: c001.append(s)
    s+=2
# class (0,1,1): sigma(s^2) = product of two DISTINCT primes, both = 1 mod 6
c011=[]
s=5
while len(c011)<3:
    if s%6==5 and isprime(s):
        f=factor(s*s+s+1)
        if len(f)==2 and all(e==1 for e in f.values()) and all(r%6==1 for r in f):
            c011.append((s,sorted(f)))
    s+=2
print(f"   class (0,1,0) and (0,0,1)  [sigma(s^2) a single notable prime]")
print(f"      smallest admissible s: {c001}")
print(f"      A_2 already contains s = {c001[0]}; the SECOND class forces a further "
      f"{c001[1]}/{c001[1]-1}")
print()
print(f"   class (0,1,1)  [sigma(s^2) = n_1 * n_2, two distinct primes = 1 mod 6]")
for s,f in c011:
    print(f"      s = {s:>3}: sigma(s^2) = {s*s+s+1:>5} = {f[0]} * {f[1]}, both = 1 mod 6")
print(f"      This is genuinely NEW: {c011[0][0]}^2+{c011[0][0]}+1 = {c011[0][1][0]}*{c011[0][1][1]}, and neither factor is")
print(f"      1 mod 12, so it cannot lie in the k=1 class (1,1).  It forces "
      f"{c011[0][0]}/{c011[0][0]-1}.")
e1=D(c001[1])/D(c001[1]-1); e2=D(c011[0][0])/D(c011[0][0]-1)
print()
print("="*70)
steps=[("A_1  (p=13, n_1=7, n_2=19)",A1),("A_2  (the 11 carried-over classes)",A2),
       (f"class (0,0,1), s={c001[1]}",e1),(f"class (0,1,1), s={c011[0][0]}",e2),
       ("A_inf (B=7, triples, all-even removed)",Ai)]
tot=D(1)
for name,v in steps:
    tot*=v
    print(f"   x {name:<42} {float(v):>10.6f}   running {float(tot):>10.6f}")
print("="*70)
print(f"   lower bound on the section 2 figure for k = 2, case (i): {tot:.6f}")
print(f"   exceeds 2?  {tot>2}")
print(f"""
   and this uses only 2 of the 56 new classes, so the true figure is larger.

VERDICT for k = 2.  The section 2 abundancy method fails in BOTH cases:
   case (ii): A_1 * A_inf alone = 2.0056 > 2, before any ordinary prime.
   case (i) : {float(tot):.4f} > 2 once two identifiable new classes are added.
The method does not reach k = 2.""")
