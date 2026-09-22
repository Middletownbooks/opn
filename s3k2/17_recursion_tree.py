#!/usr/bin/env python3
"""
The max(T) cutoff, applied recursively from the bottom up.

Branch: alpha = 2, special and both notables in T, so |W| = 0 and |T| = 5 with
role multiset (o,o,s,n,n).  For a subset S of T carrying any sub-multiset of
those roles, write

    LO(S) = min over admissible role assignments (after narrowing), see 15
    HI(S) = max over admissible role assignments
    margin(S) = LO(S) / HI(S).

CUTOFF (script 13).  If S is a subset of T, t* = max(T) is not in S and
t* >= B, then HI(T) <= HI(S)*prod of the other sups and H(T) <= H(S)*exp(tail).
Taking S = T \\ {t*}:

    T is killed as soon as   margin(S) >= corr(B, S),
    corr(B, S) = B/(B-1) * exp(1.01 * (1 + 1/(sqrt(B)-1)) * (u/(1-u))
                               * prod_{t in S} (1 - t^{-1/2})^{-1}),  u = B^{-1/2}.

corr is decreasing in B and tends to 1, so a set S with margin(S) > 1 yields a
FINITE threshold  B(S) = min{ B : corr(B,S) <= margin(S) }, and every superset
T = S u {t*} with t* >= B(S) dies.  Building upward, the sets that survive at
each level are

    live_{L+1} = { S u {t} : S in live_L,  t > max(S),  t < B(S) }

together with the sets S that have margin(S) <= 1, for which B(S) = infinity and
which therefore spawn a one-parameter family that this test cannot kill.  Those
are the exceptions, and they are what the recursion is for: finding them.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math

Y = 10**24; TARGET = F(18,13)
def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
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
f_ord=lambda t: geom(t,2); sup=lambda t: F(t,t-1)

FULL = ('o','o','s','n','n')
def subprofiles(L):
    return sorted({tuple(sorted(c)) for c in combinations(FULL, L)})

def bounds(T, roles):
    lo=hi=None
    for perm in set(permutations(range(len(T)))):
        l=F(1); h=F(1); ok=True
        for r,i in zip(roles,perm):
            t=T[i]
            if r=='o': l*=f_ord(t); h*=f_ord(t)
            elif r=='n': l*=geom(t,4); h*=sup(t)
            else:
                if t%12!=1: ok=False; break
                l*=geom(t,1); h*=sup(t)
        if not ok: continue
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

def corr(B, S):
    u=B**-0.5
    tail=(1+1/(math.sqrt(B)-1))*(u/(1-u))*euler(S)
    return (B/(B-1.0))*math.exp(1.01*tail)

def margin(S):
    L=len(S); los=[];his=[]
    for pr in subprofiles(L):
        lo,hi=bounds(S,pr)
        if lo is None: continue
        los.append(lo); his.append(hi)
    if not los: return None, None, []
    LO=min(los); HI=max(his)
    Sm=smooth_x(S); etb=math.exp(1.000001*tailY(S))
    for _ in range(60):
        R=TARGET/LO; H=F(1)
        for x in Sm:
            if f_ord(x)<=R: H*=f_ord(x)
        Hf=float(H)*etb
        Hup=F(math.ceil(Hf*10**12)+1,10**12)
        nl=TARGET/Hup
        if nl<=LO: break
        LO=nl
    return float(LO)/float(HI), float(LO), Sm

def threshold(S, m):
    """smallest B with corr(B,S) <= m; None if m <= 1."""
    if m <= 1.0: return None
    lo, hi = 2.0, 1e18
    if corr(hi, S) > m: return float('inf')
    while hi/lo > 1.0001:
        mid=math.sqrt(lo*hi)
        if corr(mid,S) <= m: hi=mid
        else: lo=mid
    return hi

PRIMES1=[p for p in range(7,10**6) if p%3==1 and isprime(p)]
live={1:[(13,)]}
excep=[]
for L in (1,2,3,4):
    nxt=[]
    print(f"=== level {L} -> {L+1} " + "="*50)
    for S in live[L]:
        m,LO,Sm = margin(S)
        B = threshold(S, m)
        if B is None or B == float('inf'):
            excep.append((S, m))
            print(f"  S = {str(list(S)):24s} margin = {m:.6f}  -> NO cutoff "
                  f"(one-parameter family)   Sm = {Sm}")
            continue
        ext=[t for t in PRIMES1 if t > S[-1] and t < B]
        print(f"  S = {str(list(S)):24s} margin = {m:.6f}  B(S) = {B:11.1f}  "
              f"-> {len(ext)} extensions   Sm = {str(Sm)[:30]}")
        for t in ext: nxt.append(tuple(sorted(S+(t,))))
    live[L+1]=sorted(set(nxt))
    print(f"  live sets at level {L+1}: {len(live[L+1])}")
    print()
    if not live[L+1]: break

print("="*66)
print(f"EXCEPTIONAL SETS (margin <= 1, no cutoff available): {len(excep)}")
for S,m in excep: print(f"   {list(S)}   margin = {m:.6f}")
print()
print(f"live 5-sets reached by the recursion: {len(live.get(5,[]))}")
for T in live.get(5,[])[:40]: print("   ", list(T))
