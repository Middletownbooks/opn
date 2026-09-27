#!/usr/bin/env python3
"""
Audit Part A2: recompute the section-14d cutoff thresholds from the lemma as
re-derived in AUDIT_S3K2_RESULT.md (written independently of s3k2/34):

  T = S u R, |R| = k, every r in R >= B.  For x in Sm(T)\\Sm(S):
      log f(x) <= (sqrt(M)-1)^(-1) <= (1 + 1/(sqrt(B)-1)) M^(-1/2)      (a2_corr_factor_check)
      sum_x M^(-1/2) <= E(S) * (prod_R (1 - r^(-1/2))^(-1) - 1) <= E(S) ((1-B^(-1/2))^(-k) - 1)
  and every R-factor < B/(B-1).  So PROD_T(R) * PROD_U(T) < H0(S) * corr(B), with
      corr(B) = (B/(B-1))^k * exp((1 + 1/(sqrt B - 1)) * E(S) * ((1-B^-1/2)^-k - 1)),
  (no 1.01 needed), and T dies if (18/13) / (H0(S) HI(S)) >= corr(B).
Margins (18/13)/(H0 HI) are recomputed from scratch for S = {7}, {13} (Sm empty).
"""
import math
from fractions import Fraction as F
T13 = F(18, 13)
def E(S): return math.prod(1 / (1 - t ** -0.5) for t in S)
def corr(B, S, k, fac=1.0):
    u = B ** -0.5
    return (B / (B - 1)) ** k * math.exp(fac * (1 + 1 / (math.sqrt(B) - 1)) * E(S) * ((1 - u) ** -k - 1))
def thr(S, m, k, fac=1.0):
    lo, hi = 2.0, 1e30
    while hi / lo > 1.00001:
        mid = math.sqrt(lo * hi)
        if corr(mid, S, k, fac) <= m: hi = mid
        else: lo = mid
    return hi
# margins from scratch: {7}: roles o (57/49) or n (geom 7,4); 's' impossible (7 != 1 mod 12); Sm({7}) = {} (x=2 <5, x=18 composite)
HI7 = max(F(57, 49), F(7, 6)); m7 = float(T13 / HI7)
# {13}: 'o' 183/169 or 'n'; 's' impossible when 7 not in T (13 = -1 mod 7 -> 7 | sigma(13^e), e odd); Sm({13}) = {} (x=3 = 0 mod 3)
HI13 = max(F(183, 169), F(13, 12)); m13 = float(T13 / HI13)
print(f"margin {{7}}  = {m7:.6f}   (repo 1.186813)")
print(f"margin {{13}} = {m13:.6f}   (repo 1.278107)")
rows = [((7,), m7, 4, 1751), ((13,), m13, 4, 712), ((7, 13), 1.095520, 3, 5970), ((7, 13, 19), 1.036272, 2, 27723)]
for S, m, k, rep in rows:
    print(f"S={list(S)} k={k}: B (no 1.01) = {thr(S, m, k):9.1f}   B (with 1.01, as coded) = {thr(S, m, k, 1.01):9.1f}   repo {rep}"
          f"   | k=1 (the 14d error) {thr(S, m, 1, 1.01):8.1f}")
