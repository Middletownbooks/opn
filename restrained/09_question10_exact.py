#!/usr/bin/env python3
"""
Ochem-Zelinsky's Question 10, settled EXACTLY for all pairs (p, r) below a bound.

Question 10: are there primes x, y, p, r and integers a > b > 0 with
        x^2 + x + 1 = p^a r,      y^2 + y + 1 = p^b r ?
NOTES_RESTRAINED.md section 4 shows p = 1 (mod 3), p >= 7, and records a null search over
primes x <= 10^6 (all p, r).  That covers every (p, r) but bounded x.

This script covers the other axis: for each FIXED pair (p, r), the equation
        x^2 + x + 1 = r * p^c      (c >= 0 free)
has one free exponent, so s3k2/32's Skolem solver lists ALL its solutions, for
every c, with no bound on x.  A pair answers Question 10 exactly when two of those
solutions have positive prime x, y and exponents a > b >= 1.

r ranges over 3 and the primes = 1 (mod 3), since every prime factor of
t^2+t+1 is one of those; r = p is included.  Pairs for which the solver cannot
settle every residue class are reported as UNSETTLED and claimed nothing about.

VALIDATION.  Ochem-Zelinsky's two near-examples (composite x) must appear:
  (p, r) = (7, 19):    30^2+30+1   = 7^2 * 19,    11^2+11+1   = 7 * 19;
  (p, r) = (409, 523): 9353^2+9353+1 = 409^2 * 523, 462^2+462+1 = 409 * 523.

Run:  python3 09_question10_exact.py <PMAX>      (pairs with p, r < PMAX)
"""
import importlib.util, os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sk", os.path.join(here, "..", "s3k2", "32_skolem.py"))
sk = importlib.util.module_from_spec(spec); spec.loader.exec_module(sk)

def all_solutions(p, r):
    """all (c, x) with x^2+x+1 = r p^c, c >= 0, x >= 0; or None if unsettled."""
    if r != p:
        sols, status = sk.solve([r], p)
        if sols is None: return None
        return sorted({(c, x) for c, x in sols if x >= 0})
    # r = p: the equation is x^2+x+1 = p^(c+1), a single-prime equation; solve it
    # as such and shift the exponent (solution p^C gives c = C - 1).
    sols, status = sk.solve([], p)
    if sols is None: return None
    return sorted({(C - 1, x) for C, x in sols if x >= 0 and C >= 1})

def q10_hits(p, r, sols):
    """pairs (a, x), (b, y) with a > b >= 1; returns (all, prime-only)."""
    pos = [(c, x) for c, x in sols if c >= 1 and x >= 2]
    allp = [((a, x), (b, y)) for a, x in pos for b, y in pos if a > b]
    prim = [h for h in allp if sk.isprime(h[0][1]) and sk.isprime(h[1][1])]
    return allp, prim

if __name__ == "__main__":
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print("VALIDATION: Ochem-Zelinsky's near-examples")
    for p, r, want in [(7, 19, ((2, 30), (1, 11))), (409, 523, ((2, 9353), (1, 462)))]:
        s = all_solutions(p, r)
        allp, prim = q10_hits(p, r, s)
        print(f"   (p, r) = ({p}, {r}): solutions {s};  a > b pairs {allp}")
        assert want in allp, "near-example NOT reproduced"
    print("   both reproduced.\n")

    ps = [q for q in range(7, PMAX) if q % 3 == 1 and sk.isprime(q)]
    rs = [3] + ps
    print(f"ALL PAIRS p in {len(ps)} primes = 1 mod 3 below {PMAX}, r in {len(rs)} (3 and those primes)", flush=True)
    t0 = time.time(); unsettled = []; composite_hits = []; prime_hits = []; n = 0
    for p in ps:
        for r in rs:
            s = all_solutions(p, r); n += 1
            if s is None: unsettled.append((p, r)); continue
            allp, prim = q10_hits(p, r, s)
            if allp: composite_hits.append((p, r, allp))
            if prim: prime_hits.append((p, r, prim))
        print(f"   p = {p:>4} done  ({n} pairs, {time.time()-t0:.0f}s)", flush=True)
    print()
    print(f"pairs settled exactly: {n - len(unsettled)} of {n};  UNSETTLED: {unsettled}")
    print(f"pairs with a > b solutions (any x, y): {len(composite_hits)}")
    for h in composite_hits: print("      ", h)
    print(f"Question-10 solutions (x, y prime): {prime_hits}")
