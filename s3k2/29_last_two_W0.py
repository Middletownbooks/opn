#!/usr/bin/env python3
"""
The two |W| = 0 profiles other than the one closed in sections 8-10.

  (i)  alpha = 1, special and both notables in T, so tau = 4.  |U| >= 5.
  (ii) alpha = 0, special and both notables in T, so tau = 3.  |U| >= 6.

Same finishing move as section 11: omega(N) = 4 + alpha + |U| >= 10 gives
|U| >= 6 - alpha, U is inside Sm(T), so T dies when |Sm(T)| < 6 - alpha.

For (i) the single ordinary prime a forces F(a) inside T, so enumerate FORWARD
from a: T contains {13, a} u F(a), and the remaining slots are filled from a
small pool.  For (ii) there is no ordinary prime in T at all, so closure has
nothing to act on and T must be drawn from a pool -- that row keeps a pool
restriction and would need the max(T) cutoff of section 8 to be exhaustive.
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
_F={}
def Fset(t):
    if t not in _F: _F[t]=frozenset(p for p in fac(t*t+t+1) if p%3==1)
    return _F[t]
def smooth(T,Y):
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

FILL=[p for p in range(7,600) if p%3==1 and isprime(p)]

print("="*74)
print("(i)  alpha = 1, tau = 4, |W| = 0 :  one ordinary a, special, two notables")
print("     need |U| >= 5")
print("="*74)
ORDC=[p for p in range(7,20000) if p%3==1 and isprime(p)]
cands=set()
for a in ORDC:
    base={13,a}|Fset(a)
    if len(base)>4: continue
    if len(base)==4: cands.add((tuple(sorted(base)),a))
    else:
        free=4-len(base)
        for extra in combinations([f for f in FILL if f not in base], free):
            cands.add((tuple(sorted(base|set(extra))),a))
print(f"   ordinary candidates a below 20000 whose closure fits : "
      f"{len({a for _,a in cands})}")
print(f"   candidate (T, a) combinations : {len(cands)}")
seen={}; alive=[]; best=[]
for T,a in cands:
    rest=[t for t in T if t!=a]
    if not any(t%12==1 for t in rest): continue
    if T not in seen: seen[T]=smooth(T,10**30)
    S=seen[T]
    best.append((len(S),T,a,S))
    if len(S)>=5: alive.append((T,a,S))
best.sort(reverse=True)
print(f"   tested                          : {len(best)}")
print(f"   surviving (|Sm(T)| >= 5)        : {len(alive)}")
print(f"   largest |Sm(T)| seen            : {best[0][0] if best else 0}")
for n,T,a,S in best[:6]:
    print(f"      T = {str(list(T)):24s} ordinary {a:>6}  |Sm| = {n}  Sm = {S}")
print()
print("="*74)
print("(ii) alpha = 0, tau = 3, |W| = 0 :  special and two notables, no ordinary")
print("     prime = 1 (mod 3) at all; need |U| >= 6")
print("="*74)
POOL=[p for p in range(7,1500) if p%3==1 and isprime(p)]
alive2=[]; best2=[]
for rest in combinations([p for p in POOL if p!=13],2):
    T=tuple(sorted((13,)+rest))
    if not any(t%12==1 for t in T): continue      # a special is needed
    S=smooth(T,10**48)
    best2.append((len(S),T,S))
    if len(S)>=6: alive2.append((T,S))
best2.sort(reverse=True)
print(f"   T drawn from primes = 1 (mod 3) below 1500 : {len(best2)} sets tested")
print(f"   surviving (|Sm(T)| >= 6)                   : {len(alive2)}")
print(f"   largest |Sm(T)| seen                       : {best2[0][0] if best2 else 0}")
for n,T,S in best2[:6]:
    print(f"      T = {str(list(T)):20s} |Sm| = {n}  Sm = {S}")
