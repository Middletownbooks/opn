#!/usr/bin/env python3
"""
D2: which of s3k2/36's exceptions on profile 2,yes,1,4,1 arise at levels 1-2?
Replays run()'s logic (same order of tests: None, raw-minimum kill, 13-rule,
plain cutoff) for levels 1 and 2 only (tau = 4, so the closure-driven last level
is level 3 and is NOT replayed here).  Imports 36 unchanged.
"""
import os, sys
S3 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "s3k2")
sys.argv = ['x', 'none']
exec(open(os.path.join(S3, "36_profile_recursion.py")).read().split('if __name__ == "__main__":')[0])
FULL, Wrole, alpha = PROFILES["2,yes,1,4,1"]; tau = len(FULL)
exc = []; lvl3 = 0
for wc in w_configs(Wrole, alpha):
    live = [(7,), (13,)]
    for L in (1, 2):
        nxt = []
        for S in live:
            LO, HI, keep = margin(S, FULL, wc, alpha)
            if LO is None: continue
            m = float(LO) / float(HI)
            if RAW[(S, wc[0])] > TARGET: continue
            if 13 not in S:
                if S[-1] < 13: nxt.append(tuple(sorted(S + (13,))))
                continue
            B = threshold_k(S, m, tau - L)
            if B == float('inf') or B > 5e8:
                exc.append((S, wc[0], L, round(m, 6))); continue
            for t in primes1_upto(B):
                if t > S[-1]: nxt.append(tuple(sorted(S + (t,))))
        live = sorted(set(nxt))
    lvl3 += len(live)
print("run() exceptions at levels 1-2:", exc)
print("level-3 sets (all W configs):", lvl3)
