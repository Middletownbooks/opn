//! The cyclic-order graph CO_n, written from Woodall's definition.
//!
//! Vertices: cyclic orderings of {0..n-1}, canonicalised by rotating 0 to the
//! front.  Edges: transpose the elements at cyclic positions i, i+1 (mod n),
//! including the wrap-around pair (n-1, 0).  Each edge is labelled by the
//! unordered pair of ground elements that were swapped.

use std::collections::{HashMap, HashSet, VecDeque};

pub fn next_permutation(a: &mut [u8]) -> bool {
    let n = a.len();
    if n < 2 {
        return false;
    }
    let mut i = n - 1;
    while i > 0 && a[i - 1] >= a[i] {
        i -= 1;
    }
    if i == 0 {
        return false;
    }
    let mut j = n - 1;
    while a[j] <= a[i - 1] {
        j -= 1;
    }
    a.swap(i - 1, j);
    a[i..].reverse();
    true
}

/// Rotate a cyclic sequence so that element 0 comes first.
pub fn canon_rot(seq: &[u8]) -> Vec<u8> {
    let pos = seq.iter().position(|&x| x == 0).expect("0 missing");
    (0..seq.len()).map(|i| seq[(pos + i) % seq.len()]).collect()
}

pub struct Co {
    pub n: usize,
    pub nv: usize,
    pub perms: Vec<Vec<u8>>,
    index: HashMap<Vec<u8>, u32>,
    /// adj[v] = list of (neighbour, label) -- one entry per cyclic position i.
    pub adj: Vec<Vec<(u32, u8)>>,
    pub rev: Vec<u32>,
    pub npairs: usize,
    pub pair_idx: Vec<Vec<u8>>,
    pub pairs: Vec<(u8, u8)>,
    pub dist: Vec<u8>,
}

impl Co {
    pub fn new(n: usize) -> Co {
        Co::new_relabelled(n, 0)
    }

    /// relabel_seed != 0: vertex indices are a pseudo-random permutation of
    /// the lexicographic order (so "lexicographically smallest index tuple"
    /// becomes a different canonical form).
    pub fn new_relabelled(n: usize, relabel_seed: u64) -> Co {
        let mut pairs = Vec::new();
        let mut pair_idx = vec![vec![255u8; n]; n];
        for x in 0..n {
            for y in x + 1..n {
                pair_idx[x][y] = pairs.len() as u8;
                pair_idx[y][x] = pairs.len() as u8;
                pairs.push((x as u8, y as u8));
            }
        }
        let mut perms = Vec::new();
        let mut rest: Vec<u8> = (1..n as u8).collect();
        loop {
            let mut p = vec![0u8];
            p.extend_from_slice(&rest);
            perms.push(p);
            if !next_permutation(&mut rest) {
                break;
            }
        }
        if relabel_seed != 0 {
            let mut st = relabel_seed;
            for i in (1..perms.len()).rev() {
                st ^= st << 13;
                st ^= st >> 7;
                st ^= st << 17;
                let j = (st % (i as u64 + 1)) as usize;
                perms.swap(i, j);
            }
        }
        let nv = perms.len();
        let index: HashMap<Vec<u8>, u32> = perms
            .iter()
            .enumerate()
            .map(|(i, p)| (p.clone(), i as u32))
            .collect();
        let lookup = |s: &[u8]| -> u32 { index[&canon_rot(s)] };
        let mut adj = Vec::with_capacity(nv);
        let mut rev = Vec::with_capacity(nv);
        for p in &perms {
            let mut nb = Vec::with_capacity(n);
            for i in 0..n {
                let j = (i + 1) % n;
                let mut q = p.clone();
                q.swap(i, j);
                nb.push((lookup(&q), pair_idx[p[i] as usize][p[j] as usize]));
            }
            adj.push(nb);
            // reverse cyclic order: read the cycle backwards
            let r: Vec<u8> = (0..n).map(|i| p[(n - i) % n]).collect();
            rev.push(lookup(&r));
        }
        let mut dist = vec![255u8; nv * nv];
        for s in 0..nv {
            let mut q = VecDeque::new();
            dist[s * nv + s] = 0;
            q.push_back(s);
            while let Some(u) = q.pop_front() {
                let du = dist[s * nv + u];
                for &(w, _) in &adj[u] {
                    let w = w as usize;
                    if dist[s * nv + w] == 255 {
                        dist[s * nv + w] = du + 1;
                        q.push_back(w);
                    }
                }
            }
        }
        Co { n, nv, perms, index, adj, rev, npairs: pairs.len(), pair_idx, pairs, dist }
    }

    pub fn idx(&self, seq: &[u8]) -> usize {
        self.index[&canon_rot(seq)] as usize
    }
    pub fn parse(&self, s: &str) -> usize {
        let seq: Vec<u8> = s.bytes().map(|b| b - b'0').collect();
        assert_eq!(seq.len(), self.n, "bad cyclic order {}", s);
        let mut chk = seq.clone();
        chk.sort();
        assert_eq!(chk, (0..self.n as u8).collect::<Vec<_>>(), "not a permutation: {}", s);
        self.idx(&seq)
    }
    pub fn name(&self, v: usize) -> String {
        self.perms[v].iter().map(|&x| (b'0' + x) as char).collect()
    }
    #[inline]
    pub fn d(&self, a: usize, b: usize) -> u8 {
        self.dist[a * self.nv + b]
    }
    #[inline]
    pub fn dbar(&self, a: usize, b: usize) -> u8 {
        self.d(a, self.rev[b] as usize)
    }
    pub fn dbar_table(&self) -> Vec<u8> {
        let nv = self.nv;
        let mut t = vec![0u8; nv * nv];
        for a in 0..nv {
            for b in 0..nv {
                t[a * nv + b] = self.dbar(a, b);
            }
        }
        t
    }

    /// For every (s,t): AND and OR of the label sets of all shortest s-t paths.
    /// Indexed [s*nv + t].  Dynamic programme over the geodesic DAG towards t:
    /// a shortest s-t path is an edge (s,u) with d(u,t) = d(s,t)-1 followed by
    /// a shortest u-t path, and AND_i(A u B_i) = A u AND_i B_i.
    pub fn geodesic_and_or(&self) -> (Vec<u32>, Vec<u32>) {
        let nv = self.nv;
        let full: u32 = if self.npairs >= 32 { !0 } else { (1u32 << self.npairs) - 1 };
        let mut and_t = vec![0u32; nv * nv];
        let mut or_t = vec![0u32; nv * nv];
        let mut order: Vec<usize> = (0..nv).collect();
        let mut a = vec![0u32; nv];
        let mut o = vec![0u32; nv];
        for t in 0..nv {
            order.sort_by_key(|&s| self.d(s, t));
            for &s in &order {
                if s == t {
                    a[s] = 0;
                    o[s] = 0;
                    continue;
                }
                let k = self.d(s, t);
                let mut aa = full;
                let mut oo = 0u32;
                let mut found = false;
                for &(u, l) in &self.adj[s] {
                    let u = u as usize;
                    if self.d(u, t) + 1 == k {
                        aa &= (1u32 << l) | a[u];
                        oo |= (1u32 << l) | o[u];
                        found = true;
                    }
                }
                assert!(found);
                a[s] = aa;
                o[s] = oo;
            }
            for s in 0..nv {
                and_t[s * nv + t] = a[s];
                or_t[s * nv + t] = o[s];
            }
        }
        (and_t, or_t)
    }

    /// Antipath tables: FA[a*nv+b] / FO[a*nv+b] = AND / OR of label sets over
    /// all shortest a -> rev(b) paths.
    pub fn antipath_tables(&self) -> (Vec<u32>, Vec<u32>) {
        let nv = self.nv;
        let (and_t, or_t) = self.geodesic_and_or();
        let mut fa = vec![0u32; nv * nv];
        let mut fo = vec![0u32; nv * nv];
        for a in 0..nv {
            for b in 0..nv {
                let t = self.rev[b] as usize;
                fa[a * nv + b] = and_t[a * nv + t];
                fo[a * nv + b] = or_t[a * nv + t];
            }
        }
        (fa, fo)
    }

    /// Explicit list of the distinct label sets of all shortest s-t paths.
    /// (Independent of geodesic_and_or; used to cross-check it.)
    pub fn geodesic_label_sets(&self, s: usize, t: usize) -> Vec<u32> {
        fn rec(co: &Co, v: usize, t: usize, memo: &mut HashMap<usize, Vec<u32>>) -> Vec<u32> {
            if v == t {
                return vec![0];
            }
            if let Some(x) = memo.get(&v) {
                return x.clone();
            }
            let k = co.d(v, t);
            let mut set = HashSet::new();
            for &(u, l) in &co.adj[v] {
                let u = u as usize;
                if co.d(u, t) + 1 == k {
                    for ls in rec(co, u, t, memo) {
                        set.insert(ls | (1u32 << l));
                    }
                }
            }
            let mut r: Vec<u32> = set.into_iter().collect();
            r.sort();
            memo.insert(v, r.clone());
            r
        }
        let mut memo = HashMap::new();
        rec(self, s, t, &mut memo)
    }
}

/// Readings of "antipath" (see the convention warning in the task).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Family {
    /// vertex-simple and label-distinct
    Both,
    /// label-distinct, vertices may repeat
    Walk,
    /// vertex-simple, labels may repeat
    Path,
    /// arbitrary walks
    Arbitrary,
}

impl Family {
    pub fn all() -> [Family; 4] {
        [Family::Both, Family::Walk, Family::Path, Family::Arbitrary]
    }
    pub fn from_str(s: &str) -> Family {
        match s {
            "both" => Family::Both,
            "walk" => Family::Walk,
            "path" => Family::Path,
            "arbitrary" => Family::Arbitrary,
            _ => panic!("unknown family {}", s),
        }
    }
}

/// For a small CO (npairs <= 6), W[u*nv+w] = bitmask over label subsets L
/// (0..64) such that some u -> w route of the given family has label set L.
/// The zero-length route (u == w, L = {}) is included in every family.
pub fn route_label_sets(co: &Co, fam: Family) -> Vec<u64> {
    assert!(co.npairs <= 6 && co.nv <= 64);
    let nv = co.nv;
    let mut res = vec![0u64; nv * nv];
    for u in 0..nv {
        match fam {
            Family::Arbitrary | Family::Walk => {
                // state = (vertex, label set used so far); exhaustive search.
                let mut seen = vec![false; nv * 64];
                let mut stack = vec![(u, 0usize)];
                seen[u * 64] = true;
                while let Some((v, ls)) = stack.pop() {
                    res[u * nv + v] |= 1u64 << ls;
                    for &(w, l) in &co.adj[v] {
                        if fam == Family::Walk && (ls >> l) & 1 == 1 {
                            continue;
                        }
                        let l2 = ls | (1usize << l);
                        let w = w as usize;
                        if !seen[w * 64 + l2] {
                            seen[w * 64 + l2] = true;
                            stack.push((w, l2));
                        }
                    }
                }
            }
            Family::Path | Family::Both => {
                fn dfs(co: &Co, fam: Family, v: usize, visited: u64, ls: usize, row: &mut [u64]) {
                    row[v] |= 1u64 << ls;
                    for &(w, l) in &co.adj[v] {
                        let w = w as usize;
                        if (visited >> w) & 1 == 1 {
                            continue;
                        }
                        if fam == Family::Both && (ls >> l) & 1 == 1 {
                            continue;
                        }
                        dfs(co, fam, w, visited | (1u64 << w), ls | (1usize << l), row);
                    }
                }
                let mut row = vec![0u64; nv];
                dfs(co, fam, u, 1u64 << u, 0, &mut row);
                res[u * nv..(u + 1) * nv].copy_from_slice(&row);
            }
        }
    }
    res
}
