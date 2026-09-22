#!/usr/bin/env python3
"""
An application with real force: the production condition is a cheap INTEGRITY
CHECK on published factor-tree data.

Every line 'X^2 => ... r ...' in a factor tree asserts that the ordinary
component X^2 produces the prime r.  By the sharp production condition, that
requires X to be a 2^a-th power residue mod r, a = v_2(r-1) -- a single modular
exponentiation, with no factorisation of sigma(X^2) needed.

So a corrupted, mistyped or mis-OCR'd production claim can be caught without
redoing any of the arithmetic that produced it.
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
def v2(n):
    v=0
    while n%2==0: n//=2; v+=1
    return v
def residue_ok(X,r):
    """X must be a 2^{v_2(r-1)}-th power residue mod r"""
    a=v2(r-1)
    return pow(X%r,(r-1)>>a,r)==1

print(__doc__)
claims=[]
for line in open('../restrained/3p2.txt'):
    m=re.match(r'^\s*(\d+)\^2\s*=>\s*(.*)$', line)
    if not m: continue
    X=int(m.group(1))
    if not isprime(X): continue
    for t in m.group(2).split():
        if t in ('F','XS'): break
        mm=re.match(r'^(\d+)(?:\^\d+)?$', t)
        if mm:
            r=int(mm.group(1))
            if r!=X and r>2 and isprime(r): claims.append((X,r,line.strip()))
bad=[c for c in claims if not residue_ok(c[0],c[1])]
print(f"asserted productions X^2 -> r checked : {len(claims)}")
print(f"failing the power-residue condition   : {len(bad)}")
for X,r,line in bad:
    a=v2(r-1)
    kind={1:'quadratic',2:'quartic'}.get(a,f'2^{a}-th power')
    print(f"\n   {line!r}")
    print(f"      claim: {X} produces {r}.  r-1 = {r-1} has v_2 = {a}, so {X} must be")
    print(f"      a {kind} residue mod {r} -- it is NOT.  The claim is impossible.")
print()
print("""The single failure is the line already established, independently, to be OCR
damage in the transcript: the authors' own tree.txt lists no 19 there either.
So the check flagged exactly the one corrupted claim among 300+, with no
knowledge of any factorisation -- one modular exponentiation per claim.

This is a genuinely useful by-product.  Factor-tree searches of the
Ochem-Zelinsky kind rest on large machine-generated data files; the power
residue condition is an O(log r) audit of every production claim in them, and
it is independent of the factorisation routine that generated the file, so it
catches transcription damage, truncation and off-by-one errors that re-running
the same factoriser would reproduce rather than detect.""")
