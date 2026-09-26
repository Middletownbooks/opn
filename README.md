# Odd perfect numbers: audit and continuation

Working repository for two connected pieces of work:

1. an **audit** of Mantovanelli, *Certified Minimal-Prime Branch Closures for
   Odd Perfect Numbers* (arXiv:2607.04365);
2. a **continuation** of Ochem & Zelinsky, *On odd perfect numbers with exactly
   one even exponent greater than 2* (arXiv:2607.19746), from their `k = 1`
   (*restrained*) case to `k = 2`.

Everything is standard-library Python, no external data. Entry points below.

---

## Status in one table

| item | where | status |
|---|---|---|
| Audit of Mantovanelli | `AUDIT_REPORT.md` | **Category C.** Proposition A: acceptance and validity are mutually exclusive for the tail envelope. Decisive, needs no `ω` bound. |
| Verification of Ochem–Zelinsky §§2–3 | `NOTES_RESTRAINED.md` | Reproduces exactly. §4 has a non-reproducing constant; `loopless.cpp` has a 64-bit overflow. Both recorded. |
| `k = 2`, `3 ∤ N` (their §2) | `NOTES_K2.md`, `AUDIT_K2_MODEL_RESULT.md` | **Closed.** My first attempt was wrong (double-counted the prime 5); a reasoning model's fixed-support bound repaired it and I audited it. |
| `k = 2`, `3` ordinary (their §3) | `NOTES_S3_K2.md` | **All 14 role profiles eliminated; none uses a pool.** **10 of 14 unconditional** (only `ω(N) ≥ 10`). The other 4 rest on 15 named Thue–Mahler sets plus stated search bounds (§14). Two errors in the earlier recursion were found and corrected (§14d, §14f). |
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
| `Sm(T)` searched to | `10²⁴` at `\|T\|=5` | up to `10⁴⁰⁰` at `\|T\|=1` |

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

1. **`ω(N) ≥ 10`** (Nielsen 2015). A theorem, used by every counting argument.
   Ten of the fourteen §3 profiles use nothing else.
2. **Fifteen named Thue–Mahler sets** (below). For each, `Sm(T)` was searched
   to `10²⁴` (four or five primes), `10⁴⁸` (three) or `10¹⁶⁰` (two), and must
   be complete. Each is a finiteness statement about one explicit equation, not
   an unbounded hypothesis.
3. **Case-B and Vieta searches** in two `|W| = 1` profiles (`NOTES_S3_K2.md`
   §14e). No solution was found in any of them. Each is "`(t²+t+1)/3` is
   `S`-smooth" for an explicit two- or three-prime `S`, searched to `10³⁰⁰` or
   `10¹²⁰`, plus Vieta pairs to sequence index 1500.
4. **No pool restrictions and no other search bounds.** The four bounds of
   §13d and §9c's case-B bound are all replaced by proofs (§14a–c, §14g).

## The residual Thue–Mahler statements

The `α = 2`, `|W| = 0`, `τ = 5` branch (§10b + §14f), need `|U| ≥ 4`:

| `T` | `Sm(T)` known | admissible for `U` |
|---|---|---|
| `{7, 13, 19, 37, 67}` | 11, 29, 653 | 653 |
| `{7, 13, 19, 37, 127}` | 11, 107, 653 | 107, 653 |
| `{7, 13, 19, 43, 127}` | 11, 107, 653 | 107, 653 |
| `{7, 13, 19, 127, 409}` | 11, 53, 107, 653 | 53, 107, 653 |
| `{7, 13, 19, 127, 1723}` | 11, 41, 107, 653 | 41, 107, 653 |
| `{7, 13, 19, 31, 127}` | 5, 11, 107, 191, 653 | 191, 653 |
| `{7, 13, 19, 31, 331}` | 5, 11, 191, 653 | 191, 653 |

The `|W| = 1` profiles (§14e):

| profile | `T` | `W` | `Sm(T)` | need |
|---|---|---|---|---|
| `0,yes,1,2,1` | `{7,13}` | notable 11 | ∅ | 6 |
| `1,yes,1,3,1` | `{13,61,151}`, `{13,61,157}` | notable 5 | ∅ | 5 |
| `1,yes,1,3,1` | `{7,13,19}` | notable 23 | 11, 653 | 5 |
| `2,yes,1,4,1` | `{13,61,157,8269}` | notable 5 | ∅ | 4 |
| `2,yes,1,4,1` | `{7,13,19,127}` | notable 29, 41, 47 | 11, 107, 653 | 4 |

Every one fails only on the count `|U| ≥ 6 − α`. Settling
`x²+x+1 = ∏_{t∈T} t^{c_t}` completely for these sets, together with the
Case-B/Vieta searches, would make §3 at `k = 2` unconditional apart from
`ω(N) ≥ 10`.

---

## Where to resume

Ranked by value, with what blocks each:

1. **Settle the residual equations without a CAS.** All of them have `Y = 1`.
   With `z = x − ω`, `z − z̄ = −√−3` is fixed while `|z|` is huge, so
   `arg z = arg ε + arg γ + Σ c_t arg π_t` gives a real linear form in
   logarithms that is exponentially small in the exponents. That needs only
   the archimedean case: Matveev's lower bound, then LLL or Baker–Davenport
   reduction, both feasible in standard-library Python. **Needed from the user:**
   an exact statement of Matveev's bound with its constants. It is not cited in
   the repo and must not be reconstructed from memory. This is the standard
   method, not a new one.
2. **An audit pass** for the pattern behind §14d and §14f: a lemma proved for
   a special case but applied more generally, or a kill cited without saying
   whether it was unconditional. Also a `verify_all` runner that re-derives
   every figure the README quotes.
3. **Sharper final tests** from constraints not yet used everywhere:
   * valuation caps in every final test;
   * forced primes of `p+1` for the special at every odd `e`, not only `e = 1`;
   * the production constraint: primes `≡ 2 (mod 3)` never divide `x²+x+1`,
     so `U` and `W` are fed only by the three big components.

   This could shrink the named list before item 1 is even needed. The
   production constraint is an unchecked lead.
4. **`3` notable at `k = 2`.** The open sub-case is `p ≡ 5 (mod 12)` with
   `p^e ‖ σ(n₂^{q₂})`; `PROMPT_S4_K2_SPECIAL.md` is the brief that produced the
   `m` bound. The hard branch is `f = ord_p(n₂) > 1` with `p ∤ q₂+1`, where
   `e = v_p(n₂^f − 1)` and no bound is known. A lower bound on `q` is the sieve
   half of their §4 and is out of reach without heavy computation.

## Layout

```
AUDIT_REPORT.md            the audit of Mantovanelli; audit/01-06
NOTES_INVERSION.md         Theorem 1 inversion; inversion/01-10
NOTES_RESTRAINED.md        verification of Ochem-Zelinsky; restrained/01-08
NOTES_Q3.md                the q = 3 investigation; q3/01-06
NOTES_K2.md                k = 2, section 2; k2/01-04 and k2/audit/01-04
NOTES_S3_K2.md             k = 2, section 3 -- the main result; s3k2/01-38
NOTES_S4_K2.md             k = 2, section 4 -- 3 notable; s4k2/01-03
PROMPT_*.md                self-contained briefs written for a reasoning model
AUDIT_*_MODEL_RESULT.md    audits of what those briefs returned
```

Every script is runnable as `python3 <file>`; the longer sweeps in `s3k2/`
(scripts 15, 22, 23, 27, 35, and 36 on profile 2,yes,1,4,1) take 10-40 minutes and print progress by profile.
