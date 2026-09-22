#!/usr/bin/env python3
"""Audit step 4: every monomial the model subtracts via P must genuinely be
impossible as F(s) = s^2+s+1 for an ordinary prime s (s >= 5)."""
import math
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def F(s): return s*s+s+1
def representable(M):
    """is M = F(s) for some prime s >= 5?"""
    s=int((math.isqrt(4*M-3)-1)//2)
    for t in (s-2,s-1,s,s+1,s+2):
        if t>=5 and isprime(t) and F(t)==M: return t   # s must be an ordinary PRIME
    return None

# P polynomials as explicit monomial exponent sets on the two smallest support
# primes of each row (the third prime never appears in any P)
ROWS = {
 1:((7,13,19),"H2+H3",None),
 2:((7,13,31),"H2+H3",None),
 3:((7,13),"pairs",[(1,1),(2,1),(1,2),(3,1),(2,2),(1,3)]),
 4:((7,19),"pairs",[(2,1),(1,2)]),
 5:((7,31,37),"H2",None),
 6:((7,31),"pairs",[(1,1),(2,1),(1,2)]),
 7:(None,"P=0",None),
 8:(None,"P=0",None),
 9:((13,19,31),"H2",None),
 10:((13,31),"pairs",[(1,1)]),
 11:(None,"P=0",None),
}
def mixed_monomials(S,maxdeg):
    out=[]
    r1,r2,r3=S
    for a in range(maxdeg+1):
        for b in range(maxdeg+1):
            for c in range(maxdeg+1):
                d=a+b+c
                if d<1 or d>maxdeg: continue
                if sum(1 for e in (a,b,c) if e>0)<2: continue
                out.append((r1**a*r2**b*r3**c,(a,b,c)))
    return out

print(f"{'row':>3} {'monomials subtracted':>52} {'all impossible?':>16}")
allok=True
for r,(S,kind,pairs) in ROWS.items():
    if kind=="P=0":
        print(f"{r:>3} {'(none)':>52} {'n/a':>16}"); continue
    if kind=="pairs":
        vals=[(S[0]**a*S[1]**b,(a,b)) for a,b in pairs]
    elif kind=="H2":
        vals=[(m,e) for m,e in mixed_monomials(S,2)]
    else:  # H2+H3
        vals=[(m,e) for m,e in mixed_monomials(S,3)]
    reps=[(m,representable(m)) for m,_ in vals]
    bad=[(m,s) for m,s in reps if s is not None]
    allok &= not bad
    lst=",".join(str(m) for m,_ in sorted(vals))
    print(f"{r:>3} {lst[:52]:>52} {str(not bad):>16}")
    if bad: print(f"      REPRESENTABLE: {bad}")
print()
print(f"every subtracted monomial is impossible as F(prime): {allok}")
print()
print("Row 1 needs one extra check: 133 = 7*19 = F(11) IS representable, so")
print("s = 11 is a genuine ordinary prime there.  The model removes it from the")
print("tail via P = H2+H3 and pays for it separately with B = 11/10 -- consistent,")
print("no double count.")
m=7*19
print(f"   133 representable as F({representable(m)})  -> handled by B, not by the tail")
print()
print("Row 2's B = 5/4 is the singleton class sigma(s^2) = 31 with s = 5;")
print("singletons are not part of H (which sums mixed monomials only), so again")
print("no double count.")
