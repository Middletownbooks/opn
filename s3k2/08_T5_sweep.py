#!/usr/bin/env python3
"""
|T| = 5 at k = 2:  a two-sided fixed-support test, swept over all admissible T.

THE TEST.  In the sub-case |T| = 5 the prime divisors of N are exactly
{3} u T u U, where U is the set of ordinary primes = 2 (mod 3).  Splitting
sigma(N)/N = 2 by component gives the exact identity

        2 = (13/9) * PROD_T * PROD_U,        i.e.   PROD_T * PROD_U = 18/13.

Two upper bounds, both elementary:

  g(T) = prod_{t in T} t/(t-1)                 >  PROD_T     (any exponents)
  h(T) = prod_{x in Sm(T), x >= 5} (1+1/x+1/x^2)  >=  PROD_U

where Sm(T) = { x prime, x = 2 (mod 3), every prime factor of x^2+x+1 in T }.
The second bound is what makes this work: an ordinary component contributes
EXACTLY 1+1/x+1/x^2, and U is forced to sit inside Sm(T) because every prime
factor of x^2+x+1 is = 1 (mod 3) and divides N.

        >>> if  g(T) * h(T) <= 18/13  then T is impossible. <<<

SCOPE / HONESTY.  Sm(T) is computed from the factorisations of x^2+x+1 for all
primes x = 2 (mod 3) up to the bound XMAX below, so h(T) is a lower estimate of
the true h(T): a member x > XMAX would raise it by a factor < 1 + 1/XMAX.  Sm(T)
is finite (Thue-Mahler for the form X^2+XY+Y^2), but I have not enumerated it
completely, so the sweep's verdicts are conditional on no large members.  The
margin by which each T fails is printed so the reader can see how much room a
missed member would have to make up.
"""
from fractions import Fraction as F
from itertools import combinations
import sys

def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

XMAX  = 3 * 10**6      # primes x = 2 (mod 3) up to here
TMAX  = 500            # T drawn from primes = 1 (mod 3) below this
TARGET = 18/13

# ---- sieve primes up to XMAX ------------------------------------------------
sieve = bytearray([1])*(XMAX+1); sieve[0]=sieve[1]=0
for i in range(2,int(XMAX**0.5)+1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
primes = [i for i in range(2,XMAX+1) if sieve[i]]

def factorset(n, small):
    f = set()
    for p in small:
        if p*p > n: break
        while n % p == 0: f.add(p); n //= p
    if n > 1: f.add(n)
    return f

small = [p for p in primes if p <= 2*10**6]

# ---- index: for each x = 2 (mod 3) with all factors of x^2+x+1 below TMAX ----
POOL = [p for p in primes if p < TMAX and p % 3 == 1]
poolset = set(POOL)
from collections import defaultdict
bysig = defaultdict(list)
cnt = 0
for x in primes:
    if x < 5 or x % 3 != 2: continue
    v = x*x + x + 1
    fs = factorset(v, small)
    if fs <= poolset:
        bysig[frozenset(fs)].append(x)
        cnt += 1
print(f"primes x = 2 (mod 3) below {XMAX}: whose x^2+x+1 factors all lie in the")
print(f"pool of {len(POOL)} primes = 1 (mod 3) below {TMAX}:  {cnt}")
print()
print("the signatures F(x) = set of prime factors of x^2+x+1, smallest x first:")
shown = sorted(((min(v), sorted(k), v) for k, v in bysig.items()))[:18]
for mn, k, v in shown:
    print(f"   F = {str(k):24s}  x = {str(sorted(v))[:44]}")
print()

sigs = [(frozenset(k), sum_) for k, sum_ in
        ((k, None) for k in bysig)]
sig_val = {}
for k, xs in bysig.items():
    p = F(1)
    for x in xs: p *= F(x*x+x+1, x*x)
    sig_val[k] = p

# ---- sweep ------------------------------------------------------------------
print("=" * 78)
print(f"SWEEP over all 5-subsets T of the pool with 13 in T   (test: g*h <= 18/13)")
print("=" * 78)
alive = []; dead = 0; worst = []
rest_pool = [p for p in POOL if p != 13]
for rest in combinations(rest_pool, 4):
    T = (13,) + rest
    Ts = frozenset(T)
    g = F(1)
    for t in T: g *= F(t, t-1)
    h = F(1)
    for k, val in sig_val.items():
        if k <= Ts: h *= val
    gh = g * h
    if gh > TARGET:
        alive.append((sorted(T), float(g), float(h), float(gh)))
    else:
        dead += 1
        worst.append((float(gh), sorted(T)))
tot = dead + len(alive)
print(f"   5-subsets tested : {tot}")
print(f"   killed (g*h <= 18/13 = {TARGET:.9f}) : {dead}")
print(f"   surviving        : {len(alive)}")
print()
if alive:
    print("   SURVIVING SETS:")
    for T, g, h, gh in sorted(alive, key=lambda z: -z[3])[:40]:
        print(f"      T = {str(T):28s} g = {g:.6f}  h = {h:.6f}  g*h = {gh:.6f}")
worst.sort(reverse=True)
print()
print("   the killed sets with the SMALLEST margin (closest to surviving):")
for gh, T in worst[:12]:
    print(f"      T = {str(T):28s} g*h = {gh:.9f}   deficit factor {TARGET/gh:.6f}")
