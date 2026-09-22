# Audit: the model's `k = 2`, `3 ∤ N` closure

The reasoning model returned an argument closing the case I had claimed was out
of reach. **It survives audit.** Scripts in `k2/audit/`.

---

## 0. Verdict

| claim | verdict |
|---|---|
| Case (ii), one notable `≡ 2 (mod 3)` | **correct** — and **my own treatment was wrong** |
| Case (iii), both notables `≡ 2 (mod 3)` | **correct** — a case I had missed entirely |
| Case (i), both `≡ 1 (mod 3)`: the weighted fixed-support bound | **verified**, all 11 rows |
| Overall: no 2-restrained odd perfect number with `3 ∤ N` | **holds, as presented** |

## 1. My case (ii) was wrong — I double-counted the prime 5

I bounded case (ii) by `A₁ = (13/12)(7/6)(5/4)` taking `n₂ = 5`, while keeping
`A₂ = 1.320519`, which **contains the factor `5/4` from the ordinary prime
`s = 5`** (the class `σ(s²) = 31`). If `n₂ = 5` then 5 has exponent `≥ 4` and is
**not ordinary**. I counted the prime 5 twice — once as a notable component and
once as an ordinary one.

The model's repair is correct and neat:

- `n₂ ≠ 5` ⟹ `n₂ ≡ 5 (mod 6)` and `n₂ ≥ 11`, so the bound is
  `B₁ · 11/10 = 1.857529 < 2`.
- `n₂ = 5` ⟹ 5 is unavailable as an ordinary prime, so the class
  `σ(s²) = n₁` moves its minimum from 5 to 17 (since `F(11) = 133 = 7·19`),
  giving `B₁ · (17/16)/(5/4) · (5/4) = B₁ · 17/16 = 1.794204 < 2`.

## 2. Case (iii), which I had missed

If **both** notables are `≡ 2 (mod 3)`, neither ever divides any `σ(s²)`, so
every ordinary `σ(s²)` is supported on `p` alone. Bennett–Levin then forces
`σ(s²) = p`, so there is at most one ordinary prime and `ω(N) ≤ 4`,
contradicting `ω(N) ≥ 12`. Clean, and I did not have this case.

## 3. Case (i): the weighted fixed-support bound, verified

The device: fix the support `S = {r₁<r₂<r₃}`, set `x = r₁^{-1/2}` etc., and sum
`M^{-1/2}` over mixed monomials,
`H = (xy+xz+yz−2xyz)/((1−x)(1−y)(1−z))` — **formula re-derived and confirmed**.
Each class hosts at most one `s`, and `F(s) = M < (s+1)²` gives
`log(s/(s−1)) < 1/(s−1) < 1/(√M−2)`, so the mixed tail is at most
`(H−P)/(1−2xy)` where `P` sums the excluded monomials. `H−P` has nonnegative
coefficients, so replacing `x,y,z` by upper bounds is conservative — **correct,
and the point on which the whole method's validity turns.**

Checks performed:

| check | result |
|---|---|
| exclusion table `F(u) < M < F(u+1)` | **18/18 correct** |
| `X_r > r^{-1/2}` for all 7 values | **all valid** |
| per-row `R/d ≤ L` | **11/11** |
| per-row `A·B·E(L) < 2` | **11/11**, max **1.96031** (rows 3 and 4) |
| `E(t) ≥ eᵗ` via `n! ≥ 2·3^{n−2}` | **correct** |
| case division exhaustive | **365 support-triple × flag combinations, 0 failures** |
| row lower-triples are coordinatewise valid | **0 failures** |
| every monomial subtracted by `P` impossible | **yes**, sole exception `133 = F(11)` in row 1, which is explicitly paid for by `B = 11/10` — no double count |
| rows 4–6: third prime must be special | **correct** (`7, 19, 31 ≡ 7 mod 12`) |
| singleton floors 5 / 17 / 59 | **correct** (`F(11)=133`, `F(23)=553`, `F(47)=2257` all composite; `F(59)=3541` prime, `59 ≡ 11 mod 12`) |

My exact-rational recomputation gives slightly *better* products than the
model's rounded ceilings (1.95895 and 1.96031 against its 1.9738 and 1.9737),
consistent with its rounding being upward.

## 4. Why this does not contradict my `k = 2` refutation — and where my framing was wrong

My result was about Ochem–Zelinsky's method **as literally formulated**, which
takes, for each class, the minimum of `m` over **all admissible supports**. That
formulation does produce a number above 2 at `k = 2`; that part stands.

But I wrote it up as "`k = 2` fails", which was misleading. The model replaced
the method with a **fixed-support** bound — precisely the lossy step I had
identified in the brief — and that suffices. So:

- the literal method fails at `k = 2` ✓ (my result, unchanged);
- the case itself is closable ✗ (my implication, wrong);
- and case (ii) of my analysis contained a real double-counting error.

## 5. What was actually achieved, stated carefully

> **There is no 2-restrained odd perfect number `N` with `3 ∤ N`** — that is, no
> odd perfect number with `3 ∤ N` and exactly two even exponents exceeding 2.

This is the `k = 2` analogue of Ochem–Zelinsky's §2, and as far as I know it is
new; their paper treats `k = 1` only.

**It is one of three cases.** At `k = 1`, §2 (`3 ∤ N`) was the *easy* case: §3
(3 ordinary) and §4 (3 notable) are factor-tree arguments, and §4 needed a
three-week computation to reach `q ≥ 23×10⁹`. Both would have to be redone at
`k = 2`, with two notable components, and the tree must then branch on which
component is which. **That is where the difficulty lives, and it is untouched.**

**Audit standard.** I verified the arithmetic and the logical skeleton as
presented. That is not the same as refereeing it: a referee would want the
monomial enumerations re-derived independently for every row, the singleton-floor
case analysis re-done from scratch, and the `B` values justified for each
sub-case of rows 3, 7 and 8 where the identity of the special prime varies. I
spot-checked those by hand and found them sound, but I did not exhaust them.
