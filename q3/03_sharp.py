#!/usr/bin/env python3
"""NO2CYCLE pushed: the sharp production condition, the tournament theorem,
and a test of its predictions against real data from the literature."""
import re
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def primes(a,b): return [p for p in range(a,b) if isprime(p)]
def leg(a,p):
    r=pow(a%p,(p-1)//2,p)
    return -1 if r==p-1 else r
def v2(n):
    v=0
    while n%2==0: n//=2; v+=1
    return v
def sig_mod(t,e,r):
    s=0; x=1
    for _ in range(e+1):
        s=(s+x)%r; x=(x*t)%r
    return s

print("="*74); print("1.  SHARP PRODUCTION CONDITION (power-residue form of Theorem 1')"); print("="*74)
print("""A non-Euler t produces r only if ord_r(t) | n_t, which is odd; equivalently

    ord_r(t) | oddpart(r-1)  <=>  t is a 2^a-th power residue mod r,  a = v_2(r-1).

    r = 3 (mod 4)  a = 1   t must be a QUADRATIC residue mod r  (density 1/2)
    r = 5 (mod 8)  a = 2   t must be a QUARTIC residue mod r    (density 1/4)
    r = 1 (mod 8)  a >= 3  t must be a 2^a-th power residue     (density 2^-a)

Lemma QR is the a = 1 case, where it is EXACT.  That exactness is what lets
reciprocity act on it.""")
bad=0; n=0
for r in primes(5,300):
    a=v2(r-1)
    for t in primes(3,200):
        if t==r: continue
        prod=any(sig_mod(t,e,r)==0 for e in range(2,60,2))
        pr=pow(t%r,(r-1)>>a,r)==1
        n+=1
        if prod and not pr: bad+=1; print("   FAIL",t,r)
print(f"   {n} (t,r) pairs tested, even exponents to 58: {bad} violations")

print(); print("="*74); print("2.  TOURNAMENT THEOREM"); print("="*74)
print("""T = {p | N : p = 3 (mod 4)}; since pi = 1 (mod 4) every member is non-Euler.
For p, s in T reciprocity gives (p/s)(s/p) = -1, so EXACTLY ONE of the two
symbols is +1.  By the a = 1 case, p can produce s only if (p/s) = 1.  Hence
the production digraph restricted to T lies inside the TOURNAMENT Lambda_T
given by p -> s iff (p/s) = 1, and is 2-cycle-free.  The permitted direction of
every pair is fixed in advance by a Legendre symbol -- no order computation.""")

print(); print("="*74); print("3.  PREDICTION TEST against Ochem-Zelinsky's 3p2.txt"); print("="*74)
print("""Each line 'X^2 => ... r ...' asserts X produces r.  When X and r are both
3 (mod 4) the theorem predicts r canNOT produce X; as X = 3 (mod 4) that is
exactly (r/X) = -1, tested directly below.""")
pairs=set()
for line in open('../restrained/3p2.txt'):
    m=re.match(r'^\s*(\d+)\^2\s*=>\s*(.*)$', line)
    if not m: continue
    X=int(m.group(1))
    if X%4!=3 or not isprime(X): continue
    for t in m.group(2).split():
        if t in ('F','XS'): break
        mm=re.match(r'^(\d+)(?:\^\d+)?$', t)
        if mm:
            r=int(mm.group(1))
            if r!=X and r%4==3 and isprime(r): pairs.add((X,r))
pairs=sorted(pairs); ok=0; fail=[]
for X,r in pairs:
    if leg(r,X)==-1: ok+=1
    else: fail.append((X,r))
print(f"   pairs (X -> r), both 3 mod 4, found in the file : {len(pairs)}")
print(f"   of these, (r/X) = -1 so r cannot produce X      : {ok}")
print(f"   violations                                      : {len(fail)}  {fail if fail else ''}")
print(); print("   sample of the free deductions:")
for X,r in pairs[:10]:
    print(f"      {X:>6} produces {r:<8} => {r} cannot produce {X}    "
          f"[({X}/{r})={leg(X,r):+d}, ({r}/{X})={leg(r,X):+d}, product={leg(X,r)*leg(r,X):+d}]")

print(); print("="*74); print("4.  WHAT THIS DOES NOT GIVE, AND WHY"); print("="*74)
print("""Recorded so they are not repeated:

(a) Longer cycles.  A directed cycle inside T forces every forward symbol to +1
    and, by reciprocity, every backward symbol to -1 -- perfectly consistent.
    Cycles of length >= 3 are NOT obstructed; only 2-cycles die.

(b) In-degree starvation.  Each p in T needs in-degree >= 1 in the full
    digraph.  One might hope a vertex of Lambda_T with in-degree 0 must be
    produced from outside T, but tournaments need not have such a vertex, and
    producers may lie outside T anyway: the Euler prime can produce ANY
    p = 3 (mod 4) unconstrained, since ord_p(pi) | p-1 has v_2 <= 1
    automatically when v_2(p-1) = 1.

(c) At q = 3 specifically.  3 is in T.  Producers of 3 are = 1 (mod 3), i.e.
    = 1 or 7 (mod 12); 3 produces only primes = +-1 (mod 12).  Those meet T in
    the DISJOINT classes 7 and 11 (mod 12), so NO2CYCLE is automatically
    satisfied at 3 and adds nothing there.  This is the decisive negative for
    the q = 3 application.

(d) Stronger reciprocity.  For r = 1 (mod 4) the production condition is
    quartic or higher, so an obstruction would need biquadratic or octic
    reciprocity.  Rational biquadratic laws exist (Burde, Gauss), so this is a
    real avenue -- not attempted here.""")
