//! The group G = S_n x <rev> acting on V(CO_n), and a canonical form for
//! multisets of vertices under G.
//!
//! Canonical form: the lexicographically smallest sorted tuple of vertex
//! indices among all images g(M), g in G.  Vertex index 0 is the identity
//! cyclic order 0123...; G is transitive, so that minimum starts with 0, and
//! it starts with exactly mu zeros, where mu is the largest multiplicity in M
//! (more leading zeros is lexicographically smaller).  Hence the minimum is
//! attained by some g sending a max-multiplicity element of M to 0, and it is
//! enough to scan those g (|Stab(0)| = 2n of them per such element).

use crate::co::{next_permutation, Co};

pub struct Sym {
    pub nv: usize,
    pub ng: usize,
    /// act[g*nv + v] = g(v)
    pub act: Vec<u16>,
    /// whether g involves rev
    pub is_rev: Vec<bool>,
    /// to_zero[v] = all g with g(v) = 0
    pub to_zero: Vec<Vec<u32>>,
}

impl Sym {
    pub fn new(co: &Co) -> Sym {
        let n = co.n;
        let nv = co.nv;
        let mut act = Vec::new();
        let mut is_rev = Vec::new();
        let mut sigma: Vec<u8> = (0..n as u8).collect();
        loop {
            for r in 0..2 {
                for v in 0..nv {
                    let q: Vec<u8> = co.perms[v].iter().map(|&x| sigma[x as usize]).collect();
                    let mut w = co.idx(&q);
                    if r == 1 {
                        w = co.rev[w] as usize;
                    }
                    act.push(w as u16);
                }
                is_rev.push(r == 1);
            }
            if !next_permutation(&mut sigma) {
                break;
            }
        }
        let ng = is_rev.len();
        let mut to_zero = vec![Vec::new(); nv];
        for g in 0..ng {
            for v in 0..nv {
                if act[g * nv + v] == 0 {
                    to_zero[v].push(g as u32);
                }
            }
        }
        Sym { nv, ng, act, is_rev, to_zero }
    }

    /// ms must be sorted ascending; writes the canonical sorted tuple to best.
    #[inline]
    pub fn canon(&self, ms: &[u16], best: &mut [u16]) {
        let m = ms.len();
        let mut mu = 0;
        let mut i = 0;
        while i < m {
            let mut j = i;
            while j < m && ms[j] == ms[i] {
                j += 1;
            }
            mu = mu.max(j - i);
            i = j;
        }
        for b in best.iter_mut() {
            *b = u16::MAX;
        }
        let mut img = [0u16; 16];
        let mut i = 0;
        while i < m {
            let mut j = i;
            while j < m && ms[j] == ms[i] {
                j += 1;
            }
            if j - i == mu {
                for &g in &self.to_zero[ms[i] as usize] {
                    let row = &self.act[g as usize * self.nv..(g as usize + 1) * self.nv];
                    for k in 0..m {
                        img[k] = row[ms[k] as usize];
                    }
                    let s = &mut img[..m];
                    // insertion sort (m <= 16)
                    for a in 1..m {
                        let x = s[a];
                        let mut b = a;
                        while b > 0 && s[b - 1] > x {
                            s[b] = s[b - 1];
                            b -= 1;
                        }
                        s[b] = x;
                    }
                    if *s < *best {
                        best.copy_from_slice(s);
                    }
                }
            }
            i = j;
        }
    }

    /// Stabiliser of a canonical (sorted) multiset: (order, contains a
    /// rev-element).  Every stabilising g maps some max-multiplicity element
    /// to 0 (because 0 is a max-multiplicity element of the canonical form),
    /// so scanning to_zero of those elements finds all of them.
    pub fn stabiliser(&self, ms: &[u16]) -> (u32, bool) {
        let m = ms.len();
        let mut mult0 = 0;
        while mult0 < m && ms[mult0] == ms[0] {
            mult0 += 1;
        }
        assert_eq!(ms[0], 0, "stabiliser expects canonical form");
        let mut count = 0;
        let mut has_rev = false;
        let mut img = [0u16; 16];
        let mut i = 0;
        while i < m {
            let mut j = i;
            while j < m && ms[j] == ms[i] {
                j += 1;
            }
            if j - i == mult0 {
                for &g in &self.to_zero[ms[i] as usize] {
                    let row = &self.act[g as usize * self.nv..(g as usize + 1) * self.nv];
                    for k in 0..m {
                        img[k] = row[ms[k] as usize];
                    }
                    img[..m].sort_unstable();
                    if img[..m] == *ms {
                        count += 1;
                        if self.is_rev[g as usize] {
                            has_rev = true;
                        }
                    }
                }
            }
            i = j;
        }
        (count, has_rev)
    }
}

pub fn pack(v: &[u16]) -> u128 {
    let mut x = 0u128;
    for &e in v {
        debug_assert!(e < 1024);
        x = (x << 10) | e as u128;
    }
    x
}

pub fn unpack(x: u128, m: usize, out: &mut [u16]) {
    for i in 0..m {
        out[i] = ((x >> (10 * (m - 1 - i))) & 0x3ff) as u16;
    }
}
