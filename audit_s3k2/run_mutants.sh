#!/bin/bash
# Part C batch: every mutant on the scripts it touches (fast profiles only; the
# 37-minute profile 2,yes,1,4,1 is run separately for the mutants that matter).
export MUTDIR=/tmp/claude-0/-home-user-opn/29d8ccf1-27b9-5592-82bc-38990ba368e7/scratchpad
cd "$(dirname "$0")"
P36="36_profile_recursion.py"
ALL6="$P36 0,no,2,2,1|$P36 0,yes,2,3,0|$P36 1,yes,2,4,0|$P36 1,no,2,3,1|$P36 0,yes,1,2,1|$P36 1,yes,1,3,1"
A1="$P36 1,yes,2,4,0|$P36 1,no,2,3,1|$P36 1,yes,1,3,1"
IFS='|' read -ra ALL <<< "$ALL6"
IFS='|' read -ra AL1 <<< "$A1"
python3 mutate.py corr1 "$P36 validate" "${ALL[@]}"
python3 mutate.py dropsplit_o "${AL1[@]}"
python3 mutate.py dropsplit_n "${AL1[@]}"
python3 mutate.py dropsplit_s "${AL1[@]}"
python3 mutate.py caseB_to_B "${AL1[@]}"
python3 mutate.py nogenericW "${ALL[@]}"
python3 mutate.py noHIW "${ALL[@]}"
python3 mutate.py theta "39_baker_lll.py validate" "39_baker_lll.py residual"
python3 mutate.py c112 "39_baker_lll.py validate" "39_baker_lll.py residual"
python3 mutate.py novieta "38_closure_dfs.py 2,yes,1,4,1 2"
echo BATCH DONE
