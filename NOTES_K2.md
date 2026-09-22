# k = 2 — does the ladder's next rung exist?

Working notes. Scripts in `k2/`. Follows `NOTES_RESTRAINED.md` and `NOTES_Q3.md`.

**Setting.** `N` odd perfect, `N = p^e m²`, `p ≡ e ≡ 1 (mod 4)` special.
McDaniel: at least one even exponent exceeds 2. Call `N` **`k`-restrained** when
exactly `k` do; `k = 1` is Ochem–Zelinsky's *restrained*. For `k = 2` write the
notable components `n₁^{q₁}, n₂^{q₂}` with `q_i ≥ 4` even; *ordinary* = exponent 2.

Motivation: since restrained ⟹ `3 | N` ⟹ `q = 3`, the `k`-restrained ladder is
non-vacuous exactly at `q = 3`, so `k = 2` is the natural continuation of their
programme. This checkpoint asks whether their **§2 argument** (the case
`3 ∤ N`) still closes at `k = 2`.

## 1. The argument transfers structurally

Their §2 for `k = 1` goes through verbatim with **pairs replaced by triples**:

- every ordinary `s` is `≡ 2 (mod 3)` (else `3 | σ(s²)` and `3 | N`), and being
  odd, `s ≡ 5 (mod 6)`;
- every prime factor of `s²+s+1` other than 3 is `≡ 1 (mod 3)`, hence not
  ordinary, hence lies in `{p, n₁, n₂}`. So every ordinary `s` is *regular*:
  **`σ(s²) = p^a n₁^b n₂^c`**;
- each triple `(a,b,c)` determines at most one ordinary `s`, since `s²+s+1`
  determines `s`.

So the question is purely quantitative.

## 2. Three things get worse, and they are enough

| | `k = 1` | `k = 2` |
|---|---|---|
| classes of total degree `k` | `k − 1` (**linear**) | `(k+1)(k+2)/2 − 3` (**quadratic**) |
| `A₁` covers | special + 1 notable | special + 2 notables |
| size floor `B` | 7 | 7, or **5** if a notable is `≡ 2 (mod 3)` |
| `A_∞` | **1.011787** | **1.0645** (B=7) / **1.2695** (B=5) |

(`A_∞` computed with the all-even classes removed as well as the pure powers —
the count most favourable to the method. The cruder count gives 1.0713/1.3045.)

## 3. Case (ii): a notable `≡ 2 (mod 3)` — fails outright

Such a notable is `≡ 5 (mod 6)`, so it can be 5, and every factor of `σ(s²)` is
then only guaranteed `≥ 5`. With `p = 13, n₁ = 7, n₂ = 5`:

> `A₁ · A_∞ = 1.579861 × 1.269494 = ` **`2.0056 > 2`**

and that is **before a single ordinary prime is counted**. Since the ordinary
contribution is `≥ 1`, the bound can never fall below 2. **The method cannot
close case (ii).**

## 4. Case (i): both notables `≡ 1 (mod 3)` — fails once two new classes are named

*First pass was too hasty.* With the crude class count I got 2.0053 > 2 and
concluded failure; with the refined count (fair to the method) it is
**1.9926 < 2** — not settled. Two identifiable new classes settle it.

The 11 tabulated `k = 1` classes all have `c = 0`, so they carry over unchanged
and contribute `A₂ = 1.320519`. Two new classes can be pinned exactly:

- **`σ(s²)` a single notable prime.** Both `(0,1,0)` and `(0,0,1)` need
  `s²+s+1` prime and `≡ 1 (mod 6)`. The smallest such ordinary `s` are
  `5, 17, 41, …`. `A₂` already contains `5/4`; the second class forces a
  further **`17/16`**.
- **`σ(s²) = n₁ n₂`, two distinct primes `≡ 1 (mod 6)`.** Smallest is
  `s = 11`: `11²+11+1 = 133 = 7 · 19`. **Genuinely new** — neither 7 nor 19 is
  `≡ 1 (mod 12)`, so this cannot be the `k = 1` class `(1,1)` (whose smallest
  is 29). Forces **`11/10`**.

| factor | value | running |
|---|---|---|
| `A₁` (`p=13, n₁=7, n₂=19`) | 1.334105 | 1.334105 |
| `A₂` (11 carried-over classes) | 1.320519 | 1.761711 |
| class `(0,0,1)`, `s = 17` | 1.062500 | 1.871818 |
| class `(0,1,1)`, `s = 11` | 1.100000 | 2.059000 |
| `A_∞` (B=7, all-even removed) | 1.064538 | **2.191885** |

> **2.1919 > 2**, using only 2 of the 56 new low classes. The true figure is larger.

## 5. Verdict

> **The §2 abundancy method does not reach `k = 2`.** It fails in case (ii)
> before any ordinary prime is counted, and in case (i) once two identifiable
> new classes are added.

The reason is structural, not a numerical accident: the class count per degree
goes from linear to quadratic, `A₁` must cover a third component, and a notable
`≡ 2 (mod 3)` drops the floor from 7 to 5. At `k = 1` the final figure was
1.6887, which looks comfortable; the margin is consumed entirely at the very
next rung.

**This is a limit on the method, not on the conjecture.** `k = 2` may well be
closable — but not by this argument, and not by tuning its constants.

## 6. What this does to the roadmap

I previously called `k = 2` "the live continuation" of their programme. That
needs tempering: it remains the best-defined target at `q = 3`, but **the
natural method for it does not work**, so it is not the cheap next step I
implied.

Note also that §3 and §4 (the cases `3` ordinary and `3` notable) would need
redoing too, and those are factor-tree arguments that get materially harder
with two notable components — the tree must branch on which component is which.

What would be needed for a `k = 2` §2: either a much better lower bound on the
smallest solutions `m(a,b,c)` for the new triple classes (their `pairs.py`
generalised to triples, which is a real computation), or an extra structural
constraint cutting the class count back toward linear growth. The second is the
interesting one, and I do not have it.
