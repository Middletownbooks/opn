#!/usr/bin/env python3
"""
An independent rebuild of the section-3 profile search (scripts 34/35/36/38).

Written from the SPECIFICATION (NOTES_S3_K2.md sections 1-2 and 5, and the
audit's proofs audit_s3k2/AUDIT_S3K2_RESULT.md Pf.1-Pf.5), not from the code of
36.  The architecture is deliberately different.

  * ONE depth-first search over ROLE-ASSIGNED partial sets, from the seeds to
    the leaves.  Script 36 recursed over SETS and took min/max over role
    assignments.
  * Closure PINNING at every level.  36 used it only at the last level, and 38
    only for exceptions.
  * The cutoff is the audit's lemma (Pf.2), evaluated directly:
        (18/13) / (H0(K) * HI(K))  >=  corr_u(B, K)
    in Decimal arithmetic with outward rounding.  The per-term factor is
    c_B = (1 + 1/(sqrt(B)-1))^2, proved below, instead of 1.01.
  * Stronger valid filters.
      - Forced primes of p+1 at EVERY odd exponent, for a special prime in T or
        in W.
      - Exponent admissibility against every prime = 1 (mod 3) below lb, not
        only below min T.
      - Exponents are never declared impossible because of a search cap; there
        is a lower-bound fallback instead.
  * WB = 1000 (36 used 500).
  * Every conditional item is DISCHARGED at the end by the AUDITOR's solver,
    audit_s3k2/a4_solver.py, not by s3k2/39.

What must agree with 36/38 is the VERDICT (nothing alive; every conditional item
settled), not internal counts.

SPECIFICATION
  Components: 3^2 (ordinary), the special p^e (p = e = 1 mod 4), two notables
  n^q (q even >= 4), and ordinaries x^2.
  T = primes = 1 (mod 3) dividing N;  W = big components = 2 (mod 3);
  U = ordinary primes = 2 (mod 3).
  prod_{C != 3^2} sigma(C)/C = 18/13  (sigma(3^2)/3^2 = 13/9).
  omega(N) = 4 + alpha + |U| >= 10, so |U| >= 6 - alpha.
  Role factor of t in T: 'o' exactly f(t) = 1 + 1/t + 1/t^2;
    's' (t = 1 mod 12, e = 1 mod 4) in [sigma(t^e0)/t^e0, t/(t-1));
    'n' (q even >= 4) in [sigma(t^q0)/t^q0, t/(t-1)).
  3-budget: alpha + sum over T-bigs of v3(k+1) + [special in W](v3(w+1) + v3(e+1)) = 2.
    Used as <=, each term separately; a relaxation.
  Necessary conditions ("pinning"): every prime = 1 (mod 3) dividing
    sigma(t^2) (t ordinary), t+1 (t special in T), or w+1 (w special in W)
    lies in T.
  Admissibility: sigma(t^k) has no prime factor = 1 (mod 3) that is known NOT
    to lie in T.

TAIL AND NEW-MEMBER BOUND (proved here).  For x in U, M = x^2+x+1 is T-smooth
and 3 does not divide M.  log f(x) <= 1/x + 1/x^2 and M^(-1/2) >= 1/(x+1), so
log f(x) <= (1+1/x)^2 M^(-1/2) <= (1 + 1/(sqrt(M0)-1))^2 M^(-1/2) whenever
M >= M0 (because x >= sqrt(M) - 1).  Distinct x give distinct M.  Hence:
  * members with M > Y:  sum log f <= c_Y * Y^(-eps) prod_t (1 - t^(eps-1/2))^(-1)
    (Rankin);
  * members new in T = K u R (R the unknowns, all >= B): M has an R-factor, so
    M >= B and sum log f <= c_B * E(K) * ((1 - B^(-1/2))^(-u) - 1),
    with E(K) = prod_{t in K} (1 - t^(-1/2))^(-1).
Every R-factor is < B/(B-1) in any role.  So T (smallest unknown >= B) is
impossible if  (18/13) / (H0(K) * HI(K))  >=  (B/(B-1))^u exp(c_B E(K) ((1-B^(-1/2))^(-u) - 1)),
where H0(K) = prod f(x) over x in Sm_Y(K) \ {w} with f(x) <= (18/13)/LO_raw(K),
times the tail factor.  The cap uses only LO_raw(K), which is valid for every
superset.

Run:  python3 41_rebuild_dfs.py <profile>      e.g. 1,yes,1,3,1   or   all
"""
import sys, math, os, time, bisect
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
getcontext().prec = 60
TARGET = F(18, 13); Y = 10**24; WB = 1000
SLACK = D(1) + D(10) ** -40            # relative outward rounding

# ------------------------------------------------------------ arithmetic
def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n % p == 0: return n == p
    d = n-1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
def _rho(n):
    if n % 2 == 0: return 2
    c = 1
    while True:
        x = y = 2; d = 1
        g = lambda v: (v*v + c) % n
        while d == 1:
            x = g(x); y = g(g(y)); d = math.gcd(abs(x-y), n)
        if d != n: return d
        c += 1
_fc = {}
def factor(n):
    """prime factorisation (set of primes) of n >= 1."""
    if n in _fc: return _fc[n]
    out = set(); m = n
    for p in range(2, 1000):
        if m % p == 0:
            out.add(p)
            while m % p == 0: m //= p
    stack = [m] if m > 1 else []
    while stack:
        a = stack.pop()
        if a == 1: continue
        if isprime(a): out.add(a); continue
        d = _rho(a); stack += [d, a//d]
    _fc[n] = frozenset(out); return _fc[n]
def P1(n): return frozenset(p for p in factor(n) if p % 3 == 1)
def v3(n):
    k = 0
    while n % 3 == 0: n //= 3; k += 1
    return k
def sig(t, k): return (t**(k+1) - 1)//(t - 1)
def f(x): return F(x*x + x + 1, x*x)

SMALLQ = [q for q in range(7, 1000) if q % 3 == 1 and isprime(q)]
_P1 = []
def primes1_between(lo, hi):
    """primes = 1 mod 3 in (lo, hi), via a growing sieve."""
    global _P1
    if not _P1 or _P1[-1] < hi:
        n = int(max(hi, 1000)) + 2
        s = bytearray([1])*(n+1); s[0] = s[1] = 0
        for i in range(2, math.isqrt(n)+1):
            if s[i]: s[i*i::i] = bytearray(len(range(i*i, n+1, i)))
        _P1 = [p for p in range(7, n+1) if s[p] and p % 3 == 1]
    return _P1[bisect.bisect_right(_P1, lo):bisect.bisect_left(_P1, hi)]

# ------------------------------------------------------------ admissibility, minima
def excluded(K, lb):
    """primes = 1 mod 3 known NOT to lie in T: those <= lb and not in K."""
    return tuple(q for q in SMALLQ if q <= lb and q not in K)
def admissible(t, k, excl):
    for q in excl:
        if q == t: continue
        if t % q == 1:
            if (k+1) % q == 0: return False
        elif (pow(t, k+1, q) - 1) % q == 0: return False
    return True
_rm = {}
def role_min(t, role, excl, rem):
    """least factor sigma(t^k)/t^k over admissible k for the role; None only
       when the role is structurally impossible.  Exponents are searched up to
       200; beyond that the fallback is a valid lower bound, because
       sigma(t^k)/t^k increases with k."""
    key = (t, role, excl, rem)
    if key in _rm: return _rm[key]
    r = None
    if role == 'o':
        r = f(t)
    elif role == 's':
        if t % 12 == 1:
            for e in range(1, 200, 4):
                if v3(e+1) <= rem and admissible(t, e, excl): r = F(sig(t, e), t**e); break
            else: r = F(sig(t, 201), t**201)
    else:
        for q in range(4, 200, 2):
            if v3(q+1) <= rem and admissible(t, q, excl): r = F(sig(t, q), t**q); break
        else: r = F(sig(t, 200), t**200)
    _rm[key] = r; return r
def role_hi(t, role): return f(t) if role == 'o' else F(t, t-1)

# ------------------------------------------------------------ W configurations
def w_configs(Wrole, alpha):
    """(label, w or None, cost, forced, LOW(excl), HIW, e1)"""
    if Wrole is None: return [("W empty", None, 0, frozenset(), lambda ex: F(1), F(1))]
    out = []; ws = [w for w in range(5, WB) if w % 3 == 2 and isprime(w)]
    if Wrole == 'n':
        for w in ws:
            def low(ex, w=w):
                for q in range(4, 200, 2):
                    if admissible(w, q, ex): return F(sig(w, q), w**q)
                return F(sig(w, 200), w**200)
            out.append((f"n={w}", w, 0, frozenset(), low, F(w, w-1)))
        out.append((f"n>={WB}", None, 0, frozenset(), lambda ex: F(1), F(WB, WB-1)))
    else:
        for w in ws:
            if w % 12 != 5: continue
            c = v3(w+1)
            if alpha + c > 2: continue
            forced = P1(w+1)                      # w+1 | sigma(w^e) for every odd e
            out.append((f"s={w},e=1", w, c, forced, lambda ex, w=w: F(w+1, w), F(w+1, w)))
            def low5(ex, w=w, c=c):
                for e in range(5, 200, 4):
                    if alpha + c + v3(e+1) <= 2 and admissible(w, e, ex): return F(sig(w, e), w**e)
                return F(sig(w, 201), w**201)
            out.append((f"s={w},e>=5", w, c, forced, low5, F(w, w-1)))
        out.append((f"s>={WB}", None, 1, frozenset(), lambda ex: F(1), F(WB, WB-1)))
    return out

# ------------------------------------------------------------ smooth numbers, tail
_sm = {}
def Sm_Y(K):
    """primes x = 2 mod 3, x >= 5, with x^2+x+1 K-smooth and <= Y."""
    K = tuple(sorted(K))
    if K in _sm: return _sm[K]
    out = []
    def rec(i, m):
        if i == len(K):
            d = 4*m - 3; r = math.isqrt(d)
            if r*r == d:
                x = (r-1)//2
                if x >= 5 and x % 3 == 2 and isprime(x): out.append(x)
            return
        v = m
        while v <= Y: rec(i+1, v); v *= K[i]
    rec(0, 1); _sm[K] = sorted(set(out)); return _sm[K]
_tl = {}
def tail_factor(K):
    """upper bound for prod f(x) over x with K-smooth x^2+x+1 > Y (Decimal)."""
    K = tuple(sorted(K))
    if K in _tl: return _tl[K]
    Yd = D(Y); best = None
    for j in range(1, 50):
        eps = D(j)/100
        v = Yd ** (-eps)
        for t in K: v /= (1 - D(t) ** (eps - D(1)/2))
        best = v if best is None or v < best else best
    cY = (1 + 1/(Yd.sqrt() - 1))**2
    _tl[K] = (cY*best*SLACK).exp()*SLACK
    return _tl[K]
def E_of(K):
    e = D(1)
    for t in K: e /= (1 - D(t) ** D(-0.5))
    return e*SLACK
def corr(B, K, u):
    Bd = D(B); sB = Bd.sqrt()
    cB = (1 + 1/(sB - 1))**2
    val = (Bd/(Bd-1))**u * (cB*E_of(K)*((1 - 1/sB)**(-u) - 1)).exp()
    return val*SLACK

# ------------------------------------------------------------ bounds for a state
def bounds(K, wc, excl, rem):
    """(LO_raw, HI) as Fractions, or None if some role is impossible."""
    lo = wc[4](excl); hi = wc[5]
    for t, r in K.items():
        m = role_min(t, r, excl, rem)
        if m is None: return None
        lo *= m; hi *= role_hi(t, r)
    return lo, hi
def H0(K, lo, w):
    cap = TARGET/lo; h = F(1)
    for x in Sm_Y(K):
        if x != w and f(x) <= cap: h *= f(x)
    return D(h.numerator)/D(h.denominator)*SLACK * tail_factor(K)
def Dfrac(q): return D(q.numerator)/D(q.denominator)

def threshold(K, base, u):
    """least integer B >= 3 with corr(B) <= base, or None."""
    if corr(10**12, K, u) > base: return None
    lo, hi = 3, 10**12
    if corr(lo, K, u) <= base: return lo
    while hi - lo > 1:
        mid = (lo + hi)//2
        if corr(mid, K, u) <= base: hi = mid
        else: lo = mid
    assert corr(hi, K, u) <= base
    return hi

# ------------------------------------------------------------ the search
class Out:
    def __init__(s):
        s.dead = {}; s.cond = []; s.unres = []; s.alive = []; s.states = 0
    def kill(s, why): s.dead[why] = s.dead.get(why, 0) + 1

def forced_set(K, wc):
    N = set(wc[3])
    for t, r in K.items():
        if r == 'o': N |= P1(t*t + t + 1)
        elif r == 's': N |= P1(t + 1)
    return {x for x in N if x not in K}

def role_ok(t, r):
    return not (r == 's' and t % 12 != 1)

def dfs(K, lb, left, wc, alpha, out, final_excl_all=True):
    out.states += 1
    N = forced_set(K, wc)
    if any(x <= lb for x in N): out.kill('closure: forced prime not in T'); return
    if len(N) > len(left): out.kill('closure: too many forced primes'); return
    rem = 2 - alpha - wc[2]
    excl = excluded(K, lb) if left else tuple(q for q in SMALLQ if q not in K)
    b = bounds(K, wc, excl, rem)
    if b is None: out.kill('impossible role'); return
    lo, hi = b
    if lo > TARGET: out.kill('raw minimum > 18/13'); return
    if not left: return terminal(K, wc, alpha, lo, hi, out)
    if N:
        x = min(N)
        for r in set(left):
            if role_ok(x, r):
                l2 = list(left); l2.remove(r)
                dfs({**K, x: r}, lb, tuple(l2), wc, alpha, out)
        return
    h0 = H0(K, lo, wc[1])
    base = D(TARGET.numerator)/D(TARGET.denominator)/(h0*Dfrac(hi)*SLACK)
    u = len(left)
    B = threshold(K, base, u) if base > 1 else None
    if B is not None and B <= 5*10**8:
        for t in primes1_between(lb, B):
            if t in K: continue
            for r in set(left):
                if role_ok(t, r):
                    l2 = list(left); l2.remove(r)
                    dfs({**K, t: r}, t, tuple(l2), wc, alpha, out)
        return
    # no cutoff: only ordinary unknowns can be handled
    if all(r == 'o' for r in left) and u in (1, 2):
        EXP = 300 if len(K) <= 2 else (120 if len(K) == 3 else 60)
        out.cond.append(('caseB', tuple(sorted(K)), wc[0], EXP))
        for t in caseB(tuple(sorted(K)), EXP):
            if t > lb and t not in K:
                l2 = list(left); l2.remove('o')
                dfs({**K, t: 'o'}, lb, tuple(l2), wc, alpha, out)
        if u == 2:
            # coupled pair: each unknown divides the other's x^2+x+1.  e_a = 2
            # for an ordinary a, and the partner's sigma spends one unit, so U
            # uses a (and a') at most once: |U| <= 2 + #(admissible Sm(K)).
            adm = [x for x in Sm_Y(K) if x != wc[1] and f(x) <= TARGET/lo]
            if len(adm) + 2 < 6 - alpha:
                out.kill('coupled pair: count'); out.cond.append(('SmK-coupled', tuple(sorted(K)), wc[0], len(adm)))
            else:
                out.unres.append(('coupled', dict(K), lb, left, wc[0]))
        return
    out.unres.append(('no cutoff', dict(K), lb, left, wc[0], float(base)))

_cb = {}
def caseB(K, EXP):
    """primes t = 1 mod 3 with (t^2+t+1)/3 K-smooth and <= 10^EXP."""
    key = (K, EXP)
    if key in _cb: return _cb[key]
    lim = 10**EXP; out = []
    def rec(i, m):
        if i == len(K):
            d = 12*m - 3; r = math.isqrt(d)
            if r*r == d:
                t = (r-1)//2
                if t % 3 == 1 and isprime(t): out.append(t)
            return
        v = m
        while v <= lim: rec(i+1, v); v *= K[i]
    rec(0, 1); _cb[key] = sorted(set(out)); return _cb[key]

def terminal(T, wc, alpha, lo, hi, out):
    Tk = tuple(sorted(T)); w = wc[1]
    h = H0(T, lo, w)                              # every x in U has f(x) <= 18/13/lo
    lo_n = max(Dfrac(lo), D(TARGET.numerator)/D(TARGET.denominator)/h)
    if lo_n >= Dfrac(hi): out.kill('final: two-sided abundancy'); return
    cap = D(TARGET.numerator)/D(TARGET.denominator)/lo_n
    adm = sorted((x for x in Sm_Y(Tk) if x != w and Dfrac(f(x)) <= cap), reverse=True)
    need = 6 - alpha
    if len(adm) < need:
        out.kill('final: count (Sm complete)'); out.cond.append(('SmT', Tk, wc[0], tuple(adm))); return
    pr = F(1)
    for x in adm[:need]: pr *= f(x)                 # the need smallest factors
    if Dfrac(pr) > cap:
        out.kill('final: count product (Sm complete)'); out.cond.append(('SmT', Tk, wc[0], tuple(adm))); return
    out.alive.append((dict(T), wc[0], adm))

PROFILES = {   # T roles, W role, alpha   (NOTES_S3_K2.md 13c)
    "0,no,2,2,1":  (('n','n'), 's', 0),
    "0,yes,1,2,1": (('s','n'), 'n', 0),
    "0,yes,2,3,0": (('s','n','n'), None, 0),
    "1,no,2,3,1":  (('o','n','n'), 's', 1),
    "1,yes,1,3,1": (('o','s','n'), 'n', 1),
    "1,yes,2,4,0": (('o','s','n','n'), None, 1),
    "2,yes,1,4,1": (('o','o','s','n'), 'n', 2),
    "2,yes,2,5,0": (('o','o','s','n','n'), None, 2),
}

def run_profile(name, log=print):
    roles, Wrole, alpha = PROFILES[name]; out = Out(); t0 = time.time()
    for wc in w_configs(Wrole, alpha):
        # seeds: min T is 7 or 13 (13 is in T; no prime = 1 mod 3 lies between 7 and 13)
        rs = set(roles)
        for r7 in rs:
            for r13 in rs:
                l = list(roles); l.remove(r7)
                if r13 not in l: continue
                l.remove(r13)
                if role_ok(7, r7) and role_ok(13, r13):
                    dfs({7: r7, 13: r13}, 13, tuple(l), wc, alpha, out)
        for r13 in rs:
            l = list(roles); l.remove(r13)
            if role_ok(13, r13):
                dfs({13: r13}, 13, tuple(l), wc, alpha, out)
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
    names = list(PROFILES) if sys.argv[1] == "all" else sys.argv[1:]
    for n in names: run_profile(n)
