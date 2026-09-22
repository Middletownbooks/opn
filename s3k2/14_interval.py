#!/usr/bin/env python3
"""
An interval-narrowing version of the |T| = 5 test -- still UNCONDITIONAL, and
much sharper, because it feeds the two bounds into each other.

Write  L <= PROD_T <= G  and  1 <= PROD_U <= H, with PROD_T * PROD_U = 18/13.

   G = g*(T) = max over role assignments of
          prod_{ordinary t} (1 + 1/t + 1/t^2) * prod_{special, notable} t/(t-1)
       (strict: an ordinary component has exponent EXACTLY 2, so it is capped
       well below t/(t-1); the other two roles only approach t/(t-1))
   L0 = min over role assignments, as before (special = 1 mod 12, notable q>=4)

Iteration.  Given a lower bound L on PROD_T, PROD_U <= R = (18/13)/L, so every
x in U must satisfy 1 + 1/x + 1/x^2 <= R on its own; that is, U is contained in

        Sm*(T) = { x in Sm(T) : 1 + 1/x + 1/x^2 <= R }.

Hence PROD_U <= H = prod_{Sm*(T)} (1+1/x+1/x^2) * exp(tail), which gives the
improved lower bound L' = max(L, (18/13)/H).  L is non-decreasing, so iterate to
a fixed point.

        >>> T is impossible as soon as L >= g*(T). <<<

Nothing here assumes Sm(T) is completely known: dropping members of Sm(T) only
makes H smaller and L larger, i.e. only makes the test claim MORE.  So the tail
must be handled in the safe direction -- it is, by the Euler-product bound of
script 09, which is an upper bound on the missing part of H.
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

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
Y = 10**24; TARGET = F(18,13)
def geom(t,k): return F(sum(t**i for i in range(k+1)), t**k)
f_ord = lambda t: geom(t,2)

def bounds_T(T):
    lo = hi = None
    for perm in set(permutations(range(5))):
        s = T[perm[0]]
        if s % 12 != 1: continue
        n1, n2 = T[perm[1]], T[perm[2]]
        o1, o2 = T[perm[3]], T[perm[4]]
        l = geom(s,1)*geom(n1,4)*geom(n2,4)*f_ord(o1)*f_ord(o2)
        h = F(s,s-1)*F(n1,n1-1)*F(n2,n2-1)*f_ord(o1)*f_ord(o2)
        if lo is None or l < lo: lo = l
        if hi is None or h > hi: hi = h
    return lo, hi

def smooth_x(T):
    out=[]; L=list(T)
    def rec(i,m):
        if i==5:
            d=4*m-3; r=math.isqrt(d)
            if r*r==d and r%2==1:
                x=(r-1)//2
                if x>=5 and x%3==2 and isprime(x): out.append(x)
            return
        v=m
        while v<=Y: rec(i+1,v); v*=L[i]
    rec(0,1); return sorted(set(out))

def tail_bound(T):
    best=None; lnY=math.log(Y)
    for k in range(1,100):
        eps=0.5*k/100.0
        if eps>=0.5: break
        v=-eps*lnY
        for t in T: v-=math.log(1.0-t**(eps-0.5))
        if best is None or v<best: best=v
    return math.exp(best)/(1-Y**-0.5)

POOL=[p for p in range(7,TMAX) if isprime(p) and p%3==1]
dead_old=dead_new=0; alive=[]
for rest in combinations([p for p in POOL if p!=13],4):
    T=tuple(sorted((13,)+rest))
    L,G = bounds_T(T)
    if L is None: dead_old+=1; continue
    S=smooth_x(T); tb=tail_bound(T)
    g_crude=1.0
    for t in T: g_crude*=t/(t-1.0)
    h_crude=math.exp(1.000001*tb)
    for x in S: h_crude*=1.0+1.0/x+1.0/x**2
    old_dead = (L>TARGET) or (g_crude*h_crude <= 18/13)
    # interval narrowing
    for _ in range(40):
        R = TARGET/L
        H = F(1)
        for x in S:
            if f_ord(x) <= R: H *= f_ord(x)
        Hf = float(H)*math.exp(1.000001*tb)
        Hup = F(math.ceil(Hf*10**12) + 1, 10**12)     # round H UP: keeps L a valid lower bound
        newL = max(L, TARGET/Hup)
        if newL == L: break
        L = newL
    new_dead = (L >= G) or (L > TARGET)
    if old_dead: dead_old += 1
    if new_dead or old_dead: dead_new += 1
    else: alive.append((T,S,float(L),float(G)))
tot=dead_new+len(alive)
print(f"|T| = 5, pool = primes = 1 mod 3 in [7,{TMAX}) ; {tot} sets with 13 in T")
print(f"   unconditionally dead, crude two-sided test (scripts 09/10) : {dead_old:6d}"
      f"  ({100.0*dead_old/tot:.1f}%)")
print(f"   unconditionally dead, interval narrowing                   : {dead_new:6d}"
      f"  ({100.0*dead_new/tot:.1f}%)")
print(f"   still alive                                                : {len(alive):6d}")
print()
for T,S,L,G in alive[:20]:
    print(f"   T = {str(list(T)):26s} L = {L:.7f}  g* = {G:.7f}  Sm = {str(S)[:34]}")
