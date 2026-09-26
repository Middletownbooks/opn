#!/usr/bin/env python3
"""
The max(T) recursion for an ARBITRARY role profile of section 3 at k = 2,
including a single W slot.  Aim: remove the pool from the seven "limited"
profiles of section 13c.

PROFILE.  T carries the role multiset  'o' * alpha + 's' * [sp in T] + 'n' * nt,
tau = |T|, and W (|W| <= 1 for every limited profile) is either empty, a notable
w = 2 (mod 3) ('n'), or the special w = 5 (mod 12) ('s').  The identity is

        PROD_T * PROD_W * PROD_U = 18/13,     |U| >= 6 - alpha  (omega >= 10).

W CONFIGURATIONS.  The W prime is independent of the T-recursion, so it is
enumerated as a configuration:
  * explicit prime w < WB, w = 2 (mod 3):
        notable : factor in [sigma(w^q0)/w^q0, w/(w-1)), q0 the least admissible q;
        special : w = 5 (mod 12); split e = 1 (factor (w+1)/w EXACTLY, and every
                  prime = 1 (mod 3) of w+1 must lie in T) and e >= 5;
  * generic w >= WB: factor in (1, WB/(WB-1)).
  w is removed from Sm(T) (it is not ordinary).

3-BUDGET.  e_3 = 2: alpha ordinary primes = 1 (mod 3) spend alpha; a special in
W spends v_3(w+1) + v_3(e+1) >= 1; T-bigs spend v_3(k+1).  Role minima allow
every exponent with v_3(k+1) <= 2 - alpha - cost(W).  That is a relaxation of the
true constraint, and relaxing only LOWERS the minima, so LO stays a valid lower
bound.

RECURSION.  As in script 34 (k-prime cutoff), per W configuration:
    S = the |S| smallest elements of T, k = tau - |S| primes remain above max(S);
    margin(S) = LO/HI after interval narrowing, both including the W factor;
    T dies if max(S) < (|S|+1)-th element and that element >= B_k(S);
    at |S| = tau: the unconditional two-sided test, then the conditional count.
A configuration with margin <= 1 below the top level is an EXCEPTION (an
infinite family this test cannot kill); it is reported, never dropped.

VALIDATION.  With profile (o,o,s,n,n), W empty, this must reproduce script 34's
level counts exactly: 59, 1372, 31925, 488860, and its three exceptions.
Run:  python3 36_profile_recursion.py validate
      python3 36_profile_recursion.py <profile-name>
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math, sys, time, bisect

Y = 10**24; TARGET = F(18, 13); WB = 500

def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
def geom(t, k): return F(sum(t**i for i in range(k+1)), t**k)
def sig(t, k): return sum(t**i for i in range(k+1))
def v3(n):
    k = 0
    while n % 3 == 0: n //= 3; k += 1
    return k
def _fac(n):
    f = set(); d = 2
    while d*d <= n and d < 10**8:
        while n % d == 0: f.add(d); n //= d
        d += 1 if d == 2 else 2
    if n > 1: f.add(n)
    return f
_Fc = {}
def Fset(t):
    if t not in _Fc: _Fc[t] = frozenset(p for p in _fac(t*t+t+1) if p % 3 == 1)
    return _Fc[t]
SMALL1 = [p for p in range(7, 2000) if p % 3 == 1 and isprime(p)]

def admissible(t, k, MIN):
    """sigma(t^k) has no prime factor = 1 (mod 3) below MIN (other than t)."""
    v = sig(t, k)
    for q in SMALL1:
        if q >= MIN: break
        if q != t and v % q == 0: return False
    return True
_mf = {}
def min_factor(t, role, MIN, b3):
    key = (t, role, MIN, b3)
    if key in _mf: return _mf[key]
    r = None
    if role == 'o':
        r = geom(t, 2) if admissible(t, 2, MIN) else None
    elif role == 's':
        if t % 12 == 1:
            for k in range(1, 120, 4):
                if v3(k+1) > b3: continue
                if admissible(t, k, MIN): r = geom(t, k); break
    else:
        for k in range(4, 120, 2):
            if v3(k+1) > b3: continue
            if admissible(t, k, MIN): r = geom(t, k); break
    _mf[key] = r; return r

def closure_ok(S, ords, size):
    Ss = set(S); mx = max(S); extra = set()
    for t in ords:
        for f in Fset(t):
            if f in Ss: continue
            if f < mx: return False
            extra.add(f)
    return len(extra) <= size - len(S)

def forced_ok(S, forced, size):
    """every prime in `forced` (all = 1 mod 3) must lie in T."""
    Ss = set(S); mx = max(S); extra = set()
    for f in forced:
        if f in Ss: continue
        if f < mx: return False
        extra.add(f)
    return len(extra) <= size - len(S)

def bounds(S, roles, MIN, b3, size):
    lo = hi = None
    for perm in set(permutations(range(len(S)))):
        l = F(1); h = F(1); ok = True; ords = []
        for r, i in zip(roles, perm):
            t = S[i]; f = min_factor(t, r, MIN, b3)
            if f is None: ok = False; break
            if r == 'o': ords.append(t)
            l *= f; h *= (geom(t, 2) if r == 'o' else F(t, t-1))
        if not ok or not closure_ok(S, ords, size): continue
        if lo is None or l < lo: lo = l
        if hi is None or h > hi: hi = h
    return lo, hi

_sm = {}
def smooth_x(T):
    if T in _sm: return _sm[T]
    out = []; L = list(T)
    def rec(i, m):
        if i == len(L):
            d = 4*m - 3; r = math.isqrt(d)
            if r*r == d and r % 2 == 1:
                x = (r-1)//2
                if x >= 5 and x % 3 == 2 and isprime(x): out.append(x)
            return
        v = m
        while v <= Y: rec(i+1, v); v *= L[i]
    rec(0, 1); _sm[T] = sorted(set(out)); return _sm[T]
def tailY(T):
    best = None; lnY = math.log(Y)
    for k in range(1, 100):
        eps = 0.5*k/100.0
        v = -eps*lnY
        for t in T: v -= math.log(1.0 - t**(eps-0.5))
        if best is None or v < best: best = v
    return math.exp(best)/(1 - Y**-0.5)
def euler(T):
    e = 1.0
    for t in T: e /= (1.0 - t**-0.5)
    return e
def corrk(B, S, k):
    u = B**-0.5
    return (B/(B-1.0))**k * math.exp(1.01*(1+1/(math.sqrt(B)-1))*((1-u)**-k - 1)*euler(S))
def threshold_k(S, m, k):
    if m is None or m <= 1.0: return float('inf')
    lo, hi = 2.0, 1e30
    if corrk(hi, S, k) > m: return float('inf')
    while hi/lo > 1.0001:
        mid = math.sqrt(lo*hi)
        if corrk(mid, S, k) <= m: hi = mid
        else: lo = mid
    return hi

# ------------------------------------------------------------ W configurations
def w_configs(Wrole, alpha):
    """list of (label, w or None, LOW-function(MIN) -> Fraction|None, HIW, cost3, forced)"""
    out = []
    if Wrole is None:
        return [("W empty", None, lambda MIN: F(1), F(1), 0, ())]
    ws = [w for w in range(5, WB) if w % 3 == 2 and isprime(w)]
    if Wrole == 'n':
        for w in ws:
            def low(MIN, w=w):
                for q in range(4, 200, 2):
                    if admissible(w, q, MIN): return geom(w, q)
                return None
            out.append((f"n={w}", w, low, F(w, w-1), 0, ()))
        out.append((f"n>={WB}", None, lambda MIN: F(1), F(WB, WB-1), 0, ()))
    else:  # special in W, w = 5 (mod 12)
        for w in ws:
            if w % 12 != 5: continue
            c = v3(w+1)
            if alpha + c > 2: continue
            forced = tuple(sorted(p for p in _fac(w+1) if p % 3 == 1))
            out.append((f"s={w},e=1", w, lambda MIN, w=w: F(w+1, w), F(w+1, w), c, forced))
            def low5(MIN, w=w, c=c):
                for e in range(5, 200, 4):
                    if alpha + c + v3(e+1) > 2: continue
                    if admissible(w, e, MIN): return geom(w, e)
                return None
            out.append((f"s={w},e>=5", w, low5, F(w, w-1), c, ()))
        out.append((f"s>={WB}", None, lambda MIN: F(1), F(WB, WB-1), 1, ()))
    return out

# ------------------------------------------------------------ margin
def subprofiles(FULL, L): return sorted({tuple(sorted(c)) for c in combinations(FULL, L)})

RAW = {}
def margin(S, FULL, wc, alpha):
    label, w, low, HIW, cost, forced = wc
    MIN = S[0]; tau = len(FULL)
    if forced and not forced_ok(S, forced, tau): return None, None, None
    LOW = low(MIN)
    if LOW is None: return None, None, None
    b3 = 2 - alpha - cost
    los = []; his = []
    for pr in subprofiles(FULL, len(S)):
        lo, hi = bounds(S, pr, MIN, b3, tau)
        if lo is None: continue
        los.append(lo); his.append(hi)
    if not los: return None, None, None
    LO = min(los)*LOW; HI = max(his)*HIW
    RAW[(S, label)] = LO        # role minimum before narrowing: valid for every T containing S
    Sm = [x for x in smooth_x(S) if x != w]
    etb = math.exp(1.000001*tailY(S)); keep = Sm
    for _ in range(60):
        R = TARGET/LO; H = F(1); keep = []
        for x in Sm:
            if geom(x, 2) <= R: H *= geom(x, 2); keep.append(x)
        Hup = F(math.ceil(float(H)*etb*10**12) + 1, 10**12)
        nl = TARGET/Hup
        if nl <= LO: break
        LO = nl
    return LO, HI, keep

# ------------------------------------------------------------ primes
_P = []; _PMAX = [0]
def primes1_upto(B):
    if B > _PMAX[0]:
        n = int(B) + 1; s = bytearray([1])*(n+1); s[0] = s[1] = 0
        for i in range(2, math.isqrt(n)+1):
            if s[i]: s[i*i::i] = bytearray(len(range(i*i, n+1, i)))
        _P[:] = [p for p in range(7, n+1) if s[p] and p % 3 == 1]; _PMAX[0] = n
    return _P[:bisect.bisect_left(_P, B)]


# ------------------------------------------------------------ closure-driven last level
MB_EXP = {1: 600, 2: 300, 3: 120, 4: 60}   # case-B search bound 10^MB_EXP[|S|]

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
    if LO > TARGET: return None, None      # raw role minimum already exceeds 18/13
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

_cB = {}
def caseB(S, exp10):
    """primes t > max(S), t = 1 (mod 3), with (t^2+t+1)/3 S-smooth and <= 10^exp10."""
    key = (S, exp10)
    if key in _cB: return _cB[key]
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
    rec(0, 1); _cB[key] = sorted(set(out)); return _cB[key]

def last_candidates(S, FULL, wc, alpha):
    """All t > max(S) such that T = S u {t} can satisfy closure, split on t's role.
       Returns (candidates, caseB_used, exceptions).  See section 14e."""
    tau = len(FULL); MIN = S[0]; b3 = 2 - alpha - wc[4]
    cands = set(); usedB = False; exc = []
    for rho in sorted(set(FULL)):
        pr = list(FULL); pr.remove(rho); pr = tuple(sorted(pr))
        free = False; freeB = False
        for perm in set(permutations(range(len(S)))):
            ords = []; ok = True
            for r, i in zip(pr, perm):
                if min_factor(S[i], r, MIN, b3) is None: ok = False; break
                if r == 'o': ords.append(S[i])
            if not ok or not closure_ok(S, ords, tau): continue
            need = set()
            for s0 in ords: need |= {f for f in Fset(s0) if f not in S}
            if len(need) > 1: continue
            if need:
                t = next(iter(need))
                if rho == 'o' and not (Fset(t) <= set(S)): continue
                cands.add(t)
            elif rho == 'o':
                freeB = True
            else:
                free = True
        if freeB:
            # t ordinary, F(t) inside S.  With a finite cutoff B for this role split,
            # t < B gives (t^2+t+1)/3 < B^2, so the S-smooth enumeration to B^2 is
            # EXACT.  Only a margin <= 1 falls back to the conditional search bound.
            LO, HI = margin_pr(S, pr, FULL, wc, alpha)
            if LO is not None:
                B = threshold_k(S, float(LO)/float(HI), 1)
                if B < 1e150:
                    cands |= set(caseB(S, 2*int(math.log10(B)) + 2))
                else:
                    cands |= set(caseB(S, MB_EXP[len(S)])); usedB = True
        if free:
            LO, HI = margin_pr(S, pr, FULL, wc, alpha)
            if LO is None: continue
            m = float(LO)/float(HI)
            B = threshold_k(S, m, 1)
            if B == float('inf') or B > 5e8:
                exc.append((S, wc[0], 't:'+rho, m)); continue
            cands |= {t for t in primes1_upto(B) if t > S[-1]}
    return sorted(t for t in cands if t > S[-1]), usedB, exc

# ------------------------------------------------------------ one profile
def run(FULL, Wrole, alpha, verbose=True, levels_out=None, closure_last=True):
    tau = len(FULL); need = 6 - alpha
    res = dict(uncond=0, cond=0, nocfg=0, rawdead=0, alive=[], cond_sets=[], exceptions=[], levels={}, caseB=[])
    for wc in w_configs(Wrole, alpha):
        live = [(7,), (13,)]
        for L in range(1, tau+1):
            nxt = []
            for S in live:
                LO, HI, keep = margin(S, FULL, wc, alpha)
                if LO is None:
                    if L == tau: res['nocfg'] += 1
                    continue
                m = float(LO)/float(HI)
                if RAW[(S, wc[0])] > TARGET:
                    # role minima of S alone exceed 18/13; they only grow with T and
                    # PROD_U >= 1, so every T containing S is dead (no narrowing used)
                    res['rawdead'] += 1; continue
                if L == tau:
                    if LO >= HI or LO > TARGET: res['uncond'] += 1; continue
                    R = TARGET/LO
                    pr = F(1)
                    for x in keep[-need:]: pr *= geom(x, 2)
                    if len(keep) < need or pr > R:
                        res['cond'] += 1; res['cond_sets'].append((S, wc[0])); continue
                    res['alive'].append((S, wc[0], keep)); continue
                if 13 not in S:
                    # 13 is in T and nothing = 1 (mod 3) lies strictly between 7 and 13,
                    # so the next element is 13 itself: no cutoff is needed.
                    if S[-1] < 13: nxt.append(tuple(sorted(S + (13,))))
                    continue
                if closure_last and alpha >= 1 and L == tau - 1:
                    cands, usedB, exc = last_candidates(S, FULL, wc, alpha)
                    Bf = threshold_k(S, m, 1)           # the plain cutoff still applies
                    res['exceptions'] += exc
                    if usedB: res['caseB'].append((S, wc[0]))
                    for t in cands:
                        if t < Bf: nxt.append(tuple(sorted(S + (t,))))
                    continue
                B = threshold_k(S, m, tau - L)
                if B == float('inf'):
                    res['exceptions'].append((S, wc[0], m)); continue
                if B > 5e8:
                    res['exceptions'].append((S, wc[0], f"B={B:.3g} too large")); continue
                for t in primes1_upto(B):
                    if t > S[-1] and ((13 in S) or t == 13):
                        nxt.append(tuple(sorted(S + (t,))))
            live = sorted(set(nxt))
            if verbose and len(live) > 20000:
                print(f"      {wc[0]}: level {L+1} has {len(live)} sets "
                      f"(max prime {max(x[-1] for x in live)})", flush=True)
            if L+1 <= tau:
                res['levels'].setdefault(L+1, 0); res['levels'][L+1] += len(live)
            if not live: break
        if verbose: print(f"   {wc[0]:14s} done; running totals uncond {res['uncond']} "
                          f"cond {res['cond']} exc {len(res['exceptions'])} alive {len(res['alive'])}",
                          flush=True)
    return res

PROFILES = {
    # name: (T roles, W role, alpha)       rows of section 13c
    "1,no,2,3,1":  (('o','n','n'),      's', 1),
    "1,yes,1,3,1": (('o','s','n'),      'n', 1),
    "1,yes,2,4,0": (('o','s','n','n'),  None, 1),
    "2,yes,1,4,1": (('o','o','s','n'),  'n', 2),
    "0,no,2,2,1":  (('n','n'),          's', 0),
    "0,yes,1,2,1": (('s','n'),          'n', 0),
    "0,yes,2,3,0": (('s','n','n'),      None, 0),
    # the alpha = 2, |W| = 0 branch of sections 8-10, for validating the final test
    "2,yes,2,5,0": (('o','o','s','n','n'), None, 2),
}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if arg == "validate":
        print("VALIDATION: profile (o,o,s,n,n), W empty, recursion levels 2..4 vs script 34")
        FULL = ('o','o','s','n','n')
        wc = w_configs(None, 2)[0]
        live = [(7,), (13,)]; counts = []; exc = []
        for L in range(1, 5):
            nxt = []
            for S in live:
                LO, HI, keep = margin(S, FULL, wc, 2)
                if LO is None: continue
                m = float(LO)/float(HI)
                B = threshold_k(S, m, 5 - L)
                if B == float('inf'): exc.append((S, round(m, 6))); continue
                for t in primes1_upto(B):
                    if t > S[-1] and ((13 in S) or t == 13): nxt.append(tuple(sorted(S+(t,))))
            live = sorted(set(nxt)); counts.append(len(live))
        print("   level counts :", counts, "  expected [59, 1372, 31925, 488860]")
        print("   exceptions   :", exc)
        assert counts == [59, 1372, 31925, 488860], "does NOT reproduce script 34"
        assert [list(s) for s, _ in exc] == [[7,13,19,31], [7,13,31,79], [7,13,31,307]]
        print("   reproduced exactly.")
        sys.exit(0)
    FULL, Wrole, alpha = PROFILES[arg]
    t0 = time.time()
    print(f"PROFILE {arg}: T roles {FULL}, W {Wrole}, alpha {alpha}, need |U| >= {6-alpha}", flush=True)
    r = run(FULL, Wrole, alpha)
    print(f"   level counts (summed over W configs): {r['levels']}")
    print(f"   killed early (raw role minimum > 18/13): {r['rawdead']}")
    print(f"   final sets: uncond dead {r['uncond']}, conditional dead {r['cond']}, "
          f"no role/config {r['nocfg']}, ALIVE {len(r['alive'])}")
    print(f"   exceptions (no cutoff): {len(r['exceptions'])}")
    for e in r['exceptions'][:40]: print("      ", e)
    for a in r['alive'][:40]: print("   ALIVE", a)
    print(f"   case-B enumerations (conditional on 10^MB_EXP bound): {len(r['caseB'])}")
    for c in r['caseB'][:30]: print("      ", c)
    print(f"   conditional sets: {len(r['cond_sets'])}")
    for c in r['cond_sets'][:60]: print("      ", c)
    print(f"   time {time.time()-t0:.0f}s")
