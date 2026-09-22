import json,glob,os,collections
from fractions import Fraction
D='/home/user/mantovanelli1110/opn-small-prime-closure-certificates'
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def primes_from(q,c):
    o=[];p=q
    while len(o)<c:
        if isprime(p): o.append(p)
        p+=2
    return o
def H(t):
    v=Fraction(1)
    for p in t: v*=Fraction(p,p-1)
    return v
k0={}
for q in (5,7,11,13,17):
    P=primes_from(q,600);v=Fraction(1);k=0
    while v<=2:
        v*=Fraction(P[k],P[k]-1);k+=1
    k0[q]=k
print("elementary abundancy floors k0(q):",k0)
print()
for q in (5,7,11,13,17):
    f=f'{D}/q{q}_master_bundle.jsonl'
    recs=[json.loads(l) for l in open(f) if l.strip()]
    types=collections.Counter(r.get('type') for r in recs)
    withBM=[r for r in recs if 'B' in r and 'M' in r]
    bm=collections.Counter((r['B'],r['M']) for r in withBM)
    print(f"=== q={q}: {len(recs)} records, {len(types)} types; {len(withBM)} records carry (B,M) ===")
    print(f"    (B,M) multiset: {dict(bm)}")
    # any numerator/denominator fields?
    numfields=set()
    for r in recs:
        for k in r:
            if 'num' in k.lower() or 'den' in k.lower(): numfields.add(k)
    print(f"    numerator/denominator fields present anywhere: {sorted(numfields) or 'NONE'}")
    # evaluate each distinct (B,M,kernel)
    seen=set()
    for r in withBM:
        kern=r.get('K_base') or r.get('pure_kernel') or r.get('K_env') or []
        key=(tuple(kern),r['B'],r['M'])
        if key in seen: continue
        seen.add(key)
        t=len(kern); B,M=r['B'],r['M']
        asserted_omega=t+M
        floor=k0[q]
        ok = asserted_omega>=floor
        print(f"    K={list(kern)} B={B} M={M} -> asserts omega(N)<={asserted_omega}; floor k0={floor}; consistent? {ok}")
    print()
