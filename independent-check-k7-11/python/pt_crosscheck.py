#!/usr/bin/env python3
"""Independent, deliberately naive re-implementation of the pseudo-tightness
test, written from the definitions only, sharing no code with the Rust
implementation.  Differences in method on purpose:
  * cyclic orders are tuples, labels are frozensets {x,y};
  * shortest-antipath label sets are enumerated EXPLICITLY (as Python sets of
    frozensets), never summarised as AND/OR bitmasks by a DP;
  * CO_4 route label sets come from a BFS over (vertex, frozenset) states;
  * the existence of N : {0..n-1} -> V(CO_4) is decided by brute force over
    ALL 6^n assignments (numpy), with no backtracking or forward checking;
  * the transversal number is found by iterative deepening.

Usage:
  pt_crosscheck.py selftest
  pt_crosscheck.py quads FILE      (FILE lines: 4 cyclic orders + Rust verdict)
"""
import itertools
import sys
from collections import deque

import numpy as np


def canon(seq):
    i = seq.index(0)
    return tuple(seq[i:] + seq[:i])


class CO:
    def __init__(self, n):
        self.n = n
        self.verts = [canon((0,) + p) for p in itertools.permutations(range(1, n))]
        self.vset = set(self.verts)
        self.nbrs = {}
        for v in self.verts:
            out = []
            for i in range(n):
                j = (i + 1) % n
                w = list(v)
                w[i], w[j] = w[j], w[i]
                out.append((canon(tuple(w)), frozenset((v[i], v[j]))))
            self.nbrs[v] = out
        self._dist = {}

    def rev(self, v):
        return canon((v[0],) + tuple(reversed(v[1:])))

    def dist_from(self, s):
        if s not in self._dist:
            d = {s: 0}
            q = deque([s])
            while q:
                u = q.popleft()
                for w, _ in self.nbrs[u]:
                    if w not in d:
                        d[w] = d[u] + 1
                        q.append(w)
            self._dist[s] = d
        return self._dist[s]

    def geodesic_label_sets(self, s, t):
        """Set of frozensets: label sets of all shortest s-t paths."""
        dt = self.dist_from(t)
        memo = {}

        def rec(v):
            if v == t:
                return {frozenset()}
            if v in memo:
                return memo[v]
            res = set()
            for w, lab in self.nbrs[v]:
                if dt[w] == dt[v] - 1:
                    for L in rec(w):
                        res.add(L | {lab})
            memo[v] = res
            return res

        return rec(s)


def co4_route_sets(co4, family):
    """dict (u, w) -> set of frozensets of labels of u->w routes."""
    res = {}
    for u in co4.verts:
        if family in ("arbitrary", "walk"):
            seen = {(u, frozenset())}
            q = deque(seen)
            while q:
                v, L = q.popleft()
                res.setdefault((u, v), set()).add(L)
                for w, lab in co4.nbrs[v]:
                    if family == "walk" and lab in L:
                        continue
                    st = (w, L | {lab})
                    if st not in seen:
                        seen.add(st)
                        q.append(st)
        else:
            def dfs(v, visited, L):
                res.setdefault((u, v), set()).add(L)
                for w, lab in co4.nbrs[v]:
                    if w in visited:
                        continue
                    if family == "both" and lab in L:
                        continue
                    dfs(w, visited | {w}, L | {lab})
            dfs(u, {u}, frozenset())
    return res


class PT:
    def __init__(self, src, family="arbitrary"):
        self.src = src
        self.co4 = CO(4)
        self.routes = co4_route_sets(self.co4, family)
        self.v4 = self.co4.verts
        n = src.n
        self.assign = np.array(list(itertools.product(range(6), repeat=n)), dtype=np.int8)

    def is_pt(self, quad):
        src = self.src
        n = src.n
        # explicit label sets of all shortest antipaths, per pair of the 4-set
        # M'-pair {i,j} is identified with the CO_4 label frozenset({i,j})
        pairsets = {}
        for i, j in itertools.combinations(range(4), 2):
            pairsets[frozenset((i, j))] = src.geodesic_label_sets(quad[i], src.rev(quad[j]))
        ok = np.ones(len(self.assign), dtype=bool)
        for x, y in itertools.combinations(range(n), 2):
            g = frozenset((x, y))
            forced = frozenset(p for p, sets in pairsets.items() if all(g in L for L in sets))
            poss = frozenset(p for p, sets in pairsets.items() if any(g in L for L in sets))
            C = np.zeros((6, 6), dtype=bool)
            for iu, u in enumerate(self.v4):
                for iv, v in enumerate(self.v4):
                    for L in self.routes.get((u, self.co4.rev(v)), ()):
                        if forced <= L <= poss:
                            C[iu, iv] = True
                            break
            ok &= C[self.assign[:, x], self.assign[:, y]]
            if not ok.any():
                return False
        return bool(ok.any())


def parse(s):
    return canon(tuple(int(c) for c in s))


def antisum(co, ms):
    return sum(co.dist_from(a)[co.rev(b)] for a, b in itertools.combinations(ms, 2))


def transversal_number(edges):
    def hit(es, k):
        if not es:
            return True
        if k == 0:
            return False
        e = min(es, key=len)
        for p in e:
            if hit([f for f in es if p not in f], k - 1):
                return True
        return False
    k = 0
    while not hit(edges, k):
        k += 1
    return k


def analyse(pt, ms):
    co = pt.src
    edges = []
    for q in itertools.combinations(range(len(ms)), 4):
        if not pt.is_pt([ms[i] for i in q]):
            edges.append(frozenset(frozenset(p) for p in itertools.combinations(q, 2)))
    return edges


def selftest():
    co6 = CO(6)
    co4 = CO(4)
    sizes = {}
    for fam in ("both", "walk", "path", "arbitrary"):
        r = co4_route_sets(co4, fam)
        sizes[fam] = sum(len(s) for s in r.values())
    print("CO_4 family sizes:", sizes)
    ex = [parse(s) for s in ("012345", "013542", "032541", "045231")]
    order = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    print("(4,6) antidistances:", [co6.dist_from(ex[i])[co6.rev(ex[j])] for i, j in order])
    print("(4,6) #label sets:", [len(co6.geodesic_label_sets(ex[i], co6.rev(ex[j]))) for i, j in order])
    for fam in ("both", "walk", "path", "arbitrary"):
        print("(4,6) pseudo-tight under", fam, ":", PT(co6, fam).is_pt(ex))
    co7 = CO(7)
    pt = PT(co7, "arbitrary")
    rep = [parse(s) for s in "0123456 0123456 0125463 0152436 0163452 0452136 0543621 0625431 0634125 0635421 0643521".split()]
    print("219 representative: antisum", antisum(co7, rep))
    edges = analyse(pt, rep)
    print("219 representative: t =", len(edges), " tau =", transversal_number(edges))
    a = parse("0123456")
    z = [a] * 5 + [co7.rev(a)] * 6
    ez = analyse(pt, z)
    print("Zarankiewicz 5a+6rev(a), a=0123456: antisum", antisum(co7, z), " t =", len(ez))


def quads(path):
    co7 = CO(7)
    pt = PT(co7, "arbitrary")
    agree = disagree = nonpt = 0
    for line in open(path):
        f = line.split()
        if len(f) < 5:
            continue
        q = [parse(s) for s in f[:4]]
        mine = pt.is_pt(q)
        theirs = f[4] == "1"
        if not mine:
            nonpt += 1
        if mine == theirs:
            agree += 1
        else:
            disagree += 1
            print("DISAGREE:", line.strip(), "python says", int(mine))
    print(f"quads: agree {agree}, disagree {disagree}, non-PT (python) {nonpt}")


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        selftest()
    elif sys.argv[1] == "quads":
        quads(sys.argv[2])
