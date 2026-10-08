# Spot checks of "The crossing number of complete bipartite graphs" (OpenAI, 2026)

Exact-arithmetic (rational and integer) checks of the paper's lower-bound
chain. All pass; the controls fail as they should.

| script | what it checks | result |
|---|---|---|
| `check_rank_detector.py` | Lemma 4.1/4.2: Φ kills row-plus-column and diagonal matrices; Φ(E_pq) has rank 1; Φ(S_≺) is invertible | all 6 / 120 / 5040 orders for n = 3, 5, 7; 300 random orders for n = 9; no failures |
| `check_drawing_chain.py` | the whole chain on straight-line drawings, with J built exactly as in (3.1): Lemma 3.2, R_ik = X_i − Y_k, rank R_ii = d, rank R_ik ≤ c_ik, Σ rank ≥ 2 d_m d_n | holds on 18 random drawings, K_{3,3} … K_{7,7} |
| (same) | Zarankiewicz axis drawings | **tight everywhere**: c(D) = d_m d_n, Σ rank = 2c(D), and rank R_ik = c_ik for every block |
| (same) | control: crossing-sign convention flipped | Lemma 3.2 fails (the test is convention-sensitive) |
| `check_polyline_cycles.py` | Lemma 3.2 on 40 random polyline drawings: 4,326 crossings; 1,160 pairs crossing ≥ 2 times, 952 with cancelling signs; 999 crossing adjacent pairs | holds on all 40 |
| (control) | half-weight vertex terms dropped | Lemma 3.2 fails |

Not checked: Appendix A (normalization); Lemma 3.1 for general curves
beyond polylines with ≤ 2 bends; Lemma 2.1 beyond a line-by-line reading and
its sharp example; the even-n counting step (standard).


# Spot checks of "The crossing number of complete graphs" (OpenAI, 2026)

Exact arithmetic (rationals, or integers modulo the prime 2^61 − 1). All pass;
all controls fail as they should.

| script | what it checks | result |
|---|---|---|
| `kn_order_detector.py` | Lemmas 3.2–3.3: two-triangle interpolation on 2s nodes; the order pairing M is nonsingular on P_{s−1,s−2} × P_{s−2,s−1} | all 24 and all 720 orders for 4 and 6 nodes; 400 and 60 random orders for 8 and 10 nodes; no failures |
| `kn_chain.py` | Section 5: the two-page drawing has exactly Z(n) crossings | n = 5 … 20 |
| (same) | Lemma 4.1 (polynomial cycle identity), Lemma 4.2 (E injective), Prop 4.3 (E(S) isotropic for diag(a)), and \|T\|/2 ≥ dim S, on random straight-line drawings | n = 5, 7, 9, 11 |
| (same) | the same on the paper's two-page optimal drawings | **tight**: c(D) = Z(n), \|T\| = 2Z(n), rank E = \|T\|/2 (the image is maximal isotropic), n = 5 … 13 |
| (same) | Lemma 4.1 on random polyline drawings with repeated, cancelling and adjacent crossings | holds on all 6 |
| (same) | controls: shuffled spoke orders, no half terms, flipped crossing signs | Lemma 4.1 fails for each |

Not checked: Appendix A; Lemma 2.1 for general curves beyond polylines with
≤ 2 bends; the order detector for s ≥ 4 beyond random orders. The even case
is the standard vertex-deletion count.
