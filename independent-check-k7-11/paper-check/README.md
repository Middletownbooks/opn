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
