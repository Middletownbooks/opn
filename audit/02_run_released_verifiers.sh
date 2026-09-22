#!/usr/bin/env bash
# Run the five verifier commands advertised in the paper's Table 6.
D="${1:-/home/user/mantovanelli1110/opn-small-prime-closure-certificates}"
cd "$D" || exit 1
for q in 5 7 11 13 17; do
  case $q in
    5) v=q5_branch_closure_verifier_strict.py ;;
    *) v=q${q}_branch_closure_verifier.py ;;
  esac
  echo "===== python3 $v q${q}_master_bundle.jsonl ====="
  python3 "$v" "q${q}_master_bundle.jsonl" 2>&1 | tail -6
  echo "   [exit=${PIPESTATUS[0]}]"
done
