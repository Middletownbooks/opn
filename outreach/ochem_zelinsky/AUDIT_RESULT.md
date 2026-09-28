# Independent audit of the note to Ochem & Zelinsky — IN PROGRESS

Interim record (the full report replaces this file).

* C1 overflow line: confirmed by reading `sources/loopless.cpp:135` and by computing
  `r²+r+1` exactly and mod 2⁶⁴ for the first four primes above 2³².
* C3/C5: the auditor's own Algorithm 1 (`audit/auditor_algorithm1.c`, direct factoring of
  `r²+r+1` and `r+1`, no code shared) gives the identical survivor list to `13` on
  `(3·10⁶, 2·10⁸]` (957,150 survivors) and identical `ln A`. `12` agrees with `13` line
  for line at 2·10⁸. At Z = 2·10⁷ with Q = 4·10⁶ and Q = 10⁷, `13`'s survivors equal the
  auditor's Q-restricted survivors and contain every exact survivor.
* Bug found in `14_bound_from_run.py`: Decimal `//` truncates toward zero, so the
  "round up" rounds down. At z the result is unaffected; at 10¹² the correct bound is
  `q ≥ 120,009,648,968`, not `…966`.
