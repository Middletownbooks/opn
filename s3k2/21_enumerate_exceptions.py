#!/usr/bin/env python3
"""
Turning the remaining exceptional families into explicit finite lists.

For an exceptional 4-set S (the four SMALLEST elements of T), the closure
condition of script 20 pins down the fifth prime t* > max(S).  Enumerate by
which two elements of T are ordinary:

  CASE A   both ordinary primes lie in S.  Then union F(x) over them is inside
           T, so E = union F(x) minus S has at most one element; if |E| = 1 then
           t* = that element, and if |E| = 0 then t* is unconstrained here (but
           must then carry a special or notable role).
  CASE B   t* is one of the two ordinary primes, the other is x in S.  Then
           F(x) minus S is inside {t*}, AND F(t*) is inside T.  Since t* does
           not divide t*^2+t*+1, that says

               (t*^2 + t* + 1)/3   is  S-smooth,

           which is enumerated exactly by the "4M - 3 is a square" test over the
           S-smooth numbers M (times 3), the same device as Sm(T).

In both cases T must still contain a prime = 1 (mod 12) for the special role,
outside the two ordinary ones.
"""
from itertools import combinations
import math, sys

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
    f=set(); d=2
    while d*d<=n and d<10**8:
        while n%d==0: f.add(d); n//=d
        d += 1 if d==2 else 2
    if n>1: f.add(n)
    return f
def Fset(t): return frozenset(p for p in factor(t*t+t+1) if p%3==1)

YB=10**28
def caseB_candidates(S):
    """all primes t* > max(S), t* = 1 (mod 3), with (t*^2+t*+1)/3 S-smooth."""
    out=[]; L=list(S)
    def rec(i,m):
        if i==len(L):
            M=3*m; d=4*M-3; r=math.isqrt(d)
            if r*r==d and r%2==1:
                t=(r-1)//2
                if t>max(S) and t%3==1 and isprime(t): out.append(t)
            return
        v=m
        while v<=YB: rec(i+1,v); v*=L[i]
    rec(0,1); return sorted(set(out))

def analyse(S):
    S=tuple(sorted(S)); Sset=set(S); mx=max(S)
    print(f"S = {list(S)}   (the four smallest elements of T; t* > {mx})")
    for t in S: print(f"      F({t}) = {sorted(Fset(t))}")
    cands=set(); notes=[]
    # CASE A
    for O in combinations(S,2):
        E=set()
        bad=False
        for x in O:
            for f in Fset(x):
                if f in Sset: continue
                if f < mx: bad=True; break
                E.add(f)
            if bad: break
        if bad:
            notes.append(f"   A: ordinary {list(O)} -> forces a T-prime below max(S): impossible")
            continue
        if len(E)>1:
            notes.append(f"   A: ordinary {list(O)} -> needs {sorted(E)} as well: too many, impossible")
        elif len(E)==1:
            t=E.pop()
            notes.append(f"   A: ordinary {list(O)} -> t* = {t}")
            cands.add(t)
        else:
            notes.append(f"   A: ordinary {list(O)} -> t* unconstrained by closure (t* is s or n)")
            cands.add(None)
    # CASE B
    B=caseB_candidates(S)
    notes.append(f"   B: t* ordinary requires (t*^2+t*+1)/3 S-smooth; solutions t* > {mx}"
                 f" up to (t*^2) ~ 3*10^28 : {B}")
    for t in B:
        ok=False
        for x in S:
            E={f for f in Fset(x) if f not in Sset}
            if E and (min(E)<mx or E!={t}): continue
            # F(t*) must lie in T = S u {t*}
            if not (Fset(t) <= (Sset | {t})): continue
            ok=True; break
        if ok: cands.add(t)
        else: notes.append(f"        t* = {t}: F(t*) = {sorted(Fset(t))} not inside T -> out")
    for n in notes: print(n)
    concrete=sorted(c for c in cands if c is not None)
    free = None in cands
    print(f"   => explicit fifth primes: {concrete}")
    print(f"   => a family with t* unconstrained by closure: {free}")
    print()
    return concrete, free

for S in [(7,13,19,31),(7,13,31,79),(7,13,31,307)]:
    analyse(S)
