# Ideas for making (7,13) cheaper — what was tested, and results

All three cuts below are opt-in environment switches in the Rust code
(`COK_PARITY=1`, `COK_EXACT2=1`, `COK_EXACT3=1`). Each reproduces the exact
(7,7)/81 survivor set: the same 460,618 orbits as the unpruned enumeration.

## 1. Parity-aware cascade thresholds — sound, free, large gain

Antisums of odd-size multisets have fixed parity. The recursion
T_{k−1} = T_k − ⌈2T_k/k⌉ should first lower T_k to the largest value of the
correct parity. My earlier code did that only at the top. For B13 the
thresholds change from […, 60, 85, 114, 147, …] to […, 59, 83, 113, 146, …].

| B13 (Abar ≤ 320, τ ≤ 1) | before | with parity |
|---|---|---|
| level 6 | 27.8M | 11.1M |
| level 7 | 243.7M | 36.8M |
| level 8 | 541.6M | 211.7M |
| cost up to level 8 | ≈ 4.9 core-hours | ≈ 1.2 core-hours |

On the (11,7) top-225 τ = 0 control, level 7 drops from 29.4M to 5.1M.

## 2. Exact lookahead for the last two elements — sound, huge gain below the optimum

The old lookahead r·μ(S) + A*(r) lets all r new elements sit at the cheapest
vertex and be mutually antipodal at once. For r = 2 the exact value
min_{w1,w2} c(w1) + c(w2) + dbar(w1,w2) is cheap: sort by c and prune.

| run | level 9 before | level 9 with exact r = 2 | survivors |
|---|---|---|---|
| (11,7) case B (top 221, 4 below optimum 225) | 29,502,925 | **1,602** | 0 = 0 |
| (11,7) case A (top 223, 2 below optimum) | 8,476,729 | **436,284** | 0 = 0 |
| (11,7) top-225 control (target = optimum) | 96.0M | 84.7M | (control) |

The collapse happens when the target is below the optimum, which is exactly
the (7,13) situation (322 < 324). The Zarankiewicz 11-set's best two-element
completion gives 225 + 99 = 324. So the Zarankiewicz layers at levels 11–12,
the dominant projected cost, should largely disappear.

Exact r = 3 (pruned triple loop, per candidate) was **too slow as
implemented**: over 30 minutes at a level that takes 54 s without it, and it
was aborted before giving a count. It needs evaluation per orbit after
de-duplication, and a better algorithm.

## 3. Tightness instead of pseudo-tightness — tested, no gain

| sets | non-PT 4-subsets | non-tight 4-subsets | τ changes |
|---|---|---|---|
| (7,7), all 13,448 at Abar 79 | 219,826 | 219,828 | none |
| 3000 (7,7) Abar-81 τ = 0 sets | 0 | 0 | none |
| 20 (11,7) Abar-225 τ = 0 sets, 219 set, Zarankiewicz | — | — | none |

Pseudo-tightness already captures essentially everything 4-subsets can say.
The cost lies in near-optimal configurations, which local predicates do not
reject. (5-subset pseudo-tightness is untested and expected to behave the
same near the optimum.)

## Revised projection for (7,13), single pass (measured through level 8; levels 9+ extrapolated)

* B13: levels 9–10 are the remaining cost, ≈ 5–12 core-hours. Level 11,
  with exact r = 2, should collapse as above, and levels 12–13 are then
  negligible. Total ≈ 7–15 core-hours, down from 20–200.
* C13 ≈ 10–30 core-hours; A13 ≈ 3–6.
* The region below 318 (τ ≥ 3) remains the main unknown. Exact lookahead
  applies there too, since it is also below the optimum.

Overall: **a few tens of core-hours per pass** (uncertainty ±3× or more),
compared with 10²–10³·⁵ before.

## Running it on many short sessions (e.g. Kaggle CPU notebooks)

* Shards need no shared state. Canonical augmentation makes every stored
  frontier orbit's subtree independent. With parity, the B13 frontier at
  level 7 (36.8M orbits) is regenerated deterministically in about 3 min of
  wall time in every session, so nothing has to be uploaded between sessions.
* Session i processes the frontier orbits with index ≡ i (mod N),
  interleaved to spread the heavy tail. It writes a small result file: shard
  id, number of parents done, nodes per level, survivors, wall time, binary
  hash.
* Size each shard so a session finishes well inside its time limit, and stop
  at a wall-clock deadline after writing the completed range. Output of a
  session killed at the limit may not be saved.
* Memory is small: the frontier (≤ 1 GB) plus the 47 MB PT table.
* Use a static (musl) release binary built for x86-64-v2 or v3, uploaded as
  a dataset.
* Completeness ledger: every shard present, and per-shard parent counts sum
  to the frontier size. Verification: a second full pass under a relabelled
  canonical form (seed), which must also give 0 survivors.
