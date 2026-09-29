# New ideas for the restrained-OPN tail: what was tested, and what it showed

Answer to `PROMPT_IDEAS_RESTRAINED_TAIL.md`. Scripts are in this directory, numbered
`00`–`11`; each has a header saying what it computes and how to run it, and outputs
are saved beside them (`*.out`, `runs/`). Existing files were not modified.

Labels: **proved** (proof given here), **standard** (a textbook or published result,
cited only where I am confident it exists), **measured** (a computation, exact unless
it says "sample" or "pilot"), **heuristic**, **conjectural**.

---

## 0. Summary

**Main question (a proof that `Σ_{can be ordinary} ln(r/(r−1)) < c`).** My judgement:
**not reachable along the survivor-tail route with current methods, and the look-ahead
does not change that.** The decisive test was cheap (`07`). Take the primes as the
input sequence, so primality costs nothing, and ignore every error term. Even then, the
best Selberg bound for Algorithm-1 survivors is **5.4× the true count at the
Bombieri–Vinogradov level** and **3.15× at an Elliott–Halberstam level**. A proof needs
**≤ 3.1–4.5×** (depending on the base and the tail model). So no sieve of this kind closes the gap unconditionally, whatever the
explicit constants. Under an explicit EH-type hypothesis it might just close (Idea 5). The
look-ahead's large gain is carried entirely by the largest prime factor of `r²+r+1`.
Sieves cannot see that factor without raising the dimension from about 2 to about 6.6,
which costs about 10⁴ times more than it gains.

A reformulation makes the difficulty concrete (`11`). **94–98% of Algorithm-1
survivors are Bateman–Horn prime pairs**: primes `r` with `(r²+r+1)/3^{[r≡1 (3)]}`
also prime. So the main question is, up to a few percent, an *explicit Brun-constant
bound* for a 2-dimensional prime-pair problem, within about 3–4.5 times the true tail.
For the best-studied analogue, twin primes, the best known upper bound I know of is
about 3.4 times the Hardy–Littlewood prediction (Wu 2004), and it is not explicit.

**Secondary question (a), a much larger rigorous `q`.** Three sound improvements, each
tested:

| step | what changes | `q ≥` | status |
|---|---|---|---|
| brief | `K_max(10¹²)/2` | `1.2·10¹¹` | rigorous |
| **Idea 1** | greedy-fill count (Lemma G0), all primes beyond 10¹² | **`2.25·10¹³`** | **rigorous** (explicit prime estimates only) |
| **Idea 2** | plus the look-ahead base, with the special branch dropped (the special prime is unique) | **`7.6·10¹³`** | **rigorous** (exact C run below 3.4·10¹⁰, cross-checked) |
| **Idea 3** | Selberg pilot re-accounted (weighted main term + Lemma G) | `≈ 3.1·10¹⁴` (old base), **`≈ 2.8·10¹⁵`** (look-ahead base) | pilot; sound in principle |

Idea 3's bound becomes rigorous once `16c`'s tables are recomputed with outward rounding.
That needs no new mathematics. The brief's own Selberg projection (`7.4·10¹²`) lies
**below** the no-sieve bound of Idea 1; §4 explains the accounting slip.

**Secondary question (b).** The routes through `σ(3^q)` and `σ(p^e)` give real lemmas
but no contradiction. One is an exact identity, `e = Σ_{s ordinary} v_p(s²+s+1) +
v_p(σ(3^q))`. It shows that `σ(p^e)`'s capacity is fed by the ordinary primes in two
residue classes mod `p`, which can be arbitrarily large. The other gives congruence
restrictions on `q + 1` (`08`). Both are negative for a contradiction (Ideas 7–8).

**Secondary question (c).** A bootstrap proof that the survivors' reciprocal sum
*converges*, i.e. that the survival rate provably tends to 0, looks feasible. The
seed pilot (`10`) finds a positive share for `M₂` from about `10¹⁴` on. It cannot give
`< c` (Idea 4).

The falling rate itself has a simple explanation, measured in `11`. Survivors are
mostly Bateman–Horn pairs, whose density among primes falls like `1/ln r`: 8.84%, 7.30%,
7.07% at `r ~ 3·10⁷`, `1.4·10⁹`, `2.8·10⁹`, the ratios `1/ln r` predicts. The non-pair
survivors, those with a factor from the sparse allowed set `D`, add a share that grows
slowly: 2.4% below `10⁸`, 5.2–5.6% at `10⁹`. This is why the fitted exponent is about
0.86–0.9 rather than 1.

**New sound strengthening, measured.** With the special branch removed (Lemma U), the
look-ahead removes **85–89%** of survivors at depth 1 (samples, static `M₂` below `10⁸`),
against the brief's 82.9%. The exact run over every survivor below `3.4·10¹⁰` removes
84.7–85.7% with the cheaper lists below `3·10⁶` or `10⁷`. At depth 2 it removes
**94–98%**, at every scale from `3·10⁶` to `10¹²`. So in
the heuristic picture only about 2–5% of Algorithm-1 survivors can be ordinary.

---

## 1. The ideas, ranked by (value) × (chance of working)

| rank | idea | serves | P(works) | value |
|---|---|---|---|---|
| 1 | Greedy-fill count (Lemma G0/G) | (a) | 0.97 (done) | ×190 in `q`, free |
| 2 | Unique special prime ⇒ stronger look-ahead; exact look-ahead base | (a) | 0.95 (done) | ×3.4 more (rigorous); ×9 in the Selberg pilot |
| 3 | Weighted Selberg + Lemma G, made rigorous | (a) | 0.85 | `q ≈ 3·10¹⁵` |
| 4 | Bootstrap: provable convergence of the survivors' sum | (c) | 0.4 | explains the falling rate; no contradiction |
| 5 | The level barrier, and conditional closure under EH | main (verdict) | 0.3 (conditional theorem) | settles what is needed |
| 6 | Iterated look-ahead / chain forest (L1, L4) | main, (a) | 0.01 (main); 0.9 (base) | small for (a) |
| 7 | `σ(3^q)` ⇒ restrictions on `q+1` | (b) | < 0.01 | restrictions only |
| 8 | Capacity via `e = Σ v_p(σ(C))` (L2) | (b) | < 0.02 | negative |
| 9 | Eisenstein bilinear structure (L3) | main | < 0.01 | negative |

"P(works)" is my probability that the idea delivers what the "serves" column says. For
Ideas 1–2 the delivery is done and checked.

---

### Idea 1 — Greedy fill: count the whole superset, and push `z` to where the product hits `c`

**(a) Statement (proved; §2.1).** Let `O` be the set of ordinary primes and
`w(s) = ln(s/(s−1))`.

**Lemma G0.** Let `U` be a set of primes `≤ z` with `U ⊇ O ∩ (3·10⁶, z]` and
`Λ = Σ_{u∈U} w(u) < c`. Then `|O| > |U| + (c − Λ)/ln(1 + 1/z)`.

The brief keeps `U` equal to the survivors up to the last computed `z`, and reads off
`q ≈ K_max/2`. But `U` may be *any* superset, for example the survivors below `10¹²`
together with **all primes** in `(10¹², z]`. And `|U| + K` increases with `z` while
`Λ(z) < c`, because its derivative is about `c − Λ(z) > 0`. So `z` should be pushed to
where `Λ(z) = c`.

**(b) Barriers.** It is bookkeeping, so none apply. It is not a route to the full proof.

**(c) Computation.** None; 0.1 s.

**(d) Test run** (`01_greedy_fill_trivial.py`, `01_greedy_fill_trivial.out`). It uses
explicit prime estimates only. With `U = T ∪ {primes in (10¹², z]}`, where `T` is the
`Q = 2³⁵` superset run below `10¹²` (`|T| = 2,670,032,132`, `ln A ≤ 0.0503326…`):

    optimum z ~ 1.5792e+15: Lambda <= 0.287681906 (< c),
    |O| >= 45,090,839,525,422, so q >= 22,545,419,762,710

against the brief's `q ≥ 120,009,648,968`: **190 times larger, with no new computation.**

**(e) Probability: 0.97.** The only outside inputs are explicit estimates for `Σ 1/p`
and `π(x)` (§2.1, where they are listed with my confidence in them). The margin is wide:
multiplying their error terms by 10 moves `z*` by a few percent.

### Idea 2 — The special prime is unique, so the look-ahead's special branch almost never applies

**(a) Statement (proved; §2.2).**

**Lemma U.** At most **two** ordinary primes `r` have `P⁺(r²+r+1) = p > r`.

*Proof.* Such an `r` satisfies `r < p` and `p | r² + r + 1`. The congruence
`x² + x + 1 ≡ 0 (mod p)` has at most two roots in `[0, p)`. ∎

So apart from those two primes, every ordinary `r` whose `r²+r+1` has a prime factor
`P > r` has `P` **ordinary**. That means no prime of `M₂` divides `P²+P+1`. The
brief's look-ahead (`restrained/17`) also allowed "`P` special" for every `r`.

**Depth 2.** If `P` is ordinary and `P' = P⁺(P²+P+1) > P`, then `P'` is ordinary,
except for at most 2 values of `P`. Each such `P` comes from at most 2 values of `r`, so
this adds at most 4 more exceptions.

**Lemma P (proved).** No factoring is needed to find `P`. For an Algorithm-1 survivor
`r`, divide `r²+r+1` by `3^{[r≡1 (3)]}` and by every power of the **D-primes** below `r`.
A D-prime is a prime `≡ 1 (mod 3)` that is not in `M₂`. What is left is `1` or the
prime `P`.

*Proof.* The prime factors of `r²+r+1` below `r` are 3 or `≡ 1 (mod 3)` (F3). Those
`≡ 1 (mod 3)` are not in `M₂`, because `r` survived; primes below `3·10⁶` that are
`≡ 1 (mod 3)` are all in `M₂`. So those factors are D-primes. The cofactor `C` then has
no prime factor below `r`. Since `C ≤ r²+r+1 < (r+1)²`, `C` is 1 or a prime. ∎

**(b) Barriers.** This is a finite computation that improves the base value
`Λ₀ = ln A(10¹²)`, not the tail, so the parity, level and capacity barriers do not arise.

**(c) Computation.**
* `05_lookahead_base.c` is `13_sieve.c` plus D-prime tracking and the test, in exact
  mode. It covers `[3·10⁶, 3.4·10¹⁰)` in four pieces, about about 4 core-hours (the slowest piece took 49 min) on 4 cores, with at
  most 6 GB for the largest piece.
* The static `M₂` list is below `10⁷` for `r < 10⁹` and below `3·10⁶` above. A list
  below `10⁸` adds about 2 points of removal at 10–60 times the cost.
* Depth 2 needs `P²+P+1` factored, up to `r⁴ ≈ 10⁴²`. That is beyond 128-bit C, so here
  it was only sampled.

**(d) Tests run.**
* `06` checks `05` by independent full factorisation on `[3·10⁶, 5·10⁶)`. All five
  counts are identical (13,393 survivors, 11,346 removed, `ln A` kept
  `0.000523328807081162`).
* Every `05` run reproduces `restrained/13`'s exact `k` and `ln A` to every printed
  digit at its end point.
* `04` measures the rates on samples of 1,500. Below `10⁸` the survivors are exact;
  above, they are the "static" superset (`M₂` below `10⁸` only), so those rows are
  indicative.

  | `x` | `P > r` | old (special allowed) | **new (Lemma U)** | **new, depth 2** | terminal |
  |---|---|---|---|---|---|
  | `3·10⁶` | 100.0% | 81.1% | **87.5%** | **98.3%** | 0 |
  | `10⁷` | 99.9% | 84.1% | **88.5%** | **97.7%** | 1 |
  | `2.5·10⁷` | 99.9% | 81.5% | **87.3%** | **97.1%** | 1 |
  | `5·10⁷` | 100.0% | 83.5% | **88.9%** | **97.8%** | 0 |
  | `10⁹` (static) | 97.2% | 80.0% | 85.3% | 94.5% | 42 |
  | `10¹⁰` (static) | 98.4% | 82.5% | 87.3% | 96.1% | 24 |
  | `10¹¹` (static) | 98.5% | 81.3% | 86.3% | 96.0% | 22 |
  | `10¹²` (static) | 98.9% | 81.5% | 85.6% | 96.5% | 16 |

  The "old" column reproduces the brief's 82.9%. **The rates do not decay with `r`.**
  The "terminal" counts above `10⁸` are inflated by the static superset: its members
  include `r` that `M₂` primes in `[10⁸, r)` would remove.
* **Exact base** (`09_combine.py`):

  | look-ahead range | survivors | removed | kept | `ln A` kept |
  |---|---|---|---|---|
  | `[3·10⁶, 5·10⁸)` (list below 10⁷) | 2,210,628 | 1,894,046 | 14.3% | 0.003863 |
  | `[5·10⁸, 10⁹)` (list below 10⁷) | 1,943,288 | 1,665,404 | 14.3% | 0.000387 |
  | `[10⁹, 2·10⁹)` | 3,649,303 | 3,090,720 | 15.3% | 0.000389 |
  | `[2·10⁹, 10¹⁰)` | 26,064,080 | 22,080,808 | 15.3% | 0.000816 |
  | `[10¹⁰, 1.1·10¹⁰)` | 3,083,537 | 2,612,483 | 15.3% | 0.000045 |
  | `[1.1·10¹⁰, 2·10¹⁰)` | 26,906,448 | 22,796,107 | 15.3% | 0.000274 |
  | `[2·10¹⁰, 2.2·10¹⁰)` | 5,825,045 | 4,934,544 | 15.3% | 0.000042 |
  | `[2.2·10¹⁰, 3.4·10¹⁰)` | 34,184,207 | 28,962,026 | 15.3% | 0.000190 |

  Below `3.4·10¹⁰`, Algorithm 1 has `k = 103,866,536` and `ln A = 0.041215`. The
  look-ahead keeps `k = 15,830,398` with `ln A = 0.006005`.

  With the `Q = 2³⁵` superset for `[3.4·10¹⁰, 10¹²]` and the two exceptions, the base
  below `10¹²` becomes `|T'| ≥ 2,581,995,994` and `Λ₀ ≤ 0.015124` (was 0.050333).
  Then Lemma G0 gives, **rigorously, `q ≥ 76,398,309,880,154`** (`z* ≈ 5.5·10¹⁵`).
  The Selberg pilot on the same base gives `q ≈ 2.8·10¹⁵` (`z* ≈ 5.2·10¹⁷`).

  The pieces ending at `5·10⁸`, `2·10⁹`, `1.1·10¹⁰` and `2.2·10¹⁰` come from the first,
  slower runs, stopped at those checkpoints. The rest come from reruns with the faster
  remainder (`05`: Lemire–Kaser–Kurz). The reruns were checked against the division-based
  test on every call on `[10⁹, 1.01·10⁹)` and `[3·10⁶, 5·10⁶)`, with identical results.
  Raw outputs are in `runs/`.

**(e) Probability: 0.95.** Done. The value is moderate: it shrinks `Λ₀` by about
0.035 (from 0.0503 to 0.0151), and `q` grows exponentially in `c − Λ₀`.

### Idea 3 — The Selberg pilot, re-accounted, and made rigorous

**(a) Statement.** Lemma S (standard; §2.3) and Lemma G (proved; §2.1):
`Σ_{r ∈ S ∩ (x, ρx]} 1/r ≤ ln ρ / G(ξ) + 2(1 + E₁(ξ)²)/x`, fed into the greedy fill.

`16d` bounded the reciprocal sum on `(x, 2x]` by `(count bound)/x`. That overstates the
main term by `1/ln 2 = 1.44`. It also used `q ≈ K_max/2`.

**(b) Barriers.** This runs straight into the level and dimension barriers. The bound
is still `0.56–0.81` of the trivial prime sum (`02`, table at the top of its output), and
it has a ceiling. With a sieve bound at `θ` of the prime density, the greedy fill gives
`z* ≈ z₀^{exp((c−Λ₀)/θ)}`. For `θ ≥ 0.5` and `z₀ = 10¹²` that is at most about
`10^{21}`, so `q ≲ 10^{19}` (for θ = 0.6 instead: `q ≲ 10^{17}`). **`q ~ 10⁴⁹` (the brief's L5 example) is out of reach.**

**(c) Computation.**
* Recompute `16c`'s tables (`G`, `E₁`) in exact or interval arithmetic: minutes.
* Optionally extend the exact-`M₂` table from `10⁸` to `10⁹`. The present layout needs
  about 13 GB, so it needs a leaner design.

**(d) Test run** (`02`, `09`).
* Old base: `q ≈ 3.1·10¹⁴`, against `16d`'s `7.4·10¹²`.
* Look-ahead base: `q ≈` `2.8·10¹⁵`.

The sensitivity table in `02.out` shows how strongly `Λ₀` matters.

**(e) Probability: 0.85** that a rigorous version gives `q ≥ 10¹⁵`.

### Idea 4 — Bootstrap: a provable proof that the survival rate tends to 0 (question (c))

**(a) Conjecture to prove.** There are explicit `x₀`, `δ > 0` with two properties:
* for every `x ≥ x₀`, `M₂` contains at least `δ · π(x, 2x; 3, 1)` primes of `(x, 2x]`;
* hence Algorithm-1 survivors have density `≤ C (ln x)^{−δ'}` for an explicit `δ' > 0`,
  and `Σ_{survivors} 1/r < ∞`.

**Mechanism.** `M₂ ⊇ {primes ≡ 1 (3)} ∖ (S ∪ Sp)`, where `Sp` is the special
candidates. So upper bounds on the survivors `S` and on `Sp` in `(x, 2x]` give a lower
bound on `M₂` there. That lower bound makes `G(ξ)` grow at the next scales, which lowers
the survivor bound, and so on.

One sieve issue remains: `M₂` membership is not known individually beyond the exact
table. Handle it by sieving with `ω = 3` at *every* prime `≡ 1 (3)` in `[Y, ξ)`. Then
add back the `r` with a factor in `(S ∪ Sp) ∩ [Y, ξ)`, by a union bound controlled by the
induction hypothesis.

**(b) Barriers.** None for *convergence*. It needs only `θ_S + θ_Sp < 1` at one seed
scale. It does nothing for the constant: the resulting bound on `ln A(∞)` would be well
above `c`.

**(c) Computation.** Moderate: a family of Selberg bounds with explicit `λ_d` estimates.

**(d) Test run** (`10_bootstrap_seed.py`, a pilot). It estimates the lower bound
`1 − θ_S − θ_Sp` on `M₂`'s share of the primes `≡ 1 (mod 3)`:

    x      theta_S  theta_Sp  M2 share >=
    1e+10    0.921     0.371       -0.292
    1e+12    0.792     0.321       -0.113
    1e+14    0.692     0.284        0.024
    1e+16    0.615     0.289        0.096

So there is **no seed at `10¹²`**, but one appears from about `10¹⁴`. The truth is
about 0.90, so the bound on special candidates, `θ_Sp`, is the weak link. It sieves
`(r+1)/2` only by primes below `ξ`, while the true special candidates are about 1% of the
primes `≡ 1 (mod 3)` (`03`: 21,670 below `10⁸`). This lowered my estimate from 0.6 to 0.4.

**(e) Probability: 0.4** for a complete rigorous proof. It answers (c) qualitatively.

### Idea 5 — The level barrier (verdict on the main question), and conditional closure

**(a) Measured statement** (`07_level_ideal.py`). Take the primes in `(x, 2x]` as the
sequence, sift them by the two root classes of `r²+r+1` for every `M₂` prime below `ξ`,
and use Selberg's upper bound with level `D = ξ²` and **no error term**. Then:

| range | true survivors | BV level (`D = √x`) | EH level (`D = x`) |
|---|---|---|---|
| `(10⁹, 2·10⁹]` | 3,649,303 | 5.37× | 3.15× |
| `(4·10⁹, 8·10⁹]` | 12,948,576 | 5.39× | 3.15× |
| `(1.6·10¹⁰, 3.2·10¹⁰]` | 46,192,027 | 5.46× | 3.17× |

For comparison, **the overshoot a proof can afford** is the budget `c − Λ₀(z₀)` divided
by the heuristic Algorithm-1 tail beyond `z₀`:
* 3.1 at `z₀ = 3.4·10¹⁰`;
* 3.4 at `10¹²`;
* 3.9 at `10¹²` with the look-ahead base of Idea 2.

**Conjecture (heuristic).** These ratios persist, rising slowly, at larger `x`.

**(a′) The same barrier, seen as a prime-pair problem** (`11_bh_pairs.c`, measured).
Call `r` a *Bateman–Horn pair* if `r` and `n = (r²+r+1)/3^{[r≡1 (3)]}` are both prime.

*Lemma (proved).* Every pair is an Algorithm-1 survivor, and every other survivor has a
D-prime factor. For a pair, `n` is a prime `> r`, so no `M₂` prime below `r` divides
`r²+r+1`. For a non-pair survivor, the cofactor of Lemma P is `< n`, so some D-prime was
divided out.

Measured shares of the survivors:

| range | pairs / survivors | share of `Σ w` |
|---|---|---|
| `(3·10⁶, 10⁸]` | 490,328 / 502,588 = 97.6% | 98.5% |
| `(10⁹, 2·10⁹]` | 3,459,577 / 3,649,303 = 94.8% | 94.8% |
| `(2·10⁹, 4·10⁹]` | 6,487,863 / 6,869,861 = 94.4% | 94.5% |

So a proof of `ln A(∞) < c` needs, for the pairs alone, an explicit bound on
`Σ_{pairs, r > z₀} 1/r` within a factor of about 3–4.5 of the truth. That is an explicit
"Brun constant" for a 2-dimensional prime-pair problem.

The best-studied analogue is the twin primes. The best upper bound I know for
`π₂(x)` is about 3.4 times the Hardy–Littlewood prediction (J. Wu, *Acta Arith.* 114,
2004; I am fairly confident of the constant 3.3996, but please check). It rests on Chen's
switching principle and Bombieri–Vinogradov, and it is **not explicit**. Explicit
bounds for Brun's constant itself (Riesel–Vaughan 1983, `B₂ < 2.347`, and later small
improvements) are, as far as I know, well above the true value. That supports the same
conclusion; I have not reconstructed their tail overshoot, so treat this as a pointer
rather than evidence.

*A second tail model* (heuristic). The pair density fits `1.54/ln r`, the Bateman–Horn
shape (8.84%, 7.30%, 7.07% at `r ~ 3·10⁷`, `1.4·10⁹`, `2.8·10⁹`). Adding the non-pair
share of 6–10% puts the Algorithm-1 tail beyond `10¹²` at about 0.060, against the
brief's fitted 0.0704. The allowed overshoot then rises to about 4.0 (old base) or
4.5 (look-ahead base). The verdict is unchanged: the BV-level ideal of 5.4 still
exceeds it.

**Consequences.**
* **Unconditionally, the survivor-tail route cannot close.** Sieving the integers for
  primality costs a further factor of about 2.8 (`16f`'s ideal 8.8 against 3.15).
  Sieving the primes needs a level of distribution, and even a perfectly explicit
  Bombieri–Vinogradov at level `√x` leaves 5.4. That exceeds the 3.1–4.5 allowed under
  either tail model.
* **Conditionally**, an explicit Elliott–Halberstam-type hypothesis for primes in the
  root progressions of `x² + x + 1` might suffice. It would need moduli up to
  `x^{1−ε}` and small explicit error. Then the ratio 3.15–3.2 sits below the ~3.9
  allowed, and heuristically `Λ₀ + 3.2 × 0.0704 ≈ 0.24 < c`. The margin is small.

**(b)** This *is* the barrier. The parity factor the brief cites is part of it: with the
primes as the input sequence, parity shows up as the level restriction.

**(c)** Done: `07` runs in 0.4 s.

**(d)** Done (above). The quickest way to *refute* the verdict would be a sieve that
beats Selberg's Λ² at this level in dimension about 0.93. For dimension 1 at `s = 2`,
Selberg's bound is known to be optimal by Selberg's parity example (standard). I am not
aware of an optimality theorem for non-integer dimension, so that part is expert
judgement.

**(e) Probability.** That the unconditional route works: < 0.01. That the conditional
statement can be made rigorous: 0.3. It needs the error terms and the bootstrap of
Idea 4.

### Idea 6 — Iterated look-ahead, chain forest (leads L1, L4)

**(a) Statement (proved).** Let `φ(r) = P⁺(r²+r+1)` when this exceeds `r`.
* On `O ∖ E`, `φ` maps into `O ∪ {p}`, is strictly increasing, and is at most 2-to-1.
* So every ordinary prime lies on a finite chain `r → φ(r) → …`. The chain ends at a
  *terminal* ordinary prime `t` (with `P⁺(t²+t+1) < t`) or at `p`.
* Each chain step is a sound test at the scale `r^{2^k}` (Lemma U and its depth-`k`
  version).

**Measured** (`04`): depth 2 removes 94–98% of survivors. Terminal primes are 0–0.1% of
exact survivors.

**Heuristic:** only about `10⁻³ f` of primes could complete a chain. So the true
density of ordinary primes is plausibly 100–1000 times below Algorithm 1's.

**(b) Barriers.**
* Depth `k` is a condition on a number of size `r^{2^{k+1}}`.
* As a sieve problem, depth 1 alone adds about 4 excluded classes per `M₂` prime
  (the roots of `(r²+r+1)² + s(r²+r+1) + s² ≡ 0`). That takes the dimension from
  about 1.9 to about 6.6.
* Selberg's asymptotic loss `2^κ Γ(κ+1)` is then about `2.2·10⁵`, against a gain of
  about 8.
* Parametrising by `P` instead needs the roots of `x²+x+1 mod P` to be equidistributed
  over a sieve-defined set of `P`. That is ineffective where it is known at all.
* The fixed-point and percolation reading (L4) needs *unbounded* depth. Any finite
  depth is exactly this idea at the base.

**(c) Computation.** Depth 2 at the base needs more than 128-bit factoring of
`P²+P+1`. It would take `Λ₀` down by about a further 0.005, which is about ×1.5 in `q`.

**(d) Test run:** `04`. The rates are flat in `x`. A sieve that *saw* depth 1 could
afford a loss of about 30, but the dimension cost above is about 10⁴ times that.

**(e) Probability.** Main question: 0.01. As a base improvement: 0.9, but small.

### Idea 7 — What `σ(3^q)` forces on `q + 1` (question (b))

**(a) Lemma Q (proved).** If an odd prime `ℓ` divides `q+1`, then every prime `t` with
`3^ℓ ≡ 1 (mod t)` divides `σ(3^q)`, and hence divides `N`.

So if some such `t` is known not to divide `N`, then `ℓ ∤ q+1`. "Known not to divide"
covers four kinds of `t`:
* primes below `3·10⁶`;
* primes in `M₂`;
* non-survivors `≡ 2 (mod 3)`;
* a large `t` whose `t²+t+1` has an `M₂` factor, provided `t` cannot be special.

**(b)** This can only ever exclude divisors. `q+1` may be a large prime, or a product of
primes `ℓ` whose `Φ_ℓ(3)` cannot be factored. The paper already needs `q ≥ 2.3·10¹⁰`, so
no size contradiction is possible.

**(d) Test run** (`08_q_plus_1.py`).
* For odd primes `ℓ < 400`, 59 are excluded by a factor of `3^ℓ − 1` below `10⁸`.
* 2 more are excluded by a prime cofactor.
* 16 remain open after that pass. The first are `59, 79, 101`.
* Factoring `(3^ℓ−1)/2` settles `59, 79, 101` too. For `ℓ = 59`,
  `t = 14425532687 ≡ 2 (mod 3)` has `109 | t² + t + 1`, so `t ∤ N`.
* The run was stopped by hand after `ℓ = 163`, which is also excluded (by the factor
  `8882811705390167`). It was then running ECM on a 95-digit cofactor for `ℓ = 199`. So
  every odd prime `ℓ < 199` is excluded as a divisor of `q + 1`: `q + 1` has no prime factor below 199.

**(e) Probability** of a contradiction: < 0.01. Value: congruence information on `q`.

### Idea 8 — Capacity again: `σ(p^e)` is fed by ordinary primes in two residue classes (lead L2)

**(a) Lemma E (proved).** `e = Σ_{s ∈ O} v_p(s² + s + 1) + v_p(σ(3^q))`.

*Proof.* `v_p(σ(N)) = v_p(2N) = e`, and `p ∤ σ(p^e)`. ∎

Also `v_p(σ(3^q)) = v_p(3^{d}−1) + v_p((q+1)/d)` (LTE, with `d = ord_p 3`), which is
`1 + v_p(q+1)` unless `p` is a base-3 Wieferich prime. So

`ln σ(p^e) ≤ ln(2p) + Σ_{s ∈ O_p} ln σ(s²) + ln(p-part of σ(3^q))`, where
`O_p = {s ∈ O : p | s² + s + 1}`, and `O_p` lies in two residue classes mod `p`.

**Corollary (proved).** Every ordinary `t ≡ 5 (mod 12)` has `t | e + 1` or
`p^{t−1} ≡ 1 (mod t²)`. It needs `t² ‖ σ(p^e)` (Corollary B of the notes), and then LTE
applies.

**(b) Why it still fails.** `O_p` can contain arbitrarily large primes. Their abundancy
is negligible, but they buy `σ(p^e)` unlimited capacity, so every counting argument of
Lemma-8 type stays open. The Wieferich-type condition constrains the unknown `p`, which
the argument never fixes.

**(d) Test.** The argument above is the test: the adversary's construction (large
`s ≡ ρ_p (mod p)`) costs nothing in abundancy.

**(e) Probability:** < 0.02.

### Idea 9 — Eisenstein bilinear structure (lead L3)

`r² + r + 1 = N(r − ω)`. Bilinear (Type II) methods, as in Friedlander–Iwaniec or
Heath-Brown, need a two-parameter family. The Eisenstein integers `r − ω` lie on a line
of one parameter.
* A factorisation `r − ω = αβ` imposes the bilinear constraint `ad + bc − bd = −1` on
  `α = a + bω`, `β = c + dω`. That is a thin, Farey-type set with no averaging to exploit.
* Survivors have `r² + r + 1 = m·P` with `P ≈ r²/m`, so there is no balanced
  factorisation to begin with.

**Probability < 0.01.** I did not find a test cheaper than this argument.

---

## 2. The top ideas in full (Ideas 1–3)

### 2.1 The greedy fill

**Setting (proved from the brief's facts).**
* `O ⊂ (3·10⁶, ∞)`, by (F1), since 3 is notable and `p` is special.
* `Σ_{s ∈ O} w(s) > c`. Indeed `∏_{s∈O} σ₋₁(s²) = 2/(σ₋₁(3^q)σ₋₁(p^e))`, with
  `σ₋₁(3^q) < 3/2` and `σ₋₁(p^e) < p/(p−1) ≤ 1 + 1/(6·10⁶)`. The last step uses
  `p ≥ 6,000,033`: `(p+1)/2` is at least the first prime above `3·10⁶`.
  Also `σ₋₁(s²) = 1 + 1/s + 1/s² < s/(s−1)`.
* Write `w⁺(y) = ln(1 + 1/y)`. Every prime `s > y` has `w(s) ≤ w⁺(y)`, and every prime
  `u ≤ y` has `w(u) ≥ ln(y/(y−1)) > w⁺(y)`.

**Lemma G0 (proved).** If `U ⊇ O ∩ (3·10⁶, z]` is a set of primes `≤ z` and
`Λ = Σ_U w < c`, then `|O| > |U| + (c − Λ)/w⁺(z)`.

*Proof.* Let `A = O ∩ (3·10⁶, z] ⊆ U` and `B = O ∖ A`, a finite set of primes `> z`.
Then `|B| w⁺(z) ≥ Σ_B w > c − Σ_A w = c − Λ + Σ_{U∖A} w ≥ c − Λ + |U ∖ A| w⁺(z)`.
So `|O| = |A| + |B| > |A| + |U∖A| + (c−Λ)/w⁺(z)`. ∎

**Lemma G (proved).** Take `y₀ < y₁ < … < y_J` and a set `T ⊇ O ∩ (3·10⁶, y₀]` with
`Σ_T w ≤ Λ₀`. Let `V_j ≥ Σ_{s ∈ O ∩ (y_j, y_{j+1}]} w(s)`. Then

`|O| > |T| + Σ_{j<J} V_j / w⁺(y_j) + (c − Λ₀ − Σ_{j<J} V_j) / w⁺(y_J)`.

*Proof.* Write `n_j` for `|O ∩ (y_j, y_{j+1}]|` and `W_j` for the matching sum of
`w`, so `W_j ≤ V_j` and `n_j ≥ W_j / w⁺(y_j)`. Let `R = O ∩ (y_J, ∞)` and
`A₀ = O ∩ (3·10⁶, y₀]`.
* From the abundancy, `|R| w⁺(y_J) > c − Σ_{A₀} w − Σ_j W_j`.
* Since `A₀ ⊆ T`, we have
  `Σ_{A₀} w ≤ Λ₀ − Σ_{T∖A₀} w ≤ Λ₀ − |T∖A₀| · w⁺(y_J)`.
* Adding up, `|O| = |A₀| + Σ n_j + |R|` exceeds
  `|T| + Σ_j W_j (1/w⁺(y_j) − 1/w⁺(y_J)) + (c − Λ₀)/w⁺(y_J)`.
* Each coefficient `1/w⁺(y_j) − 1/w⁺(y_J)` is negative, so replacing `W_j` by
  `V_j ≥ W_j` only lowers the right side. ∎

Choose `J` to maximise the bound. Upper bounds on the `V_j` are all that is needed. A
larger `V_j` lowers the bound, so sieve upper bounds are sound here.

**Explicit prime estimates used in `01` and `09`** (standard):
* **(RS-a)** `Σ_{p ≤ x} 1/p < ln ln x + B + 1/(2 ln² x)` for `x ≥ 286`.
* **(RS-b)** `Σ_{p ≤ x} 1/p > ln ln x + B − 1/(2 ln² x)` for `x > 1`.
* **(RS-c)** `π(x) > x/ln x` for `x ≥ 17`.

All three are in Rosser–Schoenfeld, *Approximate formulas for some functions of prime
numbers*, Illinois J. Math. 6 (1962). I am confident of the paper and of these
inequalities' form; the exact equation numbers (around (3.17)–(3.20) and (3.5)) should be
checked. The table value `π(10¹²) = 37,607,912,018` is standard.
`Σ_{p>10¹²} (w(p) − 1/p) < 10⁻¹²` is elementary. Dusart's sharper bounds (2010, 2018)
would add a few percent. They are not needed.

### 2.2 The look-ahead base

Lemmas U and P are proved above.

**Soundness of the combination (proved).** Let `T'` be the union of three sets:
* the look-ahead-kept survivors in `(3·10⁶, 3.4·10¹⁰)`;
* the exceptions `E` (`|E| ≤ 2`, all Algorithm-1 survivors);
* the `Q = 2³⁵` superset's survivors in `[3.4·10¹⁰, 10¹²]`.

Then `T' ⊇ O ∩ (3·10⁶, 10¹²]`.
* `|T'|` is at least the kept count plus the superset count.
* `Σ_{T'} w ≤ Λ_LA + (ln A_sup(10¹²) − ln A(3.4·10¹⁰)) + 2 ln(3·10⁶/(3·10⁶−1))`.

Lemma G0 then applies unchanged. `M₂` itself is never enlarged by the look-ahead: a
removed `r` might be one of the exceptions, so it cannot be declared "not dividing `N`".

**Numerics.** `ln A` is accumulated in `long double` with Neumaier compensation, as in
`13`, and each range is padded by `10⁻¹⁵` in `09`.

### 2.3 The weighted Selberg bound (Lemma S; standard)

Sift `n ∈ (x, ρx]` (with `x ≥ ξ`) by the classes `Ω_p = {0, ρ_p, ρ_p²}` for
`p ∈ M₂ ∩ [7, ξ)` and `Ω_p = {0}` for the other `p < ξ`. Use weights `a_n = x/n ∈ (0, 1]`.
* Every Algorithm-1 survivor in `(x, ρx]` avoids all `Ω_p`.
* By Selberg's Λ² method (standard; e.g. Halberstam–Richert, *Sieve Methods*, ch. 3),
  `Σ_n a_n (Σ_{d | P(n)} λ_d)² = Σ_{d,e} λ_d λ_e A_{[d,e]}`, where
  `A_m = X_w ω(m)/m + R_m`, `X_w = x ln ρ`, and `|R_m| ≤ 2ω(m)`. The remainder bound
  holds because `a_n` is monotone and at most 1.
* The optimal `λ` gives main term `X_w / G(ξ)`. The remainder is at most
  `2 (Σ_{d<ξ} ω(d)|λ_d|)² = 2 E₁(ξ)²`, using the standard `|λ_d| ≤ 1` or the sharper
  `|λ_d| ≤ h(d) G(ξ/d)/G(ξ)` that `16c` uses.

Hence `Σ_{r ∈ S ∩ (x, ρx]} 1/r ≤ ln ρ / G(ξ) + 2 E₁(ξ)²/x`, and `w(r) ≤ (1/r)(1 + 1/(r−1))`.

**What is still needed for rigour** (as `16g` notes): write out the λ-bound, use
outward rounding in `G` and `E₁`, and have an independent check. The `M₂` table below
`10⁸` is already exact.

---

## 3. Critique of the whole programme

**Is "`ln A(∞) < c`" plausibly provable with current methods? No.**

**Strongest reason: it needs about 3.9× precision where the best conceivable
unconditional sieve gives 5.4×.** The contradiction must come from the sparsity, at
*every* scale beyond any computation, of a set defined by the full factorisation of
`r² + r + 1`. Past the computed range only upper-bound sieves certify anything. They see
the primes of `M₂` below `D^{1/2}`, where `D` is the level of distribution:
* for primes in progressions, `D ≤ √x` unconditionally (Bombieri–Vinogradov, which is
  not explicit);
* sieving the integers for primality instead costs the parity factor.

`07` measures the best such bound *with no error term*: 5.4× the truth at level `√x`,
3.15× at level `x`. The budget is 3.1–3.9× (about 4–4.5× under the Bateman–Horn tail
model of Idea 5).

Put differently, since 94–98% of survivors are prime pairs `(r, (r²+r+1)/3^a)`, the
programme needs an *explicit* upper bound for a Brun-type constant that beats the best
*non-explicit* twin-prime upper bound constant known to me (about 3.4, Wu 2004). That
problem is decades old and well studied, which makes the difficulty concrete.

**What each strengthening does and does not change.**
* **The look-ahead** changes the *truth* by a factor of about 8 at depth 1 and about
  30–50 at depth 2. It changes nothing a low-dimensional sieve can certify, because it lives in
  the largest prime factor of `r²+r+1`, and no explicit method bounds how often that
  factor falls in a sparse set.
* **Global arguments** fail for the reason the notes already give, now sharpened by
  Lemma E. `σ(p^e)` and `σ(3^q)` absorb any multiplicity demand, and absorbing it costs
  the adversary nothing in abundancy.

**What would change my mind.**
1. An explicit EH-type distribution result for primes in the root classes of
   `x² + x + 1` to moduli near `x`. That would take a major advance.
2. An upper bound for `#{r ≤ x : P⁺(r²+r+1) ∈ 𝒜}` for a set `𝒜` of primes of relative
   density `δ`, of order `δ · π(x)` with a small explicit constant. That is a
   "largest prime factor lies in a thin set" theorem, and I know of none.
3. A completely different contradiction. None of the structures probed here — `q+1`,
   `e`, the Wieferich conditions, mod-4 and mod-8 parities (§5) — yields one.

**How far `q` can be pushed with this framework.**
* `q ≥ 7.6·10¹³` rigorously now.
* About `3·10¹⁵` once Idea 3 is made rigorous.
* A ceiling of about `10^{17}–10^{19}`: the greedy fill gives
  `z* ≈ z₀^{exp((c−Λ₀)/θ)}`, and unconditional sieves keep `θ ≳ 0.5`.

Brute force past `10¹²` is almost worthless for `q`. The no-sieve extension already
achieves the same `d|O|/dz ≈ c − Λ(z)` up to `1.6·10¹⁵`. Compute is better spent
lowering `Λ₀`, as Idea 2 does.

---

## 4. Things in the brief I believe are wrong or misleading

1. **"`q ≥ 1.2·10¹¹` rigorously … the `q` bound grows only linearly in `z`".** The
   rigorous bound from the *same* data is `q ≥ 2.25·10¹³` (Lemma G0, `01`). With the
   look-ahead base of Idea 2 it is `q ≥ 7.6·10¹³` (`09`). The
   `K_max/2` accounting stops at the last computed `z` and leaves out that any superset
   may be counted. With all primes in `(10¹², z]`, `|U| + K` keeps growing until
   `Λ(z) = c` at `z ≈ 1.6·10¹⁵`. For the same reason, brute force beyond `10¹²` buys
   nothing for `q` unless it also lowers `Λ`.
2. **§4 item 2: "Carried from `10¹²`, it projects only `q ≳ 7·10¹²`".** This is below
   the no-sieve bound in item 1. Two accounting losses cause it (`02`):
   * `16d` bounds `Σ 1/r` on `(x, 2x]` by the count bound divided by `x`, which
     overstates the main term by `1/ln 2`;
   * it uses `K_max/2` instead of the greedy fill.

   Corrected, the same tables give `q ≈ 3.1·10¹⁴`. The large-sieve figure
   (`q ≳ 10¹³`) presumably has the same two issues. I did not recompute it.
3. **§3, look-ahead: "special needs `P ≡ 1 (mod 12)` and …".** This is correct, but
   because the special prime is unique, the special branch can rescue at most two `r`
   (Lemma U). The look-ahead is therefore stronger than measured: 85–89% at depth 1,
   94–98% at depth 2, flat in `r` (`04`).
4. **§4, last paragraph: "the allowed factor grows to perhaps 10–20".** That holds only
   for a sieve that sees the look-ahead in the *tail*. For the Algorithm-1 tail sieve,
   the look-ahead acts through the base `Λ₀` alone, and the allowed factor rises only
   from 3.4 to about 3.9.
5. **§4 item 3: "a factor of about 2 is forced by the parity barrier".** True, but it
   hides the larger loss. With the primes as input, and so no parity loss from sieving
   for primality, the ideal ratio is still 5.4 at the BV level (`07`). The level is the
   binding constraint.
6. **Minor.** In the setting, `p > 6·10⁶` can be sharpened to `p ≥ 6,000,033`: `(p+1)/2`
   is at least the least prime above `3·10⁶`, which is 3,000,017. It does not matter
   numerically.

Everything else I checked agrees with the brief. That covers (F1)–(F7), `c`, the §3
table (the `05` runs reproduce `restrained/13` exactly at `10⁹`, `10¹⁰`, `2·10¹⁰` and
`3.4·10¹⁰`), the 90.4% `M₂` share below `10⁸` (`03`: 2,604,985 primes), and the
survival-rate fit.

---

## 5. Smaller observations (recorded so they are not retried)

* **Mod-4 and mod-8.** `σ(N) = 2N` fixes the parity of `#{s ∈ O : s ≡ 1 (mod 4)}` in
  terms of `σ(p^e)/2 (mod 4)`. It is free for the adversary to satisfy.
* **Special candidates are rare.** There are 21,670 below `10⁸`, about 0.8% of the
  primes `≡ 1 (mod 3)` (`03`). Putting them into `M₂` is sound only with a case split
  on `p`. Their effect on the density exponent is about 0.01, which is negligible.
* **Base-3 Wieferich primes** make `v_t(σ(3^q)) ≥ 2` possible without `t | q+1`.
  The known ones, 11 and 1006003, are below `3·10⁶`, so excluded (F1).

---

## 6. Files

| file | what it does | runtime |
|---|---|---|
| `00_ntlib.py` | Miller–Rabin, Pollard–Brent, ECM (copied from `restrained/15`) | — |
| `01_greedy_fill_trivial.py` | Lemma G0 with explicit estimates: `q ≥ 2.25·10¹³` | 0.1 s |
| `02_selberg_reaccount.py` | weighted Selberg + Lemma G from `16c` tables (pilot) | 1 s |
| `03_state.py` | exact Algorithm-1 state below `10⁸` (status byte map) | 3 min |
| `04_lookahead_scaling.py` | look-ahead rates by scale: old, new (Lemma U), depth 2 | ~1 h |
| `05_lookahead_base.c` | exact Algorithm 1 + depth-1 look-ahead (Lemmas U, P) | about 4 core-hours (the slowest piece took 49 min) |
| `06_check_05.py` | independent factoring check of `05` | 20 s |
| `07_level_ideal.py` | ideal Selberg at BV / EH level vs truth | 0.4 s |
| `08_q_plus_1.py` | Lemma Q: which small `ℓ` can divide `q+1` | minutes |
| `09_combine.py` | the `q` bound with the look-ahead base (rigorous + pilot) | 2 s |
| `10_bootstrap_seed.py` | seed for Idea 4 (pilot) | 4 s |
| `11_bh_pairs.c` | Bateman–Horn pairs vs survivors | 1 min |
| `runs/` | raw outputs of `04`, `05` | — |
