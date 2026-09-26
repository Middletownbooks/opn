#!/usr/bin/env python3
"""
Resolve the exceptions of script 36: sets S one prime short of T (k = 1) whose
margin is <= 1, so the cutoff gives no finite bound on the last prime t.

The method of section 9a, made general.  Split on the role rho taken by t; S
then carries the sub-profile FULL - {rho}.
  (1) REFINED MARGIN.  Recompute LO/HI (with narrowing) over that one
      sub-profile only.  If it is > 1, the one-prime cutoff (k = 1) gives a
      finite B, and every t < B is tested in full.
  (2) CASE A.  rho != 'o' and an ordinary s in S: closure puts F(s) inside T, so
      t in F(s) \\ S.  A finite explicit list, provided F(s) \\ S is non-empty for
      every admissible choice of s (otherwise the branch is reported unresolved).
  (3) CASE B.  rho = 'o': F(t) inside S, i.e. (t^2+t+1)/3 is S-smooth
      (v_3 = 1 for t = 1 mod 3).  Enumerated by running over S-smooth M up to
      MB and testing whether 12M - 3 is an odd square.  CONDITIONAL on the bound MB
      (a Thue-Mahler statement of rank |S|); tallied separately.
Every candidate T = S u {t} gets script 36's full final test (all role
assignments, not only rho).  That test is weaker than one restricted to rho,
and so still valid.

Run:  python3 37_resolve_exceptions.py <profile-name>
"""
import sys, math
from fractions import Fraction as F
sys_argv = sys.argv[:]
sys.argv = ['x', 'none']
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "36_profile_recursion.py")).read().split('if __name__ == "__main__":')[0])
sys.argv = sys_argv

MB_EXP = {2: 300, 3: 120, 4: 60}      # Case-B search bound 10^MB_EXP[|S|]

def final_test(T, FULL, wc, alpha):
    need = 6 - alpha
    LO, HI, keep = margin(T, FULL, wc, alpha)
    if LO is None: return 'nocfg'
    if LO >= HI or LO > TARGET: return 'uncond'
    R = TARGET/LO; pr = F(1)
    for x in keep[-need:]: pr *= geom(x, 2)
    if len(keep) < need or pr > R: return 'cond'
    return 'alive'

def margin_pr(S, pr, FULL, wc, alpha):
    """margin() restricted to the single sub-profile pr of S."""
    label, w, low, HIW, cost, forced = wc
    MIN = S[0]; tau = len(FULL)
    if forced and not forced_ok(S, forced, tau): return None, None
    LOW = low(MIN)
    if LOW is None: return None, None
    lo, hi = bounds(S, pr, MIN, 2 - alpha - cost, tau)
    if lo is None: return None, None
    LO = lo*LOW; HI = hi*HIW
    Sm = [x for x in smooth_x(S) if x != w]
    etb = math.exp(1.000001*tailY(S))
    for _ in range(60):
        R = TARGET/LO; H = F(1)
        for x in Sm:
            if geom(x, 2) <= R: H *= geom(x, 2)
        Hup = F(math.ceil(float(H)*etb*10**12) + 1, 10**12)
        nl = TARGET/Hup
        if nl <= LO: break
        LO = nl
    return LO, HI

def ordinary_choices(S, pr, MIN, b3, tau):
    """for each admissible assignment of pr to S: the set of ordinary primes."""
    out = set()
    for perm in set(permutations(range(len(S)))):
        ords = []; ok = True
        for r, i in zip(pr, perm):
            if min_factor(S[i], r, MIN, b3) is None: ok = False; break
            if r == 'o': ords.append(S[i])
        if ok and closure_ok(S, ords, tau): out.add(tuple(sorted(ords)))
    return out

def caseB(S, exp10):
    MB = 10**exp10; out = []; L = list(S)
    def rec(i, m):
        if i == len(L):
            d = 12*m - 3; r = math.isqrt(d)
            if r*r == d and r % 2 == 1:
                t = (r-1)//2
                if t > S[-1] and t % 3 == 1 and isprime(t): out.append(t)
            return
        v = m
        while v <= MB: rec(i+1, v); v *= L[i]
    rec(0, 1); return sorted(set(out))

def resolve(name):
    FULL, Wrole, alpha = PROFILES[name]; tau = len(FULL)
    configs = {wc[0]: wc for wc in w_configs(Wrole, alpha)}
    r = run(FULL, Wrole, alpha, verbose=False)
    print(f"PROFILE {name}: {len(r['exceptions'])} exceptions from script 36")
    tally = dict(nocfg=0, uncond=0, cond=0, alive=0)
    condB = []; unresolved = []
    for exc in r['exceptions']:
        S, wl = exc[0], exc[1]; wc = configs[wl]
        if tau - len(S) != 1 or not isinstance(exc[2], float):
            unresolved.append((S, wl, "k > 1 or huge B")); continue
        MIN = S[0]; b3 = 2 - alpha - wc[4]
        print(f"   S = {list(S)}  W: {wl}   (margin {exc[2]:.6f})")
        for rho in sorted(set(FULL)):
            pr = list(FULL); pr.remove(rho); pr = tuple(sorted(pr))
            LO, HI = margin_pr(S, pr, FULL, wc, alpha)
            if LO is None:
                print(f"      t {rho}: no admissible assignment of {pr} to S -> dead"); continue
            m = float(LO)/float(HI)
            if m > 1:
                B = threshold_k(S, m, 1)
                cands = [t for t in primes1_upto(B) if t > S[-1]]
                how = f"refined margin {m:.6f} > 1, B = {B:.1f}"
            elif rho != 'o':
                chs = ordinary_choices(S, pr, MIN, b3, tau)
                cands = set(); bad = False
                for ords in chs:
                    need_t = set()
                    for s in ords: need_t |= {f for f in Fset(s) if f not in S}
                    if not need_t: bad = True
                    cands |= need_t
                if bad or not chs and 'o' in pr:
                    unresolved.append((S, wl, rho)); print(f"      t {rho}: UNRESOLVED"); continue
                if 'o' not in pr:
                    unresolved.append((S, wl, rho)); print(f"      t {rho}: UNRESOLVED (no ordinary in S)"); continue
                cands = sorted(t for t in cands if t > S[-1])
                how = f"case A: t in F(ordinary) \\ S"
            else:
                e = MB_EXP[len(S)]
                cands = caseB(S, e)
                how = f"case B: (t^2+t+1)/3 {list(S)}-smooth, searched to 10^{e}"
                condB.append((S, wl, e, cands))
            res = {}
            for t in cands:
                v = final_test(tuple(sorted(S + (t,))), FULL, wc, alpha)
                res[v] = res.get(v, 0) + 1
                if v == 'alive': print(f"         ALIVE: {sorted(S+(t,))}")
                if v == 'cond': print(f"         conditional: {sorted(S+(t,))}")
                tally[v] += 1
            print(f"      t {rho}: {how}; {len(cands)} candidates -> {res}")
    print(f"   TOTAL over candidates: {tally}")
    print(f"   unresolved branches: {unresolved}")
    print(f"   case-B search bounds used: {[(list(S), wl, '10^%d' % e) for S, wl, e, _ in condB]}")
    return tally, unresolved, condB

if __name__ == "__main__":
    resolve(sys.argv[1])
