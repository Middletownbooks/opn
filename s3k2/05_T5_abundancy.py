#!/usr/bin/env python3
"""
Section 3 (3 ordinary, 3^2 || N) at k = 2, sub-case |T| = 5.

SETTING.  N is 2-restrained: exactly two components n_1^{q_1}, n_2^{q_2} have
even exponent q_i >= 4 (NOTABLE), one component p^e has p = e = 1 (mod 4)
(SPECIAL), every other component is x^2 (ORDINARY).  Section 3 assumes 3 is
ordinary, so 3^2 || N and e_3 = 2 exactly.

T  = the primes = 1 (mod 3) dividing N.   13 in T always, since sigma(3^2)=13.
A  = ordinary primes in T;   |A| <= 2 by the 3-budget (script 01).
U  = ordinary primes = 2 (mod 3).

|T| = 5 is the maximal case: |A| = 2 AND p, n_1, n_2 all = 1 (mod 3).
Then the prime divisors of N are exactly  {3} u T u U, with |T| = 5,
and T = A u {p, n_1, n_2}.

THE EXACT ABUNDANCY IDENTITY.  sigma(N)/N = 2 factors over components:

    2 = (13/9) * PROD_T * PROD_U ,     PROD_U = prod_{x in U} (1 + 1/x + 1/x^2)

so       PROD_T * PROD_U = 18/13 = 1.3846153...

Since PROD_U >= 1 this gives a RIGOROUS, FINITE test:

    >>> if the minimum possible PROD_T over all role assignments to T
    >>> already exceeds 18/13, that T is impossible. <<<

Role minima (each decreasing in t, so the minimum is at the smallest exponent):
    special  e = 1 (mod 4), min at e = 1 :  1 + 1/t
    ordinary exponent exactly 2          :  1 + 1/t + 1/t^2
    notable  q >= 4 even, min at q = 4   :  1 + 1/t + 1/t^2 + 1/t^3 + 1/t^4
"""
from fractions import Fraction as F
from itertools import combinations, permutations

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

def f_spec(t): return F(t+1, t)
def f_ord(t):  return F(t*t + t + 1, t*t)
def f_not(t):  return F(t**4 + t**3 + t*t + t + 1, t**4)

def min_prod_T(T):
    """minimum of PROD_T over assignments of 1 special, 2 notable, 2 ordinary."""
    best = None
    for perm in set(permutations(range(5))):
        idx = list(perm)
        s = T[idx[0]]; no = (T[idx[1]], T[idx[2]]); od = (T[idx[3]], T[idx[4]])
        v = f_spec(s) * f_not(no[0]) * f_not(no[1]) * f_ord(od[0]) * f_ord(od[1])
        if best is None or v < best: best = v
    return best

TARGET = F(18, 13)
P1 = [p for p in range(7, 4000) if isprime(p) and p % 3 == 1]   # primes = 1 mod 3

print("=" * 74)
print("RIGOROUS TEST:  PROD_T(min) > 18/13 = %.9f  kills the set T." % float(TARGET))
print("=" * 74)
print()

# T must contain 13.  Enumerate all 5-subsets of the small primes = 1 mod 3.
POOL = [p for p in P1 if p < 400]
killed = []
survivors = []
for rest in combinations([p for p in POOL if p != 13], 4):
    T = tuple(sorted((13,) + rest))
    m = min_prod_T(T)
    if m > TARGET: killed.append((T, m))
    else: survivors.append((T, m))

print(f"5-subsets of primes = 1 (mod 3) below 400 containing 13 : "
      f"{len(killed)+len(survivors)}")
print(f"   killed outright by the abundancy identity             : {len(killed)}")
print(f"   surviving                                             : {len(survivors)}")
print()
print("The killed sets are exactly the ones made of small primes.  Sample:")
for T, m in killed[:12]:
    print(f"   T = {str(list(T)):26s} min PROD_T = {float(m):.9f}")
print()
print("The lexicographically smallest SURVIVING sets:")
for T, m in survivors[:12]:
    print(f"   T = {str(list(T)):26s} min PROD_T = {float(m):.9f}"
          f"   forces PROD_U <= {float(TARGET/m):.6f}")
print()

# how large can max(min T) be among killed sets -> i.e. which primes are excluded
print("=" * 74)
print("WHAT THE TEST ACTUALLY EXCLUDES")
print("=" * 74)
if killed:
    allk = set()
    for T,_ in killed: allk |= set(T)
    print(f"   primes appearing in some killed T : {sorted(allk)}")
    # is every T containing 7 killed?
    with7 = [(T,m) for T,m in survivors if 7 in T]
    print(f"   surviving sets that contain 7      : {len(with7)}")
    if with7:
        for T,m in with7[:8]:
            print(f"        {list(T)}  min PROD_T = {float(m):.9f}")
print()

# Now the complementary, non-rigorous-but-computable direction: for a surviving T,
# U must supply PROD_U = (18/13)/PROD_T, and every x in U has x^2+x+1 T-smooth.
print("=" * 74)
print("THE COMPLEMENTARY CONSTRAINT ON U")
print("=" * 74)
print("""Every ordinary x = 2 (mod 3) has sigma(x^2) = x^2+x+1 with 3 | it false,
and every prime factor of x^2+x+1 is = 1 (mod 3).  Those factors divide N, so
they lie in T.  Hence for every x in U:

        x^2 + x + 1  is T-smooth   (only the five primes of T allowed).

Moreover the two ORDINARY primes of T carry exponent exactly 2, so across ALL
components at most two units of each are available; sigma(3^2) = 13 already
spends one if 13 is ordinary.  So all but at most four members of U satisfy

        x^2 + x + 1  =  p^alpha * n_1^beta * n_2^gamma     (three primes only).

Below: for each of the first surviving T, the primes x = 2 (mod 3), x < 10^5,
whose x^2+x+1 is T-smooth, and the largest PROD_U they could supply.""")
print()

def tsmooth(v, T):
    for t in T:
        while v % t == 0: v //= t
    return v == 1

X = 10**5
cand2 = [x for x in range(5, X) if x % 3 == 2 and isprime(x)]
print(f"{'T':28s} {'PROD_U needed':>14} {'x<1e5 T-smooth':>16} {'max PROD_U':>12}")
for T, m in survivors[:15]:
    need = TARGET / m
    hits = [x for x in cand2 if tsmooth(x*x+x+1, T)]
    mx = F(1)
    for x in hits: mx *= f_ord(x)
    print(f"{str(list(T)):28s} {float(need):>14.6f} {str(hits)[:16]:>16} {float(mx):>12.6f}")
