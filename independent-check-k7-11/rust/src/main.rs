mod co;
mod pt;
mod search;
mod sym;

use co::{Co, Family};
use pt::PtTester;
use search::*;
use std::collections::BTreeMap;
use std::io::Write;
use std::time::Instant;
use sym::{pack, unpack, Sym};

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
}

fn build_ctx(n: usize, fam: Family) -> Ctx {
    build_ctx_r(n, fam, 0)
}

fn build_ctx_r(n: usize, fam: Family, relabel: u64) -> Ctx {
    let t0 = Instant::now();
    let co = Co::new_relabelled(n, relabel);
    if relabel != 0 {
        eprintln!("[ctx] vertex indices relabelled with seed {}; vertex 0 is now {}", relabel, co.name(0));
    }
    let co4 = Co::new(4);
    let dbar = co.dbar_table();
    let (fa, fo) = co.antipath_tables();
    let sym = Sym::new(&co);
    let pt = PtTester::new(&co4, fam, &co);
    eprintln!("[ctx] CO_{} built: {} vertices, |G| = {}, family {:?}, {:.2}s", n, co.nv, sym.ng, fam, t0.elapsed().as_secs_f64());
    Ctx { co, dbar, fa, fo, sym, pt }
}

fn check(name: &str, ok: bool, detail: String) -> bool {
    println!("[{}] {} -- {}", if ok { "PASS" } else { "FAIL" }, name, detail);
    ok
}

fn arg_val<T: std::str::FromStr>(args: &[String], key: &str, default: T) -> T {
    for i in 0..args.len() {
        if args[i] == key && i + 1 < args.len() {
            return args[i + 1].parse().ok().expect("bad arg");
        }
    }
    default
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cmd = args.get(1).map(|s| s.as_str()).unwrap_or("help");
    match cmd {
        "selfcheck" => selfcheck(),
        "enumerate" => enumerate(&args),
        "brute4" => brute4(&args),
        "dumpquads" => dumpquads(&args),
        "pt4" => pt4(&args),
        "minantisum" => minantisum(&args),
        "enumtau" => enumtau(&args),
        "recanon" => recanon(&args),
        "extendfrom" => extendfrom(&args),
        "coresearch" => coresearch(&args),
        "enumtau2" => enumtau2(&args),
        "equivariance" => equivariance(),
        "pttable-check" => pttable_check(&args),
        _ => eprintln!("usage: selfcheck | enumerate M T TARGET [--fam F] [--threads N] [--taucap C] [--dump FILE] | brute4 T | dumpquads COUNT SEED | pt4"),
    }
}

// ------------------------------------------------------------------------
fn selfcheck() {
    let mut all_ok = true;
    let t0 = Instant::now();
    let co4 = Co::new(4);
    let co6 = Co::new(6);
    let ctx = build_ctx(7, Family::Arbitrary);
    let co = &ctx.co;
    let nv = co.nv;

    // ---- Check 1 ----
    println!("== Check 1: CO_7 basics ==");
    let regular = co.adj.iter().all(|nb| {
        let mut s: Vec<u32> = nb.iter().map(|e| e.0).collect();
        s.sort();
        s.dedup();
        s.len() == 7
    });
    all_ok &= check("CO_7 vertex count", nv == 720, format!("{}", nv));
    all_ok &= check("CO_7 7-regular, 7 distinct neighbours per vertex", regular, String::new());
    let mut edges_sym = true;
    for v in 0..nv {
        for &(w, l) in &co.adj[v] {
            if !co.adj[w as usize].iter().any(|&(x, l2)| x as usize == v && l2 == l) {
                edges_sym = false;
            }
        }
    }
    all_ok &= check("edge relation symmetric with matching labels", edges_sym, String::new());
    let diam = *co.dist.iter().max().unwrap();
    let connected = !co.dist.iter().any(|&d| d == 255);
    all_ok &= check("connected, diameter 9", connected && diam == 9, format!("diameter {}", diam));
    let mut ok_self = true;
    let mut ok_anti = true;
    let mut ok_unique = true;
    let mut ok_revinv = true;
    for a in 0..nv {
        ok_self &= co.dbar(a, a) == 9;
        ok_anti &= co.dbar(a, co.rev[a] as usize) == 0;
        let far: Vec<usize> = (0..nv).filter(|&b| co.d(a, b) == 9).collect();
        ok_unique &= far == vec![co.rev[a] as usize];
        ok_revinv &= co.rev[co.rev[a] as usize] as usize == a;
    }
    all_ok &= check("dbar(a,a) = 9 for all a", ok_self, String::new());
    all_ok &= check("dbar(a,rev a) = 0 for all a", ok_anti, String::new());
    all_ok &= check("rev(a) is the unique vertex at distance 9", ok_unique, String::new());
    all_ok &= check("rev is an involution", ok_revinv, String::new());
    // bipartite colouring by BFS parity from vertex 0
    let col: Vec<u8> = (0..nv).map(|v| co.d(0, v) & 1).collect();
    let bip = (0..nv).all(|v| co.adj[v].iter().all(|&(w, _)| col[w as usize] != col[v]));
    let revflip = (0..nv).all(|v| col[co.rev[v] as usize] != col[v]);
    let mut parity_ok = true;
    for a in 0..nv {
        for b in 0..nv {
            parity_ok &= (co.dbar(a, b) & 1) == (1 + col[a] + col[b]) & 1;
        }
    }
    all_ok &= check("CO_7 bipartite", bip, String::new());
    all_ok &= check("rev swaps the colour classes", revflip, String::new());
    all_ok &= check("dbar(a,b) = 1 + col a + col b (mod 2) for all a,b", parity_ok, String::new());
    // dbar symmetric
    let dsym = (0..nv).all(|a| (0..nv).all(|b| co.dbar(a, b) == co.dbar(b, a)));
    all_ok &= check("dbar symmetric", dsym, String::new());

    // ---- group action ----
    println!("== Group S_7 x <rev> ==");
    let sym = &ctx.sym;
    let mut aut_ok = true;
    for g in 0..sym.ng {
        let row = &sym.act[g * nv..(g + 1) * nv];
        let mut seen = vec![false; nv];
        for v in 0..nv {
            seen[row[v] as usize] = true;
        }
        aut_ok &= seen.iter().all(|&s| s);
        for a in 0..nv {
            let ga = row[a] as usize;
            let rr = &ctx.dbar[ga * nv..(ga + 1) * nv];
            let r0 = &ctx.dbar[a * nv..(a + 1) * nv];
            for b in 0..nv {
                if rr[row[b] as usize] != r0[b] {
                    aut_ok = false;
                }
            }
        }
    }
    all_ok &= check("every g in G (10080) is a bijection preserving dbar on all 720^2 pairs", aut_ok && sym.ng == 10080, format!("|G| = {}", sym.ng));
    let stab_sizes_ok = (0..nv).all(|v| sym.to_zero[v].len() == 14);
    all_ok &= check("|{g : g(v) = 0}| = 14 for every v", stab_sizes_ok, String::new());

    // ---- geodesic label-set DP vs explicit enumeration ----
    println!("== Shortest-antipath label sets: AND/OR DP vs explicit enumeration ==");
    {
        let mut rng = Rng(0x9e3779b97f4a7c15);
        let mut ok = true;
        let mut maxsets = 0;
        for trial in 0..3000 {
            let (a, b) = if trial < 720 { (trial, trial) } else { (rng.below(nv), rng.below(nv)) };
            let sets = co.geodesic_label_sets(a, co.rev[b] as usize);
            maxsets = maxsets.max(sets.len());
            let and = sets.iter().fold(!0u32 & ((1 << 21) - 1), |x, &y| x & y);
            let or = sets.iter().fold(0u32, |x, &y| x | y);
            ok &= and == ctx.fa[a * nv + b] && or == ctx.fo[a * nv + b];
            // each label set of a shortest path of length k has between ... and k labels
            let k = co.dbar(a, b) as u32;
            ok &= sets.iter().all(|s| s.count_ones() <= k);
            // symmetry: (a,b) and (b,a) have the same label sets
            let sets2 = co.geodesic_label_sets(b, co.rev[a] as usize);
            ok &= sets == sets2;
        }
        all_ok &= check("DP masks equal AND/OR of explicitly enumerated label sets (3000 pairs incl. all (a,a)), and pair-symmetric", ok, format!("max #distinct label sets seen for one pair: {}", maxsets));
        let co6_t = co6.antipath_tables();
        let mut ok6 = true;
        for a in 0..co6.nv {
            for b in 0..co6.nv {
                let sets = co6.geodesic_label_sets(a, co6.rev[b] as usize);
                let and = sets.iter().fold((1u32 << 15) - 1, |x, &y| x & y);
                let or = sets.iter().fold(0u32, |x, &y| x | y);
                ok6 &= and == co6_t.0[a * co6.nv + b] && or == co6_t.1[a * co6.nv + b];
            }
        }
        all_ok &= check("same on all 120^2 pairs of CO_6", ok6, String::new());
        // label masks transform correctly under the group
        let mut okg = true;
        let mut sigma: Vec<u8> = (0..7).collect();
        let mut gi = 0usize;
        loop {
            let pmap: Vec<u32> = co.pairs.iter().map(|&(x, y)| co.pair_idx[sigma[x as usize] as usize][sigma[y as usize] as usize] as u32).collect();
            let mapmask = |m: u32| -> u32 { (0..21).filter(|&p| (m >> p) & 1 == 1).fold(0u32, |acc, p| acc | (1 << pmap[p])) };
            if gi % 37 == 0 {
                for r in 0..2 {
                    let g = gi * 2 + r;
                    for _ in 0..200 {
                        let a = rng_pair(&mut rng, nv);
                        let (x, y) = a;
                        let gx = sym.act[g * nv + x] as usize;
                        let gy = sym.act[g * nv + y] as usize;
                        okg &= ctx.fa[gx * nv + gy] == mapmask(ctx.fa[x * nv + y]);
                        okg &= ctx.fo[gx * nv + gy] == mapmask(ctx.fo[x * nv + y]);
                    }
                }
            }
            gi += 1;
            if !co::next_permutation(&mut sigma) {
                break;
            }
        }
        all_ok &= check("FORCED/POSS masks are equivariant under G (sampled)", okg, String::new());
    }

    // ---- Check 2 ----
    println!("== Check 2: CO_4 route families ==");
    let mut sizes = Vec::new();
    for fam in Family::all() {
        let w = co::route_label_sets(&co4, fam);
        let cnt: u32 = w.iter().map(|x| x.count_ones()).sum();
        sizes.push(cnt);
        // symmetry W[u][rev v] vs W[v][rev u]
        let mut symok = true;
        for u in 0..6 {
            for v in 0..6 {
                symok &= w[u * 6 + co4.rev[v] as usize] == w[v * 6 + co4.rev[u] as usize];
            }
        }
        println!("    {:?}: {} (endpoint, label-set) pairs; u->rev(v) vs v->rev(u) symmetric: {}", fam, cnt, symok);
        all_ok &= symok;
    }
    all_ok &= check("CO_4 family sizes both/walk/path/arbitrary = 234/282/594/1758", sizes == vec![234, 282, 594, 1758], format!("{:?}", sizes));
    let incl = {
        let ws: Vec<Vec<u64>> = Family::all().iter().map(|&f| co::route_label_sets(&co4, f)).collect();
        (0..36).all(|i| ws[0][i] & !ws[1][i] == 0 && ws[0][i] & !ws[2][i] == 0 && ws[1][i] & !ws[3][i] == 0 && ws[2][i] & !ws[3][i] == 0)
    };
    all_ok &= check("families nested: both <= walk, path <= arbitrary", incl, String::new());
    println!("    CO_4 vertices: {:?}", (0..6).map(|v| co4.name(v)).collect::<Vec<_>>());

    // ---- Check 3 ----
    println!("== Check 3: Woodall's (4,6) example ==");
    {
        let names = ["012345", "013542", "032541", "045231"];
        let q: Vec<usize> = names.iter().map(|s| co6.parse(s)).collect();
        let order = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];
        let ad: Vec<u8> = order.iter().map(|&(i, j)| co6.dbar(q[i], q[j])).collect();
        let nsets: Vec<usize> = order.iter().map(|&(i, j)| co6.geodesic_label_sets(q[i], co6.rev[q[j]] as usize).len()).collect();
        let s: u32 = ad.iter().map(|&x| x as u32).sum();
        all_ok &= check("antidistances (3,4,2,3,2,1), antisum 15", ad == vec![3, 4, 2, 3, 2, 1] && s == 15, format!("{:?} sum {}", ad, s));
        all_ok &= check("#distinct shortest-antipath label sets per pair (1,3,1,1,1,1)", nsets == vec![1, 3, 1, 1, 1, 1], format!("{:?}", nsets));
        let (fa6, fo6) = co6.antipath_tables();
        for fam in Family::all() {
            let tester = PtTester::new(&co4, fam, &co6);
            let qq = [q[0], q[1], q[2], q[3]];
            let (fa, fo) = tester.quad_masks(&qq, &fa6, &fo6, co6.nv);
            let r = tester.is_pt(&fa, &fo);
            let rb = tester.is_pt_brute(&fa, &fo);
            all_ok &= check(&format!("(4,6) example pseudo-tight under {:?}", fam), r && rb, format!("backtrack {} brute {}", r, rb));
        }
        // print the label sets for the record
        for (k, &(i, j)) in order.iter().enumerate() {
            let sets = co6.geodesic_label_sets(q[i], co6.rev[q[j]] as usize);
            let fmt: Vec<String> = sets.iter().map(|&s| fmt_labels(&co6, s)).collect();
            println!("    pair a{}a{} dbar {}: {}", i, j, ad[k], fmt.join(" | "));
        }
    }

    // ---- PT solver cross-checks ----
    println!("== PT solver cross-checks ==");
    {
        let mut rng = Rng(12345);
        let mut agree = 0;
        let mut disagree = 0;
        let mut npt = 0;
        let mut perm_ok = true;
        let mut g_ok = true;
        for trial in 0..400 {
            // bias toward low antisum quads (the interesting ones)
            let q = random_quad(&mut rng, &ctx, trial % 2 == 0);
            let (fa, fo) = ctx.pt.quad_masks(&q, &ctx.fa, &ctx.fo, nv);
            let r = ctx.pt.is_pt(&fa, &fo);
            let rb = ctx.pt.is_pt_brute(&fa, &fo);
            if r == rb { agree += 1 } else { disagree += 1 }
            if !r { npt += 1 }
            // invariance under permuting the 4 elements
            for _ in 0..4 {
                let mut q2 = q;
                for i in (1..4).rev() {
                    let j = rng.below(i + 1);
                    q2.swap(i, j);
                }
                let (fa2, fo2) = ctx.pt.quad_masks(&q2, &ctx.fa, &ctx.fo, nv);
                perm_ok &= ctx.pt.is_pt(&fa2, &fo2) == r;
            }
            // invariance under G
            for _ in 0..4 {
                let g = rng.below(ctx.sym.ng);
                let q3 = [0, 1, 2, 3].map(|i| ctx.sym.act[g * nv + q[i]] as usize);
                let (fa3, fo3) = ctx.pt.quad_masks(&q3, &ctx.fa, &ctx.fo, nv);
                g_ok &= ctx.pt.is_pt(&fa3, &fo3) == r;
            }
        }
        all_ok &= check("backtracking PT == exhaustive 6^7 PT on 400 random 4-sets", disagree == 0, format!("agree {} disagree {} (non-PT among them: {})", agree, disagree, npt));
        all_ok &= check("PT invariant under reordering the 4 elements", perm_ok, String::new());
        all_ok &= check("PT invariant under G", g_ok, String::new());
        let mut csym = true;
        for idx in 0..4096 {
            let c = ctx.pt.comp[idx];
            for u in 0..6 {
                for v in 0..6 {
                    csym &= ((c[u] >> v) & 1) == ((c[v] >> u) & 1);
                }
            }
        }
        all_ok &= check("compatibility tables symmetric in (N[x],N[y])", csym, String::new());
    }

    // ---- transversal solver cross-check ----
    {
        let mut rng = Rng(777);
        let mut ok = true;
        for _ in 0..300 {
            let npairs = 12;
            let ne = 1 + rng.below(12);
            let edges: Vec<u64> = (0..ne)
                .map(|_| {
                    let mut e = 0u64;
                    while e.count_ones() < 3 {
                        e |= 1 << rng.below(npairs);
                    }
                    e
                })
                .collect();
            let tau = min_transversal(&edges, 64);
            ok &= has_transversal_of_size(&edges, npairs, tau as usize) && (tau == 0 || !has_transversal_of_size(&edges, npairs, tau as usize - 1));
        }
        all_ok &= check("min_transversal == brute force on 300 random hypergraphs", ok, String::new());
    }

    // ---- Check 6a ----
    println!("== Check 6a: Zarankiewicz multisets 5a + 6rev(a) ==");
    {
        let quads = Quads::new(11);
        let mut ok = true;
        let mut worst_t = 0;
        for a in 0..nv {
            let r = co.rev[a] as u16;
            let mut ms: Vec<u16> = vec![a as u16; 5];
            ms.extend(vec![r; 6]);
            let ab = antisum(&ctx, &ms);
            let e = non_pt_edges(&ctx, &quads, &ms);
            ok &= ab == 225 && e.is_empty();
            worst_t = worst_t.max(e.len());
        }
        all_ok &= check("for all 720 a: antisum 225 and t = 0", ok, format!("max t over a: {}", worst_t));
    }

    // ---- Check 7 ----
    println!("== Check 7: the antisum-219 representative ==");
    {
        let names = ["0123456", "0123456", "0125463", "0152436", "0163452", "0452136", "0543621", "0625431", "0634125", "0635421", "0643521"];
        let expect: [[u8; 11]; 11] = [
            [9, 9, 5, 5, 4, 4, 3, 3, 4, 2, 2],
            [9, 9, 5, 5, 4, 4, 3, 3, 4, 2, 2],
            [5, 5, 9, 7, 2, 2, 5, 5, 4, 2, 2],
            [5, 5, 7, 9, 2, 4, 5, 5, 2, 2, 2],
            [4, 4, 2, 2, 9, 5, 2, 2, 5, 7, 7],
            [4, 4, 2, 4, 5, 9, 4, 4, 3, 5, 5],
            [3, 3, 5, 5, 2, 4, 9, 5, 4, 4, 4],
            [3, 3, 5, 5, 2, 4, 5, 9, 4, 4, 4],
            [4, 4, 4, 2, 5, 3, 4, 4, 9, 5, 5],
            [2, 2, 2, 2, 7, 5, 4, 4, 5, 9, 7],
            [2, 2, 2, 2, 7, 5, 4, 4, 5, 7, 9],
        ];
        let ms: Vec<u16> = names.iter().map(|s| co.parse(s) as u16).collect();
        let mut mat_ok = true;
        for i in 0..11 {
            let row: Vec<u8> = (0..11).map(|j| co.dbar(ms[i] as usize, ms[j] as usize)).collect();
            println!("    {}", row.iter().map(|x| format!("{:2}", x)).collect::<Vec<_>>().join(" "));
            mat_ok &= row[..] == expect[i][..];
        }
        all_ok &= check("antidistance matrix matches the stated one", mat_ok, String::new());
        let ab = antisum(&ctx, &ms);
        all_ok &= check("antisum 219", ab == 219, format!("{}", ab));
        let quads = Quads::new(11);
        let e = non_pt_edges(&ctx, &quads, &ms);
        let tau = min_transversal(&e, 64);
        println!("    my numbers: t = {}, tau = {}", e.len(), tau);
        all_ok &= check("t = 103 (arbitrary walks)", e.len() == 103, format!("{}", e.len()));
        all_ok &= check("tau = 8", tau == 8, format!("{}", tau));
        // t under other readings, for information
        for fam in Family::all() {
            let tester = PtTester::new(&co4, fam, co);
            let mut t = 0;
            for q in &quads.quads {
                let qq = [ms[q[0]] as usize, ms[q[1]] as usize, ms[q[2]] as usize, ms[q[3]] as usize];
                let (fa, fo) = tester.quad_masks(&qq, &ctx.fa, &ctx.fo, nv);
                if !tester.is_pt(&fa, &fo) {
                    t += 1;
                }
            }
            println!("    (info) t under {:?} = {}", fam, t);
        }
        // canonical form and orbit size of this representative
        let mut sorted = ms.clone();
        sorted.sort();
        let mut best = vec![0u16; 11];
        sym.canon(&sorted, &mut best);
        let (stab, has_rev) = sym.stabiliser(&best);
        println!("    canonical form: {:?}", best.iter().map(|&v| co.name(v as usize)).collect::<Vec<_>>());
        all_ok &= check("orbit of the representative has 5040 distinct multisets", sym.ng as u32 / stab == 5040, format!("|Stab| = {}, contains a rev-element: {}", stab, has_rev));
    }

    println!("== selfcheck {} in {:.1}s ==", if all_ok { "ALL PASSED" } else { "HAD FAILURES" }, t0.elapsed().as_secs_f64());
}

fn rng_pair(rng: &mut Rng, nv: usize) -> (usize, usize) {
    (rng.below(nv), rng.below(nv))
}

fn fmt_labels(co: &Co, mask: u32) -> String {
    let v: Vec<String> = (0..co.npairs).filter(|&p| (mask >> p) & 1 == 1).map(|p| format!("{}{}", co.pairs[p].0, co.pairs[p].1)).collect();
    format!("{{{}}}", v.join(","))
}

/// Random 4-multiset; if `low`, build it greedily near-antipodal so that the
/// sample contains plenty of low-antisum (and non-pseudo-tight) quads.
fn random_quad(rng: &mut Rng, ctx: &Ctx, low: bool) -> [usize; 4] {
    let nv = ctx.co.nv;
    if !low {
        return [rng.below(nv), rng.below(nv), rng.below(nv), rng.below(nv)];
    }
    let a = rng.below(nv);
    let pick_near = |rng: &mut Rng, x: usize, maxd: u8| -> usize {
        loop {
            let y = rng.below(nv);
            if ctx.co.d(x, y) <= maxd {
                return y;
            }
        }
    };
    let ra = ctx.co.rev[a] as usize;
    let b = pick_near(rng, ra, 3);
    let c = pick_near(rng, a, 3);
    let d = pick_near(rng, ra, 3);
    [a, b, c, d]
}

// ------------------------------------------------------------------------
fn enumerate(args: &[String]) {
    let m: usize = args[2].parse().unwrap();
    let t: u32 = args[3].parse().unwrap();
    let target: u32 = args[4].parse().unwrap();
    let fam = Family::from_str(&arg_val(args, "--fam", "arbitrary".to_string()));
    let nthreads: usize = arg_val(args, "--threads", 4);
    let taucap: u32 = arg_val(args, "--taucap", 64);
    let dump: String = arg_val(args, "--dump", String::new());
    let dump_below: u32 = arg_val(args, "--dump-below", u32::MAX);
    let noanalyze = args.iter().any(|a| a == "--noanalyze");
    let astar_arg: String = arg_val(args, "--astar", String::new());
    let relabel: u64 = arg_val(args, "--relabel", 0);
    let save_level: usize = arg_val(args, "--save-level", 0);
    let save_file: String = arg_val(args, "--save-file", String::new());
    let ctx = build_ctx_r(7, fam, relabel);
    if relabel != 0 {
        println!("canonical form: lex-min under vertex relabelling seed {} (vertex 0 = {})", relabel, ctx.co.name(0));
    }
    let th = thresholds(m, t);
    println!("(m,n) = ({},7), top threshold T = {}, target = {}, family {:?}", m, t, target, fam);
    println!("thresholds T_k: {:?}", &th[1..]);
    let astar: Vec<u32> = if astar_arg.is_empty() { Vec::new() } else { astar_arg.split(',').map(|x| x.parse().unwrap()).collect() };
    let look_store;
    let look = if astar.is_empty() {
        None
    } else {
        let full = extend_astar(&astar, m);
        println!("lookahead ON, A*(r) lower bounds used for r = 0..{}: {:?}", m, full);
        look_store = Lookahead { m, t, astar: Box::leak(full.into_boxed_slice()) };
        Some(&look_store)
    };
    let t0 = Instant::now();
    let mut level: Vec<u128> = vec![pack(&[0])];
    println!("level  1: T = {:3}  orbits {:>12}", th[1], 1);
    for k in 2..=m {
        let tl = Instant::now();
        let (next, st) = extend_level(&ctx, &level, k - 1, th[k], nthreads, look);
        println!(
            "level {:2}: T = {:3}  parents {:>12}  candidates(Abar<=T) {:>14}  after max-contribution filter {:>14}  lookahead-cut {:>12}  orbits {:>12}  [{:.1}s]",
            k, th[k], st.parents, st.candidates, st.after_filter, st.lookahead_cut, st.orbits, tl.elapsed().as_secs_f64()
        );
        std::io::stdout().flush().ok();
        level = next;
        if save_level == k {
            save_list(&save_file, &level);
            println!("saved level {} ({} orbits) to {}", k, level.len(), save_file);
        }
    }
    println!("enumeration wall time {:.1}s", t0.elapsed().as_secs_f64());
    // antisum histogram at top level
    let mut ms = [0u16; 16];
    let mut hist: BTreeMap<u32, usize> = BTreeMap::new();
    for &x in &level {
        unpack(x, m, &mut ms);
        *hist.entry(antisum(&ctx, &ms[..m])).or_default() += 1;
    }
    println!("top-level orbits by antisum: {:?}", hist);
    if noanalyze {
        return;
    }
    let ta = Instant::now();
    let info = analyze(&ctx, &level, m, taucap, nthreads);
    println!("analysis wall time {:.1}s", ta.elapsed().as_secs_f64());
    let mut by_ab: BTreeMap<u32, Vec<usize>> = BTreeMap::new();
    for (i, o) in info.iter().enumerate() {
        by_ab.entry(o.abar).or_default().push(i);
    }
    let mut counterexamples = 0usize;
    let ng = ctx.sym.ng as u64;
    for (ab, idxs) in &by_ab {
        let labelled: u64 = idxs.iter().map(|&i| ng / info[i].stab as u64).sum();
        let sn_orbits: u64 = idxs.iter().map(|&i| if info[i].stab_has_rev { 1 } else { 2 }).sum();
        let tmin = idxs.iter().map(|&i| info[i].t).min().unwrap();
        let tmax = idxs.iter().map(|&i| info[i].t).max().unwrap();
        let mut tauh: BTreeMap<u32, usize> = BTreeMap::new();
        for &i in idxs {
            *tauh.entry(info[i].tau).or_default() += 1;
        }
        let bad: Vec<usize> = idxs.iter().cloned().filter(|&i| info[i].abar + 2 * info[i].tau < target).collect();
        counterexamples += bad.len();
        let minbound = idxs.iter().map(|&i| info[i].abar + 2 * info[i].tau).min().unwrap();
        println!(
            "antisum {:3}: G-orbits {:>10}  S_7-orbits {:>10}  labelled multisets {:>14}  t in [{}, {}]  min(Abar+2tau) {}  tau histogram{} {:?}  below target: {}",
            ab, idxs.len(), sn_orbits, labelled, tmin, tmax, minbound, if taucap < 64 { format!(" (capped at {})", taucap) } else { String::new() }, tauh, bad.len()
        );
        for &i in bad.iter().take(20) {
            unpack(level[i], m, &mut ms);
            println!("   COUNTEREXAMPLE: {:?} t={} tau={}", ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect::<Vec<_>>(), info[i].t, info[i].tau);
        }
    }
    println!("TOTAL counterexamples (Abar + 2 tau < {}): {}", target, counterexamples);
    if !dump.is_empty() {
        let mut f = std::io::BufWriter::new(std::fs::File::create(&dump).unwrap());
        let mut nd = 0;
        for (i, &x) in level.iter().enumerate() {
            if dump_below != u32::MAX && info[i].abar + 2 * info[i].tau > dump_below {
                continue;
            }
            unpack(x, m, &mut ms);
            let names: Vec<String> = ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect();
            writeln!(f, "{} {} {} {}", names.join(","), info[i].abar, info[i].t, info[i].tau).unwrap();
            nd += 1;
        }
        println!("dumped {} orbits to {}", nd, dump);
    }
    println!("total wall time {:.1}s", t0.elapsed().as_secs_f64());
}

/// Independent enumeration of 4-multisets with antisum <= T: every 4-multiset
/// containing vertex 0 (by transitivity every orbit has such a member),
/// canonicalised and deduplicated.  Compared against the cascade.
fn brute4(args: &[String]) {
    let t: u32 = args[2].parse().unwrap();
    let ctx = build_ctx(7, Family::Arbitrary);
    let nv = ctx.co.nv;
    let mut found: Vec<u128> = Vec::new();
    let mut best = [0u16; 4];
    for b in 0..nv {
        for c in b..nv {
            let ab0 = ctx.dbar[b] as u32 + ctx.dbar[c] as u32 + ctx.dbar[b * nv + c] as u32;
            if ab0 > t {
                continue;
            }
            for d in c..nv {
                let ab = ab0 + ctx.dbar[d] as u32 + ctx.dbar[b * nv + d] as u32 + ctx.dbar[c * nv + d] as u32;
                if ab <= t {
                    let ms = [0u16, b as u16, c as u16, d as u16];
                    ctx.sym.canon(&ms, &mut best);
                    found.push(pack(&best));
                }
            }
        }
    }
    found.sort_unstable();
    found.dedup();
    let th = thresholds(4, t);
    let mut level: Vec<u128> = vec![pack(&[0])];
    for k in 2..=4 {
        level = extend_level(&ctx, &level, k - 1, th[k], 4, None).0;
    }
    println!("4-multisets with antisum <= {}: brute force {} orbits, cascade {} orbits, identical lists: {}", t, found.len(), level.len(), found == level);
}

/// Dump random 4-multisets with their PT verdict, for the Python cross-check.
fn dumpquads(args: &[String]) {
    let count: usize = args[2].parse().unwrap();
    let seed: u64 = args[3].parse().unwrap();
    let ctx = build_ctx(7, Family::Arbitrary);
    let nv = ctx.co.nv;
    let mut rng = Rng(seed | 1);
    for i in 0..count {
        let q = random_quad(&mut rng, &ctx, i % 4 != 0);
        let (fa, fo) = ctx.pt.quad_masks(&q, &ctx.fa, &ctx.fo, nv);
        let r = ctx.pt.is_pt(&fa, &fo);
        println!("{} {} {} {} {}", ctx.co.name(q[0]), ctx.co.name(q[1]), ctx.co.name(q[2]), ctx.co.name(q[3]), if r { 1 } else { 0 });
    }
}

/// Read 4-multisets (4 cyclic orders per line) on stdin, print PT verdicts.
fn pt4(args: &[String]) {
    let fam = Family::from_str(&arg_val(args, "--fam", "arbitrary".to_string()));
    let ctx = build_ctx(7, fam);
    let nv = ctx.co.nv;
    let stdin = std::io::stdin();
    let mut line = String::new();
    while { line.clear(); stdin.read_line(&mut line).unwrap() > 0 } {
        let f: Vec<&str> = line.split_whitespace().collect();
        if f.len() < 4 {
            continue;
        }
        let q = [ctx.co.parse(f[0]), ctx.co.parse(f[1]), ctx.co.parse(f[2]), ctx.co.parse(f[3])];
        let (fa, fo) = ctx.pt.quad_masks(&q, &ctx.fa, &ctx.fo, nv);
        println!("{} {}", f[..4].join(" "), if ctx.pt.is_pt(&fa, &fo) { 1 } else { 0 });
    }
}

fn zar(k: usize) -> u32 {
    ((k / 2) * ((k.max(1) - 1) / 2)) as u32
}

/// Extend exact values A*(0..len) to sound lower bounds up to m via
/// sum_v Abar(M - v) = (r-2) Abar(M)  =>  A*(r) >= ceil(r A*(r-1) / (r-2)).
fn extend_astar(exact: &[u32], m: usize) -> Vec<u32> {
    let mut a: Vec<u32> = exact.to_vec();
    while a.len() <= m {
        let r = a.len() as u32;
        let prev = a[r as usize - 1];
        a.push(if r <= 2 { 0 } else { (r * prev + r - 3) / (r - 2) });
    }
    a.truncate(m + 1);
    a
}

/// Minimum antisum A*(k) of (k,7)-sets for k = 0..=K, each found by running
/// the (complete) cascade at T = 9 Z(k), the antisum of a Zarankiewicz
/// multiset (floor(k/2) copies of a, ceil(k/2) of rev a), which is an upper
/// bound.  The lookahead for size k uses the A*(r), r < k, already found.
fn minantisum(args: &[String]) {
    let upto: usize = args[2].parse().unwrap();
    let nthreads: usize = arg_val(args, "--threads", 4);
    let ctx = build_ctx(7, Family::Arbitrary);
    let mut astar: Vec<u32> = vec![0, 0];
    for k in 2..=upto {
        let t = 9 * zar(k);
        let th = thresholds(k, t);
        let full = extend_astar(&astar, k);
        let look = Lookahead { m: k, t, astar: &full };
        let mut level: Vec<u128> = vec![pack(&[0])];
        let tl = Instant::now();
        let mut sizes = Vec::new();
        for j in 2..=k {
            let (next, st) = extend_level(&ctx, &level, j - 1, th[j], nthreads, Some(&look));
            sizes.push(st.orbits);
            level = next;
        }
        let mut ms = [0u16; 16];
        let mut hist: BTreeMap<u32, usize> = BTreeMap::new();
        for &x in &level {
            unpack(x, k, &mut ms);
            *hist.entry(antisum(&ctx, &ms[..k])).or_default() += 1;
        }
        let mn = *hist.keys().next().unwrap();
        println!("k = {:2}: T = 9 Z(k) = {:3}; level sizes {:?}; orbits by antisum {:?}; A*({}) = {}  [{:.1}s]", k, t, sizes, hist, k, mn, tl.elapsed().as_secs_f64());
        std::io::stdout().flush().ok();
        astar.push(mn);
    }
    println!("A* = {:?}", astar);
}

/// tau-pruned cascade: all orbits of (m,7)-sets with Abar + 2 tau <= T.
fn enumtau(args: &[String]) {
    let m: usize = args[2].parse().unwrap();
    let t: u32 = args[3].parse().unwrap();
    let fam = Family::from_str(&arg_val(args, "--fam", "arbitrary".to_string()));
    let nthreads: usize = arg_val(args, "--threads", 4);
    let dump: String = arg_val(args, "--dump", String::new());
    let relabel: u64 = arg_val(args, "--relabel", 0);
    let astar_arg: String = arg_val(args, "--astar", String::new());
    let ctx = build_ctx_r(7, fam, relabel);
    let exact: Vec<u32> = astar_arg.split(',').map(|x| x.parse().unwrap()).collect();
    let astar = extend_astar(&exact, m);
    let abmax: u32 = arg_val(args, "--abmax", t);
    let th0 = thresholds(m, t.min(abmax));
    println!("tau-pruned cascade: (m,n) = ({},7), survivors = orbits with Abar + 2 tau <= {}, family {:?}", m, t, fam);
    if relabel != 0 {
        println!("canonical form: lex-min under vertex relabelling seed {} (vertex 0 = {})", relabel, ctx.co.name(0));
    }
    println!("A*(r) lower bounds used, r = 0..{}: {:?}  (exact input: {:?}; rest derived by A*(r) >= ceil(r A*(r-1)/(r-2)))", m, astar, exact);
    if abmax < t {
        println!("additional cap: Abar <= {}", abmax);
    }
    println!("tau = 0 thresholds T_k: {:?}", &th0[1..]);
    let look = Lookahead { m, t: t.min(abmax), astar: &astar };
    let t0 = Instant::now();
    let mut level: Vec<u128> = vec![pack(&[0])];
    let mut info: Vec<(u32, u32, u32)> = vec![(0, 0, 0)];
    for k in 2..=m {
        let tl = Instant::now();
        let (children, st) = extend_level(&ctx, &level, k - 1, th0[k], nthreads, Some(&look));
        let tg = tl.elapsed().as_secs_f64();
        let (kept, inf, fs) = tau_filter(&ctx, &children, k, m, t, abmax, &astar, nthreads);
        println!(
            "level {:2}: parents {:>11}  cand(Abar<=T_k) {:>13}  max-contrib {:>13}  lookahead-cut {:>12}  orbits {:>11}  tau-hist {:?}  kept {:>11}  [gen {:.1}s, tau {:.1}s]",
            k, st.parents, st.candidates, st.after_filter, st.lookahead_cut, fs.before, &fs.tau_hist[..6], fs.after, tg, tl.elapsed().as_secs_f64() - tg
        );
        std::io::stdout().flush().ok();
        level = kept;
        info = inf;
    }
    println!("search wall time {:.1}s", t0.elapsed().as_secs_f64());
    let mut hist: BTreeMap<(u32, u32), usize> = BTreeMap::new();
    for &(ab, _, tau) in &info {
        *hist.entry((ab, tau)).or_default() += 1;
    }
    println!("SURVIVORS (orbits with Abar + 2 tau <= {}): {}", t, level.len());
    for ((ab, tau), n) in &hist {
        println!("   Abar {:3}  tau {}  : {} orbits", ab, tau, n);
    }
    if !dump.is_empty() {
        let mut f = std::io::BufWriter::new(std::fs::File::create(&dump).unwrap());
        let mut ms = [0u16; 16];
        for (i, &x) in level.iter().enumerate() {
            unpack(x, m, &mut ms);
            let names: Vec<String> = ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect();
            writeln!(f, "{} {} {} {}", names.join(","), info[i].0, info[i].1, info[i].2).unwrap();
        }
        println!("dumped {} orbits to {}", level.len(), dump);
    }
}

/// Read a dump (first field = comma-separated cyclic orders), print each line
/// with the multiset replaced by its canonical form under the DEFAULT vertex
/// numbering.  Lets runs with different canonical forms be compared.
fn recanon(_args: &[String]) {
    let ctx = build_ctx(7, Family::Arbitrary);
    let stdin = std::io::stdin();
    let mut line = String::new();
    let out = std::io::stdout();
    let mut out = std::io::BufWriter::new(out.lock());
    while {
        line.clear();
        stdin.read_line(&mut line).unwrap() > 0
    } {
        let f: Vec<&str> = line.split_whitespace().collect();
        if f.is_empty() {
            continue;
        }
        let mut ms: Vec<u16> = f[0].split(',').map(|s| ctx.co.parse(s) as u16).collect();
        ms.sort();
        let mut best = vec![0u16; ms.len()];
        ctx.sym.canon(&ms, &mut best);
        let names: Vec<String> = best.iter().map(|&v| ctx.co.name(v as usize)).collect();
        writeln!(out, "{} {}", names.join(","), f[1..].join(" ")).unwrap();
    }
}

fn save_list(path: &str, list: &[u128]) {
    let mut f = std::io::BufWriter::new(std::fs::File::create(path).unwrap());
    for &x in list {
        f.write_all(&x.to_le_bytes()).unwrap();
    }
}

fn load_list(path: &str) -> Vec<u128> {
    let bytes = std::fs::read(path).unwrap();
    assert_eq!(bytes.len() % 16, 0);
    bytes.chunks(16).map(|c| u128::from_le_bytes(c.try_into().unwrap())).collect()
}

/// Largest value <= x that a k-multiset antisum can take.  For odd k the
/// antisum is C(k,2) + (k-1)*(colour sum) = C(k,2) (mod 2) since CO_7 is
/// bipartite with dbar(a,b) = 1 + col a + col b (mod 2); for even k both
/// parities occur.
fn parity_floor(x: u32, k: usize) -> u32 {
    if k % 2 == 1 {
        let p = ((k * (k - 1) / 2) % 2) as u32;
        if x % 2 == p { x } else { x - 1 }
    } else {
        x
    }
}

/// Resume a cascade from a saved complete level: FILE must hold every orbit
/// of K-multisets with Abar <= FILE_T (as produced by `enumerate ... --save-level K`).
/// Valid for target (m, T) iff parity_floor(thresholds(m,T)[K], K) <= FILE_T,
/// which is checked.
fn extendfrom(args: &[String]) {
    let file = &args[2];
    let kf: usize = args[3].parse().unwrap();
    let file_t: u32 = args[4].parse().unwrap();
    let m: usize = args[5].parse().unwrap();
    let t: u32 = args[6].parse().unwrap();
    let target: u32 = arg_val(args, "--target", 0);
    let nthreads: usize = arg_val(args, "--threads", 4);
    let astar_arg: String = arg_val(args, "--astar", String::new());
    let dump: String = arg_val(args, "--dump", String::new());
    let relabel: u64 = arg_val(args, "--relabel", 0);
    let ctx = build_ctx_r(7, Family::Arbitrary, relabel);
    if relabel != 0 {
        println!("canonical form: lex-min under vertex relabelling seed {} (vertex 0 = {}); the file must come from a run with the same seed", relabel, ctx.co.name(0));
    }
    let th = thresholds(m, t);
    let need = parity_floor(th[kf], kf);
    println!("extendfrom: level-{} file with all orbits of Abar <= {}; target (m,T) = ({},{}); thresholds {:?}; level {} needs Abar <= {} (parity floor of {})", kf, file_t, m, t, &th[1..], kf, need, th[kf]);
    assert!(need <= file_t, "saved level is not complete enough for this target");
    let astar: Vec<u32> = if astar_arg.is_empty() { Vec::new() } else { astar_arg.split(',').map(|x| x.parse().unwrap()).collect() };
    let full = if astar.is_empty() { Vec::new() } else { extend_astar(&astar, m) };
    let look = Lookahead { m, t, astar: &full };
    let mut level = load_list(file);
    println!("loaded {} orbits", level.len());
    let mut ms = [0u16; 16];
    // keep only those within this target's threshold at level kf
    level.retain(|&x| {
        unpack(x, kf, &mut ms);
        antisum(&ctx, &ms[..kf]) <= th[kf]
    });
    println!("level {:2}: {} orbits with Abar <= {}", kf, level.len(), th[kf]);
    let t0 = Instant::now();
    for k in kf + 1..=m {
        let (next, st) = extend_level(&ctx, &level, k - 1, th[k], nthreads, if full.is_empty() { None } else { Some(&look) });
        println!(
            "level {:2}: T = {:3}  parents {:>12}  candidates(Abar<=T) {:>14}  after max-contribution filter {:>14}  lookahead-cut {:>12}  orbits {:>12}",
            k, th[k], st.parents, st.candidates, st.after_filter, st.lookahead_cut, st.orbits
        );
        level = next;
    }
    println!("extension wall time {:.1}s", t0.elapsed().as_secs_f64());
    let mut hist: BTreeMap<u32, usize> = BTreeMap::new();
    for &x in &level {
        unpack(x, m, &mut ms);
        *hist.entry(antisum(&ctx, &ms[..m])).or_default() += 1;
    }
    println!("top-level orbits by antisum: {:?}", hist);
    if target > 0 && !level.is_empty() {
        let info = analyze(&ctx, &level, m, 64, nthreads);
        let ng = ctx.sym.ng as u64;
        let mut by_ab: BTreeMap<u32, Vec<usize>> = BTreeMap::new();
        for (i, o) in info.iter().enumerate() {
            by_ab.entry(o.abar).or_default().push(i);
        }
        for (ab, idxs) in &by_ab {
            let labelled: u64 = idxs.iter().map(|&i| ng / info[i].stab as u64).sum();
            let mut tauh: BTreeMap<u32, usize> = BTreeMap::new();
            for &i in idxs {
                *tauh.entry(info[i].tau).or_default() += 1;
            }
            let tmin = idxs.iter().map(|&i| info[i].t).min().unwrap();
            let tmax = idxs.iter().map(|&i| info[i].t).max().unwrap();
            let bad = idxs.iter().filter(|&&i| info[i].abar + 2 * info[i].tau < target).count();
            println!("antisum {}: G-orbits {}  labelled multisets {}  t in [{}, {}]  tau histogram {:?}  below {}: {}", ab, idxs.len(), labelled, tmin, tmax, tauh, target, bad);
        }
        if !dump.is_empty() {
            let mut f = std::io::BufWriter::new(std::fs::File::create(&dump).unwrap());
            for (i, &x) in level.iter().enumerate() {
                unpack(x, m, &mut ms);
                let names: Vec<String> = ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect();
                writeln!(f, "{} {} {} {} stab={}", names.join(","), info[i].abar, info[i].t, info[i].tau, info[i].stab).unwrap();
            }
        }
    }
}

/// All orbits of (m,7)-sets with Abar + 2 tau <= T, found through
/// pseudo-tight cores (see search::core_filter for the argument).
fn coresearch(args: &[String]) {
    let m: usize = args[2].parse().unwrap();
    let t: u32 = args[3].parse().unwrap();
    let nthreads: usize = arg_val(args, "--threads", 4);
    let dump: String = arg_val(args, "--dump", String::new());
    let relabel: u64 = arg_val(args, "--relabel", 0);
    let fam = Family::from_str(&arg_val(args, "--fam", "arbitrary".to_string()));
    let astar_arg: String = arg_val(args, "--astar", String::new());
    let only_j: i64 = arg_val(args, "--only-j", -1);
    let ctx = build_ctx_r(7, fam, relabel);
    let exact: Vec<u32> = astar_arg.split(',').map(|x| x.parse().unwrap()).collect();
    let astar = extend_astar(&exact, m);
    let mut jmax = 0usize;
    while t >= 2 * (jmax as u32 + 1) && t - 2 * (jmax as u32 + 1) >= astar[m] {
        jmax += 1;
    }
    println!("core search: (m,n) = ({},7), survivors = orbits with Abar + 2 tau <= {}, family {:?}", m, t, fam);
    if relabel != 0 {
        println!("canonical form: lex-min under vertex relabelling seed {} (vertex 0 = {})", relabel, ctx.co.name(0));
    }
    println!("A*(r) lower bounds, r = 0..{}: {:?}  (exact input {:?})", m, astar, exact);
    println!("cases tau(M) = j for j = 0..{} (tau >= {} would need Abar <= {} < A*({}) = {})", jmax, jmax + 1, t as i64 - 2 * (jmax as i64 + 1), m, astar[m]);
    let t0 = Instant::now();
    let mut all: Vec<(u128, u32, u32, u32)> = Vec::new();
    for j in 0..=jmax {
        if only_j >= 0 && only_j as usize != j {
            continue;
        }
        let tj = Instant::now();
        let tm = t - 2 * j as u32;
        let mz = m - j;
        let th_loose = thresholds(mz, tm - astar[j]);
        println!("--- case j = {}: cores of size {}, Abar(M) <= {}, loose core thresholds {:?}", j, mz, tm, &th_loose[1..]);
        let look = Lookahead { m, t: tm, astar: &astar };
        let mut level: Vec<u128> = vec![pack(&[0])];
        for k in 2..=mz {
            let tl = Instant::now();
            let (children, st) = extend_level_ex(&ctx, &level, k - 1, th_loose[k], nthreads, Some(&look), true);
            let (kept, fs) = core_filter(&ctx, &children, k, m, j, tm, &astar, nthreads);
            println!(
                "  level {:2}: parents {:>11}  cand {:>13}  max-contrib {:>13}  t>0 cut {:>12}  lookahead cut {:>12}  orbits {:>11}  kept {:>11}  [{:.1}s]",
                k, st.parents, st.candidates, st.after_filter, st.t0_cut, st.lookahead_cut, fs.before, fs.after, tl.elapsed().as_secs_f64()
            );
            std::io::stdout().flush().ok();
            level = kept;
        }
        let (found, tested) = extend_cores(&ctx, &level, m, j, tm, t, &astar, nthreads);
        println!("  cores of size {}: {}; full sets M tested: {}; orbits with Abar + 2 tau <= {} found: {}  [case {:.1}s]", mz, level.len(), tested, t, found.len(), tj.elapsed().as_secs_f64());
        all.extend(found);
    }
    all.sort_unstable();
    all.dedup();
    println!("search wall time {:.1}s", t0.elapsed().as_secs_f64());
    let mut hist: BTreeMap<(u32, u32), usize> = BTreeMap::new();
    for &(_, ab, _, tau) in &all {
        *hist.entry((ab, tau)).or_default() += 1;
    }
    println!("SURVIVORS (orbits with Abar + 2 tau <= {}): {}", t, all.len());
    for ((ab, tau), n) in &hist {
        println!("   Abar {:3}  tau {}  : {} orbits", ab, tau, n);
    }
    if !dump.is_empty() {
        let mut f = std::io::BufWriter::new(std::fs::File::create(&dump).unwrap());
        let mut ms = [0u16; 16];
        for &(x, ab, tc, tau) in &all {
            unpack(x, m, &mut ms);
            let names: Vec<String> = ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect();
            writeln!(f, "{} {} {} {}", names.join(","), ab, tc, tau).unwrap();
        }
        println!("dumped {} orbits to {}", all.len(), dump);
    }
}

fn pttable_check(args: &[String]) {
    let n: usize = args[2].parse().unwrap();
    let ctx = build_ctx(7, Family::Arbitrary);
    let tl = Instant::now();
    let tab = PtTable::build(&ctx, 4);
    let ones: u64 = tab.bits.iter().map(|w| w.count_ones() as u64).sum();
    println!("PT table built in {:.1}s; {} of {} ordered triples (b,c,d) give PT(0,b,c,d)", tl.elapsed().as_secs_f64(), ones, 720u64 * 720 * 720);
    let nv = ctx.co.nv;
    let mut rng = Rng(0xdeadbeef);
    let mut bad = 0;
    let mut npt = 0;
    for i in 0..n {
        let q = random_quad(&mut rng, &ctx, i % 2 == 0);
        let (fa, fo) = ctx.pt.quad_masks(&q, &ctx.fa, &ctx.fo, nv);
        let direct = ctx.pt.is_pt(&fa, &fo);
        let looked = tab.pt(&ctx.sym.act, q[0], q[1], q[2], q[3]);
        if direct != looked {
            bad += 1;
        }
        if !direct {
            npt += 1;
        }
    }
    println!("random 4-multisets: {} checked, {} non-PT, {} disagreements between table and direct test", n, npt, bad);
}

/// tau-pruned cascade, cuts applied per candidate using the PT table.
/// Finds every orbit with Abar + 2 tau <= T and tau <= taumax.
fn enumtau2(args: &[String]) {
    let m: usize = args[2].parse().unwrap();
    let t: u32 = args[3].parse().unwrap();
    let nthreads: usize = arg_val(args, "--threads", 4);
    let dump: String = arg_val(args, "--dump", String::new());
    let relabel: u64 = arg_val(args, "--relabel", 0);
    let taumax: u32 = arg_val(args, "--taumax", 3);
    let abmax: u32 = arg_val(args, "--abmax", u32::MAX);
    let astar_arg: String = arg_val(args, "--astar", String::new());
    let ctx = build_ctx_r(7, Family::Arbitrary, relabel);
    let exact: Vec<u32> = astar_arg.split(',').map(|x| x.parse().unwrap()).collect();
    let astar = extend_astar(&exact, m);
    let mut kill = 0u32;
    while t >= 2 * kill && t - 2 * kill >= astar[m] {
        kill += 1;
    }
    let tau_stop = kill.min(taumax + 1);
    assert!(tau_stop <= 4);
    println!("tau-pruned cascade (per-candidate cuts, PT lookup table): (m,n) = ({},7)", m);
    println!("survivors = orbits with Abar + 2 tau <= {} and tau <= {} (tau >= {} cut; A*({}) >= {} alone would cut tau >= {})", t, tau_stop - 1, tau_stop, m, astar[m], kill);
    if relabel != 0 {
        println!("canonical form: lex-min under vertex relabelling seed {} (vertex 0 = {})", relabel, ctx.co.name(0));
    }
    println!("A*(r) lower bounds, r = 0..{}: {:?}", m, astar);
    if abmax != u32::MAX {
        println!("additional cap: Abar <= {}", abmax);
    }
    for tau in 0..tau_stop {
        println!("thresholds for tau = {}: {:?}", tau, &thresholds(m, (t - 2 * tau).min(abmax))[1..]);
    }
    let tl = Instant::now();
    let tab = PtTable::build(&ctx, nthreads);
    println!("PT table built in {:.1}s", tl.elapsed().as_secs_f64());
    let t0 = Instant::now();
    let mut level: Vec<u128> = vec![pack(&[0])];
    for k in 2..=m {
        let tl = Instant::now();
        let (next, st) = extend_level_tau_cap(&ctx, &tab, &level, k - 1, m, t, abmax, tau_stop, &astar, nthreads);
        println!(
            "level {:2}: parents {:>11}  cand(Abar<=T_k) {:>13}  max-contrib {:>13}  lookahead-cut {:>12}  tau/threshold-cut {:>12}  kept cand by tau {:?}  orbits {:>11}  [{:.1}s]",
            k, st.parents, st.candidates, st.after_maxcontrib, st.lookahead_cut, st.tau_cut, &st.tau_hist[..tau_stop as usize], st.orbits, tl.elapsed().as_secs_f64()
        );
        std::io::stdout().flush().ok();
        level = next;
    }
    println!("search wall time {:.1}s", t0.elapsed().as_secs_f64());
    // re-verify survivors with the direct PT test (not the table)
    let info = analyze(&ctx, &level, m, 64, nthreads);
    let mut hist: BTreeMap<(u32, u32), usize> = BTreeMap::new();
    let mut viol = 0;
    for o in &info {
        *hist.entry((o.abar, o.tau)).or_default() += 1;
        if o.abar + 2 * o.tau > t || o.tau > taumax || o.abar > abmax {
            viol += 1;
        }
    }
    println!("SURVIVORS (orbits with Abar + 2 tau <= {}, tau <= {}): {}   (re-verified with direct PT test; inconsistent: {})", t, tau_stop - 1, level.len(), viol);
    for ((ab, tau), n) in &hist {
        println!("   Abar {:3}  tau {}  : {} orbits", ab, tau, n);
    }
    if !dump.is_empty() {
        let mut f = std::io::BufWriter::new(std::fs::File::create(&dump).unwrap());
        let mut ms = [0u16; 16];
        for (i, &x) in level.iter().enumerate() {
            unpack(x, m, &mut ms);
            let names: Vec<String> = ms[..m].iter().map(|&v| ctx.co.name(v as usize)).collect();
            writeln!(f, "{} {} {} {}", names.join(","), info[i].abar, info[i].t, info[i].tau).unwrap();
        }
        println!("dumped {} orbits to {}", level.len(), dump);
    }
}

/// Exhaustive: for every g = (sigma, r) in G and every (a, b) in V^2,
/// FA(g a, g b) = sigma(FA(a, b)) and FO(g a, g b) = sigma(FO(a, b)), where
/// sigma acts on the 21 ground pairs.  (rev does not change labels.)  Since
/// pseudo-tightness is a function of these masks that is invariant under
/// renaming the ground set consistently, this makes PT exactly G-invariant,
/// which is what the PT lookup table relies on.
fn equivariance() {
    let ctx = build_ctx(7, Family::Arbitrary);
    let co = &ctx.co;
    let nv = co.nv;
    let t0 = Instant::now();
    let mut sigmas: Vec<Vec<u8>> = Vec::new();
    let mut sg: Vec<u8> = (0..7).collect();
    loop {
        sigmas.push(sg.clone());
        if !co::next_permutation(&mut sg) {
            break;
        }
    }
    let next = std::sync::atomic::AtomicUsize::new(0);
    let bad = std::sync::atomic::AtomicU64::new(0);
    std::thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| loop {
                let si = next.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                if si >= sigmas.len() {
                    break;
                }
                let sigma = &sigmas[si];
                let pmap: Vec<u32> = co.pairs.iter().map(|&(x, y)| co.pair_idx[sigma[x as usize] as usize][sigma[y as usize] as usize] as u32).collect();
                let mut lo = vec![0u32; 2048];
                let mut hi = vec![0u32; 1024];
                for m in 0..2048u32 {
                    for p in 0..11 {
                        if (m >> p) & 1 == 1 {
                            lo[m as usize] |= 1 << pmap[p];
                        }
                    }
                }
                for m in 0..1024u32 {
                    for p in 0..10 {
                        if (m >> p) & 1 == 1 {
                            hi[m as usize] |= 1 << pmap[11 + p];
                        }
                    }
                }
                let map = |m: u32| lo[(m & 2047) as usize] | hi[(m >> 11) as usize];
                let mut nb = 0u64;
                for r in 0..2 {
                    let g = si * 2 + r;
                    // the Sym table orders group elements as sigma-index*2 + r
                    let row = &ctx.sym.act[g * nv..(g + 1) * nv];
                    for a in 0..nv {
                        let ga = row[a] as usize;
                        for b in 0..nv {
                            let gb = row[b] as usize;
                            if ctx.fa[ga * nv + gb] != map(ctx.fa[a * nv + b]) || ctx.fo[ga * nv + gb] != map(ctx.fo[a * nv + b]) {
                                nb += 1;
                            }
                        }
                    }
                }
                bad.fetch_add(nb, std::sync::atomic::Ordering::Relaxed);
            });
        }
    });
    let nb = bad.load(std::sync::atomic::Ordering::Relaxed);
    println!(
        "[{}] FA/FO equivariance under all {} group elements x {} ordered pairs: {} violations  [{:.1}s]",
        if nb == 0 { "PASS" } else { "FAIL" },
        sigmas.len() * 2,
        nv * nv,
        nb,
        t0.elapsed().as_secs_f64()
    );
}
