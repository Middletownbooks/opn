# Reproducible audit scripts

Standard library only (tested on Python 3.11.15). Each script takes an optional
path to a checkout of the audited repository; the default is
`/home/user/mantovanelli1110/opn-small-prime-closure-certificates`.

```bash
git clone https://github.com/Mantovanelli1110/opn-small-prime-closure-certificates
cd opn-small-prime-closure-certificates && git checkout C-small-2026-07
```

| script | establishes |
|---|---|
| `01_release_integrity.py` | which published SHA256 hashes fail, and which failures are CRLF/LF vs genuine content drift |
| `02_run_released_verifiers.sh` | the five advertised verifier commands and their actual output |
| `03_support_floor_and_phi5.py` | the exact `k₀(q)` support-floor table (Proposition C), and an independent check of the `Φ₅/5` forced-prime lemma |
| `04_tail_envelope_nogo.py` | Proposition A / Corollary B, and the per-record shortfall for all 32 tail records |
| `05_mutation_tests.py` | exactly which q=17 certificate fields the verifier protects and which it transcribes |
| `06_release_tail_inventory.py` | the `(B,M)` multiset per bundle, which bundles carry numerator/denominator fields, and consistency against `k₀(q)` |

Findings are written up in `../AUDIT_REPORT.md`.
