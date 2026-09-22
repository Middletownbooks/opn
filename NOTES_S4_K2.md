# Section 4 at `k = 2`: 3 notable — the budget-and-Zsigmondy costing

Scripts in `s4k2/`, standard library only.

**Why this is the remaining case.** `N` is a 2-restrained odd perfect number.
`3 ∤ N` is closed at `k = 2`; `3` ordinary is closed (`NOTES_S3_K2.md`); and `3`
cannot be special, since `p ≡ 1 (mod 4)` while `3 ≡ 3 (mod 4)`. So **`3` is one
of the two notable components**: `3^q ‖ N` with `q` even, `q ≥ 4`. Write the
other notable `n₂^{q₂}`, the special `p^e`, and `o₁ = #{ordinary s : s ≡ 1 mod 3}`.

**What `k = 1` achieves here, for calibration.** Ochem–Zelinsky's Theorem 1 is
`n = 3` **and** `q ≥ 23 000 000 000` — a reduction, not an elimination. Their §4
does not close this case, so nothing below should be read as attempting to.

---

## 1. The budget identity and what changes at `k = 2`

`q = e₃ = Σ_{C ≠ 3^q} v₃(σ(C))`, and (verified, 501 checks, 0 failures):

| component | `v₃(σ(C))` |
|---|---|
| ordinary `s²` | `1` if `s ≡ 1 (mod 3)`, else `0` |
| notable `n₂^{q₂}`, `q₂` even | `v₃(q₂+1)` if `n₂ ≡ 1 (mod 3)`, else `0` |
| special `p^e`, `e ≡ 1 (mod 4)` | `v₃(e+1)` if `p ≡ 1 (mod 3)`; `v₃(p+1) + v₃(e+1)` if `p ≡ 2 (mod 3)` |

Writing `i = v₃(e+1)`, `j = v₃(q₂+1)·[n₂ ≡ 1 mod 3]`, `m = v₃(p+1)·[p ≡ 2 mod 3]`:

    k = 1 :   q = o₁ + m + i
    k = 2 :   q = o₁ + m + i + j

The term `j` is the whole formal difference. If it were free, `q` could be large
with `o₁` and `ω(N)` small, and the `k = 1` chain would break.

## 2. `j` is not free  (`s4k2/01`)

> **Proposition.** `v₃(σ(n^Q)) = j` forces at least `j` distinct prime divisors
> of `N`, all `≡ 1 (mod 3)`.

*Proof.* `3^j | Q+1`, so each `d = 3^k` (`k = 1..j`) divides `Q+1`. By Zsigmondy
`n^d − 1` has a primitive prime divisor `r_k` — no exception applies, since the
only exceptions for `a^n − 1` are `n = 2` with `a+1` a power of 2 and `n = 6`
with `a = 2`, while here `n = 3^k ≥ 3` and `a ≥ 5`. Then `r_k ≡ 1 (mod 3^k)`, so
`r_k` is odd and `≡ 1 (mod 3)`; `r_k ∤ n−1` by primitivity, and
`r_k | n^d − 1 | n^{Q+1} − 1`, so `r_k | σ(n^Q)`. Primitivity makes the `r_k`
pairwise distinct, and each divides `σ(N) = 2N` and is odd, hence divides `N`. ∎

Verified on explicit numbers: 24 cases in step 1 (existence, `≡ 1 mod 3^k`,
oddness) and 18 in step 2 (divisibility of `σ(n^Q)`, distinctness), 0 failures.
The same argument applies to `p` with `i` in place of `j`.

## 3. The counting bound

The primes `r_k(p)` (`k ≤ i`) and `r_k(n₂)` (`k ≤ j`) are all `≡ 1 (mod 3)` and
divide `N`. The only primes `≡ 1 (mod 3)` dividing `N` that are **not** ordinary
are `n₂` and `p` themselves — `3 ≡ 0 (mod 3)`, and there are no other
non-ordinary components. The union of the two families has at least `max(i,j)`
elements, so

    o₁ ≥ max(i, j) − 2 ≥ (i+j)/2 − 2.

With `S = i+j` and `q − m − S = o₁`, this gives `S ≤ (2(q−m)+4)/3` and hence

> **`ω(N) ≥ 3 + (q − m − 4)/3`,  where `m = v₃(p+1)` if `p ≡ 2 (mod 3)`, else 0.**

At `k = 1` the `n₂` family is absent (`j = 0`) and at most one non-ordinary prime
can occur, giving `ω(N) ≥ 2 + (q − m − 1)/2`.

**So the answer to the question that prompted this is: the second notable does
not give a free escape.** Every unit it puts into the 3-budget buys a distinct
prime divisor of `N`. The `k = 1` chain survives, with `1/3` in place of `1/2`.

## 4. The leak is `m`, and the second notable *does* open it  (`s4k2/02`)

`m = v₃(p+1)` is unpaid — it costs no prime divisors. It is non-zero only when
`p ≡ 2 (mod 3)`, i.e. `p ≡ 5 (mod 12)`. At `k = 1` that case cannot occur, and
the mechanism is worth stating because it is exactly what `k = 2` undoes. Ask
what can produce `p`, i.e. contribute to `e_p = Σ_{C ≠ p^e} v_p(σ(C))`:

* an **ordinary** `s²` has `σ(s²) = s²+s+1`, whose prime factors are `3` or
  `≡ 1 (mod 3)` (verified for all 783 primes `s < 6000`). `p ≡ 2 (mod 3)`, so no.
* `σ(p^e) ≡ 1 (mod p)`, so no.
* `σ(3^q) = (3^{q+1}−1)/2` with `q` **even**, so `q+1` is odd. If `r | σ(3^q)`
  then `ord_r(3) | q+1` is odd, so `3` is a quadratic residue mod `r`, and by
  quadratic reciprocity `r ≡ ±1 (mod 12)`. `p ≡ 5 (mod 12)` is neither, so no.
  (Verified: over `q = 4..118` even, the residues mod 12 actually occurring among
  the prime factors of `σ(3^q)` are exactly `{1, 11}`.)

At `k = 1` that exhausts the components, so `e_p = 0` — a contradiction, hence
`p ≡ 1 (mod 3)`. This is Ochem–Zelinsky's Lemma 6, recovered.

At `k = 2` there is one more component and it is under no such restriction:

> **`p ≡ 5 (mod 12)` survives at `k = 2`, and then `p^e ‖ σ(n₂^{q₂})` exactly —
> the second notable alone must supply every one of the `e` copies of `p`.**

So the door the second notable opens is *not* the one the budget identity
suggested. The new term `v₃(q₂+1)` is fully paid for; what the second notable
actually does is remove the obstruction that forced `p ≡ 1 (mod 3)`.

### 4a. How costly is the leak?

Every prime factor of `p+1` divides `N` (as `p+1 | σ(p^e)` for odd `e`), and
`p ≡ 1 (mod 4)` forces `p+1 ≡ 2 (mod 4)`, so

    p + 1 = 2 · 3^m · w,   w odd, 3 ∤ w, every prime factor of w dividing N.

Taking `w = 1` gives `p = 2·3^m − 1`, which costs **nothing** in `ω(N)`. Such
primes exist: `m = 1, 2, 3, 7, 8, 12, 20, 23, 27, 35, 56, 62, 68, 131` below 200
(`p = 5, 17, 53, 4373, 13121, 1062881, …`), all `≡ 5 (mod 12)` as they must be.
So the leak is a condition on the **shape** of `p`, not on `ω(N)`, and it cannot
be closed by counting.

## 5. Status

* **Established, unconditionally:** the costing (§2), the bound
  `ω(N) ≥ 3 + (q − m − 4)/3` (§3), and the `k = 1`/`k = 2` dichotomy for the
  special prime (§4), including a proof of Ochem–Zelinsky's Lemma 6 from
  quadratic reciprocity.
* **Not established:** any lower bound on `q` itself. That is the computational
  half of their §4 (sieves past `6·10⁶`, `loopless.cpp`), and nothing here
  touches it. Without it the bound in §3 is conditional on `q` being large.
* **The open sub-case:** `p ≡ 5 (mod 12)` with `p^e ‖ σ(n₂^{q₂})`. This is
  genuinely new at `k = 2` and is where a brief to a reasoning model would now
  be worth writing — it is a finite, fully-specified structural question, unlike
  "close 3 notable at `k = 2`", which is strictly harder than the open `k = 1`
  case.
