# Run logs

Main result
* `extend_11_219.txt` — case C: every (11,7) orbit with Abar ≤ 219 (1 orbit, τ = 8).
* `caseA_11_223_tau0.txt` — case A: Abar ≤ 223, τ = 0 → 0 survivors.
* `caseB_11_221_tau1.txt` — case B: Abar ≤ 221, τ ≤ 1 → 0 survivors.
* `plain_9_142_lookahead_saved.txt` — complete list of 9-orbits with Abar ≤ 142 (input to case C and A*(10)).
* `extend_10_178.txt` — A*(10) = 178 (267 orbits, none below).
* `minantisum_upto6.txt`, `minantisum_upto9.txt` — A*(2..8).

Second canonical form (vertex indices relabelled, seed 987654321): `relabel_*`
(identical orbit counts everywhere; `relabel_219_recanon.txt` maps the
relabelled 219 representative back to the stated one).

Self-checks and cross-checks
* `selfcheck_output.txt` — checks 1, 2, 3, 6a, 7 and solver cross-checks.
* `equivariance.txt` — exhaustive G-equivariance of the FORCED/POSS masks.
* `pttable_check.txt` — PT lookup table vs direct test on 2,000,000 quads.
* `python_selftest_output.txt`, `python_quads_check.txt` — independent Python implementation.
* `run_7_7.txt` — (7,7): 13,448 orbits at 79, min t = 10, nothing below 81.
* `run_9_7.txt` — (9,7) without τ pruning: 82 / 2,711,216 orbits at 140 / 142, nothing below 144.
* `full_7_81.txt` — all 25.8M (7,7) orbits with Abar ≤ 81, τ for each.
* `enumtau_*`, `enumtau2_*`, `stream_7_81.txt`, `augment_*`, `core_7_81.txt` — τ-pruned
  variants reproducing the unpruned survivor sets at (7,7) and (9,7).
* `check_augment_9_142.txt` — explains intermediate-count differences of canonical augmentation.
* `trace_zarankiewicz_225.txt`, `posA_11_225_tau0_augment.txt` — positive controls at top 225.

Aborted runs (kept for the record; none is part of the argument)
* `plain_11_219_aborted.txt` — unpruned (11,7) at T = 219 (level sizes too large; replaced by case C).
* `enumtau_11_223_aborted_weak_astar.txt` — τ search with the weak derived bound A*(11) ≥ 214.
* `main_11_223_tau2_aborted_at_level8.txt` — τ ≤ 2 search (memory; replaced by cases A+B+C).
* `enumtau_9_148_ab142.txt` — a validation run stopped because it barely pruned.
* `posA_11_225_tau0_aborted_oom.txt`, `posA_11_225_tau0_stream_aborted_memory.txt` — memory.
* `METHOD_draft.md` — early draft of the method notes, superseded by ../README.md.
