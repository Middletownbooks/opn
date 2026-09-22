#!/usr/bin/env python3
"""
Section 3 at k = 2: what transfers, and the opening tree.

SETTING (their section 3).  N odd perfect, 3 is ORDINARY: 3^2 || N, so e_3 = 2
exactly.  Special p^e with p = e = 1 mod 4.  k notable components n_i^{q_i},
q_i >= 4 even.  Everything else ordinary (exponent 2).
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def v3(n):
    v=0
    while n%3==0: n//=3; v+=1
    return v
print(__doc__)
print("="*74)
print("THE 3-BUDGET IS k-INDEPENDENT")
print("="*74)
print("""e_3 = 2 = sum over all components C != 3^2 of v_3(sigma(C)).  Component by
component, for a prime x != 3 with n_x = e_x + 1:

  x = 1 (mod 3) :  v_3(sigma(x^{e_x})) = v_3(n_x)            [LTE]
  x = 2 (mod 3) :  sigma is a sum of n_x terms alternating +-1 mod 3, so
                   v_3 > 0 only if n_x is EVEN, i.e. only for the Euler prime.

For an ORDINARY x (e_x = 2, n_x = 3):
  x = 1 (mod 3)  ->  v_3 = v_3(3) = 1 exactly;
  x = 2 (mod 3)  ->  v_3 = 0.

So EVERY ordinary prime = 1 (mod 3) spends exactly one unit of a budget of 2,
and ordinary primes = 2 (mod 3) spend nothing.  Hence:

   >>> at most TWO ordinary primes are = 1 (mod 3), at any k. <<<

The notable components spend v_3(q_i+1) each (zero unless n_i = 1 mod 3), and
the special spends v_3(e+1) or v_3(p+1)+v_3((e+1)/2).  More notables can only
TIGHTEN the budget, never loosen it.  This is the engine of section 3 and it is
completely unaffected by k.""")
bad=0
for x in range(5,4000):
    if not isprime(x) or x==3: continue
    got=v3(x*x+x+1); pred=1 if x%3==1 else 0
    if got!=pred: bad+=1; print("   FAIL",x,got,pred)
print(f"\n   verified v_3(sigma(x^2)) = [x = 1 mod 3] for all primes 5 <= x < 4000: "
      f"{bad} failures")
print()
print("="*74)
print("CONSEQUENCE: the regular-support set")
print("="*74)
print("""sigma(3^2) = 13, so 13 | N, and 13 = 1 (mod 3).

Let A = ordinary primes = 1 (mod 3);  |A| <= 2.
Every prime factor of x^2+x+1 other than 3 is = 1 (mod 3), so for an ordinary
x = 2 (mod 3) the whole of sigma(x^2) is supported on

   T = A  u  {p, n_1, ..., n_k} restricted to the residue 1 (mod 3),

with |T| <= 2 + (k+1).  At k = 1 that is <= 4; at k = 2 it is <= 5.""")
from fractions import Fraction as Fr
print()
print("   Why a pure abundancy argument will NOT close section 3 at k = 2:")
print("   the component 3^2 alone contributes sigma(9)/9 = 13/9, and the primes")
print("   of T contribute up to prod t/(t-1).  Taking the five smallest primes")
print("   = 1 mod 3 for T:")
T=[7,13,19,31,37]
v=Fr(13,9)
s=f"13/9"
for t in T:
    v*=Fr(t,t-1); s+=f" * {t}/{t-1}"
print(f"      {s}")
print(f"      = {float(v):.6f}   already {'EXCEEDS' if v>2 else 'below'} 2, before any")
print("      ordinary prime = 2 mod 3 is counted at all.")
print("""
   So unlike section 2, section 3 at k = 2 cannot be closed by fixing the
   support and summing a geometric series: the budget is already gone.  Their
   k = 1 section 3 works only because a factor-tree elimination first removes
   most small primes, after which T is small and explicit.  That elimination is
   the hard part, and it is what grows with k.""")
