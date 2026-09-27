#!/usr/bin/env python3
"""Print the tally line of a 36 log (and its caseB / conditional / exception lists)."""
import re, sys
for f in sys.argv[1:]:
    s = open(f).read()
    try:
        rd = re.search(r"killed early \(raw role minimum > 18/13\): (\d+)", s).group(1)
        m = re.search(r"final sets: uncond dead (\d+), conditional dead (\d+), no role/config (\d+), ALIVE (\d+)", s)
        ex = re.search(r"exceptions \(no cutoff\): (\d+)", s).group(1)
        cb = re.search(r"case-B enumerations \(conditional on 10\^MB_EXP bound\): (\d+)", s).group(1)
        lv = re.search(r"level counts \(summed over W configs\): (.*)", s).group(1)
        print(f"{f.split('/')[-1]:60s} raw {rd} uncond {m.group(1)} cond {m.group(2)} nocfg {m.group(3)} ALIVE {m.group(4)} exc {ex} caseB {cb}  levels {lv}")
    except Exception as e:
        print(f"{f}: no tally ({s.strip().splitlines()[-1][:120] if s.strip() else 'empty'})")
