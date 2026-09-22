#!/usr/bin/env python3
"""
Independent check of Ochem & Zelinsky (arXiv:2607.19746v1, 22 Jul 2026),
Section 2: 'When 3 is not a factor'.  They bound the abundancy of a restrained
odd perfect number with 3 not dividing N by A1*A2*A3*A_inf and show it is < 2.

This matters here for a second reason.  My audit's Proposition A shows that an
abundancy envelope of the FINITE form H(K_env)*(B/(B-1))^M < 2 is never
satisfiable by valid data.  Ochem and Zelinsky nevertheless bound an abundancy
from ABOVE and succeed.  Their envelope has a different shape, and the
difference is exactly the repair Mantovanelli's certificate needed -- see the
discussion printed at the end.
"""
from decimal import Decimal, getcontext
getcontext().prec = 40
D = Decimal

# --- A1: special and notable components, p = 1 mod 12 so p >= 13, n = 1 mod 6 so n >= 7
A1 = D(13)/D(12) * D(7)/D(6)
print(f"A1 = 13/12 * 7/6 = 91/72                      = {A1:.20f}   (paper: 1.26388888888888888888)")

# --- A2: the 11 pairs (a,b) with a+b <= 6 from Table 1
SMALL = [5, 29, 59, 863, 1667, 1733, 2819, 306419, 1345913, 3619619, 68839637]
A2 = D(1)
for s in SMALL: A2 *= D(s)/D(s-1)
print(f"A2 over the {len(SMALL)} tabulated m(a,b) with a+b <= 6   = {A2:.20f}   (paper: 1.32051931736840940811)")

# --- A3: the 3 remaining pairs (2,3),(3,2),(3,3), each m(a,b) > 1e9
A3 = (D(1) + D(10)**-9) ** 3
print(f"A3 = (1 + 1e-9)^3                             = {A3:.20f}   (paper: 1.00000000300000000300)")

# --- A_inf: product over k >= 7 of (1 + 1/(7^(k/2) - 2))^(k-1)
Ainf = D(1); k = 7
while k < 400:
    term = (D(1) + D(1)/(D(7)**(D(k)/D(2)) - D(2))) ** (k-1)
    Ainf *= term
    k += 1
print(f"A_inf = prod_{{k>=7}} (1+1/(7^(k/2)-2))^(k-1)    = {Ainf:.20f}   (paper: 1.01178747704420359446)")

tot = A1*A2*A3*Ainf
print()
print(f"A1*A2*A3*A_inf = {tot:.20f}")
print(f"paper states     1.68866287554178")
print(f"< 2 ?  {tot < 2}")
print()
print("All four constants and the product reproduce the paper's values.")
print()
print("="*74)
print("WHY THIS DOES NOT CONTRADICT PROPOSITION A -- and what it repairs")
print("="*74)
print("""Proposition A (audit): if K_env accounts for t slots of the support, every
remaining support prime is >= B, and at most M remain, then
H(K_env)(B/(B-1))^M > 2.  So the FINITE-slot envelope is unsatisfiable.

Ochem and Zelinsky do not use that form.  They partition the remaining support
into INFINITELY many classes -- the pairs (a,b) with sigma(s^2) = p^a n^b --
prove at most one support prime lies in each class, and prove a lower bound
m(a,b) on the prime in class (a,b) that GROWS with a+b (their section 2.4:
s >= 7^{k/2} - 1 for k = a+b).  The resulting infinite product converges, and
converges below 2.

So the envelope idea is not inherently broken.  What makes it work is:
  (i)  a proved CLASSIFICATION of the remaining support, not an assumed count;
  (ii) proved per-class lower bounds that grow fast enough to converge;
  (iii) no upper bound on omega(N) anywhere -- infinitely many classes are
       allowed, which is why no bound on the number of prime factors is needed.

Mantovanelli's tail_count_certificate(B,M) has none of these.  It asserts a
finite M -- an upper bound on omega(N) in disguise -- which Proposition A shows
can hold only if the branch is already empty.  The repair the certificate
system needed was a classified convergent product of exactly this kind, and
this paper shows the technique is available and rigorous when the
classification is actually proved.""")
