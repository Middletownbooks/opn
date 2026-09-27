#!/usr/bin/env python3
"""
Build s3k2/axioms_complete_lists.json: the ONLY external facts the certificate
checker (s3k2/46) takes on trust.

Each entry is a complete solution list:
    allow3 = false :  { x >= 0 : x^2+x+1 is T-smooth }
    allow3 = true  :  { x >= 0 : x^2+x+1 = M or 3M, M T-smooth }
Each list is computed by TWO independent complete solvers, and the file is
written only if they agree exactly:
  * s3k2/39_baker_lll.py (Matveev 1998 Thm 2.2, then LLL with a shortest-vector
    lower bound);
  * audit_s3k2/a4_solver.py (the independent auditor's: exact LLL, then
    Fincke-Pohst enumeration).
The sets T are those the certificates of s3k2/41 use: the count kills, Case B,
and the coupled-pair count.
"""
import os, sys, json, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "audit_s3k2"))
import a4_solver
spec = importlib.util.spec_from_file_location("bl", os.path.join(here, "39_baker_lll.py"))
bl = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(bl); sys.argv = _a

NEED = [   # (T, allow3)
    ((7, 13), False), ((7, 13, 19), False), ((7, 13, 19, 127), False),
    ((7, 13, 19, 31, 127), False), ((7, 13, 19, 31, 331), False), ((7, 13, 19, 37, 67), False),
    ((7, 13, 19, 37, 127), False), ((7, 13, 19, 43, 127), False), ((7, 13, 19, 127, 409), False),
    ((7, 13, 19, 127, 1723), False),
    ((7, 13), True), ((7, 13, 19), True),
]

def by39(T, allow3):
    # decimal precision is process-global and a4_solver lowers it for its own
    # rounds; script 39 needs its 600 digits back before computing theta_t.
    from decimal import getcontext
    getcontext().prec = 600
    xs = set(x for x in bl.solve_complete(T, 0, log=lambda *a: None)[0] if x >= 0)
    if allow3: xs |= set(x for x in bl.solve_complete(T, 1, log=lambda *a: None)[0] if x >= 0)
    return sorted(xs)

out = []
for T, a3 in NEED:
    s39 = by39(T, a3)
    sa4 = sorted(a4_solver.solve(list(T), allow3=a3, verbose=False))
    agree = s39 == sa4
    print(f"T = {list(T)}, allow3 = {a3}: script 39 {s39}\n{'':28s}a4_solver {sa4}   {'AGREE' if agree else 'DISAGREE'}")
    if not agree: sys.exit("solvers disagree; axioms file NOT written")
    out.append({"T": list(T), "allow3": a3, "complete": s39,
                "solvers": ["s3k2/39_baker_lll.py", "audit_s3k2/a4_solver.py"]})
with open(os.path.join(here, "axioms_complete_lists.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print(f"wrote {len(out)} axioms to s3k2/axioms_complete_lists.json")
