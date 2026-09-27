#!/usr/bin/env python3
"""
Pilot: an independent re-check of Ochem-Zelinsky's tree.txt claim, "every prime
from 11 up to 3,000,000 is ruled out" (section 4).  That claim is the input
assumption of Algorithm 1: M1 and M2 start as every prime below 3e6.

THE METHOD (tree.cpp's specification; soundness discussed in NOTES_INVERSION.md
and NOTES_RESTRAINED.md 4e).  Setting: N a restrained OPN with notable prime 3, and
5 and 7 already ruled out by hand.  Roots r are taken in increasing order, so every
prime 5 <= p < r is already known not to divide N.  To rule out r, assume r | N.
Then r is ordinary or special:
  * ordinary: sigma(r^2) = r^2+r+1 divides 2N.  Divide out the single 3 when
    r = 1 (mod 3); 2 never divides it.  Every remaining prime factor f divides N;
  * special (only if r = 1 mod 12, by Euler and their Lemma 6, and only if no other
    prime on this path is already special): e = 1 (mod 4) is odd, so r+1 | sigma(r^e).
    Every prime factor f >= 5 of (r+1)/2 divides N ((r+1)/2 = 1 mod 6 has no 2, 3).
A branch is CONTRADICTED if some such f is < root (already ruled out), or if some f
not already on the current path is itself contradicted in every status it can have
(recursion).  r is ruled out iff every branch open to it is contradicted.

IMPLEMENTATION, independent of tree.cpp:
  * small factors: g = gcd(G, P), with P the product of all primes 5..3e6.  A
    factor p < root is an immediate contradiction; factors root <= p < 3e6 are recursed on;
  * the 3e6-rough cofactor: checkfacts.txt entries are used ONLY as hints.  Each is
    verified to divide and to be a (probable) prime before use, since tree.cpp does not
    check.  The remainder is factored by Pollard-Brent with an iteration budget;
  * primality: deterministic Miller-Rabin below 3.3e24 (the first 13 prime bases),
    strong probable prime to 20 bases above (stated as such);
  * a per-root node budget.  Any root whose proof cannot finish within the budgets is
    reported UNRESOLVED, never as ruled out.

Run:  python3 15_tree_pilot.py LO HI [MAXROOTS]      (roots: primes in [LO, HI])
Prints the roots ruled out, the unresolved ones, and the timing per root.
"""
import sys, os, math, time, random

LIM = 3_000_000
HERE = os.path.dirname(os.path.abspath(__file__))

def small_primes(n):
    s = bytearray([1]) * (n + 1); s[:2] = b"\0\0"
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = bytearray(len(range(i*i, n + 1, i)))
    return s
ISP = small_primes(LIM)
PR = [p for p in range(5, LIM) if ISP[p]]
def prod_tree(xs):
    while len(xs) > 1:
        xs = [xs[i] * xs[i+1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]
P_ALL = prod_tree(PR)

MRB = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
def is_prime(n):
    if n < 2: return False
    if n <= LIM: return bool(ISP[n])
    for p in MRB:
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    bases = MRB if n < 3317044064679887385961981 else MRB + (43, 47, 53, 59, 61, 67, 71)
    for a in bases:
        y = pow(a, d, n)
        if y in (1, n - 1): continue
        for _ in range(s - 1):
            y = y * y % n
            if y == n - 1: break
        else: return False
    return True

class Budget(Exception): pass
RHO_BUDGET = 50_000_000
def brent(n):
    if n % 2 == 0: return 2
    rng = random.Random(n)
    for _ in range(20):
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g = r = q = 1; it = 0
        while g == 1:
            x = y
            for _ in range(r): y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n; q = q * abs(x - y) % n
                g = math.gcd(q, n); k += m
            r *= 2; it += r
            if it > RHO_BUDGET: raise Budget(n)
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n; g = math.gcd(abs(x - ys), n)
        if g != n: return g
    raise Budget(n)

# checkfacts.txt: "x type f" triples, type 3 = factor of x^2+x+1, type 2 = factor of x+1
HINTS = {}
cf = os.path.join(HERE, "..", "sources", "checkfacts.txt")
if os.path.exists(cf):
    tok = open(cf).read().split()
    for i in range(0, len(tok) - 2, 3):
        x, t, f = int(tok[i]), int(tok[i+1]), int(tok[i+2])
        HINTS.setdefault((x, t), []).append(f)
HINT_USED = [0]; HINT_REJECTED = []

def factor_rough(n, out):
    """all prime factors (>= 3e6) of n, into the set out"""
    stack = [n]
    while stack:
        v = stack.pop()
        if v == 1: continue
        if is_prime(v): out.add(v); continue
        d = brent(v); stack += [d, v // d]

def branch_factors(x, typ, root):
    """('F', p) if a prime factor < root exists; else ('ok', set of prime factors >= 5)"""
    if typ == 3:
        G = x * x + x + 1
        if x % 3 == 1: G //= 3
    else:
        G = (x + 1) // 2
    fs = set()
    g = math.gcd(G, P_ALL % G) if G > 1 else 1
    if g > 1:
        # factor g: all its primes are < 3e6
        for p in small_factor_list(g):
            if p < root: return ('F', p)
            fs.add(p)
        while True:
            h = math.gcd(G, g)
            if h == 1: break
            G //= h
    for f in HINTS.get((x, typ), ()):
        if f >= 5 and G % f == 0:
            if not is_prime(f): HINT_REJECTED.append((x, typ, f)); continue
            HINT_USED[0] += 1
            while G % f == 0: G //= f
            fs.add(f)
    if G > 1: factor_rough(G, fs)
    return ('ok', fs)

def small_factor_list(g):
    """prime factors of g, a product of distinct primes below 3e6"""
    out, stack = set(), [g]
    while stack:
        v = stack.pop()
        if v == 1: continue
        if is_prime(v): out.add(v); continue
        d = brent(v); stack += [d, v // d]
    return sorted(out)

NODE_BUDGET = 20000
def prove(root, x, special_used, path, cnt):
    cnt[0] += 1
    if cnt[0] > NODE_BUDGET: raise Budget(("nodes", root))
    path.add(x)
    try:
        sp_elig = (not special_used) and x % 12 == 1
        sp_ok = False
        if sp_elig:
            kind, v = branch_factors(x, 2, root)
            if kind == 'F': sp_ok = True
            else:
                for f in sorted(v):
                    if f in path: continue
                    if prove(root, f, True, path, cnt): sp_ok = True; break
            if not sp_ok: return False            # the special branch stays open
        kind, v = branch_factors(x, 3, root)
        if kind == 'F': return True
        for f in sorted(v):
            if f in path: continue
            if prove(root, f, special_used, path, cnt): return True
        return False
    finally:
        path.discard(x)

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    maxroots = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    roots = [p for p in range(max(lo, 11), min(hi, LIM - 1) + 1) if ISP[p]][:maxroots]
    t0 = time.time(); ok = 0; unres = []; worst = (0, None); nodes = 0
    for r in roots:
        t1 = time.time(); cnt = [0]
        try:
            res = prove(r, r, False, set(), cnt)
        except Budget as b:
            res = None; unres.append((r, "budget", str(b.args[0])[:40]))
        dt = time.time() - t1; nodes += cnt[0]
        if dt > worst[0]: worst = (dt, r)
        if res: ok += 1
        elif res is False: unres.append((r, "open", ""))
    T = time.time() - t0
    print(f"roots {len(roots)} in [{roots[0] if roots else '-'}, {roots[-1] if roots else '-'}]: "
          f"ruled out {ok}, unresolved {len(unres)}; {T:.1f}s total, {T/max(1,len(roots))*1000:.2f} ms/root, "
          f"{nodes/max(1,len(roots)):.1f} nodes/root, worst {worst[0]:.2f}s at {worst[1]}; "
          f"checkfacts hints used {HINT_USED[0]}, rejected {len(HINT_REJECTED)}")
    for u in unres[:30]: print("   UNRESOLVED", u)
    for h in HINT_REJECTED[:10]: print("   REJECTED HINT", h)
