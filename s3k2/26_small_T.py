#!/usr/bin/env python3
"""
The large-|W| profiles of section 3 at k = 2, and why SMALL T is an advantage.

Recall |W| = 3 - beta and tau = |T| = alpha + beta, with the budget inequality
alpha + [special in W] <= 2.  So

    |W| = 3  ->  beta = 0, the special is in W, alpha <= 1, and 13 in T forces
                 alpha = 1: exactly ONE profile, T = {13}.
    |W| = 2  ->  beta = 1, so tau = alpha + 1 <= 3.

That is the reverse of what the abundancy test likes -- W's unknown components
carry the slack -- but it is exactly what the SMOOTHNESS side likes.  U is
contained in

    Sm(T) = { x prime, x = 2 (mod 3) : x^2 + x + 1 is T-smooth }

and with |T| = 1 that is the single classical equation x^2+x+1 = p^c, with
|T| = 2 or 3 a two- or three-prime equation.  Those can be searched to bounds
enormously beyond the 10^24 used for |T| = 5, because the count of T-smooth
numbers below Y grows like (log Y)^{|T|}.

Counting then finishes the job: omega(N) >= 10 (Nielsen 2015) and
omega(N) = 1 + tau + |W| + |U| = 4 + alpha + |U| give

    |U| >= 6 - alpha  >= 4,      U inside Sm(T),

so any T with fewer than 6 - alpha admissible members is impossible.
"""
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

def solve_one(p, CMAX):
    """all x >= 2 with x^2+x+1 = p^c, c <= CMAX.  Exact: 4p^c - 3 must be square."""
    out=[]; M=1
    for c in range(1, CMAX+1):
        M *= p
        d = 4*M - 3
        r = math.isqrt(d)
        if r*r == d and r % 2 == 1:
            out.append((c, (r-1)//2))
    return out

print("=" * 72)
print("|T| = 1 : the single-prime equation  x^2 + x + 1 = p^c")
print("=" * 72)
CMAX = 1200
print(f"   searched exactly for every c <= {CMAX}  (for p = 13 that is "
      f"p^c up to about 10^{int(CMAX*math.log10(13))})")
print()
print(f"   {'p':>6}  solutions (c, x)")
for p in [pp for pp in range(7, 200) if pp % 3 == 1 and isprime(pp)]:
    s = solve_one(p, CMAX)
    keep = [(c,x) for c,x in s]
    usable = [(c,x) for c,x in s if x % 3 == 2 and isprime(x) and x >= 5]
    print(f"   {p:>6}  {str(keep):38s} usable for U: {usable}")
print()
print("""   Every solution in this range comes from c = 1, i.e. x^2+x+1 = p itself:
   x = 2, 3, 5, 6, 8, 12 and (at c = 3) x = 18.  Only x = 5 (p = 31) is both
   prime and = 2 (mod 3), so among single-prime T only Sm({31}) = {5} is
   non-empty; every other Sm({p}) here is EMPTY -- and verified far beyond any
   bound available for larger T.  In particular Sm({13}) = {} , since its one
   solution x = 3 is = 0 (mod 3).""")
print()
print("=" * 72)
print("CONSEQUENCE for the |W| = 3 profile")
print("=" * 72)
print("""   |W| = 3 forces beta = 0, the special = 2 (mod 3), hence alpha <= 1; and
   13 in T forces alpha = 1, so T = {13} and 13 is ordinary.  Then

       U is inside Sm({13}) = empty,     so |U| = 0,
       omega(N) = 1 + 1 + 3 + 0 = 5.

   Nielsen's omega(N) >= 10 is contradicted outright.  The whole |W| = 3 branch
   is ONE configuration and it dies on a count, with no abundancy input at all
   and no pool restriction -- T = {13} is forced, not chosen from a pool.""")
