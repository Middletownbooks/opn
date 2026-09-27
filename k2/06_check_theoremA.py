#!/usr/bin/env python3
"""
Independent checker for the Theorem A certificates (k = 2, 3 does not divide N).

    python3 05_theoremA_dfs.py --cert <s|sn|snn> | python3 06_check_theoremA.py

It has the same design as s3k2/46.  It trusts nothing about the search
(k2/05, s3k2/41) and shares no code with them.  At every node it recomputes,
from the specification, the children the node's case split requires, so the
tree is checked for exhaustiveness.  It re-verifies each node's claim in exact
or outward-rounded arithmetic.

SPECIFICATION (derived in k2/05's docstring).  3 does not divide N.  Every
ordinary prime is = 2 (mod 3), and these form U.  The special is = 1 (mod 12),
with 3 not dividing e+1.  A notable = 1 (mod 3) has 3 not dividing q+1.
T = the special plus the notables = 1 (mod 3); W = the notables = 2 (mod 3).
prod sigma(C)/C = 2.  U is inside Sm(T).  Forced: the primes = 1 (mod 3) of p+1
(special p) lie in T.  Admissible k: sigma(t^k) has no prime factor = 1 (mod 3)
known not to lie in T.  Tree semantics: every prime of T not in K exceeds lb.
The root is K = {} with lb = 6.

The only cited theorem this checker can invoke is Nielsen 2007
(omega(N) >= 12 when 3 does not divide N, so |U| >= 9), in the count kill.  It
reports whether any certificate actually used it.
"""
import sys, os, json, math, bisect
from fractions import Fraction as Fr
from decimal import Decimal as Dm, getcontext
getcontext().prec = 60
TGT = Fr(2); YB = 10**24; WBND = 1000; NEED_U = 9
UP = Dm(1) + Dm(10) ** -40; DOWN = Dm(1) - Dm(10) ** -40

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
def sigma_pow(t, k): return (t ** (k + 1) - 1) // (t - 1)
def fval(x): return Fr(x * x + x + 1, x * x)
def dec(q): return Dm(q.numerator) / Dm(q.denominator)
Q1 = [q for q in range(7, 1000) if q % 3 == 1 and prime(q)]

PROF = {"s": ("s", 2), "sn": ("ns", 1), "snn": ("nns", 0)}
def admissible(t, k, excl):
    for q in excl:
        if q != t and sigma_pow(t, k) % q == 0: return False
    return True
def least(t, start, step, fallback, ok):
    for k in range(start, 200, step):
        if ok(k): return Fr(sigma_pow(t, k), t ** k)
    return Fr(sigma_pow(t, fallback), t ** fallback)
def wlow(w, ex): return least(w, 4, 2, 200, lambda k: admissible(w, k, ex))
def wconfigs(nW):
    ws = [w for w in range(5, WBND) if w % 3 == 2 and prime(w)]
    if nW == 0: return {"W empty": ((), lambda ex: Fr(1), Fr(1))}
    if nW == 1:
        d = {f"n={w}": ((w,), lambda ex, w=w: wlow(w, ex), Fr(w, w - 1)) for w in ws}
        d[f"n>={WBND}"] = ((), lambda ex: Fr(1), Fr(WBND, WBND - 1)); return d
    d = {}
    for i, a in enumerate(ws):
        for b in ws[i + 1:]:
            d[f"n={a}+n={b}"] = ((a, b), lambda ex, a=a, b=b: wlow(a, ex) * wlow(b, ex), Fr(a, a - 1) * Fr(b, b - 1))
        d[f"n={a}+n>={WBND}"] = ((a,), lambda ex, a=a: wlow(a, ex), Fr(a, a - 1) * Fr(WBND, WBND - 1))
    d[f"n>={WBND}+n>={WBND}"] = ((), lambda ex: Fr(1), Fr(WBND, WBND - 1) ** 2)
    return d
def role_low(t, r, ex):
    if r == "s": return least(t, 1, 4, 201, lambda k: (k + 1) % 3 != 0 and admissible(t, k, ex))
    return least(t, 4, 2, 200, lambda k: (k + 1) % 3 != 0 and admissible(t, k, ex))
def lo_hi(K, wc, ex):
    lo, hi = wc[1](ex), wc[2]
    for t, r in K.items(): lo *= role_low(t, r, ex); hi *= Fr(t, t - 1)
    return lo, hi
_smc = {}
def smooth_members(K):
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
    return ((1 + 1 / (Dm(YB).sqrt() - 1)) ** 2 * best * UP).exp() * UP
def h0(K, lo, ws):
    cap = TGT / lo; p = Fr(1)
    for x in smooth_members(K):
        if x not in ws and fval(x) <= cap: p *= fval(x)
    return dec(p) * UP * tail(tuple(sorted(K)))
def corr(B, K, u):
    b = Dm(B); sb = b.sqrt(); cB = (1 + 1 / (sb - 1)) ** 2
    return (b / (b - 1)) ** u * (cB * euler(K) * ((1 - 1 / sb) ** (-u) - 1)).exp() * UP
_pl = []
def primes1(lo, hi):
    global _pl
    if not _pl or _pl[-1] < hi:
        n = max(hi, 10**5) + 1; s = bytearray([1]) * (n + 1); s[:2] = b"\0\0"
        for i in range(2, math.isqrt(n) + 1):
            if s[i]: s[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        _pl = [p for p in range(7, n + 1) if s[p] and p % 3 == 1]
    return _pl[bisect.bisect_right(_pl, lo):bisect.bisect_left(_pl, hi)]

class Fail(Exception): pass
def need(c, m):
    if not c: raise Fail(m)
def key_of(K, lb, left, w): return (tuple(sorted(K.items())), lb, "".join(sorted(left)), w)
def minus(left, r):
    l = list(left); l.remove(r); return "".join(sorted(l))
def role_ok(t, r): return r != "s" or t % 12 == 1
def forced_ok(f, src, K):
    need(prime(f) and f % 3 == 1, f"{f} is not a prime = 1 mod 3")
    need(K.get(src) == "s" and (src + 1) % f == 0, f"{f} is not forced by a special {src}")

STATS = {}; USED_NIELSEN = [0]
def check(line, it, WC, expect):
    nd = json.loads(line)
    K = {t: r for t, r in nd["K"]}; lb = nd["lb"]; left = "".join(sorted(nd["left"])); w = nd["w"]
    need(key_of(K, lb, left, w) == expect, f"node {key_of(K, lb, left, w)} is not the required {expect}")
    need(all(role_ok(t, r) for t, r in K.items()), "special not = 1 mod 12")
    wc = WC[w]; ex = tuple(q for q in Q1 if q not in K and (q <= lb or not left))
    a = nd["a"]; tag = a if a != "dead" else "dead:" + nd["why"]; STATS[tag] = STATS.get(tag, 0) + 1
    kids = []
    if a == "dead":
        why = nd["why"]
        if why == "closure1":
            forced_ok(nd["f"], nd["src"], K); need(nd["f"] not in K and nd["f"] <= lb, "closure1")
        elif why == "closure2":
            seen = set()
            for f, src, _ in nd["fs"]:
                forced_ok(f, src, K); need(f not in K and f not in seen, "closure2"); seen.add(f)
            need(len(seen) > len(left), "closure2: not more forced primes than slots")
        elif why == "raw":
            lo, hi = lo_hi(K, wc, ex); need(lo > TGT, "raw")
        elif why in ("final-abund", "final-count"):
            need(left == "", "final kill on an incomplete T")
            lo, hi = lo_hi(K, wc, ex)
            lon = max(dec(lo), dec(TGT) / h0(K, lo, wc[0]))
            if why == "final-abund":
                need(lon * DOWN >= dec(hi) * UP, "final-abund fails")
            else:
                raise Fail("final-count needs an axiom file; none was supplied for Theorem A")
        else:
            raise Fail(f"unsupported kill {why}")
    elif a == "pin":
        f = nd["f"]; forced_ok(f, nd["src"], K); need(f not in K and f > lb, "pin")
        for r in sorted(set(left)):
            if role_ok(f, r): kids.append(key_of({**K, f: r}, lb, minus(left, r), w))
    elif a == "cut":
        B = nd["B"]; need(isinstance(B, int) and B >= 3, "bad B")
        lo, hi = lo_hi(K, wc, ex)
        base = dec(TGT) / (h0(K, lo, wc[0]) * dec(hi) * UP) * DOWN
        need(base >= corr(B, K, len(left)), "cut: cutoff inequality fails at B")
        for t in primes1(lb, B):
            if t in K: continue
            for r in sorted(set(left)):
                if role_ok(t, r): kids.append(key_of({**K, t: r}, t, minus(left, r), w))
    else:
        raise Fail(f"node action '{a}' is not a proof step")
    for k in kids: check(next(it), it, WC, k)

if __name__ == "__main__":
    it = iter(sys.stdin); name = json.loads(next(it))["profile"]
    roles, nW = PROF[name]; WC = wconfigs(nW)
    try:
        for wl in WC: check(next(it), it, WC, key_of({}, 6, roles, wl))
        need(json.loads(next(it)).get("end") == name, "extra nodes")
        need(sum(1 for _ in it) == 0, "lines after the end marker")
        print(f"PROFILE {name}: CERTIFICATE VALID  ({sum(STATS.values())} nodes, {len(WC)} roots)")
        for k in sorted(STATS): print(f"   {k}: {STATS[k]}")
        print("   cited theorems used: none (no count kill appears)" if "dead:final-count" not in STATS else "   uses Nielsen 2007")
    except (Fail, StopIteration, KeyError) as e:
        print(f"PROFILE {name}: CERTIFICATE INVALID -- {type(e).__name__}: {e}"); sys.exit(1)
