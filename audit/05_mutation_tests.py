#!/usr/bin/env python3
"""Mutation-test the released q=17 verifier to establish exactly which
certificate fields it protects and which it merely transcribes."""
import json, copy, subprocess, sys, os, tempfile, shutil
D = sys.argv[1] if len(sys.argv) > 1 else \
    '/home/user/mantovanelli1110/opn-small-prime-closure-certificates'
WORK = tempfile.mkdtemp(prefix='q17mut_')
VER = os.path.join(WORK, 'q17_branch_closure_verifier.py')
shutil.copy(os.path.join(D, 'q17_branch_closure_verifier.py'), VER)
base = [json.loads(l) for l in open(os.path.join(D, 'q17_master_bundle.jsonl')) if l.strip()]

def run(recs, tag):
    p = os.path.join(WORK, 'b.jsonl')
    with open(p, 'w') as f:
        for r in recs:
            f.write(json.dumps(r) + '\n')
    r = subprocess.run([sys.executable, VER, p], capture_output=True, text=True)
    ok = r.returncode == 0 and 'exhausted' in r.stdout
    err = (r.stderr.strip().splitlines() or [''])[-1][:80]
    print(f"  {'ACCEPT' if ok else 'reject'}  {tag}")
    if not ok and err:
        print(f"            -> {err}")
    return ok

def idx(i):
    for j, r in enumerate(base):
        if r.get('id') == i:
            return j
    raise KeyError(i)

print("=== BASELINE ===")
run(base, "unmodified release bundle")

print("\n=== A. The load-bearing semantic parameters B and M ===")
for B, M, note in [(59, 36, "M 18->36 (inequality H*(59/58)^36<2 still TRUE)"),
                   (59, 17, "M 18->17 (strictly stronger claim, inequality still true)"),
                   (59, 60, "M 18->60 (the honest value; inequality now FALSE)"),
                   (19, 11, "B 59->19, M->11 (provable floor B; inequality still true)")]:
    m = copy.deepcopy(base)
    for r in m:
        if 'B' in r and 'M' in r:
            r['B'], r['M'] = B, M
    run(m, note)

print("\n=== B. 'endpoint_check' -- the only field spelling out the inequality ===")
m = copy.deepcopy(base)
for r in m:
    if 'endpoint_check' in r:
        r['endpoint_check'] = "H([2,3])*(1/1)^0 < 0   (nonsense)"
run(m, "endpoint_check replaced with arithmetic nonsense")
m = copy.deepcopy(base)
for r in m:
    r.pop('endpoint_check', None)
run(m, "endpoint_check field deleted entirely")

print("\n=== C. Completeness of the endpoint exclusion list ===")
m = copy.deepcopy(base)
m[idx('q17_order17_forced_prime_endpoint')]['excluded_candidates'] = [35, 52, 69, 86]
run(m, "as released: [35,52,69,86]   (18 is also ==1 mod 17 and lies in (17,103))")
m = copy.deepcopy(base)
m[idx('q17_order17_forced_prime_endpoint')]['excluded_candidates'] = [18, 35, 52, 69, 86]
run(m, "corrected to the COMPLETE candidate list [18,35,52,69,86]")

print("\n=== D. Structural / inventory checks ===")
run([r for r in base if r.get('id') != 'q17_strict_tail_e1'],
    "delete the q17_e1_forced frontier record")
m = copy.deepcopy(base); m.append(copy.deepcopy(m[idx('q17_strict_tail_n1')]))
run(m, "duplicate the q17_strict_tail_n1 record")
m = copy.deepcopy(base)
m[idx('q17_first_input_coverage_complete')]['coverage_reference'] = 'cor:does-not-exist'
run(m, "coverage_reference -> nonexistent label")
m = copy.deepcopy(base)
m[idx('q17_first_input_coverage_complete')]['coverage_note'] = 'coverage is incomplete; leaves omitted'
run(m, "coverage_note rewritten to assert INCOMPLETE coverage")
m = copy.deepcopy(base)
m[idx('q17_strict_tail_n1')]['lower_prime_avoidance'] = [3, 5, 7, 11, 13, 19, 23]
run(m, "lower_prime_avoidance extended with unjustified primes 19,23")
shutil.rmtree(WORK, ignore_errors=True)
