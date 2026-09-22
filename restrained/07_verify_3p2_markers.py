#!/usr/bin/env python3
"""
Second layer of verification on 3p2.txt: the CONTRADICTION MARKERS.

Script 06 checked that each line's asserted factorisation is correct.  This
checks the markers that actually cut the branches:

  'F t'   a prime t is forced by this line and was already ruled out, so t must
          genuinely divide the line's target.
  'XS t'  three or more copies of t are forced while t is ordinary.  Depth
          dependent, so only the local claim (t divides the target) is checked.

A marker naming a prime that does NOT divide the target is a broken cut.
Divisibility is tested against a freshly computed target, independently of the
factorisation the file asserts.
"""
import re
lines=[l.rstrip('\n') for l in open('3p2.txt')]
checked=ok=0; bad=[]
for line in lines:
    s=line.strip()
    m=re.match(r'^(\d+)\^([2e])\s*=>\s*(.*)$', s)
    if not m: continue
    X=int(m.group(1)); kind=m.group(2); rhs=m.group(3)
    toks=[]; marker=None; mval=None
    it=iter(rhs.split())
    for t in it:
        if t in ('F','XS'):
            marker=t; mval=next(it, None); break
        toks.append(t)
    if marker is None or mval is None: continue
    facs=set()
    for t in toks:
        mm=re.match(r'^(\d+)(?:\^(\d+))?$', t)
        if mm: facs.add(int(mm.group(1)))
    checked+=1
    tv=int(mval)
    target = X*X+X+1 if kind=='2' else X+1
    in_file = tv in facs
    divides = target % tv == 0
    if in_file and divides: ok+=1
    else: bad.append((s, marker, tv, in_file, divides, target))
print(__doc__)
print(f"lines carrying a marker                      : {checked}")
print(f"marker prime forced, per file AND fresh test : {ok}")
print(f"failures                                     : {len(bad)}")
for s,mk,tv,inf,div,t in bad:
    print(f"\n   {s!r}")
    print(f"      marker {mk} {tv}: listed in file's factors = {inf}; actually divides target = {div}")
    print(f"      target = {t}")
print()
print("="*72)
print("Sanity check on the reported sieve range")
print("="*72)
import math
z=216171986291
def pi(x): return x/math.log(x)
print(f"  pi(z)    ~ {pi(z):>18,.0f}   for z = {z:,}")
print(f"  pi(2^32) ~ {pi(2**32):>18,.0f}")
print(f"  The paper reports 2,500,000,000 surviving ordinary primes up to z,")
print(f"  about {100*2.5e9/pi(z):.0f}% of pi(z) -- internally consistent.")
print(f"  But pi(2^32) ~ {pi(2**32):,.0f} is far BELOW 2.5e9, so the run cannot")
print(f"  have stopped at 2^32.  It necessarily ran well past the point where")
print(f"  the released loopless.cpp's 64-bit `r*r` wraps.  Since the published")
print(f"  numbers are self-consistent, the natural reading is that a different,")
print(f"  wider-arithmetic build produced them.")
