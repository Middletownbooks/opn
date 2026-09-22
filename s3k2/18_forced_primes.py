#!/usr/bin/env python3
"""
Feeding the forcing tree into the abundancy test.

The recursion of script 17 leaves exactly one exceptional seed, S = {13, 31},
with margin 0.997482 -- 0.25% short of a cutoff.  The binding role assignment is
"13 special with e = 1, 31 ordinary", which gives the smallest possible
PROD_T-contribution (14/13) * (993/961) = 1.1127705.

But on that branch min(T) = 13, i.e. 7 does not divide N -- and
sigma(13^1) = 14 = 2 * 7 forces 7 | N.  So e = 1 is inadmissible there.

GENERAL RULE.  Every prime factor of sigma(C) divides 2N, so every ODD prime
factor divides N; the ones = 1 (mod 3) lie in T.  Hence, on a branch where the
smallest element of T is MIN, an exponent is inadmissible for a component
t^k in T whenever sigma(t^k) has a prime factor = 1 (mod 3) that is smaller
than MIN.  Detecting that needs only trial division by the primes = 1 (mod 3)
below MIN -- no factorisation of the huge sigma values.

This raises the role minima, and hence LO, on exactly the branches where the
cutoff was failing.  Admissible exponents:
    ordinary  k = 2 exactly
    special   k = 1 (mod 4), and k != 2 (mod 3) when alpha = 2 (3-budget)
    notable   k even >= 4,   and k != 2 (mod 3) when alpha = 2
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math

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
def sigma(t,k): return sum(t**i for i in range(k+1))

SMALL1 = [p for p in range(7, 2000) if p % 3 == 1 and isprime(p)]

def admissible(t, k, MIN):
    """sigma(t^k) must not be divisible by a prime = 1 (mod 3) below MIN."""
    v = sigma(t, k)
    for q in SMALL1:
        if q >= MIN: break
        if q != t and v % q == 0: return False
    return True

def min_factor(t, role, MIN, alpha):
    """smallest admissible sigma(t^k)/t^k for the given role, as a Fraction."""
    if role == 'o':
        return geom(t, 2) if admissible(t, 2, MIN) else None
    if role == 's':
        if t % 12 != 1: return None
        for k in range(1, 200, 4):
            if alpha == 2 and k % 3 == 2: continue
            if admissible(t, k, MIN): return geom(t, k)
        return None
    for k in range(4, 200, 2):
        if alpha == 2 and k % 3 == 2: continue
        if admissible(t, k, MIN): return geom(t, k)
    return None

print("S = {13, 31}, the exceptional seed.  MIN = 13, so 7 must not divide N.")
print()
print(f"{'role':>10} {'prime':>6} {'smallest admissible k':>24} {'factor':>12}")
for role, name in (('o','ordinary'), ('s','special'), ('n','notable')):
    for t in (13, 31):
        f = min_factor(t, role, 13, 2)
        ks = []
        if role == 'o': ks = [2]
        elif role == 's': ks = [k for k in range(1,60,4) if not (k%3==2)]
        else: ks = [k for k in range(4,60,2) if not (k%3==2)]
        kk = next((k for k in ks if admissible(t,k,13)), None)
        print(f"{name:>10} {t:>6} {str(kk):>24} "
              f"{('%.7f'%float(f)) if f is not None else 'role impossible':>12}")
print()
print("sigma(13^1) = 14 = 2*7  -> 7 | N, contradicting MIN = 13, so e = 1 is out.")
print("sigma(13^5) = 5229043 ; sigma(13^9) = ... ; the first admissible e is"
      " printed above.")
print()

FULL = ('o','o','s','n','n')
def subprofiles(L): return sorted({tuple(sorted(c)) for c in combinations(FULL,L)})

def bounds(T, roles, MIN, alpha=2, forced=True):
    lo=hi=None
    for perm in set(permutations(range(len(T)))):
        l=F(1); h=F(1); ok=True
        for r,i in zip(roles,perm):
            t=T[i]
            f = min_factor(t, r, MIN if forced else 0, alpha)
            if f is None: ok=False; break
            l *= f
            h *= (geom(t,2) if r=='o' else F(t,t-1))
        if not ok: continue
        if lo is None or l<lo: lo=l
        if hi is None or h>hi: hi=h
    return lo,hi

S = (13,31)
for forced in (False, True):
    los=[];his=[]
    for pr in subprofiles(2):
        lo,hi = bounds(S, pr, 13, 2, forced)
        if lo is None: continue
        los.append((lo,pr)); his.append(hi)
    LO=min(los)[0]; HI=max(his)
    tag = "with forced-prime filter" if forced else "without (script 17)"
    print(f"   LO0({S}) {tag:28s} = {float(LO):.7f}   "
          f"(binding profile {min(los)[1]})")
print()
print("The threshold that matters: 5 stays in Sm*(T) only while")
print("   R = (18/13)/LO0  >=  1 + 1/5 + 1/25 = 1.24,  i.e.  LO0 <= 1.1166324.")
