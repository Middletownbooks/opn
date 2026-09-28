# Research brief: new ideas for ruling out restrained odd perfect numbers

*Self-contained. You need no files, tools or internet. Everything you need is
below. Take as long as you need.*

You are being asked for **new ideas**, not a literature review and not a polished
proof. A computational project has reached a point where a heuristic says a famous
open case should be provable, but the obvious rigorous tools fall short by a
measured factor. We want your best thinking on how to close that gap, and equally
your honest judgement on whether it can be closed. **A well-argued "this cannot work,
and here is why" is a valuable answer.**

---

## 1. Setting

`N` is an odd perfect number: `σ(N) = 2N`, where `σ` is the sum of divisors.

* **Euler.** `N = p^e m²` with `p` prime, `p ≡ e ≡ 1 (mod 4)` and `p ∤ m`. Here `p`
  is the **special** prime.
* **Restrained** (Ochem–Zelinsky, arXiv:2607.19746, 2026). Exactly one even
  exponent exceeds 2. That component `n^q` is **notable**. Every other prime of
  `N` other than `p` has exponent exactly 2 and is **ordinary**.
* **Their Theorem 1.** In a restrained OPN, `n = 3` and `q ≥ 2.3·10¹⁰`. The cases
  `3 ∤ N` and `3² ‖ N` are ruled out completely. So **the only open case is
  "3 notable"**. They remark that "new ideas are required" to rule it out.

**Facts used below.** All are from the paper, or proved here with the short
arguments given.

* **(F1)** Every prime `5 ≤ t < 3·10⁶` does not divide `N`. (Their factor-tree
  computation; independently re-checked.)
* **(F2)** `p ≡ 1 (mod 12)` (their Lemma 6 with Euler), and `p > 6·10⁶`: `(p+1)/2`
  divides `N` and has no prime factor below `3·10⁶`.
* **(F3)** Every prime factor of `x² + x + 1` is 3 or `≡ 1 (mod 3)`. `v₃(x²+x+1) = 1`
  if `x ≡ 1 (mod 3)`, and 0 otherwise.
* **(F4)** For ordinary `s`, `σ(s²) = s² + s + 1` divides `2N`, so each of its prime
  factors divides `N`.
* **(F5)** `q = o₁ + v₃(e+1)`, where `o₁` is the number of ordinary primes
  `≡ 1 (mod 3)`. (Proof: count `v₃` of `σ(N) = 2N`, and use (F3) and LTE on
  `σ(p^e)`.) Their Lemma 8 gives `o₂ ≤ o₁ + 2`, where `o₂` counts ordinary primes
  `≡ 2 (mod 3)`, and hence `q ≥ ω(N)/2 − 2`.
* **(F6)** Every prime `r > 3` dividing `σ(3^q)` is `≡ ±1 (mod 12)`. (Proof: `q`
  even, so `ord_r(3) | q+1` is odd, so 3 is a quadratic residue mod `r`.)
* **(F7)** Each ordinary prime `t` has `t² ‖ N`, so across all components `C`, the
  numbers `σ(C)` contain exactly two copies of `t` in total.

## 2. The sieve (their Algorithm 1)

`M₁` holds primes known **not to be ordinary**; `M₂` holds primes `≡ 1 (mod 3)`
known **not to divide `N`**.
* **Initially:** `M₁` = all primes in `[5, 3·10⁶)`; `M₂` = the primes `≡ 1 (mod 3)`
  in `[7, 3·10⁶)`.
* **For each prime `r > 3·10⁶` in increasing order:**
  * If **no prime of `M₂` divides `r² + r + 1`**, `r` **survives** ("can be
    ordinary"). Set `A ← A · r/(r−1)` and `k ← k + 1`.
  * Otherwise `r` joins `M₁`. If also `r ≡ 1 (mod 3)`, and either `r ≡ 3 (mod 4)` or
    some prime factor `≥ 5` of `r + 1` lies in `M₁`, then `r` joins `M₂`. (Such an
    `r` cannot be special either, because `r + 1 | σ(r^e)` for odd `e`.)

**The count.** Let `c = ln(4/3) − ln(1 + 1/6·10⁶) = 0.287682…`. The factor `4/3` is
`2 / (3/2)`, because `σ(3^q)/3^q < 3/2`; the other factor is the special prime's
bound. Suppose `ln A(z) < c`, where `A(z)` is the product over survivors
`≤ z`.
* Ordinary primes above `z` each contribute less than `1 + 1/z` to the abundancy.
* So `N` has **more than `k(z) + K_max(z)`** ordinary primes, where
  `K_max = ⌊(c − ln A(z)) / ln(1 + 1/z)⌋`, roughly `z (c − ln A(z))`.
* Then `q ≥ (ω − 3)/2`, roughly `K_max / 2`.

**The key reduction.** If `ln A(z) < c` held for **every** `z`, then `N` would need
infinitely many ordinary primes: **no restrained OPN exists**. It suffices that
`Σ_{survivors r} ln(r/(r−1)) < c`, summed over all `r`.

## 3. Verified computations (treat as given)

**Exact Algorithm 1 up to `3.44·10¹⁰`** (independent C implementation, which agrees
with the authors' program wherever theirs is exact):

| `x` | survivors `k(x)` | `ln A(x)` |
|---|---|---|
| `10⁹` | 4,153,916 | 0.029734 |
| `2³²` | 15,656,368 | 0.034899 |
| `10¹⁰` | 33,867,299 | 0.037610 |
| `3.4·10¹⁰` | 103,866,536 | 0.041215 |

**Beyond that** (exact below `3.44·10¹⁰`, a provable superset of the survivors above,
so these are upper bounds): `ln A(2.16·10¹¹) ≤ 0.046271` and
`ln A(10¹²) ≤ 0.050333`. This gives `q ≥ 1.2·10¹¹` rigorously.

**The survival rate** (survivors / primes) falls slowly: 7.56%, 7.24%, 7.02% and
6.86% on `(10⁹, 4·10⁹]`, `(4·10⁹, 10¹⁰]`, `(10¹⁰, 2·10¹⁰]` and
`(2·10¹⁰, 3.4·10¹⁰]`.
* A fit `f(r) ≈ 1.05 (ln r)^−0.86` makes `Σ 1/r` over survivors **converge**.
  The tail beyond `3.4·10¹⁰` is about 0.079, so **`ln A(∞) ≈ 0.12`, against
  `c = 0.288`**. This is heuristic, but it is the finding we want to exploit.
* The mechanism: `M₂` grows. **90.4% of primes `≡ 1 (mod 3)` below `10⁸` are in
  `M₂`** (2,604,985 of 2,880,517). So a survivor must avoid about 90% of these
  primes, all the way up to its own size.
* A **static** version, avoiding only `M₂ ∩ [7, 3·10⁶)`, has a constant rate of
  about 11.3% of primes (0.113 `x/ln x` on `(x, 2x]`, exact to 0.5%). Its sum
  diverges.

**A new, sound strengthening: the look-ahead.** If `r` survives and `r² + r + 1`
has a prime factor `P > r`, then `P | N` (F4). `P` must be ordinary or special:
* **ordinary** needs no prime of `M₂` to divide `P² + P + 1`;
* **special** needs `P ≡ 1 (mod 12)` and no prime factor of `(P+1)/2` in `M₁`.

If both fail, `r` cannot be ordinary. Algorithm 1 never examines `P`. On a random
sample of 3,000 exact survivors in `(5·10⁷, 10⁸]`:
* 99.9% have such a `P`;
* **the look-ahead removes 82.9% of them**, using only `M₁` and `M₂` below
  `5·10⁷`.

The look-ahead can be iterated: `P`'s own large factor, and so on. So the true
"can be ordinary" density is several times smaller than Algorithm 1's.

## 4. What has been tried and failed (please do not repeat unless you see a fix)

1. **Brute force.** The `q` bound grows only linearly in `z`, about `0.12 z`, at
   hours per `10¹²`.
2. **Static Selberg Λ² upper bound** on `#{r ∈ (x, 2x] prime : no q ∈ M₂, q < 10⁸,
   divides r²+r+1}`.
   * Setup: sieve the integers in `(x, 2x]` with `ω(p) = 3` for `p ∈ M₂` and
     `ω(p) = 1` otherwise, and `|R_d| ≤ ω(d)`.
   * The bound is **5–7 times** the true static count at `x = 10¹⁰`–`10²⁰`.
     Carried from `10¹²`, it projects only `q ≳ 7·10¹²`.
   * The explicit large sieve `(N + Q²)/L` gives about `q ≳ 10¹³`.
3. **A bootstrap toward the full proof.** The primes outside `M₂` are mostly
   survivors, so the plan was an inductive density bound. In the exactly known
   range, the best Selberg bound is about **12.6 times the true survivor count**.
   An idealised `x/G(√x)`, ignoring the error term, is about **8.8 times**.
   * Both ratios rise slowly with `x`: the true survivors avoid `M₂` up to `r`,
     while a sieve sees `M₂` only below `√x`.
   * **A proof needs about 3.1 times or less.** The allowed factor rises only to
     3.4 if brute force reached `10¹²`, and to 5.9 at `10²⁸`.
   * Asymptotically, Selberg's loss in dimension `κ ≈ 1.9` is about
     `2^κ Γ(κ+1) ≈ 6.8`. A factor of about 2 is forced by the parity barrier on the
     prime condition alone.
4. **Tightening Lemma 8** (`o₂ ≤ o₁ + 2`) by capacity counting with (F6)/(F7). This
   fails, because `σ(3^q)` and `σ(p^e)` have unbounded capacity to produce copies
   of ordinary primes.

With the look-ahead, the heuristic tail shrinks severalfold, so the allowed factor
grows to perhaps 10–20. But the upper-bound sieves above do not see the look-ahead.
Capturing it seems to need sieving a degree-4 polynomial in `r`, for each small
cofactor `s` with `r² + r + 1 = s · P`. That raises the sieve dimension, and with it
the sieve's inherent loss.

## 5. The questions

**Main question.** Find **new ideas** that could turn the heuristic
`ln A(∞) ≈ 0.12 < c` into a **proof** that `Σ_{r can be ordinary} ln(r/(r−1)) < c`.
Using any sound strengthening of "can be ordinary" is allowed; the look-ahead is
one. That would rule out restrained odd perfect numbers. **Or** explain convincingly
why no approach of a given kind can work.

**Secondary questions,** valuable on their own:
* **(a)** An argument giving a much larger rigorous `q` bound (say `≥ 10¹⁵`) from
  the same structure, even if the full proof is out of reach. A proof of
  `ln A(Z) < c` for some huge but finite `Z` gives `q ≳ Z (c − ln A(Z)) / 2`.
* **(b)** A different contradiction altogether, one that does not go through the
  survivors' tail. For example, one using (F5)–(F7), the structure of
  `σ(3^q) = (3^{q+1} − 1)/2` with `q ≥ 1.2·10¹¹`, or the exact multiplicity
  constraint (F7) across all components.
* **(c)** A rigorous statement that explains *why* the survival rate falls. For
  example, a lower bound on how much of `M₂` is forced, proved without computing it.

**Leads, offered without guarantee** (unpursued; judge them critically):
* **(L1) The look-ahead as a sieve.** Iterated look-ahead, or look-ahead in the
  aggregate, might be expressible as a sieve of higher dimension, where the
  densities decay like `(ln x)^−κ` with `κ > 1`. Then the sum converges fast, and a
  large constant loss might be affordable. Is there a formulation where the loss
  grows more slowly than the gain?
* **(L2) The exact multiplicity (F7).** Each ordinary `t ≡ 1 (mod 3)` is used
  exactly twice. A survivor `s` whose `s² + s + 1` has several such factors
  consumes capacity. The obstruction is that `σ(3^q)` and `σ(p^e)` have unbounded
  capacity. But (F6) says `σ(3^q)` produces only primes `≡ ±1 (mod 12)`, and
  `σ(p^e)` is a single component. Can the capacity argument be restricted to a class
  of primes those two cannot serve?
* **(L3) The Eisenstein integers.** `r² + r + 1 = N(r − ω)` in `ℤ[ω]`. "No factor
  from `M₂` below `r`" is a condition on the Eisenstein prime factors of `r − ω`.
  Is there a bilinear structure (factorisations into two parts of controlled size),
  or a way to exploit that `r − ω` runs along a line, that beats one-dimensional
  sieve limits?
* **(L4) Self-consistency.** Every survivor's factors are themselves "can be
  ordinary" primes, recursively, at every scale. Is there a fixed-point or
  percolation-type argument that forces the density down?
* **(L5) Finite-`Z` targets.** Proving `ln A(Z) < c − δ` for `Z = 10⁵⁰`, not `∞`,
  would already give `q ≳ 10⁴⁹`. Does allowing finite `Z` change which tools apply?

## 6. What to deliver

1. **At least five distinct ideas,** ranked by your estimate of (value) × (chance
   of working). For each:
   * **(a)** the precise statement that would need to be proved;
   * **(b)** why it could get past the barriers in §4: the parity factor 2, the
     level `√x`, and unbounded capacity;
   * **(c)** what would need computing, and roughly how much (bare Python or C, on a
     machine with 4 cores and 15 GB);
   * **(d)** the quickest test that could falsify it;
   * **(e)** your honest probability that it works.
2. **For your top idea,** as much of an actual argument as you can give: lemmas
   with proofs, or precise conjectures with the evidence they would need. Mark
   every step as **proved**, **standard** (name the source only if you are
   confident it exists), or **conjectural**.
3. **A critique of the whole programme.** Is "`ln A(∞) < c`" plausibly provable
   with current methods? What is the strongest reason it might be out of reach?
4. **Anything in this brief you believe is wrong,** with the reason.

## 7. Rules

* **No invented mathematics.** Do not present a claim as proved unless you give
  the proof. Label heuristics as heuristics.
* **No literature laundering.** Cite a result only if you are confident it exists,
  and say how confident you are. "I believe there is a result of the form…" is
  fine; a fabricated reference is not. We will check every citation.
* Numbers in §3 are measured. If an idea depends on a number not given here, say
  so. We can compute it.
* Brevity is not required; clarity is. Separate the ideas cleanly so each can be
  assessed on its own.
