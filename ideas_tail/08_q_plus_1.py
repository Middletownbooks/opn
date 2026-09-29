#!/usr/bin/env python3
"""
ideas_tail/08 -- secondary question (b): what sigma(3^q) = (3^{q+1}-1)/2 forces on q+1.

LEMMA (proved in RESULT.md, Idea 7).  If an odd prime l divides q+1, then every prime
t with 3^l = 1 (mod t), t != 2, divides sigma(3^q), hence divides N.  So if some such t
is KNOWN not to divide N, then l does not divide q+1.

"Known not to divide N" (the set X), from the exact state below Y (03):
  * every prime 5 <= t < 3e6 (F1);
  * t in M2 (status 4);
  * t = 2 mod 3 and not a survivor (status 3): not ordinary, and not special (p = 1 mod 12).
For l whose small factors do not settle it, the cofactor of (3^l-1)/2 is tested when it
is a probable prime C:  C is excluded if C^2+C+1 has a factor in M2 below Y and (C = 2
mod 3, or C = 3 mod 4, or (C+1)/2 has a factor in M1 below Y).
Second pass: for each l still open, try to factor (3^l-1)/2 (rho + ECM, budgeted) and
apply the same local test to every prime factor found above Y.
Output: the odd primes l < L that are NOT excluded (so q+1 might be divisible by them).
Run:  python3 08_q_plus_1.py STATE Y L
"""
import sys, math, importlib.util as iu
spec = iu.spec_from_file_location("nt", __file__.replace("08_q_plus_1.py", "00_ntlib.py"))
nt = iu.module_from_spec(spec); spec.loader.exec_module(nt)
st = open(sys.argv[1], "rb").read(); Y = int(float(sys.argv[2])); L = int(sys.argv[3])
def excluded(t): return st[t] in (1, 4) or (st[t] == 3 and t % 3 == 2)
PM2 = nt.prod_tree([q for q in range(7, Y) if q % 3 == 1 and st[q] in (1, 4)])
PM1 = nt.prod_tree([q for q in range(5, Y) if st[q] in (1, 3, 4)])
isp = lambda n: n < 2 ** 62 and n <= Y and st[n] != 0 or (n > Y and nt.is_prime(n))
open_l = []; how = {"small": 0, "cofactor": 0}
for l in range(3, L, 2):
    if not nt.is_prime(l): continue
    R = (3 ** l - 1) // 2; found = False; cof = R
    for t in range(2 * l + 1, Y + 1, 2 * l):
        if st[t] == 0: continue                        # not a prime >= 5
        if pow(3, l, t) == 1:
            while cof % t == 0: cof //= t
            if excluded(t): found = True; break
    if found: how["small"] += 1; continue
    if cof > 1 and nt.is_prime(cof):
        C = cof
        m2 = math.gcd(PM2, C * C + C + 1) > 1
        nospec = C % 3 == 2 or C % 4 == 3 or math.gcd(PM1, (C + 1) // 2) > 1
        if m2 and nospec: how["cofactor"] += 1; continue
    open_l.append((l, len(str(cof))))
print(f"odd primes l < {L}: excluded via a factor below {Y:.0e}: {how['small']}, via a prime cofactor: {how['cofactor']}")
print(f"NOT excluded ({len(open_l)}): " + ", ".join(f"{l} (cofactor {d} digits)" for l, d in open_l[:40]))

def local_excluded(t):
    if t <= Y: return excluded(t)
    if math.gcd(PM2, t * t + t + 1) == 1: return False          # could be ordinary
    return t % 3 == 2 or t % 4 == 3 or math.gcd(PM1, (t + 1) // 2) > 1
still = []
for l, _ in open_l:
    fs, rest = nt.factor((3 ** l - 1) // 2, rho_budget=200_000)
    hit = [t for t in fs if local_excluded(t)]
    if hit: print(f"   l = {l}: excluded by the factor {hit[0]}")
    else: still.append((l, fs, [len(str(r)) for r in rest]))
print(f"after factoring: still open: {[s[0] for s in still]}")
for l, fs, rest in still: print(f"   l = {l}: factors found {fs}, unsplit parts of {rest} digits")
