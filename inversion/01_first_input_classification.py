#!/usr/bin/env python3
"""
THEOREM 1 (complete first-input classification, all odd primes q).

Let N be odd perfect, S = {p : p | N}, q = min S, N = pi^alpha * m^2 with
pi = alpha = 1 mod 4 the Euler prime.  For p in S put n_p = e_p + 1.
Write  q - 1 = 2^a * mu   with mu odd  (a >= 1 since q is odd).

Then a q-input witness exists, and

  (i)  if the witness p is non-Euler, ord_q(p) divides mu;
  (ii) if the witness is pi, ord_q(pi) divides 2*mu.

Hence the first-input coverage split has exactly d(mu) non-Euler children N_d
(d | mu) and d(2mu) = 2 d(mu) Euler children E_d (d | 2mu):

        number of first-input children  =  3 * d(mu).

PROOF.
Existence: q in S so e_q > 0, and the q-adic valuation balance
e_q = sum_{p != q} v_q(sigma(p^{e_p})) is a sum of nonnegative integers that is
positive, so some term is positive.  (Paper's Lemma 5.2.)

Let p be a q-input witness, d = ord_q(p).  The cyclotomic input condition
(paper's Lemma 3.2) gives v_q(sigma(p^{e_p})) > 0 iff  d | n_p  when d > 1, or
q | n_p when d = 1.  In either case d | n_p, and always d | q - 1 by Fermat.

(i) p non-Euler => e_p even (Euler form) => n_p odd => every divisor of n_p is
odd => d is odd.  An odd divisor of q - 1 = 2^a mu divides mu.
(ii) p = pi => e_p = alpha = 1 mod 4 => n_p = alpha + 1 = 2 mod 4 =>
v_2(n_p) = 1 => v_2(d) <= 1 for any d | n_p.  A divisor of 2^a mu with
v_2 <= 1 divides 2 mu.
Counting: mu odd, so d(2mu) = 2 d(mu).  QED

This answers the item the paper leaves open ("The residual branch q >= 19
requires a separate treatment of the possible first q-adic input orders").
Below the theorem is checked against the paper's own Table 2 for q = 5..17.
"""
def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True
def divisors(n):
    return sorted(d for d in range(1, n+1) if n % d == 0)
def oddpart(n):
    while n % 2 == 0: n //= 2
    return n

# The paper's Table 2 (First-input coverage labels), transcribed.
PAPER = {
  5:  (['N1'], ['E1','E2']),
  7:  (['N1','N3'], ['E1','E2','E3','E6']),
  11: (['N1','N5'], ['E1','E2','E5','E10']),
  13: (['N1','N3'], ['E1','E2','E3','E6']),
  17: (['N1'], ['E1','E2']),
}
print(__doc__)
print(f"{'q':>4} {'q-1':>6} {'mu':>5} {'non-Euler N_d':>26} {'Euler E_d':>34} {'#':>3} {'paper':>7}")
ok = True
for q in [p for p in range(3, 60) if isprime(p)]:
    mu = oddpart(q-1)
    N = divisors(mu)
    E = divisors(2*mu)
    tot = len(N) + len(E)
    assert tot == 3*len(divisors(mu)), q
    mine = (['N%d'%d for d in N], ['E%d'%d for d in E])
    flag = ''
    if q in PAPER:
        match = (mine[0] == PAPER[q][0] and mine[1] == PAPER[q][1])
        flag = 'MATCH' if match else 'MISMATCH'
        ok &= match
    print(f"{q:>4} {q-1:>6} {mu:>5} {','.join(mine[0]):>26} {','.join(mine[1]):>34} {tot:>3} {flag:>7}")
print()
print("All five of the paper's branches reproduced exactly:", ok)
print()
print("Predictions for the open residual branch q >= 19:")
for q in [19,23,29,31,37,41,43,47,53]:
    mu = oddpart(q-1)
    print(f"  q={q:>3}: mu={mu:>3}, {3*len(divisors(mu)):>2} first-input children "
          f"(N_d for d|{mu}, E_d for d|{2*mu})")
