# Odd perfect numbers: audit and continuation

Working repository for two connected pieces of work:

1. an **audit** of Mantovanelli, *Certified Minimal-Prime Branch Closures for
   Odd Perfect Numbers* (arXiv:2607.04365);
2. a **continuation** of Ochem & Zelinsky, *On odd perfect numbers with exactly
   one even exponent greater than 2* (arXiv:2607.19746), from their `k = 1`
   (*restrained*) case to `k = 2`.

Everything is standard-library Python, no external data. Entry points below.

---

**Start here for `k = 2`:** `K2_WRITEUP.md`, a self-contained account of Theorems A
(`3 ∤ N`) and B (`3² ‖ N`), with their trust base, verification levels and certificates.

## Status in one table

| item | where | status |
|---|---|---|
| Audit of Mantovanelli | `AUDIT_REPORT.md` | **Category C.** Proposition A: acceptance and validity are mutually exclusive for the tail envelope. Decisive, needs no `ω` bound. |
| Verification of Ochem–Zelinsky §§2–3 | `NOTES_RESTRAINED.md` | Reproduces exactly. §4's printed product is reproduced to 10 digits by the sieve's own abundancy with `K = 43·10⁹` (the text says `43.5·10⁹`); with the text's `K` the product is `1.99671 < 2`, so the conclusion follows from the sieve's output (NOTES_RESTRAINED §1a, `restrained/10`). The original `loopless.cpp` wraps past `r = 2³²`, and its reported `k, A` are not Algorithm 1's (§4b). **An overflow-free re-run (`restrained/13`, C) confirms `q ≥ 23·10⁹`** with a margin of `6.79·10⁹` primes. The same method gives `q ≥ 26,392,853,446`. This holds given the rest of their §4 (§4d). `tree.txt`'s claim (every prime `11 … 3·10⁶` ruled out) is also **independently confirmed** (§4e, `restrained/15`). Run on to `z = 10¹²`, the corrected method gives **`q ≥ 120,009,648,966`** (§4f). It is their method, offered to them, not claimed. Their Question 10 has **no solution with `p, r < 1000`**, exact for all exponents and all `x` (§4a). |
| `k = 2`, `3 ∤ N` (their §2) | `NOTES_K2.md`, `AUDIT_K2_MODEL_RESULT.md` | **Closed, with two independent proofs.** A reasoning model's fixed-support bound, audited (my first attempt double-counted the prime 5). And a **certified** proof with the section-3 machinery (`k2/05`–`07`, NOTES_K2 §7) that uses **no cited theorem at all**. |
| `k = 2`, `3` ordinary (their §3) | `NOTES_S3_K2.md` | **All 14 role profiles eliminated.** 5 profiles use no cited theorem, 5 use only `ω(N) ≥ 10` (Nielsen), and 4 use that and Matveev 1998, Thm 2.2 (`MATVEEV_1998.md`). No pool, search bound or Thue–Mahler assumption remains (§14h–i). **Independently audited** (`audit_s3k2/`, §14k): no errors, and three documentation gaps, now repaired. **Independently rebuilt** (`s3k2/41`, §14l) and **certified**: every search tree is verified by a small checker (`s3k2/46`, §14m). Two errors in the earlier recursion were found and corrected (§14d, §14f). |
| `k = 2`, `3` notable (their §4) | `NOTES_S4_K2.md`, `AUDIT_S4K2_MODEL_RESULT.md` | **Open**, as it is at `k = 1`. New structural results below. |
| `q = 3` side-investigation | `NOTES_Q3.md` | A higher-reciprocity obstruction is shown *not to exist* (explicit witness). Avenue closed. |
| Theorem 1 inversion | `NOTES_INVERSION.md` | Theorem 1′, Negative Result 1, and the `k₀(q)` floors — which are a reconstruction of Norton's, not new. |

## Definitions used throughout

`N` odd perfect, `σ(N) = 2N`. Euler form `N = p^e m²`, `p ≡ e ≡ 1 (mod 4)`; `p`
is the **special** prime. `N` is **`k`-restrained** if exactly `k` even exponents
exceed 2; those components are **notable**, and a prime with exponent exactly 2
is **ordinary**. Ochem–Zelinsky's *restrained* is `k = 1`.

---

## `k = 2`, `3` ordinary — the main result

`3² ‖ N`, so `e₃ = 2` exactly. Write `T` for the primes `≡ 1 (mod 3)` dividing
`N`, `α = |A|` for the ordinary ones among them, `W` for the big components
(special, two notables) that are `≡ 2 (mod 3)`, and `U` for the ordinary primes
`≡ 2 (mod 3)`. Then `τ = |T| = α + β`, `|W| = 3 − β`, and the 3-budget gives
`α + [special ∈ W] ≤ 2`. Fourteen profiles.

**Two complementary methods close all fourteen.** They want opposite things,
which is why together they cover the whole range of `τ`:

| | abundancy side | counting side |
|---|---|---|
| wants | `|W| = 0`, large `T` | small `T`, any `|W|` |
| identity | `PROD_T · PROD_W · PROD_U = 18/13` | `ω(N) = 4 + α + |U| ≥ 10` |
| kills when | `LO ≥ HI` after interval narrowing | `\|Sm(T)\| < 6 − α` |
| `Sm(T)` | searched (`10²⁴` at `\|T\|=5`) for the sweep | proved complete where needed (§14b, §14h) |

where `Sm(T) = { x prime, x ≡ 2 (mod 3) : x²+x+1 is T-smooth }`, and `U ⊆ Sm(T)`
because every prime factor of `x²+x+1` is `≡ 1 (mod 3)` and divides `N`.

Three ingredients did the real work:

* **the tail lemma** (`NOTES_S3_K2.md` §5b) — `Σ_{M>Y, T-smooth} M^{−1/2} ≤ Y^{−ε} ∏(1−t^{ε−1/2})^{−1}`,
  which makes `h(T)` a genuine upper bound with no Thue–Mahler input;
* **interval narrowing** (§5⅔) — a lower bound on `PROD_T` caps `PROD_U`, which
  excludes the small members of `Sm(T)` one by one, which raises the lower bound
  again; lifts the unconditional share from 76.7% to 98.3%;
* **the ordinary-closure filter** (§9) — `t ∈ T` ordinary ⟹ `F(t) ⊆ T`, where
  `F(t)` is the set of prime factors of `t²+t+1` that are `≡ 1 (mod 3)`. With
  `|T| = 5` this is severe, and it is what finally made the `max(T)` cutoff
  recursive and removed the pool restriction on the hardest branch.

**`|W| = 3` dies in three lines** with no computation (§11b): `β = 0` makes the
special `≡ 2 (mod 3)`, which spends a 3-budget unit, so `α ≤ 1`; `13 | N` forces
`α = 1` and `T = {13}` with 13 ordinary; then `σ(13²) = 183 = 3·61` puts 61 in
`T`. Contradiction.

### What §14 added

* **Proofs replacing search bounds.**
  * The coupled branch of §13b is empty, by Vieta jumping (§14a, `s3k2/31`).
  * A standard-library Skolem/Strassmann solver settles every
    `x²+x+1 = D·pᶜ` exactly (§14b, `s3k2/32`). It was validated against
    script 26's table and passes a mutation test.
  * Valuation caps (`e_a = 2` for ordinary `a`) reduce the counts to such
    single-exponent equations (§14c). Result: six profiles unconditional.
* **The pool is gone** from the seven remaining profiles (§14e, `s3k2/36`–`38`).
  This takes the `max(T)` recursion to any profile, including a single `W`
  slot, with a closure-driven last level and a closure DFS for exceptions.
  Four more profiles become unconditional.
* **Corrections.**
  * §14d: the recursion of §8 applied a one-prime cutoff lemma where up to
    four primes remain. Corrected (`s3k2/34`, `35`); §10's conclusion
    survives, but was not proved before.
  * §14f: §9a's appeal to "the pool already swept" hid two conditional sets,
    so the `α = 2` branch rests on seven named sets, not five.
* **The residual Thue–Mahler statements are solved** (§14h, `s3k2/39`) by
  Matveev's bound plus lattice reduction. Because `Y = 1`, only archimedean
  logarithms are needed. This is validated against the Skolem solver and
  against direct searches. The coupled branch closes by a valuation count
  (`s3k2/40`).

## `k = 2`, `3` notable — what is established

This is the analogue of their §4, which at `k = 1` is **not closed** — their
Theorem 1 gives `q ≥ 23 000 000 000`, a reduction, not an elimination.

* **The budget identity gains a term**: `q = o₁ + m + i + j` against `k = 1`'s
  `q = o₁ + m + i`, with `j = v₃(q₂+1)` from the second notable.
* **`j` is not free** (`NOTES_S4_K2.md` §2): each unit buys a distinct prime
  divisor of `N`, by Zsigmondy primitive divisors at `d = 3, 9, …, 3^j`. Hence
  `ω(N) ≥ 3 + (q − m − 4)/3`.
* **The leak is `m = v₃(p+1)`**, and tracing it recovered Ochem–Zelinsky's
  Lemma 6 from quadratic reciprocity: `σ(3^q)`'s prime factors are `≡ ±1 (mod 12)`
  because `q` is even, so `ord_r(3) | q+1` is odd and `3` is a QR mod `r`. At
  `k = 1` nothing can then produce a special prime `≡ 5 (mod 12)`. At `k = 2` the
  second notable can, so that case survives and `p^e ‖ σ(n₂^{q₂})` exactly.
* **A reasoning model bounded the leak** (`AUDIT_S4K2_MODEL_RESULT.md`): a
  Nielsen-style descent gives `m ≤ 4·3^{r−3} log₃(8(r−1))` with `r = ω(N)`, hence
  `q ≤ m + 3r − 8`. Audited step by step; sound. Dividend: a `k = 2` analogue of
  `q ≥ 2.3·10¹⁰` would force `ω(N) ≥ 23`.

---

## Everything still assumed

For §3 at `k = 2`, `3` ordinary:

1. **`ω(N) ≥ 10`** (Nielsen 2015). A cited theorem, used by the count test in 9
   of the 14 profiles. The other 5 need no cited theorem at all.
2. **Matveev 1998, Theorem 2.2.** A cited theorem, transcribed with every
   hypothesis checked in `MATVEEV_1998.md`. It is used only in `s3k2/39`, to
   bound the exponents before lattice reduction, for 4 profiles.

Nothing else: **no pool, no search bound, and no Thue–Mahler assumption.** The
fifteen formerly residual sets and every Case-B search are settled exactly
(`NOTES_S3_K2.md` §14h).

**How much weight this carries.** It rests on `s3k2/31`–`40`. An independent
audit (`audit_s3k2/AUDIT_S3K2_RESULT.md`; summary in `NOTES_S3_K2.md` §14k)
found no errors. It confirmed Matveev's application and the lattice lemma from
first principles, and matched all 18 residual statements with a different
solver. It did **not** independently re-implement the `s3k2/36` recursion.

---

## Where to resume

**Framing.** Nothing below approaches the existence question itself. Each item
either widens the class of structures proved impossible, or hardens a
computation that published work relies on. Items are ranked by value times
tractability; what blocks each is stated.

**Done since the last ranking:**

* the independent audit of §14 (`audit_s3k2/`, §14k);
* the independent rebuild of the profile search (`s3k2/41`–`44`, §14l);
* `verify_all.py`, which now includes the rebuild;
* the forced primes of `p + 1` at every odd `e`, now used by `s3k2/41`.

1. **Written: `K2_WRITEUP.md`.** Still needs a literature check before any claim
   of novelty. Originally: **a self-contained, checkable write-up of `k = 2`:
   `3 ∤ N` and `3` ordinary.** It would turn §§2–14 of the notes into one argument a reader can
   verify, with the scripts as its certificate, and state `3` notable as open.
   This is the highest value per effort, and it is not blocked.
   **Needed from the user:** confirmation that nothing since arXiv:2607.19746
   already covers `k = 2`. The repo cites no such search, and novelty must not
   be claimed without it. Matveev pp. 81 and 83–84 should also be checked for
   standing hypotheses.
2. **Done: overflow-free re-run of Ochem–Zelinsky's sieve** (`restrained/12`–`14`,
   NOTES_RESTRAINED §4d).
   * The re-run is exact below `3.44·10¹⁰` and a provable superset above.
   * It agrees with the authors' unmodified `loopless.cpp` on 253 lines, and with a
     Python reference.
   * True `k(z) = 599,351,328` and `A(z) = 1.047357816316`, against the published
     `2.5·10⁹` and `1.0885`. The result is `k + K_max = 52,785,706,892`.
   * **`q ≥ 23·10⁹` is confirmed; the same method gives `q ≥ 26,392,853,446`.**
   * **Extended (§4f):** at `z = 10¹²`, `q ≥ 120,009,648,966`. `tree.txt`'s claim is
     independently confirmed (§4e).
   * **Next:** report the overflow and the corrected figures to the authors. The
     user decides. The template for a `k = 2` sieve (item 5) now exists.
3. **`k = 3`, for `3 ∤ N` and for `3` ordinary,** using the engine built for
   `k = 2`: the DFS with closure pinning, the Skolem and Matveev + LLL solvers,
   and the count.
   * **What changes.** The 3-budget is `k`-independent (§1). But `|T| ≤ 6`, the
     count weakens to `|U| ≥ 5 − α`, and `3 ∤ N` must first be redone at `k = 3`.
   * **Status.** Tractable now, with an uncertain outcome. A clean statement of
     where the method stops scaling would be a useful negative result.
4. **Done: certificates (`s3k2/41 --cert`) and the checker (`s3k2/46`),
   NOTES_S3_K2.md §14m.** New follow-on: rebuild and certify Theorem A (`3 ∤ N`)
   with the same machinery, which needs `W` slots for two or three components.
   Originally: **certificates and a small independent checker.**
   * **What.** Script 41 emits one record per kill: the reason plus the exact
     numbers. A checker of a few hundred lines re-verifies every record in exact
     arithmetic, without re-running the search.
   * **Why.** It narrows the trusted code from thousands of lines to the
     checker. It speaks to the limit in §14l: the cutoff can only be justified
     by proof, but each *application* of the cutoff can be checked.
   * **Status.** Tractable now.
5. **`3` notable at `k = 2`,** the last open case of `k = 2`. It has two halves.
   * **The sieve half.** A `k = 2` analogue of their Algorithm 1, after item 2.
     With the bound of `AUDIT_S4K2_MODEL_RESULT.md`, a `k = 2` analogue of
     `q ≥ 2.3·10¹⁰` would force `ω(N) ≥ 23`. That is a reduction, not an
     elimination.
   * **The structural half.** The sub-case `p ≡ 5 (mod 12)` with
     `p^e ‖ σ(n₂^{q₂})`, whose hard branch is `f = ord_p(n₂) > 1`, `p ∤ q₂+1`.
     A candidate for a reasoning-model brief. Closing the whole case would go
     beyond the published `k = 1` state of the art.
6. **Question 10.** Two directions:
   * push the exact range beyond `p, r < 1000` (`restrained/09`), by solving each
     `p` for all `r` at once;
   * pursue the `ℤ[ω]` orientation lead of §4a in `NOTES_RESTRAINED.md`.

   This is the lever Ochem–Zelinsky name for tightening their Lemma 8. Moderate
   value, and partial results are likely.
7. **The exact `x² + x + 1` solver applied to other published factor-chain
   proofs.** Where such proofs cut infinite branches with search bounds,
   `s3k2/32`/`39` can close them exactly. This is potentially the widest
   payoff, but it is **blocked** until the user supplies a specific paper;
   none is in the repo.

## Layout

```
AUDIT_REPORT.md            the audit of Mantovanelli; audit/01-06
NOTES_INVERSION.md         Theorem 1 inversion; inversion/01-10
NOTES_RESTRAINED.md        verification of Ochem-Zelinsky; restrained/01-08
NOTES_Q3.md                the q = 3 investigation; q3/01-06
NOTES_K2.md                k = 2, section 2; k2/01-04, k2/audit/01-04, and the certified
                           rebuild k2/05 (search), 06 (checker), 07 (brute force)
NOTES_S3_K2.md             k = 2, section 3 -- the main result; s3k2/01-46
                           (41: rebuild; 45: axioms; 46: certificate checker)
K2_WRITEUP.md              self-contained account of k = 2 (Theorems A and B), with certificates
MATVEEV_1998.md            Theorem 2.2 of Matveev 1998, transcribed; used by s3k2/39
sources/                   page images of Matveev 1998, pp. 82 and 85-87
PROMPT_AUDIT_S3K2.md       brief for an independent audit of section 14
NOTES_S4_K2.md             k = 2, section 4 -- 3 notable; s4k2/01-03
PROMPT_*.md                self-contained briefs written for a reasoning model
verify_all.py              re-derives every section-14 figure (fast / full tiers)
AUDIT_*_MODEL_RESULT.md    audits of what those briefs returned
audit_s3k2/                independent audit of section 14 (report, solver, mutation harness, logs)
```

Every script is runnable as `python3 <file>`; the longer sweeps in `s3k2/`
(scripts 15, 22, 23, 27, 35, and 36 on profile 2,yes,1,4,1) take 10-40 minutes and print progress by profile.
