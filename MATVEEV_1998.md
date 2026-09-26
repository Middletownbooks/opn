# Matveev 1998, §2: the statement used here

**Source.** Е. М. Матвеев, *Явная нижняя оценка однородной рациональной
линейной формы от логарифмов алгебраических чисел*, Известия РАН, Серия
математическая, **62**:4 (1998), 81–136.

The user supplied a full OCR transcript and then clean screenshots of pp. 85–87,
kept in `sources/matveev1998_p85.png`, `…p86.png` and `…p87.png`.
Everything below is transcribed from the **screenshots**, with **one
exception**: the Kummer condition (1.5) is on p. 82, which is not among the
screenshots. It is read from the OCR text, which states it in words ("by the
strong independence condition we will mean the equality … (1.5)", later called
the Kummer condition). The formula itself was garbled as
`[ K ( V a r , . . . , > / a ^ ) : K ] =2 n`. The reading
`[K(√α₁,…,√αₙ) : K] = 2ⁿ` rests on that text plus the surrounding remark that
square roots suffice. **A page image of p. 82 is still needed** to confirm it.
No constant comes from the OCR or from memory. The transcription is kept
literal, and its use is stated separately.

## Setting (p. 85)

* `K` is an algebraic field of degree `D_K` over `ℚ`, embedded in `ℂ`.
* If `K ⊆ ℝ`, put `κ = 1`; otherwise `κ = 2`. Then `D = D_K/κ`.
* `α₁, …, α_n ∈ K*`, with `n ≥ 2`, **satisfy the Kummer condition** (1.5):
  `[K(√α₁, …, √α_n) : K] = 2ⁿ`.
* `h(α_j)` is the absolute logarithmic height, and `ln α₁, …, ln α_n` are
  arbitrary fixed values of the logarithms.
* `ρ = rank_ℝ {ln α₁, …, ln α_n}`.
* The linear form is `Λ = b₁ ln α₁ + ⋯ + b_n ln α_n`, with `b_j ∈ ℤ` and
  `b_n ≠ 0`.

## Theorem 2.2 (p. 87), the form used

Take `ϑ = 1`, `E = 1` and `C₃ = n/ρ`, and set

    A_j = max{ h(α_j), |ln α_j|/D, 1/(D·C₁) },      1 ≤ j ≤ n,          (2.13)
    B   = max{ |b_j|·A_j/A_n : 1 ≤ j ≤ n },                              (2.14)
    C₀′ = ln( C₂·D·ω / (C₁·A_n) ).                                       (2.15)

Then

    ln|Λ| > −112 · 2ⁿ · C₂ · C₀′ · D² · ω · ln(2eB).                     (2.16)

The constants come from p. 86:

    C₁ = (1 + e^{−2n}/148) · (n ln 2 + 2) · (1 + 1/n) / C₃                (2.4)
    C₂ = 4(n+1) · (6 + 5/(n ln 2 + 2)) · e^{2n} / (n^{1/2} · C₃)          (2.4)
    Ω  = A₁ ⋯ A_n,
    ω  = Ω · (C₁·D·ϑ/e)ⁿ · (C₃·exp(C₃)·E·e/(2ϑ))^ρ                        (2.5)

The paper's own remark after Theorem 2.2 bounds the `n`-dependent factor by
`2¹⁵ (ne/2ρ)^ρ · ρ(2e²ρ ln 2)ⁿ / n^{1/2}`. That agrees with the formulas as
transcribed, which is a consistency check on the transcription.

**Hypotheses of Theorem 2.2 that must be checked in each use.**

* `ϑ = 1` needs (2.1): `ϑ ≥ (1/n) Σ h(α_j)/A_j`. It holds because `A_j ≥ h(α_j)`.
* `E = 1` needs (2.2): `E ≥ (1/(nD)) max |± ln α₁/A₁ ± ⋯|`. It holds because
  `A_j ≥ |ln α_j|/D`.
* `C₃ = n/ρ` needs (2.3): `C₃* exp(C₃*)·Ee/(2ϑ) ≥ e^{n/ρ}` for some
  `C₃* ≤ C₃`. Take `C₃* = n/ρ`; the condition becomes `(n/ρ)(e/2) ≥ 1`, which
  holds since `n ≥ 2` and `ρ ≤ 2`.

## Application: `x² + x + 1 = 3^δ ∏_{t∈T} t^{c_t}`  (`s3k2/39`)

`T` is a set of primes `≡ 1 (mod 3)` and `δ ∈ {0, 1}`.

* **Field and linear form.**
  * `K = ℚ(ω)`, so `D_K = 2`, `κ = 2` and **`D = 1`**.
  * Write `z = x − ω = ε·γ·∏ π_t^{c_t}`, with one of the two primes over each
    `t`.
  * Then `z/z̄ = ζ₆^j · ∏ α_t^{e_t}`, where `α_t = π_t/π̄_t` and `e_t = ±c_t`.
    Units and `(1 − ω)/(1 − ω̄) = −ω` are sixth roots of unity.
  * So the principal value is `Log(z/z̄) = Σ e_t·Log α_t + b₀·Log ζ₆` with
    `b₀ ∈ ℤ`.
  * The `α`'s are `ζ₆` and the `α_t`, so `n = |T| + 1`.
* **`Λ ≠ 0`,** since `z` is not real (its `ω`-coefficient is `−1`).
* **`|Λ|` is small.** `z − z̄ = −√−3`, so `|z/z̄ − 1| = √3/|z|`. For `|z| ≥ 2√3`
  this gives `|Λ| ≤ 2√3/|z|`, with `|z|² = x²+x+1`.
* **`ρ = 1`,** because every `Log α_j` is purely imaginary.
* **Heights.**
  * `h(ζ₆) = 0`.
  * `h(α_t) = ½ log t`, since the minimal polynomial `t X² − (π_t² + π̄_t²) X + t`
    is primitive: `t ∤ π_t² + π̄_t²` because `π_t ∤ π̄_t`. Both roots have
    modulus 1.
* **Kummer condition.**
  * A product `ζ₆^{ε₀} ∏ α_t^{ε_t}` with some `ε_t = 1` has valuation 1 at `π_t`,
    so it is not a square in `K`.
  * `ζ₆` itself is not a square, because `ζ₁₂ ∉ ℚ(ω)`.
  * By Kummer theory for exponent 2, the degree is therefore `2ⁿ`.
* **Which `α` goes last.** `b_n ≠ 0` fixes which `α` must come last. The bound
  used is the **worst case over every admissible choice** of that index.
