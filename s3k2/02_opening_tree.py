#!/usr/bin/env python3
"""
The section 3 opening tree, computed for general k.

Rules (all conservative -- a branch is cut only when certain):
  * 3 is ordinary, e_3 = 2, so at most TWO copies of 3 may be produced.
  * an ORDINARY x contributes one copy of 3 iff x = 1 (mod 3); a third copy is
    the contradiction 'XS 3'.
  * roles for a forced prime x: ordinary; special (only if unused and
    x = 1 mod 4, forcing the odd part (x+1)/2); notable (only if a notable slot
    remains -- the chain then STOPS, since sigma(n^q) is not determined).
  * contributions of the special and notable components to the 3-budget are
    IGNORED, which only makes the search less able to cut: safe.
  * a prime already on the path is skipped (no cycle claim).
A branch closes when every admissible role is contradicted.  Primes at which a
notable slot is still available are the notable CANDIDATES.
"""
import sys
sys.setrecursionlimit(10000)
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
import math, random
def rho(n):
    if n%2==0: return 2
    while True:
        x=random.randrange(2,n); y=x; c=random.randrange(1,n); d=1
        while d==1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n
            d=math.gcd(abs(x-y),n)
        if d!=n: return d
def factor(n,out=None):
    if out is None: out=set()
    if n<=1: return out
    if isprime(n): out.add(n); return out
    d=rho(n); factor(d,out); factor(n//d,out); return out

LIMIT = 10**26        # refuse to factor beyond this; treat branch as open
class Budget: pass
def run(k, maxdepth=14):
    cands=set(); opened=[]
    def prove(x, spec_used, nots_left, threes, path, depth):
        if depth>maxdepth: opened.append(("depth",x)); return False
        if nots_left>0:
            cands.add(x)          # notable role available -> branch survives
            return False
        # ORDINARY role
        ord_bad=False
        t = threes + (1 if x%3==1 else 0)
        if t>2:
            ord_bad=True                      # XS 3
        else:
            v=x*x+x+1
            while v%3==0: v//=3
            if v>LIMIT: opened.append(("big",x))
            else:
                for r in sorted(factor(v)):
                    if r in path or r==3: continue
                    if prove(r, spec_used, nots_left, t, path|{x}, depth+1):
                        ord_bad=True; break
        if not ord_bad: return False
        # SPECIAL role
        if not spec_used and x%4==1:
            sp_bad=False
            w=(x+1)//2
            if w>LIMIT: opened.append(("big",x))
            else:
                for r in sorted(factor(w)):
                    if r in path or r in (2,3): continue
                    if prove(r, True, nots_left, threes, path|{x}, depth+1):
                        sp_bad=True; break
            if not sp_bad: return False
        return True
    prove(13, False, k, 0, {3}, 0)
    return cands, opened

for k in (1,2):
    c,o = run(k)
    print(f"k = {k}: notable candidates reached from the opening tree ({len(c)}):")
    print(f"   {sorted(c)}")
    if o: print(f"   branches left open for size/depth reasons: {len(o)} {o[:4]}")
    print()
print("Control: the paper's k=1 set is {7, 13, 19, 31, 61, 97, 127, 331}.")
c1,_=run(1)
print(f"   reproduced exactly? {sorted(c1)==[7,13,19,31,61,97,127,331]}")
