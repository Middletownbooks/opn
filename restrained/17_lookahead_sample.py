#!/usr/bin/env python3
"""
One-step LOOK-AHEAD on Algorithm-1 survivors (NOTES_RESTRAINED.md 4i).

If r survives and r^2+r+1 has a prime factor P > r, then P | sigma(r^2) | 2N, so P | N.
P != 3 (the notable prime), so P is ordinary or special.
  * ordinary => sigma(P^2) = P^2+P+1 | 2N, so no prime of M2 divides it;
  * special  => P = 1 (mod 12) (Euler; their Lemma 6), and e is odd, so (P+1) | sigma(P^e).
    Every prime of (P+1)/2 then divides N and is ordinary, so none lies in M1.
If both fail, r cannot be ordinary.  Algorithm 1 never looks at P.  This is sound and
uses only facts from the paper; using M1 and M2 below Y/2 (a subset) keeps it conservative.

It samples survivors of exact Algorithm 1 in (Y/2, Y] and reports the fraction removed.
Run:  python3 17_lookahead_sample.py Y SAMPLES      (Y = 1e8, 3000 samples: about 4 min)
"""
# Using only M2 and M1 below Y/2 (subsets of what is known at time r) keeps it sound.
import sys, math, random
Y = int(sys.argv[1]); NS = int(sys.argv[2]); LO = 3_000_000
isp = bytearray([1]) * (Y + 1); isp[:2] = b"\0\0"
for i in range(2, math.isqrt(Y) + 1):
    if isp[i]: isp[i*i::i] = bytearray(len(range(i*i, Y + 1, i)))
hit = bytearray(Y + 1); m2 = bytearray(Y + 1); surv = bytearray(Y + 1)
def add(q):
    m2[q] = 1; e = (q - 1) // 3
    rho = next(v for v in (pow(g, e, q) for g in range(2, q)) if v != 1)
    for c in (rho, q - 1 - rho):
        t = c + q
        if t <= Y: hit[t::q] = b"\1" * len(range(t, Y + 1, q))
for q in range(7, LO):
    if isp[q] and q % 3 == 1: add(q)
for r in range(LO + 1, Y + 1):
    if not isp[r]: continue
    if not hit[r]: surv[r] = 1
    elif r % 3 == 1 and (r % 4 == 3 or not surv[(r + 1) // 2]): add(r)
H = Y // 2
def prod(xs):
    while len(xs) > 1: xs = [xs[i] * xs[i+1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]
PM2 = prod([q for q in range(7, H) if m2[q]])                                  # M2 below Y/2
PM1 = prod([p for p in range(5, H) if isp[p] and (p < LO or not surv[p])])     # M1 below Y/2
def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
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
def rho_f(n):
    if n % 2 == 0: return 2
    x = y = 2; c = 1; d = 1
    while True:
        x = (x*x + c) % n; y = (y*y + c) % n; y = (y*y + c) % n; d = math.gcd(abs(x - y), n)
        if d == n: c += 1; x = y = 2; continue
        if d > 1: return d
def factors(n):
    out, st = [], [n]
    while st:
        v = st.pop()
        if v == 1: continue
        if isprime(v): out.append(v); continue
        d = rho_f(v); st += [d, v // d]
    return out
S_ = [r for r in range(H + 1, Y + 1) if surv[r]]
rng = random.Random(1); sample = rng.sample(S_, min(NS, len(S_)))
big = killed = 0
for r in sample:
    fs = factors(r * r + r + 1)
    P = max(fs)
    if P <= r: continue
    big += 1
    ordinary_ok = math.gcd(PM2 % (P*P + P + 1), P*P + P + 1) == 1
    special_ok = P % 12 == 1 and math.gcd(PM1 % ((P + 1) // 2), (P + 1) // 2) == 1
    if not ordinary_ok and not special_ok: killed += 1
print(f"survivors in ({H:,}, {Y:,}]: {len(S_):,}; sample {len(sample)}: "
      f"{big} have a prime factor P > r ({100*big/len(sample):.1f}%); "
      f"look-ahead removes {killed} ({100*killed/len(sample):.1f}% of the sample)")
