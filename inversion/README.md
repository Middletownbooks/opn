# Inversion scripts

Standard library only, tested on Python 3.11.15. Findings in
`../NOTES_INVERSION.md`.

| script | establishes |
|---|---|
| `01_first_input_classification.py` | Theorem 1 — the complete first-input classification for every odd `q` (`3·d(μ)` children), checked against the paper's Table 2 for `q = 5,7,11,13,17` |
| `02_avoidance_and_order_collision.py` | brute-force re-verification of the paper's Lemma 3.2; Theorem 2, Corollary 2a (Euler residue restriction) with density table; Lemma OC; the `L(q)` endpoint table |
| `03_where_the_inversion_bites.py` | Negative Result 1 (abundancy + cardinality force no prime); Proposition D (OC never blocks a non-Euler production); the `A(d,ℓ)` admissible-density table for `q = 17` |
| `04_fermat_prime_forcing.py` | Proposition E — Fermat-prime forcing without the minimal-prime hypothesis; `L(F)`; LTE spot-check |

`03` takes a couple of minutes (it sums `1/p` over primes past 10⁶).

| `05_verify_zelinsky_lp.py` | independent check of Zelinsky (arXiv:1706.07009v3) Theorem 1, both cases, by reconstructing the stated linear combinations symbolically |
| `06_exponent_floors_in_branch.py` | Corollary 2e — residue-dependent forced lower bounds on `e_p` in the branch `q = 17` |
