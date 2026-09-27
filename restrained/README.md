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
