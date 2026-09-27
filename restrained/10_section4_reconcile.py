#!/usr/bin/env python3
"""
Reconcile the Section 4 arithmetic of Ochem-Zelinsky (arXiv:2607.19746v1) with the
full transcript (sources/ochem_zelinsky_2607.19746_transcript.txt).

The paper says:
  (a) the sieve ran "until it said to need more than 2,500,000,000 ordinary primes up
      to z = 216,171,986,291 only to reach abundancy 1.088507187872";
  (b) "Suppose that N contains only 43,500,000,000 prime factors greater than z";
  (c) 3/2 * (1 + 1/6,000,000) * 1.076855990994 * (1 + 1/z)^43,500,000,000
        ~ 1.99209763359616948564;
  (d) hence N has more than 2.5e9 + 43.5e9 = 46e9 ordinary primes, and Lemma 8 gives
      q >= 23e9.

Script 02 found that (c) does not reproduce.  This script shows which inputs DO
reproduce the printed value, and checks that the conclusion (d) follows from the
sieve output (a) with the K of (b).  It checks the arithmetic only; whether the sieve
output (a) is correct is a separate question (NOTES_RESTRAINED.md 4b, the overflow).
"""
from decimal import Decimal as D, getcontext
getcontext().prec = 50

z = D(216171986291)
A_sieve = D("1.088507187872")         # (a)
A_prod = D("1.076855990994")          # the constant written inside (c)
K_text = D(43500000000)               # (b)
k_text = D(2500000000)                # (a)
stated = D("1.99209763359616948564")  # (c)
base = D(3) / 2 * (1 + D(1) / 6000000)
L = (1 + 1 / z).ln()

def prod(A, K): return base * A * (1 + 1 / z) ** K

print("1. Which inputs reproduce the printed product 1.99209763359616948564?")
for A, an in [(A_sieve, "A = 1.088507187872 (sieve, (a))"), (A_prod, "A = 1.076855990994 (inside (c))")]:
    for K in (D(43000000000), K_text):
        v = prod(A, K)
        print(f"   {an:34s} K = {int(K):,}:  {v:.20f}   diff {v - stated:+.2e}")
Kimp = (stated / (base * A_sieve)).ln() / L
Aimp = stated / (base * (1 + 1 / z) ** 43000000000)
print(f"   K implied by the printed value with the sieve's A:  {Kimp:,.1f}")
print(f"   A implied by the printed value with K = 43e9:        {Aimp:.13f}")
print("   => the printed product is the SIEVE's abundancy with K = 43,000,000,000, to 10")
print("      significant digits.  The text's K = 43.5e9 and its constant 1.076855990994 are")
print("      not what produced it.  1.076855990994 matches nothing tried here; its source")
print(f"      is unknown (ratio A_sieve / A_prod = {A_sieve / A_prod:.12f}).")
print()

print("2. Does conclusion (d) follow from the sieve output (a) with K = 43.5e9?")
v = prod(A_sieve, K_text)
print(f"   3/2 (1+1/6e6) * 1.088507187872 * (1+1/z)^43.5e9 = {v:.20f}  < 2 ? {v < 2}")
Amax = 2 / (base * (1 + 1 / z) ** K_text)
print(f"   largest sieve abundancy for which K = 43.5e9 still works: {Amax:.12f}"
      f"  (headroom {(Amax / A_sieve - 1) * 100:.3f}%)")
print()

print("3. The rigorous form of the count.")
print("   If N has m ordinary primes, the largest possible product of their abundancies")
print("   takes every sieve survivor below z first (each exceeds 1 + 1/z), then primes")
print("   above z.  So m <= k + K forces abundancy < 2 whenever 3/2 (1+1/6e6) A (1+1/z)^K < 2,")
print("   and therefore m >= k + K_max + 1, with K_max the largest such K.")
Au = A_sieve + D("5e-13")             # the printed A rounded up in its last place
Kmax = int(((2 / (base * Au)).ln() / L).to_integral_value(rounding="ROUND_FLOOR"))
while prod(Au, Kmax) >= 2: Kmax -= 1
print(f"   with A <= {Au} (printed value rounded up):  K_max = {Kmax:,}")
print(f"   k + K_max = {int(k_text) + Kmax:,}   (the paper uses 46,000,000,000;"
      f" margin {int(k_text) + Kmax - 46000000000:,})")
print()

print("4. Lemma 8 arithmetic.")
m = 46000000000 + 1
omega = m + 2                          # plus the special prime p and the notable prime 3
qlow = D(omega) / 2 - 2
print(f"   more than 46e9 ordinary primes: m >= {m:,}, omega(N) = m + 2 >= {omega:,}")
print(f"   q >= omega/2 - 2 >= {qlow}; q is even, so q >= 23,000,000,000.")
print()
print("5. What a re-run of the sieve has to establish (for q >= 23e9 by this route):")
print("   k(z) + K_max(A(z)) >= 46,000,000,000 for some z, where k(z), A(z) are the exact")
print("   survivor count and abundancy of Algorithm 1 run to z.  An over-inclusive sieve")
print("   (a superset of the true survivors) still gives a valid bound, because each")
print("   survivor r < z changes k + K_max by 1 - z*ln(r/(r-1)) <= 0.")
