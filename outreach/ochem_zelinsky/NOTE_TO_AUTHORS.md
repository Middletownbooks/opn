# Draft note to Pascal Ochem and Joshua Zelinsky

*Status: DRAFT, not sent. To be audited (`AUDIT_BRIEF.md`) before sending. Attach
`ochem_zelinsky_bundle.zip` (built by `make_bundle.py`). Fill in the bracketed
items. The authors' addresses are on the paper's arXiv listing and PDF.*

---

**Subject:** arXiv:2607.19746 — a 64-bit overflow in loopless.cpp, and a corrected run (Theorem 1 holds)

Dear Professor Ochem and Dr Zelinsky,

I have been reading your paper *On odd perfect numbers with exactly one even
exponent greater than 2* (arXiv:2607.19746v1), and I am writing about one issue in
the released code for §4 and a few related checks.

**Who did this work.** I should say at the outset that I am not a mathematician or
a programmer. The analysis below was done with an AI assistant (Anthropic's
Claude), working with your paper, your released programs and data, and my
direction. I cannot verify it myself. I have therefore asked for every claim to be
stated so that you can check it directly, and I have attached the programs and
outputs. Please weigh it accordingly. [Optional: *An independent AI review of
this note and the attached programs found …* — fill in from the audit.]

**The short version.** `check_M2` in `loopless.cpp` computes `r*r + r + 1` in
64-bit arithmetic, which wraps once `r ≥ 2³²`. The published sieve output at `z`
therefore does not come from Algorithm 1. An independent, overflow-free
implementation **confirms your conclusion `q ≥ 23,000,000,000`**. The corrected
run is still conservative, and it gives a larger margin than the published
figures do.

## 1. The overflow

In `loopless.cpp` [confirm: the copy downloaded from lirmm.fr/~ochem/opn/restrained/], line 135 is

    u64 val = r * r + r + 1;

`r * r` wraps modulo `2⁶⁴` once `r ≥ 2³² = 4,294,967,296`, and `get_factors` takes
a `u64` in any case. The run in §4 reached `z = 216,171,986,291`, about 50 times
past that point. So for most of the range the program tested
`(r² + r + 1) mod 2⁶⁴` rather than `r² + r + 1`. This can go either way: a wrapped
value can hide a factor in `M₂`, or supply a spurious one.

The effect shows in the published numbers. Fitting a survival rate to the
reported `k > 2.5·10⁹` and `A = 1.088507187872` gives about 9% of primes surviving
below `2³²` and about 29% above. That is nearly the square root of 9%, which is
what a wrapped (effectively random) value produces. A correct sieve's survival
rate should fall, not rise, as `r` grows, since `M₂` only gets larger. The
corrected run's rate is about 7% at `10¹⁰`.

## 2. A corrected run

`13_sieve.c` in the attachment is an independent implementation of Algorithm 1 in
C. It never forms `r² + r + 1`; instead each `q ∈ M₂` marks the residues
`r ≡ ρ, q − 1 − ρ (mod q)`, where `ρ` is a primitive cube root of unity mod `q`.

**How it was checked.** Below `2³²`, where your program is exact, it prints the
same progress lines as your unmodified `loopless.cpp`. We compared all 253 lines
from an hour of your program, up to `r = 579,733,409`. For example:

    k: 2530000  | r: 579733409  | A: 1.028007677068
    k: 15650000 | r: 4293066907 | A: 1.035513576704     (the last line before 2^32)

It also agrees line for line with a separate Python implementation. Our run to
`2³²` takes 87 seconds, so you can compare it with your own program directly.

**The result at your `z`.** For memory reasons, primes of `M₂` above
`2³⁵ ≈ 3.4·10¹⁰` are not used to exclude anything. The run is exact below
`2³⁵` and keeps a superset of the survivors above it, so the figures are upper
bounds on Algorithm 1's exact `k` and `A`. That suffices, because the count only
needs every possible ordinary prime below `z` to be among the survivors. At
`z = 216,171,986,291`:

| | published | corrected |
|---|---|---|
| survivors `k` | more than 2,500,000,000 | 599,351,328 |
| abundancy `A` | 1.088507187872 | 1.047357816316 |

With `K_max` the largest `K` such that
`3/2 · (1 + 1/6,000,000) · A · (1 + 1/z)^K < 2`:
- the corrected run gives `k + K_max = 52,785,706,892`, comfortably above the
  46,000,000,000 that §4 needs;
- so Lemma 8 gives `q ≥ 23·10⁹` with room to spare, and in fact
  `q ≥ 26,392,853,446` from the same argument.

The count first passes `46·10⁹` at about `z = 1.89·10¹¹`. The fewer true survivors
more than make up for the smaller `k`.

## 3. Other checks you may find useful

- **Primes `11 … 3·10⁶`.** `tree.txt` itself was too large for me to transfer, so
  the claim it supports was re-checked with an independent prover. It uses the
  method of `tree.cpp` but none of its code (`15_tree_pilot.py`).
  - Without using `checkfacts.txt` at all, it rules out every prime in
    `[11, 3·10⁶]` except 502013 and 2152883. There its own factoring gave up.
  - With factors from `checkfacts.txt`, both are ruled out; each factor is
    checked to divide and to be a probable prime before use.
  - All 460 entries of `checkfacts.txt` verify.
  - So the claim is confirmed.
- **Running further.** The corrected program reached your `z` in about 55 minutes
  on one core. Continued to `z = 10¹²` (3.8 hours), it gives
  `k + K_max = 240,019,297,934`, hence `q ≥ 120,009,648,966` by your argument.
  This is your method; I mention it only in case it is useful to you.
- **The final product in §4.** The printed value `1.99209763359616948564` is
  reproduced to about 10 significant digits by `A = 1.088507187872` with
  `K = 43,000,000,000`, not with the text's `1.076855990994` and `43,500,000,000`.
  With the text's `K` and the sieve's `A`, the product is `1.99671… < 2`, so the
  conclusion is unaffected. I could not find where `1.076855990994` comes from.
- **Minor.** The released `tree.cpp` loops indefinitely (`while (1)`, with the
  bounded loop commented out), so its summary is never printed.

## 4. The attachment

`ochem_zelinsky_bundle.zip` contains the programs, a README with the exact
commands and expected outputs, and our outputs. It needs only `gcc` and
`python3`, plus GMP if you want to rebuild your own program for comparison.

Thank you for the paper, and for releasing the programs and data, which made all
of this possible. I would be glad to hear whether the overflow matches your
understanding of the run. Please feel free to ignore the rest if it is not useful.

With best regards,
[Your name]
[Optional: contact details]
