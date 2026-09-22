#!/usr/bin/env python3
"""
|T| = 5 : the smoothness side.

Every ordinary prime x = 2 (mod 3) has sigma(x^2) = x^2+x+1 with 3 not dividing
it, and every prime factor of x^2+x+1 is = 1 (mod 3), hence lies in T.  So

        U  is contained in  Sm(T) = { x prime, x = 2 (mod 3), x^2+x+1 T-smooth }.

x^2+x+1 = M has a solution iff 4M-3 is a perfect square, so Sm(T) is found
EXACTLY (up to the search bound B) by running over all T-smooth M <= B.
Finiteness of Sm(T) is a Thue-Mahler statement for the form X^2+XY+Y^2; the
search below is complete up to B and I flag the largest solution found.

Combined with:
  * PROD_T * PROD_U = 18/13 and the role minima  ->  PROD_U <= R(T);
  * omega(N) >= 10 (Nielsen 2007) and omega(N) = 1 + |T| + |U|  ->  |U| >= 4;
T dies unless the four smallest members of Sm(T) already satisfy
        prod (1 + 1/x + 1/x^2)  <=  R(T).
"""
import math
from fractions import Fraction as F
from itertools import combinations

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

fs = lambda t: F(t+1, t)
fo = lambda t: F(t*t+t+1, t*t)
fn = lambda t: F(t**4+t**3+t*t+t+1, t**4)

def min_prod_T(T):
    best = None
    for i, s in enumerate(T):
        if s % 12 != 1: continue
        rest = [T[j] for j in range(5) if j != i]
        for nb in combinations(range(4), 2):
            od = [rest[j] for j in range(4) if j not in nb]
            v = fs(s)*fn(rest[nb[0]])*fn(rest[nb[1]])*fo(od[0])*fo(od[1])
            if best is None or v < best: best = v
    return best

def smooth_set(T, B):
    """all x prime, x = 2 mod 3, with x^2+x+1 T-smooth and x^2+x+1 <= B."""
    out = []
    T = list(T)
    def rec(i, m):
        if i == len(T):
            d = 4*m - 3
            r = math.isqrt(d)
            if r*r == d and (r-1) % 2 == 0:
                x = (r-1)//2
                if x >= 2 and x % 3 == 2 and isprime(x): out.append(x)
            return
        v = m
        while v <= B:
            rec(i+1, v)
            v *= T[i]
    rec(0, 1)
    return sorted(set(out))

TARGET = F(18, 13)
B = 10**32

P1 = [p for p in range(7, 400) if isprime(p) and p % 3 == 1]
print(f"search bound on x^2+x+1 : B = 10^32   (so x up to ~10^16)")
print()
print(f"{'T':28s} {'R(T)':>9} {'Sm(T)  (x = 2 mod 3, x^2+x+1 T-smooth)':>44} {'verdict':>9}")
print("-"*98)

dead = 0; alive = []
tested = 0
for rest in combinations([p for p in P1 if p != 13], 4):
    T = tuple(sorted((13,) + rest))
    if T[0] != 7: continue            # the sets containing 7: the tightest ones
    if T[4] > 200: continue
    m = min_prod_T(T)
    if m is None: continue
    R = TARGET / m
    if R < 1: 
        print(f"{str(list(T)):28s} {float(R):>9.6f} {'-- killed by abundancy alone --':>44} {'DEAD':>9}")
        dead += 1; tested += 1; continue
    S = smooth_set(T, B)
    tested += 1
    # the four smallest admissible members
    ok = [x for x in S if F(x*x+x+1, x*x) <= R]
    prod = F(1); need4 = None
    for x in ok:
        prod *= fo(x)
        if prod > R: break
    fits = 0; prod = F(1)
    for x in ok:
        if prod * fo(x) > R: break
        prod *= fo(x); fits += 1
    verdict = "DEAD" if fits < 4 else "alive"
    if verdict == "DEAD": dead += 1
    else: alive.append(T)
    print(f"{str(list(T)):28s} {float(R):>9.6f} {str(S)[:44]:>44} {verdict:>9}")

print("-"*98)
print(f"tested {tested} sets T with 7,13 in T and max(T) < 200 : {dead} dead, {len(alive)} alive")
if alive: print("   alive:", alive)
