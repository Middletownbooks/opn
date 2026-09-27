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

`ω(N) = 1 + |T| + |U| = 6 + |U|`, and `ω(N) ≥ 10` (Nielsen 2015), so `|U| ≥ 4`.
With `U ⊆ Sm(T)` and `PROD_U ≤ R(T)`, the **four largest** members of `Sm(T)`
must already fit inside `R(T)`. This test assumes `Sm(T)` has no member beyond
the search bound. `Sm(T)` *is* finite — `x²+x+1 = T`-smooth is a Thue–Mahler
equation for the form `X²+XY+Y²` — but I have not enumerated it completely, so
test 3 is tallied separately and its verdicts are **conditional**.

### 5d. Results  (`s3k2/09`, `s3k2/10`)

Over all `5`-subsets `T` of the primes `≡ 1 (mod 3)` below a bound containing 13,
with `Y = 10²⁴`:

| pool | sets | test 1 | test 2 | unconditional | needs test 3 | alive |
|---|---|---|---|---|---|---|
| `< 200` | 4845 | 6 | 3708 | **3714 (76.7%)** | 1131 | **0** |
| `< 400` | 58905 | 6 | 51672 | **51678 (87.7%)** | 7227 | **0** |

The sets that need test 3 are overwhelmingly those containing `{7, 13, 19, 31}`,
because `Sm(T)` is then rich at the bottom (`5 → 31`, `11 → 7·19`,
`191 → 7·13·31`, `653 → 7·13·19`). For those, test 1 gives `R(T) ≈ 1.003`, so
`U` can contain at most one of the known members of `Sm(T)`, and `ω(N) ≥ 10`
then demands at least three solutions of `x²+x+1 = T`-smooth with `x > 10¹²`.

---

## 5½. The other sub-cases of §3, and the full sweep  (`s3k2/12`)

`|T| = 5` is only the top rung. Writing `β` for the number of big components
(`p^e`, `n₁^{q₁}`, `n₂^{q₂}`) that are `≡ 1 (mod 3)` and `W` for the ones that are
`≡ 2 (mod 3)`, we have `τ = |T| = α + β` and `|W| = 3 − β`, and the prime
divisors of `N` are exactly `{3} ∪ T ∪ W ∪ U`. The identity generalises to

    PROD_T · PROD_W · PROD_U = 18/13.

The 3-budget gives one extra constraint. A notable `w ≡ 2 (mod 3)` with even
exponent contributes `v₃(σ(w^q)) = 0`, but the special `p ≡ 2 (mod 3)` has
`e+1` even and `3 | p+1`, so by LTE it contributes `v₃(p+1) + v₃(e+1) ≥ 1`.
Hence

> `α + [the special lies in W] ≤ 2`,

which kills the profiles with `α = 2` and the special `≡ 2 (mod 3)` outright.
The special prime is `≡ 1 (mod 12)` when it lies in `T` and `≡ 5 (mod 12)` when
it lies in `W`.

`W` is handled without truncation: each of its `|W|` slots is either an explicit
prime `≡ 2 (mod 3)` below `WB = 500`, or an unknown prime `≥ WB`, which
contributes `1` to the lower bound and at most `WB/(WB−1) = 1.002004` to the
upper bound. Small `w` is killed by test 1 (a notable `5` forces
`PROD_W ≥ 1.2496`, leaving only `1.108` for `PROD_T · PROD_U`); large `w` is
killed by test 2, because its upper-bound slack tends to 1. A `(T, W)`
configuration survives only if no test fires, and a set `T` survives only if
some configuration survives.

Test 3 generalises cleanly: `ω(N) = 1 + τ + |W| + |U| = 4 + α + |U| ≥ 10`, so
**`|U| ≥ 6 − α ≥ 4` in every sub-case**, and `U ⊆ Sm(T) \ W`.

### Results of the full sweep  (`s3k2/12`, pool `< 400`, `WB = 500`)

| `τ` | `α` | special in `T` | notables in `T` | `\|W\|` | sets | unconditional | needs test 3 | alive |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | no | 1 | 2 | 1 | 0 | 1 | 0 |
| 2 | 0 | no | 2 | 1 | 36 | 30 | 6 | 0 |
| 1 | 0 | yes | 0 | 2 | 1 | 0 | 1 | 0 |
| 2 | 0 | yes | 1 | 1 | 36 | 30 | 6 | 0 |
| 3 | 0 | yes | 2 | 0 | 630 | 594 | 36 | 0 |
| 1 | 1 | no | 0 | 3 | 1 | 0 | 1 | 0 |
| 2 | 1 | no | 1 | 2 | 36 | 0 | 36 | 0 |
| 3 | 1 | no | 2 | 1 | 630 | 428 | 202 | 0 |
| 2 | 1 | yes | 0 | 2 | 36 | 1 | 35 | 0 |
| 3 | 1 | yes | 1 | 1 | 630 | 489 | 141 | 0 |
| 4 | 1 | yes | 2 | 0 | 7140 | 6509 | 631 | 0 |
| 3 | 2 | yes | 0 | 2 | 630 | 85 | 545 | 0 |
| 4 | 2 | yes | 1 | 1 | 7140 | 5036 | 2104 | 0 |
| 5 | 2 | yes | 2 | 0 | 58905 | 51678 | 7227 | 0 |
| **all** | | | | | **75852** | **64880 (85.5%)** | 10972 | **0** |

The profiles with `α = 2` and the special `≡ 2 (mod 3)` never appear: the
budget inequality rules them out before any computation.

---

## 5⅔. Interval narrowing: 98% unconditional  (`s3k2/14`, `s3k2/15`)

The crude upper bound `g(T) = ∏ t/(t−1)` throws away two things. First, an
ordinary component has exponent *exactly* 2, so it is capped at `1+1/t+1/t²`,
well below `t/(t−1)`; write

    g*(T) = max over role assignments of ∏_{ordinary}(1+1/t+1/t²) · ∏_{special,notable} t/(t−1).

Second, and more importantly, the two bounds feed each other. Put
`P = PROD_T · PROD_W`, so `P · PROD_U = 18/13` with `LO ≤ P < HI`. Given a lower
bound `LO`, we get `PROD_U ≤ R = (18/13)/LO`, so **every** `x ∈ U` must satisfy
`1 + 1/x + 1/x² ≤ R` *on its own*: the small members of `Sm(T)` are excluded
from `U` outright. That shrinks `H`, which raises `LO`, and one iterates:

    R ← (18/13)/LO ;   Sm*(T) ← { x ∈ Sm(T)\W : 1+1/x+1/x² ≤ R } ;
    H ← ∏_{Sm*(T)} (1+1/x+1/x²) · exp(tail) ;   LO ← max(LO, (18/13)/H).

`LO` is non-decreasing, so this converges. **`LO ≥ HI` kills `T` outright**, and
this criterion subsumes the earlier `g·h ≤ 18/13`. It stays unconditional:
dropping members of `Sm(T)` only shrinks `H` and raises `LO`, i.e. only makes
the test claim more, so the unknown part of `Sm(T)` is bounded in the *upward*
direction by the Euler-product tail, and `H` is rounded up before use.

For `|T| = 5` over the pool below 200 this lifts the unconditional share from

| test | unconditional kills of 4845 |
|---|---|
| crude two-sided (`g·h ≤ 18/13`) | 3714 (76.7%) |
| **interval narrowing** | **4764 (98.3%)** |

leaving 81 sets, all of them containing `{7, 13, 19}` — the sets where `Sm(T)`
is rich at the bottom.

Run over the whole of §3 at `k = 2` with the pool below 400, it replaces the
table of §5½ with this one:

| `τ` | `α` | sp in `T` | nt in `T` | `\|W\|` | sets | unconditional | needs test 3 | alive |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | no | 1 | 2 | 1 | 0 | 1 | 0 |
| 2 | 0 | no | 2 | 1 | 36 | 31 | 5 | 0 |
| 1 | 0 | yes | 0 | 2 | 1 | 0 | 1 | 0 |
| 2 | 0 | yes | 1 | 1 | 36 | 32 | 4 | 0 |
| 3 | 0 | yes | 2 | 0 | 630 | 621 | 9 | 0 |
| 1 | 1 | no | 0 | 3 | 1 | 0 | 1 | 0 |
| 2 | 1 | no | 1 | 2 | 36 | 0 | 36 | 0 |
| 3 | 1 | no | 2 | 1 | 630 | 461 | 169 | 0 |
| 2 | 1 | yes | 0 | 2 | 36 | 1 | 35 | 0 |
| 3 | 1 | yes | 1 | 1 | 630 | 565 | 65 | 0 |
| 4 | 1 | yes | 2 | 0 | 7140 | 7134 | 6 | 0 |
| 3 | 2 | yes | 0 | 2 | 630 | 115 | 515 | 0 |
| 4 | 2 | yes | 1 | 1 | 7140 | 6046 | 1094 | 0 |
| 5 | 2 | yes | 2 | 0 | 58905 | 58653 | 252 | 0 |
| **all** | | | | | **75852** | **73659 (97.11%)** | 2193 | **0** |

So `|T| = 5`, the sub-case that looked hopeless from the `k = 1` argument,
ends up being the *easiest*: 58653 of 58905 sets die with no unproved input, and
only 252 need the conditional step. What remains conditional is concentrated in
the small-`τ`, large-`|W|` profiles, where the unknown big components `≡ 2 (mod 3)`
carry most of the abundancy and `T` is too thin for `Sm(T)` to bite.


---

## 5¾. A cutoff for `max(T)`  (`s3k2/13`)

The sweeps are finite only because the pool is. Here is the reduction that would
make them exhaustive. Let `T = T' ∪ {t*}` with `t* ≥ B` and `T'` inside the pool.
Then `g(T) ≤ g(T') · B/(B−1)`, and every `x ∈ Sm(T) \ Sm(T')` has
`x²+x+1 = t*^c · M'` with `c ≥ 1` and `M'` `T'`-smooth, so by the same Euler
product as the tail lemma,

    Σ_{x ∈ Sm(T)\Sm(T')} 1/x  ≤  (1 + 1/(√B − 1)) · (u/(1−u)) · ∏_{t∈T'} (1 − t^{−1/2})^{−1},
    u = B^{−1/2}.

| `B` | `Σ` bound (for `T' = {7,13,19,31}`) | total correction to `g·h` |
|---|---|---|
| `10³` | 1.19e−1 | 1.128459 |
| `10⁶` | 3.53e−3 | 1.003569 |
| `10⁸` | 3.52e−4 | 1.000356 |
| `10¹²` | 3.52e−6 | 1.000004 |

So a finite check on the `4`-subsets below `B = 10⁸` that clears `18/13` by a
factor `1.0004` would kill every `|T| = 5` set with `max(T) ≥ 10⁸` at a stroke.
**That check does not currently pass**: the `|T| = 4` sweep clears tests 1–2 for
91.2% of the 4-subsets below 400, not all of them. So this is the missing
ingredient, not a completed step — but it shows the gap is finite and explicit,
not open-ended.

---

## 6. Status

* **Unconditional and new:** the two-sided fixed-support test — the exact
  identity `PROD_T · PROD_W · PROD_U = 18/13`, the role minima, the `p ≡ 1 mod 12`
  / `p ≡ 5 mod 12` split, the budget inequality `α + [special ∈ W] ≤ 2`, and the
  tail lemma that makes `h(T)` a genuine upper bound with no Thue–Mahler input.
  This eliminates the large majority of every sub-case with no unproved premise.
* **Conditional:** total elimination of §3 at `k = 2` over the stated pools,
  modulo (i) `ω(N) ≥ 10` (Nielsen 2015, a theorem, cited) and (ii) completeness
  of the Thue–Mahler solution sets `Sm(T)`, searched only to `x ≤ 10¹²`.
* **Not done:** `T` containing a prime above the pool bound. §5¾ reduces that
  infinite family to an explicit finite check, but the check does not yet pass.
* **Not done:** the `k = 2` analogue of their §4, i.e. `3` notable. §2 (`3 ∤ N`)
  was closed separately; §3 is this file; `3` notable is untouched.

## 7. What would finish it

1. A Thue–Mahler solve (PARI/Magma) of `x²+x+1 = ∏_{t∈T} t^{c_t}` for the sets
   that reach test 3. That alone makes the whole sweep unconditional apart from
   the cited `ω(N) ≥ 10`.
2. Strengthening the `|T| ≤ 4` upper test enough for the `max(T)` cutoff of §5¾
   to fire at `B = 10⁸`; then the pool restriction disappears.
3. `3` notable at `k = 2`.

---

## 8. Making the cutoff recursive  (`s3k2/16`–`19`)

The pool restriction of §5½–5⅔ is the largest caveat, and §5¾ showed the cutoff
reduces `|T| = 5` with `max(T) ≥ B` to a finite check at size 4. The natural
move is to apply the same cutoff at every level. Work in the branch `α = 2`,
`|W| = 0`, so `|T| = 5` with role multiset `(o,o,s,n,n)`; a subset `S ⊆ T`
carries a sub-multiset of those roles, and

    margin(S) = LO(S)/HI(S)   (after interval narrowing),
    B(S) = min { B : corr(B,S) ≤ margin(S) }.

Since `corr(B,S) → 1`, any `S` with `margin(S) > 1` has a **finite** `B(S)`, and
every `T` with `T \ {max T} = S` and `max(T) ≥ B(S)` dies. So building upward by
the largest element,

    live_{L+1} = { S ∪ {t} : S ∈ live_L, max(S) < t < B(S) }.

`min(T)` is 7 or 13 (the two smallest primes `≡ 1 mod 3`, and `13 ∈ T` always),
so the recursion has exactly two seeds.

### 8a. Level 4 is already tiny

At the `B = 10⁸` margin, only **7 of the 7140** 4-subsets below 400 fail to
clear (`s3k2/16`). Run from the bottom (`s3k2/17`) the recursion terminated with
a single exceptional seed, `{13, 31}`, at `margin = 0.997482` — a quarter of a
percent short.

### 8b. The forced-prime filter  (`s3k2/18`)

The binding role assignment for `{13,31}` was *13 special with `e = 1`*, giving
`(14/13)·(993/961) = 1.1127705`. But `σ(p^e) = (1+p)(1+p²+⋯+p^{e−1})` for odd
`e`, so **every odd prime factor of `p+1` divides `N`** — routine, and the same
opening move as Ochem–Zelinsky's Lemma 6. Here `σ(13) = 14 = 2·7` forces
`7 | N`, contradicting `min(T) = 13`. More sharply, `13 ≡ −1 (mod 7)` and `e` is
odd, so `7 | σ(13^e)` for **every** admissible `e`:

> On the branch `7 ∤ N`, the prime 13 cannot be the special prime at all.

Generally, an exponent `k` is inadmissible for `t^k` with `t ∈ T` whenever
`σ(t^k)` has a prime factor `≡ 1 (mod 3)` below `min(T)` — that factor would be
a `T`-prime smaller than the smallest one. Detecting it costs only trial
division by a handful of small primes, never a factorisation of `σ(t^k)`.

This raises `LO₀({13,31})` from `1.1127832` to `1.1188974`, past the threshold
`1.1166324` at which `5` (whose `σ(25) = 31`) drops out of `Sm*`. `H` then
collapses to ≈ 1, `LO` jumps to ≈ `18/13`, and the exception closes.

### 8c. The recursion with the filter  (`s3k2/19`)

| level | sets to consider |
|---|---|
| 1 | 2 — the seeds `{7}`, `{13}` |
| 2 | 6 |
| 3 | 91 |
| 4 | 4324 |
| 5 | 1 015 872 |

with thresholds `B({7}) = 139.5`, `B({13}) = 63.4`, `B({7,13}) = 727.4`,
`B({13,19}) = 138.5`, `B({13,31}) = 105.9`. Six exceptional 4-sets remain, all
containing `{7,13}`, with margins just below 1:

| `S` | margin |
|---|---|
| `{7,13,19,31}` | 0.997627 |
| `{7,13,31,79}` | 0.996091 |
| `{7,13,31,307}` | 0.991151 |
| `{7,13,67,79}` | 0.991183 |
| `{7,13,67,307}` | 0.991181 |
| `{7,13,79,307}` | 0.991183 |

### 8d. Honest status of §8

The structure works — the cutoff **is** recursive, and the tree is small through
level 4. Two things are not finished:

1. **The level-5 enumeration is truncated.** Some level-4 thresholds exceed the
   script's prime bound `10⁷`, so the 1 015 872 figure is a lower bound on that
   family, not the family. The sets are individually cheap to test (~20 ms), so
   this is compute, not mathematics — but it has not been run.
2. **Six exceptional 4-sets have no cutoff.** Each spawns a one-parameter family
   `S ∪ {t*}` that the unconditional test cannot kill for large `t*`, because
   `margin(S) < 1` persists in the limit. All six are within 0.9% of closing, and
   the `{13,31}` precedent shows where the margin can come from: a sharper
   admissible-exponent filter, or the forced primes of `σ(t²)` for the ordinary
   `T`-primes (e.g. `31` ordinary forces `331 ∈ T` via `σ(31²) = 3·331`).

So §8 is a method that demonstrably works, carried far enough to show the pool
restriction is removable in principle, and stopped short of removing it.

---

## 9. The ordinary-closure filter  (`s3k2/20`–`23`)

The six exceptions of §8c all had `margin` just under 1, so what was needed was
a constraint of a different kind, not a tighter estimate. The forcing tree
supplies one, and it becomes a condition on the finite set `T`.

> **Closure condition.** An ordinary component has exponent *exactly* 2, so
> `σ(t²) = t²+t+1` is completely determined. Every prime factor of it divides
> `2N`, is odd, and is `3` or `≡ 1 (mod 3)` — and for `t ≡ 1 (mod 3)` exactly one
> factor 3 occurs. Writing `F(t)` for the prime factors of `t²+t+1` that are
> `≡ 1 (mod 3)`,
>
>     t ∈ T ordinary  ⟹  F(t) ⊆ T.

`|T| = 5`, so this is severe:

| `t` | `F(t)` | `t` | `F(t)` |
|---|---|---|---|
| 7 | {19} | 67 | {7, 31} |
| 13 | {61} | 79 | {7, 43} |
| 19 | {127} | 97 | {3169} |
| 31 | {331} | 127 | {5419} |
| 37 | {7, 67} | 163 | {7, 19, 67} |
| 61 | {13, 97} | 307 | {43, 733} |

In the recursion, `S` is always the set of the `|S|` **smallest** elements of
`T` — each level appends a new maximum — so every element of `T \ S` exceeds
`max(S)`. That sharpens the condition at every level:

* `f ∈ F(t)` with `f < max(S)` and `f ∉ S` → the assignment is impossible;
* `|⋃F(t) \ S|` must not exceed `5 − |S|`.

### 9a. Effect on the exceptions

| `S` | margin without closure | with closure | verdict |
|---|---|---|---|
| `{7,13,19,31}` | 0.997627 | 0.997627 | still no cutoff |
| `{7,13,31,79}` | 0.996091 | 0.996122 | still no cutoff |
| `{7,13,31,307}` | 0.991151 | 0.994024 | still no cutoff |
| `{7,13,67,79}` | 0.991183 | — | **no role assignment at all** |
| `{7,13,67,307}` | 0.991181 | — | **no role assignment at all** |
| `{7,13,79,307}` | 0.991183 | — | **no role assignment at all** |

Three die immediately. For the other three the filter acts one level up, where
it pins the fifth prime down (`s3k2/21`). Splitting on which two elements of `T`
are ordinary:

* **Case A**, both ordinary primes in `S`: `⋃F` must fit in `T`, so at most one
  new prime, which *is* `t*`.
* **Case B**, `t*` ordinary: then `F(t*) ⊆ T`, and since `t* ∤ t*²+t*+1` this says
  `(t*²+t*+1)/3` is `S`-smooth — enumerated exactly by the same `4M−3`-is-a-square
  device.

| `S` | admissible fifth primes |
|---|---|
| `{7,13,19,31}` | 61, 67, 127, 331 — **four explicit sets** |
| `{7,13,31,79}` | none |
| `{7,13,31,307}` | none |

For `{7,13,19,31}`: `{7,13}` ordinary forces `t* = 61`, `{7,19}` forces 127,
`{7,31}` forces 331, the pairs `{13,19}`, `{13,31}`, `{19,31}` each need two new
primes and die, and case B gives `t* = 67`. All four resulting sets lie inside
the pool already swept in §5⅔. **So none of the six exceptions is an infinite
family after all** — the closure filter converts each into a finite, explicit
list or nothing.

### 9b. Effect on the recursion  (`s3k2/22`)

Re-running the whole recursion with both filters:

| level | without closure | with closure |
|---|---|---|
| 2 | 6 | 6 |
| 3 | 91 | 91 |
| 4 | 4324 | 4324 (1378 of them now outright dead) |
| 5 | 1 015 872 (truncated) | **485 064** |
| exceptions | 6 | **3**, and §9a finishes those |

The level-5 list is no longer truncated: the largest prime it reaches is
1 145 371, well inside the script's bound. The closure condition is weak while
`|S|` is small (there is slack for `5 − |S|` further primes) and becomes decisive
at `|S| = 4` and `5`, which is exactly where the recursion needed help.

### 9c. Remaining gap in §9

Case B's enumeration searched `(t*²+t*+1)/3` `S`-smooth up to `3·10²⁸`, i.e.
`t* ≲ 10¹⁴`. Absence of solutions above that is the same Thue–Mahler statement
as the `Sm(T)` completeness of §5c, and is not proved here. It is a *finiteness*
question, not an unbounded one.

---

## 10. The level-5 pass: the branch closes  (`s3k2/23`, `s3k2/24`)

Testing every one of the 485 064 five-sets the recursion of §9b cannot discard:

| outcome | count |
|---|---|
| dead: no role assignment passes closure | 481 385 |
| dead: interval narrowing (unconditional) | 3 674 |
| **eliminated with no unproved input** | **485 059 (100.00%)** |
| dead: `ω ≥ 10` + `Sm(T)` complete (conditional) | 5 |
| **still alive** | **0** |

So on the branch `α = 2`, `|W| = 0` — 3 ordinary, `3² ‖ N`, and the special and
both notables all `≡ 1 (mod 3)` — §3 at `k = 2` closes **with no pool
restriction**. The recursion of §8 supplies the infinite tail and the closure
filter of §9 supplies the finite core; five explicit 5-sets are all that need
the conditional step, and `s3k2/24` names them.

The closure filter does the bulk of the work at this level (481 385 of 485 064),
which is the expected shape: at `|S| = 5` there is no slack left, so `F(t) ⊆ T`
must hold exactly for both ordinary primes.

### 10a. What this does and does not settle

* **Settled, unconditionally except for five named sets:** one of the fourteen
  role profiles of §3 at `k = 2`, for *all* `T`, not just `T` inside a pool.
* **Not settled:** the other thirteen profiles (`α < 2`, or some big component
  `≡ 2 (mod 3)`), which were swept only over the pool below 400. Each needs its
  own recursion. The large-`|W|` ones are where this method is weakest: the
  unknown components `≡ 2 (mod 3)` carry most of the abundancy and `T` is too
  thin for the smoothness constraint to bite.
* **Two Thue–Mahler tails**, both finiteness statements: `Sm(T)` complete beyond
  `x ≤ 10¹²` (§5c), and case B's `(t*²+t*+1)/3` `S`-smooth beyond `t* ≲ 10¹⁴`
  (§9c).

### 10b. The five residual sets, named  (`s3k2/24`, `s3k2/25`)

| `T` | `Sm(T)` | admissible for `U` under `R(T)` |
|---|---|---|
| `{7, 13, 19, 37, 67}` | 11, 29, 653 | 653 |
| `{7, 13, 19, 37, 127}` | 11, 107, 653 | 107, 653 |
| `{7, 13, 19, 43, 127}` | 11, 107, 653 | 107, 653 |
| `{7, 13, 19, 127, 409}` | 11, 53, 107, 653 | 53, 107, 653 |
| `{7, 13, 19, 127, 1723}` | 11, 41, 107, 653 | 41, 107, 653 |

All five fail for the same reason: `ω(N) ≥ 10` forces `|U| ≥ 4`, and fewer than
four members of `Sm(T)` are admissible. So the residual assumption is exactly
**five explicit Thue–Mahler statements** — that `x²+x+1 = ∏_{t∈T} t^{c_t}` has no
solution with `x > 10¹²` for these five sets. Nothing else on this branch is
conditional.

All five contain `{7, 13, 19}`, and the closure condition pins the roles almost
completely — for `{7,13,19,37,67}` to a single assignment (ordinary `{7,37}`,
special 13, notables `{19,67}`).

**A valuation sharpening** (`s3k2/25`). An ordinary prime `a` has exponent
exactly 2, so `2 = e_a = Σ_C v_a(σ(C))`. Two contributions are forced and
computable: the other ordinary prime `b` contributes `v_a(b²+b+1)`, and the
special `p` contributes at least one whenever `p ≡ −1 (mod a)` — because `e` is
odd, so `e+1` is even and `ord_a(p) = 2` divides it. (Same mechanism as
`7 | σ(13^e)` in §8b.) When those two already account for both units,
`Σ_{x∈U} v_a(x²+x+1) = 0`, so no member of `U` may be divisible by `a`.

For `{7,13,19,37,67}` this fires: `v₇(σ(37²)) = v₇(1407) = 1` and `13 ≡ −1
(mod 7)`, so `e₇ = 2` is already spent and `U` may contain no `x` with
`7 | x²+x+1` — which deletes 11 and 653, leaving only 29. The other four sets
admit a role assignment on which the balance does not close, so the deletion does
not apply to them; the union over admissible assignments is what the table's
last column shows. The sharpening therefore shrinks the Thue–Mahler problem
without eliminating it.

---

## 11. The `|W| ≥ 1` profiles: closure plus a count  (`s3k2/26`, `s3k2/27`)

After §10 the open part of §3 at `k = 2` was the thirteen profiles other than
`α = 2`, `|W| = 0`. My earlier reading — that the large-`|W|` ones are where this
machinery is thinnest — was only half right. It is true of the *abundancy* test:
`W`'s unknown components `≡ 2 (mod 3)` carry the slack there. It is the reverse
for the *smoothness* side, because the budget inequality forces small `T`:

    |W| = 3 ⟹ β = 0 ⟹ τ = α ≤ 1 ;      |W| = 2 ⟹ β = 1 ⟹ τ = α + 1 ≤ 3.

and `Sm(T) = { x prime, x ≡ 2 (mod 3) : x²+x+1 is T-smooth }` is an equation in
`|T|` primes. The count of `T`-smooth numbers below `Y` grows like `(log Y)^{|T|}`,
so a small `|T|` buys orders of magnitude in the search exponent.

| | `|W| = 0`, `α = 2` (§10) | `|W| ≥ 1` (here) |
|---|---|---|
| `|T|` | 5 | ≤ 4, and ≤ 3 once `|W| ≥ 2` |
| abundancy test | decisive | weak |
| `Sm(T)` searched to | `10²⁴` | `10⁴⁸` (`|T|=3`), `10¹⁶⁰` (`|T|=2`), `10⁴⁰⁰` (`|T|=1`) |
| what finishes it | interval narrowing + closure | **closure + a pure count** |

### 11a. The count

`ω(N) = 1 + τ + |W| + |U| = 4 + α + |U|`, so `ω(N) ≥ 10` (Nielsen 2015) gives

> `|U| ≥ 6 − α ≥ 4`,   and `U ⊆ Sm(T)`.

A profile dies at `T` whenever `|Sm(T)| < 6 − α`. No abundancy input at all.
`T` itself is pinned by the closure condition of §9: an ordinary `t ∈ T` needs
`F(t) ⊆ T`, and with `τ ≤ 3` that usually determines `T` outright instead of
leaving a pool.

### 11b. `|W| = 3` dies in three lines, unconditionally

That profile turned out not to need any computation:

> `|W| = 3` means all three big components are `≡ 2 (mod 3)`, so `β = 0` and
> `τ = α`. The special `p` is then `≡ 2 (mod 3)`, so `3 | p+1`, `3 ∤ p−1`, and
> `e+1` is even, whence `3 | σ(p^e)` — one unit of the 3-budget — so `α ≤ 1`.
> But `13 | N` (from `σ(3²) = 13`) and `13 ≡ 1 (mod 3)`, so `T ≠ ∅` and `α = 1`:
> `T = {13}` with **13 ordinary**. Then `σ(13²) = 183 = 3 · 61` forces `61 | N`,
> and `61 ≡ 1 (mod 3)` would have to lie in `T = {13}`. Contradiction. ∎

No `ω` bound, no smoothness, no abundancy, no pool. The script reports it as
"0 admissible `T`" in the closure column.

### 11c. Single-prime `Sm`  (`s3k2/26`)

For `|T| = 1` the smoothness condition is `x²+x+1 = p^c`, settled exactly by
testing whether `4p^c − 3` is a square, for every `c ≤ 1200` (for `p = 13` that
is `p^c` up to about `10¹³³⁵`). Every solution in range comes from `c = 1` —
`x = 2, 3, 5, 6, 8, 12`, plus `x = 18` at `c = 3` for `p = 7`. Only `x = 5` is
both prime and `≡ 2 (mod 3)`, so `Sm({31}) = {5}` and every other single-prime
`Sm(T)` is **empty**; in particular `Sm({13}) = ∅`, its one solution `x = 3`
being `≡ 0 (mod 3)`.

### 11d. Results so far

| `α` | sp in `T` | nt in `T` | `τ` | `|W|` | `|U|` needed | admissible `T` | survive |
|---|---|---|---|---|---|---|---|
| 0 | no | 1 | 1 | 2 | 6 | 1 | 0 |
| 0 | no | 2 | 2 | 1 | 6 | 49 | 0 |
| 0 | yes | 0 | 1 | 2 | 6 | 1 | 0 |
| 0 | yes | 1 | 2 | 1 | 6 | 49 | 0 |
| 1 | no | 0 | 1 | 3 | 5 | **0** | 0 |
| 1 | no | 1 | 2 | 2 | 5 | 1 | 0 |
| 1 | no | 2 | 3 | 1 | 5 | 1141 | 0 |
| 1 | yes | 0 | 2 | 2 | 5 | 1 | 0 |
| 1 | yes | 1 | 3 | 1 | 5 | 1141 | 0 |
| 2 | yes | 0 | 3 | 2 | 4 | *running* | |
| 2 | yes | 1 | 4 | 1 | 4 | *running* | |

Nine of the eleven `|W| ≥ 1` profiles are eliminated with zero survivors. The
last two are still computing at the time of writing; this table will be updated
with their counts rather than assumed.

### 11e. What is still assumed here

Only the completeness of `Sm(T)` beyond the search bound — the same Thue–Mahler
finiteness statement as §5c, but at `10⁴⁸` to `10⁴⁰⁰` instead of `10²⁴`. For the
`α = 0` rows there is additionally a pool restriction (`T` drawn from primes
below 600), because with no ordinary prime in `T` the closure condition has
nothing to act on; those rows need the `max(T)` cutoff of §8 to be exhaustive.
`|W| = 3` (§11b) is free of both.

### 11f. The `|W| ≥ 1` table, complete  (`s3k2/27`, `s3k2/28`)

The `τ = 4` row stalled in `s3k2/27`, which enumerated `T` by running over all
`(τ−1)`-subsets of the pool — about `10⁹` of them. `s3k2/28` enumerates forward
from the ordinary pair instead: `T ⊇ {13, a₁, a₂} ∪ F(a₁) ∪ F(a₂)`, which must
already have at most four elements. 276 ordinary pairs survive that, giving 322
candidate `T`, and none reaches `|Sm(T)| ≥ 4` (the best reach 3).

| `α` | sp in `T` | nt in `T` | `τ` | `|W|` | `|U|` needed | admissible `T` | survive |
|---|---|---|---|---|---|---|---|
| 0 | no | 1 | 1 | 2 | 6 | 1 | 0 |
| 0 | no | 2 | 2 | 1 | 6 | 49 | 0 |
| 0 | yes | 0 | 1 | 2 | 6 | 1 | 0 |
| 0 | yes | 1 | 2 | 1 | 6 | 49 | 0 |
| 1 | no | 0 | 1 | 3 | 5 | **0** (§11b) | 0 |
| 1 | no | 1 | 2 | 2 | 5 | 1 | 0 |
| 1 | no | 2 | 3 | 1 | 5 | 1141 | 0 |
| 1 | yes | 0 | 2 | 2 | 5 | 1 | 0 |
| 1 | yes | 1 | 3 | 1 | 5 | 1141 | 0 |
| 2 | yes | 0 | 3 | 2 | 4 | 1 | 0 |
| 2 | yes | 1 | 4 | 1 | 4 | 322 | 0 |

All eleven eliminated.

---

## 12. Section 3 at `k = 2`: all fourteen profiles  (`s3k2/29`)

The two `|W| = 0` profiles other than the one closed in §§8–10 yield to the same
counting move:

| profile | `|U|` needed | `T` enumerated by | tested | largest `|Sm(T)|` | survive |
|---|---|---|---|---|---|
| `α = 1`, `τ = 4`, `|W| = 0` | 5 | closure, forward from the ordinary `a` | 14 189 | 4 (`T = {7,13,19,31}`) | 0 |
| `α = 0`, `τ = 3`, `|W| = 0` | 6 | pool (no ordinary prime to close on) | 6 441 | 2 | 0 |

So **every one of the fourteen role profiles of §3 at `k = 2` is eliminated**, by
two complementary methods:

* `α = 2`, `|W| = 0`, `τ = 5` — the hard one — by the recursion of §8, interval
  narrowing, and the closure filter of §9, **with no pool restriction**, leaving
  five named Thue–Mahler statements (§10b);
* the other thirteen by **closure plus a count**, which needs no abundancy input
  at all.

The two methods are complementary in exactly the way the structure demands: the
abundancy test wants `|W| = 0` (nothing unknown carries the slack) and large `T`;
the counting test wants small `T` (so `Sm(T)` is searchable to `10³⁰`–`10⁴⁰⁰`)
and tolerates any `|W|`. Between them they cover the range of `τ`.

### 12a. Everything still assumed, in one place

1. **`ω(N) ≥ 10`** (Nielsen 2015) — a theorem, used by every counting argument.
2. **`Sm(T)` complete** beyond the search bound: `10²⁴` at `|T| = 5`, `10³⁰` at
   `|T| = 4`, `10⁴⁸` at `|T| = 3`, `10¹⁶⁰` at `|T| = 2`, `10⁴⁰⁰` at `|T| = 1`.
   This is Thue–Mahler finiteness for `X²+XY+Y²`, not an unbounded hypothesis.
3. **Pool restrictions**, now confined to the profiles where closure has nothing
   to act on or the ordinary prime is bounded by hand: `α = 0` rows draw `T` from
   primes below 600 (`|W| ≥ 1`) or 1500 (`|W| = 0`); `α ≥ 1` rows bound the
   ordinary primes by 20 000. The `α = 2`, `|W| = 0` branch has **no** pool
   restriction, and §11b has none either.
4. Case B of §9a searched `(t*²+t*+1)/3` `S`-smooth to `3·10²⁸`.

### 12b. What is untouched

`3` **notable** at `k = 2` — the analogue of Ochem–Zelinsky's §4, where at `k = 1`
they needed `q ≥ 23 000 000 000` and heavy computation. Nothing here bears on it.

---

## 13. Removing the pool restrictions  (`s3k2/30`)

§12a listed pool restrictions as one of the four remaining assumptions. The
closure condition can replace the pool wherever it determines `T` outright.

**The criterion.** Let `A` be the set of ordinary primes of `T`, `|A| = α`.
Closure gives `F(a) ⊆ T` for each `a ∈ A`, so

    B := A ∪ {13} ∪ ⋃_{a∈A} F(a)   ⊆   T,

and **every element of `B` is determined by `A`** — it is in `A`, or is 13, or is
a prime factor of some `a²+a+1`. So `T = B` together with `τ − |B|` further
primes that closure says nothing about. Hence

* `τ = |B|` → `T` is completely determined by `A`, no pool needed;
* `τ > |B|` → `T` has free slots and the pool restriction stands.

And `A` itself is exactly enumerable whenever closure confines `F(a)` to a
**fixed** finite set of primes `S`, because then

    (a² + a + 1)/3  is S-smooth        (`v₃(a²+a+1) = 1` for `a ≡ 1 mod 3`)

is solved exactly by running over `S`-smooth `M` and testing whether `4(3M) − 3`
is a square — the device of §11c, usable to bounds far beyond any pool.

### 13a. `τ = 2`, `α = 1` (profiles with `|W| = 2`, need `|U| ≥ 5`)

`T = {13, t}` with one element ordinary.

* 13 ordinary → `F(13) = {61} ⊆ T` → `t = 61`, so `T = {13, 61}`.
* `t` ordinary → `F(t) ⊆ {13, t}`, and `t ∤ t²+t+1`, so `(t²+t+1)/3 = 13^c`.
  **No solutions** for any `c` with `3·13^c ≤ 10³⁰⁰`, i.e. `c ≤ 269`.

So the complete list is `T = {13, 61}`, and `Sm({13,61}) = ∅` (searched to
`10¹⁶⁰`) against a requirement of 5. **Dead, pool-free.**

### 13b. `τ = 3`, `α = 2` (`|W| = 2`, need `|U| ≥ 4`)

`T = {a₁, a₂, special}` with the special `≡ 1 (mod 12)`.

* **13 ordinary.** Then `61 ∈ T`.
  * `a₂ = 61`: then `B = {13,61} ∪ F(13) ∪ F(61) = {13, 61, 97}`, exactly three
    elements, and `97 ≡ 1 (mod 12)` so it can be the special. **`T = {13,61,97}`.**
  * `a₂ ≠ 61`: `F(a₂) ⊆ {13, 61}`, i.e. `(a₂²+a₂+1)/3` is `{13,61}`-smooth.
    **No solutions** below `10¹⁵⁰`.
* **13 not ordinary**, so 13 is the special. Then `F(a₁) ⊆ {13,a₂}` and
  `F(a₂) ⊆ {13,a₁}`. The uncoupled branch needs a solution of
  `(a²+a+1)/3 = 13^c`, of which there are none (13a). The coupled branch
  (`a₂ | a₁²+a₁+1` **and** `a₁ | a₂²+a₂+1`) was searched directly over
  `a₁ < 2·10⁶`: none.

So the complete list is `T = {13, 61, 97}`, and `Sm({13,61,97}) = ∅` against a
requirement of 4. **Dead, pool-free.**

I originally dropped the `a₂ = 61` branch, reasoning that `F(61) = {13,97}`
could not fit — wrong, since `97` is exactly the third slot. Corrected above.

### 13c. Where the pool survives, and why

| profile (`α`, sp in `T`, nt in `T`, `τ`, `|W|`) | pool? | reason |
|---|---|---|
| `0, no, 1, 1, 2` | **free** | `T = {13}` is forced, not chosen |
| `0, yes, 0, 1, 2` | **free** | same |
| `1, no, 0, 1, 3` | **free** | no admissible `A` at all (§11b) |
| `1, no, 1, 2, 2` | **free (new)** | §13a |
| `1, yes, 0, 2, 2` | **free (new)** | §13a |
| `2, yes, 0, 3, 2` | **free (new)** | §13b |
| `0, no, 2, 2, 1` | limited | `α = 0`: no ordinary prime for closure to act on |
| `0, yes, 1, 2, 1` | limited | same |
| `0, yes, 2, 3, 0` | limited | same |
| `1, no, 2, 3, 1` | limited | `|B| ≤ 3` leaves `F(a) ⊆ {13, w}` with `w` free |
| `1, yes, 1, 3, 1` | limited | same |
| `1, yes, 2, 4, 0` | limited | same, worse |
| `2, yes, 1, 4, 1` | limited | `|B| = 3 < τ` leaves one free slot |

Together with the `α = 2`, `|W| = 0`, `τ = 5` branch of §§8–10, **seven of the
fourteen profiles are now free of any pool restriction**, up from one.

The seven that remain limited all fail the criterion for the same structural
reason: a slot of `T` that closure does not reach. Where `α = 0` there is no
ordinary prime at all, so closure is vacuous; where `τ` exceeds `|B|` the
surplus slots hold big components, whose primes nothing forces.

### 13d. What replaced the pool

The pool-free profiles now rest on bounds for **specific Diophantine equations**
rather than on a range of `T`:

| equation | searched to | solutions |
|---|---|---|
| `(t²+t+1)/3 = 13^c` | `c ≤ 269` | none |
| `(a²+a+1)/3` is `{13,61}`-smooth | `10¹⁵⁰` | none |
| coupled `a₂ \| a₁²+a₁+1`, `a₁ \| a₂²+a₂+1` | `a₁ < 2·10⁶` | none |
| `Sm({13,61})`, `Sm({13,61,97})` | `10¹⁶⁰`, `10⁶⁰` | empty |

That is a strictly weaker hypothesis than a pool: the surviving `T` are two
explicit sets rather than an unbounded family, and each equation is a candidate
for an exact Thue–Mahler solve.

---

## 14. Replacing search bounds by proofs  (`s3k2/31`–)

§13d rests the pool-free profiles on four search bounds. Some of them do not
need a Thue–Mahler solver: they have a structure that an elementary argument
settles exactly. This section records which ones, and how.

### 14a. The coupled branch is empty — proved  (`s3k2/31`)

Setting (§13b, "13 not ordinary"): `T = {13, a₁, a₂}`, 13 special, `a₁ ≠ a₂`
ordinary, both `≡ 1 (mod 3)`, and the **coupled** condition
`a₂ | a₁²+a₁+1`, `a₁ | a₂²+a₂+1`. Previously searched over `a₁ < 2·10⁶`.

**Step 1 — Vieta jumping.** (Proved here; it is the standard descent, not cited
from any source.) Distinct primes are coprime, so the coupled condition gives
`a₁a₂ | a₁² + a₂² + a₁ + a₂ + 1`, i.e.

    x² + y² + x + y + 1 = k·x·y.

For fixed `k`, a solution with `x < y` has other root `y' = (x²+x+1)/y < y`, so
the minimal solution has `x = y`, whence `x = 1`, `k = 5`. For `k = 5`, `y = x+1`
is impossible, so `y ≥ x+2` and `y' ≤ x`: the descent `(x,y) → (y',x)` is strict
and invertible. Hence **every** solution is a consecutive pair of

    a₀ = a₁ = 1,  a_{n+1} = 5a_n − a_{n−1} − 1 :   1, 1, 3, 13, 61, 291, 1393, 6673, …

with `a_n² + a_n + 1 = a_{n−1}·a_{n+1}`.

**Step 2 — closure.** Let the pair be `(a_n, a_{n+1})`. Since `3 ≢ 1 (mod 3)` and 13
is the special, `n ≥ 4`. Then:

* `F(a_n) ⊆ {13, a_{n+1}}` forces `a_{n−1} = 3·13ˣ`. (The exponent of `a_{n+1}` is 1,
  by size; then divide Vieta's product.)
* `F(a_{n+1}) ⊆ {13, a_n}` forces `a_{n+2} = 3·13ᵘ·a_n^{v−1}` with `v ≥ 1`.

The **ratio lemma** `4.6·a_m < a_{m+1} < 5·a_m` for `m ≥ 3` (induction from
`61/13 > 4.6`) finishes it:

* `v = 1`: `a_{n+2}/a_{n−1} = 13^{u−x}` lies in `(97.3, 125)`, and no power of 13 does.
* `v = 2`: `a_{n+2}/a_n = 3·13ᵘ` lies in `(21.2, 25)`, and no `3·13ᵘ` does.
* `v ≥ 3`: `a_{n+2} ≥ 3a_n² > 25·a_n`.

**The coupled branch is empty.** The proof uses no search bound, no
Thue–Mahler input, and not even primality of the `aᵢ`.

`s3k2/31` checks each step. (A) A direct search of all pairs with `x ≤ 30 000`
finds exactly the consecutive pairs of the sequence. (B) It checks Vieta's
identity and the ratio lemma to `n = 400`. (C) No pair in range satisfies both
closure conditions. (D) Script 30's old search, re-run to `10⁵`, still finds
nothing. That is a reproduction check, not an input.

**Effect on §13b.** Two of its three branches rested on search bounds. The
coupled branch is now proved empty. The uncoupled branch still rests on
`(t²+t+1)/3 = 13ᶜ` having no solution (searched to `c ≤ 269`), and so does
§13a; §14b addresses that equation. The row
`coupled … a₁ < 2·10⁶` of the §13d table is **removed**.

### 14b. Single-exponent equations solved exactly — Skolem's method  (`s3k2/32`)

**Method.** (Proved in the script docstring. Skolem's method and Strassmann's
theorem are classical; the argument is written out in full there rather than
cited.) The equation is `x²+x+1 = D·pᶜ` with `D` fixed and `c` free. In `ℤ[ω]`,
`N(x−ω) = x²+x+1`, and the two conjugate primes over a split `q` cannot both
divide `x − ω`. So

    x − ω = ε·γ·πᶜ,

with 6 units `ε` and finitely many conjugate choices for `γ` and `π`. The
condition is that the `ω`-coefficient `B_c = −1`, where `B_c` is an integer
linear recurrence. For a prime `ℓ ≥ 5` let `L` be the period of `π` mod `ℓ`. On
each class `c ≡ c₀ (mod L)`, `B_c + 1` is an `ℓ`-adic power series in
`t = (c−c₀)/L`. Its linear coefficient is `≡ B_{c₀+L} − B_{c₀} (mod ℓ²)`, and
every higher coefficient has valuation `≥ 2`. By Strassmann, a class is either
**empty** (`B_{c₀}+1 ≢ 0 mod ℓ`) or has **at most one** solution (linear
coefficient of valuation exactly 1). Combining several `ℓ` whose periods divide
a common modulus settles each residue class. The solver reports "complete" only
when every class is settled, and otherwise claims nothing.

**Trust checks**, all in the script:

* **Reproduction.** Script 26 searched `x²+x+1 = pᶜ` for all 21 primes
  `p ≡ 1 (mod 3)` below 200, `c ≤ 1200`. The solver reproduces that table
  exactly, including Nagell's `18² + 18 + 1 = 7³`, and now proves it for all `c`.
* **Cross-check.** Each new equation below agrees with a direct `4Dpᶜ−3 = □`
  search for `c ≤ 400`.
* **Mutation.** With the known-solution search capped below `c = 3`, the solver
  refuses to call `x²+x+1 = 7ᶜ` complete. It does not drop the hidden solution
  `x = 18`.

**Results**, complete for every `c ≥ 0`. Solutions are listed as `(c, x)`, one of
each pair `x ↔ −1−x`, and only those with `x ≥ 1`:

| equation | solutions | where it is used |
|---|---|---|
| `x²+x+1 = 13ᶜ` | `(1, 3)` | `Sm({13}) = ∅` (§11c) |
| `x²+x+1 = 3·13ᶜ` | `(0, 1)`, `(2, 22)` | §13a; uncoupled branch of §13b |
| `x²+x+1 = 3·61ᶜ` | `(0, 1)`, `(1, 13)` | §13b, 13 ordinary |
| `x²+x+1 = 39·61ᶜ` | none | §13b, 13 ordinary |
| `x²+x+1 = 61ᶜ` | none | count for `T = {13,61}` |
| `x²+x+1 = 13·61ᶜ` | `(0, 3)` | count for `T = {13,61}` |
| `x²+x+1 = 97ᶜ` | none | count for `T = {13,61,97}` |
| `x²+x+1 = 61·97ᶜ` | none | count for `T = {13,61,97}` |

**Why this is not a Thue–Mahler solve.** Each equation has one free exponent,
so the unit-and-exponent group has rank 1 and Skolem's method applies directly.
With two or more free exponents (the five `|T| = 5` statements of §10b, or
`Sm(T)` for general `T`), the same method needs Baker-type bounds plus lattice
reduction. That still needs a CAS.

### 14c. The valuation step that makes the counts single-exponent  (`s3k2/33`)

`Sm({13,61})` and `Sm({13,61,97})` are two- and three-exponent problems. In
these profiles, though, the `T`-primes' own exponent balance caps how much of
each `U` may use. The mechanism is the valuation sharpening of §10b. An ordinary
prime `a` has `e_a = 2 = Σ_C v_a(σ(C))`, and every term is `≥ 0`:

* `T = {13, 61}` (§13a): 13 is ordinary. `σ(3²) = 13` spends one unit, so each
  `x ∈ U` has `x²+x+1 = 61ᶜ` or `13·61ᶜ`.
* `T = {13, 61, 97}` (§13b): 13 and 61 are ordinary. `σ(3²) = 13` and
  `σ(61²) = 3·13·97` spend both units of 13, and `σ(13²) = 3·61` spends one unit
  of 61. So each `x ∈ U` has `x²+x+1 = 97ᶜ` or `61·97ᶜ`.
* §13b with 13 ordinary and `a₂ ≠ 61`: 61 is the special, and the same count
  gives `v₁₃(a₂²+a₂+1) ≤ 1`. The `{13,61}`-smooth search to `10¹⁵⁰` becomes the
  two equations `3·61ᶜ` and `39·61ᶜ`, whose only prime solution is `a₂ = 13 = a₁`.

By §14b, every one of these equations has no solution usable in `U`.

**Result.** All six profiles marked **free** in §13c are now eliminated with no
search bound and no Thue–Mahler assumption. Their only input is `ω(N) ≥ 10`
(Nielsen 2015, a theorem). They are:

* `0,no,1,1,2` and `0,yes,0,1,2`: `T = {13}`, and `Sm({13}) = ∅` exactly.
* `1,no,0,1,3`: §11b; this was already unconditional.
* `1,no,1,2,2` and `1,yes,0,2,2`: §13a with §14b and §14c.
* `2,yes,0,3,2`: §13b with §14a, §14b and §14c.

**Updated tally for the fourteen profiles of §3 at `k = 2`:**

| status | profiles |
|---|---|
| **unconditional** (only `ω(N) ≥ 10`) | **6**: the six above |
| conditional on 5 named Thue–Mahler statements + case-B bound `3·10²⁸` | 1: `α=2, |W|=0, τ=5` |
| conditional on a pool + `Sm(T)` search bounds | 7: the "limited" rows of §13c |

**The §13d table, revised:**

| equation | status |
|---|---|
| `(t²+t+1)/3 = 13ᶜ` | **solved exactly** (§14b) |
| `(a²+a+1)/3` is `{13,61}`-smooth | **replaced** by `3·61ᶜ`, `39·61ᶜ`, both solved (§14c) |
| coupled `a₂ \| a₁²+a₁+1`, `a₁ \| a₂²+a₂+1` | **proved empty** (§14a) |
| `Sm({13,61})`, `Sm({13,61,97})` | **replaced** by four single-exponent equations, all solved (§14c) |

### 14d. An error in the §8 recursion, corrected; §10's conclusion survives  (`s3k2/34`, `s3k2/35`)

**The error.** Script 13's cutoff lemma is stated for `T = S ∪ {t*}`, with
**one** prime above `S`. Scripts 17, 19 and 22 applied it at every level. At
level `L`, though, `S` is the `L` smallest elements of a 5-set, so once the
`(L+1)`-th element is `≥ B` there are `k = 5 − L` primes `≥ B`, not one. The
correct lemma (proved in the `s3k2/34` docstring) is

    corr_k(B,S) = (B/(B−1))^k · exp(1.01·(1 + 1/(√B−1))·((1−u)^{−k} − 1)·E(S)),   u = B^{−1/2},

which reduces to script 13's `corr` at `k = 1`. Because `corr − 1 ∝ B^{−1/2}`,
the threshold grows by roughly `k²`:

| `S` | margin | `B` as used (k = 1) | `B` correct |
|---|---|---|---|
| `{7}` | 1.186813 | 139.5 | 1751 (k = 4) |
| `{13}` | 1.278107 | 63.4 | 712 (k = 4) |
| `{7,13}` | 1.095520 | 727.4 | 5970 (k = 3) |
| `{7,13,19}` | 1.036272 | 7081 | 27 723 (k = 2) |

So §8c and §9b pruned sets at levels 2–4 without justification, and the
"no pool restriction" claim of §10 was **not established** by the scripts cited
for it. The level-4 → 5 step (`k = 1`) was correct.

**The re-run.** `s3k2/34` is script 22 with `corr_k` substituted, and nothing
else changed:

| level | §9b (k = 1 throughout) | corrected |
|---|---|---|
| 2 | 6 | 59 |
| 3 | 91 | 1 372 |
| 4 | 4 324 | 31 925 |
| 5 | 485 064 | **488 860** |
| exceptions | 3 | **the same 3** (`{7,13,19,31}`, `{7,13,31,79}`, `{7,13,31,307}`) |

`s3k2/35` runs script 23's level-5 tests on the corrected list:

| outcome | count |
|---|---|
| dead: no role assignment passes closure | 485 179 |
| dead: interval narrowing (unconditional) | 3 676 |
| **unconditional** | **488 855** |
| dead: `ω ≥ 10` + `Sm(T)` complete (conditional) | 5 — the same five sets as §10b |
| still alive | **0** |

**Verdict.** §10's conclusion stands exactly as stated: the branch closes with
no pool restriction, apart from the same five Thue–Mahler statements and the
case-B bound of §9c. It is now actually proved by the scripts cited. Before
this correction it was not. The exceptions are the ones §9a already handles.
The level lists are regenerated by `python3 34_recursion_k_correct.py 4` in
about a minute and are not committed.

### 14f. Two more residual sets on the `α = 2, |W| = 0` branch  (`s3k2/38`)

§9a finished the exception `{7,13,19,31}` by noting that its four admissible
fifth primes (61, 67, 127, 331) give sets "inside the pool already swept in
§5⅔". That sweep (`s3k2/15`) has no closure or forced-exponent filter, and it
does not record **how** each of those sets died. Resolving the exception with
exact roles (`python3 38_closure_dfs.py 2,yes,2,5,0`) shows:

| `T` | roles | `Sm(T)` to `10²⁴` | admissible under `R(T)` | verdict |
|---|---|---|---|---|
| `{7,13,19,31,61}` / `{…,67}` | — | — | — | dead, unconditional |
| `{7,13,19,31,127}` | 7, 19 ordinary; 13 special; 31, 127 notable | 5, 11, 107, 191, 653 | 191, 653 | **conditional**: need 4 |
| `{7,13,19,31,331}` | 7, 31 ordinary; 13 special; 19, 331 notable | 5, 11, 191, 653 | 191, 653 | **conditional**: need 4 |

The other two exceptions of §9a (`{7,13,31,79}`, `{7,13,31,307}`) have no
admissible completion, as §9a said.

**Correction to §10b and the README.** The `α = 2, |W| = 0` branch rests on
**seven** named Thue–Mahler statements, not five: the five of §10b plus
`{7,13,19,31,127}` and `{7,13,19,31,331}`. Nothing is alive. Closure mode of
`s3k2/36` on this profile agrees independently: it reaches no exceptions and
ends with exactly these seven conditional sets.

### 14e. The seven pool-limited profiles, without a pool  (`s3k2/36`–`38`)

§13c left seven profiles drawing `T` from a finite pool. `s3k2/36` runs the
`max(T)` recursion of §8 on any role profile, using the corrected `k`-prime
cutoff of §14d, and handles the single `W` slot that every one of these
profiles has:

* **`W` slot.** The slot is either an explicit prime `w ≡ 2 (mod 3)` below
  `WB = 500` or a generic `w ≥ 500`, which contributes a factor in
  `(1, 500/499)`.
  * A notable `w` contributes a factor in `[σ(w^{q₀})/w^{q₀}, w/(w−1))`.
  * A special `w ≡ 5 (mod 12)` is split two ways. With `e = 1`, the factor is
    exactly `(w+1)/w`, and every prime `≡ 1 (mod 3)` dividing `w+1` is forced
    into `T`. With `e ≥ 5`, the interval is tight.
* **3-budget.** Role minima admit every exponent with
  `v₃(k+1) ≤ 2 − α − cost(W)`. This is a relaxation, which is safe because it
  only lowers the minima.
* **Last level for `α ≥ 1`.** The last level is driven by closure, split on the
  role of the last prime `t`:
  * An ordinary prime in `S` pins `t ∈ F(s) \ S`.
  * If `t` is ordinary, `(t²+t+1)/3` must be `S`-smooth. When the margin
    restricted to that role split gives a finite cutoff `B`, enumerating
    `S`-smooth numbers up to `B²` is **exact**. Only a margin `≤ 1` falls back to
    a stated search bound ("Case B").
  * Otherwise the per-split cutoff applies.
* **Exceptions.** An exception with two or more primes missing goes to the
  closure DFS of `s3k2/38`, which propagates `F(t) ⊆ T` over partial role
  assignments. For two ordinary unknowns it also uses the Vieta
  classification of §14a. Anything unresolved is reported, never dropped.

**Validation.** On the `α = 2, |W| = 0, τ = 5` profile, the plain-cutoff mode of
`s3k2/36` reproduces script 34's level counts and script 35's final outcome
exactly: 485 179 sets with no role assignment, 3 676 unconditional, 5
conditional, 0 alive, and the same 3 exceptions. `s3k2/37` (one-prime exception
resolver) and `s3k2/38` (DFS) agree on the `τ = 3` profiles. For the two
`|W| = 0` profiles, the final test run directly on every `T` in the old pool
below 400 kills them all unconditionally (`7140 = 6469 + 671`,
`630 = 231 + 399`), consistent with the recursion.

**Results** (final code; each row is `python3 s3k2/36_profile_recursion.py <profile>`,
and each exception is resolved by `python3 s3k2/38_closure_dfs.py <profile>`):

| profile (`α`, sp, nt, `τ`, `|W|`) | killed early (raw min > 18/13) | unconditional | no role/config | conditional sets | alive | verdict |
|---|---|---|---|---|---|---|
| `0,no,2,2,1` | 6 | 551 | 17 | 0 | 0 | **unconditional** |
| `0,yes,2,3,0` | 0 | 80 | 17 | 0 | 0 | **unconditional** |
| `1,yes,2,4,0` | 0 | 618 | 9 | 0 | 0 | **unconditional** |
| `1,no,2,3,1` | 17 | 4 249 | 16 | 0 | 0 | **unconditional** |
| `0,yes,1,2,1` | 2 | 260 | 341 | 1 | 0 | conditional: 1 named set |
| `1,yes,1,3,1` | 16 | 4 349 | 52 | 3 | 0 | conditional: 3 named sets + one Case-B search |
| `2,yes,1,4,1` | 22 | 357 | 310 | 4 | 0 | conditional: 4 named sets + Case-B/Vieta searches |

"Killed early" is the check added after the first run: a set `S` whose **raw**
role minimum (before narrowing) already exceeds `18/13` is dead for every `T ⊇ S`,
since role factors only grow and `PROD_U ≥ 1`. The narrowed `LO` is **not** valid
for supersets, so it is never used this way. Without this check, the recursion
had reported spurious "exceptions", for example `{13,61,97}` with `W` notable 5,
whose raw minimum is `1.38962 > 18/13`.

**Named conditional sets** (`Sm` searched to `10⁴⁸` for three primes, `10¹⁶⁰`
for two, `10²⁴` for four):

| profile | `T` | `W` | `Sm(T)` | admissible | need |
|---|---|---|---|---|---|
| `0,yes,1,2,1` | `{7,13}` | notable 11 | ∅ | ∅ | 6 |
| `1,yes,1,3,1` | `{13,61,151}` | notable 5 | ∅ | ∅ | 5 |
| `1,yes,1,3,1` | `{13,61,157}` | notable 5 | ∅ | ∅ | 5 |
| `1,yes,1,3,1` | `{7,13,19}` | notable 23 | 11, 653 | 653 | 5 |
| `2,yes,1,4,1` | `{13,61,157,8269}` | notable 5 | ∅ | ∅ | 4 |
| `2,yes,1,4,1` | `{7,13,19,127}` | notable 29 | 11, 107, 653 | 653 | 4 |
| `2,yes,1,4,1` | `{7,13,19,127}` | notable 41, 47 | 11, 107, 653 | 107, 653 | 4 |

**Case-B and Vieta searches** (no solution found in any):

* `(t²+t+1)/3` `{7,13}`-smooth, to `10³⁰⁰`, in `1,yes,1,3,1` and `2,yes,1,4,1`;
* `(t²+t+1)/3` `S`-smooth, to `10¹²⁰`, for `S = {13,61,151}`, `{13,61,157}`,
  `{13,61,28057}` and `{7,13,19}`, in `2,yes,1,4,1`;
* Vieta pairs to sequence index 1500 (about `10¹⁰²⁰`), in `2,yes,1,4,1`.

**Cost.** `2,yes,1,4,1` takes 37 minutes; 315 329 of its 340 091 level-3 sets
come from the `W = 5` configuration. The other six profiles take seconds.


**What is conditional here.**

1. **Count on the named sets above** (`ω(N) ≥ 10` plus `Sm(T)` complete).
2. **Case-B and Vieta searches above.** A solution beyond a bound would only
   create a candidate set, which would still have to pass the full test.

These are the same kind of statement as the named `|T| = 5` sets: Thue–Mahler
problems of rank 2 or 3, not pool restrictions.

### 14g. Section 3 at `k = 2`: the tally after §14

| status | profiles | what they rest on |
|---|---|---|
| **unconditional** (only `ω(N) ≥ 10`) | **10** | nothing else |
| conditional | `α=2, |W|=0, τ=5` | 7 named sets (§10b + §14f) |
| conditional | `0,yes,1,2,1` | 1 named set |
| conditional | `1,yes,1,3,1` | 3 named sets + one Case-B search |
| conditional | `2,yes,1,4,1` | 4 named sets + Case-B/Vieta searches |

The ten unconditional profiles are the six of §14c and the four of §14e.
**No profile rests on a pool.** Every residual statement is an equation
`x²+x+1 = ∏_{t∈T} t^{c_t}` of rank `|T| ≥ 2` with `T` explicit, or the matching
`(t²+t+1)/3` search. §9c's case-B bound `3·10²⁸` is no longer used: the DFS of
`s3k2/38` finishes the §9a exceptions exactly.

### 14h. The residual statements, solved: Matveev plus lattice reduction  (`s3k2/39`, `s3k2/40`)

**Method.** This is the standard Baker-plus-reduction method, not a new one.
Because the equations have `Y = 1`, only archimedean logarithms are needed. With
`z = x − ω`:

    Log(z/z̄) = Σ e_t·Log(π_t/π̄_t) + b₀·Log ζ₆,      |Log(z/z̄)| ≤ 2√3/|z|.

Matveev's Theorem 2.2 (Izv. RAN 62:4, 1998) bounds the exponents. Its
transcription and the check of every hypothesis are in `MATVEEV_1998.md`: the
Kummer condition, `D = 1`, `ρ = 1`, and `h(π_t/π̄_t) = ½ log t`.

* **Initial bound.** Matveev gives `H ≤ 10¹¹` (`|T| = 2`) up to `6·10¹⁵`
  (`|T| = 5`). Floating-point constants are inflated by 1%.
* **Reduction.** A de Weger-style lattice argument, written out in the
  docstring, brings `ln(x²+x+1)` down to at most **153** (`|T| = 5`), 121
  (`|T| = 4`) and 89 (`|T| = 3`). The lower bound on the shortest vector is
  `min|b*_i|` of the output basis, which is valid for **any** basis of the
  lattice. The output is checked to be a basis by comparing exact determinants,
  so soundness does not depend on the LLL routine being correct.
* **Exhaustive search.** Every `3^δ·T`-smooth `M` below the proved bound is
  tested for `4M − 3 = □`.

**Validation** (`python3 39_baker_lll.py validate`):

* The identity `Λ = Σ e_t θ_t + b₀π/3` holds on known solutions to `10⁻⁴⁰⁰`.
* Rank one agrees **exactly** with the independent Skolem solver of §14b, for 8
  primes with `δ = 0, 1`.
* For `{7,13}`, `{7,13,19}` and `{7,13,19,31}`, the proved-complete list equals a
  direct search to `10¹⁵⁰`, including `653` and `18`.

**Results** (`python3 39_baker_lll.py residual`):

| statement | proved bound `ln(x²+x+1) ≤` | complete answer | same as the old search? |
|---|---|---|---|
| the seven `α = 2` named 5-sets | 152.3–153.1 | the `Sm(T)` lists of §10b and §14f | yes, all seven |
| `{7,13}` | 61.2 | `Sm = ∅` | yes |
| `{13,61,151}`, `{13,61,157}` | 89.5 | `Sm = ∅` | yes |
| `{7,13,19}` | 89.2 | `Sm = {11, 653}` | yes |
| `{13,61,157,8269}` | 117.4 | `Sm = ∅` | yes |
| `{7,13,19,127}` | 121.2 | `Sm = {11, 107, 653}` | yes |
| Case B, `S = {7,13}` | 61.2 | no `t` | yes |
| Case B, `S = {13,61,151}`, `{13,61,157}`, `{13,61,28057}` | 89.5 | only `t = 13 < max S` | yes |
| Case B, `S = {7,13,19}` | 89.2 | only `t = 7 < max S` | yes |

Every count-based kill therefore holds as recorded, now unconditionally. The
Case-B searches produce no candidate.

**The coupled branch** (`s3k2/40`), previously "Vieta pairs to index 1500",
closes by a count instead:

* Both unknowns `a, a′` are ordinary and each divides the other's `x²+x+1`, so
  `U` may use at most one unit of `a` and at most one of `a′`.
* Every other member of `U` lies in `Sm({7,13})`, whose complete list
  `{0, 2, 3, 9, 18}` has no usable member.
* So `|U| ≤ 2 < 4`.

### 14i. Section 3 at `k = 2`: status

**All fourteen role profiles are eliminated.** The only inputs are:

1. `ω(N) ≥ 10` — Nielsen 2015, a cited theorem;
2. Theorem 2.2 of Matveev 1998, a cited theorem, transcribed in `MATVEEV_1998.md`
   from the user-supplied pages.

No pool, no search bound and no Thue–Mahler assumption remain.

**How much weight this carries.** The claim now rests on a large amount of code
written in this session (`s3k2/31`–`40`). Each piece was validated against an
independent method or a reproduction target, and two errors in the earlier
scripts were found and corrected along the way (§14d, §14f). It has **not** had
an independent audit. That is the recommended next step before this result is
relied on.

### 14j. Reproducibility  (`verify_all.py`)

`python3 verify_all.py` (fast tier, 16 checks, about 4 min) and
`python3 verify_all.py full` (19 checks, about 45 min) re-run the scripts behind
every figure quoted in §§14a–14h. Each output is compared with the value
written in the runner, which is copied from these tables. At commit time: **19 of
19 pass**, including 488 860 level-5 sets with 0 alive (scripts 34, 35) and the
`2,yes,1,4,1` tally `(22, 357, 4, 310, 0, 1, 4)`. This checks reproducibility,
not correctness; correctness is the audit's job (`PROMPT_AUDIT_S3K2.md`).

### 14k. Independent audit  (`audit_s3k2/AUDIT_S3K2_RESULT.md`)

An independent session ran `PROMPT_AUDIT_S3K2.md` from a cold start. Its full
report, scripts and logs are in `audit_s3k2/`. It re-derived the key items
before reading the code:

* the profile list;
* the cutoff lemma;
* Matveev's application, from the page images;
* a **different** complete solver: exact LLL, then Fincke–Pohst enumeration,
  then exponent-vector enumeration.

It then reviewed every script and ran twelve mutations.

**Verdict: the claim stands, conditional on the two cited theorems, with repairs
to documentation only. No finding has status `ERROR`.**

**Agreement with independent methods.**

* Its solver agrees with `s3k2/39` on all 18 residual statements (13 named
  `Sm(T)` sets and 5 Case-B sets), and on the 8 single-exponent equations of
  `s3k2/33`.
* Its final bounds are tighter (`L ≤ 27.5`, `44.9`, `54.0` against the repo's
  `61.2`, `121.2`, `152.7`), and the lists are identical.
* The answers are insensitive to Matveev's constant up to a factor of `10³⁰`.
* It reproduced every figure of §§14d–14h, and `verify_all.py full` gave 19 of 19.

**Corrected tally.** §14i said "ten profiles use only `ω(N) ≥ 10`". That
understated the result:

| input | profiles |
|---|---|
| **no cited theorem at all** | 5: `1,no,0,1,3` (§11b), and `0,no,2,2,1`, `0,yes,2,3,0`, `1,yes,2,4,0`, `1,no,2,3,1` (§14e) |
| `ω(N) ≥ 10` only | 5: `0,no,1,1,2`, `0,yes,0,1,2`, `1,no,1,2,2`, `1,yes,0,2,2`, `2,yes,0,3,2` (§14c) |
| `ω(N) ≥ 10` and Matveev 1998, Thm 2.2 | 4: `2,yes,2,5,0`, `0,yes,1,2,1`, `1,yes,1,3,1`, `2,yes,1,4,1` |

The first five profiles have no conditional set, exception or Case-B search.
Every kill is by abundancy, closure or raw minimum. Nielsen enters only through
the count test, which those five never reach.

**Findings and what was done.**

* **G1** — narrowing and supersets. The narrowed `LO(S)` is **not** a lower bound
  for `T ⊋ S` (`107 ∈ Sm({7,13,19,31,127}) ∖ Sm({7,13,19,31})`), so the
  justification in `s3k2/34`'s docstring and in §14d was wrong. The kill is
  valid for a different reason, proved in the audit's Pf.2: the cap uses only the
  raw minimum, and `margin ≥ corr_k` is equivalent to
  `(18/13)/(H₀·HI) ≥ corr_k`. **Done:** `s3k2/34`'s docstring is corrected and
  warns against letting the cap depend on narrowed information.
* **G2** — the factor `1.01` in `corr_k`. Its stated justification fails for
  `B ≲ 10⁴`. The inequality actually needed, `log f(x)·(√M − 1) < 1`, holds for
  every `x ≥ 2` (`audit_s3k2/a2_corr_factor_check.py`), so `1.01` is slack.
  **Done:** documented in `s3k2/34`.
* **G3** — narrowing is exactly one step. §5⅔'s "one iterates" performs no second
  exclusion: after the first pass the new cap is `Hup₀`, which already bounds
  every admitted `f(x)`. This is what makes G1's repair work.
* **D2** — coverage. `verify_all` relied on the DFS level cut-off happening to
  include every exception of `s3k2/36`. It did, since the one exception is at
  level 2, but that was not checked. **Done:** `verify_all.py` now asserts that
  every exception printed by `36` is a DFS input for the same profile. After the
  change, `verify_all.py full` passes **20 of 20**, including the new coverage
  check on `2,yes,1,4,1`. A
  last-level (`t:`-tagged) exception, which the DFS never sees, fails the check.
* **X1** — `verify_all` detects drift, not unsoundness. An over-pruning change can
  only remove sets, so it never produces `ALIVE`. Mutations C1 (`corr_1`), C4
  (dropped split) and others are silent on several profiles. **Done:** stated in
  the runner's docstring. Soundness rests on the audit's proofs Pf.2–Pf.5.
* **M2** — `|Λ| ≤ (π√3/2)/|z|` holds for **all** `x ≥ 0`, a small strengthening.
  No change is needed; the repo's `L ≥ ln 12` covers the rest correctly.
* **M3** — the remark after (2.16) fails by a factor tending to about 4, for both
  `ρ = 1` and `ρ = 2`. That is consistent with a loose remark and not with a
  misreading; the zoomed crops read as transcribed.
* **F1, F2** — trial division capped at `10⁸` in `Fset`, and floating point in
  `threshold_k`. Both are harmless here, for reasons given in the report, but
  are not made rigorous.

**What the audit did not establish:**

* Matveev's and Nielsen's theorems themselves;
* Matveev pp. 81 and 83–84, which could hold further standing hypotheses;
* an independent **re-implementation** of the `s3k2/36` recursion. It was reviewed
  line by line, mutation-tested, and spot-checked, but not rewritten.

Of these, the last is the natural next check.
