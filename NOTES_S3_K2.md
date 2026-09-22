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
