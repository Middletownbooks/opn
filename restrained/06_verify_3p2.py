#!/usr/bin/env python3
"""Verify every factorisation asserted in Ochem-Zelinsky's 3p2.txt.

Each line 'X^2 => f1 f2 ...' claims the multiset {f_i} is the prime
factorisation of sigma(X^2) = X^2+X+1.
Each line 'X^e => 2 f1 f2 ...' claims it is the factorisation of X+1, the
factor of sigma(X^e) available when X is the special prime (e odd).
Trailing 'F t' / 'XS t' are contradiction markers, not part of the product.
"""
import re
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

ok=bad=0; problems=[]
for line in open('3p2.txt'):
    line=line.strip()
    m=re.match(r'^(\d+)\^([2e])\s*=>\s*(.*)$', line)
    if not m: continue
    X=int(m.group(1)); kind=m.group(2); rhs=m.group(3)
    toks=[]
    for t in rhs.split():
        if t in ('F','XS'): break
        toks.append(t)
    prod=1; comp=[]
    good=True
    for t in toks:
        mm=re.match(r'^(\d+)(?:\^(\d+))?$', t)
        if not mm: good=False; break
        b=int(mm.group(1)); ex=int(mm.group(2) or 1)
        if not isprime(b): comp.append(b)
        prod *= b**ex
    if not good: continue
    target = X*X+X+1 if kind=='2' else X+1
    if prod==target and not comp:
        ok+=1
    else:
        bad+=1
        problems.append((line, target, prod, comp))
print(__doc__)
print(f"lines checked : {ok+bad}")
print(f"correct       : {ok}")
print(f"incorrect     : {bad}")
for line,t,p,c in problems:
    print(f"   {line!r}")
    print(f"      target {t}  product {p}  non-prime entries {c}")
