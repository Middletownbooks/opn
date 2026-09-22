#!/usr/bin/env python3
"""
A cutoff for max(T):  reducing the infinite family to a finite check.

The sweeps run over T drawn from a finite pool.  Here is the reduction that
would make them exhaustive.

LEMMA (tail of one large prime).  Let T = T' u {t*} with t* >= B and every
element of T' below B.  Then

    g(T)  =  g(T') * t*/(t*-1)  <=  g(T') * B/(B-1),

and, writing Sm(T) = Sm(T') u E where E is the set of x with t* | x^2+x+1,

    sum_{x in E} 1/x  <=  (1 + 1/(sqrt(B)-1)) * [ u/(1-u) ] * prod_{t in T'}
                          (1 - t^{-1/2})^{-1},      u = B^{-1/2},

because every x in E has x^2+x+1 = t*^c * M' with c >= 1 and M' T'-smooth, so
x > sqrt(t*^c M') - 1, distinct x give distinct values, and the double sum
factors as an Euler product.  Hence

    h(T)  <=  h(T') * exp(1.01 * that bound).

COROLLARY.  If for EVERY 4-subset T' of the primes = 1 (mod 3) below B
containing 13,

    g(T') * h(T') * (B/(B-1)) * exp(1.01 * tail(T', B))  <=  18/13,

then every |T| = 5 set with max(T) >= B is killed by test 2, and the sweep over
the pool below B is exhaustive.  The same shape works for |T| = 4 and below.

This script prints the numerical size of the correction factor, so one can see
what margin the finite check has to clear.
"""
import math
from itertools import combinations

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

def euler(Tp):
    v = 1.0
    for t in Tp: v /= (1.0 - t**-0.5)
    return v

print(f"{'B':>12} {'B/(B-1)':>10} {'Euler(7,13,19,31)':>19} {'tail bound':>12} "
      f"{'total correction':>18}")
Tp = [7, 13, 19, 31]
E = euler(Tp)
for B in (10**3, 10**4, 10**6, 10**8, 10**10, 10**12, 10**16):
    u = B**-0.5
    tail = (1 + 1/(math.sqrt(B)-1)) * (u/(1-u)) * E
    corr = (B/(B-1.0)) * math.exp(1.01*tail)
    print(f"{B:>12} {B/(B-1.0):>10.8f} {E:>19.6f} {tail:>12.3e} {corr:>18.9f}")
print()
print("So for B = 10^8 the whole correction is below 1.0004: a finite check on")
print("the 4-subsets below B, clearing 18/13 by a factor 1.0004, would make the")
print("|T| = 5 sweep exhaustive.  The current |T| = 4 sweep (script 11) clears")
print("tests 1-2 for 91.2% of 4-subsets below 400 but not all, so this cutoff is")
print("NOT yet available -- it is the missing ingredient, not a completed step.")
