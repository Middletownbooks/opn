#!/usr/bin/env python3
"""
The coupled ("Vieta") branch of the closure DFS, closed by a count: no
search bound.

Where it arises (script 38, profile 2,yes,1,4,1): K = {7, 13} carries the
special and the notable, W is the notable 11, and the two remaining T-primes
a < a' are BOTH ordinary and COUPLED: a | a'^2+a'+1 and a' | a^2+a+1.
Script 38 searched such pairs along the Vieta sequence to index 1500.

THE COUNT.  alpha = 2, so omega(N) >= 10 forces |U| >= 4.  T = {7, 13, a, a'}.
  * a is ordinary, so e_a = 2 = sum over C != a^2 of v_a(sigma(C)), every term
    >= 0.  Coupling gives v_a(sigma(a'^2)) >= 1, so sum over x in U of
    v_a(x^2+x+1) <= 1.  At most ONE member of U has a | x^2+x+1.
  * The same holds for a'.
  * Every other x in U has x^2+x+1 {7,13}-smooth, i.e. x lies in Sm({7,13}).
    (W = {11} and U are primes = 2 (mod 3), which never divide x^2+x+1.)
  * Script 39 (Matveev + LLL) proves that the COMPLETE set of integers with
    x^2+x+1 {7,13}-smooth is {0, 2, 3, 9, 18} (with -1-x).  None is a prime
    x >= 5 with x = 2 (mod 3).
  * Hence |U| <= 2 < 4: dead, for every coupled pair, with no enumeration.
The argument uses neither the Vieta classification nor any bound on a.
"""
import importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bl", os.path.join(here, "39_baker_lll.py"))
bl = importlib.util.module_from_spec(spec); sys.argv = ['x']; spec.loader.exec_module(bl)

sols, L = bl.solve_complete((7, 13), 0, log=lambda *a: None)
print("complete {x : x^2+x+1 is {7,13}-smooth}, x >= 0:", [x for x in sols if x >= 0])
usable = [x for x in sols if x >= 5 and x % 3 == 2 and bl.isprime(x)]
print("usable in U (prime, >= 5, = 2 mod 3):", usable)
assert usable == []
need = 6 - 2
print(f"|U| <= 2 (one member for a, one for a')  <  {need} = 6 - alpha.  Coupled branch DEAD.")
