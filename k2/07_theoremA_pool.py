#!/usr/bin/env python3
"""
Brute-force cross-check of Theorem A's search (k2/05) against the terminal test.

For every T drawn from the primes = 1 (mod 3) below a pool bound (T = special,
plus 0, 1 or 2 notables), every W configuration, and every role assignment, apply
the complete-information terminal test of k2/05: forced primes inside T, raw
minimum, two-sided abundancy, count.  Report every configuration that SURVIVES
the abundancy tests.  k2/05 found none, so none may survive here.
Run:  python3 07_theoremA_pool.py <pool bound>
"""
import sys, os, itertools, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ta", os.path.join(here, "05_theoremA_dfs.py"))
ta = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(ta); sys.argv = _a
P = int(sys.argv[1]) if len(sys.argv) > 1 else 200
pool = [q for q in range(7, P) if q % 3 == 1 and ta.isprime(q)]
total = surv = 0
for name, (roles, nW) in ta.PROFILES.items():
    wcs = ta.w_configs(nW); n = s = 0
    for T in itertools.combinations(pool, len(roles)):
        for perm in set(itertools.permutations(roles)):
            K = dict(zip(T, perm))
            if any(r == 's' and t % 12 != 1 for t, r in K.items()): continue
            if ta.forced_src(K): continue
            ex = tuple(q for q in ta.SMALLQ if q not in K)
            for wc in wcs:
                n += 1
                b = ta.bounds(K, wc, ex)
                if b is None: continue
                lo, hi = b
                if lo > ta.TARGET: continue
                o = ta.Out(); ta.terminal(K, wc, lo, hi, None, o)
                if o.alive or o.cond: s += 1; print("   SURVIVOR", name, K, wc[0])
    print(f"profile {name}: {n} configurations, pool < {P}: {s} survive the abundancy tests")
    total += n; surv += s
print("PASS" if surv == 0 else "FAIL")
