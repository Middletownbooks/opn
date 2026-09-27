#!/usr/bin/env python3
"""
Theorem A (k = 2, 3 does not divide N): the profile search, with certificates.

A rebuild of NOTES_K2.md / AUDIT_K2_MODEL_RESULT.md using the Theorem-B machinery
of s3k2/41, so that Theorem A no longer rests on the reasoning model's
fixed-support argument or on Bennett-Levin.  Its certificates are checked by
k2/06_check_theoremA.py.

SPECIFICATION (derived here).  N odd perfect, 3 does not divide N, exactly two
notables (even exponent >= 4), a special p^e (p = e = 1 mod 4), and ordinary
components x^2.
  * An ordinary prime s = 1 (mod 3) gives 3 | s^2+s+1 | 2N, which is impossible.
    So every ordinary prime is = 2 (mod 3): these form U.
  * No component may contribute a 3:
      special p = 2 (mod 3): e+1 is even and 3 | p+1, so 3 | sigma(p^e), which is
        impossible.  So the special is = 1 (mod 3), hence = 1 (mod 12), and
        3 does not divide e+1;
      notable n = 1 (mod 3): v3(sigma(n^q)) = v3(q+1) = 0;
      notable n = 2 (mod 3) with q even: sigma = 1 (mod 3), no constraint.
  * T = primes = 1 (mod 3) dividing N = the special plus the notables = 1 (mod 3);
    W = the notables = 2 (mod 3).  Profiles: T roles 's' (|W| = 2), 'sn' (|W| = 1),
    'snn' (|W| = 0).
  * prod over all components of sigma(C)/C = 2.
  * U is inside Sm(T) = {x prime = 2 mod 3 : x^2+x+1 is T-smooth}.
    omega(N) = 3 + |U|, and Nielsen 2007 (omega >= 12 when 3 does not divide N)
    gives |U| >= 9.  This is used only by the count kill, and is reported
    separately.
  * Forced: every prime = 1 (mod 3) dividing p+1 (special, e odd) lies in T.
  * Admissible exponent k: sigma(t^k) has no prime factor = 1 (mod 3) known not
    to lie in T.
The search starts from K = {} with lb = 6, so the smallest element of T is
enumerated under the cutoff, like every other.

Run:  python3 05_theoremA_dfs.py [s|sn|snn|all]
      python3 05_theoremA_dfs.py --cert <profile>     (proof tree to stdout)
"""
import sys, os, time, json, importlib.util
from fractions import Fraction as F
from decimal import Decimal as D
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "..", "s3k2", "41_rebuild_dfs.py"))
rb = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(rb); sys.argv = _a
isprime, P1, sig, f, v3 = rb.isprime, rb.P1, rb.sig, rb.f, rb.v3
SMALLQ, Sm_Y, tail_factor, corr, Dfrac = rb.SMALLQ, rb.Sm_Y, rb.tail_factor, rb.corr, rb.Dfrac
TARGET = F(2); WB = 1000; SLACK = rb.SLACK
NEED_U = 9                                      # Nielsen 2007

def admissible(t, k, excl):
    return rb.admissible(t, k, excl)
def role_min(t, role, excl):
    if role == 's':
        if t % 12 != 1: return None
        for e in range(1, 200, 4):
            if (e + 1) % 3 != 0 and admissible(t, e, excl): return F(sig(t, e), t**e)
        return F(sig(t, 201), t**201)
    for q in range(4, 200, 2):
        if (q + 1) % 3 != 0 and admissible(t, q, excl): return F(sig(t, q), t**q)
    return F(sig(t, 200), t**200)
def role_hi(t): return F(t, t - 1)

def w_low(w, excl):
    for q in range(4, 200, 2):
        if admissible(w, q, excl): return F(sig(w, q), w**q)
    return F(sig(w, 200), w**200)
WS = [w for w in range(5, WB) if w % 3 == 2 and isprime(w)]
def w_configs(nW):
    """(label, explicit ws, LOW(excl), HIW)"""
    if nW == 0: return [("W empty", (), lambda ex: F(1), F(1))]
    if nW == 1:
        out = [(f"n={w}", (w,), lambda ex, w=w: w_low(w, ex), F(w, w - 1)) for w in WS]
        out.append((f"n>={WB}", (), lambda ex: F(1), F(WB, WB - 1)))
        return out
    out = []
    for i, w1 in enumerate(WS):
        for w2 in WS[i+1:]:
            out.append((f"n={w1}+n={w2}", (w1, w2), lambda ex, a=w1, b=w2: w_low(a, ex)*w_low(b, ex), F(w1, w1-1)*F(w2, w2-1)))
        out.append((f"n={w1}+n>={WB}", (w1,), lambda ex, a=w1: w_low(a, ex), F(w1, w1-1)*F(WB, WB-1)))
    out.append((f"n>={WB}+n>={WB}", (), lambda ex: F(1), F(WB, WB-1)**2))
    return out

CERT = None
def emit(K, lb, left, wc, **a):
    if CERT is None: return
    CERT.write(json.dumps({"K": sorted([t, r] for t, r in K.items()), "lb": lb,
                           "left": sorted(left), "w": wc[0], **a}) + "\n")

class Out:
    def __init__(s): s.dead = {}; s.cond = []; s.unres = []; s.alive = []; s.states = 0
    def kill(s, why): s.dead[why] = s.dead.get(why, 0) + 1

def forced_src(K):
    N = {}
    for t in sorted(K):
        if K[t] == 's':
            for x in sorted(P1(t + 1)): N.setdefault(x, (t, 's'))
    return {x: v for x, v in N.items() if x not in K}

def bounds(K, wc, excl):
    lo = wc[2](excl); hi = wc[3]
    for t, r in K.items():
        m = role_min(t, r, excl)
        if m is None: return None
        lo *= m; hi *= role_hi(t)
    return lo, hi
def H0(K, lo, ws):
    cap = TARGET / lo; h = F(1)
    for x in Sm_Y(K):
        if x not in ws and f(x) <= cap: h *= f(x)
    return Dfrac(h) * SLACK * tail_factor(K)

def dfs(K, lb, left, wc, out):
    out.states += 1
    NS = forced_src(K); N = set(NS)
    low = sorted(x for x in N if x <= lb)
    if low:
        x = low[0]; emit(K, lb, left, wc, a="dead", why="closure1", f=x, src=NS[x][0], kind='s')
        out.kill('closure'); return
    if len(N) > len(left):
        emit(K, lb, left, wc, a="dead", why="closure2", fs=[[x, NS[x][0], 's'] for x in sorted(N)])
        out.kill('closure'); return
    excl = tuple(q for q in SMALLQ if q not in K and (q <= lb or not left))
    b = bounds(K, wc, excl)
    if b is None: emit(K, lb, left, wc, a="dead", why="impossible"); out.kill('impossible'); return
    lo, hi = b
    if lo > TARGET: emit(K, lb, left, wc, a="dead", why="raw"); out.kill('raw'); return
    if not left: return terminal(K, wc, lo, hi, lb, out)
    if N:
        x = min(N); emit(K, lb, left, wc, a="pin", f=x, src=NS[x][0], kind='s')
        for r in sorted(set(left)):
            if not (r == 's' and x % 12 != 1):
                l2 = list(left); l2.remove(r); dfs({**K, x: r}, lb, tuple(l2), wc, out)
        return
    base = D(2) / (H0(K, lo, wc[1]) * Dfrac(hi) * SLACK)
    B = rb.threshold(K, base, len(left)) if base > 1 else None
    if B is None or B > 5 * 10**8:
        emit(K, lb, left, wc, a="unresolved"); out.unres.append((dict(K), lb, left, wc[0])); return
    emit(K, lb, left, wc, a="cut", B=B)
    for t in rb.primes1_between(lb, B):
        if t in K: continue
        for r in sorted(set(left)):
            if not (r == 's' and t % 12 != 1):
                l2 = list(left); l2.remove(r); dfs({**K, t: r}, t, tuple(l2), wc, out)

def terminal(T, wc, lo, hi, lb, out):
    ws = wc[1]; h = H0(T, lo, ws)
    lo_n = max(Dfrac(lo), D(2) / h)
    if lo_n >= Dfrac(hi):
        emit(T, lb, (), wc, a="dead", why="final-abund"); out.kill('final: two-sided abundancy'); return
    cap = D(2) / lo_n
    adm = sorted((x for x in Sm_Y(tuple(sorted(T))) if x not in ws and Dfrac(f(x)) <= cap), reverse=True)
    if len(adm) < NEED_U:
        emit(T, lb, (), wc, a="dead", why="final-count")
        out.kill('final: count'); out.cond.append(('SmT', tuple(sorted(T)), wc[0], tuple(adm))); return
    pr = F(1)
    for x in adm[:NEED_U]: pr *= f(x)
    if Dfrac(pr) > cap:
        emit(T, lb, (), wc, a="dead", why="final-count")
        out.kill('final: count'); out.cond.append(('SmT', tuple(sorted(T)), wc[0], tuple(adm))); return
    emit(T, lb, (), wc, a="alive"); out.alive.append((dict(T), wc[0], adm))

PROFILES = {"s": (('s',), 2), "sn": (('n', 's'), 1), "snn": (('n', 'n', 's'), 0)}

def run_profile(name, log=print):
    roles, nW = PROFILES[name]; out = Out(); t0 = time.time()
    for wc in w_configs(nW):
        dfs({}, 6, tuple(sorted(roles)), wc, out)
    log(f"PROFILE {name}: {out.states} states, {time.time()-t0:.0f}s")
    for k in sorted(out.dead): log(f"   dead, {k}: {out.dead[k]}")
    log(f"   conditional items: {len(out.cond)}")
    for c in sorted(set(out.cond)): log(f"      {c}")
    log(f"   UNRESOLVED: {len(out.unres)}")
    for u in out.unres[:20]: log(f"      {u}")
    log(f"   ALIVE: {len(out.alive)}")
    for a in out.alive[:20]: log(f"      {a}")
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--cert":
        CERT = sys.stdout; name = args[1]
        CERT.write(json.dumps({"profile": name}) + "\n")
        run_profile(name, log=lambda *a: None)
        CERT.write(json.dumps({"end": name}) + "\n"); sys.exit(0)
    names = list(PROFILES) if (not args or args[0] == "all") else args
    for n in names: run_profile(n)
