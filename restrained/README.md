# Scripts for the Ochem–Zelinsky restrained framework

Standard library only. Findings in `../NOTES_RESTRAINED.md`.

| script | establishes |
|---|---|
| `01_notable_component_mod12.py` | Lemma A — every prime factor of `σ(3^q)` is `≡ ±1 mod 12` — with verification for even `q ≤ 32` and an odd-`q` control; Corollary B |
| `02_verify_sections_3_and_4.py` | recomputes all five §3 abundancy bounds (all match) and the §4 final product (does not reproduce from the text's constants; see `10`) |
| `03_question10_search.py` | collision search for their Question 10; run at 200000 and 1000000 |
| `04_question10_p3_excluded.py` | Question 10 has no solution with `p = 3`; root structure mod `p²` |

`q10_1e6.txt` is the output of the `x < 10⁶` run.
| `05_loopless_overflow.py` | audit of `loopless.cpp`: `r*r` wraps modulo 2^64 past `r = 2^32`, with a demonstration that the sieve verdict flips |
| `06_verify_3p2.py` | mechanical verification of all 385 factorisations asserted in `3p2.txt` (382 exact) |

`3p2.txt` here is the transcription supplied to this session, not a copy of the
authors' file; it is kept only so `06` is reproducible.
| `07_verify_3p2_markers.py` | second pass over `3p2.txt`: checks every `F t` / `XS t` marker prime actually divides the line's target (239/241) |
| `08_repair_59083_branch.py` | closes the one broken cut by `XS 3` instead of `F 19`, so the file's conclusion stands |
| `10_section4_reconcile.py` | §4 reconciled against the full transcript: the printed product is the sieve's `A = 1.088507187872` with `K = 43·10⁹`; with the text's `K = 43.5·10⁹` it is `1.99671 < 2`; `k + K_max = 46,355,827,007`; what a re-run must show |
| `11_wrap_signature.py` | the 64-bit wrap is visible in the paper's reported `k, A`: fitted survival fraction 0.093 below `2³²`, 0.295 above (`≈ √`); and the mechanism measured on sampled primes (exact ≈ 0.11, wrapped ≈ 0.36–0.44) |
| `12_algorithm1_reference.py` | exact bare-CPython Algorithm 1 for small ranges (optional cutoff `Q`); matches the released `loopless.cpp` line for line |
| `13_sieve.c` | the overflow-free re-run of Algorithm 1, C with the standard library only. It is exact for `r < Q`; above `Q` it keeps a provable superset of the survivors (header comment). It matches `12` exactly at `2·10⁸`, both exact and with `Q = 5·10⁷`, and the released `loopless.cpp` on every line compared |
| `14_bound_from_run.py` | turns `13`'s checkpoint lines into `k + K_max` and the resulting `q` bound |
| `loopless_build/gmp.h` | a declaration-only stand-in for the missing `<gmp.h>`, so the authors' `loopless.cpp` compiles **unmodified** against the system `libgmp.so.10` (`g++ -O3 -I loopless_build ../sources/loopless.cpp /usr/lib/x86_64-linux-gnu/libgmp.so.10`) |
| `runs/` | records of the runs: the full `13` run to `z` with `Q = 2³⁵` (checkpoints, stderr, gzipped progress lines), the `14` bound table, the exact `10¹⁰` checkpoints, and one hour of the released `loopless.cpp` |
| `15_tree_pilot.py` | independent re-check of `tree.txt`'s claim, that every prime `11 … 3·10⁶` is ruled out. It uses `tree.cpp`'s method but none of its code, with gcd, Pollard–Brent and pure-Python ECM factoring. `checkfacts.txt` is used only as verified hints, and `NOHINTS=1` ignores it. All 216,812 are ruled out (`runs/15_tree_full_range.txt`) |
| `16_selberg_pilot.py` | pilot, first pass: sanity checks (exact `G` at least `G_low`; sieve bound at least a brute-force count; bound against the true static count) and a crude projection |
| `16b_m2_dump.py` | exact Algorithm-1 `M₂` below `Y`, as a byte map |
| `16c_selberg_tables.c` | `G(ξ)`, `W(ξ)` and the sharper weighted error sum for `ξ < 10⁸`, with `ω = 3` on `M₂` |
| `16d_selberg_projection.py` | loss factors, projections and the sensitivity table (`runs/16d_*`); a qualified negative, `NOTES_RESTRAINED` §4g |
| `16e_tail_heuristic.py` | heuristic: the survivors' abundancy appears to converge (`ln A(∞) ≈ 0.12 < 0.2877`); a proof needs a tail bound within a factor of about 3.1 |
| `16f_bootstrap_pilot.py` | the Selberg bound against the true survivors: about 12.6 times (idealised 8.8), against the 3.1 needed; negative (§4h) |
| `17_lookahead_sample.py` | one-step look-ahead: a survivor whose large factor `P > r` of `r²+r+1` can be neither ordinary nor special is removed. It removes 82.9% of a 3,000-survivor sample in `(5·10⁷, 10⁸]` (`runs/17_*`, §4i) |
| `18_verify_lookahead.py` | independent check of `ideas_tail/05` below `10⁸` by full factorisation: identical counts and `ln A` (§4j) |
