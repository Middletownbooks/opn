#!/usr/bin/env python3
"""Does the production/avoidance framework have closure power, or only
constraining power?  Two negative results and one positive structural one."""
from fractions import Fraction
def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True
def primes(lo,hi): return [p for p in range(lo,hi) if isprime(p)]
def oddpart(n):
    while n%2==0: n//=2
    return n
def divisors(n): return sorted(d for d in range(1,n+1) if n%d==0)
def gcd(a,b):
    while b: a,b=b,a%b
    return a
def pfactors(n):
    f=set(); d=2
    while d*d<=n:
        while n%d==0: f.add(d); n//=d
        d+=1
    if n>1: f.add(n)
    return f

print("="*74)
print("NEGATIVE RESULT 1.  Abundancy + cardinality cannot force any prime into S.")
print("="*74)
print("""One might hope that since prod_{p|N} p/(p-1) > 2 only barely holds for the
k0(q) smallest primes >= q, the support must be 'dense among small primes'.
It must not.  omega(N) has no upper bound, so for ANY prime P the primes >= P
can supply the required product on their own.""")
for q,P in ((17,101),(17,1009)):
    v=Fraction(1); k=0; p=P
    while v<=2:
        while not isprime(p): p+=2
        v*=Fraction(p,p-1); k+=1; p+=2
    print(f"   q={q}: a support using only primes >= {P:>6} reaches abundancy 2 "
          f"with k={k} primes (largest {p}).")
print("   And this never stops working: sum_p 1/p diverges (Mertens), so for")
print("   EVERY bound P the primes >= P supply the required product on their own.")
print("   So no particular prime is forced.  Any argument of this shape is dead;")
print("   this is the natural wrong turn and it is worth recording as closed.")

print()
print("="*74)
print("PROPOSITION D.  Lemma OC alone can never block a non-Euler production.")
print("="*74)
print("""Let r in S be produced by a non-Euler witness p of order d = ord_r(p) > 1,
so d | r-1 and d | n_p with n_p odd, hence d odd.  By Theorem 2 the admissible
residues of p mod an odd prime l < q are
      {1}  if l does not divide d,   together with   {x : x^d != 1 mod l}.
The count is  A(d,l) = (l-1) - gcd(d,l-1) + [l does not divide d].
A(d,l) = 0 requires BOTH (l-1) | d AND l | d.  But l-1 is even and d is odd,
so (l-1) | d is impossible.  Hence A(d,l) >= 1 for every l < q: no non-Euler
production order is ever excluded outright.  QED""")
print()
print("Verification of A(d,l) >= 1 over all odd d <= 999 and odd primes l < 60:")
mn=min(( (l-1)-gcd(d,l-1)+(0 if d%l==0 else 1), d, l)
        for d in range(1,1000,2) for l in primes(3,60))
print(f"   minimum of A(d,l) over that range = {mn[0]} (attained at d={mn[1]}, l={mn[2]})")

print()
print("However the constraint is strong, and quantifiable.  For q=17 the")
print("admissible density of a non-Euler witness producing r by order d is")
print("prod_{l in {3,5,7,11,13}} A(d,l)/(l-1):")
print()
LS=[3,5,7,11,13]
def density(d):
    v=Fraction(1)
    for l in LS:
        A=(l-1)-gcd(d,l-1)+(0 if d%l==0 else 1)
        v*=Fraction(A,l-1)
    return v
print(f"{'r':>5} {'oddpart(r-1)':>13} {'production':>10} {'admissible non-Euler orders d>1':>34} {'best density':>13}")
for r in primes(17,120):
    op=oddpart(r-1)
    ds=[d for d in divisors(op) if d>1]
    free = any(f>=17 for f in pfactors(op)) if op>1 else False
    kind = 'free' if free else ('ORDER-1 ONLY' if not ds else 'hard')
    best = max((density(d) for d in ds), default=Fraction(0))
    print(f"{r:>5} {op:>13} {kind:>10} {str(ds):>34} {float(best):>13.4f}")

print()
print("'free'          = oddpart(r-1) has a prime factor >= q, so an order d")
print("                  coprime to every constraint exists; production is cheap.")
print("'hard'          = every prime factor of oddpart(r-1) is < q, so Lemma OC")
print("                  bites and the witness is confined to the stated density.")
print("'ORDER-1 ONLY'  = r-1 is a power of 2, so a non-Euler witness must have")
print("                  order 1: p = 1 mod r and r | n_p, forcing e_p >= r-1 and")
print("                  a new support prime = 1 mod r.  This is the expensive")
print("                  case the paper's forced mechanism exploits at r = q.")
