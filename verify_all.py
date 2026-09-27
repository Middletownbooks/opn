#!/usr/bin/env python3
"""
Re-derive every figure that NOTES_S3_K2.md section 14 and README.md quote for
section 3 at k = 2, and fail loudly on any mismatch.

    python3 verify_all.py          fast tier, about 10 minutes
    python3 verify_all.py full     adds scripts 34, 35 and profile 2,yes,1,4,1
                                   (about an hour; run it under nohup)

Each check runs a script in s3k2/ and compares its output with the value
written below.  These values are copied from the notes tables, so a drift in
either the code or the notes shows up here.  Exit status is 0 only if every
check passes.

LIMITATION (independent audit, finding X1).  This detects DRIFT, not
UNSOUNDNESS.  A change that over-prunes (for example, the one-prime cutoff
where k primes remain) can only remove sets, so it can never produce ALIVE.
Such a change is caught only if it moves a recorded count, and those counts
came from the same code.  Soundness rests on the proofs in
audit_s3k2/AUDIT_S3K2_RESULT.md, appendix Pf.2-Pf.5, not on this runner.

COVERAGE (audit recommendation D2).  After the runs, every exception that
script 36 prints must appear among the exceptions that script 38 resolves,
for the same profile.  An exception raised inside the closure-driven last level
(tagged 't:<role>') is never a DFS input, so its presence fails the check.
"""
import subprocess, sys, re, time, os

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = os.path.join(HERE, "s3k2")
FULL = len(sys.argv) > 1 and sys.argv[1] == "full"
results = []
outputs = {}

def run(args, timeout):
    t0 = time.time()
    p = subprocess.run([sys.executable] + args, cwd=S3, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr, time.time() - t0

def check(name, args, timeout, tests):
    """tests: list of (description, predicate on output)."""
    try:
        rc, out, dt = run(args, timeout)
    except subprocess.TimeoutExpired:
        results.append((name, False, f"TIMEOUT after {timeout}s")); print(f"FAIL  {name}: timeout", flush=True); return
    outputs[name] = out
    bad = [] if rc == 0 else [f"exit code {rc}"]
    for desc, pred in tests:
        try:
            ok = pred(out)
        except Exception as e:
            ok = False; desc += f" ({e})"
        if not ok: bad.append(desc)
    results.append((name, not bad, "; ".join(bad) if bad else f"{dt:.0f}s"))
    print(f"{'PASS' if not bad else 'FAIL'}  {name}  ({dt:.0f}s)" + ("" if not bad else "\n      " + "\n      ".join(bad)), flush=True)
    if bad:
        print("      --- last lines of output ---\n      " + "\n      ".join(out.strip().splitlines()[-12:]), flush=True)

has = lambda s: (lambda out: s in out)

def profile_tally(expect):
    """expect = (rawdead, uncond, cond, nocfg, alive, exceptions, caseB)"""
    def pred(out):
        rd = int(re.search(r"killed early \(raw role minimum > 18/13\): (\d+)", out).group(1))
        m = re.search(r"final sets: uncond dead (\d+), conditional dead (\d+), no role/config (\d+), ALIVE (\d+)", out)
        ex = int(re.search(r"exceptions \(no cutoff\): (\d+)", out).group(1))
        cb = int(re.search(r"case-B enumerations \(conditional on 10\^MB_EXP bound\): (\d+)", out).group(1))
        got = (rd, int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), ex, cb)
        if got != expect: raise ValueError(f"got {got}, expected {expect}")
        return True
    return pred

def dfs_clean(out):
    if "ALIVE 0" not in out and "ALIVE" in out: raise ValueError("an ALIVE count is nonzero")
    for line in out.splitlines():
        m = re.search(r"ALIVE (\d+)\s+unresolved (\d+)", line)
        if m and (m.group(1) != "0" or m.group(2) != "0"): raise ValueError(line.strip())
    return True

# ------------------------------------------------------------------ fast tier
print("=== fast tier ===", flush=True)
check("31 coupled branch (Vieta jumping)", ["31_coupled_vieta.py"], 600,
      [("coupled branch empty", has("Coupled branch of section 13b: EMPTY"))])
check("32 Skolem solver", ["32_skolem.py"], 900,
      [("reproduces script 26", has("reproduction: EXACT")),
       ("cross-check vs direct search", has("all eight agree")),
       ("mutation test refused", has("all refused -> sound"))])
check("33 six profiles exact", ["33_six_profiles_exact.py"], 900,
      [("all six eliminated", has("All six pool-free profiles of section 13c are eliminated"))])
check("36 validate (reproduces 34's levels)", ["36_profile_recursion.py", "validate"], 900,
      [("reproduced", has("reproduced exactly."))])
PROFILES = {   # (rawdead, uncond, cond, nocfg, alive, exceptions, caseB)   NOTES_S3_K2.md 14e
    "0,no,2,2,1":  (6, 551, 0, 17, 0, 0, 0),
    "0,yes,2,3,0": (0, 80, 0, 17, 0, 0, 0),
    "1,yes,2,4,0": (0, 618, 0, 9, 0, 0, 0),
    "1,no,2,3,1":  (17, 4249, 0, 16, 0, 0, 0),
    "0,yes,1,2,1": (2, 260, 1, 341, 0, 0, 0),
    "1,yes,1,3,1": (16, 4349, 3, 52, 0, 0, 1),
}
for p, e in PROFILES.items():
    check(f"36 profile {p}", ["36_profile_recursion.py", p], 900, [("tally", profile_tally(e))])
check("38 DFS on 1,yes,1,3,1 exceptions", ["38_closure_dfs.py", "1,yes,1,3,1"], 900,
      [("nothing alive or unresolved", dfs_clean)])
check("38 DFS on 2,yes,1,4,1 level-2 exceptions", ["38_closure_dfs.py", "2,yes,1,4,1", "2"], 1800,
      [("nothing alive or unresolved", dfs_clean)])
check("38 DFS on the alpha=2 exceptions (section 14f)", ["38_closure_dfs.py", "2,yes,2,5,0"], 1800,
      [("nothing alive or unresolved", dfs_clean),
       ("the two extra sets appear", lambda o: "127: 'n'" in o and "331: 'n'" in o)])
check("39 Baker+LLL validation", ["39_baker_lll.py", "validate"], 1800,
      [("validation passed", has("VALIDATION PASSED"))])
SM = [   # NOTES_S3_K2.md 14h: complete Sm(T), in the order script 39 prints them
    [11, 29, 653], [11, 107, 653], [11, 107, 653], [11, 53, 107, 653], [11, 41, 107, 653],
    [5, 11, 107, 191, 653], [5, 11, 191, 653],
    [], [], [], [11, 653], [], [11, 107, 653]]
CB = [[], [13], [13], [13], [7]]
def residual_ok(out):
    sm = [eval(m) for m in re.findall(r"Sm\(T\) complete = (\[[^\]]*\])", out)]
    cb = [eval(m) for m in re.findall(r"solutions t = (\[[^\]]*\])", out)]
    if sm != SM: raise ValueError(f"Sm lists {sm}")
    if cb != CB: raise ValueError(f"case-B lists {cb}")
    return True
check("39 residual statements", ["39_baker_lll.py", "residual"], 3600,
      [("complete lists as in 14h", residual_ok)])
check("40 coupled branch by count", ["40_coupled_count.py"], 900,
      [("dead", has("Coupled branch DEAD"))])
# ---- Theorem A (k = 2, 3 does not divide N): certified rebuild (NOTES_K2.md 7) ----
K2 = os.path.join(HERE, "k2")
for prof in ["s", "sn", "snn"]:
    t0 = time.time()
    gen = subprocess.Popen([sys.executable, "05_theoremA_dfs.py", "--cert", prof], cwd=K2,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    chk = subprocess.run([sys.executable, "06_check_theoremA.py"], cwd=K2, stdin=gen.stdout,
                         capture_output=True, text=True, timeout=3600)
    gen.stdout.close(); gen.wait()
    ok = chk.returncode == 0 and "CERTIFICATE VALID" in chk.stdout and "cited theorems used: none" in chk.stdout
    results.append((f"Theorem A certificate {prof}", ok, "" if ok else chk.stdout[-300:]))
    print(f"{'PASS' if ok else 'FAIL'}  Theorem A certificate {prof}, no cited theorem  ({time.time()-t0:.0f}s)", flush=True)
p7 = subprocess.run([sys.executable, "07_theoremA_pool.py", "400"], cwd=K2, capture_output=True, text=True, timeout=3600)
ok = p7.returncode == 0 and p7.stdout.strip().endswith("PASS")
results.append(("Theorem A brute-force cross-check", ok, "" if ok else p7.stdout[-300:]))
print(f"{'PASS' if ok else 'FAIL'}  Theorem A brute-force cross-check (pool < 400)", flush=True)

# ------------------------------------------------------------------ full tier
if FULL:
    print("=== full tier ===", flush=True)
    check("34 corrected recursion", ["34_recursion_k_correct.py", "4"], 3600,
          [("level counts", lambda o: all(s in o for s in ["level 2: 59 sets", "level 3: 1372 sets",
                                                             "level 4: 31925 sets", "level 5: 488860 sets"])),
           ("three exceptions", has("exceptions: [([7, 13, 19, 31], 0.997627), ([7, 13, 31, 79], 0.996122), ([7, 13, 31, 307], 0.994024)]"))])
    check("35 level-5 pass", ["35_level5_k_correct.py"], 7200,
          [("closure kills", lambda o: re.search(r"no role assignment passes closure\s*:\s*485179", o) is not None),
           ("narrowing kills", lambda o: re.search(r"interval narrowing \(unconditional\)\s*:\s*3676", o) is not None),
           ("five conditional", lambda o: re.search(r"CONDITIONAL\)\s*:\s*5\b", o) is not None),
           ("none alive", lambda o: re.search(r"STILL ALIVE\s*:\s*0\b", o) is not None)])
    check("36 profile 2,yes,1,4,1", ["36_profile_recursion.py", "2,yes,1,4,1"], 7200,
          [("tally", profile_tally((22, 357, 4, 310, 0, 1, 4)))])
    # ---- the independent rebuild (NOTES_S3_K2.md 14l) ----
    REBUILD = {   # profile -> set of conditional items script 41 must report
        "0,no,2,2,1": set(), "0,yes,2,3,0": set(), "1,yes,2,4,0": set(), "1,no,2,3,1": set(),
        "0,yes,1,2,1": {('SmT', (7, 13), 'n=11', ())},
        "1,yes,1,3,1": {('SmT', (7, 13, 19), 'n=23', (653,)), ('caseB', (7, 13), 'n=11', 300)},
        "2,yes,1,4,1": {('SmK-coupled', (7, 13), 'n=11', 0), ('SmT', (7, 13, 19, 127), 'n=29', (653,)),
                        ('SmT', (7, 13, 19, 127), 'n=41', (653, 107)), ('SmT', (7, 13, 19, 127), 'n=47', (653, 107)),
                        ('caseB', (7, 13), 'n=11', 300), ('caseB', (7, 13, 19), 'n=23', 120)},
        "2,yes,2,5,0": {('SmT', (7, 13, 19, 31, 127), 'W empty', (653, 191)), ('SmT', (7, 13, 19, 31, 331), 'W empty', (653, 191)),
                        ('SmT', (7, 13, 19, 37, 67), 'W empty', (653,)), ('SmT', (7, 13, 19, 37, 127), 'W empty', (653, 107)),
                        ('SmT', (7, 13, 19, 43, 127), 'W empty', (653, 107)), ('SmT', (7, 13, 19, 127, 409), 'W empty', (653, 107, 53)),
                        ('SmT', (7, 13, 19, 127, 1723), 'W empty', (653, 107, 41))},
    }
    def rebuild_ok(out):
        import ast
        blocks = re.split(r"^PROFILE ", out, flags=re.M)[1:]
        seen = {}
        for b in blocks:
            name = b.split(":")[0]
            items = {ast.literal_eval(l.strip()) for l in b.splitlines() if l.strip().startswith("('")}
            if not re.search(r"UNRESOLVED: 0\b", b): raise ValueError(f"{name}: unresolved states")
            if not re.search(r"ALIVE: 0\b", b): raise ValueError(f"{name}: ALIVE")
            seen[name] = items
        for name, exp in REBUILD.items():
            if seen.get(name) != exp: raise ValueError(f"{name}: items {seen.get(name)} expected {exp}")
        return True
    check("41 rebuild, all eight profiles", ["41_rebuild_dfs.py", "all"], 7200,
          [("nothing alive or unresolved; conditional items as recorded", rebuild_ok)])
    import tempfile
    tf = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False)
    tf.write(outputs.get("41 rebuild, all eight profiles", "")); tf.close()
    check("43 discharge by the auditor's solver", ["43_discharge.py", tf.name], 3600,
          [("all discharged", has("ALL DISCHARGED"))])
    # ---- certificates (NOTES_S3_K2.md 14m): search -> independent checker ----
    for prof in ["0,no,2,2,1", "0,yes,1,2,1", "0,yes,2,3,0", "1,no,2,3,1",
                 "1,yes,1,3,1", "1,yes,2,4,0", "2,yes,1,4,1", "2,yes,2,5,0"]:
        t0 = time.time()
        gen = subprocess.Popen([sys.executable, "41_rebuild_dfs.py", "--cert", prof], cwd=S3,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        chk = subprocess.run([sys.executable, "46_check_certificate.py"], cwd=S3, stdin=gen.stdout,
                             capture_output=True, text=True, timeout=7200)
        gen.stdout.close(); gen.wait()
        ok = chk.returncode == 0 and "CERTIFICATE VALID" in chk.stdout
        name = f"certificate {prof} checked by s3k2/46"
        outputs[name] = chk.stdout
        results.append((name, ok, "" if ok else chk.stdout.strip()[-300:]))
        print(f"{'PASS' if ok else 'FAIL'}  {name}  ({time.time()-t0:.0f}s)" + ("" if ok else "\n      " + chk.stdout.strip()[-300:]), flush=True)
    for prof, pool in (("2,yes,1,4,1", "140"), ("2,yes,2,5,0", "140")):
        check(f"42 pool cross-check {prof} (pool < {pool})", ["42_pool_crosscheck.py", prof, pool], 3600,
              [("no survivor missing", has("   PASS"))])

# ------------------------------------------------------------------ coverage (D2)
def exc36(out):
    """exceptions printed by script 36: [(S tuple, W label, tag or None)]"""
    ex = []; on = False
    for line in out.splitlines():
        if line.strip().startswith("exceptions (no cutoff)"): on = True; continue
        if on:
            m = re.match(r"\s+\(\(([\d, ]+)\), '([^']+)'(?:, '(t:[a-z])')?", line)
            if not m: break
            ex.append((tuple(int(v) for v in m.group(1).split(",") if v.strip()), m.group(2), m.group(3)))
    return ex
def dfs_inputs(out):
    return {(tuple(int(v) for v in m.group(1).split(",")), m.group(2))
            for m in re.finditer(r"S = \[([\d, ]+)\]  W (\S+):", out)}
COVER = {   # 36 run  ->  38 run that must cover its exceptions
    "36 profile 1,yes,1,3,1": "38 DFS on 1,yes,1,3,1 exceptions",
    "36 profile 2,yes,1,4,1": "38 DFS on 2,yes,1,4,1 level-2 exceptions",
}
for n36 in [k for k in outputs if k.startswith("36 profile")]:
    ex = exc36(outputs[n36])
    if not ex: continue
    n38 = COVER.get(n36)
    covered = dfs_inputs(outputs.get(n38, "")) if n38 else set()
    missing = [e for e in ex if e[2] is not None or (e[0], e[1]) not in covered]
    ok = not missing
    results.append((f"coverage: {n36}", ok, "" if ok else f"not resolved by a DFS run: {missing}"))
    print(f"{'PASS' if ok else 'FAIL'}  coverage: every exception of {n36} is a DFS input ({len(ex)} exception(s))"
          + ("" if ok else f"\n      missing: {missing}"), flush=True)

print()
nf = sum(1 for r in results if not r[1])
print(f"{len(results) - nf} passed, {nf} failed" + ("" if FULL else "   (fast tier; run 'full' for scripts 34, 35 and profile 2,yes,1,4,1)"))
sys.exit(1 if nf else 0)
