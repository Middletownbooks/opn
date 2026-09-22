# Section 3 at `k = 2`: the case `3` ordinary, `3² ‖ N`

Scripts in `s3k2/`, standard library only, no external data.

Setting. `N` is a **2-restrained** odd perfect number: exactly two components
`n₁^{q₁}`, `n₂^{q₂}` have even exponent `q_i ≥ 4` (**notable**), one component
`p^e` has `p ≡ e ≡ 1 (mod 4)` (**special**), and every other component is `x²`
(**ordinary**). Ochem–Zelinsky's restrained case is `k = 1`; this is the next
rung. Following their §3 I assume throughout that **`3` is ordinary**, so
`3² ‖ N` and

    e₃ = Σ_{C ≠ 3²} v₃(σ(C)) = 2   exactly.

---

## 1. The 3-budget is `k`-independent  (`s3k2/01`)

For an ordinary prime `x ≠ 3`,

    v₃(x² + x + 1) = 1 if x ≡ 1 (mod 3),   0 if x ≡ 2 (mod 3),

verified for every prime `5 ≤ x < 4000` (0 failures). So each ordinary prime
`≡ 1 (mod 3)` spends exactly one unit of a budget of 2 and each ordinary prime
`≡ 2 (mod 3)` spends nothing. The notable and special components spend

    v₃(σ(n^q)) = v₃(q+1)          if n ≡ 1 (mod 3),   0 if n ≡ 2 (mod 3), q even
    v₃(σ(p^e)) = v₃(e+1)          if p ≡ 1 (mod 3)
               = v₃(p+1)+v₃(e+1)  if p ≡ 2 (mod 3)   (LTE, e+1 even)

which is `≥ 0` always. Hence, **at any `k`**,

> **at most two ordinary primes are `≡ 1 (mod 3)`.**

Adding notable components can only tighten this, never loosen it. This is the
engine of their §3 and it survives the passage from `k = 1` to `k = 2` intact.

## 2. The regular-support set `T`

`σ(3²) = 13`, so `13 | N`, and `13 ≡ 1 (mod 3)`. Let

* `A` = ordinary primes `≡ 1 (mod 3)`, so `|A| ≤ 2` by §1;
* `T` = **all** primes `≡ 1 (mod 3)` dividing `N` = `A ∪ ({p, n₁, …, n_k} ∩ 1 mod 3)`;
* `U` = ordinary primes `≡ 2 (mod 3)`.

Then `|T| ≤ 2 + (k+1)`: at most **4** when `k = 1`, at most **5** when `k = 2`.
Every prime factor of `x²+x+1` other than 3 is `≡ 1 (mod 3)`, and `3 ∤ x²+x+1`
when `x ≡ 2 (mod 3)`, so for every `x ∈ U` the whole of `σ(x²)` is supported on
`T`.

## 3. The opening tree  (`s3k2/03`)

Semantics that matter: a forced prime may take the ordinary role (forcing the
factors of `σ(x²)`), the special role (once, needs `x ≡ 1 mod 4`, forcing the
odd part of `(x+1)/2`), or the **notable** role — in which case the chain
*stops*, because `σ(n^q)` is not determined. So the set of primes reached under
"no prime is notable" is the candidate set for a notable prime.

* **Layer 1** reproduces Ochem–Zelinsky's set exactly:
  `S = {7, 13, 19, 31, 61, 97, 127, 331}`, tree closes, 0 open branches.
  This holds at **every** `k ≥ 1`: at least one prime of `S` is notable.
* **Layer 2 is negative.** Fix each `s ∈ S` as the first notable and stop the
  chain there; *every* resulting tree stays alive. The branch through `s`
  survives by construction, so no contradiction is available and **the opening
  tree gives no constraint at all on the second notable.**

That negative result is why `k = 2` cannot simply re-run their §3, and it is
what sent me to the abundancy side.

## 4. Why the `k = 1` abundancy argument dies at `|T| = 5`  (`s3k2/04`)

Their §3 finishes by fixing `T` and bounding the `T`-primes by `t/(t−1)`:

| `|T|` | smallest `T` | `13/9 · ∏ t/(t−1)` | room left to 2 |
|---|---|---|---|
| 3 | 7, 13, 19 | 1.927040 | 1.037861 |
| 4 | 7, 13, 19, 31 | 1.991275 | 1.004382 | ← `k = 1` ceiling |
| 5 | 7, 13, 19, 31, 37 | 2.046588 | 0.977236 | ← `k = 2` ceiling |

At `|T| = 4` the bound leaves a factor 1.0044 for the ordinary primes
`≡ 2 (mod 3)` — tight but nonzero, which is why their §3 could be finished once
the factor tree had pinned `T` down. At `|T| = 5` the same bound already exceeds
2 *before a single ordinary prime `≡ 2 (mod 3)` is counted*, so the argument in
that form is vacuous. **`|T| = 5` needs a different obstruction**, and the rest
of these notes supplies one.

---

## 5. The sub-case `|T| = 5`: an exact abundancy identity

`|T| = 5` forces `|A| = 2` **and** `p, n₁, n₂ ≡ 1 (mod 3)`. Consequences:

* the prime divisors of `N` are exactly `{3} ∪ T ∪ U`, with `T = {a₁,a₂,p,n₁,n₂}`;
* the 3-budget is fully spent by `a₁, a₂`, so `v₃(σ(p^e)) = v₃(σ(n_i^{q_i})) = 0`,
  i.e. `e ≢ 2 (mod 3)` and `q_i ≢ 2 (mod 3)` (so `q_i ≡ 0, 4 mod 6`);
* `p ≡ 1 (mod 3)` and `p ≡ 1 (mod 4)` give **`p ≡ 1 (mod 12)`**.

Splitting `σ(N)/N = 2` by component and using `σ(3²)/3² = 13/9` exactly:

> **Identity.** `PROD_T · PROD_U = 18/13`, where
> `PROD_T = ∏_{t∈T} σ(t^{e_t})/t^{e_t}` and `PROD_U = ∏_{x∈U} (1 + 1/x + 1/x²)`.

The `U`-factor is *exact*, not an estimate, because an ordinary component has
exponent exactly 2. That is what makes a two-sided test possible.

### 5a. Lower bound on `PROD_T` — kills small `T`  (test 1, unconditional)

`σ(t^e)/t^e` increases with `e`, so each role has a minimum:

| role | admissible exponents | minimum factor |
|---|---|---|
| special | `e ≥ 1`, `e ≡ 1 mod 4`, and `t ≡ 1 mod 12` | `1 + 1/t` |
| ordinary | exactly 2 | `1 + 1/t + 1/t²` |
| notable | `q ≥ 4` even | `1 + 1/t + 1/t² + 1/t³ + 1/t⁴` |

Minimising over the assignment of one special, two notable and two ordinary
roles gives `minPROD_T(T)`. Since `PROD_U ≥ 1`, **`minPROD_T(T) > 18/13` kills
`T`.** The congruence `p ≡ 1 (mod 12)` matters here: without it only
`{7,13,19,31,37}` dies; with it six sets die
(`{7,13,19,31,37}`, `{7,13,19,31,43}`, `{7,13,19,31,61}`, `{7,13,19,31,67}`,
`{7,13,19,31,73}`, `{7,13,19,37,43}`). Equivalently it bounds `PROD_U` above by
`R(T) = (18/13)/minPROD_T(T)` — typically `1.001` to `1.01`, i.e. the ordinary
primes `≡ 2 (mod 3)` are forced to be **large and few**.

### 5b. Upper bound — kills large `T`  (test 2, unconditional)

`PROD_T < g(T) = ∏_{t∈T} t/(t−1)` for any exponents. For the other factor, every
`x ∈ U` has `σ(x²) = x²+x+1` supported on `T`, so

    U ⊆ Sm(T) = { x prime, x ≡ 2 (mod 3), x²+x+1 is T-smooth },
    PROD_U ≤ h(T) = ∏_{x ∈ Sm(T), x ≥ 5} (1 + 1/x + 1/x²).

> **`g(T) · h(T) ≤ 18/13` kills `T`.**

`Sm(T)` is computed *exactly* below a bound `Y` by running over all `T`-smooth
`M ≤ Y` and testing whether `4M − 3` is a perfect square (`x²+x+1 = M` is
solvable iff it is). The terms above `Y` are bounded unconditionally:

> **Tail lemma.** If `x²+x+1 = M > Y` then `x > √M − 1`, and distinct `x` give
> distinct `M`. For any `0 < ε < 1/2`, since `M > Y` implies `1 ≤ (M/Y)^ε`,
>
>     Σ_{M T-smooth, M > Y} M^{−1/2} ≤ Y^{−ε} · ∏_{t∈T} (1 − t^{ε−1/2})^{−1}
>
> the right-hand product being the full Euler product, which converges.

With `Y = 10²⁴` the optimised bound is below `2.2 · 10⁻⁷` for every `T` tested,
so `h(T) ≤ (head product) · exp(1.000001 · tail)` is a genuine upper bound. **No
Thue–Mahler input and no completeness assumption enter test 2.**

### 5c. The counting test  (test 3, conditional)

`ω(N) = 1 + |T| + |U| = 6 + |U|`, and `ω(N) ≥ 10` (Nielsen 2007), so `|U| ≥ 4`.
With `U ⊆ Sm(T)` and `PROD_U ≤ R(T)`, the **four largest** members of `Sm(T)`
must already fit inside `R(T)`. This test assumes `Sm(T)` has no member beyond
the search bound. `Sm(T)` *is* finite — `x²+x+1 = T`-smooth is a Thue–Mahler
equation for the form `X²+XY+Y²` — but I have not enumerated it completely, so
test 3 is tallied separately and its verdicts are **conditional**.

### 5d. Results  (`s3k2/09`, `s3k2/10`)

Over all `5`-subsets `T` of the primes `≡ 1 (mod 3)` below 200 containing 13
(4845 sets), with `Y = 10²⁴`:

| test | assumes | eliminated |
|---|---|---|
| 1 — `minPROD_T > 18/13` | nothing | 6 |
| 2 — `g·h ≤ 18/13` | nothing | 3708 |
| | | **3714 (76.7%) unconditionally** |
| 3 — `ω ≥ 10` + `Sm(T)` complete | see 5c | 1131 |
| | | **0 survive** |

The 1131 sets that need test 3 are overwhelmingly those containing
`{7, 13, 19, 31}`, because `Sm(T)` is then rich at the bottom
(`5 → 31`, `11 → 7·19`, `191 → 7·13·31`, `653 → 7·13·19`). For those, test 1
gives `R(T) ≈ 1.003`, so `U` can contain at most one of the known members of
`Sm(T)`, and `ω(N) ≥ 10` then demands at least three solutions of
`x²+x+1 = T`-smooth with `x > 10¹²`.

A wider sweep (pool below 400, 58905 sets) is in `s3k2/` as the same script with
argument `400`.

---

## 6. Status

* **Unconditional, new:** the two-sided fixed-support test for `|T| = 5`, with
  the rigorous tail lemma, and its 76.7% elimination rate over the pool below
  200. The identity `PROD_T · PROD_U = 18/13` and the role minima are exact.
* **Conditional:** total elimination of `|T| = 5` over that pool, modulo
  completeness of the Thue–Mahler solution sets `Sm(T)` (searched to `x ≤ 10¹²`)
  and `ω(N) ≥ 10`.
* **Not done:** `|T| ≤ 4` at `k = 2`. That is the shape their §3 closes at
  `k = 1`, but with two notables the role assignment changes and the opening
  tree (§3 above) supplies nothing about the second one. Also not done: `T` with
  a prime above the sweep's pool bound — the test is finite in `T` only because
  the pool is, and a cutoff argument for `max(T)` large is missing.

## 7. What would finish it

1. A Thue–Mahler solve (PARI/Magma) of `x²+x+1 = ∏_{t∈T} t^{c_t}` for the 1131
   sets, which would make the `|T| = 5` elimination unconditional.
2. A cutoff on `max(T)`: show that `g(T)·h(T) ≤ 18/13` whenever `T` contains a
   prime above some explicit bound. Heuristically clear — a large `t` adds
   almost nothing to `g` and can only add `x` with `t | x²+x+1` to `Sm(T)` — but
   it needs a proof.
3. The `|T| ≤ 4` sub-cases.
