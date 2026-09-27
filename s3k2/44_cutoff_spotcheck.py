#!/usr/bin/env python3
"""
Spot-check of script 41's CUTOFF against the complete-information terminal test.

The pool cross-check (script 42) cannot test the cutoff.  The cutoff only ever
removes LARGE primes (thresholds run from thousands to millions), and a
brute-force pool contains only small ones.  This check targets it directly.

  1. Run script 41's DFS on a profile, recording states (K, lb, left, W, B) at
     which the cutoff fires: the smallest unknown is claimed to be < B.
  2. For recorded states whose unknown roles are all notable ('n'), which impose
     no forced primes, build complete sets T = K u {t_1 < ... < t_u}, with the
     t_i random primes = 1 (mod 3) in [B, 3B].
  3. Every such T must die under the terminal test of script 41, which has
     complete information.

The cutoff lemma says every T whose smallest unknown is >= B is impossible, so a
survivor would expose an unsound threshold.  Under a mutation that lowers
thresholds, the samples fall into the gap between the mutated and the true B,
and this check fails.

Run:  python3 44_cutoff_spotcheck.py <profile> [samples per state]
"""
import sys, os, random, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "41_rebuild_dfs.py"))
rb = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(rb); sys.argv = _a

_orig = rb.threshold

def rand_primes1(lo, hi, k, avoid):
    out = set(); tries = 0
    while len(out) < k and tries < 100000:
        t = random.randrange(lo, hi); tries += 1
        if t % 3 == 1 and t not in avoid and rb.isprime(t): out.add(t)
    return sorted(out)

if __name__ == "__main__":
    name = sys.argv[1]; S = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    random.seed(12345)
    roles, Wrole, alpha = rb.PROFILES[name]
    states = []
    # record each cutoff state by reading the calling dfs frame's locals
    import inspect
    def thr(K, base, u):
        fr = inspect.currentframe().f_back
        lb, left, wc = fr.f_locals['lb'], fr.f_locals['left'], fr.f_locals['wc']
        B = _orig(K, base, u)
        if B is not None and all(r == 'n' for r in left):
            states.append((dict(K), lb, tuple(left), wc, B))
        return B
    rb.threshold = thr
    rb.run_profile(name, log=lambda *a: None)
    print(f"{name}: {len(states)} cutoff states with notable-only unknowns recorded")
    tested = survived = 0; bad = []
    random.shuffle(states)
    for K, lb, left, wc, B in states[:400]:
        for _ in range(S):
            ts = rand_primes1(B, 3*B, len(left), set(K))
            if len(ts) < len(left): continue
            T = dict(K); T.update({t: 'n' for t in ts})
            if rb.forced_set(T, wc): continue          # closure already kills it
            excl = tuple(q for q in rb.SMALLQ if q not in T)
            b = rb.bounds(T, wc, excl, 2 - alpha - wc[2])
            if b is None: continue
            lo, hi = b
            tested += 1
            if lo > rb.TARGET: continue
            o = rb.Out(); rb.terminal(T, wc, alpha, lo, hi, o)
            if o.alive or o.cond:
                survived += 1; bad.append((sorted(T), wc[0], B))
    print(f"   sampled complete T above the threshold: {tested};  surviving the terminal test: {survived}")
    for x in bad[:10]: print("      SURVIVOR", x)
    print("   PASS" if tested and not survived else ("   FAIL" if survived else "   NO SAMPLES"))
