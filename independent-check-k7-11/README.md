# Independent check: no (11,7)-set has antisum + 2·τ below 225

**Result of this re-implementation: confirmed.** No (11,7)-set M with
Abar(M) ≤ 223 has Abar(M) + 2τ(M) < 225. Together with the Zarankiewicz
drawing this gives cr(K_{7,11}) = 225, *provided* Woodall's Theorems 5 and 6
hold as stated in the task (I did not re-derive them; see "Not verified").

Everything here was written from the task's specification. I did not read,
request or look for any existing implementation, and did not open any other
file of this repository. The main code is Rust (no external crates). The
pseudo-tightness test was also written a second time, naively, in Python, to
cross-check it. Antipaths are **arbitrary walks** throughout, including the
zero-length walk.

## My numbers (stated before any comparison)

| quantity | my value | figure in the task |
|---|---|---|
| CO_7: vertices, regularity, diameter | 720, 7-regular, 9; rev(a) the unique vertex at distance 9 | 720, 7-regular |
| dbar(a,a), dbar(a,rev a) | 9, 0 for all a | 9, 0 |
| CO_7 bipartite, rev swaps classes, dbar ≡ 1+col a+col b | yes (all 720² pairs) | yes |
| CO_4 route families both / walk / path / arbitrary | 234 / 282 / 594 / 1758 | 234 / 282 / 594 / 1758 |
| (4,6) example: antidistances | (3,4,2,3,2,1), antisum 15 | same |
| (4,6) example: #shortest-antipath label sets | (1,3,1,1,1,1) | same |
| (4,6) example pseudo-tight | yes, under all four readings | yes |
| (7,7): minimum antisum | 79 | 79 |
| (7,7): orbits at 79 under S_7×⟨rev⟩ | **13,448** (26,770 under S_7 alone; 134,920,800 labelled multisets) | 13,448 |
| (7,7): min t over those | **10** (t ∈ [10,29]; τ ∈ {3,4,5}) | 10 |
| (7,7): sets with Abar+2τ < 81 | 0 (min Abar+2τ = 85) | 0 |
| (9,7): minimum antisum | 140 | 140 |
| (9,7): orbits at 140 / 142 | 82 / 2,711,216 | — |
| (9,7): sets with Abar+2τ < 144 | 0 (min Abar+2τ = 148) | 0 |
| Zarankiewicz 5a+6rev(a) | antisum 225, t = 0, for every one of the 720 a | 225, t = 0 |
| antisum-219 representative: matrix | identical to the stated matrix | — |
| … t, τ | **t = 103, τ = 8** (bound 235) | 103, 8 |
| (11,7): minimum antisum | **219** | 219 |
| (11,7): orbits with Abar ≤ 219 | **exactly 1**, of size **5040** (stabiliser of order 2, containing a reversing element) | 1 orbit, 5040 |
| (11,7): counterexamples (Abar ≤ 223, Abar+2τ < 225) | **0** | 0 |

Minimum antisums A*(k) of (k,7)-sets, each from a complete enumeration:
A*(1..11) = 0, 0, 9, 18, 36, 54, 79, 107, 140, 178, 219. The numbers of orbits
at the minimum are 1, 1, 159, 61, 96,821, 6,045, 13,448, 1,069, 82, 267, 1.

I found no disagreement with any figure in the task. The (4,6) example, t = 103,
τ = 8 and the CO_4 family sizes were each reproduced independently by the
Python implementation.

## What was computed, and why it is a proof

Antisums of 11-multisets are always odd (C(11,2) = 55, and the colour term
has the even coefficient 10). So a counterexample satisfies
Abar + 2τ ≤ 223. It falls into one of three cases, each settled by its own
complete search:

| case | what is searched | result | cost |
|---|---|---|---|
| **C** Abar ≤ 219 | every orbit with Abar ≤ 219, no τ cut | 1 orbit (the stated one), τ = 8, so its bound is 235 | 2 min wall (generating level 9) + 1.4 s |
| **B** Abar = 221 ⇒ τ ≤ 1 | every orbit with Abar ≤ 221 and τ ≤ 1 | **0** | 9 min 44 s wall, 37.5 core-min |
| **A** Abar = 223 ⇒ τ = 0 | every orbit with Abar ≤ 223 and τ = 0 | **0** | 2 min wall, 7.6 core-min |

Total for the claim: about 15 minutes wall and under one core-hour on 4 cores.
The figure the task gives for the original route is about 9 core-hours.

### Enumeration method: a cascade, not a prefix tree

For an m-multiset M write c_M(v) = Σ_{u∈M−v} dbar(u,v). Since
Σ_v c_M(v) = 2·Abar(M), deleting a max-contribution element gives
Abar(M−v) ≤ Abar(M) − ⌈2·Abar(M)/m⌉. The right-hand side is non-decreasing
in Abar(M). So with T_{k−1} = T_k − ⌈2T_k/k⌉, every M with Abar(M) ≤ T_m has
a chain M_1 ⊂ M_2 ⊂ … ⊂ M_m = M with Abar(M_k) ≤ T_k, in which each step adds
a max-contribution element. Level L_k is built from L_{k−1} by trying all 720
vertices on every representative, keeping X+v only if

1. Abar(X+v) ≤ T_k,
2. v is a max-contribution element of X+v (sound: g maps the chain's added
   element to such an element of the representative),
3. the lookahead holds (below),
4. the τ conditions hold (below),

then canonicalising and de-duplicating. Every cut is G-invariant and is
satisfied by every chain set of every target M. So by induction L_k contains
a representative of every chain-set orbit, and the top level contains every
target orbit.

**Canonical form.** The lexicographically smallest sorted tuple of vertex
indices among all 10080 images. It begins with as many copies of vertex 0 as
the largest multiplicity in M, so only the 14 group elements sending each
max-multiplicity element to 0 need to be scanned. The given 219
representative is already lex-min under my default vertex numbering, so the
original may well use the same convention. Every result was therefore
**repeated under a second canonical form**: lex-min after a pseudo-random
relabelling of the 720 vertex indices (seed 987654321, under which vertex 0
is 0165342). All orbit counts, level by level, are identical. The level
counts are orbit counts of G-invariant sets, so they *must* be identical if
both runs are correct. The relabelled run's 219 representative is a
different tuple, and it maps back to the stated one.

**Lookahead** (sound for every antipath reading). For S ⊆ M with
r = |M|−|S| > 0:

  Abar(M) = Abar(S) + Σ_{v∈M−S} c_S(v) + Abar(M−S) ≥ Abar(S) + r·μ(S) + A*(r),

where μ(S) is the minimum over **all** 720 vertices w of c_S(w).
The values A*(r) come from complete runs of this same cascade (run at
T = 9·Z(r), which a Zarankiewicz multiset attains). A*(10) = 178 comes from
extending the complete list of 9-orbits with Abar ≤ 142.

**τ conditions.** τ is monotone under taking sub-multisets: a transversal of
M's non-pseudo-tight family, restricted to the pairs inside S, is a
transversal of S's family. So for a target M and any chain set S,
Abar(M) ≤ min(T − 2τ(S), cap). Every cut above is applied to S with that top
value, and τ(S) ≥ the τ limit of the case discards S. τ(S) is computed
exactly up to the needed cap by branch and bound, which was cross-checked
against brute force.

**Case C** uses no τ at all. Every 11-set with Abar ≤ 219 has a chain set at
level 9 with Abar ≤ T_9 = 143, hence ≤ 142 by parity (9-multiset antisums are
even). The complete list of all 2,711,298 9-orbits with Abar ≤ 142 was
generated once and extended by two levels.

**Speed.** Pseudo-tightness is G-invariant, which I checked exhaustively:
FORCED/POSS masks are equivariant for all 10080 g and all 720² pairs, with 0
violations. Hence PT(a,b,c,d) = PT(0, g b, g c, g d) for any g with g(a) = 0.
A 720³-bit table (47 MB, built in 7 s) turns each test into a lookup; it
agrees with the direct test on 2,000,000 random 4-multisets. All final
survivors are re-verified with the direct test, never the table.

### Level counts (orbits kept per level; canonical-form independent)

| level | case A (≤223, τ=0) | case B (≤221, τ≤1) |
|---|---|---|
| 2 | 21 | 21 |
| 3 | 912 | 912 |
| 4 | 56,085 | 92,530 |
| 5 | 935,682 | 4,265,471 |
| 6 | 3,444,625 | 26,897,890 |
| 7 | 5,062,946 | 35,192,903 |
| 8 | 11,546,630 | 56,218,406 |
| 9 | 8,477,729 | 29,502,925 |
| 10 | 0 | 0 |
| 11 | **0** | **0** |

Candidates tried, and the number removed by each cut, are in `logs/caseA_*`
and `logs/caseB_*`. In both cases level 10 dies at the r = 1 lookahead. That
lookahead is exact: the best possible 11th element is tried. In case A, no
10-multiset with all 4-subsets pseudo-tight and Abar ≤ 182 can be completed
to antisum ≤ 223. Case C's levels: 2,711,298 (level 9) → 4 (level 10) → 1
(level 11).

## Self-checks and cross-checks (all passed)

* All seven requested self-checks (logs: `selfcheck_output.txt`,
  `run_7_7.txt`, `run_9_7.txt`, `extend_11_219.txt`).
* The shortest-antipath AND/OR dynamic programme equals AND/OR over
  explicitly enumerated label sets: 3000 random CO_7 pairs (including all
  (a,a)) and all 120² CO_6 pairs.
* Backtracking PT solver = exhaustive 6^7 search on 400 random 4-sets.
  PT is invariant under reordering the four elements and under G (sampled),
  and the masks are exactly equivariant under all of G (exhaustive).
* The Python implementation agrees with Rust on 400 random 4-multisets
  (43 non-PT), and on t = 103, τ = 8 and the Zarankiewicz t = 0.
* **τ-pruning validated against no pruning.** At (7,7) top 81, the τ-pruned
  search, the per-candidate τ search and the depth-first variant each return
  exactly the same 460,618 orbits (Abar 81, τ = 0). These are the orbits that
  an unpruned enumeration of all 25,804,868 + 13,448 orbits with Abar ≤ 81
  selects after computing τ for every one of them. At (9,7), the unpruned run
  (24 min) and the τ-pruned runs (97 s and 14 s) all find 0 counterexamples.
* The lookahead leaves complete levels unchanged: (9,7) level 9 has 2,711,298
  orbits with and without it.
* Positive controls: every Zarankiewicz multiset has t = 0. The τ-pruned
  search keeps 460,618 orbits at (7,7)/81. The (11,7) top-225 τ = 0 control
  is in the section below.
* Two more completion mechanisms agree with breadth-first de-duplication on
  the final survivor sets:
  * depth-first expansion with de-duplication only at the top (460,618
    identical orbits at (7,7)/81);
  * canonical augmentation, where each orbit is accepted only from its
    canonical parent (460,618 at (7,7)/81; 0 at (9,7)/142).

  Their *intermediate* counts can be lower than the breadth-first ones. A
  node that is a subset of no target may have a canonical parent that was
  cut while another max-contribution deletion survived. I checked this
  explanation directly: at (9,7)/142, exactly 806,098 of the 807,358
  breadth-first level-5 orbits have their canonical parent in level 4, which
  is the augmentation count (`logs/check_augment_9_142.txt`).

## Positive control at top 225 for (11,7)

I ran case A's search with the top raised from 223 to 225 (τ = 0, all
Abar ≤ 225). It keeps **124,368,968 orbits, all at antisum 225**. None are at
≤ 223, consistent with case A.

* Levels 2–8 are breadth-first and identical to case A's code path. The
  level-8 count is 77,038,754.
* Levels 9–11 used canonical augmentation, visiting 95,992,501 /
  159,701,116 / 124,368,968 orbits. That took 63 min wall and 4.1 core-hours.
* 64 sampled survivors were re-checked with the direct (non-table) PT test:
  all have t = 0 and τ = 0.
* The Zarankiewicz multiset 5a + 6·rev(a) is traced link by link through
  every cut of this search (`logs/trace_zarankiewicz_225.txt`). The same
  trace at T = 223 stops only at the last link, because its antisum is 225.

Two earlier attempts to store the whole top level ran out of memory
(`logs/posA_*aborted*`; one restarted the container). This is only the τ = 0
part of the full top-225 survivor set. I did not run the parts with
Abar 223/τ ≤ 1 and Abar 221/τ ≤ 2 at top 225.

## Is the "2·τ" sharpening sound?

Yes, I agree with it. Crossings of a good drawing D are partitioned by the
pair of m-side stars involved, so cr(D) = Σ_pairs cr_D(a,b). By Theorem 5,
cr_D(a,b) ∈ {dbar, dbar+2, …}. If B is the set of pairs with
cr_D ≥ dbar+2, then cr(D) ≥ Abar + 2|B|. A 4-subset all of whose six pairs
attain dbar is tight (Woodall's argument, as quoted in the task), hence
pseudo-tight. So B meets every non-pseudo-tight 4-subset, |B| ≥ τ, and
cr(D) ≥ Abar + 2τ, with the same parity. With repeated elements everything
is done on positions, which is what the code does.

## Not verified

* Woodall's Theorem 5 (pairwise bound and parity) and the step "a 4-subset
  whose pairs all attain their antidistance in a drawing is tight". I used
  them as stated; I checked only the counting step from there to Abar + 2τ.
* That the definitions in the task (CO_n, antipaths, the (pseudo-)tightness
  quantifiers) match Woodall's paper. I implemented them exactly as quoted.
* Only the arbitrary-walk reading was used for the main search. The other
  readings give larger t (e.g. 104 for the 219 set under "both" and "path"),
  so the bound could only increase under them. I did not run them.
* The code was not formally verified. Correctness rests on the arguments
  above and the cross-checks listed. The PT solver, label-set dynamic
  programme and transversal solver were each checked against independent
  brute force; the enumeration was checked against counts that don't depend
  on the canonical form (13,448; 1 orbit of 5040) and against a second
  canonical form.
* The top-225 positive control covers only its τ = 0 part (above).
* I did not compare against the original program's own node/leaf counts or
  survivor counts (I was not given them). Its tree differs from mine, so only
  the orbit-level counts reported here are comparable.

## Reproducing

```
cd rust && cargo build --release            # binary: target/release/cokcheck
cokcheck selfcheck                           # checks 1,2,3,6a,7 + cross-checks
cokcheck equivariance                        # exhaustive G-equivariance of FORCED/POSS
cokcheck enumerate 7 80 81                   # (7,7): 13,448 orbits at 79, min t = 10
cokcheck enumerate 9 142 144                 # (9,7) unpruned, 0 below 144
A=0,0,0,9,18,36,54,79,107,140,178,219
cokcheck enumerate 9 142 144 --astar 0,0,0,9,18,36,54,79,107 --noanalyze --save-level 9 --save-file L9.bin
cokcheck extendfrom L9.bin 9 142 10 178 --astar 0,0,0,9,18,36,54,79,107,140                 # A*(10) = 178
cokcheck extendfrom L9.bin 9 142 11 219 --target 225 --astar 0,0,0,9,18,36,54,79,107,140,178 # case C
cokcheck enumtau2 11 223 --astar $A --taumax 0                # case A
cokcheck enumtau2 11 223 --astar $A --taumax 1 --abmax 221    # case B
# add --relabel 987654321 to any of these for the second canonical form
python3 python/pt_crosscheck.py selftest
```
