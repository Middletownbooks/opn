# Kickoff prompt — odd perfect numbers, `k = 2` continuation

Paste this as the first message. The repository is
`middletownbooks/opn`, branch `claude/odd-perfect-number-audit-h2mlf9`.
`README.md` is the entry point and states the mathematical position; everything
below is what is **not** in the repo.

---

## What this is

Two connected pieces of work: an audit of Mantovanelli (arXiv:2607.04365), and a
continuation of Ochem–Zelinsky (arXiv:2607.19746) from their `k = 1`
(*restrained*) case to `k = 2`. Read `README.md` first — it has a status table,
the definitions, every remaining assumption in one place, and a ranked resume
list at the bottom. Do not re-derive anything it records as settled.

## Ground rules that produced the results so far

These came from the original research brief and have been load-bearing. Keep
them.

* **No invented mathematics.** Every claim is either proved in the notes, cited
  to a named paper, or verified computationally with the script named. If you
  assert something, say which of the three it is.
* **No literature laundering.** Do not attribute a result to the literature
  unless it is cited in the repo or the user supplies it. One real error in this
  project was claiming the `k₀(q)` support floors as new when they reconstruct
  Norton's bounds — check before claiming novelty, especially against Norton,
  Nielsen, Iannucci, Goto–Ohno, Cohen.
* **Distinguish unconditional from conditional, always, in the tally.** The
  notes keep separate counts for "eliminated with no unproved input" and
  "eliminated assuming `Sm(T)` complete". That separation is the main reason the
  work is trustworthy. Preserve it in anything new.
* **A negative result is a good outcome.** "This cannot be closed this way, and
  here is the obstruction" has been worth more than several partial advances.
  Say so plainly rather than manufacturing a weak bound.
* **Report failures.** `NOTES_RESTRAINED.md` records an attempt that failed and
  why, so it is not repeated. Do likewise.

## Environment facts

* **No computer algebra system.** No PARI/`gp`, no Magma, no Sage, and **no
  sympy** — the container has bare CPython. Every script in the repo is
  standard-library only, deliberately, so it runs anywhere. Keep that.
* The **highest-value open item needs a CAS** (an exact Thue–Mahler solve; see
  `README.md`). You cannot do it here. Do not fake it with a bounded search and
  call it settled — bounded searches are fine, but the bound must be stated.
* **Long sweeps:** several scripts in `s3k2/` run 10–40 minutes. Launch them
  with `nohup … &` and poll the output file; do not block.
* **The container gets reclaimed.** Commit and push early and often. Everything
  worth keeping must be on the remote, not the disk.
* **Never use `pkill -f <scriptname>`.** The pattern matches the shell's own
  command line and kills your session (exit 144). This happened three times.
  Use the PID from `pgrep` instead.
* Scripts that factor large numbers by trial division will hang. Prefer
  *stripping* a known prime set (divide out repeatedly, check the residue is 1)
  over factoring; prefer modular arithmetic over big-integer `σ`; prefer
  "is `4M − 3` a perfect square" over searching for `x`.

## What the user can supply that you cannot fetch

* **Full transcripts of arXiv papers**, or answers from another model to a
  specific query about a named arXiv URL. Ask if you need a source. The
  Ochem–Zelinsky and Zelinsky papers arrived this way, as did their C++ sources
  (`all.cpp`, `tree.cpp`, `loopless.cpp`) and data files.
* **A frontier reasoning model, no tools,** which the user will relay a
  self-contained brief to. Two briefs went out and both produced real results:
  `PROMPT_S_UNIT_BOUND.md` (closed `k = 2`, `3 ∤ N`) and
  `PROMPT_S4_K2_SPECIAL.md` (bounded the `m` leak). Read both before writing a
  third — the shape that works is: setting, verified facts marked as given,
  one sharp question, leads flagged as unpursued, and an explicit statement that
  a negative answer is acceptable. Both returned corrections to errors in my own
  briefs, so audit what comes back rather than accepting it.

## Errors made in this project, so you do not repeat them

Each was caught and corrected; the pattern matters more than the instance.

1. **Double-counted a prime across two roles.** I minimised an abundancy class
   using `n₂ = 5` while still crediting the ordinary prime 5 in the same
   product. If a prime takes a non-ordinary role, remove it from the ordinary
   count. The reasoning model caught this.
2. **Read theorem numbers off `\label` order** instead of compiled numbering,
   and mis-cited five results. Check against the compiled document.
3. **Asserted a hand-wavy lead.** I wrote that `p ≡ 5 (mod 12)` makes the odd
   part of `p−1` congruent to `1 (mod 3)` (false: `p = 41`), and that
   `p = 2·3^m − 1` bounds `ord_p(3)` by `2m` "-ish" (false: `p = 17` gives 16).
   The "-ish" was doing work the claim could not support. Don't ship a lead you
   haven't checked, even labelled as a lead.
4. **Dropped a branch by assuming it could not fit.** In the `τ = 3` closure
   enumeration I discarded `a₂ = 61` on the grounds that `F(61) = {13, 97}`
   wouldn't fit a 3-element `T` — but `97` *was* the third slot, and that branch
   held the profile's only surviving `T`. Enumerate; don't reason away a case.
5. **Got tree semantics backwards**, returning early when a notable slot was
   available, so whole branches went unexplored. The fix reproduced
   Ochem–Zelinsky's set exactly, which is how I knew it was right — **find a
   published value your code should reproduce, and reproduce it, before trusting
   the code on new input.**
6. **Wrote an enumeration that could never finish** (~10⁹ subsets) and let it
   run. Estimate the count before launching.

## Where to pick up

`README.md` ends with a ranked resume list. In one line each:

1. The five named Thue–Mahler statements and the four search bounds in
   `NOTES_S3_K2.md` §13d — blocked here for want of a CAS.
2. The seven remaining pool restrictions (`NOTES_S3_K2.md` §13c) — **not
   blocked**, just not done; needs either a `max(T)` cutoff for the counting
   test or an abundancy recursion for the `|W| ≥ 1` profiles.
3. `3` notable at `k = 2` — genuinely open, as it is at `k = 1`. Do **not**
   attempt to close it outright: Ochem–Zelinsky's Theorem 1 reduces the `k = 1`
   case to `q ≥ 2.3·10¹⁰` rather than eliminating it, so closing `k = 2` would
   exceed the published state of the art. The tractable sub-case is
   `p ≡ 5 (mod 12)` with `p^e ‖ σ(n₂^{q₂})`; the hard branch inside it is
   `f = ord_p(n₂) > 1` with `p ∤ q₂+1`.

Start by telling me which of these you intend to work on and why, before
writing code.

## Working conventions

* Commit to `claude/odd-perfect-number-audit-h2mlf9` and push with
  `git push -u origin claude/odd-perfect-number-audit-h2mlf9`. Do not open a
  pull request unless asked.
* One notes file per section (`NOTES_S3_K2.md`, `NOTES_S4_K2.md`, …), scripts
  numbered in the matching directory (`s3k2/`, `s4k2/`), and every claim in the
  notes pointing at the script that checks it.
* Update `README.md` when a status changes. It is the only file anyone reads
  first, and it is the only place the assumptions are collected.
