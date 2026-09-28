# Independent audit of the note to Ochem & Zelinsky and its attachment

*This audits `NOTE_TO_AUTHORS.md`, `BUNDLE_README.md`, `make_bundle.py` and the
programs they cite, following `AUDIT_BRIEF.md`. It was done in a fresh session on
2026-09-28. Every verdict comes from something re-run in this session, not from the
other session's reports. The auditor's own code is in `audit/`. Commands were run in
a scratch directory, on copies of the repo files and on an unpacked copy of the zip.*

**Caveat about independence.** The auditor is also Claude: a separate session of
the same AI. It shares no context with the first session, and it wrote its own code
wherever the brief asked. But it is not independent in the way a human expert would
be, and the two sessions could share blind spots. The note should say this (§3 below).

---

## 1. Verdict per claim

| # | verdict | in one line |
|---|---|---|
| C1 | **CONFIRMED** | line 135 wraps for `r ≥ 2³²`; `get_factors` takes `u64`; the wrap flips verdicts both ways |
| C2 | **CONFIRMED; wording should change** | the fit gives 9.3% and 29.5%, as stated. Exact figures exist, need no fit, and are stronger. |
| C3 | **CONFIRMED** | the auditor's own direct-factoring Algorithm 1 gives the identical survivor list. The superset claim holds when tested directly. |
| C4 | **CONFIRMED** | the unmodified `loopless.cpp`, run here for 70 min, printed 260 lines. All match `13`, and the first 253 are byte-identical to the repo record. `13` reaches `2³²` in 81 s. |
| C5 | **CONFIRMED** | `12` and `13` agree line for line at `2·10⁸` |
| C6 | **CONFIRMED** | re-run: all 219 checkpoints identical to the record; `14` output identical |
| C7 | **CONFIRMED** | the argument is sound, including with a superset of survivors. The note should say what it takes from the rest of the paper. |
| C8 | **CONFIRMED on a sample; full range not re-run** | 40,000+ random roots ruled out; two provers; all 460 `checkfacts.txt` entries verify |
| C9 | **CONFIRMED except one number** | `k + K_max = 240,019,297,934` is right. The `q` bound it gives is `≥ 120,009,648,968`, not `…966` (a rounding bug in `14`). |
| C10 | **CONFIRMED** | `A = 1.088507187872`, `K = 43·10⁹` gives `1.99209763353720…`, a relative difference of 3·10⁻¹¹ from the printed value |
| C11 | **CONFIRMED, but not worth sending** | `while (1)`, with the bounded loop commented out. The file's own `Run:` line suggests this is deliberate. |
| C12 | **CONFIRMED** | 16 files, each byte-identical to its source; the zip rebuilds bit for bit; README §§1, 2, 5, 7 and the `2·10⁸` diff work from an unpacked copy |

### C1: the overflow

Read `sources/loopless.cpp` directly:
* Line 135 is `u64 val = r * r + r + 1;`.
* `r` is `u64` (`typedef uint64_t u64`, line 12). `get_factors(u64 n, …)` is at line 98.
* `u128` is used only in `power_mod` and `pollard_rho`.

The first four primes above `2³²`, computed exactly in Python and then reduced mod `2⁶⁴`:

    4294967311  18446744206853538033  ->  133143986417
    4294967357  18446744601990532807  ->  528280981191
    4294967371  18446744722249619013  ->  648540067397
    4294967377  18446744773789227507  ->  700079675891

`05_loopless_overflow.py` shows that a wrap can hide a factor that lies in `M₂`: for
example, `4294967357` is excluded by 7 but passes when wrapped. The note also says the
wrap can "supply a spurious one". The repo did not demonstrate that direction, so I
tested it separately. Some primes survive Algorithm 1 for certain, because
`(r²+r+1)/3` is prime and so has no factor below `r`. Yet their wrapped value is
divisible by a prime in the initial `M₂`, so `loopless.cpp` would exclude them. The
first three above `2³²`:

    r = 4294967977   wrapped value divisible by 13
    r = 4294968607   wrapped value divisible by 571
    r = 4294968637   wrapped value divisible by 13

**Both directions occur, and the second is the unsafe one:** it can drop a genuine
possible ordinary prime.

I could not fetch the authors' page: the container's network policy refuses
`lirmm.fr`. That `sources/loopless.cpp` matches the file on the authors' page rests on
the sender's own copy (`sources/README.md`).

### C2: the wrap's signature

`python3 restrained/11_wrap_signature.py 10000 7` (82 s) reproduces the recorded fit
exactly: `f0 = 0.0929`, `f1 = 0.2945`, `sqrt(f0) = 0.3049`. Part 2 gives
0.1133 / 0.4358 / 0.3592 (wrapped), as recorded.

The fit is crude, and a fit is not needed. Below `2³²`, `loopless.cpp` is exact, so its
survival rate there is known exactly from the corrected run:
* `15,656,368` survivors among the `π(2³²) − π(3·10⁶) = 203,063,405` primes, i.e.
  **7.7%**, not 9%.
* Above `2³²`, the published `k > 2.5·10⁹` means at least `2,484,343,632` survivors
  among about `8.42·10⁹` primes, i.e. **at least 29.5%**.
* `√7.7% ≈ 27.8%`, so "nearly the square root" still holds.
* In the corrected run, the rate on `(2³², z)` is **6.9%**. It falls, as the note says it
  should. Near `10¹⁰` the local rate is 7.1% and the cumulative rate 7.4%, so "about 7%
  at 10¹⁰" is fair.

"Which is what a wrapped (effectively random) value produces" is a heuristic. Part 2
supports it against a fixed `M₂`, but the wrapped run's own `M₂` differs from the true
one. It should be worded as an expectation, not a fact (§2 below).

A more direct argument is also available, and the note does not use it. The corrected
`k(z) = 599,351,328` is an **upper bound** on Algorithm 1's exact `k(z)`. So the
published "more than 2,500,000,000" cannot be Algorithm 1's output, whatever the
statistics say.

### C3 and C5: Algorithm 1

**My own implementation** is `audit/auditor_algorithm1.c`, written from the pseudocode
in the transcript. It shares no code or method with `12`/`13`:
* it factors `r²+r+1` and `r+1` directly (trial division, Pollard–Brent, and a
  Miller–Rabin test that is deterministic in this range);
* it keeps `M₁` and `M₂` as explicit arrays;
* it uses no cube roots and no `(r+1)/2` shortcut.

With `Q` it excludes only with `M₂` primes `< Q`.

| test | result |
|---|---|
| exact, `(3·10⁶, 2·10⁷]` | survivor list identical to `13`'s (102,073 primes); `ln A` identical to all 21 printed digits |
| exact, `(3·10⁶, 2·10⁸]` | survivor list identical (957,150 primes); all 95 progress lines identical; `ln A = 0.0231760522980211608487` in both |
| `12` vs `13`, `2·10⁸` | `diff` of progress lines empty (33.8 s) |
| `Z = 2·10⁷`, `Q = 4·10⁶` and `Q = 10⁷` | `13`'s survivors (dumped by a scratch copy of `13` with one added `fprintf`) equal mine in the same mode. **Every exact survivor is among them.** Below `Q` they equal the exact ones. |

I also checked the header of `13_sieve.c` by reading it:
* **Cube roots.** For a prime `q ≡ 1 (mod 3)`, `q | r²+r+1` exactly when `r ≡ ρ` or
  `ρ² = q−1−ρ (mod q)`. Only hits `r > q` are marked. That is exactly Algorithm 1: at
  time `r`, only primes `< r` can be in `M₂`.
* **Joining `M₂`.** "`r` joins `M₂` iff `r ≡ 3 (mod 4)` or `(r+1)/2` is not a
  survivor", for `r ≡ 1 (mod 3)`. This is correct while `(r+1)/2 < 9·10¹²`. Then
  `s = (r+1)/2` is odd, prime to 3, and either has a prime factor below `3·10⁶` (that
  factor is in `M₁`) or is itself a prime `> 3·10⁶` (in `M₁` iff it did not survive).
  The header states this condition. The range used, `z ≤ 10¹²`, is far inside it.
* **The superset induction** is right. `M₂' ⊆ M₂` gives `S' ⊇ S`, hence
  `M₁' ⊆ M₁`, hence `M₂' ⊆ M₂` at the next step.
* **Buckets.** The next hit of `q` is at most `2q < 2Q` away, so fewer than `NB` chunks
  ahead; the "bucket wrap" guard is never needed. `q << 22` fits 64 bits for
  `Q < 2⁴²`.

### C4: agreement with the authors' program

I built the unmodified `sources/loopless.cpp` with
`g++ -O3 -I <shim> -o loopless loopless.cpp /usr/lib/x86_64-linux-gnu/libgmp.so.10`.
`restrained/loopless_build/gmp.h` contains only typedefs, prototypes and `#define`s
that map the names to `__gmpf_*`. The `mpf` struct layout is GMP's.

I ran it for 70 minutes on a loaded 4-core machine and it printed 260 progress lines.
* `diff` against the first 260 `k:` lines of `13`'s run to `2³²` is empty.
* Its first 253 lines are byte-identical to `restrained/runs/loopless_released_1h.txt`,
  whose last line is `k: 2530000  | r: 579733409  | A: 1.028007677068`.

`13` run to `2³²` from the unpacked zip, per README §2:
* **81 s** (the note says 87 s);
* it prints `k: 2530000  | r: 579733409  | A: 1.028007677068` and
  `k: 15650000 | r: 4293066907 | A: 1.035513576704`;
* at `2³²`, `k = 15,656,368`, `ln A = 0.0348989960116071389319`, and
  `exp(ln A) = 1.035515112361`, as in the README.

### C6: the corrected run to `z`

`./sieve 216171986291 34359738368 0` ran in 2,585 s (43 min) at 5.76 GB. Output:
`SUMMARY … k=599351328 lnA=0.0462706273871303976052 m2=3997201149 m2big=3313545857`.
* All 219 `CP` lines are identical to `restrained/runs/13_z_Q2e35_checkpoints.txt`.
* `14_bound_from_run.py` on this output is identical to
  `restrained/runs/14_bound_z_Q2e35.txt`:
  `A = 1.047357816316`, `K_max = 52,186,355,564`, `k + K_max = 52,785,706,892`,
  `q ≥ 26,392,853,446`.
* **The count first reaches `46·10⁹` between the checkpoints `1.88·10¹¹`
  (45,979,497,315) and `1.89·10¹¹` (46,221,277,691).** "About `1.89·10¹¹`" is fair.

I recomputed `K_max` with my own code: 80-digit `Decimal`, a closed form, and the
strict inequality handled.
* At `z`: `(ln 2 − ln 3/2 − ln(1+1/6·10⁶) − ln A) / ln(1+1/z) = 52,186,355,564.465`,
  so `K_max = 52,186,355,564`.
* The fractional part, 0.465, means `ln A` would have to be wrong by about
  `2·10⁻¹²` to move `K_max`. The compensated long-double sum is accurate to far better
  than that.
* The margin over `46·10⁹` is `6.79·10⁹` primes, so no rounding question touches the
  conclusion `q ≥ 23·10⁹`.

### C7: the argument

I checked this against the transcript (§4 and Lemma 8).

1. **Survivors.** If `r > 3·10⁶` is ordinary, `r²+r+1 | 2N`, so no prime of `M₂` divides
   it; `r` survives.
   * The initial `M₁`/`M₂` are right because every prime `5 … 3·10⁶` does not divide `N`.
   * A non-survivor `r ≡ 1 (mod 3)` can enter `M₂` for two reasons. Either
     `r ≡ 3 (mod 4)`, so it cannot be special. Or `r+1 | σ(r^e)` for odd `e` and a
     prime `t | r+1` lies in `M₁`. Then `t ≠ r` and `t ≠ 3`, so `t` is neither special
     nor notable. So `t` does not divide `N`, and neither does `r`.

   **Sound.**
2. **The count.** Let the ordinary primes number `j` below `z` (a subset of the `k`
   survivors) and `K` above `z`.
   * Each survivor `r ≤ z` has `r/(r−1) > 1 + 1/z`. So the `j` of them contribute at
     most `A · (1+1/z)^{−(k−j)}`.
   * The primes above `z` contribute less than `(1+1/z)^K`.
   * If `j + K ≤ k + K_max`, then `σ₋₁(N) < 3/2 · (1+1/6·10⁶) · A · (1+1/z)^{K_max} < 2`,
     a contradiction.

   So there are **at least `k + K_max + 1` ordinary primes**. This uses only that the
   survivor set **contains** the ordinary primes below `z`, so a superset is safe; it
   just gives a weaker bound. **Sound, no off-by-one:** the strict `<` gives `K_max`,
   and the `+1` follows.
3. **`ω` and Lemma 8.** `ω = 2 + #ordinary`, because the only non-ordinary primes are
   `p` and `3`. Lemma 8 gives `q ≥ ω/2 − 2`. With `B = k + K_max`, this is
   `q ≥ (B+3)/2 − 2 = (B−1)/2`. `q` is even, because `N = p^e m²`.
   * At `z`: `q ≥ 26,392,853,445.5`, so `q ≥ 26,392,853,446`. ✓
   * At `10¹²`: `q ≥ 120,009,648,966.5`, so `q ≥ 120,009,648,967`, and since `q` is even,
     **`q ≥ 120,009,648,968`**. The note says `…966` (see C9).
4. **What §4 takes from outside Algorithm 1.**
   * `σ₋₁(3^q) < 3/2`: immediate.
   * `p > 6·10⁶`: the paper does not spell this out. It follows because
     `(p+1)/2 | N` (`e` is odd); `3 ∤ p+1` (`p ≡ 1 mod 3`, Lemma 6); so every prime of
     `(p+1)/2` is `> 3·10⁶`, and `p > 6·10⁶`. Valid.
   * Primes `11 … 3·10⁶`: `tree.txt` (C8 below).
   * 5 and 7, by hand: I re-verified every factorisation in the two trees, and the
     three `σ₋₁ > 2` values (2.0835, 2.0520, 2.0023). I did not re-derive the
     `XS 7` step.
   * Lemma 8 itself: read and followed. Its inputs (Bennett–Levin, Lemma 3 of [8],
     Theorem 2 of [1]) were not checked.

**Does the note overstate?** Mildly, in two places:
* The subject line says "Theorem 1 holds". The work checks the §4 computation, not
  the whole theorem.
* "An independent, overflow-free implementation confirms your conclusion" should say
  that the confirmation is of the computation, with the rest of the argument taken
  from the paper.

Wording is proposed in §2.

### C8: primes `11 … 3·10⁶`

**Soundness of `15_tree_pilot.py` as used.** I read it against `tree.cpp` and against
§§1 and 4 of the paper.
* **Branches.** An assumed `x | N` with `x ≥ 5` is either ordinary or special, because
  the notable prime is 3.
  * Ordinary: every prime `≥ 5` of `x²+x+1` divides `N`. `x²+x+1` is odd and has
    `v₃ ≤ 1`, so removing a single 3 is right.
  * Special: `x ≡ 1 (mod 12)` (Euler, and Lemma 6). With `e` odd, `x+1 | σ(x^e)`, and
    `(x+1)/2 ≡ 1 (mod 6)`.
* **Special eligibility** is refused when an ancestor on the path is special. That is
  correct: there is only one special prime.
* **The path/cycle rule** skips a factor already assumed to divide `N`. Skipping only
  loses proving power, never soundness.
* **The factor-below-root rule** relies on induction over roots in increasing order.
  It also needs 5 and 7 from the paper's hand trees.
* **3** is never treated as a contradiction. Correct.
* **Budgets** raise `Budget` and report UNRESOLVED, never "ruled out".
* **Hints** are used only after the division and a probable-prime test.
* **ECM** returns a gcd, so it cannot produce a false factor.
* **The one trust assumption** is the probable-prime test on factors above
  `3.3·10²⁴`. `tree.cpp` has the same trust assumption, and a weaker one: 25
  random-base Miller–Rabin rounds, and no check of `checkfacts.txt` entries.

The logic matches `tree.cpp`'s `prove()`. I found no unsound step.

**Re-runs.**

| run | result |
|---|---|
| `15` on 20,000 random roots (seed 2026) + the 15 listed roots, with hints | 20,012 roots, **all ruled out**, 256 s; 19 hints used, 0 rejected |
| `15` on 20,000 random roots (seed 2027) + the 15, `NOHINTS=1` | 20,015 roots: **20,014 ruled out**. The one exception is `2152883`, which the random draw happened to include. It stopped on the ECM budget (reported as unresolved, not as an open branch), exactly as recorded. 0 hints; 33 ECM splits; 4,957 s. |
| `15`, `502013` and `2152883` with hints | both ruled out (2 hints each, 0 rejected) |
| `15`, `502013` and `2152883`, `NOHINTS=1` | HARDROOTS |
| **auditor's own prover** (`audit/auditor_tree_prover.py`, written from the paper only), 5,000 random roots (seed 99) + the 15 + the 2 | 4,977 ruled out, **0 open**; 39 hit its small Pollard budget (it has no ECM). With a larger budget 9 more were ruled out. `15` rules out the remaining 14 without hints. Given `checkfacts.txt` factors, my prover rules out `502013` and `2152883`. |
| `checkfacts.txt`, auditor's own check | **460 entries, 0 failures**: each factor divides its `x²+x+1` (type 3) or `x+1` (type 2) and passes 13 fixed-base plus 30 random-base strong-probable-prime tests |

**Negative control.** Run on roots 5 and 7, where nothing smaller is ruled out, my
prover does not claim them; it gives up.

The full range was not re-run (about 4 CPU-hours). The claim rests on the recorded
run plus these samples.

### C9: `z = 10¹²`

* `14_bound_from_run.py results/13_1e12_Q2e35_checkpoints.txt`, run from the unpacked
  zip, reproduces `results/14_bound_1e12_Q2e35.txt` exactly.
* The 218 checkpoints up to `z` are identical to the `z` run's (and to my re-run).
* The 11 checkpoints of `13_1e10_exact_checkpoints.txt` equal the `z` run's.
* My own `K_max` code gives `K_max = 237,349,265,802` and `k + K_max = 240,019,297,934`,
  as stated.

**But the `q` bound is off by 2.** `14_bound_from_run.py` line 45 is
`q = int(-(-D(qb) // 1))`. `Decimal`'s `//` truncates toward zero, unlike `int`'s, so
this "round up" rounds down:

    >>> -(-Decimal('120009648966.5') // 1)
    Decimal('120009648966')

At `z` the error is hidden by the even-rounding step (`…445` rounds up to `…446`, which
is right). At `10¹²` it gives `…966` instead of `…968`. The stated bound is still
*true*, since it is weaker, but it is not what the argument gives.

I did not re-run the 3.8 h job.

### C10: the product

With 50-digit `Decimal`:

    A = 1.088507187872, K = 43.0e9  ->  1.99209763353720007…   (printed 1.99209763359616948564)
    A = 1.088507187872, K = 43.5e9  ->  1.99671063469240028…
    A = 1.076855990994, K = 43.5e9  ->  1.97533818169217888…   (the text's own inputs)

The match is to about 10 significant digits, as claimed, and `1.99671… < 2`.
`10_section4_reconcile.py` gives the same.

### C11: `tree.cpp`

Line 305 is `while (1) {`, with `//while (r <= bound) {` and `//mpz_class r = 1009;`
commented out above it. Since only the line breaks are reconstructed, one might ask
whether `while (1)` could itself sit inside a comment. It cannot: `r` must be declared
and the braces must balance, so `mpz_class r = bound; while (1) {` is live code. The
loop is infinite, and the summary is unreachable.

However, the file's header says `Run: ./tree_search 11`, so the argument is the
*starting* root. The program was evidently meant to be run with `-v` and stopped by
hand. This is not a defect worth the authors' time.

### C12: the bundle

* `make_bundle.py` rebuilt the zip with the same SHA-256
  (`512ac53a…0b9ff`); `git status` stayed clean.
* The zip holds 16 files. Each is byte-identical to the repo file `make_bundle.py`
  maps it to.
* From a fresh unpacked copy:
  * §1 (`05`) runs and matches the repo run;
  * §2 builds and runs in 81 s with the quoted lines, and the `12`/`13` diff at
    `2·10⁸` is empty;
  * §5 (`11`, 10000 7) reproduces the recorded numbers;
  * §7 (`10`) runs;
  * `14` on both `results/…checkpoints.txt` files reproduces both `results/14_…`
    tables exactly.

---

## 2. Errors found, with proposed fixes

### In the note (`NOTE_TO_AUTHORS.md`)

1. **Subject line overstates.** Replace "(Theorem 1 holds)" with
   **"(the bound q ≥ 23·10⁹ still holds)"**.
2. **Salutation.** Pascal Ochem is, to my knowledge, a CNRS researcher rather than a
   professor. I do not know Joshua Zelinsky's title. Neutral and safe:
   **"Dear Pascal Ochem and Joshua Zelinsky,"**.
3. **"The short version", sentence 3.** Replace "An independent, overflow-free
   implementation confirms your conclusion `q ≥ 23,000,000,000`." with:
   > An overflow-free re-run of Algorithm 1, with the rest of your §4 argument as
   > written, still gives `q ≥ 23,000,000,000`.
4. **§1, the signature paragraph.** Replace from "Fitting a survival rate…" to "…about
   7% at `10¹⁰`." with:
   > The effect shows in the published numbers. Below `2³²` your program is exact, and
   > there 7.7% of primes survive (15,656,368 of the 203,063,405 primes in
   > `(3·10⁶, 2³²)`). Above `2³²`, `k > 2.5·10⁹` means that at least 29.5% of the
   > roughly `8.4·10⁹` primes in `(2³², z)` survived. That is close to
   > `√7.7% ≈ 28%`, which is about what one expects when the tested value behaves like
   > an unrelated 64-bit number. An exact sieve's survival rate should drift down, not
   > up, since `M₂` only grows; in the corrected run it is 6.9% on `(2³², z)`.
   >
   > The wrap errs in both directions. For example, `r = 4,294,967,977` can be ordinary
   > as far as Algorithm 1 is concerned (`(r²+r+1)/3` is prime), but its wrapped value
   > is divisible by 13, so `loopless.cpp` excludes it.
5. **§1, add the direct argument** after "does not come from Algorithm 1" (or in §2
   under the table):
   > Since the corrected `k` is an upper bound on Algorithm 1's exact count, the
   > published "more than 2,500,000,000" cannot be its output.
6. **§2, last sentence.** "The fewer true survivors more than make up for the smaller
   `k`" is confusing, because fewer survivors *is* the smaller `k`. Replace with:
   > The smaller `k` is more than made up for by the smaller `A`, which raises `K_max`.
7. **§3, "Running further".** Change `q ≥ 120,009,648,966` to
   **`q ≥ 120,009,648,968`**.
8. **§3, "Minor" item on `tree.cpp`.** Delete it. The header's `Run: ./tree_search 11`
   shows the argument is a starting point, and the endless loop is evidently
   deliberate. Mentioning it reads as nitpicking.
9. **§3, primes `11 … 3·10⁶`.** After "So the claim is confirmed." add:
   > (up to probable-prime tests on the largest factors, as in `tree.cpp`).
10. **The disclosure placeholder.** Fill it in as:
    > A second, separate session of the same assistant, told to trust nothing from the
    > first, re-ran the main computations with its own code. That included its own
    > implementation of Algorithm 1, which factors `r²+r+1` directly. It confirmed
    > them, apart from two small slips that have been corrected. This is not the same
    > as an independent human check.
11. Optional: the note mixes "I" with "we"/"our" ("We compared", "Our run"). Either
    is fine, but one is better.

### In the README (`BUNDLE_README.md`)

1. §4: `q >= 120,009,648,966` → **`q >= 120,009,648,968`** (after fixing `14`, its
   output will say so).
2. §6: "about 4.5 CPU-hours" → **"about 4 CPU-hours"** (the recorded shards sum to
   14,558 s). Add that 502013 and 2152883 each take about an hour before giving up
   without hints.
3. Add a line under "Files": the programs' comments refer to repository files
   (`NOTES_RESTRAINED.md`, `sources/…`, `restrained/10`) that are not included.
   `05`'s printed text also carries some repository history ("UPDATE (later
   work…)").
4. §3's "Expected" block is a paraphrase, not `14`'s actual output format (a table).
   Harmless; say "Expected (the row for x = 216,171,986,291):".

### In the programs

1. **`14_bound_from_run.py` line 45 (a real bug, conservative direction).** Replace
   ```python
   qb = (B + 3) / 2 - 2                     # q >= omega/2 - 2, omega >= B + 3
   q = int(-(-D(qb) // 1)); q += q % 2       # round up to an even integer
   ```
   with
   ```python
   q = B // 2; q += q % 2                   # q >= omega/2 - 2 = (B-1)/2, so q >= B//2; q even
   ```
   (For an integer `B`, `⌈(B−1)/2⌉ = ⌊B/2⌋`.) Then regenerate the two `runs/14_*`
   files and rebuild the zip. Only the `q ≥` column changes, and only at odd `⌊B/2⌋`.
2. **`13_sieve.c`, cosmetic.** When `Z_END = 216171986291`, the checkpoint at `z`
   is printed twice (it is both the paper's `z` and `Z_END`). This is why `14`'s table
   shows the `z` row twice. Harmless.

No other errors were found in `13`, `12`, `15`, `05`, `10` or `11`.

---

## 3. What the note should add or remove

* **Add** the direct argument (fix 5) and the two-direction example (fix 4). They make
  the overflow claim checkable in seconds, without statistics.
* **Add** the qualification that the confirmation covers the §4 computation. The rest
  of the argument is the paper's (fixes 1 and 3).
* **Add** an honest line on the audit (fix 10).
* **Remove** the `tree.cpp` "Minor" item (fix 8).
* **Keep** the product (C10) item. It is correct and useful, and the note already
  says the conclusion is unaffected.

---

## 4. Plain-language summary for the sender

The note's main claim is correct. I re-checked it from scratch with my own code,
including a separate program that does the authors' sieve a different way. The
authors' program does have an arithmetic overflow past about 4.3 billion, so their
published count is not what their algorithm would give. Done correctly, the
computation still proves their theorem's bound, with room to spare. I found two small
numerical slips:
* one figure in the "running further" paragraph is off by 2 (it should end in 968,
  not 966);
* the statistics paragraph uses a rough estimate where exact figures are available.

I also recommend softening the subject line, which claims more than was checked. The
note can be sent **after the listed fixes**, none of which changes its substance.
Please keep in mind that this second opinion also comes from the same AI, not from a
mathematician.
