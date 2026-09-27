# Audit of §3 at `k = 2` (3 ordinary), `NOTES_S3_K2.md` §14

Independent audit following `PROMPT_AUDIT_S3K2.md`. Every script named here is in
`audit_s3k2/` unless its path starts with `s3k2/`. Standard library only. Logs of
every run quoted are in `audit_s3k2/logs/`. No existing note or script was edited.

Throughout, **"verified by script X"** means I ran X and it printed the stated
result. **"Proved here"** means the argument is written out in this file. Results
attributed to the literature are only the two the repo cites: Nielsen 2015
(`ω(N) ≥ 10`) and Matveev 1998, Theorem 2.2.

---

## 1. Verdict

**The claim of §1 stands, conditional on the two cited theorems, with repairs to
documentation only.**

* **No cited theorem at all: 5 profiles.** These are `1,no,0,1,3` (§11b, by hand)
  and the four §14e profiles `0,no,2,2,1`, `0,yes,2,3,0`, `1,yes,2,4,0`,
  `1,no,2,3,1`. Their tallies have 0 conditional sets, 0 exceptions and 0 Case-B
  searches, so every kill is abundancy, closure or raw minimum. `ω(N) ≥ 10` is
  never used for them.
* **(i) only: 5 profiles.** `0,no,1,1,2`, `0,yes,0,1,2`, `1,no,1,2,2`,
  `1,yes,0,2,2`, `2,yes,0,3,2`, via `s3k2/33` (Skolem + valuation + Vieta).
* **(i) and (ii): 4 profiles.** `2,yes,2,5,0`, `0,yes,1,2,1`, `1,yes,1,3,1`,
  `2,yes,1,4,1`, via `s3k2/39`/`40`.

The repo's "ten use only (i)" is therefore an over-statement in the safe
direction.

I hunted specifically for the failure pattern of §14d–§14f: a bound proved for one
object and applied to a larger class. I checked every kill in the chain against
supersets, other role assignments and other `W` configurations. I found **no kill
that is invalid**.

I found three places where the written justification is **incomplete or wrong
while the inequality actually used is true**:

* the narrowing argument in `s3k2/34`'s docstring (finding G1);
* the factor `1.01` in `corr_k` (G2);
* the "iterated" narrowing of §5⅔ (G3).

My independent Matveev computation and my independent lattice solver agree with
`s3k2/39` on every one of the 18 statements it settles:

* the 13 named `Sm(T)` sets and the 5 Case-B sets;
* the 8 single-exponent equations of `s3k2/33`;
* the three sets named in the brief.

My solver uses a different reduction: exact LLL, then complete Fincke–Pohst
enumeration, then enumeration of exponent vectors. The result is insensitive to
Matveev's constant up to a factor `10³⁰`.

What this audit does **not** establish:

* the correctness of Theorem 2.2 itself, or of Nielsen's theorem;
* the transcription of `MATVEEV_1998.md`, which the user is checking;
* a from-scratch re-implementation of the `s3k2/36` recursion. I reviewed it line
  by line, mutation-tested it, and re-derived its thresholds and final kills on
  samples, but did not rewrite it.

See §5.

---

## 2. Findings

Status key: `CONFIRMED` (checked and holds), `ERROR` (wrong and affects the
claim), `GAP` (a justification is missing or wrong, but the statement used is
true; I supply the repair), `COULD NOT VERIFY`.

**No finding has status `ERROR`.**

### 2.1 The chain of kills, one inequality each

Notation. `X = PROD_T(S) · PROD_W` is the product over the known `T`-primes and
the `W` slot. `Y = PROD_T(T∖S) · PROD_U`. The identity is `X·Y = 18/13`, and
`f(x) = 1 + 1/x + 1/x²`.

`LO_raw(S)` is the minimum over admissible role assignments of `S` of the product
of role minima, times `LOW` for the `W` configuration. `HI(S)` is the maximum of
the role maxima, times `HIW`. `H₀(S)` is the product of `f(x)` over those
`x ∈ Sm_{≤10²⁴}(S)∖{w}` with `f(x) ≤ (18/13)/LO_raw(S)`, times the Rankin tail,
rounded up.

| # | kill | exact inequality | valid for supersets `T ⊋ S` (built upward)? | other role assignments? | other `W` configs? | status |
|---|---|---|---|---|---|---|
| K1 | `margin()`/`bounds()` returns `None` | no role assignment of `S` passes `min_factor ≠ None` ∧ `closure_ok` ∧ `forced_ok`, or `LOW = None` | yes. Each filter is a necessary condition on `T`, given that `T ∩ (0, max S] = S` and `MIN = S[0] = min T` | all assignments tried | per config | CONFIRMED |
| K2 | raw minimum (`36`, lines 352–356) | `LO_raw(S) > 18/13` ⇒ `X·Y ≥ LO_raw(S)·1·1 > 18/13` | yes: extra role factors are `> 1`, `PROD_U ≥ 1` | min over all | per config (`LOW` is the config minimum) | CONFIRMED |
| K3 | cutoff (`34`, `36`, `38`) | `(18/13)/(H₀(S)·HI(S)) ≥ corr_k(B,S)` ⇒ no `T` whose `(|S|+1)`-th element is `≥ B` | yes. Proof in §3.2: `Y < H₀(S)·corr_k(B,S)` for every such `T` | min/max over all | per config | CONFIRMED (docstring GAP G1) |
| K4 | final two-sided test | `T` complete, `LO_n(T) ≥ HI(T)` or `LO > 18/13` | not applied to supersets | global min/max ⊇ true assignment | per config | CONFIRMED |
| K5 | count | `|keep| < 6−α`, or the product of the `6−α` smallest admissible `f > 18/13/LO_n` | `T` complete; needs `Sm(T)` complete, which `39` supplies | global | per config | CONFIRMED |
| K6 | last level (`last_candidates`) | `t` pinned by closure, or `t` ordinary with `(t²+t+1)/3` `S`-smooth and `< B²` (exact), or per-split cutoff `B` | exhaustive split (§3.4) | per split, all perms | per config | CONFIRMED |
| K7 | DFS (`38`) | pinning; W-forced; raw `> 18/13`; cutoff on the smallest unknown with `u` unknowns; exact Case B; conditional Case B / Vieta passed to `39` / `40` | invariant "every unknown `> lb`, and `K ∪ unknowns = T`" is maintained (§3.5) | branches over all roles | per config | CONFIRMED |
| K8 | level-5 closure (`35`) | no assignment with `F(a) ⊆ T` for both ordinary `a`, special `≡ 1 (mod 12)` with admissible `e`, notables with admissible `q` | `T` complete | all 30 | `W` empty | CONFIRMED |

### 2.2 Findings table

| id | status | location | statement | evidence | affects claim? |
|---|---|---|---|---|---|
| A1 | CONFIRMED | `NOTES_S3_K2.md` §1–2, §13c | exactly 14 profiles; `ω(N) = 4+α+|U|`; `|U| ≥ 6−α` | §3.1, proved here | — |
| A2 | CONFIRMED | `s3k2/34` docstring, `36:163` `corrk` | the `k`-prime cutoff lemma | §3.2, proved here; thresholds recomputed from scratch (`a2_thresholds.py`: `{7}` 1751, `{13}` 712, `{7,13}` 5970, `{7,13,19}` 27 723, all matching §14d) | — |
| G1 | GAP | `s3k2/34` docstring line 20; `NOTES` §14d | "interval narrowing on `S` stays valid because `R(T) ≤ R(S)`". The **narrowed** `LO(S)` is **not** a lower bound for `X` when `T ⊋ S`. For example `107 ∈ Sm(S∪{127})∖Sm(S)` for `S = {7,13,19,31}`. The kill is valid for another reason: the narrowing is exactly one step (G3), its cap uses only `LO_raw` (superset-valid), and `margin ≥ corr_k` is then equivalent to `(18/13)/(H₀·HI) ≥ corr_k` | §3.2 | **no**. But a future change that lets the cap depend on narrowed information would silently break superset validity. Recommend stating the lemma in the form of §3.2. |
| G2 | GAP | `s3k2/34` docstring lines 13–22; `13_cutoff_lemma.py` | the factor `1.01` is justified by `1/x < (1+1/(√B−1))M^{−1/2}` "plus `1/x²`", which needs `1/x ≤ 0.01`, i.e. `B ≳ 10⁴`. Several thresholds are below that (`B({13}) = 712`) | the needed per-term inequality `log f(x) ≤ 1.01(1+1/(√B−1))M^{−1/2}` holds for all `x ≥ 2`: `log f(x)·(√M−1) < 1` for every `x` (`a2_corr_factor_check.py`: max `1.000000`; analytic for `x ≥ 100`) | **no** |
| G3 | GAP (exposition) | `NOTES` §5⅔ "one iterates"; loops at `36:228`, `36:265`, `38` `lohi_roles`, `35` | the narrowing loop never excludes anything after its first pass: the new cap is `Hup ≥ H ≥ f(x)` for every admitted `x` | proved here, §3.3 | no. It explains why K3 is valid (G1). |
| M1 | CONFIRMED | `MATVEEV_1998.md`, `39:120–149` | Theorem 2.2 is applicable: `K = ℚ(ω)`, `D = 1`, `ρ = rank_ℝ = 1` (read from `p85.png`), Kummer (1.5) holds (`p82.png`), `h(π/π̄) = ½ log t`, `ϑ = E = 1`, `C₃ = n/ρ` satisfy (2.1)–(2.3), `Λ ≠ 0`, `|Λ| ≤ 2√3/|z|`, `|b₀|`, `b_n ≠ 0` | §3.6, and `a3_matveev_bound.py` | — |
| M2 | CONFIRMED (a small strengthening) | `MATVEEV_1998.md`, `39:15` | the repo uses `|Λ| ≤ 2√3/|z|` only for `|z| ≥ 2√3` and covers the rest with `L ≥ ln 12`. In fact `|Λ| = 2|arg z| ≤ π|sin arg z| = (π√3/2)/|z|` for **all** `x ≥ 0` | §3.6 | no (the repo's version is also correct) |
| M3 | CONFIRMED | `MATVEEV_1998.md` correction; p. 87 | the remark after (2.16) fails by `2.06` (`n = 2`) to `3.23` (`n = 10`), the same for `ρ = 1, 2`, tending to `≈ 4`. This is consistent with a loose remark (it would hold with `2¹⁷` for `2¹⁵`), **not** with a misreading of (2.4): the zoomed crops read exactly as transcribed | `a3_matveev_bound.py` (`remark_check`) | no. Insensitive: ×`10⁶` (repo's own code, all 18 statements, `logs/mut_c112x1e6__*`) and ×`10³⁰` (my code, `logs/a4_solver_factor1e30.log`) leave every answer unchanged |
| M4 | CONFIRMED | `39` `matveev_X0` | initial bound for `{7,13,19}` | mine `H ≤ 2.18·10¹²`; repo `2.42·10¹²`. The repo's is more conservative: `|b₀| ≤ 3kH+1`, worst `A_n` over all indices including `ζ₆`, `+1%`. `Ω` and `ω` agree to 4 digits | — |
| L1 | CONFIRMED | `39` docstring, `reduce_bound` | lattice lemma: `‖v‖ ≥ min|b*_i|` for **any** basis; `|det R| = |det Bm|` with unimodular steps ⇒ `R` is a basis of `Γ`; `T₀ = (Σ|e_t|+|b₀|)/2`; `|b₀| ≤ 3kH + 3/π` needs `|Λ| ≤ 1`, i.e. `|z| ≥ 2√3`, and the rest is `L < ln 12`, covered by `L = max(L, ln 12)`; the final search is exhaustive over `3^δ T`-smooth `M ≤ e^L` | proved here, §3.7 | — |
| L2 | CONFIRMED | `39 residual` | complete lists | independent solver `a4_solver.py`, a different reduction; agrees on **all** 13 named sets and 5 Case-B sets (`logs/a4_all_residual.log`) and the brief's three sets (§4) | — |
| S1 | CONFIRMED | `s3k2/32` | Skolem/Strassmann: `Λ ≡ X (mod ℓ²)` (true for `ℓ ≥ 3`); `v(a_k) ≥ ⌈(3k+1)/4⌉ ≥ 2` for `k ≥ 2`, `ℓ ≥ 5`; a class is "settled" only if `E`, or `O` with a known solution in the same `ℓ`-class | proved here, §3.8; the 8 equations cross-checked by my lattice solver (`logs/a4_check33.log`) | — |
| V1 | CONFIRMED | `s3k2/31` | Vieta classification (`k = 5` forced; strict descent) and ratio lemma (base `61 > 4.6·13`, induction from `m = 4`) | re-proved by hand, §3.9 | — |
| C1 | CONFIRMED | `s3k2/33` | valuation caps: `e_a = 2 = Σ_{C≠a²} v_a(σ(C))`, every term `≥ 0`; counted contributions are `σ(3²)=13`, `σ(61²)=3·13·97`, `σ(13²)=3·61` | checked | — |
| R1 | CONFIRMED | `s3k2/36` | `W` configurations cover every `w`: explicit `w < 500`, generic `w ≥ 500` with factor in `[1, 500/499)`, special split `e = 1` / `e ≥ 5` (`e ≡ 1 mod 4`). The budget relaxation only lowers minima. `admissible()` can only fire with `q = 7` (`MIN ∈ {7, 13}`), valid because `MIN = min T`. `closure_ok`/`forced_ok` are valid under "unknowns `> max S`". The rule "after 7 comes 13" is right: 13 ∈ `T`, and no prime `≡ 1 (mod 3)` lies strictly between 7 and 13 | §3.4 | — |
| R2 | CONFIRMED | `36:292` `last_candidates` | three cases per (last role, assignment) are exhaustive: `|need| ≥ 2` impossible, `|need| = 1` pins `t`, `need = ∅` gives "ordinary ⇒ Case B" or "non-ordinary ⇒ free". Case B up to `10^{2⌊log₁₀B⌋+2} ≥ B²` is exact for `t < B` | §3.4 | — |
| D1 | CONFIRMED | `s3k2/38` | DFS exhaustive: no silent drop. Every `return` without a tally is a valid kill (closure, W-forced, raw `> 18/13`, impossible role, empty exact Case B) | §3.5; outputs `logs/38_*.log` | — |
| D2 | CONFIRMED (test-suite GAP) | `verify_all.py`, `38 … 2,yes,1,4,1 2` | the DFS run with `Lmax = 2` covers `36`'s only exception on `2,yes,1,4,1`. This holds because `run()` has no level-3 exception, not because `verify_all` checks it | §3.10, `d2_exceptions_levels12.py` | no |
| N1 | CONFIRMED | `s3k2/40` | the count covers the only coupled branch the DFS reaches: `K = {7: n, 13: s}`, `W = 11`, two ordinary unknowns (`logs/38_2yes141_L2.log`: the Vieta bound appears only for `S = [7,13]`, `W n=11`, and in no other DFS run) | — | — |
| P1 | CONFIRMED | `NOTES` §5b, `tailY` | tail lemma (Rankin) and its conversion `log f(x) ≤ M^{−1/2}(1+O(M^{−1/2}))` for `M > 10²⁴` | proved here, §3.3 | — |
| P2 | CONFIRMED | role minima | special in `T`: `p ≡ 1 (mod 12)`, min `1+1/p`; in `W`: `p ≡ 5 (mod 12)`; notable min `σ(t⁴)/t⁴`; ordinary exactly `f(t)` | §3.1 | — |
| F1 | GAP (robustness, harmless here) | `36:67` `_fac` (also `34`, `35`) | trial division stops at `10⁸`, so `Fset(t)` is exact only when `t² + t + 1` has at most one prime factor `> 10⁸`. In every use either `t < 10⁸` (so exact), or `(t²+t+1)/3` is `S`-smooth (Case B, so exact), or a composite cofactor only makes closure *fail* where the truth also fails | §3.4 | no |
| F2 | GAP (rigour, negligible) | `36` `threshold_k`, `corrk` | floating point in the cutoff. The slack from `1.01` (G2 shows the true factor is `< 1`) exceeds float error by `≥ 10⁹` for every `B ≤ 5·10⁸`; larger `B` is sent to exceptions anyway | — | no |
| X1 | observation | `verify_all.py` | `verify_all` checks reproducibility, not soundness. Every mutation that *prunes* (e.g. `corr_1`) can only remove sets, so it can never produce an `ALIVE` set; it is caught only by regression counts. Several such mutations are silent (§4) | §4 | no |

### 2.3 Part D — headline numbers reproduced

| figure (NOTES §14d–14h) | reproduced value | source |
|---|---|---|
| 34 level counts 2/3/4/5 | 59 / 1 372 / 31 925 / 488 860; exceptions `{7,13,19,31}`, `{7,13,31,79}`, `{7,13,31,307}` | `verify_all full` PASS; `wc -l s3k2/out34_level*.txt` |
| 35 level-5 tally | closure 485 179, narrowing 3 676, conditional 5 (the five §10b sets), alive 0 | `logs/35.log` |
| 38 on `2,yes,2,5,0` | the two §14f sets `{7,13,19,31,127}`, `{7,13,19,31,331}` conditional; `{7,13,31,79}`, `{7,13,31,307}` empty | `logs/38_2yes250.log` |
| seven α=2 residual sets | 5 (35) + 2 (38) = the seven of §14f | above |
| 36 tallies, six fast profiles | exactly the §14e table | `logs/36_*.log`, `compare_tally.py` |
| 36 tally `2,yes,1,4,1` | RESULT_TALLY | `logs/36_2yes141.log` |
| complete `Sm(T)` lists | all 13 sets and 5 Case-B sets as in §14h | `logs/39_residual.log` and my solver |
| `verify_all.py full` | RESULT_VERIFY | `logs/verify_all_full.log` |

---

## 3. Proofs and details behind the findings

### 3.1 Profiles (A1), re-derived from the definitions

* `v₃(σ(N)) = v₃(N) = 2` and `σ(3²) = 13`, so the other components spend exactly 2.
* Ordinary `x ≠ 3`: `v₃(x²+x+1) = 1` if `x ≡ 1 (mod 3)` (because `x = 1+3j` gives
  `3 + 9j + 9j²`), else 0.
* A notable `n ≡ 1 (mod 3)` spends `v₃(q+1)` (LTE). A notable `n ≡ 2 (mod 3)` with
  `q` even gives `σ ≡ 1 (mod 3)`, so it spends 0.
* The special `p ≡ 1 (mod 3)` spends `v₃(e+1)`. The special `p ≡ 2 (mod 3)` spends
  `v₃(p+1) + v₃(e+1) ≥ 1`, because `e+1` is even and `p² ≡ 1 (mod 3)`.
* Hence `α + s̄ ≤ 2`, with `s̄ = [special ∈ W]`.

Now enumerate. `s = [special ∈ T] ∈ {0,1}`, `m = #notables in T ∈ {0,1,2}`, and
`α ∈ {0,1,2}` with `α ≤ 1 + s`. Also `13 ∈ T`, so `τ = α + s + m ≥ 1`.

* `s = 1` gives 9 profiles.
* `s = 0` gives 6, minus `(α, m) = (0, 0)` (where `τ = 0`), so 5.
* Total **14**, exactly the list of §13c.

None is wrongly excluded: the only exclusions are `α = 2 ∧ special ∈ W` (budget)
and `τ = 0` (13 ∈ `T`).

The prime divisors of `N` are the disjoint union `{3} ∪ T ∪ W ∪ U`:

* the three big components are distinct primes;
* `W` holds the `3 − β` of them that are `≡ 2 (mod 3)`;
* `N` is odd, so `2 ∉ U`.

So `ω(N) = 1 + (α+β) + (3−β) + |U| = 4 + α + |U|`, and Nielsen gives
`|U| ≥ 6 − α`.

Special in `T`: `p ≡ 1 (mod 4)` and `≡ 1 (mod 3)`, so `p ≡ 1 (mod 12)`. In `W`:
`p ≡ 5 (mod 12)`.

### 3.2 The `k`-prime cutoff lemma (A2, G1), stated and proved

**Setting.**

* Fix a profile, a `W` configuration `c`, and `S` equal to the `|S|` smallest
  elements of `T`.
* Let `R = T ∖ S`, with `|R| = k`, and suppose every `r ∈ R` is `≥ B`.
* Let `ρ` be the true role assignment. Its restriction to `S` is one of those over
  which `LO_raw(S)` and `HI(S)` are the min and max.

Then `X := PROD_T(S)·PROD_W ∈ [LO_raw(S), HI(S))`. The upper end is strict because
every profile has a non-ordinary role in `T`.

**Cap.** For `x ∈ U`, `f(x) ≤ PROD_U = (18/13)/(X·PROD_T(R)) ≤ (18/13)/LO_raw(S)`.
So `U ∩ Sm(S)` lies inside the set used to form `H₀(S)`, and
`PROD_{U∩Sm(S)} f ≤ H₀(S)`. The tail term covers the members with `M > 10²⁴`
(§3.3). **Only `LO_raw` enters here, and `LO_raw(S)` is a valid lower bound for
`X` for every such `T`.**

**New members.** Each `x ∈ U ∖ Sm(S)` has `M = x²+x+1` divisible by some `r ∈ R`,
so `M ≥ B`. Then:

* `log f(x) ≤ 1/(√M − 1)`, since `log f(x)·(√M−1) < 1` for all `x ≥ 2`
  (`a2_corr_factor_check.py`, and analytic for `x ≥ 100`);
* `1/(√M − 1) = (1 + 1/(√M−1))·M^{−1/2} ≤ (1 + 1/(√B−1))·M^{−1/2}`;
* distinct `x` give distinct `M`, and every such `M` is `T`-smooth with a
  nontrivial `R`-part, so
  `Σ M^{−1/2} ≤ E(S)·(∏_R (1−r^{−1/2})^{−1} − 1) ≤ E(S)·((1−B^{−1/2})^{−k} − 1)`.

**`R`-factors.** Each is `< r/(r−1) ≤ B/(B−1)` in any role.

**Conclusion.** `Y < H₀(S)·corr_k(B,S)`, with `corr_k` as coded in `36:163` (with
`1.01`, which is slack). So `X > (18/13)/(H₀(S)·corr_k)`.

**Kill.** If `(18/13)/(H₀·HI) ≥ corr_k`, then `X > HI(S)`, a contradiction.

**Equivalence with the code.** The code computes `margin = LO_n/HI`, with
`LO_n = max(LO_raw, (18/13)/Hup₀)`, because the loop is one step (§3.3).

* If `margin ≥ corr_k > 1`, then `LO_n > HI ≥ LO_raw`.
* So `LO_n = (18/13)/Hup₀`, and `margin ≥ corr_k` is exactly the condition above.
* `corr_k` is decreasing in `B`, so every `t ≥ B` is also killed.

∎

**Answers to the brief's questions.**

* **Is `LO(S) ≤ LO(T)` legitimate?** Yes for the raw minimum.
* **Which `LO`?** The raw one for any lower bound on a superset. The narrowed
  `LO_n(S)` is **not** a lower bound for `T ⊋ S`, because `Sm(T) ⊋ Sm(S)` and the
  `R`-factors enlarge `Y`. For `S = {7,13,19,31}` and `T = S ∪ {127}`, `107` enters
  `Sm(T)`.
* **Is narrowing on `S` legitimate for `T ⊋ S`?** Only its cap step, which uses
  `LO_raw`. The kill uses narrowing correctly **because** it compares with `corr_k`.

### 3.3 Narrowing is one step (G3); the tail (P1)

In the loop, `LO₁ = (18/13)/Hup₀`, so the new cap is `R₁ = (18/13)/LO₁ = Hup₀`.

* Every `x` admitted at step 0 has `f(x) ≤ H₀ ≤ Hup₀`, because `H₀` is a product
  of factors `≥ 1` that includes `f(x)`. So it stays admitted.
* Every `x` rejected at step 0 had `f(x) > R₀ > R₁`. So it stays rejected.
* Hence step 2 reproduces step 1 and the loop exits. §5⅔'s "one iterates" performs
  no second exclusion.

This is also why mutation C2 (§4) is silent.

**Tail.** For `M > Y` we have `1 ≤ (M/Y)^ε`, so
`Σ_{M>Y} M^{−1/2} ≤ Y^{−ε} Σ M^{ε−1/2} = Y^{−ε} ∏(1 − t^{ε−1/2})^{−1}`.
The code also:

* divides by `1 − Y^{−1/2}`;
* multiplies by `1.000001`;
* rounds `H` up by `10⁻¹²`.

Each of these dominates the corresponding error (`M > 10²⁴`).

### 3.4 `s3k2/36` (R1, R2, F1)

**Seeds and ordering.** Seeds `(7,)`, `(13,)`. From `(7,)` the only next element
is 13 (lines 364–367). Every later level appends a prime `> max S`. So `S` is always
the `|S|` smallest elements of `T`, and `MIN = S[0] = min T`.

**`admissible(t,k,MIN)`.** It rejects `k` if a prime `q ≡ 1 (mod 3)` with `q < MIN`
divides `σ(t^k)`. Such a `q` would lie in `T` below its minimum. With `MIN ∈ {7,13}`
only `q = 7` is ever tested.

The search stops at `k < 120`. It returns `None` only when no exponent is
admissible at all:

* for `'s'`, `k = 1` is admissible unless `t ≡ −1 (mod 7)`, and then every odd `k`
  is inadmissible;
* for `'n'`, `k = 4` is always admissible.

So the cap at 120 loses nothing.

**Budget.** `b3 = 2 − α − cost(W)`, with the special in `W` costed at `v₃(w+1)`
(ignoring `v₃(e+1)`), or at 1 when generic. The true budget is tighter, so this
only lowers minima.

**`W` configurations.**

* Explicit `w < 500`:
  * notable: `[σ(w^{q₀})/w^{q₀}, w/(w−1))`;
  * special `e = 1`: exactly `(w+1)/w`, forced primes of `w+1` in `T`;
  * special `e ≥ 5`: forced primes dropped, a relaxation.
* Generic `w ≥ 500`: `[1, 500/499)`. This covers every `w ≥ 500` because
  `w/(w−1) ≤ 500/499`.
* Explicit `w` is removed from `Sm(S)`; a generic one is not (conservative).

**`closure_ok` / `forced_ok`.**

* An `f ∈ F(t)` with `f < max S`, `f ∉ S` is impossible.
* The number of new primes must be at most `τ − |S|`.
* Both conditions are valid for upward supersets.

**Raw kill.** See K2.

**`last_candidates`.** For each role `ρ` of the last prime, and each assignment of
the remaining roles to `S` that passes `min_factor` and closure, let
`need = ⋃_{ordinary s∈S} F(s) ∖ S`. Then:

* `|need| ≥ 2` is impossible (one slot).
* `need = {t}` pins `t`. If `t` is ordinary, it also needs `F(t) ⊆ S`.
* `need = ∅` leaves two cases:
  * `ρ = 'o'`: `F(t) ⊆ S` ⇔ `(t²+t+1)/3` is `S`-smooth (`v₃ = 1` for
    `t ≡ 1 mod 3`, and `t ∤ t²+t+1`). Enumerating `S`-smooth `m ≤ 10^{2⌊log₁₀B⌋+2}`
    and testing `12m − 3 = □` is exact for `t < B`, because
    `(t²+t+1)/3 < B² ≤ 10^{2⌊log₁₀B⌋+2}`. Larger `t` are killed by the per-split
    cutoff.
  * `ρ ∈ {'s','n'}`: the per-split cutoff with `k = 1`.
* Flags are OR-ed over assignments, which is conservative.
* `W`-forced primes are ignored here but enforced at level `τ` by `forced_ok`
  (conservative).
* Candidates are then filtered by the overall `B_f`, which is valid.

**`_fac` (F1).** Trial division runs to `10⁸`. Ordinary primes whose `F` is used
are `< 10⁸` (the largest level prime is `319 057`), or come from Case B, where
`t²+t+1 = 3·(S-smooth)` is fully factored.

**Final test.** K4 then K5, with `need = 6 − α` and `keep` excluding explicit `w`.

### 3.5 `s3k2/38` (D1)

**Invariant.** `T = K ∪ {unknowns}`, every unknown is `> lb`, and every prime of `T`
that is `≤ lb` is in `K`. It holds at each step:

* **Start:** `K = S` with its roles, `lb = max S`.
* **Pinning:** a forced `f ∉ K` must be an unknown, so `f > lb`. `lb` is kept.
* **Cutoff:** if `(18/13)/(H₀(K)·HI(K)) ≥ corr_u(B, K)` then the smallest unknown is
  `< B`. It is enumerated, and `lb` is set to it. §3.2 applies with `S := K`,
  because the lemma never used "`S` = smallest elements", only `R ≥ B`.
* **Exact Case B** (`u = 1`, ordinary, `B < 10¹⁵⁰`): as in §3.4.
* **`u = 2`, both ordinary:** either some unknown has `F ⊆ K` (Case B, conditional,
  passed to `39`), or `a′ ∈ F(a)` and `a ∈ F(a′)` (coupled, passed to `40`).
* Anything else is `unresolved` and printed.

Every silent `return` is a valid kill.

### 3.6 Matveev applied (M1–M4), from the page images only

1. **Linear form.**
   * `z = x − ω = ε λ^δ ∏ ρ_t^{c_t}` with `ρ_t ∈ {π_t, π̄_t}`. Both cannot divide `z`,
     since `t ∤ z` (its `ω`-coefficient is `−1`).
   * So `z/z̄ = ζ ∏ (π_t/π̄_t)^{b_t}`, with `b_t = ±c_t` and `ζ ∈ μ₆`
     (`λ/λ̄ = −ω`).
   * `Λ := Log(z/z̄) = b₀·(iπ/3) + Σ b_t·iθ_t`, with principal `θ_t` and `b₀ ∈ ℤ`.
   * `Λ ≠ 0`, because `Im z = −√3/2`.
2. **Size.** `Λ = 2i·arg z` and `Re z = x + ½ > 0`, so
   `|Λ| ≤ π|sin arg z| = π√3/(2|z|) < 2√3/|z|` for all `x ≥ 0`.
3. **Kummer (1.5, `p82.png`).**
   * Any product of `α`'s that contains some `π_t/π̄_t` has odd `π_t`-valuation.
   * `ζ₆` is not a square: `μ(K) = μ₆`, whose squares form `μ₃`.
   * `μ₂ ⊂ K`, so Kummer theory gives degree `2ⁿ`.
   * Note that `ω` itself **would fail** (`ω = (ω²)²`). The repo correctly uses
     `ζ₆`.
4. **`D = 1`.** `D_K = 2` and `κ = 2`. **`ρ = 1`**: `rank_ℝ` (I checked the glyph on
   an enlarged crop of `p85.png`), and all logs are in `iℝ`.
5. **Height.** `h(π_t/π̄_t) = ½ log t`: the minimal polynomial
   `tX² − Tr(π_t²)X + t` is primitive and has roots on the unit circle.
6. **Parameters.** (2.1) holds since `A_j ≥ h(α_j)`. (2.2) holds since
   `A_j ≥ |ln α_j|/D`. (2.3) holds with `C₃* = n/ρ`, since `(n/ρ)(e/2) ≥ 1`.
7. **`|b₀|`.** `|b₀|π/3 ≤ |Λ| + π·Σ|b_t|`.
8. **`b_n ≠ 0`.** Put last an `α_t` with `c_t ≠ 0`, and take the worst `A_n`.

My initial bounds (`a3_matveev_bound.py`):

| `T` | mine `H ≤` | repo `H ≤` |
|---|---|---|
| `{7,13}` | `8.45·10¹⁰` | `9.32·10¹⁰` |
| `{7,13,19}` | `2.18·10¹²` | `2.42·10¹²` |
| `{7,13,19,127}` | `8.64·10¹³` | `9.73·10¹³` |
| `{7,13,19,31,127}` | `2.18·10¹⁵` | `2.45·10¹⁵` |

`Ω` and `ω` agree with the repo's printed `ω` (`31.76`, `51.75`, `123.0`, `192.4`).

### 3.7 `39` lattice step (L1)

For `v ≠ 0` with `Σe_t² ≤ kX² = S` we have `φ̃² ≥ ℓ² − S`, and
`|Cφ − φ̃| ≤ T₀ = (Σ|e_t| + |b₀|)/2` (precision `10⁻⁶⁰⁰`, with `C ≤ 10¹²²`), so
`C|φ| ≥ √(ℓ²−S) − T₀`. `ℓ ≥ min|b*_i|` holds for any basis: take the last nonzero
coordinate. The `det` check certifies that `R` is a basis, because its rows lie in
`Γ` (integer row operations).

`v = 0` means `x²+x+1 = 3^δ`, so `L < ln 12`. Rounds only ever shrink the bound. A
failed first round raises an exception.

### 3.8 `32` Skolem (S1)

* `X = M^L − I ≡ 0 (mod ℓ)`, and `Λ = log(I+X) = X − X²/2 + …`.
  * `v(X^k/k) ≥ k − v_ℓ(k) ≥ 2` for `k ≥ 2`, `ℓ ≥ 3`, so `Λ ≡ X (mod ℓ²)`.
  * The linear coefficient is `≡ B_{c₀+L} − B_{c₀} (mod ℓ²)`.
  * The `k`-th coefficient has `v ≥ k − (k−1)/(ℓ−1) ≥ (3k+1)/4 > 1` for `ℓ ≥ 5`.
* Strassmann then gives "empty" or "at most one".
* A class mod `Mod` is settled by an `ℓ` with `L | Mod` whose class is empty, or
  unique and containing a known solution. Otherwise the solver reports failure (it
  refuses the hidden `x = 18`).
* The forms are complete: `D` is squarefree with one conjugate choice per prime, 6
  units, and `π` or `π̄`.

### 3.9 `31` Vieta (V1)

The minimal solution has `x = y`, which forces `x = 1`, `k = 5`. For `k = 5`,
`y ≥ x+2`, so `y′ ≤ x`, a strict descent to `(1,1)`.

* **Step 2.** `y = 1` by size; `v = 1, 2, ≥ 3` are excluded by the ratio lemma
  applied at indices `n−1, n, n+1 ≥ 3`.
* **Ratio lemma.** Base `a₄/a₃ = 61/13 > 4.6`. The induction uses
  `a_{m−1} < a_m/4.6` from `m = 4` on, so it does **not** need `a₂/…`.

### 3.10 Coverage of `36`'s exceptions by the DFS runs (D2)

`verify_all.py` checks the DFS for `2,yes,1,4,1` only on exceptions through
**level 2** (`38_closure_dfs.py 2,yes,1,4,1 2`). The DFS's own
`exceptions_upto` uses the plain cutoff and no raw-minimum kill, so on levels
`≤ τ − 1` it covers a superset of `run()`'s exceptions. But `run()` can also raise
exceptions at level `τ − 1 = 3`, inside `last_candidates`, and a level-2 DFS would
not see those.

**Check.** `d2_exceptions_levels12.py` replays `run()`'s levels 1–2. It finds
exactly one exception, `S = (7,13)`, `W = n=11`, at level 2, with margin
`0.995927`, and `340 091` level-3 sets (the §14e figure). `run()`'s total is 1
(RESULT_D2). So level 3 contributes none, and the one exception is among the six
the DFS resolves. The DFS disposes of it (`nocfg 4`, `logs/38_2yes141_L2.log`)
using only:

* Case B `{7,13}` to `10³⁰⁰`, which `39` settles (no `t`);
* Vieta pairs, which `40` settles.

For the other profiles:

* `1,yes,1,3,1` has 0 `run()` exceptions; its DFS run is a redundant cross-check.
* `2,yes,2,5,0`'s three level-4 exceptions are all resolved (`logs/38_2yes250.log`),
  giving the two §14f sets.

**Recommendation.** `verify_all` should assert that every exception printed by
`36` appears among the DFS inputs, rather than rely on the level cut-off matching.

---

## 4. Part A comparisons (mine next to the repo's)

| item | independent value (this audit) | repo | agree? |
|---|---|---|---|
| number of profiles | 14; list in §3.1 | 14 (§13c) | yes |
| `ω(N)` | `4 + α + |U|`, `|U| ≥ 6−α` | same | yes |
| margin `{7}`, `{13}` (profile `o,o,s,n,n`) | 1.186813, 1.278107, from scratch | 1.186813, 1.278107 | yes |
| cutoff `B` for `{7}`(k=4), `{13}`(4), `{7,13}`(3), `{7,13,19}`(2) | 1751.0, 711.7, 5969.4, 27720.5 (with `1.01`); 1720, 700, 5857, 27185 (the sharp factor of G2) | 1751, 712, 5970, 27 723 | yes (bisection tolerance) |
| same with `k = 1` (the §14d error) | 139.5, 63.4, 727.3, 7081.3 | 139.5, 63.4, 727.4, 7081 | yes |
| Matveev `H`, `T = {7,13,19}` | `2.18·10¹²` | `2.42·10¹²` | repo more conservative |
| Matveev `ω` for the four sets | 31.76, 51.75, 123.0, 192.4 | 31.76, 51.75, 123.0, 192.4 | yes |
| remark after (2.16), LHS/RHS | 2.06 (n=2) … 3.09 (n=8) … 3.23 (n=10), same for ρ = 1, 2 | "2.06 … 3.09" | yes |
| `{7,13}`: all `x ≥ 0` | 0, 2, 3, 9, 18 | 0, 2, 3, 9, 18 | yes |
| `{7,13,19,127}`: all `x ≥ 0` | 0, 2, 3, 9, 11, 18, 30, 68, 107, 146, 653 (11) | 11 solution pairs; `Sm = {11,107,653}` | yes |
| `{7,13,19,31,127}`: all `x ≥ 0` | 0, 2, 3, 5, 9, 11, 18, 30, 68, 87, 107, 146, 191, 273, 315, 653 (16) | 16 pairs; `Sm = {5,11,107,191,653}` | yes |
| all 13 named `Sm(T)`, all 5 Case-B sets | `logs/a4_all_residual.log` | §14h table | **all 18 agree** |
| the 8 single-exponent equations of `33` | `logs/a4_check33.log` | §14b table | all 8 agree |
| α=2 sets with `|Sm| ≥ 4`: admissible under `R(T)` | `{…,409}`: 53,107,653; `{…,1723}`: 41,107,653; `{…,31,127}`: 191,653; `{…,31,331}`: 191,653 | same (§10b, §14f) | yes, all `< 4` |
| ×`10⁶` on Matveev | my code: identical lists (4 sets); repo code: identical final bounds and answers for all 18 statements | claimed for 3 sets | yes |

**How my solver differs** (`a4_solver.py`). It uses:

* the unknown `L = ln(x²+x+1)`, with weights `≈ ln t`;
* exact rational LLL;
* **complete Fincke–Pohst enumeration** of an ellipsoid that provably contains
  every solution with `L_min ≤ L ≤ L_cur` (no shortest-vector lemma);
* a final enumeration of exponent vectors with `Σ c_t ln t ≤ L_final`, testing
  `4N − 3 = □` (no search in `x`).

`a4_selftest.py` forces small `C` and checks that every known solution in range is
enumerated (PASS). Every set also agrees with brute force for `x < 10⁶`. Final
proved bounds are `L ≤ 27.5`, `44.9` and `54.0` for the three sets, against the
repo's 61.2, 121.2 and 152.7. The method differs; the lists are the same.

---

## 5. Mutation tests (Part C)

`mutate.py` applies one exact textual patch to a copy of `s3k2/` and refuses a
patch that does not match exactly once. `run_mutants.sh` runs the batch. Tallies
are `(raw, uncond, cond, nocfg, ALIVE, exc, caseB)`; logs are
`logs/mut_<name>__*.log`.

| mutation | effect | caught by | silent? why |
|---|---|---|---|
| **C1** `corr_k → corr_1` in `36` | `36 validate` asserts (levels ≠ 34's). `0,yes,2,3,0`: uncond 80→77, nocfg 17→14. `1,yes,2,4,0`: 618→617. `1,no,2,3,1` and `1,yes,1,3,1`: level-2 counts fall (1632→503, 1972→603), final tallies unchanged. **No ALIVE** | verify_all: `36 validate` and two tallies | silent on `0,no,2,2,1`, `0,yes,1,2,1`: `τ = 2`, so `k = 1` anyway (legitimate). Silent in the tallies of two more profiles |
| **C2** narrowed `LO` used for the raw-minimum kill | identical output on all six fast profiles | nothing | **legitimately silent**: narrowed `LO > 18/13` ⟺ raw `LO > 18/13`, and then they are equal (the loop admits nothing and `Hup ≥ 1`) |
| **C3** `θ₁₃ += 10⁻³⁰` in `39` | `validate`: V1 fails (residual `2·10⁻³⁰`). `residual`: **every list unchanged**; final bounds shift (e.g. 152.3→153.1) | verify_all: `39 validate` | `residual` alone would miss it: the true solutions are tiny, so a lattice built on a wrong `θ` still returns the right lists. Only V1 guards the *proof*. |
| **C4** drop one role split in `last_candidates` | drop `'o'`: `1,no,2,3,1` 4249→4247, `1,yes,2,4,0` 618→613, `1,yes,1,3,1` caseB 1→0. Drop `'s'`: `1,yes,1,3,1` 4349→3653, `1,yes,2,4,0` nocfg 9→0. Drop `'n'`: `1,no,2,3,1` collapses (uncond 2) | tallies | drop `'n'` is **silent on `1,yes,1,3,1` and `1,yes,2,4,0`**: there the `'n'` split's candidates are a subset of the `'s'` split's (both "free", same `S`). That redundancy is data-dependent, not structural. |
| **C5** Matveev `112 → 11.2` | `validate` passes; `residual` final bounds and answers identical; round-0 bounds ~10× lower | nothing | **legitimately silent**: the reduction depends on the initial bound logarithmically. Also silent at ×`10⁶` (C5b). No check could detect a factor-10 error in this constant, and none is needed. |
| extra: exact Case B only to `B` (not `B²`) | `1,no,2,3,1` 4249→4247; `1,yes,2,4,0` 618→615 | tallies | silent on `1,yes,1,3,1` |
| extra: drop generic notable `w ≥ 500` | `0,yes,1,2,1` 260→257; `1,yes,1,3,1` 4349→4340 | tallies | no-op where `W` is special or empty |
| extra: `HI` without `HIW` | large changes | tallies | — |
| extra: remove the Vieta enumeration from `38` | identical output | nothing | **legitimately silent**: the enumeration to index 1500 never yields a candidate. The branch is closed by `40`, which does not use it. |

**General observation (X1).** Every mutation that makes the argument
**unsound by over-pruning** (C1, C4, Case B to `B`, dropping a `W` config) can only
*remove* sets, so it can never produce `ALIVE`. Such errors are caught only by
regression counts, and those counts were produced by the same code. So
`verify_all` detects **drift**, not **unsoundness**. The soundness of the
recursion rests on the proofs in §3.2–3.5, not on the test suite.

---

## 6. What I did not check, and why

* **The transcription `MATVEEV_1998.md` against `sources/`.** Excluded by the
  brief. I read the pages myself for A3; my reading of (1.5), the §2 setting,
  (2.1)–(2.5) and (2.13)–(2.16) agrees with the transcription.
* **Matveev's Theorem 2.2 and Nielsen's `ω(N) ≥ 10`.** Cited theorems, not
  re-proved.
* **Matveev pp. 81, 83–84.** They are not in `sources/`. If the paper places
  further standing hypotheses there, I have not seen them. The ones visible on
  p. 85 (Kummer, `n ≥ 2`, `b_n ≠ 0`, arbitrary log values) are all satisfied,
  and so is `Λ ≠ 0`.
* **An independent re-implementation of the `36`/`34` recursion.** I reviewed the
  code line by line, recomputed margins and thresholds for four sets, re-derived
  the final count kills for the four hardest `α = 2` sets independently
  (`a4_all_residual.py`), and ran twelve mutations. I did not regenerate the level
  lists (59 / 1 372 / 31 925 / 488 860) or the `2,yes,1,4,1` tally with separate
  code.
* **Floating point in `threshold_k`/`corrk`.** Argued negligible (F2), not made
  rigorous with interval arithmetic.
* **`isprime` above `3.3·10²⁴`.** Miller–Rabin with fixed bases is then
  probabilistic. A composite passing as prime can only add a spurious member or
  candidate, which is conservative; a prime is never rejected.
* **`s3k2/37`** (a cross-check only) and **scripts 01–30**. None of them is in the
  final chain. §11b's three-line argument was checked by hand.
