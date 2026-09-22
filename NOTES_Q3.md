# The q = 3 branch — first checkpoint

Working notes. Scripts in `q3/`, standard library only. Setting: `N` odd
perfect, `N = π^α m²` with `π ≡ α ≡ 1 (mod 4)`, `n_p = e_p + 1`. Since
`3 ≡ 3 (mod 4)`, **3 is never the Euler prime**, so `e_3` is even whenever
`3 | N` and `n_3` is odd.

---

## 1. What dies, and why the branch really is different

The engine of the whole minimal-prime programme is **lower-prime avoidance**:
for every odd prime `ℓ < q` and every `p | N`, `v_ℓ(σ(p^{e_p})) = 0`. At
`q = 3` the set of odd primes below `q` is **empty**, so the hypothesis is
vacuous and every tool built on it dies with it — Corollary 2e (exponent
floors), Lemma OC, the forbidden-set machinery, the residue restrictions on
`π`. That is not a gap in anyone's argument; it is the structural fact the
literature flags.

**The second instrument dies too, and this is the part worth emphasising.** At
`q = 5…17` the other live tool was the abundancy floor `k₀(q)` — the thing that
refuted `M = 18`. It grew fast: `7, 15, 27, 41, 62`. At `q = 3` it collapses to
`k₀(3) = 3`, because **3 itself supplies almost all of the required factor 2**:

| `e_3` | `σ(3^{e_3})/3^{e_3}` | left for everything else |
|---|---|---|
| 2 | 1.444444 | 1.384615 |
| 4 | 1.493827 | 1.338843 |
| 6 | 1.499314 | 1.333943 |
| → ∞ | → 1.5 | → 4/3 |

and `∏ p/(p−1)` over primes `≥ 5` exceeds `4/3` after just **two** primes
(`5, 7`). So abundancy constrains essentially nothing here.

**Both instruments that drove the `q = 5…17` work are therefore absent at
`q = 3`.** Something else has to carry the weight.

## 2. What survives

Everything needing only Euler's form and valuation balance: the balance
identity, the cyclotomic input condition, **Theorem 1′** (input classification
at every prime divisor — its proof never used minimality), and **Proposition E**,
since `3 − 1 = 2` makes `μ(3) = 1`: **3 is a Fermat prime**, so it has
production width 1.

Proposition E at `F = 3` gives a clean trichotomy — either some non-Euler
`p ≡ 1 (mod 3)` has `3 | e_p+1`, or `π ≡ 1 (mod 3)` with `3 | α+1`, or
`π ≡ −1 (mod 3)`. But it is **weak here**: its force elsewhere is
`e_p ≥ F − 1`, which at `F = 3` reads `e_p ≥ 2` and is vacuous. Honest
assessment: Proposition E does not do useful work at `q = 3`.

## 3. Three constraints that do survive — quadratic residues

These need no lower primes, so they are available at `q = 3`.

> **Lemma QR.** Let `p` be a **non-Euler** prime factor of `N` and `r` a prime
> dividing `σ(p^{e_p})`. Then `p` is a quadratic residue mod `r`.

*Proof.* `p` non-Euler ⟹ `e_p` even ⟹ `n_p` odd. `r | σ(p^{e_p})` ⟹
`ord_r(p) | n_p`, so `ord_r(p)` is odd; writing `r−1 = 2^a m` with `m` odd and
`a ≥ 1`, `ord_r(p) | m | (r−1)/2`, so `p^{(r−1)/2} ≡ 1`. ∎

*Sharpness.* For `r ≡ 3 (mod 4)`, `v₂(r−1) = 1`, so "`ord_r(p)` odd" is
**equivalent** to `(p/r) = 1` — nothing is lost. For `r ≡ 1 (mod 4)` the order
condition is strictly stronger. Verified on 90 instances, no failures.

This is Ochem–Zelinsky's Lemma 4 in quadratic-residue clothing; the value of
the QR form is that reciprocity applies to it.

> **Lemma 3MOD12.** If `3 | N` then every prime `r > 3` dividing `σ(3^{e_3})`
> satisfies `r ≡ ±1 (mod 12)`.

Immediate from Lemma QR plus `(3/r) = 1 ⟺ r ≡ ±1 (mod 12)`. **No "restrained"
hypothesis** — this is the general-`N` form of the lemma I found earlier inside
Ochem–Zelinsky's framework. Verified for all prime factors below `10⁵` of
`σ(3^e)`, even `e ≤ 32`, no violations.

*Corollary.* The component `3^{e_3}` can **never** produce a prime `≡ 5` or
`≡ 7 (mod 12)`.

> **Lemma NO2CYCLE.** Let `p, s` be distinct non-Euler prime factors of `N`
> with `p ≡ s ≡ 3 (mod 4)`. Then they cannot each produce the other.

*Proof.* Mutual production gives `(p/s) = (s/p) = 1` by Lemma QR. But
`p ≡ s ≡ 3 (mod 4)` makes `(p−1)/2` and `(s−1)/2` both odd, so reciprocity
forces `(p/s)(s/p) = −1`. ∎

So **among the prime factors `≡ 3 (mod 4)`, production is 2-cycle-free.**
Verified: zero mutual pairs among the 24 primes `≡ 3 mod 4` below 200, with
even exponents up to 12 on both sides — as reciprocity requires. Worked
instance: `ord₁₁(7) = 10` is even so `11 ∤ σ(7^{even})`, while `ord₇(11) = 3`
is odd and `7 | σ(11²) = 133`; the Legendre symbols multiply to `−1`.

This is the one piece here I would flag as possibly new; it is elementary, so
it may well be known. It needs a literature check before being called new.

## 4. The exact 3-adic balance

Component valuations, verified on 500 instances with no failures:

- `p ≡ 1 (mod 3)`: `v₃(σ(p^{e_p})) = v₃(n_p)` (LTE).
- `p ≡ 2 (mod 3)`: `σ(p^{e_p})` is a sum of `n_p` terms alternating `±1 mod 3`,
  so `v₃ > 0` iff `n_p` is even iff `p` is the Euler prime; then
  `v₃ = v₃(p+1) + v₃(n_p/2)`.

Hence, for any odd perfect `N` with `3 | N`:

> **`e_3 = Σ_{non-Euler p ≡ 1 (3)} v₃(e_p + 1) + E`**, where `E = v₃(α+1)` if
> `π ≡ 1 (mod 3)`, and `E = v₃(π+1) + v₃((α+1)/2)` if `π ≡ 2 (mod 3)`.

**Every non-Euler `p ≡ 2 (mod 3)` contributes nothing.** The entire 3-adic
supply comes from primes `≡ 1 (mod 3)` whose exponent satisfies `3 | e_p+1`,
plus the single Euler component. This is the general form of the identity
`q = o₁ + v₃(e+1)` I proved for the restrained case, without the "ordinary"
hypothesis that made every term there equal 1.

## 5. A parity constraint on the 3-component

`3^{e+1} ≡ 3 (mod 24)` for odd `e+1`, so `σ(3^{e_3}) ≡ 1 (mod 12)`. Since all
its prime factors are `≡ ±1 (mod 12)`, and a product of such primes is
`≡ 1 (mod 12)` exactly when evenly many are `≡ −1`:

> **`σ(3^{e_3})` has an even number of prime factors `≡ 11 (mod 12)`, counted
> with multiplicity.**

Verified for all even `e ≤ 38`, no failures.

## 5b. NO2CYCLE pushed — sharp form, and where it leads

Worked as though novel. Results, in order of what they are worth.

### The sharp production condition

The right general statement is not about quadratic residues at all:

> A non-Euler `t` produces `r` only if `ord_r(t) | oddpart(r−1)`, equivalently
> **`t` is a `2^a`-th power residue mod `r`, where `a = v₂(r−1)`.**

| `r` | `a` | condition on `t` | density |
|---|---|---|---|
| `≡ 3 (mod 4)` | 1 | quadratic residue | 1/2 |
| `≡ 5 (mod 8)` | 2 | quartic residue | 1/4 |
| `≡ 1 (mod 8)` | ≥3 | `2^a`-th power residue | `2^{−a}` |

This is Theorem 1′ in power-residue language. **Lemma QR is the `a = 1` case,
where it is exact** — and that exactness is precisely what lets reciprocity act
on it. Verified on 2656 `(t,r)` pairs with even exponents to 58: no violations.

### Tournament theorem

> Let `T = {p | N : p ≡ 3 (mod 4)}`. Every member is non-Euler (`π ≡ 1 mod 4`).
> For `p, s ∈ T`, reciprocity gives `(p/s)(s/p) = −1`, so **exactly one** symbol
> is `+1`; by the `a = 1` case, `p` can produce `s` only if `(p/s) = 1`. Hence
> the production digraph restricted to `T` lies inside the **tournament** `Λ_T`
> given by `p → s ⟺ (p/s) = 1`, and is 2-cycle-free.

The permitted direction of every pair in `T` is fixed in advance by a Legendre
symbol — no order computation. Tested against the 336 pairs `X → r` with both
`≡ 3 mod 4` appearing in Ochem–Zelinsky's `3p2.txt`: **335 confirm the
prediction**, and the single flag is `(59083, 19)` — the line independently
established as OCR damage.

### The payoff that is actually real: an integrity check

That last observation generalises into something useful. Checking a production
claim `X → r` costs **one modular exponentiation** and needs **no
factorisation** of `σ(X^{e_X})`. So the condition audits factor-tree data
independently of the routine that generated it.

Run over every asserted `X² → r` in `3p2.txt`:

| | |
|---|---|
| production claims checked | **882** |
| failing the power-residue condition | **2** |

and **both failures are the two bogus factors on the one corrupted line**
(`59083 → 19` fails a quadratic-residue test; `59083 → 6604392133` fails a
quartic one). All 880 genuine claims pass.

This matters because searches of this kind rest on large machine-generated
files. Re-running the same factoriser reproduces transcription damage,
truncation and off-by-one errors rather than detecting them; an independent
`O(log r)` test per claim catches them.

### What it does not give — and the decisive negative for `q = 3`

Recorded so they are not repeated:

- **Longer cycles are not obstructed.** A directed cycle inside `T` forces every
  forward symbol to `+1` and every backward symbol to `−1` — perfectly
  consistent. Only 2-cycles die.
- **In-degree starvation fails.** Tournaments need not have an in-degree-0
  vertex, and producers may lie outside `T` regardless: the Euler prime can
  produce **any** `p ≡ 3 (mod 4)` unconstrained, since `ord_p(π) | p−1` has
  `v₂ ≤ 1` automatically when `v₂(p−1) = 1`.
- **At `q = 3` it adds nothing.** This is the decisive point. `3 ∈ T`.
  Producers of 3 are `≡ 1 (mod 3)`, i.e. `≡ 1` or `7 (mod 12)`; 3 produces only
  primes `≡ ±1 (mod 12)`. Within `T` those are the classes `7` and `11 (mod 12)`
  — **disjoint**. So NO2CYCLE is automatically satisfied at 3 and constrains
  nothing there.
- **Stronger reciprocity is the open avenue.** For `r ≡ 1 (mod 4)` the condition
  is quartic or higher, so an obstruction needs biquadratic or octic
  reciprocity. Rational biquadratic laws exist (Burde, Gauss). Not attempted —
  I would not guess at it.

**Verdict on the instruction to work it as novel.** The lemma is real and
sharp, and it yields a genuinely useful tool. It does **not** advance `q = 3`,
for the specific reason in the third bullet: the two production classes at 3
are disjoint mod 12, so the constraint is vacuous exactly where it was wanted.

---

## 6. Status and the obstruction

| result | status |
|---|---|
| tool inventory (what dies / survives) | **established** |
| Lemma QR | **proved** + verified; = Ochem–Zelinsky Lemma 4 restated |
| Lemma 3MOD12, general `N` | **proved** + verified |
| Lemma NO2CYCLE | **proved** + verified; novelty unchecked |
| exact 3-adic balance | **proved** + verified |
| parity of `11 mod 12` factors | **proved** + verified |
| Proposition E at `F = 3` | **applies but is vacuous** |
| NO2CYCLE sharp form (power residues) | **proved** + verified, 2656 pairs |
| tournament theorem | **proved**; 335/336 literature pairs confirm |
| QR integrity check on factor-tree data | **works** — 882 claims, caught both corrupt ones |
| NO2CYCLE applied to `q = 3` | **vacuous there** — classes disjoint mod 12 |
| any closure of `q = 3` | **not obtained** |

**The obstruction, precisely.** At `q = 5…17` two quantitative instruments did
the work: lower-prime avoidance (a divisibility constraint on every component)
and the abundancy floor `k₀(q)` (a lower bound on `ω(N)` that grew fast in `q`).
**Both are identically absent at `q = 3`** — the first vacuously, the second
because `3` alone supplies `~3/2` of the factor 2. What I have put in their
place are *qualitative* constraints on the production digraph (Lemmas QR,
3MOD12, NO2CYCLE) and one exact identity. They are genuine, but none of them is
yet **quantitative**: none bounds a count, so none can be fed into a counting
argument of the kind that closed the other branches.

Turning NO2CYCLE into a counting statement is the obvious next target. The
natural attempt — "if every producer of a prime `≡ 3 mod 4` also lies in that
class, then a set of size 2 needs a forbidden 2-cycle" — fails immediately,
because producers may lie outside the class, and the Euler prime can produce
any `p ≡ 3 (mod 4)` without constraint (`ord_p(π) | p−1` has `v₂ ≤ 1`
automatically when `p ≡ 3 mod 4`). I record that as tried and failed.
