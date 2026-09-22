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

**Correction (added after reading Ochem–Zelinsky 2026).** This has a one-line
proof needing no cyclotomic machinery at all: `α` is odd, so
`(π+1) | σ(π^α)`; if `ℓ | π+1` then `ℓ | σ(π^α) | σ(N) = 2N`, so `ℓ | N`,
contradicting `ℓ < q = min S`. That argument is standard — it is the first
move in Ochem–Zelinsky's Lemma 6 — so **Corollary 2a should be regarded as
known in substance**, not as a new result. It generalises the *statement* of
the paper's Proposition 9.2 (proved there only for `q = 5`, `ℓ = 3`), but the
technique is routine. It remains a real restriction on the Euler prime:

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

**A propagation tool from the literature.** Ochem–Zelinsky 2026 (Lemma 5)
supply exactly the rule this framework was missing:

> Let `x, s, t` be distinct primes with `x ∤ t−1` and `s ∤ t−1`. If
> `ord_s(t) | ord_x(t)`, then for every `v ≥ 1`, `x | σ(t^v)` implies
> `s | σ(t^v)`.

That is a *co-production* rule: producing `x` from `t` forces producing `s`
from the same component. It turns the production graph from a covering problem
into one with implications along it, which is what makes their factor trees
terminate. Their Lemma 4 — `ord_s(n)` even implies `s ∤ σ(n^q)` for even `q` —
is the same even-order observation that underlies Theorem 1 here, confirming
that mechanism is standard.

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
| Proposition E (Fermat forcing) | **proved**; but applies to ≤ 5 primes (§9e) |
| Theorem 1' (all prime divisors) | **proved** — minimality never used (§9e) |
| "restrained" usable in branches q ≥ 5 | **no** — vacuous there (§9d) |
| `k`-restrained forces `k ≥ 5` when `3 ∤ N` | **attempted and NOT proved** (§9d) |
| `L(q)` table, `A(d,ℓ)` densities | **computed**, exact |
| Zelinsky's Theorem 1, both cases | **independently verified** (§8) |
| Ochem–Zelinsky 2026 §2 abundancy bound | **independently verified** (§9b) |
| Ochem–Zelinsky Table 1 (`s < 200000`) | **reproduced exactly** (§9c) |
| Proposition D's *conclusion* | **corrected** — closure comes from iteration (§9c) |
| Corollary 2a | **proved**, but now known to be routine (§2 correction) |
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

## 9b. Ochem–Zelinsky 2026, and the repair the certificate actually needed

Ochem & Zelinsky, *On odd perfect numbers with exactly one even exponent
greater than 2*, arXiv:2607.19746v1 (22 Jul 2026), prove that a "restrained"
odd perfect number (all even exponents 2 except one) must have notable prime
3 and notable exponent `q ≥ 23,000,000,000`.

**I verified their Section 2 abundancy computation** (`inversion/07`). All four
constants reproduce to full printed precision:

| constant | recomputed | paper |
|---|---|---|
| `A₁ = 91/72` | 1.26388888888888888889 | 1.26388888888888888888 |
| `A₂` (11 tabulated `m(a,b)`) | 1.32051931736840940811 | 1.32051931736840940811 |
| `A₃ = (1+10⁻⁹)³` | 1.00000000300000000300 | 1.00000000300000000300 |
| `A_∞` | 1.01178747704420359447 | 1.01178747704420359446 |
| product | **1.68866287554177807591** | 1.68866287554178 |

### This is the correct form of the envelope my audit killed

Proposition A says the **finite-slot** envelope `H(K_env)(B/(B−1))^M < 2` is
never satisfiable by valid data. Ochem–Zelinsky nevertheless bound an abundancy
from above, successfully. There is no conflict: their envelope has a different
shape, and the difference is precisely the repair Mantovanelli's certificate
needed.

They partition the remaining support into **infinitely many classes** — the
pairs `(a,b)` with `σ(s²) = p^a n^b` — then prove (i) at most one support prime
lies in each class, and (ii) a lower bound `m(a,b)` on that prime which *grows*
with `a+b` (their §2.4: `s ≥ 7^{k/2} − 1` for `k = a+b`). The resulting infinite
product converges, and converges below 2.

What makes it work, point by point against `tail_count_certificate(B,M)`:

| requirement | Ochem–Zelinsky | Mantovanelli |
|---|---|---|
| classification of the remaining support | **proved** (the `(a,b)` classes) | none — a bare count `M` |
| per-class lower bounds | **proved**, and growing | one flat `B = 59`, asserted |
| bound on `ω(N)` needed? | **no** — infinitely many classes allowed | yes, `ω ≤ 20`, in disguise |
| convergence | proved | n/a |

So the envelope idea is not inherently broken, and my §7 verdict should be read
precisely: *the finite-`M` form* is unrepairable, because a finite `M` is an
upper bound on `ω(N)` in disguise. The move that rescues it is to allow
infinitely many classes with growing lower bounds — which costs nothing,
because no bound on `ω(N)` is then required. That is the shape a repaired
certificate would have to take, and this paper shows the technique is rigorous
and available when the classification is genuinely proved.

---

## 9c. The factor-tree prover — and a correction to Proposition D

Ochem & Zelinsky's released code (`tree.cpp`, `pairs.py`, `all.cpp`) mechanises
exactly the production/forcing framework of §3. Reading it corrects one of my
own conclusions.

### Correction to Proposition D

Proposition D showed Lemma OC can never block a *single* production, and I
concluded the framework "constrains but does not close". **That was too quick.**
`tree.cpp` closes branches with the same forcing, by *iterating* it and
terminating on one of three downstream contradictions:

| rule | meaning |
|---|---|
| `F t` | a forced prime `t` is one already ruled out (their driver: any prime below the current root) |
| `XS t` | three or more copies of `t` are forced, but `t` is ordinary (`e_t = 2`) and supplies only two |
| `a(·) > 2` | the partial product of **exact** component abundancies `σ(p^e)/p^e` over the known components already exceeds 2 |

The correct statement: no single production obligation is contradictory
(Proposition D stands), but the *transitive closure* of the obligations can be.
§3 was missing the iteration and these termination rules, not the constraints.

### The two sound abundancy directions

Worth stating plainly, because it sharpens the audit:

1. **Partial lower bound.** `σ(N)/N = ∏ σ(p^{e_p})/p^{e_p}` with every factor
   `> 1`, so a partial product over *known* components exceeding 2 is a
   contradiction. Exact, finite, needs no classification. This is `a(·) > 2`.
2. **Classified upper envelope.** Proved classes, proved growing per-class
   lower bounds, convergent product `< 2` (§9b).

Mantovanelli's tail envelope is neither — it is an upper bound over a finite
*assumed* slot count. Direction 1 was available to him for free and requires no
certificate at all.

### Reproduction of their Table 1

I re-ran their `pairs.py` at limit 200000. **All seven entries of Table 1 with
`s < 200000` reproduce exactly**, including the `p` and `n` values:

| (a,b) | s | p | n |
|---|---|---|---|
| (0,1) | 5 | – | 31 |
| (1,0) | 59 | 3541 | – |
| (1,1) | 29 | 13 | 67 |
| (1,2) | 863 | 15217 | 7 |
| (2,1) | 1667 | 13 | 16453 |
| (1,3) | 1733 | 8761 | 7 |
| (1,4) | 2819 | 61 | 19 |

(Their code is not redistributed here; only the result is recorded.)

### Code-audit observations on `tree.cpp`

In the same spirit as the main audit, what the program does and does not
establish:

- **The early-abort rule is inductive, not self-contained.**
  `factorize_with_early_abort` treats "a forced prime `< root`" as a
  contradiction. That is valid only given "every prime below `root` has already
  been excluded", which is established *outside* the program (hand arguments
  for 5 and 7, `3p2.txt` to 1000, `tree.txt` to 3,000,000). The program's
  output is meaningful only inside that induction. The paper's narrative
  handles this correctly; the code alone does not show it.
- **Primality is probabilistic.** `miller_rabin(n, 25)` and
  `mpz_probab_prime_p(x, 25)`. The factorisations underpinning the proof are
  therefore probabilistic, not certified — exactly the class of trusted
  computational input this project tracks. A certified version would need
  primality certificates.
- **Cycle handling is conservative, hence safe.** When a forced prime is
  already on the path the code `continue`s rather than claiming a
  contradiction, which can only weaken the prover.
- **Both branches are required.** `prove` returns
  `ord_contradicted && sp_contradicted` when the special branch is eligible —
  correct, since `x` could be either.
- **`x % 12 == 1` encodes Lemma 6.** `x ≡ 1 mod 4` is Euler's condition and
  `x ≡ 1 mod 3` is their Lemma 6, which is proved only for *restrained* `N`.
  So the program inherits that hypothesis.
- **The special branch follows only `(x+1)/2`**, a valid *subset* of the primes
  forced by `σ(x^e)`; conservative, hence sound.
- **`G /= 3` when `x ≡ 1 mod 3` is exact**: `v₃(x²+x+1) = 1` there, since
  `x = 1+3k` gives `3(1+3k+3k²)` with the cofactor `≡ 1 mod 3`.
- **The released `main()` does not terminate.** `mpz_class r = bound;
  while (1) { … mpz_nextprime(r, r); }` — the commented-out
  `//mpz_class r = 1009; while (r <= bound)` shows the intended bounded form.
  As shipped, the SUMMARY block is unreachable and the run must be killed. Not
  a soundness defect; each root is still tested correctly.

### Why the tree does not transfer to a general minimal-prime branch

`tree.cpp` branches on exactly two possibilities per prime: ordinary
(`e_x = 2`, so `σ(x²) = x²+x+1`, one number to factor) and special (the odd
part of `x+1`, one number). **That bounded branching is precisely what the
restrained hypothesis buys.**

In a general minimal-prime branch there is no such bound: `e_x` ranges over
every even number with `n_x` odd and avoiding `Forb(x)`, so `σ(x^{e_x})` is one
of infinitely many integers and the tree branches infinitely at every node.
Corollary 2e bounds `e_x` from *below*, which delays the branching but does not
make it finite.

Verified instance (`inversion/08`): at `q = 17`, every `ord_ℓ(17)` for
`ℓ ∈ {3,5,7,11,13}` is even (2, 4, 6, 10, 6), so `Forb(17) = ∅` and **no prime
below 17 can ever divide `σ(17^{e_17})`** — which is exactly why 17 is
admissible as a least prime, and why `e_17` carries no lower-prime constraint.
Taking the least exponent `e_17 = 2` gives `σ(17²) = 307`, prime, `≡ 1 mod 17`;
then `Forb(307) = {3}`, so `e_307 ≥ 4`.

**So the transfer needs an upper bound on exponents** — the same missing
ingredient as everywhere else here. That is the obstruction, stated exactly.

---

## 9d. Why "restrained" is not available to me — and Theorem 1'

### The restrained hypothesis is *vacuous* in every branch I care about

Ochem–Zelinsky's Theorem 1 is conditional: *if* `N` is restrained then `n = 3`
and `q ≥ 23,000,000,000`. Their route there is the point:

- **§2** assumes `N` restrained and `3 ∤ N`, and shows **no such `N` exists**
  (the `A₁A₂A₃A_∞ < 2` computation I reproduced in §9b).
- **§3** assumes `N` restrained and `3² ‖ N`, and shows no such `N` exists.
- **§4** concludes 3 must be the notable prime.

So **restrained ⟹ 3 | N ⟹ min S = 3**, and therefore:

> **Corollary.** No restrained odd perfect number has smallest prime factor
> `≥ 5`. The restrained sub-case of every branch `q ∈ {5,7,11,13,17}` — indeed
> of every `q ≥ 5` — is already closed unconditionally, by their §2 alone.

That is why I cannot simply adopt it. In a minimal-prime branch with `q ≥ 5`
the hypothesis "restrained" is already known to be unsatisfiable, so anything I
proved under it would be **vacuously true**. I need a hypothesis that bounds
exponents *and* is non-vacuous when `3 ∤ N`.

### The right generalisation: the `k`-restrained ladder

Call `N` **`k`-restrained** if exactly `k` of its even exponents exceed 2
(McDaniel gives `k ≥ 1`; restrained is `k = 1`). This is the natural ladder:
it is non-vacuous for `k ≥ 2` when `3 ∤ N`, and the factor tree keeps **finite
branching at ordinary nodes** for any fixed `k`, since all but `k` components
have `e_p = 2`.

Corollary 2e bites here directly: when `3 ∤ N`, every `p ∈ S` with `p ≡ 1 mod 3`
has `e_p ≠ 2`, hence is non-ordinary, so

  `k ≥ #{p ∈ S : p ≡ 1 mod 3} − 1`   (the `−1` for the Euler prime, which is
  `≡ 1 mod 3` by Corollary 2d).

**An attempt that did not work, recorded so it is not repeated.** I tried to
turn this into "`k`-restrained with `3 ∤ N` forces `k ≥ 5`", via: every ordinary
`p ≡ 2 mod 3` has all prime factors of `σ(p²)` congruent to `1 mod 3`, so the
map *ordinary prime ↦ largest prime factor of `σ(p²)`* would be injective into
`A = {p ∈ S : p ≡ 1 mod 3}`, giving `ω(N) ≤ 2|A| + …` and contradicting
`ω(N) ≥ 12`. **The injectivity step does not transfer.** Zelinsky's Lemma 4
establishes it only for components whose `σ(p²)` has at most two prime factors
(his `S₁`, `S₂`); for `S₃` the size argument `σ(a²)/q > √(σ(a²))` fails. The
weaker valid replacement — each `a ∈ A` absorbs at most `e_a` such
contributions — gives no bound, because the `e_a` are unbounded. So the
`k ≥ 5` claim is **not proved** and should not be quoted.

---

## 9e. Theorem 1' — the classification holds at every prime divisor

Working on Proposition E showed that Theorem 1 was understated.

> **Theorem 1'.** Let `N` be odd perfect and let `r` be **any** prime with
> `r | N`. Write `r − 1 = 2^a·μ(r)` with `μ(r)` odd. Then some `p ∈ S`,
> `p ≠ r`, is an `r`-input witness, and `ord_r(p) | μ(r)` if `p` is non-Euler,
> `ord_r(π) | 2μ(r)` if `p = π`.

The proof is the one already given, and **it never uses `q = min S`** — only
`r | N` (for `e_r ≥ 1`), `e_p` even for non-Euler `p`, and `α + 1 ≡ 2 mod 4`.
The earlier Theorem 1 is the case `r = q`.

Define the **production width** `w(r) = d(μ(r))`, the number of odd divisors of
`r − 1`. Then `r` admits `w(r)` non-Euler input orders and `2w(r)` Euler ones —
`3w(r)` input types.

**Proposition E is exactly the case `w(r) = 1`**, i.e. `r − 1` a power of 2,
i.e. `r` a Fermat prime; the sole non-Euler order is 1, forcing `p ≡ 1 mod r`
and `r | n_p`, hence `e_p ≥ r − 1`.

### The ceiling on Proposition E, stated plainly

`w(r) = 1` iff `r` is a Fermat prime. Only 3, 5, 17, 257, 65537 are known, and
none others exist below `2^{2^32}`. **So Proposition E has content for at most
five primes** — in a branch `q = min S`, only the Fermat primes `≥ q`, which
for `q = 17` means `{17, 257, 65537}`. It is a sharp statement about a very
thin set, not a general tool. I would rather say that than let it look bigger
than it is.

What survives the ceiling is Theorem 1' and the invariant `w(r)`. Width over
primes `r < 10000`:

| `w(r)` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | >8 |
|---|---|---|---|---|---|---|---|---|---|
| primes | 4 | 253 | 13 | 458 | 3 | 122 | 2 | 241 | 132 |
| share | 0.33% | 20.6% | 1.1% | 37.3% | 0.2% | 9.9% | 0.2% | 19.6% | — |

Low width is common — over 20% of primes have `w(r) = 2`, where production
needs `ord ∈ {1, ℓ}` for a single odd prime `ℓ`. So the *mechanism* behind
Proposition E is broadly applicable even though Proposition E itself is not.

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
