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

## 3. Case (ii): a notable `≡ 2 (mod 3)` — fails, and the reason is simpler than I first said

**Correction to my first pass.** I treated case (ii) with *triple* classes and a
floor `B = 5`. That was wrong-headed. If `n₂ ≡ 2 (mod 3)` then `n₂` can **never**
divide any `σ(s²)`, since every prime factor of `s²+s+1` other than 3 is
`≡ 1 (mod 3)`. So `c = 0` for every ordinary prime: **the class structure
collapses back to the `k = 1` pairs**, and the floor stays at 7 because only `p`
and `n₁` ever appear. `A₂` and `A_∞` are unchanged from `k = 1`; only `A₁` grows,
since it must cover a third non-ordinary component and `n₂ ≡ 5 (mod 6)` can be 5.

| factor | value |
|---|---|
| `A₁` (`p=13, n₁=7, n₂=5`) | 1.579861 |
| `A₂` (k=1 classes, unchanged) | 1.320519 |
| `A_∞` (k=1 tail, unchanged) | 1.011787 |
| **bound** | **2.110829 > 2** |

Same verdict as before, now with `k = 1` data only and no guesswork.

## 4. Case (i): both notables `≡ 1 (mod 3)` — fails with **no tail at all**

The 11 tabulated `k = 1` classes have `c = 0`, so they carry over and give
`A₂ = 1.320519`. Two new classes have *exactly known* minima:

- **`σ(s²)` a single notable prime.** Both `(0,1,0)` and `(0,0,1)` need `s²+s+1`
  prime and `≡ 1 (mod 6)`; the two smallest ordinary `s` are `5` and `17`. `A₂`
  already holds the `5/4`, so the second forces **`17/16`**.
- **`σ(s²) = n₁n₂`,** two distinct primes `≡ 1 (mod 6)`. Smallest is `s = 11`:
  `133 = 7·19`. Genuinely new — neither factor is `≡ 1 (mod 12)`, so it cannot
  be the `k=1` class `(1,1)` (smallest 29). Forces **`11/10`**.

| factor | running |
|---|---|
| `A₁` (`p=13, n₁=7, n₂=19`) | 1.334105 |
| `A₂` | 1.761711 |
| `(0,0,1)`, `s=17` | 1.871818 |
| `(0,1,1)`, `s=11` | **2.059000** |

> **2.0590 > 2 with `A_∞` set to 1** — the entire tail discarded.

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

## 5b. Better data on the class minima cannot rescue the method

The bound is a product over classes of `m/(m−1)`, so better data can only *raise*
some `m` and *lower* that factor. But every ingredient above is already exact or
discarded in the method's favour:

- the 11 `k = 1` minima are exact;
- `m = 17` is exact (5 and 17 are provably the two smallest ordinary `s` with
  `s²+s+1` prime and `≡ 1 mod 6`);
- `m = 11` is exact (`133 = 7·19`, and no smaller ordinary `s` works);
- `A_∞` is set to **1** in case (i), and to its `k = 1` value in case (ii).

**So computing better lower bounds on the triple-class minima is pointless for
rescuing this method.** The failure is driven by exactly-known small solutions,
not by pessimistic estimates. Margins over 2: case (i) 0.0590, case (ii) 0.1108.

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
