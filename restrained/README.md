# Scripts for the Ochem–Zelinsky restrained framework

Standard library only. Findings in `../NOTES_RESTRAINED.md`.

| script | establishes |
|---|---|
| `01_notable_component_mod12.py` | Lemma A — every prime factor of `σ(3^q)` is `≡ ±1 mod 12` — with verification for even `q ≤ 32` and an odd-`q` control; Corollary B |
| `02_verify_sections_3_and_4.py` | recomputes all five §3 abundancy bounds (all match) and the §4 final product (does not reproduce; conclusion unaffected) |
| `03_question10_search.py` | collision search for their Question 10; run at 200000 and 1000000 |
| `04_question10_p3_excluded.py` | Question 10 has no solution with `p = 3`; root structure mod `p²` |

`q10_1e6.txt` is the output of the `x < 10⁶` run.
| `05_loopless_overflow.py` | audit of `loopless.cpp`: `r*r` wraps modulo 2^64 past `r = 2^32`, with a demonstration that the sieve verdict flips |
| `06_verify_3p2.py` | mechanical verification of all 385 factorisations asserted in `3p2.txt` (382 exact) |

`3p2.txt` here is the transcription supplied to this session, not a copy of the
authors' file; it is kept only so `06` is reproducible.
| `07_verify_3p2_markers.py` | second pass over `3p2.txt`: checks every `F t` / `XS t` marker prime actually divides the line's target (239/241) |
| `08_repair_59083_branch.py` | closes the one broken cut by `XS 3` instead of `F 19`, so the file's conclusion stands |
