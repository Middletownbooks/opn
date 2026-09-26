#!/usr/bin/env python3
"""
Closure propagation for exceptions with SEVERAL primes still missing.

Script 36 reports an exception when a set S (the |S| smallest elements of T)
has margin <= 1, so no cutoff bounds the next prime.  Script 36's closure-driven
last level handles one missing prime.  This script handles any number, by a
depth-first search over PARTIAL ROLE ASSIGNMENTS:

  state  K = {t: role} (known T-primes with roles), `left` = roles of the unknown
         T-primes, all of which are distinct primes > lb.
  (1) PINNING.  For ordinary t in K, F(t) \\ K must consist of unknowns.  If some
      such f <= lb, or there are more such f than unknowns: dead.  Otherwise
      pick one f and branch on its role (f is an unknown; lb is unchanged).
  (2) CUTOFF.  Nothing pinned: compute LO/HI for K with its EXACT roles (after
      narrowing), and B = B_u(K) from the u-prime lemma of script 34
      (u = #unknowns).  If B is finite, the SMALLEST unknown is < B: enumerate it
      and set lb to it.
  (3) CASE B.  Margin <= 1 and every unknown ordinary:
        u = 1: F(t) inside K, so (t^2+t+1)/3 is K-smooth; searched to 10^MB.
        u = 2: either some unknown has F inside K (as u = 1), or each divides
               the other's x^2+x+1, which by section 14a (Vieta jumping) makes
               them consecutive terms of 1,1,3,13,61,291,...; searched to index NSEQ.
      Conditional on those bounds, and tallied separately.
  (4) anything else: UNRESOLVED, reported, never dropped.
  (5) u = 0: the final test with the exact roles (two-sided narrowing, then the
      count |U| >= 6 - alpha, which is conditional).

Run:  python3 38_closure_dfs.py <profile-name>
It re-runs script 36 on the profile and sends every exception here.
"""
import sys, math, os
from fractions import Fraction as F
_argv = sys.argv[:]; sys.argv = ['x', 'none']
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "36_profile_recursion.py")).read().split('if __name__ == "__main__":')[0])
sys.argv = _argv

NSEQ = 1500
SEQ = [1, 1]
while len(SEQ) < NSEQ: SEQ.append(5*SEQ[-1] - SEQ[-2] - 1)

def role_ok(t, r, MIN, b3):
    return min_factor(t, r, MIN, b3) is not None

def lohi_roles(K, wc, alpha):
    label, w, low, HIW, cost, forced = wc
    Ks = tuple(sorted(K)); MIN = Ks[0]; b3 = 2 - alpha - cost
    LOW = low(MIN)
    if LOW is None: return None, None, None
    lo = LOW; hi = HIW
    for t, r in K.items():
        f = min_factor(t, r, MIN, b3)
        if f is None: return None, None, None
        lo *= f; hi *= (geom(t, 2) if r == 'o' else F(t, t-1))
    if lo > TARGET: return None, None, None     # raw role minimum > 18/13: dead for all T >= K
    Sm = [x for x in smooth_x(Ks) if x != w]
    etb = math.exp(1.000001*tailY(Ks)); LO = lo; keep = Sm
    for _ in range(60):
        R = TARGET/LO; H = F(1); keep = []
        for x in Sm:
            if geom(x, 2) <= R: H *= geom(x, 2); keep.append(x)
        Hup = F(math.ceil(float(H)*etb*10**12) + 1, 10**12)
        nl = TARGET/Hup
        if nl <= LO: break
        LO = nl
    return LO, hi, keep

def sub(left, r):
    l = list(left); l.remove(r); return tuple(l)

def dfs(K, lb, left, wc, alpha, out, depth=0):
    Ks = tuple(sorted(K)); MIN = Ks[0]; b3 = 2 - alpha - wc[4]
    if wc[5] and not all(f in K or f > lb for f in wc[5]): return      # W-forced primes
    N = set()
    for t, r in K.items():
        if r == 'o': N |= {f for f in Fset(t) if f not in K}
    if wc[5]: N |= {f for f in wc[5] if f not in K}
    if any(f <= lb for f in N) or len(N) > len(left): return
    if not left:
        LO, HI, keep = lohi_roles(K, wc, alpha)
        if LO is None: out['nocfg'] += 1; return
        if LO >= HI or LO > TARGET: out['uncond'] += 1; return
        need = 6 - alpha; R = TARGET/LO; pr = F(1)
        for x in keep[-need:]: pr *= geom(x, 2)
        if len(keep) < need or pr > R:
            out['cond'] += 1; out['cond_sets'].append((dict(K), wc[0])); return
        out['alive'].append((dict(K), wc[0])); return
    if N:
        f = min(N)
        for r in set(left):
            if role_ok(f, r, MIN, b3): dfs({**K, f: r}, lb, sub(left, r), wc, alpha, out, depth+1)
        return
    LO, HI, keep = lohi_roles(K, wc, alpha)
    if LO is None: return
    u = len(left); m = float(LO)/float(HI)
    B = threshold_k(Ks, m, u)
    if B < 1e150 and all(r == 'o' for r in left) and u == 1:
        # t ordinary with F(t) inside K and t < B: (t^2+t+1)/3 is K-smooth and < B^2,
        # so this enumeration is EXACT (no search bound).
        for t in caseB(Ks, 2*int(math.log10(B)) + 2):
            if t > lb and t not in K and role_ok(t, 'o', MIN, b3):
                dfs({**K, t: 'o'}, t, (), wc, alpha, out, depth+1)
        return
    if B < 5e7:
        for t in primes1_upto(B):
            if t <= lb or t in K: continue
            for r in set(left):
                if role_ok(t, r, MIN, b3): dfs({**K, t: r}, t, sub(left, r), wc, alpha, out, depth+1)
        return
    if all(r == 'o' for r in left) and u in (1, 2):
        e = MB_EXP[min(len(K), 4)]
        out['bounds'].add((Ks, wc[0], f"(t^2+t+1)/3 {list(Ks)}-smooth to 10^{e}"))
        for t in caseB(Ks, e):
            if t > lb and t not in K and role_ok(t, 'o', MIN, b3):
                dfs({**K, t: 'o'}, lb, sub(left, 'o'), wc, alpha, out, depth+1)
        if u == 2:
            out['bounds'].add((Ks, wc[0], f"Vieta pairs to index {NSEQ}"))
            for n in range(2, NSEQ-1):
                a, b = SEQ[n], SEQ[n+1]
                if a <= lb or a in K or b in K: continue
                if a % 3 != 1 or b % 3 != 1 or not isprime(a) or not isprime(b): continue
                if role_ok(a, 'o', MIN, b3) and role_ok(b, 'o', MIN, b3):
                    dfs({**K, a: 'o', b: 'o'}, lb, (), wc, alpha, out, depth+1)
        return
    out['unresolved'].append((dict(K), lb, left, wc[0], round(m, 6)))

def resolve_exception(S, wl, FULL, wc, alpha, out):
    """start the DFS from every admissible role assignment of S."""
    MIN = S[0]; b3 = 2 - alpha - wc[4]
    for pr in subprofiles(FULL, len(S)):
        left = list(FULL)
        for r in pr: left.remove(r)
        for perm in set(permutations(range(len(S)))):
            K = {}; ok = True
            for r, i in zip(pr, perm):
                if not role_ok(S[i], r, MIN, b3): ok = False; break
                K[S[i]] = r
            if ok: dfs(K, S[-1], tuple(sorted(left)), wc, alpha, out)

def exceptions_upto(FULL, Wrole, alpha, Lmax):
    """script 36's recursion (plain cutoff) through level Lmax; its exceptions."""
    tau = len(FULL); exc = []
    for wc in w_configs(Wrole, alpha):
        live = [(7,), (13,)]
        for L in range(1, Lmax+1):
            nxt = []
            for S in live:
                LO, HI, keep = margin(S, FULL, wc, alpha)
                if LO is None: continue
                if 13 not in S:
                    if S[-1] < 13: nxt.append(tuple(sorted(S + (13,))))
                    continue
                B = threshold_k(S, float(LO)/float(HI), tau - L)
                if B == float('inf') or B > 5e8: exc.append((S, wc[0])); continue
                nxt += [tuple(sorted(S + (t,))) for t in primes1_upto(B) if t > S[-1]]
            live = sorted(set(nxt))
    return exc

def main(name, Lmax=None):
    FULL, Wrole, alpha = PROFILES[name]
    cfg = {wc[0]: wc for wc in w_configs(Wrole, alpha)}
    if Lmax is None: Lmax = len(FULL) - 1
    exc = exceptions_upto(FULL, Wrole, alpha, Lmax)
    print(f"PROFILE {name}: {len(exc)} exceptions from script 36's recursion through level {Lmax}")
    for e in exc:
        S, wl = e[0], e[1]
        out = dict(nocfg=0, uncond=0, cond=0, alive=[], cond_sets=[], unresolved=[], bounds=set())
        resolve_exception(S, wl, FULL, cfg[wl], alpha, out)
        print(f"   S = {list(S)}  W {wl}: uncond {out['uncond']}  nocfg {out['nocfg']}  "
              f"cond {out['cond']}  ALIVE {len(out['alive'])}  unresolved {len(out['unresolved'])}")
        for c in out['cond_sets']: print("        conditional:", c)
        for a in out['alive']: print("        ALIVE:", a)
        for u in out['unresolved']: print("        UNRESOLVED:", u)
        for b in sorted(out['bounds']): print("        bound used:", b[2])

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
