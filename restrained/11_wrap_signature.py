#!/usr/bin/env python3
"""
Is the 64-bit wrap of loopless.cpp (NOTES_RESTRAINED.md 4b) visible in the paper's
own reported numbers?

The released loopless.cpp (sources/loopless.cpp, the file the user attached; line
135: `u64 val = r * r + r + 1;`) is exact for r < 2^32.  Beyond that it tests
(r^2 + r + 1) mod 2^64 instead of r^2 + r + 1.

PART 1.  Two-level fit from the paper's output.  The paper reports k = 2.5e9
survivors and abundancy A = 1.088507187872 at z = 216,171,986,291.  Suppose the
survival fraction (survivors / primes) is f0 on (3e6, 2^32) and f1 on (2^32, z).
Then
    ln A ~ f0 * ln(ln 2^32 / ln 3e6) + f1 * ln(ln z / ln 2^32)
    k    ~ f0 * #primes(3e6, 2^32) + f1 * #primes(2^32, z)
fix f0 and f1.  An exact sieve's survival fraction can only DECREASE with r,
because M2 only grows.

PART 2.  The mechanism.  A prime q = 1 (mod 3) divides x^2 + x + 1 for 2 residues
of x mod q, so it divides r^2 + r + 1 with probability about 2/q.  A wrapped value
is essentially an unrelated 64-bit number, divisible by q with probability about 1/q.
So the survival probability under the wrap is about
    prod (1 - 1/q) ~ sqrt( prod (1 - 2/q) ),
the square root of the exact one.  This is tested on sampled primes, using the
INITIAL M2 (all primes = 1 mod 3 in [7, 3e6)): exact test versus wrapped test.

Parts 1 and 2 are evidence about the published run.  They are not a
re-computation of the sieve.

Run:  python3 11_wrap_signature.py [samples] [seed]
Recorded (NOTES_RESTRAINED.md 4b): 10000 samples, seed 7:
   exact 0.1133 / 0.1163 / 0.1133,  wrapped 0.1133 / 0.4358 / 0.3592
for r in 1e7..1e8, 2^32..2^32+1e9, 1e11..z.  (3000 samples at the default seed give
exact 0.1017 / 0.1317 / 0.1097: the spread is sampling noise.)
"""
import math, random, sys

def li(x, a=2.0, n=200000):
    la, lb = math.log(a), math.log(x); s = 0.0
    for i in range(n):
        t = la + (i + 0.5) * (lb - la) / n; s += math.exp(t) / t
    return s * (lb - la) / n

z = 216171986291; LO = 3_000_000; T = 2**32
print("PART 1: two-level fit to the paper's reported (k, A) at z")
P0, P1 = li(T) - li(LO), li(z) - li(T)
w0, w1 = math.log(math.log(T) / math.log(LO)), math.log(math.log(z) / math.log(T))
lnA, k = math.log(1.088507187872), 2.5e9
det = w0 * P1 - w1 * P0
f0 = (lnA * P1 - w1 * k) / det; f1 = (w0 * k - lnA * P0) / det
print(f"   primes in (3e6, 2^32) ~ {P0:.3e};  in (2^32, z) ~ {P1:.3e}")
print(f"   fitted survival fraction:  below 2^32 f0 = {f0:.4f},  above 2^32 f1 = {f1:.4f}")
print(f"   sqrt(f0) = {math.sqrt(f0):.4f}   (the wrap heuristic predicts f1 ~ sqrt(f0))")
print("   An exact sieve would have f1 < f0.  The reported output has f1 ~ 3 f0.")
print()

print("PART 2: exact versus wrapped test against the initial M2, on sampled primes")
sieve = bytearray([1]) * LO; sieve[:2] = b"\0\0"
for i in range(2, int(LO ** 0.5) + 1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(range(i*i, LO, i)))
M2 = [q for q in range(7, LO) if sieve[q] and q % 3 == 1]
def product_tree(xs):
    while len(xs) > 1:
        xs = [xs[i] * xs[i+1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]
PM2 = product_tree(M2)                 # product of the initial M2
def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        y = pow(a, d, n)
        if y in (1, n - 1): continue
        for _ in range(s - 1):
            y = y * y % n
            if y == n - 1: break
        else: return False
    return True
def survives(v):                       # no prime of the initial M2 divides v
    if v % 3 == 0: v //= 3
    return math.gcd(PM2 % v, v) == 1 if v > 1 else True
print(f"   |initial M2| = {len(M2)}")
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20260927)
NS = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
print(f"   {'range of r':28s} {'exact':>8s} {'wrapped':>8s} {'sqrt(exact)':>12s}   (samples = {NS})")
for lo, hi, name in [(10**7, 10**8, "1e7 .. 1e8 (no wrap)"),
                     (2**32, 2**32 + 10**9, "2^32 .. 2^32+1e9"),
                     (10**11, z, "1e11 .. z")]:
    ex = wr = n = 0
    while n < NS:
        r = rng.randrange(lo, hi) | 1
        if not is_prime(r): continue
        n += 1
        v = r * r + r + 1
        ex += survives(v); wr += survives(v % 2**64)
    fe, fw = ex / n, wr / n
    print(f"   {name:28s} {fe:8.4f} {fw:8.4f} {math.sqrt(fe):12.4f}")
print("""
Reading.  Against the same M2, the wrapped test lets through about sqrt(exact) of
the primes, as the heuristic predicts (just above 2^32 even more, because there the
wrapped value is a structured quadratic in r - 2^32, not a random 64-bit number).  Below 2^32 the two tests coincide, as they
must.  The paper's output shows the same signature (Part 1): its survival fraction
triples at 2^32.  So the published k and A at z are, on this evidence, the output of
the wrapped test and not of Algorithm 1.  What the exact sieve gives is for the
re-run to settle.  Part 1 suggests the exact survivor set is SMALLER, and a smaller
set only raises k + K_max (restrained/10, item 5).  That is a heuristic, not a
result.""")
