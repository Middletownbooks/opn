# Odd perfect numbers with exactly two even exponents above 2

**The cases `3 ∤ N` and `3² ‖ N`: a self-contained account with machine-checkable certificates**

This document collects the `k = 2` results of this repository into one argument
that a reader can check. It is written to be read without the working notes;
every step points to where its details and checks live.

---

## 0. Status, scope and caveats

**Claims.**

> **Theorem A** (`3 ∤ N`). There is no odd perfect number `N` with `3 ∤ N` and
> exactly two even exponents greater than 2.
>
> **Theorem B** (`3² ‖ N`). There is no odd perfect number `N` with `3² ‖ N` and
> exactly two even exponents greater than 2.

Together these leave, among odd perfect numbers with exactly two even exponents
above 2, only the case where **3 is one of those two exponents' primes** (`3^q ‖ N`
with `q ≥ 4` even). That case is **open** (§5).

**Cited theorems.** Nothing else is assumed.

| result | used for | where cited |
|---|---|---|
| Nielsen 2015: `ω(N) ≥ 10` | the count in 9 of the 14 profiles of Theorem B | `README.md` |
| Matveev 1998, Theorem 2.2 (Izv. RAN 62:4) | exact solution lists, used by 4 of the 14 profiles of Theorem B | `MATVEEV_1998.md`, transcribed from the page images in `sources/` and checked line by line against them |

**Theorem A uses no cited theorem.** Its certified proof (§2) needs only the
abundancy identity, closure and the cutoff. The earlier argument for Theorem A,
kept below as an independent second proof, used Nielsen 2007 (`ω(N) ≥ 12` if
`3 ∤ N`) and Bennett–Levin. The certified proof needs neither.

**How thoroughly each part has been checked.** The two theorems are not equally
well established, and this should be read before relying on either.

* **Theorem B** has been:
  * proved in the notes (`NOTES_S3_K2.md` §§1–14);
  * **independently audited** by a separate session (`audit_s3k2/`, no errors);
  * **independently rebuilt** with a different architecture (`s3k2/41`);
  * **certified**: every search tree is checked by a small independent checker
    (`s3k2/46`), which rejects deliberately forged trees (§4).
* **Theorem A** has two independent proofs.
  * The first is a fixed-support abundancy argument produced by a reasoning
    model. Its arithmetic and skeleton were audited (`AUDIT_K2_MODEL_RESULT.md`,
    `k2/audit/`), but it was not refereed in full.
  * The second is **certified**. It was rebuilt with Theorem B's machinery
    (`k2/05`), every search tree is checked by an independent checker (`k2/06`)
    that rejects forged trees, and a brute-force cross-check agrees (`k2/07`).
    It uses no cited theorem.

**Novelty.** This document claims **no** novelty until a literature search
confirms that nothing since Ochem–Zelinsky (arXiv:2607.19746, which treats one
even exponent above 2) already covers these cases. That search has not been done
in this repository.

---

## 1. Setting

Let `N` be an odd perfect number, so `σ(N) = 2N`. By Euler, `N = p^e m²` with
`p ≡ e ≡ 1 (mod 4)`; `p` is the **special** prime. Call a prime-power component
`r^a ‖ N`:

* **ordinary** if `a = 2`;
* **notable** if `a` is even and `a ≥ 4`.

`N` is **`k`-restrained** if it has exactly `k` notable components. Ochem and
Zelinsky treat `k = 1`. This document treats `k = 2`.

Two facts are used throughout.

* For an ordinary prime `x`, `σ(x²) = x² + x + 1`.
* Every prime factor of `x² + x + 1` is 3 or `≡ 1 (mod 3)`. Moreover
  `v₃(x² + x + 1) = 1` if `x ≡ 1 (mod 3)`, and `0` otherwise.

---

## 2. Theorem A: `3 ∤ N`

### 2.1 The certified proof  (`k2/05`–`07`, `NOTES_K2.md` §7)

**Structure** (each step proved in `k2/05`'s docstring).

* An ordinary `s ≡ 1 (mod 3)` gives `3 | s² + s + 1 | 2N`. So every ordinary
  prime is `≡ 2 (mod 3)`; call their set `U`.
* A special `p ≡ 2 (mod 3)`, with `e` odd, gives
  `σ(p^e) ≡ Σ_{i ≤ e} (−1)^i = 0 (mod 3)`. So the special is `≡ 1 (mod 3)`,
  hence `≡ 1 (mod 12)`, and `3 ∤ e + 1`.
* A notable `n ≡ 1 (mod 3)` needs `3 ∤ q + 1`.
* `T` is the special plus the notables `≡ 1 (mod 3)`; `W` holds the other
  notables. There are three profiles: `T` roles `s`, `sn`, `snn`, with `|W| = 2, 1, 0`.
* `∏ σ(C)/C = 2`, and `U ⊆ Sm(T)`.
* Forcing: the primes `≡ 1 (mod 3)` dividing `p + 1` lie in `T`.

**Search.** The search starts from `K = ∅` with `lb = 6`, so the smallest element
of `T` is itself enumerated under the cutoff. The `W` slots run over every pair
of notables `≡ 2 (mod 3)`: explicit below 1000, or generic.

**Result.**

| profile | nodes | kills |
|---|---|---|
| `s` (two notables in `W`) | 7 484 | every `W` pair: the cutoff leaves only `p = 13`, and `13 + 1 = 14` forces `7 ∈ T`, a contradiction |
| `sn` | 630 | closure 100, two-sided abundancy 87 |
| `snn` | 54 | closure 14, two-sided abundancy 7 |

**Every certificate is VALID, and no count kill appears.** So Theorem A needs
neither Nielsen's `ω` bound nor any solution list. A brute-force cross-check
agrees: every `T` from the primes below 400, with every role and every `W`,
through the complete-information test. Of 31 481 configurations, **none
survives** (`k2/07`).

### 2.2 An independent second proof: the reasoning model's argument

Full argument: `NOTES_K2.md`, `AUDIT_K2_MODEL_RESULT.md`, `k2/audit/01`–`04`.

Since `3 ∤ N`, no ordinary prime is `≡ 1 (mod 3)`, because it would put 3 into
`σ(N)`. So every ordinary `s` is `≡ 5 (mod 6)`. Every prime factor of
`s² + s + 1` is then `≡ 1 (mod 3)`, hence not ordinary, hence one of
`p, n₁, n₂`. So each ordinary `σ(s²)` is supported on the three big components.
Split on the residues of the two notables mod 3.

* **(iii) Both notables `≡ 2 (mod 3)`.** They never divide any `s² + s + 1`, so
  every ordinary `σ(s²)` is a power of `p`. By Bennett–Levin, `σ(s²) = p`, so
  there is at most one ordinary prime and `ω(N) ≤ 4`. That contradicts
  `ω(N) ≥ 12`.
* **(ii) Exactly one notable `≡ 2 (mod 3)`.** The ordinary classes collapse to
  those of `k = 1`. A fixed-support abundancy bound gives a product below 2 in
  both sub-cases: `n₂ ≠ 5`, giving `1.8575`, and `n₂ = 5`, giving `1.7942`. The
  second removes 5 from the ordinary primes. Counting it in both roles was an
  error in an earlier draft, recorded in the audit.
* **(i) Both notables `≡ 1 (mod 3)`.** A *weighted* fixed-support bound. Fix the
  support `{r₁ < r₂ < r₃}` of the classes. Each class `(a,b,c)` hosts at most one
  ordinary `s`, and `log(s/(s−1)) < 1/(√M − 2)` with `M = s² + s + 1`. The tail
  over mixed monomials is bounded by a closed form in `x = r₁^{−1/2}`, etc. An
  11-row case division on the smallest support primes gives a product below 2
  in every row. The largest is `1.96031`, verified in exact rationals
  (`k2/audit/02`). The division is checked exhaustive over 365
  support-and-flag combinations (`k2/audit/03`).

---

## 3. Theorem B: `3² ‖ N`

Full argument: `NOTES_S3_K2.md` §§1–14. Audit: `audit_s3k2/AUDIT_S3K2_RESULT.md`.

### 3.1 Structure

`3² ‖ N` means `3` is ordinary, and `σ(3²) = 13`, so `13 | N`. Let:

* `T` be the primes `≡ 1 (mod 3)` dividing `N` (so `13 ∈ T`);
* `A ⊆ T` the ordinary ones, with `α = |A|`;
* `W` the big components (special or notable) that are `≡ 2 (mod 3)`;
* `U` the ordinary primes `≡ 2 (mod 3)`.

**3-budget** (§1 of the notes). `v₃(σ(N)) = v₃(N) = 2`, and `σ(3²) = 13` supplies
none of it. The other components spend:

* 1 per ordinary prime in `A`;
* `v₃(k+1)` per big component `≡ 1 (mod 3)` (its exponent `k`);
* `v₃(w+1) + v₃(e+1) ≥ 1` for a special `w ∈ W`;
* 0 for everything else.

Hence `α + [special ∈ W] ≤ 2`.

**Identity.** `∏_{C ≠ 3²} σ(C)/C = 2 · 9/13 = 18/13`, where the ordinary factor
is exactly `f(x) = 1 + 1/x + 1/x²`.

**Count.** The prime divisors are `{3} ⊔ T ⊔ W ⊔ U`, and the three big components
split between `T` and `W`. So `ω(N) = 4 + α + |U|`, and Nielsen 2015 gives
**`|U| ≥ 6 − α`**. Every `x ∈ U` has `x² + x + 1` supported on `T`, so
`U ⊆ Sm(T) := {x prime, x ≡ 2 (mod 3) : x² + x + 1 is T-smooth}`.

**Profiles.** A role profile records `α`, whether the special is in `T`, and the
number of notables in `T`. Exactly **14** profiles are consistent with the budget
and with `13 ∈ T` (notes §13c; re-derived in the audit's Pf.1).

### 3.2 The tools

Each tool is valid for every configuration it is applied to, including supersets
of a partial `T`. The audit's appendix Pf.2–Pf.5 checks exactly this.

| tool | statement | where |
|---|---|---|
| role ranges | ordinary: exactly `f(t)`. Special in `T`: `t ≡ 1 (mod 12)`, factor in `[σ(t^{e₀})/t^{e₀}, t/(t−1))`. Notable: `[σ(t^{q₀})/t^{q₀}, t/(t−1))`. `e₀, q₀` are the least admissible exponents | notes §5a; `s3k2/41` |
| forcing (closure) | prime factors `≡ 1 (mod 3)` of `t² + t + 1` (`t` ordinary), of `t + 1` (`t` special, `e` odd), and of `w + 1` (`w` special in `W`) lie in `T` | notes §9; `s3k2/41` |
| tail (Rankin) | members of `Sm(T)` with `x² + x + 1 > Y` contribute at most `exp(c_Y · Y^{−ε} ∏(1 − t^{ε−½})^{−1})` | notes §5b |
| new-member bound | `log f(x) ≤ (1 + 1/(√M₀ − 1))² M^{−½}` whenever `M = x²+x+1 ≥ M₀` | `s3k2/41` docstring |
| cutoff | if `(18/13)/(H₀(K)·HI(K)) ≥ corr_u(B, K)`, no `T ⊇ K` has its smallest unknown `≥ B`. The cap in `H₀` uses only the **raw** role minimum | audit Pf.2; `s3k2/41` |
| two-sided test | `max(LO, (18/13)/H) ≥ HI` is a contradiction | notes §5⅔ |
| count | `|U| ≥ 6 − α` with `U ⊆ Sm(T)`, which needs `Sm(T)` complete | §3.1 |
| valuation caps | an ordinary `a` has `e_a = 2 = Σ_{C≠a²} v_a(σ(C))`, so contributions already forced cap what `U` may use | notes §14c |
| coupled pairs | two ordinary unknowns each dividing the other's `x² + x + 1` use at most one unit each of `U`'s budget | notes §14a, §14h; `s3k2/40` |

**Exact solution lists.** The count needs `Sm(T)` complete.

* **One free exponent.** `x² + x + 1 = D·pᶜ` is solved for all `c` by Skolem's
  method (`s3k2/32`, notes §14b).
* **Several free exponents.** The equation `x² + x + 1 = 3^δ ∏ t^{c_t}` has
  `Y = 1`, so only archimedean logarithms appear. Matveev's bound followed by
  lattice reduction gives the complete list (`s3k2/39`, notes §14h).
* **Independent agreement.** Every list used is also produced by the auditor's
  independent solver (`audit_s3k2/a4_solver.py`: exact LLL with Fincke–Pohst
  enumeration). The two agree on all of them (`s3k2/45`).

### 3.3 The fourteen profiles

Profiles are written (`α`, special in `T`, notables in `T`, `τ = |T|`, `|W|`).

| profile | eliminated by | cited theorems used |
|---|---|---|
| `1,no,0,1,3` | the 3-budget and forcing, by hand (notes §11b) | none |
| `0,no,2,2,1`, `0,yes,2,3,0`, `1,yes,2,4,0`, `1,no,2,3,1` | search: forcing, raw minimum, cutoff, two-sided test | none |
| `0,no,1,1,2`, `0,yes,0,1,2` | `T = {13}`, `Sm({13}) = ∅` (Skolem), count | Nielsen 2015 |
| `1,no,1,2,2`, `1,yes,0,2,2` | `T = {13, 61}` forced; valuation caps; Skolem; count (notes §13a, §14c) | Nielsen 2015 |
| `2,yes,0,3,2` | `T = {13, 61, 97}`, or the coupled branch (Vieta, notes §14a); Skolem; count | Nielsen 2015 |
| `0,yes,1,2,1`, `1,yes,1,3,1`, `2,yes,1,4,1` | search; the named sets in §3.4 need complete `Sm`; coupled count | Nielsen 2015, Matveev 1998 |
| `2,yes,2,5,0` | search; seven named sets in §3.4 | Nielsen 2015, Matveev 1998 |

### 3.4 The named sets that need complete solution lists

These are the only places the Matveev + LLL lists are used. Each dies because
fewer than `6 − α` members of the complete `Sm(T)` are admissible.

| `T` | `W` | complete `Sm(T)` | admissible | need |
|---|---|---|---|---|
| `{7,13,19,37,67}` | ∅ | 11, 29, 653 | 653 | 4 |
| `{7,13,19,37,127}` | ∅ | 11, 107, 653 | 107, 653 | 4 |
| `{7,13,19,43,127}` | ∅ | 11, 107, 653 | 107, 653 | 4 |
| `{7,13,19,127,409}` | ∅ | 11, 53, 107, 653 | 53, 107, 653 | 4 |
| `{7,13,19,127,1723}` | ∅ | 11, 41, 107, 653 | 41, 107, 653 | 4 |
| `{7,13,19,31,127}` | ∅ | 5, 11, 107, 191, 653 | 191, 653 | 4 |
| `{7,13,19,31,331}` | ∅ | 5, 11, 191, 653 | 191, 653 | 4 |
| `{7,13}` | notable 11 | ∅ | ∅ | 6 |
| `{7,13,19}` | notable 23 | 11, 653 | 653 | 5 |
| `{7,13,19,127}` | notable 29 / 41 / 47 | 11, 107, 653 | ≤ 2 | 4 |

Two further items close by the same lists:

* **Case-B searches.** For `S = {7,13}` and `{7,13,19}`, the complete lists of `t`
  with `(t²+t+1)/3` `S`-smooth contain no admissible `t`.
* **The coupled pair at `{7,13}`.** It dies by the count, since
  `Sm({7,13}) = ∅`.

---

## 4. Certificates

**What is certified.** For each of the eight profiles handled by search, the
search (`s3k2/41`) writes its **entire proof tree**, one node per line. The
checker (`s3k2/46`, one file, no code shared with the search) verifies two
things.

1. **Exhaustiveness.** At every node the checker recomputes, from the
   specification alone, the complete list of children that node's case split
   requires, and demands exactly those children.
   * roots: every seed `min T ∈ {7, 13}`, with every role and every `W`
     configuration;
   * pin: every role of the forced prime;
   * cut: every prime `≡ 1 (mod 3)` in `(lb, B)`, with every role;
   * Case B: every `t` in the complete list.
2. **Each claim.** Every kill is re-verified in exact or outward-rounded
   arithmetic:
   * a forcing claim comes with a divisibility witness;
   * raw minima, two-sided tests and cutoff inequalities are recomputed;
   * a count uses the axioms file.

**Trust base.** To accept the searched profiles (all of Theorem A, and 8 of the 14 profiles of Theorem B) you must trust:

* the checkers, `s3k2/46` for Theorem B and `k2/06` for Theorem A, about 300 lines each and sharing one design;
* the axioms file `s3k2/axioms_complete_lists.json`: 12 complete solution lists,
  each produced by two independent solvers that agree (`s3k2/45`);
* the cited theorems.

You need not trust the search, which is about 450 lines, nor scripts 34–38.

**Results.**

| profile | certificate nodes | verdict |
|---|---|---|
| `0,no,2,2,1` | 839 | VALID |
| `0,yes,1,2,1` | 664 | VALID |
| `0,yes,2,3,0` | 146 | VALID |
| `1,no,2,3,1` | 86 720 | VALID |
| `1,yes,1,3,1` | 21 857 | VALID |
| `1,yes,2,4,0` | 7 090 | VALID |
| `2,yes,1,4,1` | 1 227 157 | VALID |
| `2,yes,2,5,0` | 1 679 712 | VALID |
| Theorem A: `s`, `sn`, `snn` | 7 484, 630, 54 | VALID (checker `k2/06`) |

The checker's list of axioms used confirms the tally of §3.3 independently. The
four profiles `0,no,2,2,1`, `0,yes,2,3,0`, `1,no,2,3,1` and `1,yes,2,4,0` use
no solution list and no count.

**The checker rejects forged proofs.** Each forgery comes from a deliberately
broken search, so every node is consistent with the broken logic; these are not
hand-edited files. Every one is rejected:

| forgery | checker's verdict |
|---|---|
| cutoff with one prime instead of `u` (the error of notes §14d) | INVALID: cutoff inequality fails |
| cutoff thresholds 10× too small | INVALID: cutoff inequality fails |
| over-eager forcing (`f ≤ 3·lb`) | INVALID: closure claim false |
| raw kill at 99% of `18/13` | INVALID: raw minimum does not exceed `18/13` (on every profile where it changes the tree) |
| a role split dropped at cut nodes | INVALID: a required child is missing |

The first two matter most. Neither can be detected by any empirical test,
because the cutoff is conservative relative to the complete-information test
(notes §14l). The checker catches both because it re-proves every cutoff.

**Not covered by certificates.** The six profiles closed by hand or by short
scripts: `1,no,0,1,3` (notes §11b), and the five of §14c (`s3k2/31`, `s3k2/33`).
Their arguments are a few lines each and are in the notes.

---

## 5. What is open

* **`3` notable (`3^q ‖ N`, `q ≥ 4` even).** This is the one remaining `k = 2`
  case. At `k = 1`, Ochem–Zelinsky reduce it to `q ≥ 2.3·10¹⁰` rather than
  eliminating it. The partial `k = 2` results are in `NOTES_S4_K2.md` and
  `AUDIT_S4K2_MODEL_RESULT.md`:
  * a Zsigmondy costing of the second notable;
  * the bound `q ≤ m + 3ω(N) − 8`, with `m` bounded by a Nielsen-style descent.
* **Certify the six small profiles of Theorem B** that are closed by hand or by
  short scripts. This is optional, since each is a few lines.
* **Literature check** (§0), before any claim of novelty.

---

## 6. Reproducing

```
python3 verify_all.py full              # every figure of NOTES_S3_K2.md §14 (about 1.5 h)
python3 s3k2/45_axioms.py               # the 12 axioms, by two solvers
for p in 0,no,2,2,1 0,yes,1,2,1 0,yes,2,3,0 1,no,2,3,1 1,yes,1,3,1 1,yes,2,4,0 2,yes,1,4,1 2,yes,2,5,0; do
  python3 s3k2/41_rebuild_dfs.py --cert $p | python3 s3k2/46_check_certificate.py
done                                    # certificates (about 1 h in total)
for p in s sn snn; do
  python3 k2/05_theoremA_dfs.py --cert $p | python3 k2/06_check_theoremA.py
done                                    # Theorem A certificates (about 1 min)
python3 k2/07_theoremA_pool.py 400      # Theorem A brute-force cross-check
python3 k2/audit/02_check_case_i.py     # Theorem A, second proof: case (i) rows
```

Everything is standard-library Python 3.
