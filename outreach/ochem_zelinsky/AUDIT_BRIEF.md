# Audit brief: the note to Ochem & Zelinsky, and its attachment

Paste this into a **fresh** session on branch
`claude/odd-perfect-number-audit-h2mlf9` of `middletownbooks/opn`. You are
auditing another session's work before a note is sent to the authors of a paper.
**Your value comes from being independent of that session.** Do not trust its
reasoning. Treat every claim as a hypothesis to confirm or refute. Re-run things
rather than reason about them wherever you can.

The person sending the note is neither a mathematician nor a programmer and cannot
check it themselves. **Your report is their only second opinion.** Say plainly
what you confirmed, what you refuted, and what you could not check.

---

## 1. What is being claimed

The paper is P. Ochem and J. Zelinsky, *On odd perfect numbers with exactly one
even exponent greater than 2*, arXiv:2607.19746v1. The full text is in
`sources/ochem_zelinsky_2607.19746_transcript.txt`. Its §4 bounds the notable
exponent: `q ≥ 23·10⁹`. It does so with a sieve (Algorithm 1, run by
`loopless.cpp`), then an abundancy count, then Lemma 8.

The draft note is `outreach/ochem_zelinsky/NOTE_TO_AUTHORS.md`. Its attachment is
built by `outreach/ochem_zelinsky/make_bundle.py`, with
`outreach/ochem_zelinsky/BUNDLE_README.md` as its README. The note claims:

| # | claim | where the other session's work is |
|---|---|---|
| C1 | `loopless.cpp` line 135, `u64 val = r * r + r + 1;`, wraps for `r ≥ 2³²`; `get_factors` takes `u64` | `sources/loopless.cpp`, `restrained/05` |
| C2 | the published `k`, `A` show the wrap's signature: a survival rate of about 9% below `2³²` and about 29% above, which is about the square root | `restrained/11`, `NOTES_RESTRAINED.md` §4b |
| C3 | `restrained/13_sieve.c` implements Algorithm 1 exactly for `r < Q`, and keeps a superset of the survivors above `Q` | header of `13_sieve.c` |
| C4 | `13` agrees with the unmodified `loopless.cpp` on all 253 lines of one hour's output (to `r = 579,733,409`), including `k: 2530000 \| r: 579733409 \| A: 1.028007677068`, and prints `k: 15650000 \| r: 4293066907 \| A: 1.035513576704`; the run to `2³²` takes about 87 s | `restrained/runs/loopless_released_1h.txt` |
| C5 | `13` agrees line for line with `restrained/12_algorithm1_reference.py` at `2·10⁸` | §4d |
| C6 | at `z = 216,171,986,291` with `Q = 2³⁵`: `k = 599,351,328`, `A = 1.047357816316`, `k + K_max = 52,785,706,892`, `q ≥ 26,392,853,446`; the count first passes `46·10⁹` near `1.89·10¹¹` | `restrained/runs/14_bound_z_Q2e35.txt` |
| C7 | the §4 counting argument: survivors that are a superset of the possible ordinary primes below `z` suffice; ordinary primes `≥ k + K_max + 1`; `ω = 2 + ordinary`; Lemma 8 with `q` even gives the `q` bound | `restrained/10`, `restrained/14`, §1a |
| C8 | every prime `11 … 3·10⁶` is ruled out by `tree.cpp`'s method: without `checkfacts.txt`, all but 502013 and 2152883; those two with verified `checkfacts.txt` factors; all 460 entries of `checkfacts.txt` verify | `restrained/15`, `restrained/runs/15_tree_full_range.txt`, §4e |
| C9 | at `z = 10¹²`: `k + K_max = 240,019,297,934`, `q ≥ 120,009,648,966`, taking about 3.8 h | `restrained/runs/14_bound_1e12_Q2e35.txt` |
| C10 | the printed product `1.99209763359616948564` matches `A = 1.088507187872` with `K = 43·10⁹` to about 10 digits; the text's `K = 43.5·10⁹` with that `A` gives `1.99671… < 2` | `restrained/10` |
| C11 | the released `tree.cpp` never terminates (`while (1)`) | `sources/tree.cpp` (reformatted; the layout is not the authors') |
| C12 | the zip contains exactly the repo files listed in `make_bundle.py`, and the README's commands work from an unpacked copy | `make_bundle.py` |

## 2. Ground rules

* Bare CPython with the standard library, plus `gcc`/`g++`. The system has
  `libgmp.so.10` but no GMP headers. To build `loopless.cpp`, use
  `restrained/loopless_build/gmp.h`, and check that it only declares things.
* Run anything over a few minutes with `nohup … &` and poll it. **Never use
  `pkill -f <pattern>` or `pgrep -f` inside a loop whose own command line contains
  the pattern.** It matches your own shell and kills the session. Use explicit PIDs.
* Commit and push early: the container can be reclaimed. Write your report to
  `outreach/ochem_zelinsky/AUDIT_RESULT.md`. **Do not edit the note, the README or
  the programs.** Put proposed changes in your report.
* Estimate cost before launching anything long.

## 3. Tasks

**A. The overflow (C1).** Read `sources/loopless.cpp` yourself. Confirm the line,
its types, and that `get_factors` takes `u64`. For a few primes just above `2³²`,
compute `r² + r + 1` exactly and modulo `2⁶⁴`.

**B. Your own Algorithm 1 (C3, C5).** Write **your own** implementation from the
pseudocode (`sources/ochem_zelinsky_algorithm1.txt`, or §4 of the transcript).
Do not use the other session's code. Direct factoring of `r² + r + 1` is fine for
small ranges. Compare survivors and `A` with `13` and `12` on at least
`(3·10⁶, 2·10⁷]`.
* Then attack the header of `13_sieve.c`. Check the cube-root marking, the claim
  that `r` joins `M₂` iff `r ≡ 3 (mod 4)` or `(r+1)/2` is not a survivor, and the
  superset induction.
* Test the superset claim directly: at a small `Q`, is every exact survivor also a
  survivor of `13`?

**C. Agreement with the authors' program (C4).** Build `loopless.cpp` with the
shim and run it for at least 20 minutes. Compare its lines with `13`'s run to `2³²`.
Confirm the two quoted lines and the 87 s timing, to the right order of magnitude.

**D. The corrected run (C6, C9).** Re-run `./sieve 216171986291 34359738368 0`
(about 55 min, 6 GB) and `14_bound_from_run.py`. Confirm the figures. For C9, it
is enough to check that `14` applied to `restrained/runs/13_1e12_Q2e35_checkpoints.txt`
gives the stated numbers, and that those checkpoints agree with the `z` run up to
`z`. A full re-run of C9 is optional (3.8 h).

**E. The argument (C7).** Using the transcript, check independently that `z`,
`k`, `A` and `K_max` give the stated lower bound on the number of ordinary primes,
and that this gives the `q` bound through Lemma 8. Recompute `K_max` in your own
code. Look hard for off-by-one errors, the direction of each inequality, and
whether a superset of survivors really is safe. Also check what the §4 argument
takes from outside Algorithm 1: `p > 6·10⁶`, `σ₋₁(3^q) < 3/2`, and primes below
`3·10⁶`. Does the note overstate what was checked?

**F. The wrap signature (C2).** Re-run `restrained/11` and check its fit. Is the
note's wording ("nearly the square root", "should fall, not rise") fair?

**G. Primes `11 … 3·10⁶` (C8).**
* Read `15_tree_pilot.py` against `tree.cpp` and the paper. Is the prover sound as
  used: branches, special eligibility, the path/cycle rule, the "factor below
  root" rule, and the handling of 3?
* Re-run a random sample of at least 20,000 roots, plus 502013, 2152883 and the
  15 listed in the run record. Check them with and without `NOHINTS=1`.
* Re-verify all 460 `checkfacts.txt` entries with your own code.
* A full re-run is optional (about 4.5 CPU-hours).

**H. The product (C10) and `tree.cpp` (C11).** Recompute the product. Check the
loop.

**I. The bundle (C12).** Run `make_bundle.py`. Unzip into a fresh directory and
follow `BUNDLE_README.md` §§1, 2, 5 and 7 there, plus the `2·10⁸` comparison.
Confirm that each zipped file is byte-identical to the repo file it names.

**J. The note as a whole.**
* Is every factual sentence supported? Are all numbers exactly as the evidence
  gives them?
* Is anything overstated? Is anything misattributed, or claimed as new?
* Is the tone appropriate for writing to the authors?
* Is the disclosure paragraph accurate?

## 4. Report format

`AUDIT_RESULT.md`:
1. **Verdict per claim C1–C12**: CONFIRMED, REFUTED or NOT CHECKED, with the
   command and output that decided it.
2. **Errors found** in the note, the README or the programs, with exact proposed
   wording or fixes.
3. **Anything the note should add or remove.**
4. **A one-paragraph plain-language summary for the sender:** can the note be
   sent as it stands, with fixes, or not at all?
