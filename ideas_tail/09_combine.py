#!/usr/bin/env python3
"""
ideas_tail/09 -- the q bound with the look-ahead base (Ideas 1-3 of RESULT.md combined).

Inputs: pieces FILE:LO:X of 05 outputs covering [3e6, 3.4e10) in disjoint look-ahead
ranges [LO, X): X is the "CP x=X" line of a run stopped early, or "end" for a run's
SUMMARY.  Where restrained/13 has a checkpoint at X, the piece's Algorithm-1 k and ln A
must agree with it to every printed digit.

Base set T' below 1e12 (sound superset of O n (3e6, 1e12], up to the exceptions E):
  * survivors in (3e6, 3.4e10) kept by the depth-1 look-ahead (05);
  * the Q = 2^35 superset run's survivors in [3.4e10, 1e12] (restrained/13);
  * the exceptions E (|E| <= 2; each has w < ln(3e6/(3e6-1))) -- counted in Lambda only.
Then:
  (A) RIGOROUS, no sieve beyond 1e12 (Lemma G0, the method of 01);
  (B) PILOT, the weighted Selberg bound of 02 with remainder 2 E1^2 (Lemma G).
Run:  python3 09_combine.py FILE:LO:X ...   (see RESULT.md for the exact command)
"""
import sys, re, math, os
from decimal import Decimal as D, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
ref = {}
for l in open(os.path.join(HERE, "..", "restrained", "runs", "13_1e12_Q2e35_checkpoints.txt")):
    m = re.match(r"CP x=(\d+) k=(\d+) lnA=(\S+)", l)
    if m: ref[int(m[1])] = (int(m[2]), m[3])
kla, lna, ranges = 0, D(0), []
for spec in sys.argv[1:]:                      # FILE:LO:X  (X = a CP x, or "end" for SUMMARY)
    fn, lo, x = spec.split(":"); lo = int(lo)
    if x == "end":
        line = [l for l in open(fn) if l.startswith("SUMMARY")][0]
        g = dict(re.findall(r"(\w+)=(\S+)", line)); hi = int(g["ZEND"])
        assert int(re.match(r"\[(\d+),", g["LA"]).group(1)) == lo
    else:
        hi = int(x)
        line = [l for l in open(fn) if l.startswith(f"CP x={hi} ")][0]
        g = dict(re.findall(r"(\w+)=(\S+)", line))
    if hi in ref:
        assert int(g["k"]) == ref[hi][0] and g["lnA"] == ref[hi][1], f"{fn}: mismatch with restrained/13 at {hi}"
    kla += int(g["kLA"]); lna += D(g["lnALA"]) + D("1e-15")
    ranges.append((lo, hi, int(g["nsurv"]), int(g["nP"]), int(g["nfail"]), int(g["kLA"]), g["lnALA"]))
ranges.sort()
assert ranges[0][0] == 3_000_000 and all(a[1] == b[0] for a, b in zip(ranges, ranges[1:])) and ranges[-1][1] == 34 * 10**9
print("look-ahead ranges (k, ln A checked against restrained/13 wherever it has a checkpoint):")
print(f"{'range':>26} {'survivors':>11} {'with P':>11} {'removed':>11} {'kept %':>7} {'ln A kept':>12}")
for lo, hi, ns, nP, nf, k, l in ranges:
    print(f"[{lo:.2e}, {hi:.2e}) {ns:11,d} {nP:11,d} {nf:11,d} {100*(ns-nf)/ns:7.2f} {float(l):12.6f}")
R1 = 34 * 10**9
k1, l1 = ref[R1][0], D(ref[R1][1])
kS, lS = ref[10**12][0], D(ref[10**12][1]) + D("1e-15")
wmax = (D(3_000_000) / D(2_999_999)).ln()
T = kla + (kS - k1)
LAM0 = lna + (lS - l1) + 2 * wmax
print(f"\nAlgorithm 1 below 3.4e10: k = {k1:,d}, ln A = {float(l1):.6f};  look-ahead kept: k = {kla:,d}, ln A = {float(lna):.6f}")
print(f"base below 1e12:  |T'| >= {T:,d},  Lambda_0 <= {float(LAM0):.6f}   (was {kS:,d}, {float(lS):.6f})")

# (A) rigorous, no sieve (Lemma G0 + RS-a, RS-c, pi(1e12))
c = (D(4) / D(3)).ln() - (1 + D(1) / D(6_000_000)).ln()
Z0, PI_Z0 = D(10) ** 12, 37_607_912_018
def lnln(x): return x.ln().ln()
def boundA(z):
    lam = LAM0 + lnln(z) - lnln(Z0) + 1 / (2 * z.ln() ** 2) + 1 / (2 * Z0.ln() ** 2) + 1 / Z0
    if lam >= c: return None
    O = T + int(z / z.ln()) - PI_Z0 + int((c - lam) / (1 + 1 / z).ln()) + 1
    return (O + 2) // 2 - 2
lo_, hi_ = Z0, Z0 * 10**6
for _ in range(300):
    mid = (lo_ * hi_).sqrt()
    if boundA(mid) is None: hi_ = mid
    else: lo_ = mid
print(f"\n(A) rigorous, no sieve beyond 1e12:  q >= {boundA(lo_):,d}   (z ~ {float(lo_):.3e})")

# (B) pilot: weighted Selberg from the 16c tables, remainder 2 E1^2, Lemma G
tab = [tuple(map(float, l.split())) for l in
       open(os.path.join(HERE, "..", "restrained", "runs", "16c_selberg_tables_M2_1e8.txt"))]
cf = float(c)
def V(x): return min(math.log(2) / G + 2 * (1 + E1 * E1) / x for t, G, W, E1 in tab if t < x) * (1 + 1 / x)
def greedy(lam0, T0):
    lam, y, acc, best = lam0, 1e12, float(T0), (0.0, 0.0)
    while y < 1e300:
        w = math.log1p(1 / y)
        if lam <= cf and acc + (cf - lam) / w > best[0]: best = (acc + (cf - lam) / w, y)
        v = V(y)
        if lam + v > cf: break
        lam += v; acc += v / w; y *= 2
    return best
for name, l0, t0 in (("old base", float(lS), kS), ("look-ahead base", float(LAM0), T)):
    b = greedy(l0, t0)
    print(f"(B) pilot, Selberg beyond 1e12, {name:16s}: q ~ {b[0] / 2:.3e}  (z ~ {b[1]:.2e})")
