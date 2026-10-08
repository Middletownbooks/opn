//! Pseudo-tightness test for a (4,n)-set, straight from Woodall's definition.
//!
//! Input: for each of the 6 pairs p of the 4-set (in CO_4 label order), the
//! AND (FA) and OR (FO) of the label sets of all shortest antipaths in CO_n.
//! For a ground pair g = {x,y}:
//!   FORCED(g) = { p : g in FA[p] }   (g occurs in EVERY shortest p-antipath)
//!   POSS(g)   = { p : g in FO[p] }   (g occurs in SOME shortest p-antipath)
//! The 4-set is pseudo-tight iff there is N : {0..n-1} -> V(CO_4) such that
//! for every g = {x,y} some N[x] -> rev(N[y]) route in CO_4 (of the chosen
//! family) has label set L with FORCED(g) <= L <= POSS(g).

use crate::co::{route_label_sets, Co, Family};

pub struct PtTester {
    pub n_src: usize,
    pub npairs_src: usize,
    /// cons_pair[x][y] = index of ground pair {x,y} in the source CO_n.
    pub cons_pair: Vec<Vec<usize>>,
    /// comp[(F<<6)|P][u] = bitmask of v in V(CO_4) such that some route
    /// u -> rev(v) has a label set L with F <= L <= P.
    pub comp: Vec<[u8; 6]>,
    /// quad_pairs[p] = (i,j): CO_4 label p is the pair of the i-th and j-th
    /// elements of the 4-set.
    pub quad_pairs: [(usize, usize); 6],
    pub w: Vec<u64>,
    pub rev4: Vec<usize>,
}

impl PtTester {
    pub fn new(co4: &Co, fam: Family, src: &Co) -> PtTester {
        assert_eq!(co4.n, 4);
        assert_eq!(co4.nv, 6);
        assert!(src.n <= 7);
        let w = route_label_sets(co4, fam);
        let rev4: Vec<usize> = co4.rev.iter().map(|&r| r as usize).collect();
        let mut comp = vec![[0u8; 6]; 64 * 64];
        for f in 0..64usize {
            for p in 0..64usize {
                let mut allowed = 0u64;
                for l in 0..64usize {
                    if l & f == f && l & !p == 0 {
                        allowed |= 1u64 << l;
                    }
                }
                let mut c = [0u8; 6];
                for u in 0..6 {
                    for v in 0..6 {
                        if w[u * 6 + rev4[v]] & allowed != 0 {
                            c[u] |= 1 << v;
                        }
                    }
                }
                comp[(f << 6) | p] = c;
            }
        }
        let mut quad_pairs = [(0usize, 0usize); 6];
        for (p, &(i, j)) in co4.pairs.iter().enumerate() {
            quad_pairs[p] = (i as usize, j as usize);
        }
        let n = src.n;
        let mut cons_pair = vec![vec![usize::MAX; n]; n];
        for x in 0..n {
            for y in 0..n {
                if x != y {
                    cons_pair[x][y] = src.pair_idx[x][y] as usize;
                }
            }
        }
        PtTester { n_src: n, npairs_src: src.npairs, cons_pair, comp, quad_pairs, w, rev4 }
    }

    /// Gather FA/FO for a 4-multiset of source vertices.
    #[inline]
    pub fn quad_masks(&self, q: &[usize; 4], fa_t: &[u32], fo_t: &[u32], nv: usize) -> ([u32; 6], [u32; 6]) {
        let mut fa = [0u32; 6];
        let mut fo = [0u32; 6];
        for p in 0..6 {
            let (i, j) = self.quad_pairs[p];
            fa[p] = fa_t[q[i] * nv + q[j]];
            fo[p] = fo_t[q[i] * nv + q[j]];
        }
        (fa, fo)
    }

    #[inline]
    fn forced_poss(&self, fa: &[u32; 6], fo: &[u32; 6]) -> ([u8; 21], [u8; 21]) {
        let mut fp = [0u8; 21];
        let mut pp = [0u8; 21];
        for p in 0..6 {
            for g in 0..self.npairs_src {
                fp[g] |= (((fa[p] >> g) & 1) as u8) << p;
                pp[g] |= (((fo[p] >> g) & 1) as u8) << p;
            }
        }
        (fp, pp)
    }

    pub fn is_pt(&self, fa: &[u32; 6], fo: &[u32; 6]) -> bool {
        let (fp, pp) = self.forced_poss(fa, fo);
        let mut cons = [[0u8; 6]; 21];
        for g in 0..self.npairs_src {
            cons[g] = self.comp[((fp[g] as usize) << 6) | pp[g] as usize];
        }
        let dom = [0x3fu8; 7];
        self.solve(0, &dom, &cons)
    }

    fn solve(&self, x: usize, dom: &[u8; 7], cons: &[[u8; 6]; 21]) -> bool {
        let n = self.n_src;
        if x == n {
            return true;
        }
        let mut d = dom[x];
        while d != 0 {
            let u = d.trailing_zeros() as usize;
            d &= d - 1;
            let mut nd = *dom;
            let mut ok = true;
            for y in x + 1..n {
                nd[y] &= cons[self.cons_pair[x][y]][u];
                if nd[y] == 0 {
                    ok = false;
                    break;
                }
            }
            if ok && self.solve(x + 1, &nd, cons) {
                return true;
            }
        }
        false
    }

    /// Tightness (Woodall): choose ONE shortest-antipath label set L_p for
    /// each of the 6 pairs; then for every ground pair g the route Q_g must
    /// have label set exactly {p : g in L_p}.  Tight iff some choice admits N.
    /// (Pseudo-tightness is the relaxation FORCED <= L <= POSS.)
    pub fn is_tight(&self, sets: &[Vec<u32>; 6]) -> bool {
        let mut idx = [0usize; 6];
        loop {
            let mut ex = [0u8; 21];
            for p in 0..6 {
                let l = sets[p][idx[p]];
                for g in 0..self.npairs_src {
                    ex[g] |= (((l >> g) & 1) as u8) << p;
                }
            }
            let mut cons = [[0u8; 6]; 21];
            for g in 0..self.npairs_src {
                cons[g] = self.comp[((ex[g] as usize) << 6) | ex[g] as usize];
            }
            if self.solve(0, &[0x3fu8; 7], &cons) {
                return true;
            }
            // next combination
            let mut p = 0;
            loop {
                if p == 6 {
                    return false;
                }
                idx[p] += 1;
                if idx[p] < sets[p].len() {
                    break;
                }
                idx[p] = 0;
                p += 1;
            }
        }
    }

    /// Exhaustive version: tries all 6^n assignments and tests each ground
    /// pair directly against the route table (no precomputed comp table, no
    /// forward checking).  Used only to cross-check is_pt.
    pub fn is_pt_brute(&self, fa: &[u32; 6], fo: &[u32; 6]) -> bool {
        let n = self.n_src;
        let (fp, pp) = self.forced_poss(fa, fo);
        let total = 6usize.pow(n as u32);
        let mut nn = vec![0usize; n];
        'outer: for code in 0..total {
            let mut c = code;
            for x in 0..n {
                nn[x] = c % 6;
                c /= 6;
            }
            for x in 0..n {
                for y in x + 1..n {
                    let g = self.cons_pair[x][y];
                    let routes = self.w[nn[x] * 6 + self.rev4[nn[y]]];
                    let mut found = false;
                    for l in 0..64u32 {
                        if (routes >> l) & 1 == 1
                            && (l as u8) & fp[g] == fp[g]
                            && (l as u8) & !pp[g] == 0
                        {
                            found = true;
                            break;
                        }
                    }
                    if !found {
                        continue 'outer;
                    }
                }
            }
            return true;
        }
        false
    }
}
