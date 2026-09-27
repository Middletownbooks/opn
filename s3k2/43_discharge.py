#!/usr/bin/env python3
"""
Discharge every conditional item of script 41 with the AUDITOR's solver.

Script 41 marks three kinds of item as conditional on a complete solution list:
  ('SmT', T, W, adm)     a count kill that used Sm_Y(T), the search to 10^24;
  ('caseB', K, W, E)     candidates t with (t^2+t+1)/3 K-smooth, searched to 10^E;
  ('SmK-coupled', K, W, n)  the coupled-pair count, which used Sm_Y(K).
Each becomes unconditional once the COMPLETE solution set of
x^2 + x + 1 = 3^delta * (T-smooth) is known and adds nothing to the searched list.

The complete lists come from audit_s3k2/a4_solver.py: an exact rational LLL
followed by Fincke-Pohst enumeration, written by the independent auditor without
reading s3k2/39.  So this discharge does not use the repo's own Matveev + LLL code.

Input: the stdout of `python3 41_rebuild_dfs.py <profiles>` (a file), whose
'conditional items' lines are Python tuples.
Run:   python3 43_discharge.py <41-output-file> [...]
"""
import sys, os, ast, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "audit_s3k2"))
import a4_solver
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "41_rebuild_dfs.py"))
rb = importlib.util.module_from_spec(spec); _a = sys.argv; sys.argv = ['x']; spec.loader.exec_module(rb); sys.argv = _a

items = set()
for fn in sys.argv[1:]:
    for line in open(fn):
        s = line.strip()
        if s.startswith("('SmT'") or s.startswith("('caseB'") or s.startswith("('SmK-coupled'"):
            items.add(ast.literal_eval(s))
print(f"{len(items)} distinct conditional items from {len(sys.argv)-1} file(s)")

_cache = {}
def complete(K, allow3):
    key = (tuple(sorted(K)), allow3)
    if key not in _cache: _cache[key] = a4_solver.solve(list(K), allow3=allow3, verbose=False)
    return _cache[key]

ok_all = True
for it in sorted(items):
    kind, K = it[0], it[1]
    if kind in ('SmT', 'SmK-coupled'):
        xs = complete(K, False)
        # allow3=False: every x returned has x^2+x+1 exactly K-smooth
        smc = sorted(x for x in xs if x >= 5 and x % 3 == 2 and rb.isprime(x))
        smy = rb.Sm_Y(K)
        ok = smc == smy
        print(f"   {kind:12s} K={list(K)} W={it[2]}: complete Sm = {smc}; searched Sm_Y = {smy} -> {'OK' if ok else 'DIFFERS'}")
    else:
        xs = complete(K, True)
        ts = sorted(x for x in xs if x % 3 == 1 and x > 1 and rb.isprime(x)
                    and (x*x + x + 1) % 3 == 0)
        searched = rb.caseB(tuple(sorted(K)), it[3])
        extra = [t for t in ts if t not in searched]
        ok = not extra
        print(f"   {kind:12s} K={list(K)} W={it[2]}: complete t-list = {ts}; searched = {searched} -> {'OK' if ok else 'EXTRA ' + str(extra)}")
    ok_all &= ok
print("ALL DISCHARGED" if ok_all else "NOT ALL DISCHARGED")
