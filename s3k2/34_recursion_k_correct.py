#!/usr/bin/env python3
"""
The max(T) recursion of scripts 17/19/22, with the cutoff lemma CORRECTED for
several remaining primes.

THE ERROR.  Script 13's lemma is stated for T = S u {t*}: ONE prime above S.
Scripts 17, 19 and 22 applied it at every level L of the recursion, but at level
L the set S is the L smallest elements of a 5-set T, so when the (L+1)-th
smallest prime is >= B there are k = 5 - L primes >= B, not one.

THE LEMMA FOR k PRIMES.  Let T = S u R, |R| = k, every r in R >= B.  Then
  * every T-factor of an R-prime is < r/(r-1) <= B/(B-1), in any role, so
        HI(T) <= HI(S) * (B/(B-1))^k ;
  * x in Sm(T) \ Sm(S) has x^2+x+1 = M_S * M_R with M_S S-smooth, M_R > 1
    R-smooth, M >= B, and 1/x < (1 + 1/(sqrt(B)-1)) M^(-1/2); summing,
        sum 1/x <= (1 + 1/(sqrt(B)-1)) * E(S) * ( prod_{r in R} (1-r^(-1/2))^(-1) - 1 )
                <= (1 + 1/(sqrt(B)-1)) * E(S) * ( (1-u)^(-k) - 1 ),   u = B^(-1/2),
    E(S) = prod_{t in S} (1 - t^(-1/2))^(-1);
  * LO(T) >= LO(S) (R-factors are >= 1), and interval narrowing on S stays
    valid because R(T) <= R(S).
  [CORRECTED after the independent audit, audit_s3k2/AUDIT_S3K2_RESULT.md,
   findings G1-G3 and proof Pf.2.  The two sentences just above give the wrong
   reason.  The NARROWED LO(S) is NOT a lower bound for T strictly containing S:
   for S = {7,13,19,31}, 107 enters Sm(S u {127}).  Only the RAW role minimum
   LO_raw(S) is.  The kill is nevertheless valid, for this reason:
     - the narrowing loop is exactly one step (G3): the new cap equals Hup_0,
       which already bounds every admitted f(x);
     - its cap uses only LO_raw, which is valid for supersets;
     - LO_raw <= HI, so margin > 1 forces the narrowed LO to equal (18/13)/Hup_0.
   Hence margin(S) >= corr_k is exactly (18/13)/(H_0(S) * HI(S)) >= corr_k, and
   Pf.2 proves that this kills every T whose (|S|+1)-th element is >= B.
   Do NOT let the cap depend on narrowed information: that would break superset
   validity silently.
   The factor 1.01 below is not justified by "1/x plus 1/x^2" when B < ~10^4
   (G2).  What is needed, log f(x) * (sqrt(M) - 1) < 1 for all x >= 2, is true
   (audit_s3k2/a2_corr_factor_check.py), so 1.01 is slack.]
Hence T dies when margin(S) >= corr_k(B, S) with
        corr_k = (B/(B-1))^k * exp(1.01 * (1 + 1/(sqrt(B)-1)) * ((1-u)^(-k) - 1) * E(S)).
For k = 1 this is script 13's corr exactly.  The recursion below is script 22's,
character for character, except that B(S) is computed from corr_k with
k = 5 - |S|.  It checkpoints each level to s3k2/out34_level<L>.txt.
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


def corrk(B,S,k):
    u=B**-0.5
    return (B/(B-1.0))**k*math.exp(1.01*(1+1/(math.sqrt(B)-1))*((1-u)**-k-1)*euler(S))
def threshold_k(S,m,k):
    if m is None or m<=1.0: return float('inf')
    lo,hi=2.0,1e30
    if corrk(hi,S,k)>m: return float('inf')
    while hi/lo>1.0001:
        mid=math.sqrt(lo*hi)
        if corrk(mid,S,k)<=m: hi=mid
        else: lo=mid
    return hi
assert abs(corrk(10**6,(7,13,19,31),1)-corr(10**6,(7,13,19,31)))<1e-15

import sys, time, os, bisect
HERE=os.path.dirname(os.path.abspath(__file__))
_P=[]; _PMAX=[0]
def primes1_upto(B):
    """primes = 1 (mod 3) below B, sieved, grown on demand."""
    if B>_PMAX[0]:
        n=int(B)+1; s=bytearray([1])*(n+1); s[0]=s[1]=0
        for i in range(2,math.isqrt(n)+1):
            if s[i]: s[i*i::i]=bytearray(len(range(i*i,n+1,i)))
        _P[:]=[p for p in range(7,n+1) if s[p] and p%3==1]; _PMAX[0]=n
    return _P[:bisect.bisect_left(_P,B)]

STOP=int(sys.argv[1]) if len(sys.argv)>1 else 4
live={1:[(7,),(13,)]}; excep=[]
for L in range(1,STOP+1):
    nxt=[]; t0=time.time()
    print(f"=== level {L} -> {L+1}   ({len(live[L])} sets, k = {5-L}) " + "="*30, flush=True)
    for i,S in enumerate(live[L]):
        m,Sm,LO = margin(S)
        if m is None: continue
        B=threshold_k(S,m,5-L)
        if B==float('inf'):
            excep.append((S,m)); print(f"  EXCEPTION S = {list(S)} margin = {m:.6f}", flush=True)
            continue
        if B>5e8: print(f"  S = {list(S)}: B = {B:.3g} too large to sieve", flush=True); sys.exit(2)
        ext=[t for t in primes1_upto(B) if t>S[-1] and ((13 in S) or t==13)]
        if L<=2: print(f"  S = {str(list(S)):22s} margin = {m:.6f}  B_{5-L} = {B:12.1f} -> {len(ext)}", flush=True)
        for t in ext: nxt.append(tuple(sorted(S+(t,))))
        if (i+1)%2000==0: print(f"    ... {i+1}/{len(live[L])}  {time.time()-t0:.0f}s  next so far {len(nxt)}", flush=True)
    live[L+1]=sorted(set(nxt))
    with open(os.path.join(HERE,f"out34_level{L+1}.txt"),"w") as f:
        for S in live[L+1]: f.write(" ".join(map(str,S))+"\n")
    mx=max((s[-1] for s in live[L+1]),default=0)
    print(f"  level {L+1}: {len(live[L+1])} sets, max prime {mx}, {time.time()-t0:.0f}s", flush=True)
print("exceptions:", [(list(S),round(m,6)) for S,m in excep])
