#!/usr/bin/env python3
"""
Independent checker for the proof-tree certificates of section 3 at k = 2.

    python3 41_rebuild_dfs.py --cert <profile> | python3 46_check_certificate.py

The certificate is the whole search tree, one JSON line per node in preorder.
This checker trusts NOTHING about how the tree was found.  It shares no code
with the search (s3k2/41).  At every node it

  1. recomputes, from the specification alone, the complete list of children
     that node's case split REQUIRES, and demands exactly those children, so
     the tree is exhaustive;
  2. re-verifies the node's own claim in exact or outward-rounded arithmetic.

Divisibility claims come with witnesses (a forced prime and its source), so
nothing is ever factored.  The only external facts are the complete solution
lists in s3k2/axioms_complete_lists.json, each computed by two independent
solvers (s3k2/45).

SPECIFICATION (NOTES_S3_K2.md sections 1-2; audit_s3k2/AUDIT_S3K2_RESULT.md Pf.1).
  N odd perfect, 3^2 || N, exactly two notables (even exponent >= 4), one special
  p^e (p = e = 1 mod 4), every other component ordinary (exponent 2).
  T = primes = 1 (mod 3) dividing N; W = big components = 2 (mod 3);
  U = ordinary primes = 2 (mod 3).
  prod over C != 3^2 of sigma(C)/C = 18/13, and |U| >= 6 - alpha (Nielsen 2015).
  Role factor of t in T: 'o' exactly f(t) = 1 + 1/t + 1/t^2;
    's' needs t = 1 (mod 12), factor sigma(t^e)/t^e with e = 1 (mod 4), below t/(t-1);
    'n' factor sigma(t^q)/t^q with q even >= 4, below t/(t-1).
  3-budget: each big component's v3(k+1) <= 2 - alpha - cost(W), a relaxation.
  Forced: every prime = 1 (mod 3) dividing t^2+t+1 (t ordinary), t+1 (t special,
    e odd), or w+1 (w special in W) lies in T.
  Admissible exponent k: sigma(t^k) has no prime factor = 1 (mod 3) known not to
    lie in T.
  Tree semantics: every prime of T not in K exceeds lb.  So a prime = 1 (mod 3)
    that is <= lb and not in K is not in T; at a leaf, T = K.

LEMMAS applied (each proved in s3k2/41's docstring and in the audit's Pf.2).
  new-member bound: log f(x) <= (1 + 1/(sqrt(M0) - 1))^2 M^(-1/2) whenever M >= M0;
  Rankin tail for M > Y;
  cutoff: if (18/13)/(H0(K)*HI(K)) >= corr_u(B, K), no T has its smallest unknown >= B.
"""
import sys, os, json, math, bisect
from fractions import Fraction as Fr
from decimal import Decimal as Dm, getcontext
getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
TGT = Fr(18, 13); YB = 10**24; WBND = 1000
UP = Dm(1) + Dm(10) ** -40; DOWN = Dm(1) - Dm(10) ** -40

# ------------------------------------------------------------------ basic arithmetic
def prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        y = pow(a, d, n)
        if y in (1, n - 1): continue
        for _ in range(s - 1):
            y = y * y % n
            if y == n - 1: break
        else: return False
    return True
def v3(n):
    c = 0
    while n % 3 == 0: n //= 3; c += 1
    return c
def sigma_pow(t, k): return (t ** (k + 1) - 1) // (t - 1)
def fval(x): return Fr(x * x + x + 1, x * x)
def dec(q): return Dm(q.numerator) / Dm(q.denominator)
Q1 = [q for q in range(7, 1000) if q % 3 == 1 and prime(q)]

# ------------------------------------------------------------------ profiles and W
PROF = {   # T roles, W role, alpha
    "0,no,2,2,1": ("nn", "s", 0), "0,yes,1,2,1": ("sn", "n", 0), "0,yes,2,3,0": ("snn", None, 0),
    "1,no,2,3,1": ("onn", "s", 1), "1,yes,1,3,1": ("osn", "n", 1), "1,yes,2,4,0": ("osnn", None, 1),
    "2,yes,1,4,1": ("oosn", "n", 2), "2,yes,2,5,0": ("oosnn", None, 2),
}
def admissible(t, k, excl):
    for q in excl:
        if q != t and sigma_pow(t, k) % q == 0: return False
    return True
def least_factor(t, start, step, bound, fallback, ok):
    for k in range(start, bound, step):
        if ok(k): return Fr(sigma_pow(t, k), t ** k)
    return Fr(sigma_pow(t, fallback), t ** fallback)     # valid: sigma(t^k)/t^k increases in k
def wconfigs(Wrole, alpha):
    """label -> dict(w, cost, forced prime set, low(excl), hiw)"""
    if Wrole is None: return {"W empty": dict(w=None, cost=0, forced=set(), low=lambda ex: Fr(1), hiw=Fr(1))}
    out = {}
    for w in range(5, WBND):
        if w % 3 != 2 or not prime(w): continue
        if Wrole == "n":
            out[f"n={w}"] = dict(w=w, cost=0, forced=set(), hiw=Fr(w, w - 1),
                                 low=lambda ex, w=w: least_factor(w, 4, 2, 200, 200, lambda k: admissible(w, k, ex)))
        elif w % 12 == 5 and alpha + v3(w + 1) <= 2:
            c = v3(w + 1)
            fs = {q for q in range(7, w + 2) if q % 3 == 1 and prime(q) and (w + 1) % q == 0}
            out[f"s={w},e=1"] = dict(w=w, cost=c, forced=fs, hiw=Fr(w + 1, w), low=lambda ex, w=w: Fr(w + 1, w))
            out[f"s={w},e>=5"] = dict(w=w, cost=c, forced=fs, hiw=Fr(w, w - 1),
                low=lambda ex, w=w, c=c: least_factor(w, 5, 4, 200, 201,
                                                      lambda k: alpha + c + v3(k + 1) <= 2 and admissible(w, k, ex)))
    gen = f"{Wrole}>={WBND}"
    out[gen] = dict(w=None, cost=(1 if Wrole == "s" else 0), forced=set(), low=lambda ex: Fr(1), hiw=Fr(WBND, WBND - 1))
    return out

# ------------------------------------------------------------------ bounds
def role_low(t, r, excl, rem):
    if r == "o": return fval(t)
    if r == "s":
        return least_factor(t, 1, 4, 200, 201, lambda k: v3(k + 1) <= rem and admissible(t, k, excl))
    return least_factor(t, 4, 2, 200, 200, lambda k: v3(k + 1) <= rem and admissible(t, k, excl))
def role_high(t, r): return fval(t) if r == "o" else Fr(t, t - 1)
def lo_hi(K, wc, excl, rem):
    lo, hi = wc["low"](excl), wc["hiw"]
    for t, r in K.items(): lo *= role_low(t, r, excl, rem); hi *= role_high(t, r)
    return lo, hi
_smc = {}
def smooth_members(K):
    """{x prime, x = 2 mod 3, x >= 5 : x^2+x+1 is K-smooth and <= YB}, by direct enumeration"""
    key = tuple(sorted(K))
    if key in _smc: return _smc[key]
    res = set(); ps = list(key)
    def go(i, m):
        if i == len(ps):
            d = 4 * m - 3; r = math.isqrt(d)
            if r * r == d and (r - 1) // 2 >= 5:
                x = (r - 1) // 2
                if x % 3 == 2 and prime(x): res.add(x)
            return
        while m <= YB: go(i + 1, m); m *= ps[i]
    go(0, 1); _smc[key] = sorted(res); return _smc[key]
def euler(K):
    e = Dm(1)
    for t in K: e /= (1 - Dm(t) ** Dm(-0.5))
    return e * UP
def tail(K):
    best = None
    for j in range(1, 50):
        eps = Dm(j) / 100; v = Dm(YB) ** (-eps)
        for t in K: v /= (1 - Dm(t) ** (eps - Dm(1) / 2))
        best = v if best is None or v < best else best
    cY = (1 + 1 / (Dm(YB).sqrt() - 1)) ** 2
    return (cY * best * UP).exp() * UP
def h0(K, lo, w):
    cap = TGT / lo; p = Fr(1)
    for x in smooth_members(K):
        if x != w and fval(x) <= cap: p *= fval(x)
    return dec(p) * UP * tail(tuple(sorted(K)))
def corr(B, K, u):
    b = Dm(B); sb = b.sqrt(); cB = (1 + 1 / (sb - 1)) ** 2
    return (b / (b - 1)) ** u * (cB * euler(K) * ((1 - 1 / sb) ** (-u) - 1)).exp() * UP

# ------------------------------------------------------------------ axioms
AX = {}
for e in json.load(open(os.path.join(HERE, "axioms_complete_lists.json"))):
    AX[(tuple(e["T"]), e["allow3"])] = e["complete"]
USED = set()
def axiom(K, allow3):
    key = (tuple(sorted(K)), allow3)
    if key not in AX: raise AssertionError(f"no axiom for {key}")
    USED.add(key); return AX[key]

# ------------------------------------------------------------------ primes for cut children
_pl = []
def primes1(lo, hi):
    global _pl
    if not _pl or _pl[-1] < hi:
        n = max(hi, 10**5) + 1; s = bytearray([1]) * (n + 1); s[:2] = b"\0\0"
        for i in range(2, math.isqrt(n) + 1):
            if s[i]: s[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        _pl = [p for p in range(7, n + 1) if s[p] and p % 3 == 1]
    return _pl[bisect.bisect_right(_pl, lo):bisect.bisect_left(_pl, hi)]

# ------------------------------------------------------------------ the check
class Fail(Exception): pass
def need(c, msg):
    if not c: raise Fail(msg)
def key_of(K, lb, left, w): return (tuple(sorted(K.items())), lb, "".join(sorted(left)), w)
def minus(left, r):
    l = list(left); l.remove(r); return "".join(sorted(l))
def role_ok(t, r): return r != "s" or t % 12 == 1
def forced_ok(f, src, kind, K, wc):
    need(prime(f) and f % 3 == 1, f"forced {f} not a prime = 1 mod 3")
    if kind == "o": need(K.get(src) == "o" and (src * src + src + 1) % f == 0, f"{f} not forced by ordinary {src}")
    elif kind == "s": need(K.get(src) == "s" and (src + 1) % f == 0, f"{f} not forced by special {src}")
    elif kind == "w": need(wc["w"] == src and f in wc["forced"] and (src + 1) % f == 0, f"{f} not forced by W={src}")
    else: raise Fail(f"unknown forcing kind {kind}")

STATS = {}
def check(line, it, alpha, WC, expect_key):
    node = json.loads(line)
    K = {t: r for t, r in node["K"]}; lb = node["lb"]; left = "".join(sorted(node["left"])); w = node["w"]
    need(key_of(K, lb, left, w) == expect_key, f"node {key_of(K, lb, left, w)} is not the required child {expect_key}")
    need(all(role_ok(t, r) for t, r in K.items()), "role violates p = 1 mod 12")
    wc = WC[w]; rem = 2 - alpha - wc["cost"]
    excl = tuple(q for q in Q1 if q not in K and (q <= lb or not left))
    a = node["a"]; tag = a if a != "dead" else "dead:" + node["why"]
    STATS[tag] = STATS.get(tag, 0) + 1
    children = []
    if a == "dead":
        why = node["why"]
        if why == "closure1":
            f = node["f"]; forced_ok(f, node["src"], node["kind"], K, wc)
            need(f not in K and f <= lb, "closure1: forced prime is in K or above lb")
        elif why == "closure2":
            fs = node["fs"]; seen = set()
            for f, src, kind in fs:
                forced_ok(f, src, kind, K, wc); need(f not in K and f not in seen, "closure2: repeat or in K"); seen.add(f)
            need(len(seen) > len(left), "closure2: not more forced primes than open slots")
        elif why == "raw":
            lo, hi = lo_hi(K, wc, excl, rem); need(lo > TGT, "raw: minimum does not exceed 18/13")
        elif why in ("final-abund", "final-count"):
            need(left == "", "final kill on an incomplete T")
            lo, hi = lo_hi(K, wc, excl, rem)
            lon = max(dec(lo), dec(TGT) / h0(K, lo, wc["w"]))
            if why == "final-abund":
                need(lon * DOWN >= dec(hi) * UP, "final-abund: lower bound does not reach HI")
            else:
                cap = dec(TGT) / lon * UP
                sm = [x for x in axiom(K, False) if x >= 5 and x % 3 == 2 and prime(x) and x != wc["w"] and dec(fval(x)) <= cap]
                k = 6 - alpha
                if len(sm) >= k:
                    pr = Fr(1)
                    for x in sorted(sm, reverse=True)[:k]: pr *= fval(x)
                    need(dec(pr) * DOWN > cap, "final-count: U can be filled")
        else:
            raise Fail(f"unsupported kill {why}")
    elif a == "pin":
        f = node["f"]; forced_ok(f, node["src"], node["kind"], K, wc)
        need(f not in K and f > lb, "pin: forced prime is in K or <= lb")
        for r in sorted(set(left)):
            if role_ok(f, r): children.append(key_of({**K, f: r}, lb, minus(left, r), w))
    elif a == "cut":
        B = node["B"]; need(isinstance(B, int) and B >= 3, "cut: bad B")
        lo, hi = lo_hi(K, wc, excl, rem)
        base = dec(TGT) / (h0(K, lo, wc["w"]) * dec(hi) * UP) * DOWN
        need(base >= corr(B, K, len(left)), "cut: cutoff inequality fails at B")
        for t in primes1(lb, B):
            if t in K: continue
            for r in sorted(set(left)):
                if role_ok(t, r): children.append(key_of({**K, t: r}, t, minus(left, r), w))
    elif a == "caseB":
        need(set(left) == {"o"} and len(left) in (1, 2), "caseB: open slots are not all ordinary")
        # an ordinary unknown t with F(t) inside K: (t^2+t+1) = 3 * (K-smooth)
        for t in axiom(K, True):
            if t > 1 and t % 3 == 1 and prime(t) and (t * t + t + 1) % 3 == 0 and t > lb and t not in K:
                children.append(key_of({**K, t: "o"}, lb, minus(left, "o"), w))
        if len(left) == 2:
            # coupled pair: U uses each unknown at most once, the rest lie in Sm(K)
            lo, hi = lo_hi(K, wc, excl, rem); cap = TGT / lo
            sm = [x for x in axiom(K, False) if x >= 5 and x % 3 == 2 and prime(x) and x != wc["w"] and fval(x) <= cap]
            need(len(sm) + 2 < 6 - alpha, "coupled: count does not kill")
    else:
        raise Fail(f"node action '{a}' is not a proof step")
    for ck in children:
        check(next(it), it, alpha, WC, ck)

def check_profile(it, name):
    roles, Wrole, alpha = PROF[name]
    WC = wconfigs(Wrole, alpha)
    roots = []
    for wl in WC:
        rs = sorted(set(roles))
        for r7 in rs:
            for r13 in rs:
                l = list(roles); l.remove(r7)
                if r13 not in l: continue
                l.remove(r13)
                if role_ok(7, r7) and role_ok(13, r13): roots.append(key_of({7: r7, 13: r13}, 13, "".join(sorted(l)), wl))
        for r13 in rs:
            if role_ok(13, r13): roots.append(key_of({13: r13}, 13, minus(roles, r13), wl))
    for rk in roots:
        check(next(it), it, alpha, WC, rk)
    end = json.loads(next(it)); need(end.get("end") == name, "certificate has extra nodes")
    return len(roots)

if __name__ == "__main__":
    it = iter(sys.stdin)
    head = json.loads(next(it)); name = head["profile"]
    try:
        nroots = check_profile(it, name)
        leftover = sum(1 for _ in it)
        need(leftover == 0, f"{leftover} lines after the end marker")
        n = sum(STATS.values())
        print(f"PROFILE {name}: CERTIFICATE VALID  ({n} nodes, {nroots} roots)")
        for k in sorted(STATS): print(f"   {k}: {STATS[k]}")
        print(f"   axioms used: {sorted(USED)}")
    except (Fail, AssertionError, StopIteration) as e:
        print(f"PROFILE {name}: CERTIFICATE INVALID -- {type(e).__name__}: {e}")
        sys.exit(1)
