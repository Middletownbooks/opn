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

## 8. Novelty caveat

Theorem 1, Theorem 2 and Corollary 2a are elementary and may well be known;
they are stated here because the paper leaves Theorem 1 explicitly open and
proves Corollary 2a only in the case `q = 5`, `ℓ = 3`. Proposition E I have not
seen, but I have not been able to search the literature from this container.
None of these should be called new until checked — see the document requests.
