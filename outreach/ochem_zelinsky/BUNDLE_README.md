# Re-checking §4 of arXiv:2607.19746: programs and results

This bundle accompanies a note about Ochem & Zelinsky, *On odd perfect numbers with
exactly one even exponent greater than 2*, arXiv:2607.19746v1. Everything here can
be re-run with `gcc` and `python3` alone. Nothing needs GMP or any other library,
except building your own `loopless.cpp` for comparison.

The file names match the repository they come from; the numbers are that
repository's script numbers. Timings are from a single core of a 4-core cloud
container with 15 GB of RAM.

## Files

| file | what it is |
|---|---|
| `13_sieve.c` | An independent C implementation of Algorithm 1. It never forms `r² + r + 1`: each `q ∈ M₂` marks the `r ≡ ρ, q−1−ρ (mod q)`, with `ρ` a primitive cube root of unity mod `q`. The header states and proves the two reductions it uses. |
| `12_algorithm1_reference.py` | A plain Python implementation of Algorithm 1 for small ranges, used to check `13`. |
| `14_bound_from_run.py` | Turns `13`'s checkpoint lines `(x, k(x), ln A(x))` into `K_max`, `k + K_max`, and the resulting bound on `q`, following §4 of the paper. |
| `05_loopless_overflow.py` | Shows the 64-bit wrap in `check_M2` of `loopless.cpp` on the first primes above `2³²`. |
| `11_wrap_signature.py` | The statistical signature of the wrap in the published `k` and `A`, and the mechanism behind it. |
| `10_section4_reconcile.py` | The arithmetic of the final product in §4. |
| `15_tree_pilot.py` | An independent re-check of the claim that every prime `11 … 3·10⁶` is ruled out (the role of `tree.txt`). It uses the method of `tree.cpp` but none of its code. |
| `loopless_build/gmp.h` | Used only to build your **unmodified** `loopless.cpp` where GMP's header is not installed. It declares the GMP functions the program uses, so the program links against the system `libgmp.so.10`. You will not need it if GMP's development files are installed. |
| `results/` | Our outputs, for comparison. |

## 1. The overflow (seconds)

In `loopless.cpp`, `check_M2` computes `u64 val = r * r + r + 1;` (line 135 of the
file with its original line breaks). For `r ≥ 2³²` this wraps modulo `2⁶⁴`, and
`get_factors` takes a `u64` in any case. The reported run went to
`z = 216,171,986,291 ≈ 50 · 2³²`.

    python3 05_loopless_overflow.py

## 2. Our sieve agrees with `loopless.cpp` wherever `loopless.cpp` is exact

    gcc -O3 -march=native -o sieve 13_sieve.c -lm
    ./sieve 4294967296 4294967297 > exact_2p32.txt        # 87 s; exact Algorithm 1 up to 2^32

It prints progress lines in `loopless.cpp`'s own format, every 10,000 survivors.
Your program, run unchanged, should print the same lines. Two to compare:

    k: 2530000  | r: 579733409  | A: 1.028007677068       (about 1 hour of loopless.cpp here)
    k: 15650000 | r: 4293066907 | A: 1.035513576704       (the last line before 2^32)

At `2³²` exactly: `k = 15,656,368` and `ln A = 0.0348989960116071389…`
(`A = 1.035515112361`). The file `results/loopless_released_1h.txt` holds one hour
of your unmodified program's output. It agrees with ours on all 253 lines, up to
`r = 579,733,409`. We built it with:

    g++ -O3 -I loopless_build -o loopless loopless.cpp /usr/lib/x86_64-linux-gnu/libgmp.so.10

The Python reference agrees with `13` line for line (about 35 s):

    python3 12_algorithm1_reference.py 200000000 > ref.txt
    ./sieve 200000000 200000001 > c.txt
    diff <(grep '^k:' ref.txt) <(grep '^k:' c.txt)     # no output

## 3. The corrected run to your `z`

    ./sieve 216171986291 34359738368 0 > run_z.txt      # about 55 min, 6 GB
    python3 14_bound_from_run.py run_z.txt

The second argument `Q = 2³⁵` exists for memory: a prime `q ∈ M₂` with `q ≥ Q` is
not used to exclude anything.
- The run is therefore **exact for `r < 2³⁵ ≈ 3.4·10¹⁰`**.
- Above that it keeps a **superset** of Algorithm 1's survivors (induction in the
  header of `13_sieve.c`).
- So the `k(z)` and `A(z)` below are upper bounds for Algorithm 1's exact values.
  A superset of the survivors still gives a valid count, because every possible
  ordinary prime below `z` is among them.

Expected (`results/14_bound_z_Q2e35.txt`):

    x = 216,171,986,291   k = 599,351,328   A = 1.047357816316
    K_max = 52,186,355,564   k + K_max = 52,785,706,892   q >= 26,392,853,446

Here `K_max` is the largest `K` with
`3/2 · (1 + 1/6·10⁶) · A · (1 + 1/z)^K < 2`. The number of ordinary primes is at
least `k + K_max + 1`. Then Lemma 8 applies, with `ω(N) = 2 + (ordinary primes)`
and `q` even.

## 4. Further: `z = 10¹²`

    ./sieve 1000000000000 34359738368 0 > run_1e12.txt  # about 3.8 h, 6 GB
    python3 14_bound_from_run.py run_1e12.txt

Expected (`results/14_bound_1e12_Q2e35.txt`):

    x = 10^12   k = 2,670,032,132   A = 1.051620849343
    k + K_max = 240,019,297,934   q >= 120,009,648,966

Its checkpoints up to `216,171,986,291` are identical to those of the run in §3.

## 5. The wrap's signature in the published numbers

    python3 11_wrap_signature.py 10000 7               # about 1 min

## 6. Every prime `11 … 3·10⁶` is ruled out

    NOHINTS=1 python3 15_tree_pilot.py 11 3000000     # about 4.5 CPU-hours; split the range to parallelise

This ignores `checkfacts.txt` entirely. It rules out every root except 502013 and
2152883, where its own factoring (Pollard–Brent, then ECM) runs out of budget. With
your `checkfacts.txt` beside the script, both are ruled out. Each hint is checked
to divide and to be a probable prime before use:

    python3 15_tree_pilot.py 502013 502013
    python3 15_tree_pilot.py 2152883 2152883

Our output is in `results/15_tree_full_range.txt`. Separately, all 460 entries of
`checkfacts.txt` verify: each listed factor divides its `x² + x + 1` or `x + 1`
and is a probable prime.

## 7. The final product in §4

    python3 10_section4_reconcile.py
