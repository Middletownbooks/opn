#!/usr/bin/env python3
"""
THEOREM 1' (input classification at EVERY prime divisor -- minimality is never
used), and its consequence: Proposition E is the width-one case.

Setting: N odd perfect, S its prime support, pi the Euler prime, alpha the
Euler exponent, n_p = e_p + 1.

THEOREM 1'.  Let r be ANY prime with r | N.  Write r - 1 = 2^a * mu(r) with
mu(r) odd.  Then there exists p in S, p != r, with v_r(sigma(p^{e_p})) > 0
(an r-input witness), and
    p non-Euler  =>  ord_r(p) | mu(r),
    p = pi       =>  ord_r(pi) | 2*mu(r).

PROOF.  r | N gives e_r >= 1, and the r-adic valuation balance
e_r = sum_{p in S, p != r} v_r(sigma(p^{e_p})) is a positive sum of nonnegative
integers, so some term is positive.  For such a p, the cyclotomic input
condition gives ord_r(p) | n_p (order-one convention: r | n_p), and Fermat
gives ord_r(p) | r - 1.  If p is non-Euler then e_p is even, so n_p is odd, so
ord_r(p) is odd and divides mu(r).  If p = pi then n_pi = alpha + 1 = 2 mod 4,
so v_2(ord_r(pi)) <= 1 and ord_r(pi) | 2*mu(r).   QED

NOTHING IN THAT PROOF USES q = min S.  The version recorded earlier as
Theorem 1 is the special case r = q.  Define the PRODUCTION WIDTH of r to be
w(r) = d(mu(r)), the number of odd divisors of r - 1.  Then r admits exactly
w(r) non-Euler input orders and 2*w(r) Euler input orders, so 3*w(r) input
types in all.

PROPOSITION E is exactly the case w(r) = 1, i.e. mu(r) = 1, i.e. r - 1 is a
power of two: r is a Fermat prime.  Then the only non-Euler order is 1, which
forces p = 1 mod r and r | n_p, hence e_p >= r - 1.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def oddpart(n):
    while n%2==0: n//=2
    return n
def ndiv(n):
    return sum(1 for d in range(1,n+1) if n%d==0)

print(__doc__)
print("Production width w(r) = d(oddpart(r-1)) for the small primes:")
print(f"{'r':>5} {'r-1':>6} {'mu(r)':>7} {'w(r)':>5} {'input types 3w(r)':>18}  {'':<3}")
w1=[]
for r in range(3, 300):
    if not isprime(r): continue
    mu=oddpart(r-1); w=ndiv(mu)
    tag='  <-- Fermat prime, width 1' if w==1 else ''
    if w==1: w1.append(r)
    if r<100 or w==1:
        print(f"{r:>5} {r-1:>6} {mu:>7} {w:>5} {3*w:>18}{tag}")
print()
print("Width-1 primes below 300:", w1)
print()
print("="*74)
print("THE REACH OF PROPOSITION E, STATED HONESTLY")
print("="*74)
print("""w(r) = 1 iff r - 1 is a power of 2 iff r is a Fermat prime.  The only known
Fermat primes are 3, 5, 17, 257, 65537, and no others are known to exist (it is
open whether any do; none exist below 2^2^32).  So Proposition E has content
for at most five primes, and in a minimal-prime branch q = min S only for the
Fermat primes >= q.  For q = 17 that is F in {17, 257, 65537}.

That is a real ceiling on Proposition E and it should be stated plainly: it is
a sharp statement about a very thin set of primes, not a general tool.

What survives the ceiling is Theorem 1', which is the general statement.  The
useful invariant is w(r), and Proposition E is its extreme case.  Primes of
small width are the ones that are hard to produce; width grows slowly, so the
constraint is real across the board rather than only at five primes.""")
print()
print("Distribution of production width over primes r < 10000:")
from collections import Counter
c=Counter()
for r in range(3,10000):
    if isprime(r): c[ndiv(oddpart(r-1))]+=1
tot=sum(c.values())
for w in sorted(c):
    if w<=8: print(f"   w(r) = {w:>2}: {c[w]:>5} primes ({100*c[w]/tot:5.2f}%)")
print(f"   w(r) > 8: {sum(v for k,v in c.items() if k>8):>5} primes")
