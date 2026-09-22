#!/usr/bin/env python3
"""
The profiles of section 3 at k = 2 with |W| >= 1, closed by COUNTING.

Setting as in script 12/15.  beta = number of big components (special p^e and
the two notables) that are = 1 (mod 3); tau = |T| = alpha + beta; |W| = 3 - beta;
the budget gives alpha + [special in W] <= 2, and 13 is always in T.

    omega(N) = 1 + tau + |W| + |U| = 4 + alpha + |U| >= 10   =>   |U| >= 6 - alpha.

U is inside Sm(T), so a profile dies at T whenever |Sm(T)| < 6 - alpha.  This
needs no abundancy input at all -- and since |W| >= 1 forces tau <= 4 (and
|W| >= 2 forces tau <= 3), Sm(T) is an equation in at most a handful of primes,
searchable to bounds far beyond the 10^24 used for |T| = 5.

T itself is pinned by the CLOSURE condition of script 20: an ordinary t in T
needs F(t) (the prime factors of t^2+t+1 that are = 1 mod 3) inside T.  With
tau <= 3 that usually determines T outright rather than leaving a pool.
"""
import math
from itertools import combinations

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
def fac(n):
    f=set(); d=2
    while d*d<=n and d<10**8:
        while n%d==0: f.add(d); n//=d
        d += 1 if d==2 else 2
    if n>1: f.add(n)
    return f
def Fset(t): return frozenset(p for p in fac(t*t+t+1) if p%3==1)

def smooth(T, Y):
    """exact Sm(T) for x^2+x+1 <= Y."""
    out=[]; L=sorted(T)
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

# search bounds chosen so each run stays cheap; they shrink as |T| grows
YB={1:10**400, 2:10**160, 3:10**48, 4:10**30}

def closure_T(tau, alpha, pool):
    """all T of size tau containing 13 that satisfy closure for SOME choice of
       alpha ordinary members (the rest taking special/notable roles)."""
    out=[]
    for rest in combinations([p for p in pool if p!=13], tau-1):
        T=tuple(sorted((13,)+rest)); Ts=set(T)
        for O in combinations(T, alpha):
            if all(Fset(t)<=Ts for t in O):
                out.append((T,O)); break
    return out

POOL=[p for p in range(7,20000) if p%3==1 and isprime(p)]
PROFILES=[]           # (alpha, sp_in_T, nt_in_T)
for alpha in (0,1,2):
    for sp in (0,1):
        if alpha + (1-sp) > 2: continue
        for nt in (0,1,2):
            tau=alpha+sp+nt; W=3-sp-nt
            if 1<=tau<=5 and W>=1: PROFILES.append((alpha,sp,nt,tau,W))

print(f"{'alpha':>6} {'sp in T':>8} {'nt in T':>8} {'tau':>4} {'|W|':>4} "
      f"{'|U| needed':>11} {'admissible T (closure)':>24} {'survive count':>14}")
print("-"*92)
survivors=[]
for alpha,sp,nt,tau,W in PROFILES:
    need=6-alpha
    if alpha==0:
        cand=[(tuple(sorted((13,)+r)),()) for r in
              combinations([p for p in POOL if p!=13 and p<600], tau-1)]
    else:
        cand=closure_T(tau, alpha, [p for p in POOL if p<20000])
    Y=YB.get(tau, 10**60)
    alive=[]
    for T,O in cand:
        S=smooth(T,Y)
        if len(S)>=need: alive.append((T,O,S))
    print(f"{alpha:>6} {sp:>8} {nt:>8} {tau:>4} {W:>4} {need:>11} "
          f"{len(cand):>24} {len(alive):>14}")
    for a in alive: survivors.append((alpha,sp,nt,a))
print("-"*92)
print(f"profiles with |W| >= 1 : {len(PROFILES)} ; surviving (profile, T) pairs : "
      f"{len(survivors)}")
for alpha,sp,nt,(T,O,S) in survivors[:30]:
    print(f"   alpha={alpha} sp_in_T={sp} nt_in_T={nt}  T={list(T)}  ordinary={list(O)}"
          f"  |Sm(T)|={len(S)}  Sm={S[:10]}")
