#!/usr/bin/env python3
"""
Soundness cross-check for script 41's pruning, against brute force.

The audit (finding X1) pointed out that an over-pruning bug can never produce an
ALIVE set, so it is invisible to tallies.  This check makes it visible.

For a profile and a pool of small primes, enumerate EVERY T (13 in T, |T| = tau,
all elements from the pool), EVERY role assignment and EVERY W configuration of
script 41.  Apply only the complete-information terminal test: forced primes
inside T, raw minimum, two-sided abundancy, count.  Every configuration that
SURVIVES the abundancy tests (conditional on the count, or alive) must appear
among script 41's conditional items for the same (T, W).

41's DFS kills configurations earlier: pinning, the raw minimum, the cutoff
lemma, and pinned-exponent admissibility.  Each of these kills only
configurations that the terminal test also kills.  So a survivor MISSING from 41's
list would expose unsound pruning.

Run:  python3 42_pool_crosscheck.py <profile> <pool bound>
"""
import sys, os, itertools, importlib.util, time
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "41_rebuild_dfs.py"))
rb = importlib.util.module_from_spec(spec); sys.argv, _a = ['x'], sys.argv; spec.loader.exec_module(rb); sys.argv = _a

def assignments(T, roles):
    seen = set()
    for perm in itertools.permutations(roles):
        if perm in seen: continue
        seen.add(perm)
        yield dict(zip(T, perm))

def pool_survivors(name, P):
    roles, Wrole, alpha = rb.PROFILES[name]; tau = len(roles)
    pool = [q for q in range(7, P) if q % 3 == 1 and rb.isprime(q) and q != 13]
    surv = set(); n = 0
    wcs = rb.w_configs(Wrole, alpha)
    for rest in itertools.combinations(pool, tau - 1):
        T = tuple(sorted(rest + (13,)))
        for K in assignments(T, roles):
            if any(not rb.role_ok(t, r) for t, r in K.items()): continue
            for wc in wcs:
                n += 1
                if rb.forced_set(K, wc): continue                     # forced prime outside T
                excl = tuple(q for q in rb.SMALLQ if q not in K)
                b = rb.bounds(K, wc, excl, 2 - alpha - wc[2])
                if b is None: continue
                lo, hi = b
                if lo > rb.TARGET: continue
                out = rb.Out()
                rb.terminal(K, wc, alpha, lo, hi, out)
                if out.cond or out.alive: surv.add((T, wc[0]))
    return surv, n

if __name__ == "__main__":
    name, P = sys.argv[1], int(sys.argv[2])
    t0 = time.time()
    surv, n = pool_survivors(name, P)
    print(f"{name}, pool < {P}: {n} configurations by brute force, {len(surv)} survive the abundancy tests "
          f"({time.time()-t0:.0f}s)")
    out = rb.run_profile(name, log=lambda *a: None)
    dfs_items = {(c[1], c[2]) for c in out.cond if c[0] == 'SmT'} | {(tuple(sorted(a[0])), a[1]) for a in out.alive}
    missing = sorted(s for s in surv if s not in dfs_items)
    print(f"   script 41 conditional/alive items: {sorted(dfs_items)}")
    print(f"   brute-force survivors:             {sorted(surv)}")
    print(f"   survivors MISSING from script 41:  {missing}")
    print("   PASS" if not missing else "   FAIL: script 41 pruned a configuration the terminal test cannot kill")
