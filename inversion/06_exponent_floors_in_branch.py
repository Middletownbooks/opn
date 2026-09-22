#!/usr/bin/env python3
"""
COROLLARY 2e (residue-dependent exponent floor in a minimal-prime branch).

Let N be odd perfect, q = min S, and let p in S be non-Euler, so n_p = e_p + 1
is odd and >= 3.  Define the FORBIDDEN SET

   Forb(p) = { r prime : r | n_p is excluded by Theorem 2 }
           = { l < q : p = 1 mod l }  union  { d : d = ord_l(p) is an odd prime
                                                 for some odd prime l < q }.

By Theorem 2 no element of Forb(p) divides n_p.  Since n_p is odd and >= 3,

        n_p  >=  (least prime not in Forb(p)),      e_p >= that - 1.

For q = 17 the relevant data is l in {3,5,7,11,13}, whose binding odd orders
are: l=3 -> {1}; l=5 -> {1}; l=7 -> {1,3}; l=11 -> {1,5}; l=13 -> {1,3}.
So 3 in Forb(p) iff p = 1 mod 3 or ord_7(p) = 3 or ord_13(p) = 3;
   5 in Forb(p) iff p = 1 mod 5 or ord_11(p) = 5;
   7,11,13 in Forb(p) iff p = 1 mod 7, 11, 13 respectively.

CONNECTION TO THE LITERATURE.  The l = 3 instance is NOT new: it is exactly
Zelinsky's (12) together with f_3 = 0, which already gives 'every prime with
e_p = 2 is 2 mod 3' when 3 does not divide N.  What is new relative to that
literature is the extension to every odd l < q, which needs the minimal-prime
hypothesis Zelinsky does not assume.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def order(p,l):
    x,k=p%l,1
    while x!=1: x=(x*p)%l; k+=1
    return k
SMALL=[3,5,7,11,13]
BIND={3:[1],5:[1],7:[1,3],11:[1,5],13:[1,3]}
def forb(p):
    F=set()
    for l in SMALL:
        if p==l: continue
        d=order(p,l)
        if d==1: F.add(l)               # order-one rule: l does not divide n_p
        elif d in BIND[l] or (d>1 and d in (3,5,7,11,13)):
            F.add(d)                    # order-d rule: d does not divide n_p
    return F
def least_allowed(F):
    r=3
    while r in F or not isprime(r): r+=2
    return r

print(__doc__)
print("Forced exponent floors for non-Euler support primes, branch q = 17:")
print(f"{'p':>6} {'Forb(p)':>22} {'n_p >=':>7} {'so e_p >=':>10}")
from collections import Counter
cnt=Counter(); N=0
for p in range(19, 4000):
    if not isprime(p): continue
    F=forb(p); lo=least_allowed(F); N+=1
    cnt[lo-1]+=1
    if p < 200:
        print(f"{p:>6} {str(sorted(F)):>22} {lo:>7} {lo-1:>10}")
print()
print(f"Distribution of the forced floor on e_p over the {N} primes 19 <= p < 4000:")
tot=0
for e in sorted(cnt):
    tot+=cnt[e]
    print(f"   e_p >= {e:<3} forced for {cnt[e]:>4} primes ({100*cnt[e]/N:5.1f}%)   "
          f"cumulative {100*tot/N:5.1f}%")
print()
ge4 = sum(v for k,v in cnt.items() if k>=4)
print(f"=> {100*ge4/N:.1f}% of primes p in this range would be forced to have e_p >= 4")
print("   if they lie in the support of an odd perfect number with min prime 17.")
print()
print("IMPORTANT CAVEAT.  These percentages are properties of the primes in the")
print("stated range, NOT of the support S, which is not a random set.  They")
print("indicate how much the constraint bites; they are not themselves a proof")
print("of anything about N.  Turning Corollary 2e into an improved Omega/omega")
print("inequality requires counting lemmas of Zelinsky's Lemma 4 type for")
print("l = 5,7,11,13, which is the next task and is NOT done here.")
