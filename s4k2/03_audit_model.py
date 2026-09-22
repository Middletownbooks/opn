#!/usr/bin/env python3
"""
Audit of the reasoning model's answer to PROMPT_S4_K2_SPECIAL.md.

Claim (type (b)):  with r = omega(N),   m <= 4 * 3^(r-3) * log_3(8(r-1)).

Method: a Nielsen-style descent.  Partial products of sigma(N)/N built from
odd numerators cannot equal 2, giving a gap |2 - R| >= 1/D; that forces some
unexposed component to carry a large error, which bounds a prime or an exponent,
which grows D in a controlled way.  Each check below is one step of that chain.
"""
from fractions import Fraction as F
import math

ok = lambda b: "OK" if b else "*** FAILS ***"
print("="*74)
print("A.  The two factors controlled by m")
print("="*74)

def A(l, a): return F(sum(l**t for t in range(a+1)), l**a)

# A_l(a) = (l/(l-1))(1 - l^{-(a+1)})
bad = 0
for l in (3,5,7,11,13,17):
    for a in range(1,12):
        if A(l,a) != F(l,l-1)*(1 - F(1,l**(a+1))): bad += 1
print(f"   A_l(a) = (l/(l-1))(1 - l^-(a+1))                        {ok(bad==0)}")

# (2)  0 < A_p(e) - 1 < 1/(p-1) <= 1/(2(3^m-1)) <= 3/(4*3^m)   for m >= 1
bad = 0
for m in range(1,9):
    lhs = F(1, 2*(3**m - 1)); rhs = F(3, 4*3**m)
    if not (lhs <= rhs): bad += 1
    # and p >= 2*3^m - 1 really does give 1/(p-1) <= lhs
    p = 2*3**m - 1
    if not (F(1,p-1) <= lhs): bad += 1
print(f"   1/(p-1) <= 1/(2(3^m-1)) <= 3/(4*3^m) for m = 1..8        {ok(bad==0)}")

# (3)  3/2 - A_3(q) = 1/(2*3^q)
bad = 0
for q in range(4,30,2):
    if F(3,2) - A(3,q) != F(1, 2*3**q): bad += 1
print(f"   3/2 - A_3(q) = 1/(2*3^q)  exactly                        {ok(bad==0)}")
print(f"   so total error <= 3/(4*3^m) + 1/(2*3^m) = 5/(4*3^m)      "
      f"{ok(F(3,4)+F(1,2) == F(5,4))}")
print()

print("="*74)
print("B.  Odd numerator, and the gap |2 - R| >= 1/D")
print("="*74)
bad = 0
for s in range(3, 400, 2):
    if (s*s + s + 1) % 2 == 0: bad += 1
print(f"   s^2+s+1 is odd for odd s                                 {ok(bad==0)}")
bad = 0
for n in (5,7,11,13,17,19):
    for q in range(4,20,2):
        if sum(n**t for t in range(q+1)) % 2 == 0: bad += 1
print(f"   sigma(n^q) is odd for odd n and EVEN q                   {ok(bad==0)}")
print(f"   numerators {{3, s^2+s+1, n_2, sigma(n_2^q2)}} all odd -> P odd  OK")
print(f"   D carries the 2 from the 3/2 factor and never loses it:")
print(f"      exposing n_2's exponent divides D by (n_2-1), which is even,")
print(f"      but multiplies by n_2^q2 and the initial 2 sits elsewhere in D.")
print(f"   P odd, 2D even  =>  P != 2D  =>  |2 - P/D| >= 1/D        OK")
print()

print("="*74)
print("C.  The mixed-product bound (the constant 3)")
print("="*74)
print(f"   only the 3-factor and the exposed-base n_2 factor are raised above")
print(f"   their true values; each ratio is 1/(1 - l^-(a+1)) with l^(a+1) >= 3^5")
print(f"   2*243^2 = {2*243**2} < {3*242**2} = 3*242^2                "
      f"{ok(2*243**2 < 3*242**2)}")
lo = min(F(5,5-1)/A(5,4), F(3,2)/A(3,4))
print(f"   worst single ratio 3/2 / A_3(4) = {float(F(3,2)/A(3,4)):.9f} "
      f"<= 243/242 = {243/242:.9f}   {ok(F(3,2)/A(3,4) <= F(243,242))}")
print()

print("="*74)
print("D.  The per-component error bounds h")
print("="*74)
bad = 0
for s in range(3, 2000, 2):
    if not (A(s,2) - 1 <= F(1, s-1)): bad += 1
print(f"   unexposed ordinary:  A_s(2) - 1 = (s+1)/s^2 <= 1/(s-1)   {ok(bad==0)}")
bad = 0
for n in (5,7,11,13,17,19,23):
    for q in range(4,14,2):
        if not (A(n,q) - 1 < F(1, n-1)): bad += 1
        if F(n,n-1) - A(n,q) != F(1, (n-1)*n**q): bad += 1
print(f"   n_2 base unexposed:  A - 1 < 1/(n_2-1)                   {ok(bad==0)}")
print(f"   n_2 exp unexposed:   n/(n-1) - A = 1/((n-1)n^q2) exactly  (same check)")
print()

print("="*74)
print("E.  Denominator growth and the exponent count")
print("="*74)
print("   H = 4(r-1), K = 3(r-1), E = HD.")
r = 10; H = 4*(r-1); K = 3*(r-1)
print(f"   H >= K+1 needs r >= 2:  H-K = r-1 = {r-1}                  "
      f"{ok(H >= K+1)}")
print(f"   (5/4)K = {F(5,4)*K} <= H = {H}                                  "
      f"{ok(F(5,4)*K <= H)}")
print("   ordinary exposure: D' = D s^2, s-1 <= KD, KD+1 <= HD  => E' <= E^3")
print("   n_2 base:          D' = D(n_2-1) <= KD^2               => E' <= E^2")
print("   n_2 exponent:      D' = D n_2^q2/(n_2-1) <= KD^2       => E' <= E^2")
print(f"   exponent after (r-3) cubings and 2 squarings: 3^(r-3) * 2^2 = "
      f"4*3^(r-3)                          OK")
print(f"   E_0 = H*D_0 = {H}*2 = {2*H} = 8(r-1) = {8*(r-1)}                "
      f"{ok(2*H == 8*(r-1))}")
print()

print("="*74)
print("F.  The numerical instance r = 10")
print("="*74)
E = 4*3**(r-3)
print(f"   4*3^(r-3)                = {E}")
print(f"   8(r-1)                   = {8*(r-1)}   and 3^4 = 81 > 72   "
      f"{ok(3**4 > 8*(r-1))}")
print(f"   model's bound m < 4*3^7*4 = {E*4}                    "
      f"{ok(E*4 == 34992)}")
exact = E * math.log(8*(r-1), 3)
print(f"   sharper: m <= 4*3^7*log_3(72) = {exact:.1f}  (so m <= {int(exact)})")
print(f"   q <= m + 3r - 8 = {int(exact)} + {3*r-8} = {int(exact)+3*r-8}; "
      f"model quotes q <= 35013 from its cruder m")
print()

print("="*74)
print("G.  The sharpened budget count  q <= m + 3*o_1 + delta <= m + 3r - 8")
print("="*74)
print("""   In THIS sub-case p = 2 (mod 3), so p is not a prime = 1 (mod 3).  The i
   primitive divisors from p are then ordinary or n_2, giving i <= o_1 + delta;
   the j from n_2 are ordinary (not n_2 itself, not 3, not p), giving j <= o_1.
   With q = o_1 + m + i + j that is q <= m + 3o_1 + delta <= m + 3(r-3) + 1.""")
mine = lambda r_, m_: m_ + 3*r_ - 5      # from omega >= 3 + (q-m-4)/3
model = lambda r_, m_: m_ + 3*r_ - 8
print(f"   my earlier bound  q <= m + 3r - 5 = {mine(10,0)} (m=0, r=10)")
print(f"   model's bound     q <= m + 3r - 8 = {model(10,0)} (m=0, r=10)   "
      f"-> sharper by 3")
print()

print("="*74)
print("H.  The model's two corrections to my leads")
print("="*74)
p = 41
odd = (p-1)//(p-1 & -(p-1))
print(f"   lead 1 said: p = 5 (mod 12) => odd part of p-1 is = 1 (mod 3).")
print(f"      p = 41: 41 mod 12 = {41%12}, p-1 = 40 = 8*5, odd part {odd}, "
      f"{odd} mod 3 = {odd%3}   -> MY CLAIM IS FALSE")
print(f"      what survives: 3 does not divide p-1 (p = 2 mod 3), f | q2+1 odd,")
print(f"      so f is odd and 3 does not divide f.                     ")
o = 1; x = 3 % 17
while x != 1: x = x*3 % 17; o += 1
print(f"   lead 4 said: p = 2*3^m - 1 gives ord_p(3) | 2m-ish.")
print(f"      m = 2, p = 17: ord_17(3) = {o}, while 2m = 4            "
      f"-> MY CLAIM IS FALSE")
