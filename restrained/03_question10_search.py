#!/usr/bin/env python3
"""
Ochem-Zelinsky Question 10: do there exist primes x, y, p, r and integers
a > b > 0 with  x^2+x+1 = p^a r  and  y^2+y+1 = p^b r ?
They note: "If the answer to 10 is no, then we could substantially tighten
Lemma 8."  So this is the lever they themselves name.

REFORMULATION.  If x^2+x+1 = p^a r and y^2+y+1 = p^b r with the same p and r,
then dividing gives
        x^2 + x + 1 = p^{a-b} (y^2 + y + 1),
so the question is a collision in the map  x |--> (p, r)  over primes x whose
x^2+x+1 has exactly two distinct prime factors, one of them to the first power.
(Two distinct x with the SAME (p,r) automatically have a != b, since equal
exponents would force x = y.)

SEARCH.  For every prime x up to the bound, factor x^2+x+1 and keep those of
shape p^a * r with p, r distinct primes and a >= 1.  Then look for two x's
sharing (p, r).
"""
import sys, random, math
def sieve(n):
    b=bytearray([1])*(n+1); b[0]=b[1]=0
    for i in range(2,int(n**0.5)+1):
        if b[i]: b[i*i::i]=bytearray(len(b[i*i::i]))
    return b
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
def rho(n):
    if n%2==0: return 2
    while True:
        x=random.randrange(2,n); y=x; c=random.randrange(1,n); d=1
        while d==1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n
            d=math.gcd(abs(x-y),n)
        if d!=n: return d
def factor(n,out=None):
    if out is None: out={}
    if n==1: return out
    if isprime(n): out[n]=out.get(n,0)+1; return out
    d=rho(n); factor(d,out); factor(n//d,out); return out

LIM=int(sys.argv[1]) if len(sys.argv)>1 else 200000
B=sieve(LIM)
sigs={}; checked=0; shape=0
for x in range(5,LIM):
    if not B[x]: continue
    checked+=1
    f=factor(x*x+x+1)
    if len(f)!=2: continue
    (p1,e1),(p2,e2)=sorted(f.items())
    # want shape p^a * r with r to the first power
    cands=[]
    if e2==1: cands.append((p1,e1,p2))
    if e1==1: cands.append((p2,e2,p1))
    for p,a,r in cands:
        shape+=1
        sigs.setdefault((p,r),[]).append((x,a))
hits={k:v for k,v in sigs.items() if len(v)>1}
print(__doc__)
print(f"primes x examined                    : {checked}")
print(f"of shape p^a * r (two prime factors) : {shape}")
print(f"colliding (p,r) signatures           : {len(hits)}")
if hits:
    for (p,r),v in sorted(hits.items()):
        print(f"   p={p} r={r}: {v}")
else:
    print(f"\nNo collision among primes x < {LIM}.")
print()
print("""This is DATA on an open question, not a theorem.  A null search establishes
no impossibility; recorded here only as a computational bound, which is what
Question 10 currently lacks.  Their own near-examples both have composite x:
30^2+30+1 = 7^2*19 with 11^2+11+1 = 7*19, and 9353^2+9353+1 = 409^2*523 with
462^2+462+1 = 409*523.""")
