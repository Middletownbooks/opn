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

## 5. Status

| result | status |
|---|---|
| §2 and §3 of the paper | **verified**, all seven numeric bounds |
| §4 final product | **not reproduced** from the transcript; conclusion unaffected |
| Lemma A (`σ(3^q)` factors `≡ ±1 mod 12`) | **proved** + verified; a corollary of their Lemma 4 |
| Corollary B (ordinary `s ≡ 5 mod 12`) | **proved** |
| `q = o₁ + v₃(e+1)` | **proved**; shows `q ≥ o₁` is tight |
| Tightening `o₂ ≤ o₁ + 2` | **attempted, failed** — capacity is unbounded |
| Question 10 with `p = 3` | **excluded** |
| Question 10 in general | **open**; no collision for `x < 10⁶` |

Honest summary: Lemma A and Corollary B are real structural additions, and the
exact form of Lemma 8 usefully closes off one route. None of it improves
`q ≥ 23×10⁹`, and §3 above says why — the two unbounded components defeat every
counting argument I could construct against `o₂ ≤ o₁ + 2`.

## 6. What would help next

- The **PDF** of arXiv:2607.19746, to settle the §4 discrepancy.
- `loopless.cpp` and `checkfacts.txt` from `lirmm.fr/~ochem/opn/restrained/`.
  `loopless.cpp` implements Algorithm 1, the sieve that produces the
  `ω(N) > 46×10⁹` bound — the one place where a better argument directly moves
  `q`, and the place they themselves flag for improvement. Corollary B is a new
  sieve condition that could be added to it: an ordinary prime `≡ 5 mod 12`
  must be doubly produced by the special component.
- `3p2.txt` and `tree.txt`, the data files backing the "primes up to 1000" and
  "primes up to 3,000,000" eliminations, to check those are complete.
