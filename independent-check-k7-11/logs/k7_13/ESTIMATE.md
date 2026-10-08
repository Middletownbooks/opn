# Tractability estimate for cr(K_{7,13}) = 324 (measured probes + extrapolation)

Goal: rule out drawings with 320 or 322 crossings. 13-multiset antisums are
always even, so the search target is every 13-multiset M with
Abar(M) + 2τ(M) ≤ 322. (K_{7,12} = 270 already follows from 225 by counting:
12·225/10 = 270 = 9·Z(12).)

## Minimum antisums (window of antisums to search)

* A*(12) ≥ 264: proved. There is no 12-multiset with Abar ≤ 263; this is a
  complete extension of the saved 9-level (`extend_12_263.txt`). The
  averaging bound alone gives 263.
* A*(13) ≥ ⌈13·264/11⌉ = 312, and the parity is even.
* Upper bounds by local search (`localsearch.txt`): A*(12) ≤ 266 (95 hits in
  100k restarts); A*(13) ≤ 318 (816 hits in 200k restarts, never 316).
  Calibration: at m = 11 the true minimum 219 appeared in only 4 of 20k
  restarts, so 316 cannot be excluded this way.

If A*(13) = 318, the case split has exactly the (7,11) shape:

| Abar | τ needed for a counterexample | case |
|---|---|---|
| 322 | τ = 0 | A13 |
| 320 | τ ≤ 1 | B13 |
| 318 | τ ≤ 2 | C13 |

If 316 (or lower) occurs, add τ ≤ 3 (and ≤ 4, ≤ 5) cases, where τ prunes
very little. Alternatively, A*(13) ≥ 318 must first be certified by a search
with no τ cut.

## Measured level sizes (orbits; same code as the (7,11) proof)

| level | (11,7) case B: ≤221, τ≤1 | (13,7) B13: ≤320, τ≤1 | ratio |
|---|---|---|---|
| 6 | 26.9M | 27.8M | 1.0 |
| 7 | 35.2M | 243.7M | 6.9 |
| 8 | 56.2M | 541.6M | 9.6 |
| 9 | 29.5M | not run | — |
| 10 | 0 (lookahead kills all) | not run | — |

A13 (≤322, τ = 0) is level for level the same as the (11,7) top-225 τ = 0
control: 77,029,118 vs 77,038,754 orbits at level 8. That control continues
with 96.0M / 159.7M / 124.4M orbits at levels 9 / 10 / 11 and cost 4.1
core-hours. A13 then adds levels 12 and 13.

C13 (≤318, τ ≤ 2): 65.2M orbits at level 6 and 133.0M at level 7.

Costs measured here (4 cores): B13 level 7 took 10 min wall; B13 level 8
took 65 min wall (4.3 core-hours, ≈ 29 µs per level-8 orbit). B13 up to
level 8 alone is ≈ 5 core-hours, already five times the whole (7,11) proof
(≈ 1 core-hour).

## Why (13,7) is qualitatively harder

In (7,11) the cascade thresholds at levels 8–10 sat just above the minima
(T_10 = 182 vs A*(10) = 178), and the exact one-element lookahead killed
everything at level 10. For (13,7) the thresholds are
[…, 85, 114, 147, 184, 226, 272, 322]. Levels 9–12 therefore have slack
about 6 above their minima, and levels 11 and 12 reach the Zarankiewicz
values 225 and 270. Those layers are huge: the τ = 0 part alone is 124M
orbits at 225. The search must pass through two such layers, which (7,11)
never touched.

## Estimate (my method: cascade + per-candidate τ + case split + canonical augmentation)

* A13: ≈ 5–15 core-hours (≥ the 4.1 core-hour control plus two levels).
* B13: levels 9–12 projected at ~10⁸·⁵–10⁹·⁵ orbits each at 30–60 µs per
  orbit, so ≈ 20–200 core-hours.
* C13: larger lower levels (τ ≤ 2) but a smaller level 11 (Abar ≤ 223), so
  ≈ 30–300 core-hours.
* Certifying A*(13) ≥ 318 (or running the τ ≤ 3 case at 316): the biggest
  unknown. A search with no τ cut through the same Zarankiewicz layers:
  ≈ 10²–10³ core-hours.

**Total ≈ 10² – 10³·⁵ core-hours, a few hundred in the central case.** That
is roughly half a day to a few days on one 32–64-core machine, or 1–4 weeks
on a 16-core workstation. It is 2–3 orders of magnitude more than (7,11)
with the same method. Memory is not the obstacle if augmentation starts at
level ≤ 6. Levels past 8 are extrapolated, not measured, and the τ cut
grows stronger with set size, so the upper end is pessimistic for B13 and
C13.

Engineering needed: 128-bit pair masks (C(13,2) = 78 > 64); 715 4-subsets
per 13-set; augmentation from a low level, since stored levels would exceed
10⁹ orbits; sharding and checkpointing for multi-day runs; and an
independent second run (e.g. a second canonical form), as was done for
(7,11).

For a prefix-tree route that needed "a few days" for (7,11) (roughly
10²–10³ times slower than the above on (7,11)), the same growth factor puts
(7,13) at years of machine time. That is impractical without stronger cuts.
