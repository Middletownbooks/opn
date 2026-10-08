//! Cascade enumeration of (m,n)-sets with antisum <= T, and per-orbit
//! pseudo-tightness / transversal analysis.
//!
//! Soundness of the cascade.  For an m-multiset M (m >= 2) and v in M write
//! c_M(v) = sum_{u in M - v} dbar(u,v).  Then sum_v c_M(v) = 2 Abar(M), so the
//! element v of largest contribution has c_M(v) >= ceil(2 Abar(M)/m) and
//!     Abar(M - v) = Abar(M) - c_M(v) <= Abar(M) - ceil(2 Abar(M)/m).
//! The right side is non-decreasing in Abar(M) (for m >= 2), so with
//!     T_{m-1} = T_m - ceil(2 T_m / m)
//! every M with Abar(M) <= T_m is "max-contribution element added to an
//! (m-1)-set with antisum <= T_{m-1}".  L_k is built from L_{k-1} by adding
//! every vertex v of CO_n to every representative X, keeping X+v if
//! Abar(X+v) <= T_k and v is a max-contribution element of X+v, and
//! canonicalising.  Induction on k shows L_k holds a representative of every
//! G-orbit of k-multisets with Abar <= T_k; and every element of L_k does
//! satisfy Abar <= T_k, so L_k is exactly that set of orbits.

use crate::co::Co;
use crate::pt::PtTester;
use crate::sym::{pack, unpack, Sym};
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};
use std::sync::Mutex;

pub struct Ctx {
    pub co: Co,
    pub dbar: Vec<u8>,
    pub fa: Vec<u32>,
    pub fo: Vec<u32>,
    pub sym: Sym,
    pub pt: PtTester,
}

pub fn thresholds(m: usize, t: u32) -> Vec<u32> {
    let mut th = vec![0u32; m + 1];
    th[m] = t;
    for k in (2..=m).rev() {
        let tk = th[k];
        th[k - 1] = tk - (2 * tk + k as u32 - 1) / k as u32;
    }
    th
}

pub struct LevelStats {
    pub parents: usize,
    pub candidates: u64,
    pub after_filter: u64,
    pub lookahead_cut: u64,
    pub t0_cut: u64,
    pub orbits: usize,
}

/// Lookahead cut (optional).  For S a sub-multiset of the final m-multiset M
/// with r = m - |S| > 0 elements still to come,
///     Abar(M) = Abar(S) + sum_{v in M-S} c_S(v) + Abar(M-S)
///            >= Abar(S) + r * mu(S) + astar[r],
/// where mu(S) = min over ALL vertices w of c_S(w) and astar[r] is a lower
/// bound on the antisum of any r-multiset.  Both sides are G-invariant, so
/// discarding an S with Abar(S) + r mu(S) + astar[r] > T loses no orbit of
/// m-multisets with Abar <= T.
pub struct Lookahead<'a> {
    pub m: usize,
    pub t: u32,
    pub astar: &'a [u32],
}

pub fn extend_level(ctx: &Ctx, parents: &[u128], k: usize, t_child: u32, nthreads: usize, look: Option<&Lookahead>) -> (Vec<u128>, LevelStats) {
    extend_level_ex(ctx, parents, k, t_child, nthreads, look, false)
}

/// `require_t0`: parents are known to have t = 0 (every 4-subset pseudo-tight);
/// keep a child X+v only if every 4-subset containing the new copy of v is
/// pseudo-tight too, i.e. t(X+v) = 0.
pub fn extend_level_ex(ctx: &Ctx, parents: &[u128], k: usize, t_child: u32, nthreads: usize, look: Option<&Lookahead>, require_t0: bool) -> (Vec<u128>, LevelStats) {
    let nv = ctx.co.nv;
    let dbar = &ctx.dbar;
    let next = AtomicUsize::new(0);
    let cand = AtomicU64::new(0);
    let filt = AtomicU64::new(0);
    let lookcut = AtomicU64::new(0);
    let t0cut = AtomicU64::new(0);
    let results: Mutex<Vec<Vec<u128>>> = Mutex::new(Vec::new());
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut out: Vec<u128> = Vec::new();
                let mut limit = 1usize << 24;
                let mut c = vec![0u16; nv];
                let mut x = [0u16; 16];
                let mut child = [0u16; 16];
                let mut best = [0u16; 16];
                let mut cx = [0u16; 16];
                let (mut lc, mut lf, mut ll, mut lt0) = (0u64, 0u64, 0u64, 0u64);
                loop {
                    let start = next.fetch_add(256, Ordering::Relaxed);
                    if start >= parents.len() {
                        break;
                    }
                    let end = (start + 256).min(parents.len());
                    for pi in start..end {
                        unpack(parents[pi], k, &mut x);
                        let mut ab = 0u32;
                        for i in 0..k {
                            for j in i + 1..k {
                                ab += dbar[x[i] as usize * nv + x[j] as usize] as u32;
                            }
                        }
                        if ab > t_child {
                            continue;
                        }
                        for e in c.iter_mut() {
                            *e = 0;
                        }
                        for i in 0..k {
                            let row = &dbar[x[i] as usize * nv..(x[i] as usize + 1) * nv];
                            for (cv, &d) in c.iter_mut().zip(row.iter()) {
                                *cv += d as u16;
                            }
                        }
                        for i in 0..k {
                            let xi = x[i] as usize;
                            cx[i] = c[xi] - dbar[xi * nv + xi] as u16;
                        }
                        for v in 0..nv {
                            let cv = c[v];
                            if ab + cv as u32 > t_child {
                                continue;
                            }
                            lc += 1;
                            let mut ok = true;
                            for i in 0..k {
                                if cx[i] + dbar[x[i] as usize * nv + v] as u16 > cv {
                                    ok = false;
                                    break;
                                }
                            }
                            if !ok {
                                continue;
                            }
                            lf += 1;
                            if require_t0 && k >= 3 {
                                let mut all_pt = true;
                                'q: for a in 0..k {
                                    for b in a + 1..k {
                                        for cc in b + 1..k {
                                            let qq = [x[a] as usize, x[b] as usize, x[cc] as usize, v];
                                            let (fa, fo) = ctx.pt.quad_masks(&qq, &ctx.fa, &ctx.fo, nv);
                                            if !ctx.pt.is_pt(&fa, &fo) {
                                                all_pt = false;
                                                break 'q;
                                            }
                                        }
                                    }
                                }
                                if !all_pt {
                                    lt0 += 1;
                                    continue;
                                }
                            }
                            if let Some(lk) = look {
                                let r = lk.m - (k + 1);
                                if r > 0 {
                                    let row = &dbar[v * nv..(v + 1) * nv];
                                    let mut mu = u16::MAX;
                                    for (cw, &d) in c.iter().zip(row.iter()) {
                                        mu = mu.min(*cw + d as u16);
                                    }
                                    if ab + cv as u32 + r as u32 * mu as u32 + lk.astar[r] > lk.t {
                                        ll += 1;
                                        continue;
                                    }
                                }
                            }
                            // insert v into sorted x
                            let mut pos = 0;
                            while pos < k && x[pos] <= v as u16 {
                                pos += 1;
                            }
                            child[..pos].copy_from_slice(&x[..pos]);
                            child[pos] = v as u16;
                            child[pos + 1..k + 1].copy_from_slice(&x[pos..k]);
                            ctx.sym.canon(&child[..k + 1], &mut best[..k + 1]);
                            out.push(pack(&best[..k + 1]));
                        }
                        if out.len() > limit {
                            out.sort_unstable();
                            out.dedup();
                            limit = limit.max(2 * out.len());
                        }
                    }
                }
                out.sort_unstable();
                out.dedup();
                cand.fetch_add(lc, Ordering::Relaxed);
                filt.fetch_add(lf, Ordering::Relaxed);
                lookcut.fetch_add(ll, Ordering::Relaxed);
                t0cut.fetch_add(lt0, Ordering::Relaxed);
                results.lock().unwrap().push(out);
            });
        }
    });
    let parts = results.into_inner().unwrap();
    let total: usize = parts.iter().map(|p| p.len()).sum();
    let mut all = Vec::with_capacity(total);
    for p in parts {
        all.extend_from_slice(&p);
    }
    all.sort_unstable();
    all.dedup();
    let st = LevelStats {
        parents: parents.len(),
        candidates: cand.load(Ordering::Relaxed),
        after_filter: filt.load(Ordering::Relaxed),
        lookahead_cut: lookcut.load(Ordering::Relaxed),
        t0_cut: t0cut.load(Ordering::Relaxed),
        orbits: all.len(),
    };
    (all, st)
}

pub fn antisum(ctx: &Ctx, ms: &[u16]) -> u32 {
    let nv = ctx.co.nv;
    let mut ab = 0u32;
    for i in 0..ms.len() {
        for j in i + 1..ms.len() {
            ab += ctx.dbar[ms[i] as usize * nv + ms[j] as usize] as u32;
        }
    }
    ab
}

/// The 4-subsets of {0..m-1} (index level), and for each the 6 index pairs as
/// a bitmask over the C(m,2) pairs.
pub struct Quads {
    pub m: usize,
    pub quads: Vec<[usize; 4]>,
    pub pairmask: Vec<u64>,
    pub pair_of: Vec<Vec<usize>>,
}

impl Quads {
    pub fn new(m: usize) -> Quads {
        assert!(m * (m - 1) / 2 <= 64);
        let mut pair_of = vec![vec![usize::MAX; m]; m];
        let mut k = 0;
        for i in 0..m {
            for j in i + 1..m {
                pair_of[i][j] = k;
                pair_of[j][i] = k;
                k += 1;
            }
        }
        let mut quads = Vec::new();
        let mut pairmask = Vec::new();
        for a in 0..m {
            for b in a + 1..m {
                for c in b + 1..m {
                    for d in c + 1..m {
                        let q = [a, b, c, d];
                        let mut pm = 0u64;
                        for i in 0..4 {
                            for j in i + 1..4 {
                                pm |= 1u64 << pair_of[q[i]][q[j]];
                            }
                        }
                        quads.push(q);
                        pairmask.push(pm);
                    }
                }
            }
        }
        Quads { m, quads, pairmask, pair_of }
    }
}

/// Hyperedges (as pair-masks) of the non-pseudo-tight 4-subsets of ms.
pub fn non_pt_edges(ctx: &Ctx, quads: &Quads, ms: &[u16]) -> Vec<u64> {
    let nv = ctx.co.nv;
    let mut edges = Vec::new();
    for (qi, q) in quads.quads.iter().enumerate() {
        let qq = [ms[q[0]] as usize, ms[q[1]] as usize, ms[q[2]] as usize, ms[q[3]] as usize];
        let (fa, fo) = ctx.pt.quad_masks(&qq, &ctx.fa, &ctx.fo, nv);
        if !ctx.pt.is_pt(&fa, &fo) {
            edges.push(quads.pairmask[qi]);
        }
    }
    edges
}

/// min(tau, cap): minimum transversal of the hypergraph `edges` (each edge a
/// bitmask over pairs).  Branch and bound: pick an unhit edge with fewest
/// still-allowed pairs, branch on which of its pairs is in the transversal
/// (the i-th branch forbids the pairs of branches 1..i-1); lower bound = a
/// greedy packing of unhit edges that are disjoint on allowed pairs.
pub fn min_transversal(edges: &[u64], cap: u32) -> u32 {
    fn rec(edges: &[u64], chosen: u64, forb: u64, depth: u32, best: &mut u32) {
        let allowed = !forb;
        let mut pick: Option<u64> = None;
        let mut pick_sz = u32::MAX;
        for &e in edges {
            if e & chosen == 0 {
                let sz = (e & allowed).count_ones();
                if sz == 0 {
                    return; // cannot be hit any more
                }
                if sz < pick_sz {
                    pick_sz = sz;
                    pick = Some(e);
                }
            }
        }
        let e = match pick {
            None => {
                if depth < *best {
                    *best = depth;
                }
                return;
            }
            Some(e) => e,
        };
        let mut used = 0u64;
        let mut lb = 0u32;
        for &e2 in edges {
            if e2 & chosen == 0 && e2 & allowed & used == 0 {
                used |= e2 & allowed;
                lb += 1;
            }
        }
        if depth + lb >= *best {
            return;
        }
        let mut cand = e & allowed;
        let mut f = forb;
        while cand != 0 {
            let p = cand & cand.wrapping_neg();
            cand ^= p;
            rec(edges, chosen | p, f, depth + 1, best);
            f |= p;
        }
    }
    let mut best = cap;
    rec(edges, 0, 0, 0, &mut best);
    best
}

/// Brute-force check that no transversal of size < k exists (exhaustive over
/// k-1 subsets of the union of edges).  Only for small cross-checks.
pub fn has_transversal_of_size(edges: &[u64], npairs: usize, k: usize) -> bool {
    fn rec(edges: &[u64], npairs: usize, start: usize, left: usize, chosen: u64) -> bool {
        if edges.iter().all(|&e| e & chosen != 0) {
            return true;
        }
        if left == 0 {
            return false;
        }
        for p in start..npairs {
            if rec(edges, npairs, p + 1, left - 1, chosen | (1u64 << p)) {
                return true;
            }
        }
        false
    }
    rec(edges, npairs, 0, k, 0)
}

#[derive(Clone, Copy, Default)]
pub struct OrbitInfo {
    pub abar: u32,
    pub t: u32,
    pub tau: u32,
    pub stab: u32,
    pub stab_has_rev: bool,
}

pub fn analyze(ctx: &Ctx, sets: &[u128], m: usize, tau_cap: u32, nthreads: usize) -> Vec<OrbitInfo> {
    let quads = Quads::new(m);
    let next = AtomicUsize::new(0);
    let out: Mutex<Vec<(usize, Vec<OrbitInfo>)>> = Mutex::new(Vec::new());
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut ms = [0u16; 16];
                loop {
                    let start = next.fetch_add(64, Ordering::Relaxed);
                    if start >= sets.len() {
                        break;
                    }
                    let end = (start + 64).min(sets.len());
                    let mut chunk = Vec::with_capacity(end - start);
                    for i in start..end {
                        unpack(sets[i], m, &mut ms);
                        let abar = antisum(ctx, &ms[..m]);
                        let edges = non_pt_edges(ctx, &quads, &ms[..m]);
                        let tau = min_transversal(&edges, tau_cap);
                        let (stab, stab_has_rev) = ctx.sym.stabiliser(&ms[..m]);
                        chunk.push(OrbitInfo { abar, t: edges.len() as u32, tau, stab, stab_has_rev });
                    }
                    out.lock().unwrap().push((start, chunk));
                }
            });
        }
    });
    let mut parts = out.into_inner().unwrap();
    parts.sort_by_key(|p| p.0);
    parts.into_iter().flat_map(|p| p.1).collect()
}

/// tau-pruned cascade: searches for orbits M of m-multisets with
/// Abar(M) + 2 tau(M) <= T.
///
/// Soundness.  Let M be such a set and M_1 c ... c M_m = M its chain of
/// max-contribution deletions.  For every k, M_k c M, so tau(M_k) <= tau(M)
/// (a transversal of M's non-pseudo-tight family, restricted to pairs inside
/// M_k, is a transversal of M_k's family), hence
///     Abar(M) <= T - 2 tau(M) <= T - 2 tau(M_k) =: T_eff(M_k).
/// Therefore M_k satisfies every cut of the plain cascade run with top
/// threshold T_eff(M_k): Abar(M_k) <= thresholds(m, T_eff)[k] (thresholds are
/// monotone in the top value) and the lookahead
/// Abar(M_k) + r mu(M_k) + astar[r] <= T_eff.  All quantities are G-invariant,
/// so filtering every level by these tau-dependent cuts keeps a representative
/// of every chain set M_k, and the top level is exactly the set of orbits with
/// Abar + 2 tau <= T.
pub struct TauFilterStats {
    pub before: usize,
    pub after: usize,
    pub tau_hist: [usize; 8],
}

/// `abmax` additionally caps Abar(M) (sound for the same reason: every cut is
/// applied with top value min(T - 2 tau, abmax) >= Abar(M)).
pub fn tau_filter(ctx: &Ctx, level: &[u128], k: usize, m: usize, t: u32, abmax: u32, astar: &[u32], nthreads: usize) -> (Vec<u128>, Vec<(u32, u32, u32)>, TauFilterStats) {
    let nv = ctx.co.nv;
    let quads = if k >= 4 { Some(Quads::new(k)) } else { None };
    // tau large enough that T - 2 tau < A*(m): nothing can survive
    let mut tau_kill = 0u32;
    while t >= 2 * tau_kill && t - 2 * tau_kill >= astar[m] {
        tau_kill += 1;
    }
    let ths: Vec<Vec<u32>> = (0..tau_kill).map(|tau| thresholds(m, (t - 2 * tau).min(abmax))).collect();
    let next = AtomicUsize::new(0);
    let out: Mutex<Vec<(usize, Vec<(u128, u32, u32, u32)>, [usize; 8])>> = Mutex::new(Vec::new());
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut ms = [0u16; 16];
                let mut c = vec![0u16; nv];
                loop {
                    let start = next.fetch_add(64, Ordering::Relaxed);
                    if start >= level.len() {
                        break;
                    }
                    let end = (start + 64).min(level.len());
                    let mut chunk = Vec::new();
                    let mut hist = [0usize; 8];
                    for i in start..end {
                        unpack(level[i], k, &mut ms);
                        let s = &ms[..k];
                        let ab = antisum(ctx, s);
                        let (tcount, tau) = match &quads {
                            None => (0u32, 0u32),
                            Some(q) => {
                                let e = non_pt_edges(ctx, q, s);
                                (e.len() as u32, min_transversal(&e, tau_kill))
                            }
                        };
                        hist[(tau as usize).min(7)] += 1;
                        if tau >= tau_kill {
                            continue;
                        }
                        let teff = (t - 2 * tau).min(abmax);
                        if ab > ths[tau as usize][k] {
                            continue;
                        }
                        let r = m - k;
                        if r > 0 {
                            for e in c.iter_mut() {
                                *e = 0;
                            }
                            for &x in s {
                                let row = &ctx.dbar[x as usize * nv..(x as usize + 1) * nv];
                                for (cv, &d) in c.iter_mut().zip(row.iter()) {
                                    *cv += d as u16;
                                }
                            }
                            let mu = *c.iter().min().unwrap() as u32;
                            if ab + r as u32 * mu + astar[r] > teff {
                                continue;
                            }
                        }
                        chunk.push((level[i], ab, tcount, tau));
                    }
                    out.lock().unwrap().push((start, chunk, hist));
                }
            });
        }
    });
    let mut parts = out.into_inner().unwrap();
    parts.sort_by_key(|p| p.0);
    let mut st = TauFilterStats { before: level.len(), after: 0, tau_hist: [0; 8] };
    let mut keep = Vec::new();
    let mut info = Vec::new();
    for (_, chunk, hist) in parts {
        for j in 0..8 {
            st.tau_hist[j] += hist[j];
        }
        for (x, ab, tc, tau) in chunk {
            keep.push(x);
            info.push((ab, tc, tau));
        }
    }
    st.after = keep.len();
    (keep, info, st)
}


/// Search for counterexamples through pseudo-tight cores.
///
/// Claim: if Abar(M) + 2 tau(M) <= T and tau(M) = j, then M contains a
/// sub-multiset Z with |Z| = m - j, t(Z) = 0 and
///     Abar(Z) + j mu(Z) + astar[j] <= Abar(M) <= T - 2j.
/// Proof: take a minimum transversal (j pairs), delete one endpoint of each
/// pair (fewer than j deletions if pairs share endpoints; then delete further
/// arbitrary elements up to j).  Every non-pseudo-tight 4-subset contains a
/// transversal pair, hence a deleted element, so t(Z) = 0.  The inequality is
/// the lookahead identity for Z c M with r = j.
///
/// The cores Z are enumerated by the cascade on Z (max-contribution deletion
/// chain inside Z).  A chain set S c Z c M satisfies, with tm = T - 2j:
///   t(S) = 0                                   (t = 0 is inherited by subsets)
///   Abar(S) <= thresholds(m-j, tm - j mu(S) - astar[j])[|S|]
///         (Abar(Z) <= tm - j mu(Z) - astar[j] <= tm - j mu(S) - astar[j]
///          since mu(Z) >= mu(S), and thresholds are monotone)
///   Abar(S) + (m - |S|) mu(S) + astar[m - |S|] <= tm   (lookahead for S c M)
/// all G-invariant.  So every core orbit is reached; each core is then
/// extended by j vertices in every possible way (bounded by the lookahead)
/// and tau(M) is computed exactly (up to the needed cap).
pub struct CoreLevelFilter {
    pub before: usize,
    pub after: usize,
}

pub fn core_filter(ctx: &Ctx, level: &[u128], k: usize, m: usize, j: usize, tm: u32, astar: &[u32], nthreads: usize) -> (Vec<u128>, CoreLevelFilter) {
    let nv = ctx.co.nv;
    let mz = m - j;
    let ths: Vec<Vec<u32>> = (0..=tm).map(|tt| thresholds(mz, tt)).collect();
    let next = AtomicUsize::new(0);
    let out: Mutex<Vec<(usize, Vec<u128>)>> = Mutex::new(Vec::new());
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut ms = [0u16; 16];
                let mut c = vec![0u16; nv];
                loop {
                    let start = next.fetch_add(1024, Ordering::Relaxed);
                    if start >= level.len() {
                        break;
                    }
                    let end = (start + 1024).min(level.len());
                    let mut chunk = Vec::new();
                    for i in start..end {
                        unpack(level[i], k, &mut ms);
                        let sset = &ms[..k];
                        let ab = antisum(ctx, sset);
                        for e in c.iter_mut() {
                            *e = 0;
                        }
                        for &x in sset {
                            let row = &ctx.dbar[x as usize * nv..(x as usize + 1) * nv];
                            for (cv, &d) in c.iter_mut().zip(row.iter()) {
                                *cv += d as u16;
                            }
                        }
                        let mu = *c.iter().min().unwrap() as u32;
                        let need = j as u32 * mu + astar[j];
                        if need > tm {
                            continue;
                        }
                        if ab > ths[(tm - need) as usize][k] {
                            continue;
                        }
                        let r = m - k;
                        if ab + r as u32 * mu + astar[r] > tm {
                            continue;
                        }
                        chunk.push(level[i]);
                    }
                    out.lock().unwrap().push((start, chunk));
                }
            });
        }
    });
    let mut parts = out.into_inner().unwrap();
    parts.sort_by_key(|p| p.0);
    let keep: Vec<u128> = parts.into_iter().flat_map(|p| p.1).collect();
    let st = CoreLevelFilter { before: level.len(), after: keep.len() };
    (keep, st)
}

/// Extend each core (size m-j) by j vertices (nondecreasing indices), bounded
/// by Abar(P) + r mu(P) + astar[r] <= tm; for each full M with Abar(M) <= tm
/// compute tau and keep it if Abar + 2 tau <= T.  Returns canonical forms of
/// all such M (deduplicated) with (Abar, t, tau), and the number of M tested.
pub fn extend_cores(ctx: &Ctx, cores: &[u128], m: usize, j: usize, tm: u32, t: u32, astar: &[u32], nthreads: usize) -> (Vec<(u128, u32, u32, u32)>, u64) {
    let nv = ctx.co.nv;
    let mz = m - j;
    let quads = Quads::new(m);
    let next = AtomicUsize::new(0);
    let tested = AtomicU64::new(0);
    let out: Mutex<Vec<(u128, u32, u32, u32)>> = Mutex::new(Vec::new());
    fn rec(ctx: &Ctx, quads: &Quads, cur: &mut Vec<u16>, ab: u32, minv: usize, left: usize, tm: u32, t: u32, astar: &[u32], found: &mut Vec<(u128, u32, u32, u32)>, tested: &mut u64) {
        let nv = ctx.co.nv;
        if left == 0 {
            *tested += 1;
            let mut ms = cur.clone();
            ms.sort();
            let edges = non_pt_edges(ctx, quads, &ms);
            let cap = (t - ab) / 2 + 1;
            let tau = min_transversal(&edges, cap);
            if ab + 2 * tau <= t {
                let mut best = vec![0u16; ms.len()];
                ctx.sym.canon(&ms, &mut best);
                found.push((pack(&best), ab, edges.len() as u32, tau));
            }
            return;
        }
        let mut c = vec![0u16; nv];
        for &x in cur.iter() {
            let row = &ctx.dbar[x as usize * nv..(x as usize + 1) * nv];
            for (cv, &d) in c.iter_mut().zip(row.iter()) {
                *cv += d as u16;
            }
        }
        for v in minv..nv {
            let ab2 = ab + c[v] as u32;
            if ab2 > tm {
                continue;
            }
            let r = left - 1;
            if r > 0 {
                // mu of cur + v
                let row = &ctx.dbar[v * nv..(v + 1) * nv];
                let mut mu = u32::MAX;
                for (cw, &d) in c.iter().zip(row.iter()) {
                    mu = mu.min(*cw as u32 + d as u32);
                }
                if ab2 + r as u32 * mu + astar[r] > tm {
                    continue;
                }
            }
            cur.push(v as u16);
            rec(ctx, quads, cur, ab2, v, left - 1, tm, t, astar, found, tested);
            cur.pop();
        }
    }
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut ms = [0u16; 16];
                let mut found = Vec::new();
                let mut lt = 0u64;
                loop {
                    let start = next.fetch_add(16, Ordering::Relaxed);
                    if start >= cores.len() {
                        break;
                    }
                    let end = (start + 16).min(cores.len());
                    for i in start..end {
                        unpack(cores[i], mz, &mut ms);
                        let mut cur: Vec<u16> = ms[..mz].to_vec();
                        let ab = antisum(ctx, &cur);
                        rec(ctx, &quads, &mut cur, ab, 0, j, tm, t, astar, &mut found, &mut lt);
                    }
                    if found.len() > 1 << 22 {
                        found.sort_unstable();
                        found.dedup();
                    }
                }
                tested.fetch_add(lt, Ordering::Relaxed);
                out.lock().unwrap().extend(found);
            });
        }
    });
    let mut all = out.into_inner().unwrap();
    all.sort_unstable();
    all.dedup();
    (all, tested.load(Ordering::Relaxed))
}

/// Bit table of pseudo-tightness for all 4-multisets: bit (b*nv + c)*nv + d
/// holds PT(0, b, c, d).  PT is invariant under G and under reordering the
/// four elements (both checked in selfcheck), so
///     PT(a, b, c, d) = PT(0, g b, g c, g d)   for any g with g(a) = 0.
pub struct PtTable {
    pub nv: usize,
    pub bits: Vec<u64>,
    pub gz: Vec<u32>,
}

impl PtTable {
    pub fn build(ctx: &Ctx, nthreads: usize) -> PtTable {
        let nv = ctx.co.nv;
        let nbits = nv * nv * nv;
        let words: Vec<AtomicU64> = (0..(nbits + 63) / 64).map(|_| AtomicU64::new(0)).collect();
        let next = AtomicUsize::new(0);
        std::thread::scope(|s| {
            for _ in 0..nthreads {
                s.spawn(|| loop {
                    let b = next.fetch_add(1, Ordering::Relaxed);
                    if b >= nv {
                        break;
                    }
                    for c in b..nv {
                        for d in c..nv {
                            let q = [0usize, b, c, d];
                            let (fa, fo) = ctx.pt.quad_masks(&q, &ctx.fa, &ctx.fo, nv);
                            if ctx.pt.is_pt(&fa, &fo) {
                                for &(x, y, z) in &[(b, c, d), (b, d, c), (c, b, d), (c, d, b), (d, b, c), (d, c, b)] {
                                    let i = (x * nv + y) * nv + z;
                                    words[i / 64].fetch_or(1u64 << (i % 64), Ordering::Relaxed);
                                }
                            }
                        }
                    }
                });
            }
        });
        let bits = words.into_iter().map(|w| w.into_inner()).collect();
        let gz = (0..nv).map(|a| ctx.sym.to_zero[a][0]).collect();
        PtTable { nv, bits, gz }
    }

    #[inline]
    pub fn pt(&self, act: &[u16], a: usize, b: usize, c: usize, d: usize) -> bool {
        let nv = self.nv;
        let row = &act[self.gz[a] as usize * nv..];
        let (b, c, d) = (row[b] as usize, row[c] as usize, row[d] as usize);
        let i = (b * nv + c) * nv + d;
        (self.bits[i / 64] >> (i % 64)) & 1 == 1
    }
}

pub struct TauLevelStats {
    pub parents: usize,
    pub candidates: u64,
    pub after_maxcontrib: u64,
    pub lookahead_cut: u64,
    pub tau_cut: u64,
    pub tau_hist: [u64; 4],
    pub orbits: usize,
}

/// One level of the tau-pruned cascade with every cut applied to each
/// candidate child BEFORE canonicalisation (all cuts are G-invariant, so this
/// keeps exactly the orbits the post-hoc filter `tau_filter` keeps):
/// averaging threshold and lookahead with T_eff = T - 2 tau(child), and
/// tau(child) < tau_stop.  tau(child) is computed from the parent's
/// non-pseudo-tight 4-subsets plus those containing the new element.
pub fn extend_level_tau(ctx: &Ctx, tab: &PtTable, parents: &[u128], k: usize, m: usize, t: u32, tau_stop: u32, astar: &[u32], nthreads: usize) -> (Vec<u128>, TauLevelStats) {
    extend_level_tau_cap(ctx, tab, parents, k, m, t, u32::MAX, tau_stop, astar, nthreads)
}

/// As extend_level_tau, additionally capping Abar(M) <= abmax: every cut uses
/// the top value min(T - 2 tau, abmax), which is >= Abar(M) for any target M.
pub fn extend_level_tau_cap(ctx: &Ctx, tab: &PtTable, parents: &[u128], k: usize, m: usize, t: u32, abmax: u32, tau_stop: u32, astar: &[u32], nthreads: usize) -> (Vec<u128>, TauLevelStats) {
    let nv = ctx.co.nv;
    let dbar = &ctx.dbar;
    let act = &ctx.sym.act;
    let kc = k + 1;
    let quads_c = Quads::new(kc.max(4));
    let ths: Vec<Vec<u32>> = (0..tau_stop).map(|tau| thresholds(m, (t - 2 * tau).min(abmax))).collect();
    let tl = t.min(abmax);
    let next = AtomicUsize::new(0);
    let counters: Vec<AtomicU64> = (0..8).map(|_| AtomicU64::new(0)).collect();
    let results: Mutex<Vec<Vec<u128>>> = Mutex::new(Vec::new());
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut out: Vec<u128> = Vec::new();
                let mut limit = 1usize << 24;
                let mut c = vec![0u16; nv];
                let mut x = [0u16; 16];
                let mut child = [0u16; 16];
                let mut best = [0u16; 16];
                let mut cx = [0u16; 16];
                let mut pedges: Vec<u64> = Vec::new();
                let mut edges: Vec<u64> = Vec::new();
                let mut loc = [0u64; 8];
                loop {
                    let start = next.fetch_add(64, Ordering::Relaxed);
                    if start >= parents.len() {
                        break;
                    }
                    let end = (start + 64).min(parents.len());
                    for pi in start..end {
                        unpack(parents[pi], k, &mut x);
                        let mut ab = 0u32;
                        for i in 0..k {
                            for j in i + 1..k {
                                ab += dbar[x[i] as usize * nv + x[j] as usize] as u32;
                            }
                        }
                        if ab > ths[0][kc] {
                            continue;
                        }
                        for e in c.iter_mut() {
                            *e = 0;
                        }
                        for i in 0..k {
                            let row = &dbar[x[i] as usize * nv..(x[i] as usize + 1) * nv];
                            for (cv, &d) in c.iter_mut().zip(row.iter()) {
                                *cv += d as u16;
                            }
                        }
                        for i in 0..k {
                            let xi = x[i] as usize;
                            cx[i] = c[xi] - dbar[xi * nv + xi] as u16;
                        }
                        // parent's non-PT 4-subsets, as pair masks in child indexing
                        pedges.clear();
                        if k >= 4 {
                            for a in 0..k {
                                for b in a + 1..k {
                                    for cc in b + 1..k {
                                        for d in cc + 1..k {
                                            if !tab.pt(act, x[a] as usize, x[b] as usize, x[cc] as usize, x[d] as usize) {
                                                let q = [a, b, cc, d];
                                                let mut pm = 0u64;
                                                for i in 0..4 {
                                                    for j in i + 1..4 {
                                                        pm |= 1u64 << quads_c.pair_of[q[i]][q[j]];
                                                    }
                                                }
                                                pedges.push(pm);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        for v in 0..nv {
                            let cv = c[v];
                            let abc = ab + cv as u32;
                            if abc > ths[0][kc] {
                                continue;
                            }
                            loc[0] += 1;
                            let mut ok = true;
                            for i in 0..k {
                                if cx[i] + dbar[x[i] as usize * nv + v] as u16 > cv {
                                    ok = false;
                                    break;
                                }
                            }
                            if !ok {
                                continue;
                            }
                            loc[1] += 1;
                            let r = m - kc;
                            let mut mu = 0u32;
                            if r > 0 {
                                let row = &dbar[v * nv..(v + 1) * nv];
                                let mut mm = u16::MAX;
                                for (cw, &d) in c.iter().zip(row.iter()) {
                                    mm = mm.min(*cw + d as u16);
                                }
                                mu = mm as u32;
                                if abc + r as u32 * mu + astar[r] > tl {
                                    loc[2] += 1;
                                    continue;
                                }
                            }
                            // tau of the child
                            let mut tau = 0u32;
                            if kc >= 4 {
                                edges.clear();
                                edges.extend_from_slice(&pedges);
                                for a in 0..k {
                                    for b in a + 1..k {
                                        for cc in b + 1..k {
                                            if !tab.pt(act, x[a] as usize, x[b] as usize, x[cc] as usize, v) {
                                                let q = [a, b, cc, k];
                                                let mut pm = 0u64;
                                                for i in 0..4 {
                                                    for j in i + 1..4 {
                                                        pm |= 1u64 << quads_c.pair_of[q[i]][q[j]];
                                                    }
                                                }
                                                edges.push(pm);
                                            }
                                        }
                                    }
                                }
                                tau = min_transversal(&edges, tau_stop);
                            }
                            if tau >= tau_stop {
                                loc[3] += 1;
                                continue;
                            }
                            let teff = (t - 2 * tau).min(abmax);
                            if abc > ths[tau as usize][kc] || (r > 0 && abc + r as u32 * mu + astar[r] > teff) {
                                loc[3] += 1;
                                continue;
                            }
                            loc[4 + tau as usize] += 1;
                            let mut pos = 0;
                            while pos < k && x[pos] <= v as u16 {
                                pos += 1;
                            }
                            child[..pos].copy_from_slice(&x[..pos]);
                            child[pos] = v as u16;
                            child[pos + 1..kc].copy_from_slice(&x[pos..k]);
                            ctx.sym.canon(&child[..kc], &mut best[..kc]);
                            out.push(pack(&best[..kc]));
                        }
                        if out.len() > limit {
                            out.sort_unstable();
                            out.dedup();
                            limit = limit.max(2 * out.len());
                        }
                    }
                }
                out.sort_unstable();
                out.dedup();
                for i in 0..8 {
                    counters[i].fetch_add(loc[i], Ordering::Relaxed);
                }
                results.lock().unwrap().push(out);
            });
        }
    });
    let parts = results.into_inner().unwrap();
    let total: usize = parts.iter().map(|p| p.len()).sum();
    let mut all = Vec::with_capacity(total);
    for p in parts {
        all.extend_from_slice(&p);
    }
    all.sort_unstable();
    all.dedup();
    let g = |i: usize| counters[i].load(Ordering::Relaxed);
    let st = TauLevelStats {
        parents: parents.len(),
        candidates: g(0),
        after_maxcontrib: g(1),
        lookahead_cut: g(2),
        tau_cut: g(3),
        tau_hist: [g(4), g(5), g(6), g(7)],
        orbits: all.len(),
    };
    (all, st)
}

/// Filtered children of one (sorted) multiset x of size k, with exactly the
/// cuts of extend_level_tau_cap (averaging threshold, max-contribution,
/// lookahead, tau and tau-dependent threshold/lookahead).  Children are
/// returned as sorted multisets, not canonicalised.
pub struct ChildGen<'a> {
    pub ctx: &'a Ctx,
    pub tab: &'a PtTable,
    pub m: usize,
    pub t: u32,
    pub abmax: u32,
    pub tau_stop: u32,
    pub astar: &'a [u32],
    pub ths: Vec<Vec<u32>>,
    pub pair_of: Vec<Vec<usize>>,
}

impl<'a> ChildGen<'a> {
    pub fn new(ctx: &'a Ctx, tab: &'a PtTable, m: usize, t: u32, abmax: u32, tau_stop: u32, astar: &'a [u32]) -> Self {
        let ths = (0..tau_stop).map(|tau| thresholds(m, (t - 2 * tau).min(abmax))).collect();
        // pair masks are u64: valid for multisets of at most 11 elements
        // (C(11,2) = 55 <= 64).  children() asserts this.
        let pair_of = Quads::new(m.min(11).max(4)).pair_of;
        ChildGen { ctx, tab, m, t, abmax, tau_stop, astar, ths, pair_of }
    }

    pub fn children(&self, x: &[u16], out: &mut Vec<Vec<u16>>) {
        let ctx = self.ctx;
        let nv = ctx.co.nv;
        let dbar = &ctx.dbar;
        let act = &ctx.sym.act;
        let k = x.len();
        let kc = k + 1;
        assert!(kc <= 11, "pair masks are u64; children of size > 11 need u128 masks");
        let m = self.m;
        let tl = self.t.min(self.abmax);
        let mut ab = 0u32;
        for i in 0..k {
            for j in i + 1..k {
                ab += dbar[x[i] as usize * nv + x[j] as usize] as u32;
            }
        }
        if ab > self.ths[0][kc] {
            return;
        }
        let mut c = vec![0u16; nv];
        for i in 0..k {
            let row = &dbar[x[i] as usize * nv..(x[i] as usize + 1) * nv];
            for (cv, &d) in c.iter_mut().zip(row.iter()) {
                *cv += d as u16;
            }
        }
        let cx: Vec<u16> = (0..k).map(|i| c[x[i] as usize] - dbar[x[i] as usize * nv + x[i] as usize] as u16).collect();
        let mask_of = |q: [usize; 4]| -> u64 {
            let mut pm = 0u64;
            for i in 0..4 {
                for j in i + 1..4 {
                    pm |= 1u64 << self.pair_of[q[i]][q[j]];
                }
            }
            pm
        };
        let mut pedges = Vec::new();
        if k >= 4 {
            for a in 0..k {
                for b in a + 1..k {
                    for cc in b + 1..k {
                        for d in cc + 1..k {
                            if !self.tab.pt(act, x[a] as usize, x[b] as usize, x[cc] as usize, x[d] as usize) {
                                pedges.push(mask_of([a, b, cc, d]));
                            }
                        }
                    }
                }
            }
        }
        let mut edges = Vec::new();
        for v in 0..nv {
            let cv = c[v];
            let abc = ab + cv as u32;
            if abc > self.ths[0][kc] {
                continue;
            }
            if (0..k).any(|i| cx[i] + dbar[x[i] as usize * nv + v] as u16 > cv) {
                continue;
            }
            let r = m - kc;
            let mut mu = 0u32;
            if r > 0 {
                let row = &dbar[v * nv..(v + 1) * nv];
                mu = c.iter().zip(row.iter()).map(|(cw, &d)| *cw as u32 + d as u32).min().unwrap();
                if abc + r as u32 * mu + self.astar[r] > tl {
                    continue;
                }
            }
            let mut tau = 0u32;
            if kc >= 4 {
                edges.clear();
                edges.extend_from_slice(&pedges);
                for a in 0..k {
                    for b in a + 1..k {
                        for cc in b + 1..k {
                            if !self.tab.pt(act, x[a] as usize, x[b] as usize, x[cc] as usize, v) {
                                edges.push(mask_of([a, b, cc, k]));
                            }
                        }
                    }
                }
                tau = min_transversal(&edges, self.tau_stop);
            }
            if tau >= self.tau_stop {
                continue;
            }
            let teff = (self.t - 2 * tau).min(self.abmax);
            if abc > self.ths[tau as usize][kc] || (r > 0 && abc + r as u32 * mu + self.astar[r] > teff) {
                continue;
            }
            let mut ch = x.to_vec();
            let pos = ch.partition_point(|&e| e <= v as u16);
            ch.insert(pos, v as u16);
            out.push(ch);
        }
    }
}

/// Depth-first completion from a stored level: every parent is expanded to
/// size m without intermediate de-duplication; only the final sets are
/// canonicalised and de-duplicated.  Returns (sorted unique canonical forms,
/// number of nodes visited per depth).
pub fn stream_to_top(gen: &ChildGen, parents: &[u128], k: usize, nthreads: usize) -> (Vec<u128>, Vec<u64>) {
    let m = gen.m;
    let next = AtomicUsize::new(0);
    let nodes: Vec<AtomicU64> = (0..=m).map(|_| AtomicU64::new(0)).collect();
    let results: Mutex<Vec<Vec<u128>>> = Mutex::new(Vec::new());
    fn rec(gen: &ChildGen, x: &[u16], out: &mut Vec<u128>, cnt: &mut Vec<u64>) {
        let mut ch = Vec::new();
        gen.children(x, &mut ch);
        for c in ch {
            cnt[c.len()] += 1;
            if c.len() == gen.m {
                let mut best = vec![0u16; c.len()];
                gen.ctx.sym.canon(&c, &mut best);
                out.push(pack(&best));
            } else {
                rec(gen, &c, out, cnt);
            }
        }
    }
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut out = Vec::new();
                let mut cnt = vec![0u64; m + 1];
                let mut x = [0u16; 16];
                let mut limit = 1usize << 22;
                loop {
                    let start = next.fetch_add(16, Ordering::Relaxed);
                    if start >= parents.len() {
                        break;
                    }
                    for pi in start..(start + 16).min(parents.len()) {
                        unpack(parents[pi], k, &mut x);
                        rec(gen, &x[..k], &mut out, &mut cnt);
                    }
                    if out.len() > limit {
                        out.sort_unstable();
                        out.dedup();
                        limit = limit.max(2 * out.len());
                    }
                }
                out.sort_unstable();
                out.dedup();
                for i in 0..=m {
                    nodes[i].fetch_add(cnt[i], Ordering::Relaxed);
                }
                results.lock().unwrap().push(out);
            });
        }
    });
    let mut all: Vec<u128> = results.into_inner().unwrap().into_iter().flatten().collect();
    all.sort_unstable();
    all.dedup();
    (all, nodes.iter().map(|a| a.load(Ordering::Relaxed)).collect())
}

/// Canonical parent of a canonical multiset c (sorted, canonical form): c
/// minus one copy of its max-contribution element of largest vertex index,
/// canonicalised.  A function of the orbit only (c is the orbit's canonical
/// form and the choice depends only on c).
pub fn canonical_parent(ctx: &Ctx, c: &[u16]) -> Vec<u16> {
    let nv = ctx.co.nv;
    let k = c.len();
    let mut best_i = 0usize;
    let mut best_c = 0u32;
    for i in 0..k {
        let mut s = 0u32;
        for j in 0..k {
            if j != i {
                s += ctx.dbar[c[i] as usize * nv + c[j] as usize] as u32;
            }
        }
        if s > best_c || (s == best_c && c[i] >= c[best_i]) {
            best_c = s;
            best_i = i;
        }
    }
    let p: Vec<u16> = c.iter().enumerate().filter(|&(i, _)| i != best_i).map(|(_, &v)| v).collect();
    let mut out = vec![0u16; k - 1];
    ctx.sym.canon(&p, &mut out);
    out
}

/// Depth-first completion by canonical augmentation: from each stored
/// (canonical) orbit at level k, a child orbit C is accepted iff its
/// canonical parent equals the node it was generated from; accepted children
/// of one node are de-duplicated locally.  Every orbit passing the cuts is
/// then visited exactly once: its canonical parent passes the same cuts (it
/// is a max-contribution deletion, and every cut is inherited by subsets of a
/// target), so by induction the parent is visited once and generates it.
/// No global de-duplication is needed.  Returns per-level orbit counts and,
/// at the top level, a histogram by antisum plus (optionally) a sample.
pub fn augment_to_top(gen: &ChildGen, parents: &[u128], k: usize, nthreads: usize, sample_every: u64) -> (Vec<u64>, std::collections::BTreeMap<u32, u64>, Vec<u128>) {
    augment_to(gen, parents, k, gen.m, nthreads, sample_every)
}

/// As augment_to_top, but stops (only counting) at size `stop_len` <= m.
pub fn augment_to(gen: &ChildGen, parents: &[u128], k: usize, stop_len: usize, nthreads: usize, sample_every: u64) -> (Vec<u64>, std::collections::BTreeMap<u32, u64>, Vec<u128>) {
    let m = gen.m;
    let next = AtomicUsize::new(0);
    let counts: Vec<AtomicU64> = (0..=m).map(|_| AtomicU64::new(0)).collect();
    let res: Mutex<(std::collections::BTreeMap<u32, u64>, Vec<u128>)> = Mutex::new((Default::default(), Vec::new()));
    fn rec(gen: &ChildGen, node: &[u16], cnt: &mut Vec<u64>, hist: &mut std::collections::BTreeMap<u32, u64>, sample: &mut Vec<u128>, every: u64, stop_len: usize) {
        let mut ch = Vec::new();
        gen.children(node, &mut ch);
        let mut acc: Vec<Vec<u16>> = Vec::new();
        for c in ch {
            let mut cf = vec![0u16; c.len()];
            gen.ctx.sym.canon(&c, &mut cf);
            if canonical_parent(gen.ctx, &cf) == node {
                acc.push(cf);
            }
        }
        acc.sort_unstable();
        acc.dedup();
        for cf in acc {
            let l = cf.len();
            cnt[l] += 1;
            if l == stop_len {
                *hist.entry(antisum(gen.ctx, &cf)).or_default() += 1;
                if every > 0 && cnt[l] % every == 1 {
                    sample.push(pack(&cf));
                }
            } else {
                rec(gen, &cf, cnt, hist, sample, every, stop_len);
            }
        }
    }
    std::thread::scope(|s| {
        for _ in 0..nthreads {
            s.spawn(|| {
                let mut cnt = vec![0u64; m + 1];
                let mut hist = std::collections::BTreeMap::new();
                let mut sample = Vec::new();
                let mut x = [0u16; 16];
                loop {
                    let start = next.fetch_add(16, Ordering::Relaxed);
                    if start >= parents.len() {
                        break;
                    }
                    for pi in start..(start + 16).min(parents.len()) {
                        unpack(parents[pi], k, &mut x);
                        rec(gen, &x[..k], &mut cnt, &mut hist, &mut sample, sample_every, stop_len);
                    }
                }
                for i in 0..=m {
                    counts[i].fetch_add(cnt[i], Ordering::Relaxed);
                }
                let mut r = res.lock().unwrap();
                for (a, n) in hist {
                    *r.0.entry(a).or_default() += n;
                }
                r.1.extend(sample);
            });
        }
    });
    let (hist, sample) = res.into_inner().unwrap();
    (counts.iter().map(|a| a.load(Ordering::Relaxed)).collect(), hist, sample)
}
