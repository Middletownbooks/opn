# The inversion: forcing instead of enveloping

Working notes, follow-on to `AUDIT_REPORT.md`. Scripts in `inversion/`,
standard library only.

The audit's Proposition A showed that *upper* abundancy envelopes can never
close a branch: for any honest `(K_env, B, M)`, `H(K_env)(B/(B−1))^M > 2`. The
direction that remains is **forcing** — the support is obliged to contain
things, and those obligations propagate. These notes develop that side, and
report where it stalls.

---

## 0. A correction to my own earlier framing

I previously wrote that minimality of `q` forces `ω(N)` to be large, "which via
`e_q = Σ_{p≠q} v_q(σ(p^{e_p}))` forces many `q`-adic input witnesses." **That
is wrong.** A large `ω(N)` says nothing about `e_q`, which can be 2 with a
single witness. What `ω(N) ≥ k₀(q)` actually supplies is `k₀(q)` *production
obligations* — one per support prime, each needing some witness — not many
witnesses for `q` in particular. Everything below uses the corrected form.

---

## 1. Theorem 1 — complete first-input classification, every odd prime `q`

This is the item the paper leaves open ("The residual branch `q ≥ 19` requires
a separate treatment of the possible first `q`-adic input orders").

> **Theorem 1.** Let `N` be odd perfect, `q = min S`, and write
> `q − 1 = 2^a·μ` with `μ` odd. A `q`-input witness exists, and
> (i) if it is non-Euler, `ord_q(p) | μ`;
> (ii) if it is the Euler prime, `ord_q(π) | 2μ`.
> Hence the first-input coverage split has exactly `d(μ)` non-Euler children
> `N_d` and `d(2μ) = 2d(μ)` Euler children `E_d`:
> **the number of first-input children is `3·d(μ)`.**

*Proof.* Existence is the paper's Lemma 5.2. For a witness `p` with
`d = ord_q(p)`, the cyclotomic input condition gives `d | n_p` (order-one
convention: `q | n_p`), and `d | q−1` by Fermat. If `p` is non-Euler then
`e_p` is even, so `n_p` is odd, so `d` is odd, and an odd divisor of `2^a μ`
divides `μ`. If `p = π` then `n_π = α+1 ≡ 2 (mod 4)`, so `v₂(d) ≤ 1` and `d`
divides `2μ`. Since `μ` is odd, `d(2μ) = 2d(μ)`. ∎

Checked against the paper's Table 2 — all five branches reproduced exactly:

| q | μ | non-Euler | Euler | children | paper |
|---|---|---|---|---|---|
| 5 | 1 | N₁ | E₁,E₂ | 3 | match |
| 7 | 3 | N₁,N₃ | E₁,E₂,E₃,E₆ | 6 | match |
| 11 | 5 | N₁,N₅ | E₁,E₂,E₅,E₁₀ | 6 | match |
| 13 | 3 | N₁,N₃ | E₁,E₂,E₃,E₆ | 6 | match |
| 17 | 1 | N₁ | E₁,E₂ | 3 | match |

And for the open range: `q=19` → 9 children (`μ=9`); `q=23` → 6; `q=29` → 6;
`q=31` → 12 (`μ=15`); `q=37` → 9; `q=41` → 6; `q=43` → 12; `q=47` → 6.

**A branch has exactly 3 first-input children iff `μ = 1`, i.e. iff `q` is a
Fermat prime.** The paper's two smallest-inventory branches being `q = 5` and
`q = 17` is therefore structural, not luck — see §5.

---

## 2. Theorem 2 — sharp lower-prime avoidance, and the Euler residue restriction

Before using the paper's Lemma 3.2 I re-verified it by brute force: 5265 cases
over `ℓ < 30`, `p < 60`, `e ≤ 39`, zero mismatches (`inversion/02`).

> **Theorem 2.** For every odd prime `ℓ < q` and every `p ∈ S`, with
> `d_ℓ = ord_ℓ(p)`: if `d_ℓ = 1` then `ℓ ∤ n_p`; if `d_ℓ > 1` then `d_ℓ ∤ n_p`.
> For non-Euler `p` (`n_p` odd) the second clause binds only when `d_ℓ` is odd,
> i.e. `d_ℓ | oddpart(ℓ−1)`. For `π` (`n_π ≡ 2 mod 4`) it binds only when
> `v₂(d_ℓ) ≤ 1`.

> **Corollary 2a (Euler residue restriction).** For every odd prime `ℓ < q`,
> `π ≢ −1 (mod ℓ)`.

*Proof.* `π ≡ −1` gives `ord_ℓ(π) = 2`, and `2 | n_π` since `n_π ≡ 2 mod 4`,
so `π` is an `ℓ`-input, contradicting avoidance. ∎

This generalises the paper's Proposition 9.2, which proves only the case
`q = 5`, `ℓ = 3`. It is a real restriction on the Euler prime:

| q | ℓ < q | surviving fraction of residues |
|---|---|---|
| 5 | 3 | 1/2 |
| 7 | 3,5 | 3/8 |
| 11 | 3,5,7 | 5/16 |
| 13 | 3,5,7,11 | 9/32 |
| 17 | 3,5,7,11,13 | 33/128 ≈ 0.258 (mod 15015) |
| 19 | …,17 | 495/2048 ≈ 0.242 |

> **Corollary 2d.** If `3 ∤ N` (in particular if `q > 3`) then `π ≡ 1 (mod 3)`
> and `3 ∤ α+1`. So `α + 1 = 2m` with `m` odd and `gcd(m,3) = 1`.

---

## 3. Lemma OC — order collision, the engine

> **Lemma OC.** Let `p ∈ S` and `d | n_p`. For every odd prime `ℓ < q`:
> either `p ≡ 1 (mod ℓ)` and `ℓ ∤ d`, or `p ≢ 1 (mod ℓ)` and `p^d ≢ 1 (mod ℓ)`.

*Proof.* If `p ≡ 1 mod ℓ` then `ord_ℓ(p) = 1`, avoidance gives `ℓ ∤ n_p`, and
`d | n_p`. Otherwise `d_ℓ = ord_ℓ(p) > 1`, avoidance gives `d_ℓ ∤ n_p`, so
`d_ℓ ∤ d`, which is exactly `p^d ≢ 1 mod ℓ`. ∎

**Why this is the right engine.** Every `r ∈ S` must be *produced*: `e_r > 0`,
so the `r`-adic balance forces some `p ∈ S` with `ord_r(p) | n_p`. Writing
`d = ord_r(p)`, the production order divides both `r−1` and `n_p`, so Lemma OC
constrains the witness. Production is a covering problem constrained by
avoidance — a forcing constraint, not an envelope.

---

## 4. Two negative results (the honest part)

> **Negative Result 1.** Abundancy plus cardinality cannot force *any* prime
> into `S`.

The tempting thought is that since `∏ p/(p−1) > 2` only barely holds for the
`k₀(q)` smallest primes `≥ q`, the support must be dense among small primes.
It need not be. `ω(N)` has no upper bound, and `Σ 1/p` diverges, so for every
bound `P` the primes `≥ P` supply the product alone — verified: primes `≥ 101`
reach abundancy 2 with 1331 primes (largest 11199); primes `≥ 1009` do it with
82269 primes (largest 1054395). Any argument of this shape is dead; recording
it as closed saves the next person the detour.

> **Proposition D.** Lemma OC alone can never block a non-Euler production.

The admissible residue count for a witness of order `d` modulo `ℓ` is
`A(d,ℓ) = (ℓ−1) − gcd(d,ℓ−1) + [ℓ ∤ d]`. `A(d,ℓ) = 0` needs both `(ℓ−1) | d`
and `ℓ | d`; but `ℓ−1` is even and `d` is odd, so `(ℓ−1) | d` is impossible.
Hence `A(d,ℓ) ≥ 1` always (verified over all odd `d ≤ 999`, `ℓ < 60`;
minimum 1 at `d=3, ℓ=3`). **No single production obligation is ever
contradictory**, so this framework constrains but does not close.

It constrains sharply, though. For `q = 17`, the admissible density of a
witness producing `r` by order `d`, over `ℓ ∈ {3,5,7,11,13}`:

| r | oddpart(r−1) | kind | orders d>1 | best density |
|---|---|---|---|---|
| 17 | 1 | **order-1 only** | — | — |
| 19 | 9 | hard | 3, 9 | 0.278 |
| 31 | 15 | hard | 3,5,15 | 0.450 |
| 73 | 9 | hard | 3,9 | 0.278 |
| 97 | 3 | hard | 3 | 0.278 |
| 47 | 23 | free | 23 | 1.000 |
| 103 | 51 | free | 3,17,51 | 1.000 |

*free* = `oddpart(r−1)` has a prime factor `≥ q`, so production is cheap.
*hard* = all prime factors of `oddpart(r−1)` are `< q`, so OC bites.

---

## 5. Proposition E — Fermat-prime forcing, without the minimal-prime hypothesis

The one result here I think is worth something on its own.

> **Proposition E.** Let `N` be odd perfect and let `F | N` be a Fermat prime
> (`F ∈ {3,5,17,257,65537}`, `F − 1 = 2^s`). Then at least one of:
> (a) some non-Euler `p | N` has `p ≡ 1 (mod F)` and `F | e_p + 1`;
> (b) `π ≡ 1 (mod F)` and `F | α + 1`;
> (c) `π ≡ −1 (mod F)`.

*Proof.* `F ∈ S` forces an `F`-input witness `p` with `ord_F(p) | n_p`. But
`ord_F(p) | F−1 = 2^s`, so `ord_F(p)` is a power of 2. If `p` is non-Euler,
`n_p` is odd, so `ord_F(p) = 1`: case (a). If `p = π`, `v₂(n_π) = 1` forces
`ord_F(π) ∈ {1,2}`: cases (b), (c). ∎

In case (a), `Φ_F(p) | σ(p^{e_p})`, LTE gives `v_F(Φ_F(p)) = 1` (checked for
all `p ≡ 1 mod F` up to 4000, `F = 3,5,17`, no failures), and every prime of
`Φ_F(p)/F` is `≡ 1 mod F` and `> F`. So `N` acquires a support prime `≥ L(F)`
and `e_p ≥ F − 1`.

| F | L(F) | case (a) forces |
|---|---|---|
| 5 | 11 | `Ω(N) ≥ 4` |
| 17 | 103 | `Ω(N) ≥ 16` |
| 257 | 1543 | `Ω(N) ≥ 256`, and a prime factor `≥ 1543` |
| 65537 | 917519 | `Ω(N) ≥ 65536`, and a prime factor `≥ 917519` |

This is exactly the paper's `q = 5` / `q = 17` forced-or-pure mechanism **with
the hypothesis "`F` is the smallest prime factor" removed** — it applies to any
Fermat prime dividing `N`, at any position. It also explains why those two
branches had three-leaf inventories: by Theorem 1, a branch has 3 first-input
children iff `μ = 1` iff `q` is a Fermat prime, and 5 and 17 are the only
Fermat primes in `{5,7,11,13,17}`.

The unconditional readings are the interesting ones:

> If `257 | N`, then `π ≡ ±1 (mod 257)` (with the stated exponent condition),
> or `Ω(N) ≥ 256` and `N` has a prime factor `≥ 1543`.
>
> If `65537 | N`, then `π ≡ ±1 (mod 65537)`, or `Ω(N) ≥ 65536`.

---

## 6. Forced endpoints `L(q)` for every branch

`L(q)` = least prime `r > q` with `r ≡ 1 mod q`; this is the order-one forced
support prime. The complete candidate list starts at `r = q+1`, not `2q+1`.

| q | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 41 | 43 | 47 | 53 | 59 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L(q) | 11 | 29 | 23 | 53 | **103** | 191 | 47 | 59 | 311 | 149 | 83 | 173 | 283 | 107 | 709 |

Note `L(q) = 2q+1` for `q = 11, 23, 29, 41, 53`: those branches have *much*
weaker forced endpoints than `q = 17`, so the `q ≥ 19` extension is not
uniformly easier or harder — it varies with the arithmetic of `q−1`.

Footnote to the audit: the candidate `r = q+1` is always even, hence never
prime, so dropping it can never change `L(q)`. That mathematically excuses the
release certificate's list `[35,52,69,86]` for `q = 17` (which omits 18) and
the same omission in the paper's Table 6. The audit point is unaffected: the
verifier hardcodes that list and checks no completeness property, so it would
equally accept an omission that *did* matter.

---

## 7. Status

| result | status |
|---|---|
| Theorem 1 (first-input classification, all q) | **proved**; reproduces all 5 paper branches |
| Theorem 2, Corollaries 2a, 2d | **proved** |
| Lemma OC | **proved** |
| Negative Result 1 | **proved** + verified |
| Proposition D | **proved** + verified |
| Proposition E (Fermat forcing) | **proved**; LTE step spot-checked |
| `L(q)` table, `A(d,ℓ)` densities | **computed**, exact |
| Zelinsky's Theorem 1, both cases | **independently verified** (§8) |
| Corollary 2e (exponent floors) | **proved**; `ℓ=3` case known, `ℓ<q` case new-to-me |
| Improved `Ω`/`ω` bound in a branch | **not obtained** — needs the counting lemmas of §9 |
| Any branch closure | **not obtained** — and Proposition D says not by OC alone |

**Where it stalls, precisely.** Every constraint in this framework is a
forcing constraint: its consequences all have the form "`S` must contain more,
or larger, primes". No finite conjunction of such statements contradicts
`σ(N) = 2N`, because by Negative Result 1 arbitrarily sparse, arbitrarily large
supports satisfy the abundancy requirement. Closure therefore needs a
constraint of a *different kind* — a congruence obstruction, or a genuine
bound on `N` or `ω(N)`. Proposition A says the envelope route to the latter is
unavailable. That is the real bottleneck, stated exactly.

The one place the framework still has teeth is §5: Fermat-prime forcing is a
forcing constraint whose *cost* (`Ω(N) ≥ F−1`) grows super-polynomially in `F`,
so it interacts with exponent and multiplicity constraints rather than with
abundancy. That is the direction I would push next.

## 8. Zelinsky's LP method — verified, and what it says about §2

Zelinsky, *An improvement of an inequality of Ochem and Rao concerning odd
perfect numbers*, arXiv:1706.07009v3 (2017), proves

> `3 ∤ N  ⟹  Ω(N) ≥ (8/3)ω(N) − 7/3`,  `3 | N  ⟹  Ω(N) ≥ (21/8)ω(N) − 39/8`,

improving Ochem–Rao's `Ω ≥ (18/7)ω − 31/7` (*Math. Comp.* **83** (2014),
2435–2439; their second bound `Ω ≥ 2ω + 51` is stronger while `ω ≤ 81`).

**I verified both derivations independently** (`inversion/05`). Each is an
explicit nonnegative rational combination of the paper's numbered relations;
reconstructing the combinations symbolically reproduces both targets. In fact
each proves slightly *more* than stated:

| case | stated | what the combination actually gives |
|---|---|---|
| `3 ∤ N` | `Ω ≥ (8/3)ω − 7/3` | `Ω ≥ (8/3)ω − 7/3 + (2/9)s₂,₂` |
| `3 \| N` | `Ω ≥ (21/8)ω − 39/8` | `Ω ≥ (21/8)ω − 39/8 + (1/8)s₃,₂` |

Applied to the `q = 17` branch with my `k₀(17) = 62`: Ochem–Rao's `2ω + 51`
gives **`Ω(N) ≥ 175`**, and Zelinsky's `3∤N` bound gives `Ω(N) ≥ 163` — the
former wins here, consistent with Zelinsky's own remark that it does so for
`ω ≤ 81`.

### The novelty check I asked for, answered against §2

**The `ℓ = 3` case of my Theorem 2 is not new.** Zelinsky's relation (12),
`s₂,₁ + s₃,₁ ≤ f₃`, together with `f₃ = 0` when `3 ∤ N`, already yields "every
prime with `e_p = 2` is `≡ 2 (mod 3)`" — which is exactly what Theorem 2 gives
at `ℓ = 3` for the exponent 2. Ochem–Rao and Zelinsky both use it.

What is *not* in that literature is the extension to **every** odd `ℓ < q`,
which requires the minimal-prime hypothesis they do not assume. Theorem 2 is
therefore best presented as: the known `ℓ = 3` constraint, generalised along
the whole lower-prime range that a minimal-prime branch supplies.

It is also stronger than the `e_p = 2` instance even at `ℓ = 3`: it gives
`e_p ≢ 2 (mod 3)`, excluding `e_p ∈ {2, 8, 14, 20, …}` for non-Euler
`p ≡ 1 mod 3`, where the LP's `S`/`T` split only sees `e_p = 2` versus
`e_p ≥ 4`.

---

## 9. Corollary 2e — residue-dependent exponent floors

This is the form in which §2 feeds an LP.

> **Corollary 2e.** Let `q = min S` and let `p ∈ S` be non-Euler, so
> `n_p = e_p + 1` is odd and `≥ 3`. Put
> `Forb(p) = {ℓ < q : p ≡ 1 mod ℓ} ∪ {d : d = ord_ℓ(p)` is an odd prime, some
> odd `ℓ < q}`. By Theorem 2 no element of `Forb(p)` divides `n_p`, so
> `n_p ≥ (least prime not in Forb(p))` and `e_p ≥` that `− 1`.

For `q = 17` (`ℓ ∈ {3,5,7,11,13}`, binding odd orders `ℓ=7 → 3`, `ℓ=11 → 5`,
`ℓ=13 → 3`) the floors over the 543 primes `19 ≤ p < 4000` come out as:

| forced floor | share of primes | cumulative |
|---|---|---|
| `e_p ≥ 2` | 27.8% | 27.8% |
| `e_p ≥ 4` | 34.3% | 62.1% |
| `e_p ≥ 6` | 33.1% | 95.2% |
| `e_p ≥ 10` | 4.4% | 99.6% |
| `e_p ≥ 12` | 0.4% | 100.0% |

**72.2% would be forced to `e_p ≥ 4`** — matching the exact density
`1 − (1/2)(2/3)(5/6) = 13/18` for `3 ∈ Forb(p)`.

**Caveat, stated because it is the whole difficulty.** These are properties of
the primes in that range, *not* of `S`, which is not a random set. They measure
how hard the constraint bites; they prove nothing about `N` on their own. In
Zelinsky's LP, `s` counts primes with `e_p = 2` and `t` those with `e_p ≥ 4`,
and Corollary 2e would move most of `s` into `t` — but only given a *counting*
argument tying residue classes to the support. Supplying that is the analogue
of Zelinsky's Lemma 4 for `ℓ = 5, 7, 11, 13`, and it is the next task. **It is
not done here.**

If it can be done, the deliverable is concrete and in the same genre as the
Ochem–Rao / Zelinsky / Clayton–Hansen line: **an improved `Ω` versus `ω`
inequality valid in the branch `q = min S`, with the coefficient growing with
`q`.** That is real progress on the odd perfect number problem — though note it
is a *forcing* result, so by §7 it still does not close a branch.

A transcription flag: the Mantovanelli introduction attributes to
Clayton–Hansen (2023) the bounds `Ω ≥ (99/37)ω − 187/37` and, for `3 ∤ N`,
`Ω ≥ (46/19)ω − 51/19`. The second has slope ≈ 2.42, weaker than Zelinsky's
2.67 for the same hypothesis, which is odd for a later paper. I have not been
able to check Clayton–Hansen and am not relying on either figure.

---

## 10. Novelty caveat

Theorem 1, Theorem 2 and Corollary 2a are elementary and may well be known;
they are stated here because the paper leaves Theorem 1 explicitly open and
proves Corollary 2a only in the case `q = 5`, `ℓ = 3`. **Theorem 2 at `ℓ = 3`
is now confirmed to be known** — it is Zelinsky's (12) with `f₃ = 0` (§8). The
`ℓ < q` generalisation, Corollary 2e, and Proposition E remain unchecked
against the literature; I cannot search it from this container. None of them
should be called new until checked.

Still outstanding, in priority order: (1) Kishore 1981 / Norton 1961, for the
best known lower bound on `ω(N)` in terms of the least prime factor — the
novelty check on my `k₀(q)` table; (2) Ochem–Rao, *On the number of prime
factors of an odd perfect number*, Math. Comp. **83** (2014), 2435–2439, for
their full inequality system, which is what an extended LP would build on;
(3) anything pairing "Fermat prime" with "odd perfect number", to check
Proposition E.
