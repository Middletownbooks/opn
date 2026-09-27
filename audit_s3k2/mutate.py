#!/usr/bin/env python3
"""
Audit Part C: mutation tests.  Never touches s3k2/: each mutant is a copy of
s3k2/*.py in a scratch directory with ONE textual patch applied (the patch must
match exactly once, else the mutant is refused), then the named commands are run
there and their output saved to audit_s3k2/logs/mut_<name>_<cmd>.log.

    python3 mutate.py <mutant> <script args> [<script args> ...]
e.g.  python3 mutate.py corr1 "36_profile_recursion.py validate" "36_profile_recursion.py 1,yes,1,3,1"
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "s3k2")
LOGS = os.path.join(HERE, "logs")

MUTANTS = {
    # C1: the k-prime cutoff replaced by the one-prime cutoff (the section 14d error)
    "corr1": ("36_profile_recursion.py",
              "return (B/(B-1.0))**k * math.exp(1.01*(1+1/(math.sqrt(B)-1))*((1-u)**-k - 1)*euler(S))",
              "return (B/(B-1.0)) * math.exp(1.01*(1+1/(math.sqrt(B)-1))*(u/(1-u))*euler(S))"),
    # C2: record the NARROWED LO as the "raw" role minimum used by the raw-minimum kill
    "narrowedraw": ("36_profile_recursion.py",
              "        LO = nl\n    return LO, HI, keep\n",
              "        LO = nl\n    RAW[(S, label)] = LO\n    return LO, HI, keep\n"),
    # C3: perturb theta_13 by 1e-30 in the Baker+LLL solver
    "theta": ("39_baker_lll.py",
              "    return reduce_pi(2*arg_eis(a, b))\n",
              "    return reduce_pi(2*arg_eis(a, b)) + (Decimal('1e-30') if t == 13 else 0)\n"),
    # C4a/b: drop one role split of the last prime in last_candidates
    "dropsplit_o": ("36_profile_recursion.py",
              "    for rho in sorted(set(FULL)):\n        pr = list(FULL); pr.remove(rho)",
              "    for rho in [r for r in sorted(set(FULL)) if r != 'o']:\n        pr = list(FULL); pr.remove(rho)"),
    "dropsplit_n": ("36_profile_recursion.py",
              "    for rho in sorted(set(FULL)):\n        pr = list(FULL); pr.remove(rho)",
              "    for rho in [r for r in sorted(set(FULL)) if r != 'n']:\n        pr = list(FULL); pr.remove(rho)"),
    "dropsplit_s": ("36_profile_recursion.py",
              "    for rho in sorted(set(FULL)):\n        pr = list(FULL); pr.remove(rho)",
              "    for rho in [r for r in sorted(set(FULL)) if r != 's']:\n        pr = list(FULL); pr.remove(rho)"),
    # C5: Matveev's constant 112 -> 11.2
    "c112": ("39_baker_lll.py",
              "val = 112 * 2**n * C2",
              "val = 11.2 * 2**n * C2"),
    # C5b: Matveev's constant inflated by 10^6 (the insensitivity claim of MATVEEV_1998.md)
    "c112x1e6": ("39_baker_lll.py",
              "val = 112 * 2**n * C2",
              "val = 112e6 * 2**n * C2"),
    # extra: the "exact" Case-B enumeration only to B instead of B^2
    "caseB_to_B": ("36_profile_recursion.py",
              "cands |= set(caseB(S, 2*int(math.log10(B)) + 2))",
              "cands |= set(caseB(S, int(math.log10(B)) + 1))"),
    # extra: forget the generic W >= WB configuration for a notable W
    "nogenericW": ("36_profile_recursion.py",
              "        out.append((f\"n>={WB}\", None, lambda MIN: F(1), F(WB, WB-1), 0, ()))\n",
              ""),
    # extra: the Vieta branch of the DFS removed
    "novieta": ("38_closure_dfs.py",
              "            for n in range(2, NSEQ-1):",
              "            for n in range(2, 2):"),
    # extra: the cutoff in 36 fed the narrowed LO after also dividing by nothing but
    # forgetting W's upper factor HIW (a wrong HI)
    "noHIW": ("36_profile_recursion.py",
              "    LO = min(los)*LOW; HI = max(his)*HIW",
              "    LO = min(los)*LOW; HI = max(his)"),
}

def build(name):
    fn, old, new = MUTANTS[name]
    d = tempfile.mkdtemp(prefix=f"mut_{name}_", dir=os.environ.get("MUTDIR"))
    for f in os.listdir(SRC):
        if f.endswith(".py"): shutil.copy(os.path.join(SRC, f), d)
    p = os.path.join(d, fn); s = open(p).read()
    n = s.count(old)
    if n != 1: raise SystemExit(f"mutant {name}: patch matches {n} times, refused")
    open(p, "w").write(s.replace(old, new))
    return d

if __name__ == "__main__":
    name = sys.argv[1]; d = build(name)
    for cmd in sys.argv[2:]:
        args = cmd.split()
        tag = "_".join(a.replace(".py", "").replace(",", "") for a in args)
        out = os.path.join(LOGS, f"mut_{name}__{tag}.log")
        with open(out, "w") as fh:
            p = subprocess.run([sys.executable] + args, cwd=d, stdout=fh, stderr=subprocess.STDOUT)
        print(f"{name}: {cmd} -> exit {p.returncode}, log {os.path.relpath(out, HERE)}", flush=True)
    shutil.rmtree(d, ignore_errors=True)
