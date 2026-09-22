#!/usr/bin/env python3
"""
Can the max(T) cutoff be made RECURSIVE, so the pool restriction disappears?

Setting: the branch alpha = 2, special in T, both notables in T, so |W| = 0 and
|T| = 5 with profile (o,o,s,n,n).  Write T = T' u {t*} with t* >= B and T'
inside the pool below B (13 is in T and 13 < B, so 13 is in T').

t* takes one of the five roles, so T' carries one of the three reduced profiles

        (o,s,n,n)   (o,o,n,n)   (o,o,s,n)

and, by the cutoff lemma of script 13,

        HI(T)  <=  HI(T') * B/(B-1),
        H(T)   <=  H(T')  * exp(1.01 * tail(B, T')).

The narrowing is still legitimate at level 4: LO(T) >= min over the three
reduced profiles of minPROD(T'), so the same R may be used to throw small
members out of Sm(T').  Hence T is killed whenever

        LO_final(T')  >=  HI(T') * corr(B),   corr(B) = B/(B-1) * exp(1.01*tail).

If that holds for EVERY 4-subset of the pool below B, then every |T| = 5 set
with max(T) >= B dies, and the sweep below B is exhaustive.  This script
measures the pass rate.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math, sys

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

B    = int(sys.argv[1]) if len(sys.argv) > 1 else 400
Y    = 10**24
TARGET = F(18,13)
def geom(t,k): return F(sum(t**i for i in range(k+1)), t**k)
f_ord = lambda t: geom(t,2)
sup   = lambda t: F(t,t-1)

PROFILES = [('o','s','n','n'), ('o','o','n','n'), ('o','o','s','n')]

def bounds(T, roles):
    lo = hi = None
    for perm in set(permutations(range(len(T)))):
        l=F(1); h=F(1); ok=True
        for r,i in zip(roles, perm):
            t=T[i]
            if r=='o': l*=f_ord(t); h*=f_ord(t)
            elif r=='n': l*=geom(t,4); h*=sup(t)
            else:
                if t%12!=1: ok=False; break
                l*=geom(t,1); h*=sup(t)
        if not ok: continue
        if lo is None or l<lo: lo=l
        if hi is None or h>hi: hi=h
    return lo, hi

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

def tail_Y(T):
    best=None; lnY=math.log(Y)
    for k in range(1,100):
        eps=0.5*k/100.0
        if eps>=0.5: break
        v=-eps*lnY
        for t in T: v-=math.log(1.0-t**(eps-0.5))
        if best is None or v<best: best=v
    return math.exp(best)/(1-Y**-0.5)

def tail_star(T, B):
    """bound for sum 1/x over the x that the extra prime t* >= B contributes."""
    e = 1.0
    for t in T: e /= (1.0 - t**-0.5)
    u = B**-0.5
    return (1 + 1/(math.sqrt(B)-1)) * (u/(1-u)) * e

POOL=[p for p in range(7,B) if isprime(p) and p%3==1]
passed=failed=0; fails=[]
for rest in combinations([p for p in POOL if p!=13], 3):
    Tp=tuple(sorted((13,)+rest))
    los=[]; his=[]
    for pr in PROFILES:
        l,h = bounds(Tp, pr)
        if l is None: continue
        los.append(l); his.append(h)
    if not los: passed+=1; continue
    LO=min(los); HI=max(his)
    S=smooth_x(Tp); etb=math.exp(1.000001*tail_Y(Tp))
    for _ in range(40):
        R=TARGET/LO; H=F(1)
        for x in S:
            if f_ord(x)<=R: H*=f_ord(x)
        Hf=float(H)*etb
        Hup=F(math.ceil(Hf*10**12)+1,10**12)
        nl=TARGET/Hup
        if nl<=LO: break
        LO=nl
    corr = float(sys.argv[2]) if len(sys.argv)>2 else (B/(B-1.0))*math.exp(1.01*tail_star(Tp,B))
    if float(LO) >= float(HI)*corr: passed+=1
    else:
        failed+=1
        if len(fails)<15: fails.append((Tp, float(LO), float(HI)*corr, S))
tot=passed+failed
print(f"cutoff level 4, B = {B}   (pool: {len(POOL)} primes = 1 mod 3 below B)")
print(f"correction factor corr(B) for T' = [7,13,19,31] : "
      f"{(B/(B-1.0))*math.exp(1.01*tail_star((7,13,19,31),B)):.6f}")
print()
print(f"   4-subsets T' containing 13 : {tot}")
print(f"   clear the margin (so every |T|=5 with max(T) >= B dies) : {passed}"
      f"   ({100.0*passed/tot:.2f}%)")
print(f"   fail                                                    : {failed}")
print()
for Tp,lo,hi,S in fails:
    print(f"   T' = {str(list(Tp)):22s} LO = {lo:.7f}  HI*corr = {hi:.7f}   Sm = {S}")
