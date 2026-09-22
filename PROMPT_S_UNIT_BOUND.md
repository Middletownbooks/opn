# Research task: bounding the ordinary primes of a 2-restrained odd perfect number

Self-contained brief for a reasoning model with no tools (you may write and
hand-execute short programs, but assume no internet and no libraries).

Everything stated as "verified" below has been checked computationally. Treat it
as given. Everything else is the open part.

---

## 1. Setting

`N` is an **odd perfect number**: `N` odd with `σ(N) = 2N`, `σ` the
sum-of-divisors function. None is known; none is known not to exist.

**Euler's form.** `N = p^e · m²` with `p` prime, `p ≡ e ≡ 1 (mod 4)`, `p ∤ m`.
Call `p` the **special prime**. Every other prime factor of `N` has even
exponent.

**McDaniel (1970).** `m` is not squarefree: at least one even exponent is `≥ 4`.

**Definition.** `N` is **`k`-restrained** if exactly `k` of its even exponents
exceed 2. Ochem & Zelinsky's *restrained* is `k = 1`. Write the `k` components
with exponent `≥ 4` as `n_i^{q_i}` (the **notable** components). A prime with
exponent exactly 2 is **ordinary**.

**Known.** `ω(N) ≥ 9`; `ω(N) ≥ 12` if `3 ∤ N` (Nielsen 2007). `ω` counts
distinct prime factors.

---

## 2. The argument we are trying to extend

Ochem & Zelinsky (arXiv:2607.19746, 2026) prove there is **no 1-restrained odd
perfect number with `3 ∤ N`**, as follows. Assume such an `N`.

**(a) Every ordinary `s` is `≡ 5 (mod 6)`.** If `s ≡ 1 (mod 3)` then
`3 | s²+s+1 = σ(s²)`, so `3 | σ(N) = 2N`, so `3 | N`. And `s` is odd.

**(b) Every ordinary `s` is *regular*: `σ(s²) = p^a n^b`.** Every prime factor
of `s²+s+1` other than 3 is `≡ 1 (mod 3)`. Ordinary primes are `≡ 2 (mod 3)` by
(a), so such a factor is not ordinary; the only non-ordinary primes are `p` and
`n`.

**(c) Each pair `(a,b)` hosts at most one ordinary `s`,** since `s²+s+1`
determines `s`.

**(d) Bound the abundancy.** `σ(N)/N = ∏_components σ(c)/c`, every factor `> 1`,
so exhibiting an upper bound `< 2` is a contradiction.

- `A₁ = sup (p/(p−1))(n/(n−1)) = (13/12)(7/6) = 91/72 ≈ 1.26389`.
  (`p ≡ 1 mod 12` forces `p ≥ 13`; `n ≡ 1 mod 6` forces `n ≥ 7`.)
- `A₂ ≈ 1.320519`: over the 11 classes `(a,b)` with `a+b ≤ 6` whose smallest
  solutions are known, `∏ m/(m−1)` with
  `m ∈ {5, 29, 59, 863, 1667, 1733, 2819, 306419, 1345913, 3619619, 68839637}`.
- `A₃ = (1+10⁻⁹)³` for the 3 remaining classes with `a+b ≤ 6` (searched past `10⁹`).
- `A_∞ = ∏_{k≥7} (1 + 1/(7^{k/2}−2))^{k−1} ≈ 1.011787`, using
  `(s+1)² > σ(s²) ≥ 7^{a+b}` so `s ≥ 7^{k/2}−1`, and killing the two pure-power
  classes of each degree by Bennett–Levin (below).

Product `≈ 1.68866 < 2`. Contradiction. **Verified to full printed precision.**

---

## 3. Why this fails at `k = 2` (verified)

Now two notables `n₁, n₂`. Steps (a)–(c) transfer verbatim with pairs replaced
by triples: `σ(s²) = p^a n₁^b n₂^c`. Two cases.

**Case (ii): `n₂ ≡ 2 (mod 3)`.** Then `n₂` never divides any `σ(s²)` (its prime
factors are `≡ 1 mod 3`), so `c = 0` always and the class structure is exactly
the `k = 1` pairs; `A₂, A_∞` are unchanged. Only `A₁` grows: `n₂ ≡ 5 (mod 6)` so
`n₂ ≥ 5`, giving `A₁ ≤ (13/12)(7/6)(5/4) = 1.579861`.

> bound `≥ 1.579861 × 1.320519 × 1.011787 = **2.110829 > 2**`.

**Case (i): both `≡ 1 (mod 3)`.** `A₁ ≤ (13/12)(7/6)(19/18) = 1.334105`. The 11
`k=1` classes survive as `(a,b,0)`. Two new classes have exactly-known minima:
`σ(s²)` equal to a single notable prime needs `s²+s+1` prime and `≡ 1 mod 6`,
and the two smallest such ordinary `s` are `5, 17`, so the second forces `17/16`;
`σ(s²) = n₁n₂` has smallest `s = 11` (`133 = 7·19`, and neither factor is
`≡ 1 mod 12` so this is not the `k=1` class `(1,1)`, whose minimum is 29).

> bound `≥ 1.334105 × 1.320519 × (17/16) × (11/10) = **2.059000 > 2**`,
> **with the entire tail `A_∞` discarded.**

Every ingredient is exact or discarded in the method's favour, so **better data
on the class minima cannot rescue it.** The method is genuinely out of margin:
the class count per degree grows quadratically, `(k+1)(k+2)/2 − 3`, against
linearly, `k − 1`.

---

## 4. The lossy step, and the question

The bound takes, for each class, the minimum of `m` over **all admissible
`(p, n₁, n₂)`**. But a real `N` has `p, n₁, n₂` **fixed**. The bound therefore
behaves as if every class could be realised simultaneously, each by its global
minimum. That is wildly pessimistic, and it is the only obvious place where a
large factor is being thrown away.

> **PRIMARY QUESTION.** Fix distinct primes `p, n₁, n₂` with `p ≡ 1 (mod 12)`
> and `n_i ≡ 1 (mod 6)`. Let
>
> `T(p, n₁, n₂) = #{ s prime : s² + s + 1 = p^a n₁^b n₂^c for some a,b,c ≥ 0 }`.
>
> **Prove an explicit upper bound on `T`, uniform in `p, n₁, n₂`.**

**Why a bound would settle the case.** If `3 ∤ N` then `ω(N) ≥ 12`. A
2-restrained `N` has exactly three non-ordinary primes (`p, n₁, n₂`), so at
least **9** ordinary primes, each with `σ(s²)` supported on `{p, n₁, n₂}`.
Hence `T ≥ 9`. **Any uniform proof that `T ≤ 8` closes `k = 2`, `3 ∤ N`
outright** — and the same argument at general `k` needs `T ≤ ω_min − 1 − k`.

**A route, offered without guarantee.** In `Z[ω]`, `ω` a primitive cube root of
unity, `s²+s+1 = (s−ω)(s−ω̄)`. If the left side is an `S`-unit for
`S = {p, n₁, n₂}` then `s−ω` is an `S'`-unit in `Z[ω]`, and
`(s−ω) − (s−ω̄) = ω̄ − ω` is a fixed element of norm 3. That is a three-term
`S`-unit equation. Generic explicit bounds (Evertse, Győry) are of the shape
`3·7^{2|S|+3}`, astronomically too weak. The question is whether *this*
equation admits a small bound — its shape is very special.

---

## 5. What counts as success

1. An explicit uniform bound on `T`, with proof. Anything `≤ 8` closes the case.
2. Failing that, a demonstration that no bound below 9 is available by these
   means — for instance an explicit `(p, n₁, n₂)` with `T ≥ 9`, or a family
   argument. **This is equally valuable** and would retire the approach.
3. Failing both, any *other* structural constraint that materially cuts the
   class count or raises the size floor. Concretely: the class count per degree
   is `(k+1)(k+2)/2 − 3`; anything bringing it back toward `k − 1` would help.

## 6. Rules

- Do **not** state a named theorem — a reciprocity law, an `S`-unit bound, a
  Diophantine result — unless you are confident of its exact statement. If
  unsure, say so and mark the step conditional. A conditional result clearly
  labelled is useful; a misremembered theorem is worse than nothing.
- Every numerical claim must be one you computed, with the computation shown.
- Do not claim progress on the odd perfect number problem as a whole. The target
  is one case of one sub-problem.
- A precise negative result is a success, not a failure. Say plainly if you
  cannot get a bound and what specifically blocks you.

## 7. Facts you may use freely (all verified)

- Divisors of `s²+s+1` other than 3 are `≡ 1 (mod 3)`. `3 | s²+s+1` iff
  `s ≡ 1 (mod 3)`, and then `v₃ = 1` exactly.
- `s ≡ 5 (mod 12) ⟹ s²+s+1 ≡ 7 (mod 12)`; `s ≡ 11 (mod 12) ⟹ s²+s+1 ≡ 1 (mod 12)`.
- `s² < s²+s+1 < (s+1)²`, so `s²+s+1` is never a perfect square.
- **Bennett–Levin**: `z²+z+1 = r^t` has no solution with `z, r` prime and `t > 1`.
- **Bugeaud–Mihăilescu**: `x²+x+1 = 3y^t` has no integer solution for `t ≥ 3`.
- Small data: `5²+5+1 = 31`; `11²+11+1 = 133 = 7·19`; `17²+17+1 = 307`;
  `23²+23+1 = 553 = 7·79`; `29²+29+1 = 871 = 13·67`; `41²+41+1 = 1723`;
  `59²+59+1 = 3541`.
