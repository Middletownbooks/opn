#!/usr/bin/env python3
"""
Independent check of ideas_tail/05_lookahead_base.c (NOTES_RESTRAINED.md 4j).

On [3e6, Y): exact Algorithm-1 survivors; FULL factorisation of r^2+r+1 (it does not use
that session's Lemma P); P = the largest prime factor; if P > r, r is removed when some
prime of M2 below YS divides P^2+P+1 (the special branch is dropped, per that session's
Lemma U).  Compare with ideas_tail/runs/05_a_old.out at x = 1e8 (list below 1e7).
Recorded: survivors 502,588; with P > r 502,357; kept 71,897; ln A kept 0.002856582268385,
all identical to the 05 record.
Run:  python3 18_verify_lookahead.py 100000000 10000000     (about 45 min)
"""
import sys, math
sys.path.insert(0, "/home/user/opn/restrained")
Y, YS = int(sys.argv[1]), int(sys.argv[2]); LO = 3_000_000
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
S_ = []
for r in range(LO + 1, Y):
    if not isp[r]: continue
    if not hit[r]: surv[r] = 1; S_.append(r)
    elif r % 3 == 1 and (r % 4 == 3 or not surv[(r + 1) // 2]): add(r)
def prod(xs):
    while len(xs) > 1: xs = [xs[i] * xs[i+1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]
PM2 = prod([q for q in range(7, YS) if m2[q]])
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
    c = 1
    while True:
        x = y = 2; d = 1
        while d == 1:
            x = (x*x + c) % n; y = (y*y + c) % n; y = (y*y + c) % n; d = math.gcd(abs(x - y), n)
        if d != n: return d
        c += 1
def largest_prime_factor(n):
    best, st = 1, [n]
    while st:
        v = st.pop()
        if v == 1: continue
        if isprime(v): best = max(best, v); continue
        for p in (3, 7, 13, 19, 31, 37, 43):   # quick small splits
            if v % p == 0: st += [p, v // p]; break
        else:
            d = rho_f(v); st += [d, v // d]
    return best
kept = 0; lnA = math.fsum([]); terms = []; withP = 0
for r in S_:
    P = largest_prime_factor(r * r + r + 1)
    if P > r:
        withP += 1
        V = P * P + P + 1
        if math.gcd(PM2 % V, V) != 1: continue        # removed
    kept += 1; terms.append(math.log1p(1.0 / (r - 1)))
print(f"[3e6, {Y:.0e}): survivors {len(S_):,}; with P > r {withP:,}; kept {kept:,}; ln A kept {math.fsum(terms):.15f}")
