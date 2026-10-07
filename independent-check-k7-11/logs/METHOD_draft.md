# Independent re-check of "no (11,7)-set has antisum + 2·tau below 225"

Everything in this directory was written from the task specification alone.
No existing implementation of the search was read, requested or consulted
(no file of the surrounding repository was opened; the work lives in this new
directory only).

## Code

* `rust/` — the main implementation (Rust; no external crates).
  * `src/co.rs` — CO_n from Woodall's definition: vertices = cyclic orders
    with 0 rotated to the front; edges = transposition of the elements at
    cyclic positions i, i+1 (mod n, wrap-around included), labelled by the
    transposed pair; BFS distances; `rev`; AND/OR of the label sets of all
    shortest a→rev(b) paths (DP over the geodesic DAG), plus an *explicit*
    enumerator of those label sets used to cross-check the DP; the four route
    families on CO_4 (both / walk / path / arbitrary).
  * `src/pt.rs` — pseudo-tightness of a (4,n)-set. FORCED(g) / POSS(g) for
    each ground pair g come from the AND / OR masks; compatibility of
    (N[x], N[y]) = "some N[x]→rev(N[y]) route in CO_4 has a label set L with
    FORCED ⊆ L ⊆ POSS"; existence of N is decided by backtracking with forward
    checking, and (for cross-checks) by exhaustive search over all 6^n
    assignments.
  * `src/sym.rs` — the group G = S_7 × ⟨rev⟩ (10080 elements, each verified
    to preserve dbar on all 720² pairs) and the canonical form.
  * `src/search.rs` — the cascade enumeration, the lookahead cut, the τ cut,
    the 4-subset hypergraph and an exact minimum-transversal solver.
* `python/pt_crosscheck.py` — a second, deliberately naive implementation of
  the pseudo-tightness test sharing no code with the Rust one (tuples and
  frozensets, explicit label-set enumeration, BFS over (vertex, label-set)
  states, brute force over all 6^7 assignments with numpy, its own
  transversal search).
* `python/compare_dumps.py` — compares survivor lists.

Antipath reading used throughout: **arbitrary walks** (the conservative
choice). The zero-length walk is included (it is a route in every reading).

## Enumeration: the cascade (not a prefix tree)

For an m-multiset M and v ∈ M let c_M(v) = Σ_{u ∈ M−v} dbar(u,v). Then
Σ_v c_M(v) = 2·Abar(M), so the element v of largest contribution satisfies
c_M(v) ≥ ⌈2·Abar(M)/m⌉ and

    Abar(M − v) ≤ Abar(M) − ⌈2·Abar(M)/m⌉.

The right-hand side is non-decreasing in Abar(M) (m ≥ 2). So with
T_{k−1} = T_k − ⌈2T_k/k⌉, every M with Abar(M) ≤ T_m is obtained from an
(m−1)-multiset with antisum ≤ T_{m−1} by adding a max-contribution element.
Level L_k is built from L_{k−1} by adding every one of the 720 vertices to
every representative, keeping X+v when Abar(X+v) ≤ T_k and v is a
max-contribution element of X+v, then canonicalising and de-duplicating. By
induction L_k contains a representative of every G-orbit of k-multisets with
Abar ≤ T_k — and nothing else, so (without the extra cuts below) |L_k| is the
number of such orbits, a number that does not depend on the canonical form.

### Canonical form

The lexicographically smallest sorted tuple of vertex indices among the 10080
images g(M). It starts with as many 0s as the largest multiplicity in M (more
leading zeros is lexicographically smaller and G is transitive), so only the
14 group elements sending each max-multiplicity element to vertex 0 need to be
scanned. It is a true orbit invariant (the scanned set of images depends only
on the orbit), and distinct orbits get distinct forms (each form is a member
of its orbit). With `--relabel SEED` the 720 vertex indices are pseudo-randomly
permuted first, which gives a *different* canonical form.

### Extra cut 1: lookahead (sound for every reading, independent of PT)

For S ⊆ M with r = |M| − |S| > 0,

    Abar(M) = Abar(S) + Σ_{v ∈ M−S} c_S(v) + Abar(M−S) ≥ Abar(S) + r·μ(S) + A*(r),

with μ(S) = min over **all** 720 vertices w of c_S(w), and A*(r) any lower
bound on the antisum of r-multisets. Both sides are G-invariant, so a level
member failing Abar(S) + r·μ(S) + A*(r) ≤ T cannot be a chain set of any
M with Abar(M) ≤ T.

A*(r) values used: A*(0..9) = 0,0,0,9,18,36,54,79,107,140, each computed by
this same cascade (run at T = 9·Z(r), the Zarankiewicz value, which is an
upper bound; the cascade is complete, so the minimum it finds is the minimum).
Beyond that, A*(r) ≥ ⌈r·A*(r−1)/(r−2)⌉ (from Σ_v Abar(M−v) = (r−2)·Abar(M)),
giving A*(10) ≥ 175, A*(11) ≥ 214. (A*(7) = 79 and A*(9) = 140 agree with the
figures in the task.)

### Extra cut 2: τ (the search for counterexamples)

To find every orbit with Abar(M) + 2τ(M) ≤ T: if M is such a set and M_k is
any member of its deletion chain, then τ(M_k) ≤ τ(M) (a transversal of M's
non-pseudo-tight family, restricted to the pairs inside M_k, is a transversal
of M_k's family), so Abar(M) ≤ T − 2τ(M_k). Every cut above is therefore
applied to M_k with top value T_eff = T − 2τ(M_k): the averaging threshold
(T_k is monotone in the top value) and the lookahead. When
T − 2τ < A*(m) the set is discarded outright. τ is G-invariant, so this is
compatible with canonicalisation. τ(S) is computed exactly up to that kill
value by branch and bound (cross-checked against brute force).

## Soundness of the "2·tau" sharpening

Let D be a good drawing corresponding to M. Crossings of D are partitioned by
the unordered pair of m-side stars they involve (each crossing is between
edges ax and by with a ≠ b), so cr(D) = Σ_{pairs} cr_D(a,b). By Woodall's
Theorem 5, cr_D(a,b) ≥ dbar(a,b) and cr_D(a,b) ≡ dbar(a,b) (mod 2), so
cr_D(a,b) ∈ {dbar, dbar+2, …}. Let B = {pairs with cr_D ≥ dbar + 2}. Then
cr(D) ≥ Abar(M) + 2|B|. A (4,n)-subset whose six pairs all attain their
antidistance is tight (Woodall's argument: the sub-drawing of K_{4,n} on those
four stars supplies N, the P_ab and the Q_xy; crossing counts between two
stars do not depend on the other stars), hence pseudo-tight; so every
non-pseudo-tight 4-subset contains a pair of B. B is a transversal of that
family, |B| ≥ τ(M), and cr(D) ≥ Abar(M) + 2τ(M). I find this step correct.
For repeated elements everything is at the level of indices (pairs and
4-subsets of positions), which is what the code does.
