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
| `07_verify_ochem_zelinsky.py` | independent check of Ochem–Zelinsky (arXiv:2607.19746v1) Section 2: recomputes `A₁, A₂, A₃, A_∞` and their product; discusses why their envelope escapes the audit's Proposition A |
| `08_factor_tree_transfer.py` | the three contradiction rules behind Ochem–Zelinsky's factor-tree prover, the correction to Proposition D, why `Forb(17) = ∅`, and why the tree does not transfer to a general minimal-prime branch |
| `09_theorem1_prime_unrestricted.py` | Theorem 1' — the input classification at every prime divisor, the production width `w(r)`, and the honest ceiling on Proposition E |
| `10_k0_vs_norton.py` | settles the novelty question on `k₀(q)`: it reproduces Norton's bounds exactly at `q = 7, 11`, so it is a reconstruction, not a new result |
