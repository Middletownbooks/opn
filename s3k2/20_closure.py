#!/usr/bin/env python3
"""
The ordinary-closure filter: the forcing tree as a condition on the finite set T.

Branch alpha = 2, |W| = 0, so |T| = 5 with role multiset (o,o,s,n,n).

An ORDINARY component has exponent exactly 2, so sigma(t^2) = t^2+t+1 is fully
determined.  Every prime factor of it divides 2N, is odd, and is 3 or = 1 (mod 3);
the ones = 1 (mod 3) therefore lie in T.  Writing

        F(t) = { prime factors of t^2+t+1 that are = 1 (mod 3) },

we get a CLOSURE CONDITION:  if t in T is ordinary then F(t) is a subset of T.

In the recursion of script 19, S is always the set of the L SMALLEST elements of
T (each level appends a new maximum), so every element of T \\ S exceeds max(S).
That makes the closure condition bite hard at every level:

    * f in F(t) with f < max(S) and f not in S   ->   assignment impossible
    * |F(t) \\ S| must not exceed 5 - |S|         ->   assignment impossible

Filtering role assignments this way sharpens LO and HI simultaneously, because
the surviving assignments are far fewer.  Examples:
    F(7) = {19}        F(13) = {61}       F(19) = {127}
    F(31) = {331}      F(61) = {13, 97}   F(67) = {13, 347}
so, e.g., 13 and 19 cannot both be ordinary in a 5-set that also needs room for
61 and 127.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math

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

def factor(n):
    f={}
    d=2
    while d*d<=n and d<10**7:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d += 1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f

_Fc={}
def Fset(t):
    if t in _Fc: return _Fc[t]
    r=frozenset(p for p in factor(t*t+t+1) if p%3==1)
    _Fc[t]=r; return r

print("F(t) = prime factors of t^2+t+1 that are = 1 (mod 3), for the small T-primes:")
for t in (7,13,19,31,37,43,61,67,73,79,97,103,109,127,139,151,157,163,181,193,199,307):
    print(f"   F({t:>3}) = {sorted(Fset(t))}")
print()

def geom(t,k): return F(sum(t**i for i in range(k+1)), t**k)
def sig(t,k): return sum(t**i for i in range(k+1))
SMALL1=[p for p in range(7,2000) if p%3==1 and isprime(p)]
def exp_ok(t,k,MIN):
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
    if role=='o': r=geom(t,2) if exp_ok(t,2,MIN) else None
    elif role=='s':
        if t%12==1:
            for k in range(1,120,4):
                if k%3==2: continue
                if exp_ok(t,k,MIN): r=geom(t,k); break
    else:
        for k in range(4,120,2):
            if k%3==2: continue
            if exp_ok(t,k,MIN): r=geom(t,k); break
    _mf[key]=r; return r

def closure_ok(S, ordinaries, size=5):
    """S is the set of the |S| smallest elements of T; T has `size` elements."""
    Sset=set(S); mx=max(S); extra=set()
    for t in ordinaries:
        for f in Fset(t):
            if f in Sset: continue
            if f < mx: return False          # would be a T-prime below max(S)
            extra.add(f)
    return len(extra) <= size - len(S)

FULL=('o','o','s','n','n')
def subprofiles(L): return sorted({tuple(sorted(c)) for c in combinations(FULL,L)})

def bounds(S, roles, MIN, use_closure=True):
    lo=hi=None
    for perm in set(permutations(range(len(S)))):
        l=F(1); h=F(1); ok=True; ords=[]
        for r,i in zip(roles,perm):
            t=S[i]; f=min_factor(t,r,MIN)
            if f is None: ok=False; break
            if r=='o': ords.append(t)
            l*=f; h*=(geom(t,2) if r=='o' else F(t,t-1))
        if not ok: continue
        if use_closure and not closure_ok(S, ords): continue
        if lo is None or l<lo: lo=l
        if hi is None or h>hi: hi=h
    return lo,hi

Y=10**24; TARGET=F(18,13)
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
def margin(S, use_closure=True):
    MIN=S[0]; los=[];his=[]
    for pr in subprofiles(len(S)):
        lo,hi=bounds(S,pr,MIN,use_closure)
        if lo is None: continue
        los.append(lo); his.append(hi)
    if not los: return None,None
    LO=min(los); HI=max(his); Sm=smooth_x(S); etb=math.exp(1.000001*tailY(S))
    for _ in range(60):
        R=TARGET/LO; H=F(1)
        for x in Sm:
            if geom(x,2)<=R: H*=geom(x,2)
        Hf=float(H)*etb; Hup=F(math.ceil(Hf*10**12)+1,10**12)
        nl=TARGET/Hup
        if nl<=LO: break
        LO=nl
    return float(LO)/float(HI), Sm

EXC=[(7,13,19,31),(7,13,31,79),(7,13,31,307),(7,13,67,79),(7,13,67,307),(7,13,79,307)]
print("The six exceptional 4-sets of script 19, re-tested with the closure filter:")
print(f"   {'S':22s} {'margin (no closure)':>20} {'margin (closure)':>18} {'verdict':>22}")
for S in EXC:
    m0,_ = margin(S, False)
    m1,Sm = margin(S, True)
    if m1 is None:
        verdict = "NO role assignment"
        ms = "     --"
    else:
        ms = f"{m1:.6f}"
        verdict = "cutoff exists" if m1 > 1 else "still no cutoff"
    print(f"   {str(list(S)):22s} {m0:>20.6f} {ms:>18} {verdict:>22}")
