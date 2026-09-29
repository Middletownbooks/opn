#!/usr/bin/env python3
"""
ideas_tail/06 -- independent check of 05's look-ahead counts on a small range.
For every exact survivor r in [LO, HI) (from the 03 state file) it FULLY factors
r^2+r+1 (Pollard-Brent/ECM from 00_ntlib, no use of D-primes), takes the largest
prime factor P if P > r, and tests P^2+P+1 against the initial M2 (primes = 1 mod 3
in [7, 3e6)).  Prints nsurv, nP, nfail, kLA, lnALA for comparison with 05's CP line.
Run:  python3 06_check_05.py STATE LO HI
"""
import sys, math, importlib.util as iu
spec = iu.spec_from_file_location("nt", __file__.replace("06_check_05.py", "00_ntlib.py"))
nt = iu.module_from_spec(spec); spec.loader.exec_module(nt)
st = open(sys.argv[1], "rb").read(); LO, HI = int(float(sys.argv[2])), int(float(sys.argv[3]))
M2 = nt.prod_tree([q for q in range(7, 3_000_000) if q % 3 == 1 and st[q] == 1])
nsurv = nP = nfail = kla = 0; terms = []
for r in range(LO, HI):
    if st[r] != 2: continue
    nsurv += 1
    fs, rest = nt.factor(r * r + r + 1)
    assert not rest
    P = max(fs)
    term = math.log1p(1 / (r - 1))
    if P <= r: kla += 1; terms.append(term); continue
    nP += 1
    if math.gcd(M2, P * P + P + 1) > 1: nfail += 1
    else: kla += 1; terms.append(term)
print(f"nsurv={nsurv} nP={nP} nfail={nfail} kLA={kla} lnALA={math.fsum(terms):.15g}")
