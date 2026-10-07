#!/usr/bin/env python3
"""Compare two survivor dumps (lines: 'v1,v2,...,vm Abar t tau').

The orbit is identified by a canonical form computed HERE, independently of
the Rust canonical form: the lexicographically smallest sorted tuple of
cyclic-order strings over all 10080 images under S_7 x <rev>.  So dumps made
with different vertex relabellings (different Rust canonical forms) can be
compared.  Optional filter: keep only lines with Abar <= MAXAB and
Abar + 2*tau <= MAXF.
usage: compare_dumps.py A B [MAXAB MAXF] [--orbit]
"""
import itertools
import sys


def canon_rot(seq):
    i = seq.index(0)
    return seq[i:] + seq[:i]


def act(sigma, r, v):
    q = tuple(sigma[x] for x in v)
    if r:
        q = (q[0],) + tuple(reversed(q[1:]))
    return canon_rot(q)


GROUP = [(s, r) for s in itertools.permutations(range(7)) for r in (0, 1)]


def orbit_key(names):
    ms = [tuple(int(c) for c in s) for s in names]
    best = None
    for s, r in GROUP:
        img = tuple(sorted(act(s, r, v) for v in ms))
        if best is None or img < best:
            best = img
    return best


def load(path, maxab, maxf, mode):
    out = {}
    for line in open(path):
        f = line.split()
        names, ab, t, tau = f[0].split(","), int(f[1]), int(f[2]), int(f[3])
        if ab > maxab or ab + 2 * tau > maxf:
            continue
        key = orbit_key(names) if mode == "orbit" else tuple(names)
        out[key] = (ab, t, tau)
    return out


args = [a for a in sys.argv[1:] if not a.startswith("--")]
mode = "orbit" if "--orbit" in sys.argv else "text"
maxab = int(args[2]) if len(args) > 2 else 10**9
maxf = int(args[3]) if len(args) > 3 else 10**9
A = load(args[0], maxab, maxf, mode)
B = load(args[1], maxab, maxf, mode)
print("mode:", mode, "(text = both dumps must use the same canonical form; orbit = recanonicalised in Python)")
print(f"{sys.argv[1]}: {len(A)} orbits; {sys.argv[2]}: {len(B)} orbits")
print("only in A:", len(set(A) - set(B)), " only in B:", len(set(B) - set(A)))
diff = [k for k in set(A) & set(B) if A[k][:2] != B[k][:2]]
print("common orbits with different (Abar, t):", len(diff))
