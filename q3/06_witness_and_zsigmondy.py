#!/usr/bin/env python3
"""Concrete witness for the quartic mutual pair, and a forcing tool that does
survive at q = 3."""
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
def order(a,m):
    a%=m; x,k=a,1
    while x!=1: x=(x*a)%m; k+=1
    return k
def sigma(p,e): return sum(p**i for i in range(e+1))
def divisors(n): return sorted(d for d in range(1,n+1) if n%d==0)

print("="*74)
print("1.  EXPLICIT WITNESS: mutual production with p = s = 5 (mod 8)")
print("="*74)
p,s = 5,101
print(f"   p = {p}, s = {s}; both = 5 (mod 8), so both production conditions are QUARTIC.")
d1=order(p,s); d2=order(s,p)
print(f"   ord_{s}({p}) = {d1}  (odd: {d1%2==1})   -> take n_p = {d1}, e_p = {d1-1} (even)")
print(f"   ord_{p}({s}) = {d2}  (odd: {d2%2==1})   -> order one, so take n_s = {p}, e_s = {p-1} (even)")
A=sigma(p,d1-1); B=sigma(s,p-1)
print(f"   sigma({p}^{d1-1}) mod {s} = {A%s}   -> {s} divides it: {A%s==0}")
print(f"   sigma({s}^{p-1}) mod {p} = {B%p}   -> {p} divides it: {B%p==0}")
print(f"   So {p} produces {s} AND {s} produces {p}.  Mutual production occurs.")
print()
print("   Contrast, the quadratic case p = 7, s = 11 (both 3 mod 4):")
print(f"      ord_11(7) = {order(7,11)} (even) -> 11 can NEVER divide sigma(7^even)")
print(f"      ord_7(11) = {order(11,7)} (odd)  -> 7 | sigma(11^2) = {sigma(11,2)}")
print("      exactly one direction, as reciprocity forces.")

print()
print("="*74)
print("2.  A FORCING TOOL THAT SURVIVES AT q = 3: the Zsigmondy support bound")
print("="*74)
print("""THEOREM.  Let N be odd perfect and p | N, n_p = e_p + 1.  Then

        omega(N)  >=  d(n_p),      d = number-of-divisors.

PROOF.  sigma(p^{e_p}) = prod_{d | n_p, d > 1} Phi_d(p).  Every p | N has n_p
odd (n_p = e_p+1 with e_p even for non-Euler p; for the Euler prime n_pi is
even, so apply this only to non-Euler p).  Hence every divisor d > 1 of n_p is
odd and >= 3, so Zsigmondy applies without exception (the exceptions for
base p >= 3 are n = 1 and n = 2, and n = 6 only for base 2): Phi_d(p) has a
primitive prime divisor r_d with ord_{r_d}(p) = d.  Distinct d give distinct
r_d, each r_d is odd and divides sigma(p^{e_p}) | 2N so divides N, and
r_d != p.  With p itself that is d(n_p) - 1 + 1 distinct primes of N.   QED

It needs no lower primes and no abundancy, so unlike the q=5..17 machinery it
is fully available at q = 3.  In particular  omega(N) >= d(e_3 + 1).""")
print()
print("   Verification that the primitive divisors are distinct and = 1 mod d:")
print(f"   {'p':>4} {'n_p':>5} {'divisors>1':>16} {'primitive primes r_d (r_d = 1 mod d)':>44}")
for p,n in ((3,9),(3,15),(5,9),(7,9),(11,15)):
    ds=[d for d in divisors(n) if d>1]
    out=[]
    for d in ds:
        # primitive part of Phi_d(p): strip primes dividing p^k-1 for k<d
        val=sigma(p,d-1)*(p-1)+1-1  # = p^d - 1
        val=p**d-1
        for k in divisors(d):
            if k<d:
                g=p**k-1
                while True:
                    from math import gcd
                    x=gcd(val,g)
                    if x==1: break
                    val//=x
        r=None
        m=val; dd=2
        while dd*dd<=m:
            if m%dd==0: r=dd; break
            dd+=1
        if r is None: r=m
        out.append((d,r,r%d))
    ok=len(set(x[1] for x in out))==len(out)
    print(f"   {p:>4} {n:>5} {str(ds):>16} {str([(d,r) for d,r,_ in out]):>44}")
    assert ok and all(c==1 for _,_,c in out), (p,n,out)
print("   all primitive divisors distinct and = 1 mod d, as claimed")
print()
print("   Consequence at q = 3:  omega(N) >= d(e_3 + 1).")
for n in (9,15,21,45,105,225):
    print(f"      if e_3 + 1 = {n:>4} then omega(N) >= {len(divisors(n))}")
print("""
   Honest limitation: it bites only when e_3 + 1 is composite with many
   divisors.  If e_3 + 1 is prime it gives omega(N) >= 2, which is nothing.
   So it constrains the DIVISOR STRUCTURE of e_3 + 1 given a bound on omega,
   rather than bounding e_3.  Since omega(N) has no known upper bound, it
   does not close anything on its own -- but it is a genuine forcing tool that
   survives where abundancy and lower-prime avoidance do not.""")
