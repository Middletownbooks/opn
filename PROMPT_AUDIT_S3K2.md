# Audit brief: §3 at `k = 2` (the prime 3 ordinary), `NOTES_S3_K2.md` §14

Paste this into a **fresh** session on branch
`claude/odd-perfect-number-audit-h2mlf9` of `middletownbooks/opn`. You are
auditing another session's work. **Your value comes from being independent of
it.** Do not trust the notes' reasoning. Treat every claim below as a
hypothesis to confirm or refute.

---

## 1. What is claimed

`N` is an odd perfect number, `σ(N) = 2N`. It is **2-restrained**: exactly two
exponents are even and `≥ 4` (the **notable** components); one component `p^e`
has `p ≡ e ≡ 1 (mod 4)` (the **special** prime); every other component is `x²`
(**ordinary**). Assume **3 is ordinary**, so `3² ‖ N`. Definitions are in
`README.md` ("Definitions used throughout") and `NOTES_S3_K2.md` §§1–2.

> **Claim.** No such `N` exists. The only inputs are:
> (i) `ω(N) ≥ 10` (Nielsen 2015), and
> (ii) Theorem 2.2 of Matveev 1998, transcribed in `MATVEEV_1998.md` from the
> page images in `sources/`.

The argument splits into **14 role profiles**, indexed by
`(α, special in T, #notables in T, τ, |W|)`. Every profile is killed by some
combination of:

* an abundancy identity with interval narrowing;
* a `max(T)` cutoff recursion;
* a closure condition;
* valuation caps;
* a count `|U| ≥ 6 − α`;
* exact solutions of `x² + x + 1 = 3^δ ∏ t^{c_t}`.

Ten profiles use only (i). Four also use (ii) via `s3k2/39`.

The user is checking `MATVEEV_1998.md` against `sources/` line by line. **Do not
spend effort on the transcription itself.** Do audit how the theorem is
**applied**.

## 2. Ground rules

* **Say what each claim rests on:** proved in your write-up, cited to a named
  source in the repo, or verified by a script you name. Do not attribute results
  to the literature unless the repo cites them.
* **Keep unconditional and conditional separate** in anything you report.
* **A negative finding is a good outcome.** "This step is invalid, here is a
  counterexample or the failing case" is the most valuable thing you can
  produce. Do not soften it.
* **Report what you could not verify,** separately from what you verified.
* **Environment.** Bare CPython: no sympy, PARI, Sage or Magma, and all scripts
  are standard-library only. Keep yours that way.
  * Launch runs longer than a few minutes with `nohup … &` and poll the output
    file.
  * **Never run `pkill -f <scriptname>`**: the pattern matches your own shell
    and kills the session. Kill by PID.
  * Estimate an enumeration's size before launching it.
  * The container can be reclaimed at any time, so commit and push early.
* **Output.** Write `AUDIT_S3K2_RESULT.md`, plus any scripts, under `audit_s3k2/`.
  Only **add** files; do not edit the existing notes or scripts. Push to this
  branch.

## 3. The failure pattern to hunt

The session that produced §14 found **three** errors in earlier or its own
work. All three had the same shape:

1. The `max(T)` cutoff lemma was proved for **one** prime above `S`, but applied
   at levels where up to four remain (§14d).
2. A set was called "killed by the pool sweep" without saying whether that kill
   was **conditional** (§14f).
3. A lower bound valid for `S` was implicitly treated as valid for **every
   superset** of `S`, and vice versa: the *narrowed* `LO` is not valid for
   supersets, while the *raw* role minimum is (§14e).

**For every kill in the chain, state the exact inequality used, and check that
it is valid for everything it is applied to.** In particular, check validity
for supersets, for other role assignments, and for other `W` configurations.

## 4. Tasks, in order

### Part A — re-derive before reading the code

Do these from the definitions alone. Compare with the repo only afterwards.

**A1. Profiles.** From the 3-budget (`NOTES_S3_K2.md` §1, which you should
re-derive) and the definitions of `T`, `W`, `U`, `α`, `β`:

* enumerate all role profiles for `k = 2`;
* derive `ω(N) = 4 + α + |U|` and the requirement `|U| ≥ 6 − α`.

Is the list of 14 in §13c complete? Are any excluded wrongly?

**A2. The cutoff lemma for `k` remaining primes.** State and prove the bound
used in `s3k2/34` (`corr_k`).

* Is `LO(S) ≤ LO(T)` for `T ⊇ S` legitimate?
* Which `LO`: raw, or narrowed?
* Is interval narrowing on `S` legitimate when `T ⊋ S`?

**A3. Matveev's application.** Using only `sources/matveev1998_p8{2,5,6,7}.png`,
derive the exponent bound for `x² + x + 1 = 3^δ ∏_{t∈T} t^{c_t}` over `ℚ(ω)`.
Check each of these independently:

* the linear form, and `Λ ≠ 0`;
* `|Λ| ≤ 2√3/|z|`, and the range where it holds;
* the Kummer condition for `ζ₆` and the `π_t/π̄_t`. Its definition, (1.5), is
  on `sources/matveev1998_p82.png`;
* `D = 1` and `ρ = 1`;
* `h(π_t/π̄_t) = ½ log t`;
* that the choices `ϑ = 1`, `E = 1`, `C₃ = n/ρ` satisfy (2.1)–(2.3);
* the bound on `|b₀|`;
* the handling of `b_n ≠ 0`.

Compute the initial bound for `T = {7, 13, 19}` yourself. The repo's value is
`H ≤ 2.42·10¹²`.

**A4. An independent solver.** Write your own complete solver for
`x² + x + 1 = ∏_{t∈T} t^{c_t}` using a **different reduction**. Two options:

* Baker–Davenport or continued fractions on a single linear form, if you can
  arrange one;
* a lattice built differently from `s3k2/39`'s.

Run it on these sets and compare with the repo's complete lists:

| `T` | repo's complete list (`x ≥ 0`) |
|---|---|
| `{7, 13}` | `0, 2, 3, 9, 18` |
| `{7, 13, 19, 127}` | — |
| `{7, 13, 19, 31, 127}` | — |

For the second and third sets, run `s3k2/39_baker_lll.py residual` to obtain the
repo's lists.

### Part B — adversarial code review

For each script, list its claims and whether each holds.

* **`s3k2/39_baker_lll.py`**
  * The lattice argument in the docstring: `S`, `T₀`, and `min|b*_i|` as a lower
    bound for the shortest vector.
  * The determinant check.
  * The iteration.
  * Exhaustiveness of the final search, including the `L ≥ ln 12` edge.
* **`s3k2/32_skolem.py`**
  * Strassmann's bound as applied.
  * The claim `Λ ≡ X (mod ℓ²)`.
  * The valuation of the higher coefficients for `ℓ ≥ 5`.
  * The logic by which a class is "settled".
* **`s3k2/31_coupled_vieta.py`**
  * The Vieta-jumping classification.
  * The ratio lemma.
* **`s3k2/33`**
  * The valuation caps (`e_a = 2` for an ordinary `a`).
  * Which contributions are counted.
* **`s3k2/36_profile_recursion.py`** — the highest-risk script.
  * `W` configurations: the explicit `w < 500`, the generic `w ≥ 500`, and the
    special `w` split into `e = 1` and `e ≥ 5`.
  * The 3-budget relaxation.
  * The `admissible()` forced-prime filter. Is it valid given `MIN = min(T)`?
  * `closure_ok` and `forced_ok` under the "unknowns exceed `max(S)`"
    semantics.
  * The rule "the element after 7 is 13".
  * The raw-minimum kill.
  * `last_candidates`: are its three cases exhaustive? Is the "exact" Case-B
    enumeration to `B²` sound?
  * The final test.
  * About 485 000 of the level-5 sets die by **"no admissible role assignment"**.
    Check that those filters are necessary conditions, not heuristics.
* **`s3k2/38_closure_dfs.py`**
  * Exhaustiveness of the DFS: pinning, the cutoff branch, the `lb` semantics,
    and Case B.
  * That nothing unresolved is silently dropped.
* **`s3k2/40_coupled_count.py`**
  * The count argument.
  * Does it cover every coupled branch the DFS can reach?
* **Pre-§14 ingredients the result still rests on.**
  * The tail lemma (§5b).
  * Interval narrowing (§5⅔).
  * The closure filter (§9).
  * The role minima, including `p ≡ 1 (mod 12)` for a special prime in `T`, and
    `p ≡ 5 (mod 12)` when it is in `W`.

### Part C — mutation tests

Each change below should make some check fail or some profile survive. Confirm
that one does, and report any mutation that goes unnoticed.

* Replace `corr_k` by `corr_1` in `s3k2/36`.
* Use the narrowed `LO` for the raw-minimum kill.
* Perturb one `θ_t` in `s3k2/39` by `10⁻³⁰`.
* Drop one role split in `last_candidates`.
* Change the Matveev constant `112` to `11.2`.

Some of these may be silent for legitimate reasons. Explain which, and why.

### Part D — reproduce the headline numbers

Re-run the scripts and confirm the figures in `NOTES_S3_K2.md` §§14d–14h:

* the level counts;
* the unconditional / conditional / alive tallies per profile;
* the seven `α = 2` residual sets;
* the complete `Sm(T)` lists.

`36 … 2,yes,1,4,1` takes about 37 minutes; everything else runs in minutes.

## 5. Output format (`AUDIT_S3K2_RESULT.md`)

1. **Verdict** in one paragraph: does the claim of §1 stand, stand with
   repairs, or fail?
2. **Findings.** For each finding, give:
   * status: `CONFIRMED` / `ERROR` / `GAP` / `COULD NOT VERIFY`;
   * location (file and line, or notes section);
   * the exact statement;
   * evidence (your proof, counterexample, or script);
   * whether it affects the claim.
3. **Part A comparisons.** Your independently derived values next to the repo's
   values.
4. **Mutation-test table.**
5. **What you did not check,** and why.
