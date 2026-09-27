#!/usr/bin/env python3
"""
Audit Part A2: the per-term inequality behind corr_k (s3k2/34, s3k2/36).

For x in Sm(T) \\ Sm(S), M = x^2+x+1 >= B.  corr_k needs
        log(1 + 1/x + 1/x^2)  <=  1.01 * (1 + 1/(sqrt(B)-1)) * M^(-1/2).
Since (1 + 1/(sqrt(B)-1)) >= (1 + 1/(sqrt(M)-1)) for M >= B, it suffices that
        g(x) := log(1+1/x+1/x^2) * (sqrt(M) - 1)  <=  1.01          (*)
The docstring's route (1/x < (1+1/(sqrt B-1)) M^-1/2, then "1.01" for the 1/x^2
term) is only complete when 1/x <= 0.01; (*) is what actually holds.  We check
(*) exactly-enough for 2 <= x <= 10^6 with floats, and prove it for x >= 10^6:
log(1+1/x+1/x^2) <= 1/x + 1/x^2 and sqrt(M) - 1 <= x - 1/2 + 3/(8x), so
g(x) <= (1/x + 1/x^2)(x - 1/2 + 3/(8x)) = 1 + 1/(2x) + O(1/x^2) < 1.01 for x >= 100.
"""
import math
worst = (0, 0)
for x in range(2, 10**6):
    M = x * x + x + 1
    g = math.log1p(1 / x + 1 / (x * x)) * (math.sqrt(M) - 1)
    if g > worst[0]: worst = (g, x)
print(f"max over 2 <= x < 10^6 of log(1+1/x+1/x^2)*(sqrt(M)-1) = {worst[0]:.6f} at x = {worst[1]}")
x = 100
bound = (1 / x + 1 / x**2) * (x - 0.5 + 3 / (8 * x))
print(f"analytic bound at x = 100 (decreasing in x): {bound:.6f}")
assert worst[0] <= 1.01 and bound <= 1.01
# the docstring's own route needs 1 + 1/x <= 1.01, i.e. x >= 100, i.e. M >= 10101
print("docstring route (1/x + 1/x^2 <= 1.01/x) needs x >= 100; thresholds B below ~10^4 rely on (*) instead")
print("(*) HOLDS: corr_k's factor 1.01 is valid for every B >= 7")
