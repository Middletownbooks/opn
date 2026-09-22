#!/usr/bin/env python3
"""
Does a HIGHER-RECIPROCITY obstruction exist at all?

Before hunting for a biquadratic reciprocity law, test whether the obstruction
it would have to provide is even possible.

The quadratic case works because for p = s = 3 (mod 4), mutual production
forces (p/s) = (s/p) = 1 while reciprocity forces their product to be -1.  The
forcing is absolute: there is no free choice.

For the quartic analogue take p = s = 5 (mod 8), so v_2(p-1) = v_2(s-1) = 2 and
the production condition is exactly "quartic residue".  Note the condition is
not merely necessary but REALISABLE: if ord_s(p) = d is odd then taking
n_p = d (so e_p = d-1, even) gives s | sigma(p^{e_p}).  So mutual production
between p and s happens for SOME admissible exponents precisely when

    p^{(s-1)/4} = 1 (mod s)   and   s^{(p-1)/4} = 1 (mod p).

If such pairs exist, no obstruction of the quadratic shape can exist for the
quartic condition, and the avenue is dead whatever Burde's law says.
"""
def isprime(n):
    if n<2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%q==0: return n==q
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
def can_produce(t,r):
    """t can produce r for some admissible even exponent"""
    a=v2(r-1)
    return pow(t%r,(r-1)>>a,r)==1

print(__doc__)
def scan(label, cond, lim):
    P=[p for p in range(3,lim) if isprime(p) and cond(p)]
    mutual=[]
    for i,p in enumerate(P):
        for s in P[i+1:]:
            if can_produce(p,s) and can_produce(s,p): mutual.append((p,s))
    print(f"{label}")
    print(f"   primes considered below {lim}: {len(P)}")
    print(f"   MUTUAL-production pairs found: {len(mutual)}")
    if mutual:
        print(f"   first few: {mutual[:6]}")
    return mutual

print("="*74)
m3 = scan("CONTROL - both p, s = 3 (mod 4).  Reciprocity predicts ZERO.",
          lambda p: p%4==3, 400)
print()
m5 = scan("QUARTIC - both p, s = 5 (mod 8).  Is an obstruction possible?",
          lambda p: p%8==5, 600)
print()
m1 = scan("OCTIC+ - both p, s = 1 (mod 8).",
          lambda p: p%8==1, 900)

print()
print("="*74)
print("VERDICT")
print("="*74)
if m5 or m1:
    p,s = (m5 or m1)[0]
    print(f"""Mutual production IS possible beyond the quadratic case.  Explicit witness:
p = {p}, s = {s}, both in the stated class, with each a suitable power residue
modulo the other:
   ord_{s}({p}) is odd  ->  {s} | sigma({p}^e) for a suitable even e
   ord_{p}({s}) is odd  ->  {p} | sigma({s}^f) for a suitable even f

So there is NO analogue of NO2CYCLE for the quartic or octic conditions, and no
reciprocity law can supply one: the configuration the law would have to forbid
actually occurs.  The avenue flagged at the end of the previous checkpoint is
CLOSED, and it is closed without needing Burde's law at all.

Why the quadratic case is special: the Legendre symbol takes two values and
(p/s)(s/p) = -1 leaves no freedom when p = s = 3 (mod 4).  The quartic residue
character takes four values and the rational quartic reciprocity laws relate
quartic symbols to representations p = a^2 + b^2 rather than pinning a product
to -1, so they constrain WHICH pairs are mutual without forbidding mutuality.""")
else:
    print("No mutual pairs found in range -- an obstruction might exist; the law would be needed.")
