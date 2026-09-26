#!/usr/bin/env python3
"""
The six pool-free profiles of section 13c, now with no search bound.

Section 13 removed the pool from six profiles but left them resting on search
bounds (section 13d).  Script 31 (Vieta jumping) and script 32 (Skolem's
method) replace every one of those bounds that has a single free exponent.
The two Sm counts are made single-exponent by a VALUATION step:

    an ordinary prime a has e_a = 2 = sum over components C != a^2 of v_a(sigma(C)),
    every term >= 0, so contributions already forced cap what U may use.

This script assembles the chain for each profile and asserts every numerical
fact it uses.  The only input left is omega(N) >= 10 (Nielsen 2015, a theorem).
"""
import importlib.util, os
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sk", os.path.join(here, "32_skolem.py"))
sk = importlib.util.module_from_spec(spec); spec.loader.exec_module(sk)

def v(p, n):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k

def exact(Df, p):
    sols, status = sk.solve(Df, p)
    assert status == "complete", (Df, p, status)
    return sols

def U_candidates(sols):
    """x usable in U: prime, = 2 (mod 3)"""
    return sorted({x for c, x in sols if x >= 2 and x % 3 == 2 and sk.isprime(x)})

def ordinary_candidates(sols):
    """x usable as an ordinary prime of T: prime, = 1 (mod 3)"""
    return sorted({x for c, x in sols if x >= 2 and x % 3 == 1 and sk.isprime(x)})

# ------------------------------------------------------------------ facts
assert 3*3 + 3 + 1 == 13                       # sigma(3^2)
assert 13*13 + 13 + 1 == 3 * 61                # sigma(13^2)
assert 61*61 + 61 + 1 == 3 * 13 * 97           # sigma(61^2)
assert 97 % 12 == 1 and 61 % 12 == 1           # both may be special

print("Profiles with T = {13}  (alpha = 0: rows 0,no,1,1,2 and 0,yes,0,1,2)")
S13 = exact([], 13)
print("   x^2+x+1 = 13^c, all c:", S13, "-> U-usable:", U_candidates(S13))
assert U_candidates(S13) == []
print("   Sm({13}) = {} exactly; need |U| >= 6.  DEAD.\n")

print("Profile 1,no,0,1,3 (|W| = 3): section 11b, no computation.  DEAD.\n")

print("Profiles with tau = 2, alpha = 1 (rows 1,no,1,2,2 and 1,yes,0,2,2), section 13a")
E = exact([3], 13)
print("   (t^2+t+1)/3 = 13^c, all c:", E, "-> ordinary-usable:", ordinary_candidates(E))
assert ordinary_candidates(E) == []
print("   so t is not ordinary; 13 is, F(13) = {61}, T = {13, 61}.")
print("   13 ordinary: e_13 = 2, and sigma(3^2) = 13 spends one unit, so every x in U")
print("   has v_13(x^2+x+1) <= 1:  x^2+x+1 = 61^c  or  13 * 61^c.")
A, B = exact([], 61), exact([13], 61)
print("     61^c   :", A, "   13*61^c :", B)
assert U_candidates(A) == [] and U_candidates(B) == []
print("   U = {} exactly; need |U| >= 5.  DEAD.\n")

print("Profile 2,yes,0,3,2 (tau = 3, alpha = 2), section 13b")
print("   (i) 13 special: F(a1) <= {13,a2}, F(a2) <= {13,a1}.")
print("       uncoupled -> (a^2+a+1)/3 = 13^c: no ordinary-usable solution (above);")
print("       coupled   -> empty by Vieta jumping (script 31).")
print("   (ii) 13 ordinary, so 61 in T.  If a2 != 61 then 61 is the special and")
print("       F(a2) <= {13, 61}; e_13 = 2 with sigma(3^2) spending one unit gives")
print("       v_13(a2^2+a2+1) <= 1:  (a2^2+a2+1) = 3 * 61^c  or  39 * 61^c.")
C, D = exact([3], 61), exact([3, 13], 61)
print("       3*61^c :", C, "   39*61^c :", D)
cands = [x for x in ordinary_candidates(C) + ordinary_candidates(D) if x not in (13, 61)]
assert cands == []
print("       only x = 13, which is a1 itself.  So a2 = 61 and T = {13, 61, 97}.")
print("   T = {13,61,97}: 13 and 61 ordinary, 97 special.")
print(f"       e_13: sigma(3^2) gives {v(13,13)}, sigma(61^2) gives {v(13,61*61+61+1)} -> U may use 0")
print(f"       e_61: sigma(13^2) gives {v(61,13*13+13+1)}                       -> U may use at most 1")
print("       so every x in U has x^2+x+1 = 97^c or 61 * 97^c.")
F1, F2 = exact([], 97), exact([61], 97)
print("       97^c :", F1, "   61*97^c :", F2)
assert U_candidates(F1) == [] and U_candidates(F2) == []
print("   U = {} exactly; need |U| >= 4.  DEAD.\n")

print("All six pool-free profiles of section 13c are eliminated using only")
print("omega(N) >= 10 (Nielsen 2015).  No search bound, no Thue-Mahler assumption.")
