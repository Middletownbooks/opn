#!/usr/bin/env python3
"""
Section 3 at k = 2, ALL sub-cases, with interval narrowing.

Same case structure as 12_section3_k2_full.py (read that file for the setting,
the 3-budget inequality alpha + [special in W] <= 2, and the handling of W).
The difference is the test.  Write

    PROD_T * PROD_W * PROD_U = 18/13,     P = PROD_T * PROD_W.

    LO  = minPROD_T(T, profile) * minPROD_W(W)        <= P
    HI  = g*(T) * maxPROD_W(W)                        >  P
          g*(T) = max over role assignments of
                  prod_{ordinary} (1+1/t+1/t^2) * prod_{special,notable} t/(t-1)

    given a lower bound LO on P, PROD_U <= 18/13 / LO =: R, so every x in U must
    satisfy 1 + 1/x + 1/x^2 <= R on its own, hence
        U  contained in  Sm*(T) = { x in Sm(T)\\W : 1+1/x+1/x^2 <= R },
        PROD_U <= H = prod_{Sm*(T)} (1+1/x+1/x^2) * exp(tail),
    and therefore  P >= 18/13 / H,  a new lower bound.  Iterate to a fixed point.

    UNCONDITIONAL VERDICT:  dead if LO >= HI, or LO > 18/13.

This subsumes the earlier "g*h <= 18/13" test.  It is safe with respect to an
incompletely known Sm(T): omitting members only shrinks H and raises LO, which
would make the test claim more -- so the missing tail is bounded in the upward
direction by the Euler-product estimate of script 09, and H is rounded UP before
being used.

    CONDITIONAL VERDICT (test 3): omega(N) >= 10 (Nielsen 2015) gives
    |U| >= 6 - alpha, and the (6-alpha) largest members of Sm*(T) must fit
    inside R.  This one does assume Sm(T) is completely known.
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

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
WB   = 500
Y    = 10**24
TARGET = F(18,13)

def geom(t,k): return F(sum(t**i for i in range(k+1)), t**k)
f_ord = lambda t: geom(t,2)
sup   = lambda t: F(t, t-1)

def bounds_T(T, alpha, sp_in_T, nt_in_T):
    roles = ['o']*alpha + (['s'] if sp_in_T else []) + ['n']*nt_in_T
    lo = hi = None
    for perm in set(permutations(range(len(T)))):
        l = F(1); h = F(1); ok = True
        for r, i in zip(roles, perm):
            t = T[i]
            if r == 'o': l *= f_ord(t); h *= f_ord(t)
            elif r == 'n': l *= geom(t,4); h *= sup(t)
            else:
                if t % 12 != 1: ok = False; break
                l *= geom(t,1); h *= sup(t)
        if not ok: continue
        if lo is None or l < lo: lo = l
        if hi is None or h > hi: hi = h
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

def tail_bound(T):
    best=None; lnY=math.log(Y)
    for k in range(1,100):
        eps=0.5*k/100.0
        if eps>=0.5: break
        v=-eps*lnY
        for t in T: v-=math.log(1.0-t**(eps-0.5))
        if best is None or v<best: best=v
    return math.exp(best)/(1-Y**-0.5)

W_POOL=[p for p in range(5,WB) if isprime(p) and p%3==2]
POOL  =[p for p in range(7,TMAX) if isprime(p) and p%3==1]

def w_configs(m, sp_in_W):
    out=[]
    for k in range(m+1):
        for combo in combinations(W_POOL,k):
            for sp_pos in (range(k) if sp_in_W else [None]):
                mn=F(1); mx=F(1); bad=False
                for j,w in enumerate(combo):
                    if sp_in_W and j==sp_pos:
                        if w%12!=5: bad=True; break
                        mn*=geom(w,1)
                    else: mn*=geom(w,4)
                    mx*=sup(w)
                if bad: continue
                mx *= F(WB,WB-1)**(m-k)
                out.append((mn,mx,set(combo)))
            if sp_in_W and k<m:
                mn=F(1); mx=F(1)
                for w in combo: mn*=geom(w,4); mx*=sup(w)
                mx *= F(WB,WB-1)**(m-k)
                out.append((mn,mx,set(combo)))
    return out

print(f"pool T: primes = 1 mod 3 in [7,{TMAX}) : {len(POOL)}")
print(f"pool W: primes = 2 mod 3 in [5,{WB})   : {len(W_POOL)}")
print()
hdr=f"{'tau':>4} {'alpha':>6} {'sp':>3} {'#nt':>4} {'|W|':>4} {'sets':>7} {'uncond':>9} {'needs t3':>9} {'ALIVE':>7}"
print(hdr); print("-"*len(hdr))
smcache={}; grand=[]; TU=TC=TA=0
for alpha in (0,1,2):
    for sp_in_T in (0,1):
        if alpha + (1-sp_in_T) > 2: continue
        for nt_in_T in (0,1,2):
            tau = alpha+sp_in_T+nt_in_T
            if tau < 1 or tau > 5: continue
            m = 3-sp_in_T-nt_in_T
            need_U = 6-alpha
            wcfgs = w_configs(m, sp_in_W=(1-sp_in_T))
            nu=nc=0; alive=[]
            for rest in combinations([p for p in POOL if p!=13], tau-1):
                T=tuple(sorted((13,)+rest))
                lo,hi = bounds_T(T,alpha,sp_in_T,nt_in_T)
                if lo is None: nu+=1; continue
                if T not in smcache: smcache[T]=(smooth_x(T), tail_bound(T))
                S,tb = smcache[T]
                etb = math.exp(1.000001*tb)
                survived=None; used3=False
                for mn,mx,expl in wcfgs:
                    LO = lo*mn; HI = hi*mx
                    Su=[x for x in S if x not in expl]
                    for _ in range(40):
                        R = TARGET/LO
                        H = F(1); keep=[]
                        for x in Su:
                            if f_ord(x) <= R: H*=f_ord(x); keep.append(x)
                        Hf = float(H)*etb
                        Hup = F(math.ceil(Hf*10**12)+1, 10**12)
                        nl = TARGET/Hup
                        if nl <= LO: break
                        LO = nl
                    if LO >= HI or LO > TARGET: continue        # UNCONDITIONAL
                    used3 = True
                    if len(keep) < need_U: continue             # conditional
                    pr=F(1)
                    for x in keep[-need_U:]: pr *= f_ord(x)
                    if pr > TARGET/LO: continue                 # conditional
                    survived=(T,sorted(expl),keep,float(LO),float(HI)); break
                if survived is not None: alive.append(survived)
                elif used3: nc+=1
                else: nu+=1
            tot=nu+nc+len(alive); TU+=nu; TC+=nc; TA+=len(alive)
            print(f"{tau:>4} {alpha:>6} {sp_in_T:>3} {nt_in_T:>4} {m:>4} {tot:>7} {nu:>9} {nc:>9} {len(alive):>7}")
            grand += alive
G=TU+TC+TA
print("-"*len(hdr))
print(f"{'ALL':>24} {G:>19} {TU:>9} {TC:>9} {TA:>7}")
print()
print(f"unconditional share: {100.0*TU/G:.2f}%   surviving: {TA}")
for a in grand[:25]: print("   ", a)
