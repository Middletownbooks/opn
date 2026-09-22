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
