#!/usr/bin/env python3
"""
Can better lower bounds on m(a,b,c) rescue the section 2 method at k = 2?
No -- and the corrected analysis is cleaner than my first pass.
"""
from decimal import Decimal as D, getcontext
getcontext().prec = 40
A2 = D(1)
for s in [5,29,59,863,1667,1733,2819,306419,1345913,3619619,68839637]:
    A2 *= D(s)/D(s-1)
Ainf_pairs = D("1.01178747704420359446")     # their k=1 value, B=7, pairs

print("="*74)
print("CORRECTION to case (ii)")
print("="*74)
print("""My first pass treated case (ii) with TRIPLE classes and a size floor B = 5.
That was wrong-headed.  If the second notable n_2 = 2 (mod 3), then n_2 can
NEVER divide sigma(s^2) for an ordinary s, because every prime factor of
s^2+s+1 other than 3 is = 1 (mod 3).  So c = 0 for every ordinary prime: the
class structure collapses back to the k = 1 PAIRS, and the floor stays at 7
because only p and n_1 ever appear.

Only A_1 changes, since it must now cover three non-ordinary components.""")
A1_ii = D(13)/D(12)*D(7)/D(6)*D(5)/D(4)
b_ii = A1_ii*A2*Ainf_pairs
print(f"   A_1   = {A1_ii:.6f}   (p=13, n_1=7, n_2=5)")
print(f"   A_2   = {A2:.6f}   (the k=1 classes, unchanged)")
print(f"   A_inf = {Ainf_pairs:.6f}   (the k=1 tail, unchanged)")
print(f"   bound = {b_ii:.6f}    exceeds 2? {b_ii>2}")
print("   Same verdict, but now established with k=1 data only and no guesswork.")

print()
print("="*74)
print("CASE (i) FAILS WITH NO TAIL CONTRIBUTION AT ALL")
print("="*74)
A1_i = D(13)/D(12)*D(7)/D(6)*D(19)/D(18)
partial = A1_i*A2*(D(17)/D(16))*(D(11)/D(10))
print(f"   A_1                       = {A1_i:.6f}")
print(f"   A_2 (k=1 classes)         = {A2:.6f}")
print(f"   class (0,0,1), s = 17     = {D(17)/D(16):.6f}")
print(f"   class (0,1,1), s = 11     = {D(11)/D(10):.6f}")
print(f"   product, A_inf set to 1   = {partial:.6f}    exceeds 2? {partial>2}")

print()
print("="*74)
print("WHY BETTER DATA CANNOT HELP")
print("="*74)
print(f"""The bound is a PRODUCT over classes of m/(m-1), where m is the smallest
admissible ordinary prime in that class.  Better data can only raise some m,
which lowers that class's factor.  But the figures above use:

  - the 11 tabulated m(a,b) of the k = 1 analysis, which are already exact;
  - m = 17 for the class 'sigma(s^2) is the second notable prime', exact
    because 5 and 17 are provably the two smallest ordinary s with s^2+s+1
    prime and = 1 mod 6;
  - m = 11 for the class 'sigma(s^2) = n_1 n_2', exact because
    11^2+11+1 = 133 = 7*19 and no smaller ordinary s works;
  - A_inf = 1 in case (i), i.e. the entire tail DISCARDED.

Every ingredient is either exact or discarded in the method's favour, so no
improvement to the m(a,b,c) data can bring either case below 2.  Computing
better lower bounds on the triple-class minima is therefore POINTLESS for
rescuing this method: the failure is driven by exactly-known small solutions,
not by pessimistic estimates.

Case (i) margin over 2: {float(partial-2):.6f}   Case (ii) margin: {float(b_ii-2):.6f}""")
