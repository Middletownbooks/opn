# Audit of *Certified Minimal-Prime Branch Closures for Odd Perfect Numbers*

Target: Marco Mantovanelli, release `C-small-2026-07`, repository
`Mantovanelli1110/opn-small-prime-closure-certificates`, commit
`4f59cde9ca5b0562565109ff562130770ba92b7c` (the tag and `HEAD` coincide).

Everything below was obtained by reading the released `.tex` sources and JSONL
bundles, executing the released verifiers, and mutating the bundles. Scripts to
reproduce every number are in `audit/`.

---

## 0. Verdict

**Category C — substantive gap**, but with a sharper diagnosis than "a premise
is unproved".

The five branch closures all terminate in applications of the paper's
Tail Envelope Lemma (Lemma 7.4). That lemma is a *correct implication*. Its
hypotheses are supplied by `tail_count_certificate(B, M)` records with
`B = 59`, `M = 18`, whose stated obligations (Definition 7.5) are:

> (i) every unresolved support prime not already represented in the envelope
> tuple is at least `B`; (ii) at most `M` such further support-prime slots
> remain.

The decisive finding is not that (i) and (ii) are unproved. It is that

> **the verifier's acceptance test is logically equivalent to the negation of
> the obligation it is supposed to discharge.**

A tail record is accepted exactly when `H(K_env)·(B/(B−1))^M < 2`. But for any
odd perfect number actually satisfying (i) and (ii), that same quantity is
necessarily **greater** than 2 (Proposition A below, one line from abundancy).
Acceptance and validity are mutually exclusive. So every accepted tail record
in `C_small` asserts something that can be true only if the branch it is
closing is already empty — which is the theorem.

Consequently obligation (ii) is not an auxiliary finite fact awaiting a
certificate. For `q = 17` it is *logically equivalent to the conclusion*, and
no repair of the certificate format can fix this. This is a stronger result
than the adversarial audit reached, and it confirms that audit's central
criticism.

---

## 1. Proposition A (the no-go), and what it kills

**Proposition A.** Let `N` be an odd perfect number with prime support `S`.
Suppose an envelope tuple `K_env = (k_1,…,k_t)` accounts for `t` slots of `S`
(each `k_i` a prime of `S` or a certified lower bound for one), every remaining
prime of `S` is `≥ B`, and at most `M` remain. Then

```
H(K_env) · (B/(B−1))^M  >  2 ,      where H(t) = Π k/(k−1).
```

*Proof.* `σ(N)/N = Π_{p∈S} (1−p^{−(e_p+1)})/(1−p^{−1}) < Π_{p∈S} p/(p−1) = H(S)`,
and `σ(N)/N = 2`, so `H(S) > 2`. Since `x/(x−1)` is decreasing, each envelope
slot over-estimates its prime's factor, and each of the `≤ M` tail primes
contributes at most `B/(B−1)`; hence `H(S) ≤ H(K_env)(B/(B−1))^M`. ∎

**Corollary B.** The tail-envelope inequality `H(K_env)(B/(B−1))^M < 2` is
never satisfiable by data satisfying (i) and (ii). Lemma 7.4 is therefore valid
but vacuous: it can only ever fire on records whose semantic obligations fail.

This is not an abstract worry. I enumerated **every** tail record the five
released verifiers evaluate and compared its `M` against the least `M` that
`σ(N) = 2N` permits for that kernel (`audit/04`). Result: **32 of 32 accepted
tail records have `M` strictly below that minimum** — exactly as Corollary B
requires. Representative rows:

| record | `K_env` | `B` | `M` in cert | `H·(B/(B−1))^M` | least `M` compatible with `σ(N)=2N` | shortfall |
|---|---|---|---|---|---|---|
| `q17_strict_tail_n1` | (17,103) | 59 | 18 | 1.4595 | 37 | −19 |
| `q17_strict_tail_e2` | (17,19)  | 59 | 18 | 1.5256 | 34 | −16 |
| `q17_e2_phi2_pure…`  | (17,577) | 59 | 18 | 1.4478 | 37 | −19 |
| `q13_strict_tail_n1` | (13,53)  | 59 | 18 | 1.5020 | 35 | −17 |
| `q13_e2_phi2_pure…`  | (13,337) | 59 | 18 | 1.4780 | 36 | −18 |
| `q11_strict_tail_n1` | (11,23)  | 59 | 18 | 1.5643 | 33 | −15 |
| `q11_e2_phi2_pure…`  | (11,241) | 59 | 18 | 1.5026 | 35 | −17 |
| `q7_strict_tail_n1`  | (7,29,29)| 59 | 18 | 1.7024 | 28 | −10 |
| `q7_strict_tail_e2` [pure] | (7,13) | 59 | 18 | 1.7193 | 27 | −9 |
| `q5e1_pi_ge_1381_…`  | (5,1381,11) | 59 | 18 | 1.8718 | 22 | −4 |
| `q5e2_pure_c2_…`     | (5,1249) | 59 | 18 | 1.7017 | 28 | −10 |

(The `q = 7` forced rows use the repeated-slot envelope tuples of
Definition 7.3, e.g. `(7,29,29)`, which are hardcoded in
`cert_verifier_q7_strict.py` rather than carried in the bundle.)

All five branches are affected, `q = 5` included.

---

## 2. An independent, elementary refutation of `M = 18`

Proposition A is enough, but a second, fully independent route confirms it and
quantifies the error.

**Proposition C (minimal-prime support floor).** If `N` is odd perfect and
`q = min{p : p | N}`, then `ω(N) ≥ k₀(q)`, where `k₀(q)` is the least `k` with
`Π p_i/(p_i−1) > 2` over the `k` smallest primes `p_i ≥ q`.

Exact values (`audit/03`, exact rational arithmetic):

| q | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|---|
| `k₀(q)` | 3 | 7 | 15 | **27** | **41** | **62** | 85 | 115 |

The method is classical (Norton-type); `k₀(11) = 27` reproduces exactly the
literature bound the paper itself cites in Corollary 4.4 for `3,5,7 ∤ N`, which
is good evidence the reconstruction is faithful.

Now compare with what the certificates assert. A record with envelope tuple of
size `t` and `M = 18` asserts `ω(N) ≤ t + 18`:

| branch | asserted `ω(N) ≤` | floor `k₀(q)` | paper's own Cor. 4.4 | consistent? |
|---|---|---|---|---|
| q=11 | 20 | 27 | ≥ 27 | **no** |
| q=13 | 20 | 41 | ≥ 27 | **no** |
| q=17 | 20 | **62** | ≥ 27 | **no** |

For `q ∈ {11,13,17}` the tail-count assertion contradicts **a corollary the
paper proves and relies on four sections earlier**. For `q = 17` the true
floor is 62, so `M` would have to be at least 60, and
`H({17,103})·(59/58)^60 = 2.9923 > 2` — the inequality fails by a wide margin.

Stated carefully: "every odd perfect number with `min p = 17` has `ω(N) ≤ 20`"
is, given `k₀(17) = 62`, *equivalent to* "there is no odd perfect number with
`min p = 17`". That is the circularity, exactly.

---

## 3. Certificate-contract dependency table (q = 17)

`q17_master_bundle.jsonl` is 7 records, 2.4 KB. This is the whole q=17 closure.

| Claim / data | Mathematical source | Encoded where | Checked by verifier? | Independently derived? | Remaining trust |
|---|---|---|---|---|---|
| Valuation balance `e_q = Σ v_q(σ(p^{e_p}))` | Lemma 3.1, proved | — | n/a | yes, re-derived | none |
| Cyclotomic input condition | Lemma 3.2, proved | — | n/a | yes | none |
| Lower-prime avoidance for `ℓ < q` | Lemma 4.2, proved | `lower_prime_avoidance: [3,5,7,11,13]` | **string-literal equality only** | yes (trivial from minimality) | none |
| Allowed first-input orders (N₁,E₁,E₂) | Lemma 6.3, proved | leaf labels | label presence only | yes | none |
| Coverage split completeness | Prop. 6.4 | `coverage_reference: "cor:q17-first-input-coverage"` | literal string compare | — | **label does not exist in either `.tex`** |
| `103` = least prime `>17`, `≡1 mod 17` | Table 7 | `endpoint_certificate` | primality + congruence of the *listed* candidates | yes, and the claim is **true** | list is incomplete (omits 18); completeness never checked |
| `577` = first prime in `2·17^b−1` | Table 7 | `endpoint_certificate` | `b=1` composite, `577` prime | yes, true | only `b ≤ 2` screened; no argument that `b=1` is the only smaller case needed |
| forced prime `≥ 103` / `≥ 19` | Lemma 5.3 | `forced_prime_lower_bound` | hardcoded `== 103` / `== 19` | plausible, order argument sound | order-2 case rests on "least odd prime >17 is 19" only |
| **(i) all remaining support primes `≥ B = 59`** | **nothing** | `B: 59` | `assert B == 59` | **no** | **total — refuted by Prop. A** |
| **(ii) at most `M = 18` remaining slots** | Def. 7.5 *states the obligation*; nothing discharges it | `M: 18` | `assert M == 18` | **no** | **total — contradicts Cor. 4.4 and Prop. C** |
| tail inequality `< 2` | Lemma 7.4, proved | `endpoint_check` (a string) | recomputed from `B, M, K_base`; **the string is never parsed** | yes, arithmetic correct | arithmetic is fine and irrelevant |
| branch closure | Prop. 7.7 | `conclusion:` `"…exhausted_in_current_formal_certificate_system"` | literal string compare | — | inherits the (i)/(ii) gap |

The paper's own audit table (Table 5) is candid about the shape of this: for
"tail-count data" it says the paper "**states the mathematical obligation**
carried by `B` and `M`" and that Lemma 7.4 "proves the resulting
contradiction". No row claims any lemma *discharges* the obligation. Remark 7.6
goes further and volunteers that `B=59, M=18` "is not inferred from a hidden
global upper bound on `ω(N)`; it is a finite certificate obligation". Proposition A
shows there is no such thing: the obligation is not finite, it is the theorem.

---

## 4. What the verifiers actually do (mutation results, `audit/05`)

| mutation | verdict | what it proves |
|---|---|---|
| unmodified bundle | ACCEPT | baseline reproduces |
| `M: 18 → 36` (inequality still true) | reject | `assert M == 18` — literal, not mathematical |
| `M: 18 → 17` (stronger claim, still true) | reject | same |
| `B: 59 → 19, M → 11` (provable `B`, inequality still true) | reject | the verifier cannot accept a *valid* alternative certificate |
| `endpoint_check` → arithmetic nonsense | **ACCEPT** | the field is decorative; never parsed |
| `endpoint_check` deleted | **ACCEPT** | same |
| `excluded_candidates` → `[18,35,52,69,86]` (**correct, complete**) | reject | verifier rejects the mathematically correct data |
| `excluded_candidates` as released `[35,52,69,86]` (incomplete) | ACCEPT | completeness is never checked |
| `coverage_note` → "coverage is incomplete; leaves omitted" | **ACCEPT** | the coverage *semantics* is free text |
| `coverage_reference` → nonexistent label | reject | but the released value is *also* a nonexistent label |
| delete / duplicate a frontier leaf | reject | inventory bookkeeping does work |
| `lower_prime_avoidance` + `{19,23}` | reject | literal compare |

So the released q=17 verifier is a **transcript matcher**: it confirms that the
bundle contains the constants the script already hardcodes
(`EXPECTED_LEAVES`, `EXPECTED_FORCED`, `B == 59`, `M == 18`,
`excluded == [35,52,69,86]`, `coverage_reference == 'cor:…'`) and recomputes an
arithmetic inequality whose premises it cannot see. It genuinely enforces leaf
presence, uniqueness and non-duplication — real but shallow value. It
establishes **no** mathematical proposition about odd perfect numbers.

The paper says as much in one place ("the `q=17` verifier … is explicitly a
master-wrapper verifier … It should not be read as a standalone general-purpose
arithmetic verifier"), which is accurate and easy to miss.

---

## 5. q = 5 as control

Question posed: does `q=5` have a genuinely stronger independently checkable
chain, or a better-documented version of the same contract?

**Answer: genuinely stronger in the layers that are not load-bearing, and
identical in the layer that is.**

Stronger, and to the author's credit:
- 1228 records vs 7; real recursive child archives and parametric window
  closures.
- The only bundle carrying `H_kernel_num/den`, `tail_bound_num/den`,
  `upper_abundance_bound_num/den`, which `verify_lhs` recomputes and compares.
- `check_phi5_over_5_forced_prime_bound` performs a real derivation, not a
  literal compare. I verified its mathematics independently (`audit/03`):
  if `r | Φ₅(x)` then `ord_r(x) ∈ {1,5}`; `ord_r(x)=1 ⇒ Φ₅(x) ≡ 5 (mod r) ⇒ r=5`;
  so `r ≠ 5 ⇒ ord_r(x)=5 ⇒ r ≡ 1 (mod 5) ⇒ r ≥ 11`. LTE gives
  `v₅(Φ₅(x)) = 1` for `x ≡ 1 mod 5`. Checked with no violations for all 54
  primes `x ≡ 1 mod 5` up to 1381. **This lemma is sound.**

Identical where it matters — `cert_verifier_q5_strict.py:160` and `:202`:

```python
require(B == 59 and M == 18, f"{rid}: expected B=59 and M=18")
```

The same hardcoded literals. Proposition A applies unchanged (row `q=5` of the
table in §1: honest `M ≥ 22`, certificate says 18). The extra documentation
does not touch the gap.

Side note: the paper's Table 5 claims *each* tail record exposes the numerator
and denominator "which the verifier recomputes". That is true only for `q = 5`.
The `q = 7, 11, 13, 17` bundles contain no such fields at all (`audit/06`).

---

## 6. Reproducibility of the frozen release

- Both the tag `C-small-2026-07` and `HEAD` are `4f59cde9…`, so there is no
  later-commit drift to excuse mismatches.
- `sha256sum -c SHA256SUMS.txt` on a fresh Linux checkout: **12 of 22 fail.**
- 7 of those 12 match after CRLF-ifying — the hashes were taken on a
  CRLF working tree while `.gitattributes` declares `* text eol=lf`. A
  documentation defect, not content drift. Note the release is internally
  inconsistent about this: `q17_*` hash as LF, `q7_*`/`q11_*`/`q13_*` as CRLF.
- **5 files match no line-ending variant** — genuine content drift from the
  published hashes: `arxiv_q5_expanded_detail.tex`, `cert_verifier_q5_strict.py`,
  `q11_branch_closure_verifier.py`, `q13_branch_closure_verifier.py`,
  `q5_master_bundle.jsonl`.
- All five advertised verifier commands nevertheless run clean on the checked-out
  files under Python 3.11.15 and print the Table 6 terminal outputs
  (`q=5/7/11/13/17 branch inventory exhausted`; 1228/41/10/10/7 records).

So: *the verifiers accepted the checked-out certificates*. The frozen release
is **not** hash-reproducible as published.

---

## 7. Can it be repaired?

**Not within this framework, and this is provable, not a judgement.**
By Proposition A, no valid `(K_env, B, M)` satisfies the acceptance inequality.
The tail-envelope method therefore cannot close any nonempty branch, for any
parameter values, ever.

The smallest proposition that would repair a single q=17 leaf is an upper bound
`ω(N) ≤ 20` on that branch. No upper bound on `ω(N)` for odd perfect numbers is
known in any form, and by Proposition C such a bound would immediately close
the branch outright, with no tail inequality needed. The "smallest repair" is
the theorem itself.

What survives, and is worth keeping:
- Lemmas 3.1, 3.2 (valuation balance, cyclotomic input condition) — sound.
- Lemma 4.2 lower-prime avoidance and Corollary 4.4 — sound.
- Lemmas 6.2, 6.3 and Proposition 6.4, the first-input coverage split — sound,
  and the `q=17` split into `{N₁, E₁, E₂}` is correct: `17−1 = 2^4` has odd
  divisor 1 only, and `v₂(ord) ≤ 1` leaves `E₁, E₂`.
- The `Φ₅/5` forced-prime machinery — sound, and reusable.
- Lemma 7.4 itself is correctly proved; it is simply unusable.

---

## 8. Which direction is justified next

- **Direction A (repair certificate semantics for q ∈ {5,…,17})** — ruled out
  by Proposition A. Not a matter of leverage; it is impossible.
- **Direction B (extend to q ≥ 19)** — ruled out for the same reason, and
  strictly worse: `k₀(19) = 85`, so the shortfall grows with `q`. Extending the
  forced-or-pure mechanism to `q ≥ 19` would inherit the identical fatal tail
  layer. Deriving the first-input classification for `q ≥ 19` is a real but
  modest exercise (`q−1 = 2^a m`; non-Euler orders are the odd divisors of `m`,
  Euler orders those divisors of `q−1` with `v₂ ≤ 1`) whose output feeds a
  mechanism that cannot close anything.
- **Direction C (a different obstruction)** — the only defensible direction.
  The correct use of abundancy in this problem is the direction Proposition C
  points: minimality of `q` forces `ω(N)` to be **large** (62 for `q=17`,
  85 for `q=19`), hence forces a large number of `q`-adic input witnesses
  through the valuation-balance identity `e_q = Σ_{p≠q} v_q(σ(p^{e_p}))`.
  That is a genuine combinatorial constraint that grows with `q`, and it is the
  opposite of an upper envelope. Any future attempt should be built on it.

---

## 9. Confidence

| Conclusion | Status |
|---|---|
| Proposition A, and hence that no valid tail-envelope certificate can satisfy the acceptance test | **proved** |
| Proposition C and the `k₀(q)` table | **proved** (exact rational arithmetic) |
| `M = 18` contradicts the paper's own Corollary 4.4 for `q ∈ {11,13,17}` | **proved** |
| Obligation (ii) for `q=17` is equivalent to the branch being empty | **proved** |
| Verifiers hardcode `B==59, M==18`; `endpoint_check` never parsed; `coverage_note` free text; incomplete candidate list accepted while the corrected one is rejected | **computationally verified** (`audit/05`) |
| `cor:q17-first-input-coverage` absent from both `.tex` files | **computationally verified** |
| 5 files drift from published hashes; all five verifiers print the advertised output | **computationally verified** |
| `Φ₅/5` forced-prime lemma is sound | **proved** + spot-checked |
| Lemmas 3.1, 3.2, 4.2, 6.2–6.4 sound | **strongly supported** (re-derived; not line-by-line exhaustive) |
| No upper bound on `ω(N)` exists in the literature | **strongly supported** (standard; being checked independently) |

## 10. Failure modes of *this* audit

The one way §1 could be wrong is if `M` does not mean what Definition 7.5 says.
If `M` bounded only the support primes *contributing to the q-adic valuation*
rather than all remaining support primes, Proposition A would not apply. Three
things rule that reading out: Definition 7.5 says "support-prime slots" without
qualification; the proof of Lemma 7.4 writes `H(S) ≤ H(K_env)(B/(B−1))^M` over
the **entire** support `S`; and Definition 7.3 glosses envelope entries as
"independent worst-case support-prime slots". Under any reading that makes
Lemma 7.4's proof valid, Proposition A applies.

Secondarily, `k₀(q)` in Proposition C would be wrong if `σ(N)/N < Π p/(p−1)`
failed — it cannot, the inequality is term-wise and strict for every finite
exponent. `k₀(11) = 27` agreeing with the independently published bound is a
useful external check.

---

## 11. Literature cross-check

A parallel literature scan (delegated; treated as a lead, not as evidence) and
my own reading agree on the points that matter:

1. **No upper bound on `ω(N)` for an odd perfect number is known in any form.**
   The literature contains only lower bounds on `ω(N)` and upper bounds on the
   *magnitude* of `N`. This is exactly the quantity obligation (ii) requires,
   and it confirms that Remark 7.6's disclaimer ("not inferred from a hidden
   global upper bound on `ω(N)`") is describing the absence of any argument at
   all, not a substitute for one.

2. **A third, purely classical refutation of `M = 18`.**
   Grün (1952): the smallest prime `p₁` of an odd perfect `N` satisfies
   `p₁ < (2/3)ω(N) + 2`, i.e. `ω(N) > (3/2)(p₁ − 2)`. For `p₁ = 17` this gives
   `ω(N) ≥ 23 > 20`. So the q=17 tail-count assertion is refuted by a
   seventy-year-old published theorem, independently of Proposition A and of
   Proposition C. (Grün is weaker than Proposition C — 23 against 62 — but it
   is externally citable and suffices for `q = 17`.)

3. Corollary 4.4's citation chain checks out as to content: Nielsen
   (*Math. Comp.* 76, 2007) for `ω ≥ 9` and `ω ≥ 12` when `3 ∤ N`; Norton-type
   results for `ω ≥ 15` when `3·5 ∤ N` and `ω ≥ 27` when `3·5·7 ∤ N`. The
   paper's use of these bounds is legitimate. The problem is that it never
   compares them against its own tail-count records — had it done so, the
   contradiction for `q ∈ {11,13,17}` would have been visible immediately.

4. **Status of the preprint.** arXiv is blocked from this container, so I could
   **not** independently verify `arXiv:2607.04365`. What I verified directly:
   the repository exists, the tag `C-small-2026-07` and `HEAD` are both
   `4f59cde9…`, dated 2026-07-05. The delegated scan reports that the
   identifier resolves and that it found **no** citations, reviews or responses
   to the paper. Treat the arXiv record and the absence of responses as
   unverified by me.

So the gap identified here has apparently not been noted publicly, and the
result stands as an uncontested claim in the literature.
