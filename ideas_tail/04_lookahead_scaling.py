#!/usr/bin/env python3
"""
ideas_tail/04 -- how the look-ahead's removal rate behaves with r, with and without
the special branch, and at depth 2.

Setting (sound, RESULT.md Idea 3).  If r is ordinary and n = r^2+r+1 has a prime
factor P > r (there is at most one), then P | N and P is ordinary or P = p.
  * P = p happens for AT MOST TWO ordinary r: r < p and p | r^2+r+1 make r one of
    the two roots of x^2+x+1 mod p in (0, p).  (The special prime is unique.)
  * So, apart from those two r, P must be ORDINARY: no prime of M2 divides P^2+P+1.
  * Depth 2: P ordinary and P^2+P+1 has a prime factor P' > P  =>  P' ordinary, apart
    from at most two P (hence four r) with P' = p.
The brief's restrained/17 also allowed "P special" for every r; that is the column
"old".  "new" drops the special branch (the two exceptions cost at most
2 ln(r1/(r1-1)) < 7e-7 in ln A).

Survivors sampled on (x, 2x]:
  * 2x <= Y: EXACT Algorithm-1 survivors, from the 03 state file;
  * 2x >  Y: primes r whose r^2+r+1 has no factor in M2 below Y: a SUPERSET of the
    survivors ("static-Y survivors").  Rates there are indicative, not exact.
Tests use M2 and M1 below Ys (default Ys = Y = 1e8); a subset of the true sets, so
every removal is sound.  A factorisation that exceeds the budget keeps r (sound).
Run:  python3 04_lookahead_scaling.py STATE Y SAMPLES [scales...]
"""
import sys, math, random, time, importlib.util as iu
spec = iu.spec_from_file_location("nt", __file__.replace("04_lookahead_scaling.py", "00_ntlib.py"))
nt = iu.module_from_spec(spec); spec.loader.exec_module(nt)

STATE, Y, NS = sys.argv[1], int(float(sys.argv[2])), int(sys.argv[3])
SCALES = [float(s) for s in sys.argv[4:]] or [3e6, 1e7, 2.5e7, 5e7, 1e9, 1e10, 1e11, 1e12]
st = open(STATE, "rb").read()
assert len(st) == Y + 1
t0 = time.time()
M2 = [q for q in range(7, Y + 1) if q % 3 == 1 and st[q] in (1, 4)]
M1 = [q for q in range(5, Y + 1) if st[q] in (1, 3, 4)]
DP = [q for q in range(7, Y + 1) if q % 3 == 1 and st[q] in (2, 3)]
EDGES = [7, 1000, 10**4, 10**5, 10**6, 3 * 10**6, 10**7, 3 * 10**7, Y + 1]
def chunks(L):
    out = []
    for a, b in zip(EDGES, EDGES[1:]):
        out.append(nt.prod_tree([v for v in L if a <= v < b]))
    return out
M2C, M1C, PD = chunks(M2), chunks(M1), nt.prod_tree(DP)
print(f"# state Y={Y}: |M2|={len(M2)} |M1|={len(M1)} |D|={len(DP)}  ({time.time()-t0:.0f}s)", flush=True)
def hits(C, n): return any(math.gcd(c, n) > 1 for c in C)

def split_small(n):
    """n with 3 removed; returns (list of D-primes < Y with multiplicity, has_M2_factor_below_Y, cofactor)"""
    while n % 3 == 0: n //= 3
    if hits(M2C, n): return None, True, None
    g = math.gcd(PD, n); ds = []
    if g > 1:
        fs, rest = nt.factor(g)
        assert not rest
        for q in sorted(set(fs)):
            while n % q == 0: n //= q; ds.append(q)
    return ds, False, n

def big_factor(n, lower):
    """the prime factor of n exceeding `lower` (at most one exists when n < (lower+1)^2),
    as (status, P): status 'none' / 'P' / 'M2' (a factor in M2 below Y) / 'unres'"""
    ds, m2hit, C = split_small(n)
    if m2hit: return "M2", None
    cands = [q for q in ds if q > lower]
    if C > 1:
        if C <= lower: pass
        elif nt.is_prime(C): cands.append(C)
        else:
            fs, rest = nt.factor(C, rho_budget=300_000)
            if rest: return "unres", None
            cands += [f for f in fs if f > lower]
    return ("P", max(cands)) if cands else ("none", None)

def ord_ok(P): return not hits(M2C, P * P + P + 1)
def spec_ok(P): return P % 12 == 1 and not hits(M1C, (P + 1) // 2)

rng = random.Random(20260929)
print(f"{'x':>8} {'n':>5} {'P>r':>6} {'old':>6} {'new':>6} {'new d2':>7} {'unres':>6} {'term':>5}  (removal %)")
for x in SCALES:
    x = int(x); t1 = time.time()
    if 2 * x <= Y:
        pool = [r for r in range(x + 1, 2 * x + 1) if st[r] == 2]
        sample = rng.sample(pool, min(NS, len(pool)))
    else:
        sample = []
        while len(sample) < NS:
            r = rng.randrange(x + 1, 2 * x + 1) | 1
            if nt.is_prime(r) and not hits(M2C, r * r + r + 1): sample.append(r)
    nP = old = new = new2 = unres = term = 0
    for r in sample:
        s, P = big_factor(r * r + r + 1, r)
        if s == "M2": nP += 1; old += 1; new += 1; new2 += 1; continue
        if s == "unres": unres += 1; continue
        if s == "none": term += 1; continue
        nP += 1
        o, sp = ord_ok(P), spec_ok(P)
        if not (o or sp): old += 1
        if not o: new += 1; new2 += 1; continue
        s2, P2 = big_factor(P * P + P + 1, P)            # depth 2
        if s2 == "M2": new2 += 1
        elif s2 == "unres": unres += 1
        elif s2 == "P" and not ord_ok(P2): new2 += 1
    n = len(sample); f = lambda a: f"{100 * a / n:6.1f}"
    print(f"{x:8.0e} {n:5d} {f(nP)} {f(old)} {f(new)} {f(new2):>7} {unres:6d} {term:5d}   ({time.time()-t1:.0f}s)", flush=True)
