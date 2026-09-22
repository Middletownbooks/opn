#!/usr/bin/env python3
"""
The max(T) cutoff recursion, with the forced-prime filter of script 18.

Branch alpha = 2, |W| = 0, |T| = 5, role multiset (o,o,s,n,n).  min(T) is 7 or
13 (the two smallest primes = 1 mod 3, and 13 is always in T).  The recursion
builds T upward by its largest element; at each stage

    margin(S) = LO(S)/HI(S)  after interval narrowing,
    B(S)      = min { B : corr(B,S) <= margin(S) },

and every T with T \\ {max T} = S and max(T) >= B(S) is killed.  So the sets
still to consider at the next level are S u {t} with max(S) < t < B(S).

Role minima now use the smallest exponent k for which sigma(t^k) has no prime
factor = 1 (mod 3) below min(S): such a factor would be a T-prime smaller than
min(T).  Detecting it is trial division by a handful of small primes.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math

Y=10**24; TARGET=F(18,13)
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; r=0
    while d%2==0: d//=2; r+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def geom(t,k): return F(sum(t**i for i in range(k+1)), t**k)
def _fac(n):
    f=set(); d=2
    while d*d<=n and d<10**8:
        while n%d==0: f.add(d); n//=d
        d += 1 if d==2 else 2
    if n>1: f.add(n)
    return f
_Fc={}
def Fset(t):
    if t not in _Fc: _Fc[t]=frozenset(p for p in _fac(t*t+t+1) if p%3==1)
    return _Fc[t]
def closure_ok(S, ords, size=5):
    """S = the |S| smallest elements of T, so every other T-prime exceeds max(S)."""
    Ss=set(S); mx=max(S); extra=set()
    for t in ords:
        for f in Fset(t):
            if f in Ss: continue
            if f < mx: return False
            extra.add(f)
    return len(extra) <= size-len(S)
def sig(t,k): return sum(t**i for i in range(k+1))
SMALL1=[p for p in range(7,2000) if p%3==1 and isprime(p)]

def admissible(t,k,MIN):
    v=sig(t,k)
    for q in SMALL1:
        if q>=MIN: break
        if q!=t and v%q==0: return False
    return True
_mf={}
def min_factor(t,role,MIN):
    key=(t,role,MIN)
    if key in _mf: return _mf[key]
    r=None
    if role=='o':
        r = geom(t,2) if admissible(t,2,MIN) else None
    elif role=='s':
        if t%12==1:
            for k in range(1,120,4):
                if k%3==2: continue
                if admissible(t,k,MIN): r=geom(t,k); break
    else:
        for k in range(4,120,2):
            if k%3==2: continue
            if admissible(t,k,MIN): r=geom(t,k); break
    _mf[key]=r; return r

FULL=('o','o','s','n','n')
def subprofiles(L): return sorted({tuple(sorted(c)) for c in combinations(FULL,L)})
def bounds(T,roles,MIN):
    lo=hi=None
    for perm in set(permutations(range(len(T)))):
        l=F(1); h=F(1); ok=True
        ords=[]
        for r,i in zip(roles,perm):
            t=T[i]; f=min_factor(t,r,MIN)
            if f is None: ok=False; break
            if r=='o': ords.append(t)
            l*=f; h*=(geom(t,2) if r=='o' else F(t,t-1))
        if not ok: continue
        if not closure_ok(T, ords): continue
        if lo is None or l<lo: lo=l
        if hi is None or h>hi: hi=h
    return lo,hi
def smooth_x(T):
    out=[]; L=list(T)
    def rec(i,m):
        if i==len(L):
            d=4*m-3; r=math.isqrt(d)
            if r*r==d and r%2==1:
                x=(r-1)//2
                if x>=5 and x%3==2 and isprime(x): out.append(x)
            return
        v=m
        while v<=Y: rec(i+1,v); v*=L[i]
    rec(0,1); return sorted(set(out))
def tailY(T):
    best=None; lnY=math.log(Y)
    for k in range(1,100):
        eps=0.5*k/100.0
        if eps>=0.5: break
        v=-eps*lnY
        for t in T: v-=math.log(1.0-t**(eps-0.5))
        if best is None or v<best: best=v
    return math.exp(best)/(1-Y**-0.5)
def euler(T):
    e=1.0
    for t in T: e/=(1.0-t**-0.5)
    return e
def corr(B,S):
    u=B**-0.5
    return (B/(B-1.0))*math.exp(1.01*(1+1/(math.sqrt(B)-1))*(u/(1-u))*euler(S))
def margin(S):
    MIN=S[0]; los=[];his=[]
    for pr in subprofiles(len(S)):
        lo,hi=bounds(S,pr,MIN)
        if lo is None: continue
        los.append(lo); his.append(hi)
    if not los: return None,[],None
    LO=min(los); HI=max(his); Sm=smooth_x(S); etb=math.exp(1.000001*tailY(S))
    for _ in range(60):
        R=TARGET/LO; H=F(1)
        for x in Sm:
            if geom(x,2)<=R: H*=geom(x,2)
        Hf=float(H)*etb; Hup=F(math.ceil(Hf*10**12)+1,10**12)
        nl=TARGET/Hup
        if nl<=LO: break
        LO=nl
    return float(LO)/float(HI), Sm, float(LO)
def threshold(S,m):
    if m is None or m<=1.0: return float('inf')
    lo,hi=2.0,1e18
    if corr(hi,S)>m: return float('inf')
    while hi/lo>1.0001:
        mid=math.sqrt(lo*hi)
        if corr(mid,S)<=m: hi=mid
        else: lo=mid
    return hi

PRIMES1=[p for p in range(7,10**7) if p%3==1 and isprime(p)]
live={1:[(7,),(13,)]}
excep=[]; final=[]
for L in (1,2,3,4):
    nxt=[]
    print(f"=== level {L} -> {L+1} " + "="*48)
    for S in live[L]:
        m,Sm,LO = margin(S)
        if m is None:
            print(f"  S = {str(list(S)):26s} no admissible role assignment -> DEAD")
            continue
        B=threshold(S,m)
        if B==float('inf'):
            excep.append((S,m)); print(f"  S = {str(list(S)):26s} margin = {m:.6f}"
                                       f"  -> NO cutoff    Sm = {Sm}")
            continue
        ext=[t for t in PRIMES1 if t>S[-1] and t<B and (13 in S or t==13 or S[-1]<13)]
        ext=[t for t in ext if (13 in S) or (t==13)]
        print(f"  S = {str(list(S)):26s} margin = {m:.6f}  B(S) = {B:12.1f}"
              f"  -> {len(ext)} extensions")
        for t in ext: nxt.append(tuple(sorted(S+(t,))))
    live[L+1]=sorted(set(nxt))
    print(f"  sets to consider at level {L+1}: {len(live[L+1])}")
    print()
    if not live[L+1]: break
print("="*66)
print(f"exceptional sets with no cutoff : {len(excep)}")
for S,m in excep: print(f"   {list(S)}  margin = {m:.6f}")
five=live.get(5,[])
print(f"5-sets the recursion cannot discard : {len(five)}")
print(f"   max prime appearing : {max((max(t) for t in five), default=0)}")
