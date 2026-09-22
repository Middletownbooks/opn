#!/usr/bin/env python3
"""
The last |W| >= 1 profile:  alpha = 2, special in T, one notable in T, so
tau = 4 and |W| = 1.

Script 27 enumerated T by running over all (tau-1)-subsets of the prime pool,
which at tau = 4 over a pool of ~2200 primes is ~10^9 subsets -- it does not
finish.  Enumerate FORWARD from the closure condition instead: the two ordinary
primes a_1, a_2 of T force

        T  contains  {13, a_1, a_2} u F(a_1) u F(a_2)

and |T| = 4, so that union must already have at most four elements.  Since
|F(a)| >= 1 always, this is very restrictive, and the free slots (if any) are
then filled from a small pool.  One element of T outside {a_1,a_2} must be
= 1 (mod 12) to carry the special role.

Test, as in script 27: omega(N) >= 10 gives |U| >= 6 - alpha = 4, and U is
inside Sm(T), so T dies when |Sm(T)| < 4.
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

def smooth(T, Y):
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

ORD_MAX  = 20000      # candidates for the two ordinary primes of T
FILL_MAX = 600        # pool for a free slot
Y        = 10**30     # exact Sm(T) search bound at |T| = 4
NEED     = 4          # |U| >= 6 - alpha = 4

ORDC=[p for p in range(7,ORD_MAX) if p%3==1 and isprime(p)]
FILL=[p for p in range(7,FILL_MAX) if p%3==1 and isprime(p)]
print(f"ordinary candidates below {ORD_MAX}: {len(ORDC)}   "
      f"fill pool below {FILL_MAX}: {len(FILL)}")

cands=set(); pairs=0
for i,a1 in enumerate(ORDC):
    F1=Fset(a1)
    if len(F1|{13,a1})>4: continue
    for a2 in ORDC[i+1:]:
        base={13,a1,a2}|F1|Fset(a2)
        if len(base)>4: continue
        pairs+=1
        if len(base)==4:
            cands.add((tuple(sorted(base)),(a1,a2)))
        else:
            for f in FILL:
                if f in base: continue
                T=tuple(sorted(base|{f}))
                if len(T)==4: cands.add((T,(a1,a2)))
print(f"ordinary pairs surviving closure : {pairs}")
print(f"candidate (T, ordinary pair) combinations : {len(cands)}")
print()

alive=[]
seen={}
for T,O in sorted(cands):
    rest=[t for t in T if t not in O]
    if not any(t%12==1 for t in rest):      # need a special = 1 (mod 12)
        continue
    if T not in seen: seen[T]=smooth(T,Y)
    S=seen[T]
    print(f"   T = {str(list(T)):26s} ordinary {list(O)}  special from "
          f"{[t for t in rest if t%12==1]}  |Sm| = {len(S)}  Sm = {S}")
    if len(S)>=NEED: alive.append((T,O,S))
print()
print(f"   surviving (T, ordinary pair) : {len(alive)}")
for a in alive: print("      ", a)
