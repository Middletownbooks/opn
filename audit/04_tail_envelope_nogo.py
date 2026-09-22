#!/usr/bin/env python3
"""Proposition A (no-go for upper abundancy envelopes) plus exact per-record
quantification over every tail record the released verifiers evaluate."""
import json, os, sys, ast, re
from fractions import Fraction
D = sys.argv[1] if len(sys.argv) > 1 else \
    '/home/user/mantovanelli1110/opn-small-prime-closure-certificates'

def H(t):
    v = Fraction(1)
    for p in t:
        v *= Fraction(p, p - 1)
    return v

def Mmin(K, B):
    """least M with H(K)*(B/(B-1))^M > 2, i.e. least M compatible with sigma(N)=2N"""
    M = 0
    while H(K) * Fraction(B, B - 1) ** M <= 2:
        M += 1
    return M

print(__doc__)
print("PROPOSITION A.  Let N be odd perfect with support S.  Let K_env=(k_1..k_t)")
print("account for t slots of S (each k_i a prime of S or a certified lower bound for")
print("one), let every remaining prime of S be >= B, and let at most M remain.  Then")
print("        H(K_env) * (B/(B-1))^M  >  2.")
print("Proof.  sigma(N)/N = prod_{p in S} (1-p^-(e_p+1))/(1-p^-1) < prod p/(p-1) = H(S),")
print("and sigma(N)/N = 2, so H(S) > 2.  x/(x-1) is decreasing, so each envelope slot")
print("over-estimates its prime's factor and each tail prime contributes at most")
print("B/(B-1); hence H(S) <= H(K_env)(B/(B-1))^M > 2.  QED")
print()
print("COROLLARY B.  The acceptance test H(K_env)(B/(B-1))^M < 2 is unsatisfiable by")
print("data meeting obligations (i)+(ii) of Definition 7.5.  Acceptance and validity")
print("are mutually exclusive, so every accepted tail record asserts something true")
print("only if its branch is already empty.")
print()

# Effective kernel per branch, matching what each released verifier evaluates.
def kernels(q):
    out = []
    for line in open(os.path.join(D, f'q{q}_master_bundle.jsonl')):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if 'B' not in r or 'M' not in r:
            continue
        B, M, rid = r['B'], r['M'], r.get('id', '?')
        if 'forced_kernel' in r:                       # q=7 style
            out.append((rid + ' [forced]', list(r['forced_kernel']), B, M))
        elif 'K_base' in r and 'forced_prime_lower_bound' in r:
            out.append((rid + ' [forced]',
                        list(r['K_base']) + [r['forced_prime_lower_bound']], B, M))
        if 'pure_kernel' in r:
            out.append((rid + ' [pure]', list(r['pure_kernel']), B, M))
    return out

# q=7 forced kernels live in the verifier's expectation table, not the bundle.
q7_forced = {'q7_strict_tail_n1': [7, 29, 29], 'q7_strict_tail_n3': [7, 11, 13],
             'q7_strict_tail_e1': [7, 29, 29], 'q7_strict_tail_e2': [7, 13, 11],
             'q7_strict_tail_e3': [7, 37, 13], 'q7_strict_tail_e6': [7, 17, 13]}

print(f"{'record':<42} {'K_env':>18} {'B':>3} {'M':>4} {'H*(B/(B-1))^M':>14} {'<2':>5} {'honest M_min':>12} {'gap':>5}")
viol = 0
rows = []
for q in (7, 11, 13, 17):
    ks = kernels(q)
    if q == 7:
        ks += [(rid + ' [forced]', K, 59, 18) for rid, K in sorted(q7_forced.items())]
    for rid, K, B, M in sorted(set((a, tuple(b), c, d) for a, b, c, d in ks)):
        K = list(K)
        v = H(K) * Fraction(B, B - 1) ** M
        mm = Mmin(K, B)
        acc = v < 2
        if acc and M < mm:
            viol += 1
        print(f"{rid:<42} {str(K):>18} {B:>3} {M:>4} {float(v):>14.6f} {str(acc):>5} {mm:>12} {M-mm:>+5}")
# q=5 representatives taken from the q=5 verifier's own printed derivations
print()
print("q=5 (representatives from the q=5 verifier's own output):")
for rid, K in [('q5e1_pi_ge_1381_parametric_tail_closure', [5, 1381, 11]),
               ('q5n_p_ge_211_parametric_tail_closure', [5, 211, 11]),
               ('q5e2_pure_c2_equals_2_tail_certificate', [5, 1249])]:
    v = H(K) * Fraction(59, 58) ** 18
    mm = Mmin(K, 59)
    if v < 2 and 18 < mm:
        viol += 1
    print(f"{rid:<42} {str(K):>18} {59:>3} {18:>4} {float(v):>14.6f} {str(v<2):>5} {mm:>12} {18-mm:>+5}")
print()
print(f"records accepted by the verifier whose M is BELOW the minimum sigma(N)=2N permits: {viol}")
print("(Corollary B says this must be all of them.)")
