#!/usr/bin/env python3
"""
Novelty check on the k0(q) table, resolved.

Several turns ago I derived, elementarily, that an odd perfect number with
least prime factor q has omega(N) >= k0(q), where k0(q) is the least k with
prod of the k smallest primes >= q of p/(p-1) exceeding 2.  I flagged that this
might be classical and asked for Kishore/Norton to check.  The literature list
in the user's older brief settles it without needing those papers:

    "omega(N) >= 12 if 3 does not divide N (Nielsen 2007);
     >= 15 if 3,5 do not divide N (Norton);
     >= 27 if 3,5,7 do not divide N."

Those hypotheses are exactly q >= 5, q >= 7, q >= 11.  Compare:
"""
from fractions import Fraction
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def primes_from(q,c):
    o=[];p=q
    while len(o)<c:
        if isprime(p): o.append(p)
        p+=2
    return o
def k0(q):
    P=primes_from(q,600); v=Fraction(1); k=0
    while v<=2:
        v*=Fraction(P[k],P[k]-1); k+=1
    return k

print(__doc__)
cited={5:("12 (Nielsen)",12), 7:("15 (Norton)",15), 11:("27 (Norton)",27)}
print(f"{'q':>4} {'hypothesis':>22} {'k0(q) computed':>16} {'cited bound':>16} {'verdict':>12}")
for q in (5,7,11,13,17,19,23):
    hyp = {5:'3 does not divide N',7:'3,5 do not',11:'3,5,7 do not',
           13:'3,5,7,11 do not',17:'3,...,13 do not',19:'3,...,17 do not',
           23:'3,...,19 do not'}[q]
    k=k0(q)
    if q in cited:
        name,val=cited[q]
        verdict = 'MATCHES' if k==val else ('weaker' if k<val else 'stronger')
        print(f"{q:>4} {hyp:>22} {k:>16} {name:>16} {verdict:>12}")
    else:
        print(f"{q:>4} {hyp:>22} {k:>16} {'-':>16} {'(extension)':>12}")
print()
print("""CONCLUSION.  k0(7) = 15 and k0(11) = 27 reproduce Norton's cited bounds
EXACTLY.  That is decisive: the k0 computation is Norton's method, not a new
result, and the values at q >= 13 are simply the same computation continued,
which is presumably also classical.  I should not have called the table new,
and it is recorded here as a reconstruction.

At q = 5 my elementary k0(5) = 7 is WEAKER than Nielsen's 12, which is right:
Nielsen's bound is a genuinely deeper result than the abundancy count, so the
two agreeing at q = 7 and q = 11 but not q = 5 is exactly the expected pattern
(Norton's are abundancy-style, Nielsen's is not).

What the table was actually used for in this project is unaffected: it served
as an audit instrument against Mantovanelli's M = 18, and the audit's decisive
argument is Proposition A, which needs no omega bound at all.""")
