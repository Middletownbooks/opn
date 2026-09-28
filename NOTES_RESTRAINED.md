# Building on Ochem–Zelinsky, inside their restrained framework

Working notes. Target: Ochem & Zelinsky, *On odd perfect numbers with exactly
one even exponent greater than 2*, arXiv:2607.19746v1 (22 Jul 2026). Scripts in
`restrained/`, standard library only.

Setting throughout: `N` is a **restrained** odd perfect number — every even
exponent is 2 except one. `p` is the special prime with exponent `e ≡ 1 mod 4`;
the **notable** component is `n^q` with `q ≥ 4` even; all other primes are
**ordinary**, with exponent exactly 2. Their Theorem 1: `n = 3` and
`q ≥ 23,000,000,000`. Following their §4, write `O₁`, `O₂` for the ordinary
primes `≡ 1` and `≡ 2 (mod 3)`, and `o₁, o₂` for their sizes.

---

## 1. Verification of the paper

| item | result |
|---|---|
| §2 `A₁, A₂, A₃, A_∞` and product | reproduced to full printed precision; `1.68866287554177807591 < 2` |
| §2 Table 1, all 7 entries with `s < 200000` | reproduced exactly, including `p` and `n` |
| §3 "ruling out 127" | `1.9592144484846309` — **exact match** |
| §3 "ruling out 331" | `1.6675275884645718` vs `…719` — match to 15 digits |
| §3 "ruling out 19" | `1.9444209560681035` vs `…04` — match |
| §3 "ruling out 31" | `1.6927270960973606` vs `…065` — match |
| §3 "final argument" | `1.9497723588476532` — **exact match** |

Three of the §3 bounds sit within 3% of 2, so they are load-bearing; all five
reproduce. **§2 and §3 verify cleanly.**

**One discrepancy, in §4.** The final product is stated as
`1.99209763359616948564`. Recomputing from the transcribed inputs
(`z = 216171986291`, `K = 43,500,000,000`, `p > 6,000,000`) gives

- `1.97533818169217888060` using `1.076855990994` (the constant inside the
  stated product), or
- `1.99671063469240028723` using `1.088507187872` (the abundancy the text says
  the sieve reached).

Neither reproduces the stated value. The text quotes two different constants,
which points to OCR damage in the transcription I was given rather than an
error in the paper — I cannot distinguish without the PDF. **The argument is
unaffected either way: every candidate reading is `< 2`, which is all §4
needs.** The conclusion `q ≥ 23×10⁹` does not depend on the reading.

### 1a. Resolved against the full transcript (`restrained/10`)

The user supplied the full paper text (`sources/ochem_zelinsky_2607.19746_transcript.txt`).
It is not OCR damage: the paper itself prints the two constants. It says the sieve
ran "for 3 weeks until it said to need more than 2,500,000,000 ordinary primes up
to z = 216,171,986,291 only to reach abundancy 1.088507187872". Then it writes the
final product with `1.076855990994` and `K = 43,500,000,000`.

* **The printed product `1.99209763359616948564` is reproduced to 10 significant
  digits by `A = 1.088507187872` (the sieve's value) with `K = 43,000,000,000`**:
  `1.99209763353720…`, a difference of `−5.9·10⁻¹¹`. The implied `A` at
  `K = 43·10⁹` is `1.0885071879042`, which differs from the printed `A` in its 11th
  decimal. That fits a value read from a slightly later progress line; it is a
  guess, not verified.
* With the text's `K = 43.5·10⁹` and the sieve's `A`, the product is
  `1.99671063469… < 2`. **So the conclusion follows from the sieve's reported
  output as stated.** `A` could be up to `1.090300386` (a 0.165% headroom) before
  `K = 43.5·10⁹` fails.
* `1.076855990994` reproduces nothing tried. Its source is unknown, and it is not
  load-bearing.
* **The rigorous form.** Ordinary primes `m ≥ k + K_max + 1`. With the printed `A`
  rounded up, `K_max = 43,855,827,007`, so `k + K_max = 46,355,827,007`, a margin
  of `3.56·10⁸` over the `46·10⁹` needed. Lemma 8 then gives `q ≥ 23·10⁹` (`q` is
  even, and `ω/2 − 2 ≥ 22,999,999,999.5`).
* **What a re-run must show.** `k(z) + K_max(A(z)) ≥ 46·10⁹` for the exact sieve.
  The argument needs only that the survivor set contains every possible ordinary
  prime in `(3·10⁶, z)`, so an over-inclusive sieve is still sound. Each survivor
  `r` changes `k + K_max` by `1 − z·ln(r/(r−1)) ≤ 0`, so extra survivors only cost
  margin.

**Status: the §4 arithmetic discrepancy is resolved.** What remains is whether the
sieve output is correct (§4b).

---

## 2. Lemma A — the notable component can only produce primes `≡ ±1 (mod 12)`

> **Lemma A.** Every prime `r > 3` dividing `σ(3^q)` satisfies
> `r ≡ ±1 (mod 12)`.

*Proof.* `r | σ(3^q) = (3^{q+1}−1)/2` gives `ord_r(3) | q+1`, which is odd
since `q` is even; so `ord_r(3)` is odd. Writing `r−1 = 2^a m` with `m` odd and
`a ≥ 1`, we get `ord_r(3) | m | (r−1)/2`, so `3^{(r−1)/2} ≡ 1 (mod r)` and 3 is
a quadratic residue mod `r`. By quadratic reciprocity `(3/r) = 1` exactly when
`r ≡ ±1 (mod 12)`. ∎

**Attribution.** The first half is their own Lemma 4 read contrapositively
(`r | σ(n^q)` with `q` even `⟹ ord_r(n)` odd). The new part is only the
quadratic-reciprocity step and the resulting congruence. **This is a
consequence of their lemma that they do not draw, not a new lemma.**

Verified (`restrained/01`) by factoring `σ(3^q)` for every even `q` from 4 to
32 — all prime factors `≡ ±1 (mod 12)` in every case. The control confirms
evenness of `q` is essential: for `q = 3, 5, 7` the factors 5, 7, 41 appear.

> **Corollary B.** Every ordinary prime `s ≡ 5 (mod 12)` satisfies
> `v_s(σ(p^e)) = 2` — the special component alone must produce both its copies.

*Proof.* Every prime factor of `t²+t+1` is 3 or `≡ 1 (mod 3)`, so a prime
`≡ 2 (mod 3)` can never be produced by an ordinary component (they use exactly
this step in §3 for 107). `s ≡ 5 mod 12` gives `s ≡ 2 mod 3`, and `5 ≢ ±1 mod 12`
so Lemma A rules out the notable component too. Only the special component
remains, and `s` ordinary needs `e_s = 2` copies. ∎

So if 5 is ordinary then `25 | σ(p^e)`; likewise for 17, 29, 41, 53, 89, 101, …

---

## 3. An exact form of their Lemma 8, and why that route is closed

Their Lemma 8 runs `q ≥ o₁ ≥ ω(N)/2 − 2`. The first inequality is in fact an
equality:

> **Proposition.** `q = o₁ + v₃(e+1)`.

*Proof.* `q = e₃ = Σ_C v₃(σ(C))` over components `C ≠ 3^q`. For ordinary `s`,
`v₃(s²+s+1) = 1` if `s ≡ 1 mod 3` (write `s = 1+3k`: `s²+s+1 = 3(1+3k+3k²)`
with cofactor `≡ 1 mod 3`) and `0` otherwise. For the special component,
`p ≡ 1 mod 3` by their Lemma 6, so LTE gives
`v₃(σ(p^e)) = v₃(p^{e+1}−1) − v₃(p−1) = v₃(e+1)`. ∎

**This tells us where improvement is not available.** `q ≥ o₁` is tight
(equality whenever `3 ∤ e+1`), so no sharpening of Lemma 8 can come from that
step. The only slack in the chain is `o₂ ≤ o₁ + 2`, or the bound on `ω(N)`
itself — which matches their own remark that better sieve arguments are what is
needed.

**An attempt that failed, recorded so it is not repeated.** I tried to tighten
`o₂ ≤ o₁ + 2` using Lemma A. Their count is: `o₁ + o₂ − 2` incidences
(each ordinary prime forces some `r ∈ O₁` dividing `σ(s²)`, bar ≤2 exceptions)
against capacity `2o₁` (each `r ∈ O₁` has `e_r = 2`). The refined version is
`o₂ ≤ o₁ + 2 − C` where `C` counts copies of `O₁` primes produced by the
special and notable components. **`C` cannot be bounded below**, because `e`
and `q` are unbounded and so both big components have unbounded production
capacity. The same obstruction blocks every variant I tried, including counting
`O₂` production (`2o₂ ≤ q + e + o₂ − 1`, vacuous for `q ~ 2×10¹⁰`).

---

## 4. Their Question 10 — a narrowing and a search bound

They ask: are there primes `x, y, p, r` and integers `a > b > 0` with
`x²+x+1 = p^a r` and `y²+y+1 = p^b r`? — and say a negative answer "would
substantially tighten Lemma 8". So it is the lever they name.

> **Proposition.** Any solution has `p ≡ 1 (mod 3)` and `p ≥ 7`. In particular
> **`p = 3` is impossible.**

*Proof.* `v₃(t²+t+1) ≤ 1` for every integer `t` (computed above). A solution
needs `a > b > 0`, so `a ≥ 2` and `v_p(x²+x+1) ≥ 2`, which `p = 3` cannot
meet. Every prime factor of `t²+t+1` is 3 or `≡ 1 mod 3`, so `p ≡ 1 mod 3`. ∎

**Consequence for searching.** A solution needs `p² | x²+x+1` with
`p ≡ 1 mod 3`. For such `p` the congruence `t²+t+1 ≡ 0 (mod p²)` has exactly
two roots (Hensel lifts; `2t+1` is invertible mod `p` as `p ≠ 3`), so `x` lies
in just 2 residue classes mod `p²`.

**Search bound.** Dividing the two equations gives
`x²+x+1 = p^{a−b}(y²+y+1)`, so a solution is a *collision* in the map
`x ↦ (p, r)` over primes `x` whose `x²+x+1` has exactly two distinct prime
factors with `r` to the first power. (Two distinct `x` sharing `(p,r)`
automatically have `a ≠ b`, since equal exponents force `x = y`.)

| bound on `x` | primes examined | of shape `p^a·r` | collisions |
|---|---|---|---|
| 200,000 | 17,982 | 9,062 | **0** |
| 1,000,000 | 78,496 | 35,658 | **0** |

**This is data on an open question, not a theorem.** A null search establishes
no impossibility. It is recorded only because Question 10 currently has no
published computational bound, and because both of their near-examples have
composite `x` (`30²+30+1 = 7²·19` against `11²+11+1 = 7·19`, and
`9353²+9353+1 = 409²·523` against `462²+462+1 = 409·523`).

---

### 4a. Question 10 settled exactly for all `p, r < 1000`  (`restrained/09`)

The search above covers every `(p, r)` but only `x ≤ 10⁶`. The other axis is
now closed exactly. Fix `(p, r)`. Then `x² + x + 1 = r·pᶜ` has **one** free
exponent, so the Skolem solver of `s3k2/32` (`NOTES_S3_K2.md` §14b) lists **all**
its solutions, for every `c` and with no bound on `x`.

The case `r = p` is solved as `x² + x + 1 = p^{c+1}`. `r` runs over 3 and the
primes `≡ 1 (mod 3)`, which are the only possible prime factors of `t²+t+1`.

**Validation.** Both of Ochem–Zelinsky's near-examples are reproduced:

* `(7, 19)`: `30²+30+1 = 7²·19` and `11²+11+1 = 7·19`;
* `(409, 523)`: `9353²+9353+1 = 409²·523` and `462²+462+1 = 409·523`.

**Result** (`python3 restrained/09_question10_exact.py 1000`, 68 min). Every one
of the 6480 pairs is settled; none is left unsettled.

| `p, r < 1000` | count |
|---|---|
| pairs settled exactly | 6480 of 6480 |
| pairs admitting `x²+x+1 = r·p^a`, `y²+y+1 = r·p^b`, `a > b ≥ 1`, any `x, y ≥ 2` | **2**: exactly the two near-examples |
| of those, with `x` and `y` both prime (a Question-10 solution) | **0** |

> **Proposition (computational, exact).** Question 10 has no solution with
> `p < 1000` and `r < 1000`, for any `a > b > 0` and any `x, y`. Moreover, the
> only pairs in that range admitting the two equations at all, even with `x, y`
> composite, are Ochem–Zelinsky's two near-examples.

This is still data on an open question, not a resolution of it: `p` and `r` are
unbounded. It is exact within its range, where the earlier table was a
bounded search.

**A lead, not pursued.** Both near-examples satisfy `x ≡ y (mod r)` and
`x ≡ −1−y (mod p^b)`. With `y′ = −1−y`, that orientation makes
`((xy′ + x + 1) + (x − y′)ω)/p^b` an Eisenstein integer of norm `p^{a−b} r²`.
Checked on `(30, 11)`: `47² + 47·6 + 36 = 7·19²`. I see no route from this to
finiteness.

## 4b. Audit of `loopless.cpp` — a 64-bit overflow

`loopless.cpp` implements Algorithm 1, the sieve that yields
`ω(N) > 46×10⁹` and hence, via Lemma 8, `q ≥ 23×10⁹`. It is the load-bearing
computation of the paper.

Its central test is

```cpp
bool check_M2(u64 r, const PrimeSet& M2) {
    u64 val = r * r + r + 1;          // <-- 64-bit arithmetic
    if (val % 3 == 0) val /= 3;
    std::vector<u64> factors;
    get_factors(val, factors);
    for (u64 p : factors) if (M2.count(p)) return false;
    return true;
}
```

`r` and `val` are `u64`. The file defines `u128` and uses it inside
`power_mod` and `pollard_rho` for modular multiplication, **but not here**:
`r * r` is evaluated in 64-bit arithmetic and wraps modulo `2^64`.

**`r² + r + 1` first reaches `2^64` at `r = 2^32 = 4,294,967,296`.** The
paper's run reports reaching `z = 216,171,986,291` — about 50× past that — so
the wrap would affect essentially the whole sieve range. `get_factors` also
takes a `u64`, so even with exact arithmetic it could not hold
`r²+r+1 ≈ 4.7×10²²` for `r ≈ 2.2×10¹¹`.

Demonstrated on the first four primes above `2^32` (`restrained/05`): the
computed value differs from the true one in every case, and the sieve's verdict
**flips for 2 of the 4**:

| r | verdict on true value | verdict on wrapped value |
|---|---|---|
| 4294967311 | excluded by [2083, 10837] | excluded by [13, 16729] |
| 4294967357 | excluded by [7, 584509] | **can be ordinary** |
| 4294967371 | excluded by [7, 831373] | **can be ordinary** |
| 4294967377 | excluded by [19, 79273] | excluded by [875011] |

**Update (full transcript).** The paper names "the C++/GMP program
loopless.cpp", run for 3 weeks, and hosts its files at
`https://www.lirmm.fr/~ochem/opn/restrained/`.

**Update (original file).** The user copied `loopless.cpp` from the authors' page
(`lirmm.fr/~ochem/opn/restrained/`) and attached it, with its line breaks; it is
now `sources/loopless.cpp`. Ignoring whitespace it is identical to
the recovered paste, and **line 135 is `u64 val = r * r + r + 1;`**. So the file
the paper names does wrap past `r = 2³²`.

**The wrap is visible in the paper's own numbers (`restrained/11`).**
* **Part 1.** Fit a survival fraction `f₀` on `(3·10⁶, 2³²)` and `f₁` on
  `(2³², z)` to the reported `k = 2.5·10⁹` and `A = 1.088507187872`. This gives
  **`f₀ = 0.093` and `f₁ = 0.295`**, with `√f₀ = 0.305`. An exact sieve's survival
  fraction can only fall with `r`, since `M₂` only grows. The reported output
  triples at `2³²`.
* **Part 2.** Here is the mechanism, measured on sampled primes against the initial
  `M₂`. A prime `q ≡ 1 (mod 3)` divides `r² + r + 1` with probability about
  `2/q`, but divides an unrelated wrapped value with probability about `1/q`. So
  the wrapped test passes about `√(exact)`. With 10,000 samples:

  | r in | exact | wrapped |
  |---|---|---|
  | `10⁷ … 10⁸` (no wrap) | 0.1133 | 0.1133 |
  | `2³² … 2³² + 10⁹` | 0.1163 | 0.4358 |
  | `10¹¹ … z` | 0.1133 | 0.3592 |

**Reading.** On this evidence, the published `k` and `A` at `z` are the output of
the wrapped test, not of Algorithm 1. That is strong evidence, but not a
reproduction of their run. The heuristic direction is that the exact survivor set is
*smaller*, which would only raise `k + K_max` (§1a). So `q ≥ 23·10⁹` is **probably
still true, but currently unverified**. Only an exact re-run settles it. As before,
this should go to the authors as a question, not as a claimed error in the paper.

**How to read this.** The most likely explanation by far is that the published
run used a 128-bit or GMP variant that is not the released file — it already
defines `u128` and links GMP, so the authors clearly had the machinery. The
next most likely is that the released file is an earlier draft. I cannot
distinguish these from the source alone, and **this should be raised with the
authors rather than asserted as an error in the paper.**

For completeness, the direction of risk *if* the released file were the one
run: wrongly *including* a prime as ordinary inflates `A` and is conservative;
wrongly *excluding* one deflates `A` and would make the bound unsound. Both
occur in principle. In the four-prime sample above both flips were of the
conservative kind, but four samples settle nothing.

---

## 4d. Algorithm 1 re-run without the overflow (`restrained/12`–`14`)

The sieve was re-run to the paper's `z = 216,171,986,291` with the 64-bit wrap
removed. The user approved compiled C for this.

**Implementations and cross-checks.**
* `restrained/12_algorithm1_reference.py`: exact bare-CPython Algorithm 1.
* `restrained/13_sieve.c`: C with the standard library only. It never forms
  `r² + r + 1`. Instead, each `q ∈ M₂` marks the `r ≡ ρ, q−1−ρ (mod q)`, where `ρ` is a
  primitive cube root of unity mod `q`. The `M₁` test for `r ≡ 1 (mod 12)` reduces
  to one lookup: is `(r+1)/2` a survivor? (Proof in the header: `(r+1)/2 < 9·10¹²` is
  either divisible by a prime `< 3·10⁶` or is itself a prime.)
* **Memory limit.** Tracking every `q ∈ M₂` up to `z` needs about 32 GB. So a
  prime `q ≥ Q = 2³⁵` does not exclude anything. The run is **exact for
  `r < 3.44·10¹⁰`**. Above that it keeps a **provable superset** of Algorithm 1's
  survivors (induction in the header). A superset only lowers the bound, so the
  bound stays valid (§1a).
* **Agreement.** `12` and `13` agree line for line at `2·10⁸`, both exact and with
  `Q = 5·10⁷`. The authors' `loopless.cpp` was compiled **unmodified** against the
  system `libgmp` (with a declaration-only `restrained/loopless_build/gmp.h`). It agrees
  with the full run on **all 253 progress lines** it produced in one hour, to
  `r = 579,733,409`. That run is saved as `runs/loopless_released_1h.txt`.

**Result at `z`** (`runs/14_bound_z_Q2e35.txt`; 3188 s, 5.8 GB peak):

| | paper (wrapped test) | re-run (overflow-free) |
|---|---|---|
| survivors `k(z)` | "more than 2,500,000,000" | **599,351,328** |
| abundancy `A(z)` | 1.088507187872 | **1.047357816316** |
| `K_max` | (43,500,000,000 used) | **52,186,355,564** |
| `k + K_max` | 46,355,827,007 (§1a) | **52,785,706,892** |
| resulting `q ≥` | 23,000,000,000 | **26,392,853,446** |

* Exact checkpoints: at `2³²`, `k = 15,656,368` and `A = 1.035515112361`; at
  `10¹⁰`, `k = 33,867,299` and `A = 1.038326300307`.
* `k + K_max` first reaches `46·10⁹` at checkpoint `x = 1.89·10¹¹`.
* `M₂` ends with 3,997,201,149 primes. Of these, 3,313,545,857 are `≥ Q` and
  unused, which is the conservative part.

**Reading.**
1. **The paper's conclusion `q ≥ 23·10⁹` is confirmed.** It holds with a margin
   of `6.79·10⁹` in the prime count, conditional on the rest of its §4, which is
   not recomputed here. That rest is: primes `5 … 3·10⁶` ruled out (`tree.txt`),
   `p > 6·10⁶`, `σ₋₁(3^q) < 3/2`, and Lemma 8 with its cited theorems.
2. **The published sieve output is not Algorithm 1's.** The true survivor count is
   about a quarter of the reported one, as the wrap signature predicted (§4b).
   The two error directions partly cancel: a smaller survivor set makes the bound
   *stronger*. So the overflow did not endanger the theorem, and it only cost bound.
3. The same method, run correctly to the same `z`, gives **`q ≥ 26,392,853,446`**.
   This is a recomputation inside their framework, not a new method. It inherits
   every assumption in item 1, and it should be put to the authors alongside the
   overflow report before anyone quotes it.

**Numerical safety.** `ln A` is accumulated in `long double` with Neumaier
compensation, and padded by `10⁻¹⁵` in `14`. `∂K_max/∂ ln A = −1/ln(1 + 1/z) ≈ −z ≈
−2.2·10¹¹`, so the padding moves the bound by less than 1. The margin is
`6.79·10⁹`.

## 4e. `tree.txt`'s claim re-checked: every prime `11 … 3·10⁶` is ruled out (`restrained/15`)

The sieve's input assumption is that every prime `5 ≤ p < 3·10⁶` does not divide
`N`. The paper argues `5` and `7` by hand and delegates `11 … 3·10⁶` to `tree.txt`,
which `tree.cpp` generates. `tree.txt` is too large to transfer, so the claim was
re-checked here with an independent prover.

**The method** is `tree.cpp`'s, and its soundness was argued in
`NOTES_INVERSION.md`. Roots are taken in increasing order. Assume `r | N`.
* **Ordinary branch:** the prime factors `≥ 5` of `σ(r²)` (one `3` removed when
  `r ≡ 1 mod 3`) all divide `N`.
* **Special branch:** open only if `r ≡ 1 (mod 12)` and no other prime on the path is
  special. Then the prime factors of `(r+1)/2` divide `N`.
* **Closing a branch:** it closes if a factor is `< root`, or if some factor not
  already on the path closes in every status it can have.

**The implementation shares no code with `tree.cpp`.**
* Small factors come from `gcd(G, ∏ primes 5 … 3·10⁶)`.
* Larger factors come from Pollard–Brent, then a pure-Python ECM. A factor ECM
  returns is a gcd, so a bug in it can only lose completeness, never soundness.
* Primality: Miller–Rabin, deterministic below `3.3·10²⁴`, and a 20-base strong
  probable-prime test above.
* Any root that exceeds a budget is reported UNRESOLVED, never ruled out.

**Results** (`runs/15_tree_full_range.txt`):
* **Without `checkfacts.txt`** (`NOHINTS=1`, nothing of theirs but the method):
  **216,810 of 216,812** primes in `[11, 3·10⁶]` are ruled out. The run took about
  1.5 h on 3 cores, with 185 ECM splits.
* The other two, `502013` and `2152883`, stopped on ECM's budget, not on an open
  branch. **With `checkfacts.txt`'s factors, each verified to divide and to be a
  probable prime before use, both are ruled out.**
* **All 460 `checkfacts.txt` entries verify:** each listed factor divides its
  `x² + x + 1` or `x + 1` and is a probable prime.
* **So every prime `11 … 3·10⁶` is ruled out, as the paper states.** The only trust
  is in probable-prime tests on the large factors; the same is true of `tree.cpp`
  (`NOTES_INVERSION.md`).
* A first pass, before ECM and lazy recursion, also ruled out every other root. It
  left 15 on the Pollard budget, and all 15 were then ruled out with ECM.

**Together with §4d:** the computational half of the paper's §4 is now
independently confirmed. That covers `tree.txt`'s claim and the sieve. The
remaining inputs are
* the hand arguments for `5` and `7` and for `p > 6·10⁶`,
* `σ₋₁(3^q) < 3/2`, which is immediate,
* Lemma 8 and the theorems it cites (Bugeaud–Mihăilescu, Ochem–Rao Lemma 3,
  Bennett–Levin via Lemma 3).

## 4f. The corrected sieve run further: `z = 10¹²` (`restrained/13`, `14`)

The same program ran to `10¹²` with the same cutoff `Q = 2³⁵`. It is still exact
below `3.44·10¹⁰` and a provable superset above. One change was made first: the
survivor lookup for `(r+1)/2` became a forward-only queue, because a bitset to
`z/2` would not fit. Both `2·10⁸` regression runs reproduce exactly, and **every
checkpoint up to the paper's `z` is identical** to the §4d run. The run took
13,530 s at 5.8 GB (`runs/13_1e12_Q2e35_*`, `runs/14_bound_1e12_Q2e35.txt`).

| `z` | `k(z)` | `A(z)` | `k + K_max` | `q ≥` |
|---|---|---|---|---|
| `2.16·10¹¹` (paper's) | 599,351,328 | 1.047357816316 | 52,785,706,892 | 26,392,853,446 |
| `5·10¹¹` | 1,356,573,080 | 1.049706090471 | 120,942,420,398 | 60,471,210,198 |
| `10¹²` | 2,670,032,132 | 1.051620849343 | 240,019,297,934 | **120,009,648,968** |

* **Within the paper's framework, the corrected method gives `q ≥ 1.2·10¹¹`,**
  about 5.2 times its published `23·10⁹`. The bound grows about linearly in `z`,
  roughly `0.12 z`, so more compute buys more. The cost is about 3.8 h per
  `10¹²` at the current rate, growing slowly.
* **Correction (audit, 2026-09-28).** The `q` column was first printed as
  `120,009,648,966`. `14` rounded `(B−1)/2` up with `Decimal`'s `//`, which truncates
  toward zero. The correct value is `⌊B/2⌋`, rounded up to even: `120,009,648,968`.
  The weaker figure was still true. At the paper's `z` the value was unaffected.
* **It is conservative.** Of the 17.4·10⁹ primes that end in `M₂`, 16.7·10⁹ are
  `≥ Q` and were not used to exclude anything. An exact run would give a larger
  bound, but it needs a different memory design.
* **Inputs.** Everything in §4d still applies. With §4e, the only unrecomputed
  inputs are the hand arguments (5, 7, `p > 6·10⁶`), `σ₋₁(3^q) < 3/2`, and Lemma 8
  with its cited theorems.
* **Attribution.** This is Ochem–Zelinsky's method, run correctly and further.
  It is offered to them, not claimed as a new result.

## 4g. Pilot: an upper-bound sieve beyond brute force (`restrained/16*`)

**Question.** Brute force grows the `q` bound only linearly in `z`: about `0.12 z`,
at 3.8 h per `10¹²`. Can a provable upper bound on `ln A(z)` carry the §4 count much
further?

**Reduction (sound).** The count needs only an upper bound on `ln A(z)`. The
dynamic `M₂` contains `M₂ ∩ [7, Y)` for every `r > Y`, so every survivor
`r > Y` lies in the static set
`T' = {primes r : no q ∈ M₂, q < Y, divides r² + r + 1}`, with `Y = 10⁸` (exact `M₂`
from `16b`). So
`ln A(z) ≤ ln A(10¹²) + Σ over dyadic (x, 2x] of #T'(x, 2x] / x`.
Here `ln A(10¹²)` is the value from the superset run.

**The sieve.** Selberg's Λ² bound on the integers of `(x, 2x]`, sieving by every
prime `p < ξ`:
* `ω(p) = 3` for `p ∈ M₂` (the classes `0, ρ, ρ²`); `ω(p) = 1` otherwise;
* `|R_d| ≤ ω(d)`;
* bound `x/G(ξ) + (Σ_{d<ξ} ω(d)|λ_d|)²`, with `|λ_d| ≤ min(1, h(d) G(ξ/d)/G(ξ))`
  and `h(d) = ∏_{p|d}(1 + g(p))`.

`G`, `W` and the weighted sum are computed exactly for `ξ < 10⁸` (`16c`). The
Selberg inequality and the `λ_d` formula are textbook. They are **not yet written
out here**, so the pilot is not a proof. Floating point is used throughout.

**Checks.**
* The exact `G(ξ)` is at least the lower bound `G_low(ξ)` (`16`, first pass).
* A brute-force count on a small instance stays below the sieve bound.
* The measured density of the static set (`M₂` below `3·10⁶`) is `0.113 x/ln x`
  on `(x, 2x]`: exact to 0.5% at `10⁹` and `10¹⁰`
  (`runs/13_static_Q3e6_checkpoints.txt`), where the sieve bound is 11.0 and
  10.2 times the true count.

**Results** (`runs/16d_selberg_projection.txt`). "Loss" means the bound divided by
`0.113 x/ln x`.

| `x` | `10¹⁰` | `10¹²` | `10¹⁴` | `10¹⁶` | `10¹⁸` | `10²⁰` |
|---|---|---|---|---|---|---|
| loss, `|λ_d| ≤ 1` | 10.2 | 8.8 | 7.7 | 6.9 | 6.1 | 5.6 |
| loss, sharper `|λ_d|` | 7.7 | 6.7 | 5.9 | 5.3 | 4.8 | 5.2 (`ξ` capped at `10⁸`) |

Carried forward from `ln A(10¹²)`:
* crude weights: **`q ≳ 1.4·10¹²`**;
* sharper weights: **`q ≳ 7.4·10¹²`**, at `z ≈ 5·10¹⁴`.

So the gain is about 60 times the brute-force `1.2·10¹¹`, and about 300 times the
paper's `2.3·10¹⁰`. **It is not the orders of magnitude hoped for.**

**Why: the result is exponentially sensitive to the loss `L`.**

| `L` | 8 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|
| `q ≳` | `1.7·10¹²` | `9.2·10¹²` | `4.2·10¹³` | `4.9·10¹⁴` | `5.2·10¹⁶` | `5.1·10²¹` |

The loss has two parts. First, the level: the remainder term limits `ξ` to about
`x^{0.35–0.45}`, which costs a factor `ln x/ln ξ ≈ 2.2–2.9`. Second, `G(ξ)` is still
far below its asymptote `∏(q−1)/(q−3) · ln ξ`. The `ω = 3` primes are dense, and
`G` only captures products of them below `ξ`. That costs roughly another factor
of 2–2.5. An upper-bound sieve also cannot see the primes of `M₂` between `ξ` and
`x`, which the real survivors do avoid. That is why the true survival rate (about 7%
at `10¹²`) sits below the static rate (11.3%).

**Verdict.** This is a qualified negative. The elementary Selberg route is sound in
principle, and it would give about `q ≥ 7·10¹²` once made rigorous. It cannot give
the `10¹⁵–10²⁰` range. That needs a loss near 2–3, which by the table is worth 3 to
9 more orders of magnitude. Getting there needs stronger analytic input than an
elementary sieve at these scales: an explicit large sieve, or an explicit
Brun–Titchmarsh with constant near 2, for the prime condition. Under the repo's rules
that needs a specific paper, which the user would supply.

**Options.**
* **(a)** Make the `≈ 7·10¹²` rigorous. That means writing the Selberg inequality
  and the `λ_d` bound in full, outward rounding, and an independent audit. It is
  moderate work for about a 60-fold gain.
* **(b)** Import stronger explicit sieve results from a named paper, to cut `L`.
* **(c)** More brute force: linear, poor value.

## 4c. Verification of `3p2.txt`

`3p2.txt` backs the claim that, with 3 ordinary, every prime `≤ 1000` other
than `3, 7, 13, 31, 61, 193` is ruled out. Each line `X^2 => f₁ f₂ …` asserts a
factorisation of `σ(X²) = X²+X+1`; each `X^e => 2 f₁ …` asserts one of `X+1`.

**382 of 385 lines verify exactly** (`restrained/06`). The three failures:

| line as transcribed | true factorisation | reading |
|---|---|---|
| `739^2 => 7 26041` | `3 · 7 · 26041` | a dropped leading `3` — OCR |
| `953^2 => 811 5023` | `181 · 5023` | `181` misread as `811` — OCR; and `181` *is* ruled out earlier in the file, so the marker `F 811` should read `F 181` and the logic is unaffected |
| `59083^2 => 3 19 6604392133` | `3 · 18433 · 63127` | **does not resolve to a transcription slip** |

**A second, independent pass over the markers** (`restrained/07`) confirms the
discrepancy is isolated. Of the 241 lines carrying an `F t` or `XS t` marker,
**239 have the marker prime genuinely dividing the line's target**, tested
against a freshly computed target rather than the file's own factorisation. The
only two failures are the `953` line (the `811`/`181` slip above, where the cut
is valid with `181`) and the `59083` line.

### The `59083` cut, repaired

I was able to close that branch (`restrained/08`), so the file's **conclusion
stands** even though the stated reason does not.

Setting: §3, so 3 is ordinary, `3² ‖ N` and `e₃ = 2` exactly; the opening tree
of §3 puts the notable prime in `S = {7,13,19,31,61,97,127,331}`; on this
branch the special prime is `33457`. The path re-derives exactly:
`σ(659²) = 13·33457`, `33457+1 = 2·16729`, `σ(16729²) = 3·1579·59083`,
`σ(59083²) = 3·18433·63127`.

1. `659 ≡ 2 (mod 3)` contributes no 3; `16729` and `59083` are each `≡ 1 mod 3`
   and contribute one each. **Two copies of 3 are forced, and `e₃ = 2`, so the
   budget is exactly exhausted.**
2. `18433` and `63127` both divide `N`. Neither lies in `S`, so neither is
   notable; the special prime here is `33457`, so neither is special.
   **Both are therefore ordinary.**
3. Both are `≡ 1 (mod 3)`, so each forces a further copy of 3.
4. Four copies against a budget of two: **`XS 3`.**

So the cut is sound by `XS 3`, `659` remains ruled out, and `3p2.txt`'s
conclusion is unaffected.

**Resolved: it was the transcription.** The authors' own `tree.txt` entry for
`59083²` was checked directly and **does not list 19** — matching my computed
`3 · 18433 · 63127`. So the `F 19` in the paste is OCR damage, not something in
their files, and there is **no defect in Ochem–Zelinsky's data**. The `XS 3`
derivation above stands as an independent confirmation that the branch closes,
but it repairs nothing. All three `3p2.txt` failures are now attributed to the
transcription.

---

## 5. Status

| result | status |
|---|---|
| §2 and §3 of the paper | **verified**, all seven numeric bounds |
| §4 final product | **resolved** (§1a): printed value = sieve's `A` with `K = 43·10⁹`; with the text's `K` it is `1.99671 < 2` |
| Lemma A (`σ(3^q)` factors `≡ ±1 mod 12`) | **proved** + verified; a corollary of their Lemma 4 |
| Corollary B (ordinary `s ≡ 5 mod 12`) | **proved** |
| `q = o₁ + v₃(e+1)` | **proved**; shows `q ≥ o₁` is tight |
| Tightening `o₂ ≤ o₁ + 2` | **attempted, failed** — capacity is unbounded |
| Question 10 with `p = 3` | **excluded** |
| Question 10 in general | **open**; no collision for `x < 10⁶` |
| `3p2.txt` factorisations | **382/385 verify**; all 3 failures are OCR in the transcript |
| `3p2.txt` cut markers | **239/241 verify** against freshly computed targets |
| the `59083` line | **not a defect** — the authors' `tree.txt` lists no 19 either |
| `loopless.cpp` as released | **64-bit overflow past `r = 2^32`**, confirmed in the original file; the paper's reported `k, A` show the wrap's signature (§4b, `restrained/11`) |
| `tree.txt`'s claim (primes `11 … 3·10⁶` ruled out) | **confirmed independently** (§4e): all 216,812; two need `checkfacts.txt` factors, which were verified; all 460 entries verify |
| Upper-bound (Selberg) sieve beyond `10¹²`, pilot | **qualified negative** (§4g): about `q ≳ 7·10¹²` in principle (60 times the brute-force bound), not orders of magnitude; the loss factor of 5–7 is the obstacle |
| Algorithm 1, corrected, to `z = 10¹²` | `k + K_max = 240,019,297,934`, so **`q ≥ 120,009,648,968`** inside their framework (§4f) |
| Algorithm 1, overflow-free re-run to `z` | **`q ≥ 23·10⁹` confirmed** (margin `6.79·10⁹` primes); the same method gives `q ≥ 26,392,853,446`; true `k = 599,351,328`, `A = 1.047357816316` (§4d) |

Honest summary: Lemma A and Corollary B are real structural additions, and the
exact form of Lemma 8 usefully closes off one route. None of it improves
`q ≥ 23×10⁹`, and §3 above says why — the two unbounded components defeat every
counting argument I could construct against `o₂ ≤ o₁ + 2`.

## 6. What would help next

- ~~The **PDF** of arXiv:2607.19746, to settle the §4 discrepancy.~~ Done via the
  full transcript (§1a).
- **Confirmation from the authors on the two code/data points above**: which
  build of `loopless.cpp` produced the reported `z`, and what the real
  `59083^2` line of `3p2.txt` says.
- `tree.txt`, the remaining data file (primes up to 3,000,000), which did not
  transfer. The same mechanical check as `restrained/06` would apply to it.
- The original files from `https://www.lirmm.fr/~ochem/opn/restrained/`
  (`loopless.cpp` with its true line breaks, `tree.txt`), if network access to
  that host is allowed.

**On Corollary B as a sieve condition — negative.** I had hoped to add it to
Algorithm 1. It does not fit: the sieve's test is whether a candidate `r` *can
be ordinary*, and Corollary B instead constrains `σ(p^e)` for unknown `p, e`.
It eliminates no candidate, so it does not move `ω(N)` and hence does not move
`q`. Recorded so the idea is not retried.
