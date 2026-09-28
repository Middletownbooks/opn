# Recovered sources supplied by the user

*(This file describes only the eight files listed below. The `matveev1998_*.png`
page images in this directory come from other work on the branch and are not
covered here.)*

These are **not my work** and **not from the repository's own history**. The first seven were
pasted into the chat by the user during the original session, summarised out of
my context when it was compacted, and recovered afterwards from the session
transcript. They are the artefacts accompanying Ochem & Zelinsky,
arXiv:2607.19746, plus one algorithm slice from the paper itself.

| file | what it is | provenance |
|---|---|---|
| `loopless.cpp` | the authors' implementation of their **Algorithm 1**, the sieve that yields `z = 216 171 986 291` | **the original file, copied by the user from the authors' page (lirmm.fr/~ochem/opn/restrained/) and attached on 2026-09-27** (replaces the recovered paste, which is whitespace-identical to it) |
| `ochem_zelinsky_algorithm1.txt` | **Algorithm 1** pseudocode, verbatim slice of the paper transcript | user paste of the arXiv transcript |
| `all.cpp` | the §2 abundancy product computation | user paste |
| `tree.cpp` | the factor-tree search, with `checkfacts.txt` injection | user paste |
| `pairs.py` | the pair search accompanying their Question 10 | user paste |
| `checkfacts.txt` | the factorisation database `tree.cpp` reads | user paste |
| `3p2.txt` | the "3 ordinary" marker file verified in `restrained/06`–`07` | user paste |
| `ochem_zelinsky_2607.19746_transcript.txt` | **full text of the paper** (PDF text extraction) | user paste, 2026-09-27, saved directly (not recovered) |

## Read this before trusting the layout

Every paste arrived as a **single line** — the chat transport stripped the
newlines. I reinserted line breaks **mechanically**, at `;`, `{` and `}`, so:

* the **token sequence is verbatim** and the files are semantically what the
  authors wrote;
* the **indentation and line breaks are mine**, not theirs;
* **comments have been mangled** wherever a `//` comment ran into following code
  on the reconstructed line — `//` now swallows the rest of its line. Several
  header comments in `tree.cpp` and `loopless.cpp` show this. Before compiling,
  re-break those comment lines by hand, or fetch the originals from the authors'
  site, which the paper gives as `https://www.lirmm.fr/~ochem/opn/restrained/`
  (blocked by this environment's network policy as of 2026-09-27).

The data files (`checkfacts.txt`, `3p2.txt`) are whitespace-separated records and
survive this intact. `loopless.cpp` has since been replaced by the original
file, so it is exempt from this caveat.

**`tree.txt` is not here and is not needed to transfer.** It backs the paper's
"every prime from 11 up to 3,000,000 is ruled out", which is the input
assumption of Algorithm 1. It is too large to paste, and it can be regenerated
here from `tree.cpp` and `checkfacts.txt` if that step is ever checked.

## What has already been checked against them

* `restrained/05_loopless_overflow.py` — audit of `loopless.cpp`: `r*r` wraps
  modulo `2^64` past `r = 2^32`, and a demonstration that the sieve verdict
  flips. See `NOTES_RESTRAINED.md` §4b. The published `z` exceeds `2^32`, so a
  different build was probably run than the one released.
* `restrained/06`–`07` — verification of `3p2.txt`: 382 of 385 lines verify
  exactly; the three failures and their resolution are in `NOTES_RESTRAINED.md`.
* `NOTES_RESTRAINED.md` §1 — reproduction of the paper's §2 and §3 numbers,
  which match; the §4 constant does not reproduce, and both candidate constants
  are recorded there.

## Note on Algorithm 1 and the §4 gap

`Algorithm 1`'s test at line 6 is whether `F(σ(r²)) ∩ M₂ = ∅` — whether `r` *can*
be ordinary — and my note at `NOTES_RESTRAINED.md` §4 (near the end) records that
this does not fit the interpretation needed to reproduce the published product.
That mismatch, the non-reproducing constant, and the overflow are three separate
observations about the same section; none of them is claimed to invalidate the
paper's conclusion, and `NOTES_RESTRAINED.md` says exactly what each does and
does not show.
