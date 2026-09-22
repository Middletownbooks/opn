# Research task: the special prime in the last open case of the 2-restrained odd perfect number problem

Self-contained brief for a reasoning model with no tools. You may write and
hand-execute short programs, but assume no internet, no libraries, and no
long-running computation.

**Ground rules.** Everything marked *verified* below has been checked
computationally and may be treated as given. Everything marked *proved* has a
proof sketched here that you should feel free to re-derive or challenge.
Everything else is open. Please do not assert a result you have not derived,
do not attribute a claim to the literature unless it is cited below, and if you
reach a partial result say exactly how partial it is. A clean negative answer —
"this cannot be closed this way, and here is the obstruction" — is a good
outcome.

You answered an earlier brief in this project (a fixed-support abundancy bound
for 2-restrained odd perfect numbers with `3 ∤ N`). This one is a different
setting; nothing from that brief is assumed here.

---

## 1. Setting

`N` is an **odd perfect number**: `N` odd with `σ(N) = 2N`. None is known; none
is known not to exist.

**Euler's form.** `N = p^e · m²` with `p` prime, `p ≡ e ≡ 1 (mod 4)`, `p ∤ m`.
Call `p` the **special prime** and `e` its exponent. Every other prime of `N`
has even exponent.

**Definition.** `N` is **`k`-restrained** if exactly `k` of its even exponents
exceed 2. Components with even exponent `≥ 4` are **notable**; a prime with
exponent exactly 2 is **ordinary**. `k = 1` is the case studied by Ochem and
Zelinsky (arXiv:2607.19746). This brief is about `k = 2`.

**Valuation balance.** For any prime `ℓ | N` with `ℓ^{e_ℓ} ‖ N`,
`e_ℓ = Σ_C v_ℓ(σ(C))`, the sum over all components `C` of `N` other than
`ℓ^{e_ℓ}` itself. (Immediate from `σ(N) = 2N` and multiplicativity, `ℓ` odd.)

**Known, cited.** `ω(N) ≥ 10` (Nielsen 2015), where `ω` counts distinct primes.

### Why this is the last case at `k = 2`

For a 2-restrained `N`, exactly one of these holds: `3 ∤ N`; `3` is ordinary
(`3² ‖ N`); `3` is notable (`3^q ‖ N`, `q` even `≥ 4`); `3` is special. The last
is impossible because `p ≡ 1 (mod 4)` while `3 ≡ 3 (mod 4)`. The first two have
been closed elsewhere in this project. So:

> **`3` is one of the two notable components: `3^q ‖ N` with `q` even, `q ≥ 4`.**

Notation used throughout:

| symbol | meaning |
|---|---|
| `3^q` | the notable component at 3; `q` even, `q ≥ 4` |
| `n₂^{q₂}` | the other notable; `q₂` even, `q₂ ≥ 4`, `n₂ ≠ 3` |
| `p^e` | the special component; `p ≡ e ≡ 1 (mod 4)` |
| `s²` | an ordinary component, exponent exactly 2 |
| `o₁` | the number of ordinary primes `s ≡ 1 (mod 3)` |

**Calibration.** At `k = 1` this case is **not closed** in the literature.
Ochem–Zelinsky's Theorem 1 says the notable component is `3^q` with
`q ≥ 23 000 000 000` — a reduction, not an elimination, obtained with large
sieve computations. Nothing below should be read as an attempt to close the
`k = 2` case outright, and you should not attempt it either.

---

## 2. The 3-budget (verified)

Applying the valuation balance at `ℓ = 3`: `q = Σ_{C ≠ 3^q} v₃(σ(C))`, with

| component | `v₃(σ(C))` |
|---|---|
| ordinary `s²` | `1` if `s ≡ 1 (mod 3)`, else `0` |
| notable `n₂^{q₂}`, `q₂` even | `v₃(q₂+1)` if `n₂ ≡ 1 (mod 3)`, else `0` |
| special `p^e`, `e` odd | `v₃(e+1)` if `p ≡ 1 (mod 3)`; `v₃(p+1) + v₃(e+1)` if `p ≡ 2 (mod 3)` |

*Verified*: 501 checks over `n ∈ {5,…,43}`, `q ∈ {4,…,58}` even and
`p ∈ {7,…,97}`, `e ∈ {1,5,…,57}`; 0 failures. The `p ≡ 2 (mod 3)` row is
lifting-the-exponent, using that `e+1` is even and `3 | p+1`.

Write `i = v₃(e+1)`, `j = v₃(q₂+1)·[n₂ ≡ 1 mod 3]`, `m = v₃(p+1)·[p ≡ 2 mod 3]`.
Then

    q  =  o₁ + m + i + j.

## 3. What that budget costs (proved, and verified on examples)

> **Proposition 1.** `v₃(σ(n^Q)) = j` forces at least `j` distinct prime
> divisors of `N`, all `≡ 1 (mod 3)`.

*Proof.* `3^j | Q+1`, so each `d = 3^k` (`k = 1..j`) divides `Q+1`. Zsigmondy
gives `n^d − 1` a primitive prime divisor `r_k`; no exception applies, since the
only exceptions for `a^n − 1` are `n = 2` with `a+1` a power of 2, and `n = 6`
with `a = 2`, while here `n = 3^k ≥ 3` and `a ≥ 5`. Then `r_k ≡ 1 (mod 3^k)`, so
`r_k` is odd and `≡ 1 (mod 3)`; `r_k ∤ n−1` by primitivity and
`r_k | n^d − 1 | n^{Q+1} − 1`, so `r_k | σ(n^Q)`. Primitivity makes the `r_k`
distinct, and each is odd and divides `2N`, hence divides `N`. ∎

The same applies to `p` with `i` in place of `j`. The only primes `≡ 1 (mod 3)`
dividing `N` that are *not* ordinary are `n₂` and `p` themselves, so the union of
the two families gives `o₁ ≥ max(i,j) − 2`, and with `q = o₁ + m + i + j`:

    ω(N)  ≥  3 + (q − m − 4)/3.

**So `i` and `j` are paid for, and `m` is not.** `m` is the only term that adds
to the 3-budget without buying prime divisors.

## 4. Why `m = 0` at `k = 1`, and why `k = 2` breaks that (proved + verified)

`m ≠ 0` requires `p ≡ 2 (mod 3)`, hence `p ≡ 5 (mod 12)` given `p ≡ 1 (mod 4)`.
Apply the valuation balance at `ℓ = p`: `e = Σ_{C ≠ p^e} v_p(σ(C))`. Which
components can contribute?

* **ordinary `s²`**: `σ(s²) = s²+s+1`, and every prime factor of `s²+s+1` is `3`
  or `≡ 1 (mod 3)` (if `r | s²+s+1` and `r ≠ 3` then `s` has order 3 mod `r`, so
  `3 | r−1`). `p ≡ 2 (mod 3)`, so **no**. *Verified* for all 783 primes `s < 6000`.
* **`σ(p^e)`**: `≡ 1 (mod p)`, so **no**.
* **`σ(3^q) = (3^{q+1}−1)/2`**: `q` is even, so `q+1` is odd. If `r | σ(3^q)`
  then `ord_r(3) | q+1` is odd, so `3` is a quadratic residue mod `r`, so by
  quadratic reciprocity `r ≡ ±1 (mod 12)`. `p ≡ 5 (mod 12)` is neither, so
  **no**. *Verified*: over `q = 4..118` even, the residues mod 12 occurring
  among prime factors of `σ(3^q)` are exactly `{1, 11}`.

At `k = 1` those are all the components, so `e = 0` — a contradiction. Hence
`p ≡ 1 (mod 3)` and `m = 0`. (This recovers Ochem–Zelinsky's Lemma 6.)

At `k = 2` there is one further component, `n₂^{q₂}`, under no such restriction.
Therefore:

> **The open sub-case.** `p ≡ 5 (mod 12)`, and `p^e ‖ σ(n₂^{q₂})` **exactly** —
> the second notable alone supplies every one of the `e` copies of `p`.

## 5. What the leak costs, so far as is known

Every prime factor of `p+1` divides `N`, since `p+1 | σ(p^e)` for odd `e`. And
`p ≡ 1 (mod 4)` forces `p+1 ≡ 2 (mod 4)`. So

    p + 1 = 2 · 3^m · w,    w odd, 3 ∤ w, every prime factor of w dividing N.

Taking `w = 1` gives `p = 2·3^m − 1`, which costs **nothing** in `ω(N)`. Such
primes exist — *verified* for `m ≤ 200`, they occur at
`m = 1, 2, 3, 7, 8, 12, 20, 23, 27, 35, 56, 62, 68, 131`
(`p = 5, 17, 53, 4373, 13121, 1062881, …`), all `≡ 5 (mod 12)` as they must be.
So the leak is a condition on the **shape** of `p`, not on `ω(N)`, and counting
alone will not close it.

---

## 6. The question

**Main.** In the sub-case of §4 — `p ≡ 5 (mod 12)` and `p^e ‖ σ(n₂^{q₂})` — is
the leak really free? Concretely, either

  **(a)** derive a contradiction, closing the sub-case; or
  **(b)** prove a bound that makes `m` expensive, e.g. `m ≤ f(ω(N))` or
  `m ≤ f(q₂)` or `m ≤ f(e)` for an explicit `f`, so that
  `ω(N) ≥ 3 + (q − m − 4)/3` becomes useful again; or
  **(c)** show that no such bound can follow from this structure, and identify
  precisely what extra input would be needed.

Any of the three is a real answer. (c) is genuinely useful — the point of the
exercise is to find out whether this door can be shut.

### Leads I have not pursued

These are starting points, not results. Check them before relying on them.

1. **Order analysis of `p^e ‖ σ(n₂^{q₂})`.** Write `f = ord_p(n₂)`. Since
   `σ(n₂^{q₂}) = (n₂^{q₂+1} − 1)/(n₂ − 1)` and `p | σ`, we have `f | q₂+1`, which
   is **odd**, so `f` is odd; and `f | p−1`. With `p ≡ 5 (mod 12)`,
   `p − 1 ≡ 4 (mod 12)`, so the odd part of `p−1` is `≡ 1 (mod 3)`. If `f > 1`
   then `v_p(n₂−1) = 0` and lifting-the-exponent gives
   `e = v_p(n₂^f − 1) + v_p((q₂+1)/f)`. So a large `e` forces either
   `n₂^f > p^e` (so `n₂` or `q₂` enormous) or `p^{e−v} | q₂+1` (so `q₂`
   enormous). Does a large `q₂` then cost prime divisors, via the divisor
   structure of `q₂+1` and Proposition 1's argument applied to divisors other
   than powers of 3?
2. **`e = 1` is the cheap case** and is allowed (`1 ≡ 1 mod 4`). Then `i = 0`,
   `σ(p) = p+1 = 2·3^m·w`, and `q = o₁ + m + j`. Is `e = 1` separately
   constrained here? Note `p ‖ N` then.
3. **Ordinary primes `≡ 5 (mod 12)`.** The §4 argument applies verbatim to any
   ordinary `s ≡ 5 (mod 12)`: such an `s` cannot be produced by ordinary
   components or by `σ(3^q)`, so `s² | σ(p^e) · σ(n₂^{q₂})`. Since
   `σ(p^e)`'s odd part is `3^m · w · (…)`, this couples the ordinary primes
   `≡ 5 (mod 12)` to `w` and to `n₂`. Is there a counting contradiction here —
   many such `s`, only two producers?
4. **`p = 2·3^m − 1` with `m` large.** Then `3^m ≡ 2^{-1} (mod p)`, so
   `ord_p(3) | 2m`-ish; does that interact usefully with `3^q ‖ N` and with
   `q ≥ m` (which follows from `q = o₁ + m + i + j`)?

### What is *not* wanted

* Any attempt at a lower bound on `q`. That is the sieve half of
  Ochem–Zelinsky's §4 and is out of reach without heavy computation.
* Any assumption that `k = 1` results transfer. §4 above is precisely a case
  where one does not.
* Numerical searches you cannot carry out reliably by hand. Small hand-checks
  to test a claim are welcome and encouraged; large ones are not.
