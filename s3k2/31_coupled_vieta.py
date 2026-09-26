#!/usr/bin/env python3
"""
The coupled branch of section 13b, closed exactly: no search bound.

SETTING (NOTES_S3_K2.md section 13b, "13 not ordinary").  tau = 3, alpha = 2,
T = {13, a1, a2} with 13 the special prime and a1, a2 distinct ordinary primes,
both = 1 (mod 3).  Closure gives F(a1) <= {13, a2} and F(a2) <= {13, a1}.
Script 30 split this into

  * an uncoupled branch -- some (a^2+a+1)/3 is a pure power of 13 -- which is
    the equation of section 13a;
  * the COUPLED branch  a2 | a1^2+a1+1  AND  a1 | a2^2+a2+1,  which it searched
    only over a1 < 2*10^6.

This script replaces that search by a proof.

STEP 1 (Vieta jumping).  Distinct primes are coprime and a1 | a1^2 + a1, so the
coupled condition gives  a1*a2 | a1^2 + a2^2 + a1 + a2 + 1,  i.e.

        x^2 + y^2 + x + y + 1 = k x y       for some integer k >= 1.

Fix k and take a solution (x <= y) with x + y minimal.  The other root of
Y^2 - (kx-1) Y + (x^2+x+1) = 0 is y' = kx-1-y = (x^2+x+1)/y, a positive
integer.  If y > x then y^2 >= (x+1)^2 > x^2+x+1, so y' < y and (x, y') is a
smaller solution -- contradiction.  So y = x, then x^2 | 2x^2+2x+1 forces x = 1
and k = 5.  Hence k = 5 for EVERY solution.

For k = 5, y = x+1 is impossible (it gives 3x^2 + x - 3 = 0), so a solution with
x < y has y >= x+2, and then y' = (x^2+x+1)/y <= x.  The move (x,y) -> (y',x) is
therefore a strict descent with inverse (x,y) -> (y, 5y-1-x); every solution
descends to (1,1), and so every solution is a consecutive pair of

        a_0 = a_1 = 1,   a_{n+1} = 5 a_n - a_{n-1} - 1 :   1, 1, 3, 13, 61, 291, ...

with the identity  a_n^2 + a_n + 1 = a_{n-1} a_{n+1}  (Vieta's product).

STEP 2 (closure pins it).  Put {a1, a2} = {a_n, a_{n+1}}, a_n < a_{n+1}.  a_2 = 3
is not = 1 (mod 3) and a_3 = 13 is the special, so n >= 4 and a_n >= 61.

  (i)  F(a_n) <= {13, a_{n+1}} and v_3 = 1 give a_n^2+a_n+1 = 3 * 13^x * a_{n+1}^y
       with y >= 1; y = 1 because a_{n+1}^2 > a_n^2+a_n+1.  Vieta's product then
       gives  a_{n-1} = 3 * 13^x.
  (ii) F(a_{n+1}) <= {13, a_n} gives a_{n+1}^2+a_{n+1}+1 = 3 * 13^u * a_n^v with
       v >= 1, so  a_{n+2} = 3 * 13^u * a_n^(v-1).

RATIO LEMMA.  4.6 a_m < a_{m+1} < 5 a_m for every m >= 3.  (Upper: a_{m+1} =
5a_m - a_{m-1} - 1.  Lower, by induction from a_4/a_3 = 61/13 > 4.6: a_{m+1} >
5a_m - a_m/4.6 - 1 = 4.78.. a_m - 1 > 4.6 a_m once a_m >= 6.)

  v = 1:  a_{n+2} = 3*13^u and a_{n-1} = 3*13^x, so a_{n+2}/a_{n-1} = 13^(u-x);
          but n-1 >= 3 puts that ratio in (4.6^3, 5^3) = (97.3, 125), which
          contains no power of 13.
  v = 2:  a_{n+2}/a_n = 3*13^u, but the ratio lies in (4.6^2, 5^2) = (21.2, 25),
          which contains neither 3 nor 39 (nor any 3*13^u).
  v >= 3: a_{n+2} >= 3 a_n^2 > 25 a_n since a_n >= 61; contradiction.

So the coupled branch is EMPTY.  No search bound, no primality of the a_i, no
Thue-Mahler input.  Primality is not even used.

This script checks every step that can be checked numerically:
  (A) the classification: every pair x <= y with x | y^2+y+1 and y | x^2+x+1 and
      x <= XMAX is a consecutive pair of the sequence (and all such pairs occur);
  (B) the identity a_n^2+a_n+1 = a_{n-1} a_{n+1} and the ratio lemma for n <= NMAX;
  (C) the conclusion directly: no n in range satisfies both closure conditions;
  (D) script 30's direct search, re-run to 10^5, still finds nothing (a
      reproduction check of the old method, not an input to the proof).
"""
import math

XMAX = 30000
NMAX = 400

# ---------------------------------------------------------------- sequence
a = [1, 1]
while len(a) < NMAX + 3:
    a.append(5*a[-1] - a[-2] - 1)
consecutive = {(a[i], a[i+1]) for i in range(len(a)-1)}

# ---------------------------------------------------------------- (A)
def divisors_upto(n, lo):
    """all divisors d >= lo of n (n small enough to factor by trial division)"""
    f = {}; m = n; d = 2
    while d*d <= m:
        while m % d == 0: f[d] = f.get(d, 0) + 1; m //= d
        d += 1 if d == 2 else 2
    if m > 1: f[m] = f.get(m, 0) + 1
    ds = [1]
    for p, e in f.items():
        ds = [x * p**k for x in ds for k in range(e+1)]
    return [x for x in ds if x >= lo]

pairs = set()
for x in range(1, XMAX+1):
    for y in divisors_upto(x*x+x+1, x):          # y | x^2+x+1, y >= x
        if (y*y+y+1) % x == 0:
            pairs.add((x, y))
seq_pairs_in_range = {(u, v) for (u, v) in consecutive if u <= XMAX}
print("(A) pairs x<=y, x<=%d, with x|y^2+y+1 and y|x^2+x+1:" % XMAX)
print("      found      :", sorted(pairs))
print("      sequence   :", sorted(seq_pairs_in_range))
assert pairs == seq_pairs_in_range, "classification FAILS"
print("      identical -> classification confirmed in range")
for (x, y) in pairs:
    assert x*x + y*y + x + y + 1 == 5*x*y
print("      every pair has k = 5")

# ---------------------------------------------------------------- (B)
for n in range(1, NMAX+1):
    assert a[n]*a[n] + a[n] + 1 == a[n-1]*a[n+1]
for m in range(3, NMAX+1):
    assert 46*a[m] < 10*a[m+1] < 50*a[m]
print("(B) Vieta product and 4.6 < a_{m+1}/a_m < 5 hold for all n <= %d" % NMAX)

# ---------------------------------------------------------------- (C)
def strip(v, ps):
    for p in ps:
        while v % p == 0: v //= p
    return v
hits = []
for n in range(2, NMAX+1):
    lo, hi = a[n], a[n+1]
    c1 = strip((lo*lo+lo+1), (3, 13, hi)) == 1 and (lo*lo+lo+1) % hi == 0
    c2 = strip((hi*hi+hi+1), (3, 13, lo)) == 1 and (hi*hi+hi+1) % lo == 0
    if c1 and c2: hits.append((n, lo, hi))
print("(C) consecutive pairs meeting both closure conditions, n <= %d:" % NMAX, hits)
# empty: even (3, 13) fails, since 13^2+13+1 = 3*61 and 61 is not in {3, 13, 3}.
assert not hits

# ---------------------------------------------------------------- (D)
def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for b in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(b, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
found = []
for a1 in range(7, 10**5):
    if a1 % 3 != 1 or not isprime(a1): continue
    M = strip(a1*a1+a1+1, (3, 13))
    if M == 1: continue
    # M must be a power of a single prime a2 = 1 mod 3
    r = 1; base = None
    for e in range(1, 40):
        b = round(M ** (1.0/e))
        for c in (b-1, b, b+1):
            if c > 1 and c**e == M and isprime(c): base = c
        if base: break
    if base is None or base % 3 != 1 or base == a1: continue
    if strip(base*base+base+1, (3, 13, a1)) == 1: found.append((a1, base))
print("(D) script-30 style direct search, a1 < 10^5:", found)
assert not found
print("\nCoupled branch of section 13b: EMPTY, by proof (steps 1-2 of the docstring).")
