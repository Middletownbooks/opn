# Audit of the model's answer to `PROMPT_S4_K2_SPECIAL.md`

Script: `s4k2/03_audit_model.py`. Every inequality below was re-derived and
checked in exact rational arithmetic.

## Verdict

**The answer is sound.** It is a type (b) result — the leak is bounded, not
closed — and the bound is

    m  ≤  4 · 3^{r−3} · log₃(8(r−1)),        r = ω(N).

The model states plainly that this does not eliminate the sub-case, because `r`
is not bounded above. That is correct and correctly scoped.

It also **found two errors in my brief**, both of which I confirm (§5 below).

## The method

A Nielsen-style descent, and it is applied correctly. Build a partial
approximation `R = P/D` to `σ(N)/N` from: `3/2` at the 3-component, `1` at the
special, and for each remaining component either `1` or its exact factor. Every
numerator used (`3`, `s²+s+1`, `n₂`, `σ(n₂^{q₂})`) is odd, so `P` is odd; `D`
retains the `2` from `3/2`; hence `P ≠ 2D` and

    |2 − R| ≥ 1/D.

Large `m` makes the two replaced factors accurate — the total error they
contribute is `≤ 5/(4·3^m)` — so the gap must be carried by some *unexposed*
component, which bounds that component and lets it be exposed at controlled cost
to `D`. The descent terminates after at most `(r−3) + 2` exposures, and what is
left is the `3,p` error, giving `3^m ≤ HD`.

## Step-by-step check

| step | claim | verdict |
|---|---|---|
| A | `A_ℓ(a) = (ℓ/(ℓ−1))(1 − ℓ^{−(a+1)})` | OK |
| A | `1/(p−1) ≤ 1/(2(3^m−1)) ≤ 3/(4·3^m)` for `m ≥ 1`, using `p ≥ 2·3^m − 1` | OK |
| A | `3/2 − A_3(q) = 1/(2·3^q) ≤ 1/(2·3^m)`, using `q ≥ m` from the budget | OK, exact |
| A | combined error `≤ 5/(4·3^m)` | OK |
| B | `s²+s+1` odd; `σ(n^q)` odd for `q` **even**; so `P` odd | OK |
| B | `D` stays even — exposing `n₂`'s exponent divides `D` by the even `n₂−1`, but the initial `2` sits elsewhere in `D` | OK |
| C | only the 3-factor and the exposed-base `n₂` factor exceed their true values, each by `≤ 243/242` since the exponent is `≥ 4`; so every mixed product is `≤ 2(243/242)² < 3` | OK; `2·243² = 118098 < 175692 = 3·242²`, and `(3/2)/A_3(4) = 243/242` exactly, so the constant is attained, not slack |
| D | `A_s(2) − 1 = (s+1)/s² ≤ 1/(s−1)` | OK |
| D | `n₂/(n₂−1) − A_{n₂}(q₂) = 1/((n₂−1)n₂^{q₂})` | OK, exact |
| E | `H = 4(r−1) ≥ K+1 = 3(r−1)+1` and `(5/4)K ≤ H` | OK for `r ≥ 2` |
| E | ordinary exposure `E' ≤ E³`; `n₂` base and exponent `E' ≤ E²` | OK |
| E | exponent `3^{r−3}·2² = 4·3^{r−3}`, order-independent | OK |
| E | `E₀ = 2H = 8(r−1)` | OK |
| F | `r = 10 ⟹ m < 4·3⁷·4 = 34992` | OK (the sharper `4·3⁷·log₃72 = 34054` also holds) |

Two small points where the model was *less* sharp than it could have been, both
harmless: it used `log₃ 72 < 4` rather than `3.893`, and it quoted
`q ≤ 35013` where its own chain gives `q ≤ 34076`.

## The model's sharpening of my Proposition 1

Worth recording, because it improves on what I had. In this sub-case
`p ≡ 2 (mod 3)`, so `p` is *not* a prime `≡ 1 (mod 3)`. Hence the `i` primitive
divisors coming from `p` are ordinary or `n₂` (`i ≤ o₁ + δ`, `δ = [n₂ ≡ 1 mod 3]`),
and the `j` coming from `n₂` are ordinary — none is `n₂` itself, `3`, or `p`
(`j ≤ o₁`). With `q = o₁ + m + i + j`:

    q  ≤  m + 3o₁ + δ  ≤  m + 3r − 8.

My §3 bound `ω(N) ≥ 3 + (q−m−4)/3` rearranges to `q ≤ m + 3r − 5`. The model's
is **sharper by 3**, and cleaner: it drops my `o₁ ≥ max(i,j) − 2` in favour of
two separate bounds, which stay valid even when the two families of primitive
divisors overlap.

## What this is worth

The leak is no longer free: `q` is now bounded *above* in terms of `ω(N)`,

    q  ≤  4·3^{r−3} log₃(8(r−1)) + 3r − 8,

so `ω(N)` is bounded below in terms of `q`. The growth is brutal — roughly
`ω ≳ 3 + log₃(q/4)` — but it is unconditional and it covers the case my own
argument could not.

Concretely, **if** a `k = 2` analogue of Ochem–Zelinsky's `q ≥ 23 000 000 000`
were ever proved, this bound would force `ω(N) ≥ 23`:

| `ω(N)` | `q ≤` |
|---|---|
| 10 | `3.41 · 10⁴` |
| 15 | `9.13 · 10⁶` |
| 20 | `2.36 · 10⁹` |
| 22 | `2.17 · 10¹⁰` |
| 23 | `6.56 · 10¹⁰` — first value admitting `q = 2.3 · 10¹⁰` |

That is a genuine dividend: it converts the sieve half of their §4, which I
explicitly declined to ask for, into a lower bound on `ω(N)` far above the
current record of 10 — *if* that half is ever supplied at `k = 2`.

## 5. Two errors in my brief, confirmed

Both are in the "leads" section, and both are mine.

1. **Lead 1 was false.** I wrote that `p ≡ 5 (mod 12)` makes the odd part of
   `p−1` congruent to `1 (mod 3)`. Counterexample `p = 41`: `41 ≡ 5 (mod 12)`,
   `p − 1 = 40 = 8·5`, odd part `5 ≡ 2 (mod 3)`. My slip was reading
   `p − 1 = 4(3k+1)` and then attributing `≡ 1 (mod 3)` to the *odd part* rather
   than to `3k+1` itself. What survives is what the model states: `f | q₂+1` is
   odd and `3 ∤ p−1`, so `f` is odd and `3 ∤ f`.
2. **Lead 4 was false.** I suggested `p = 2·3^m − 1` gives `ord_p(3) | 2m`
   "-ish". Counterexample `p = 17`, `m = 2`: `ord₁₇(3) = 16`, while `2m = 4`.
   The relation `3^m ≡ 2^{−1} (mod p)` is correct but implies nothing about the
   order.

Neither error propagated into the model's argument — it flagged both and did not
use either.

## 6. What remains open

* The sub-case is **not** closed: `r` is unbounded, so the bound never bites.
* The model reports no bound from the order analysis in the hard branch
  `f > 1`, `p ∤ q₂+1`, where `e = v_p(n₂^f − 1)`. It does settle the easy
  branches: `f = 1` gives `e = v_p(q₂+1)` hence `p^e ≤ q₂+1`, and more generally
  `p | q₂+1` gives `m ≤ log₃((q₂+2)/2)`.
* No lower bound on `q` — as instructed.
