#!/usr/bin/env python3
"""
A narrowing of Ochem-Zelinsky's Question 10.

QUESTION 10.  Do there exist primes x, y, p, r and integers a > b > 0 with
    x^2 + x + 1 = p^a * r      and      y^2 + y + 1 = p^b * r ?

PROPOSITION.  Any solution has p = 1 (mod 3) and p >= 7.  In particular
p = 3 is impossible.

PROOF.  v_3(t^2+t+1) <= 1 for every integer t: if t = 1 (mod 3), write
t = 1+3k, then t^2+t+1 = 3(1+3k+3k^2) and 1+3k+3k^2 = 1 (mod 3), so v_3 = 1;
if t = 0 or 2 (mod 3) then t^2+t+1 = 1 (mod 3) and v_3 = 0.  A solution needs
a > b > 0, hence a >= 2, so p^a | x^2+x+1 forces v_p(x^2+x+1) >= 2.  With
p = 3 that contradicts v_3 <= 1.  Every prime factor of t^2+t+1 is 3 or
= 1 (mod 3), so p = 1 (mod 3), and the least such prime is 7.   QED

CONSEQUENCE.  A solution requires p^2 | x^2+x+1 with p = 1 (mod 3), p >= 7.
For such p the congruence t^2+t+1 = 0 (mod p^2) has exactly two roots (Hensel
lifts of the two roots mod p; the derivative 2t+1 is invertible mod p since
p != 3), so x lies in just 2 residue classes mod p^2.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def v3(n):
    v=0
    while n%3==0: n//=3; v+=1
    return v
print(__doc__)
print("Verification that v_3(t^2+t+1) <= 1 for t = 1..200000:", 
      max(v3(t*t+t+1) for t in range(1,200001)))
print()
print("Verification that every prime factor of t^2+t+1 is 3 or 1 mod 3 (t <= 3000):")
def factor(n):
    f=set(); d=2
    while d*d<=n:
        while n%d==0: f.add(d); n//=d
        d+=1
    if n>1: f.add(n)
    return f
bad=[(t,r) for t in range(1,3001) for r in factor(t*t+t+1) if r!=3 and r%3!=1]
print("   violations:", bad if bad else "none")
print()
print("Two roots of t^2+t+1 = 0 mod p^2, for the first primes p = 1 mod 3:")
print(f"{'p':>6} {'p^2':>9} {'roots mod p^2':>26} {'least prime x in those classes':>32}")
for p in [q for q in range(7,120) if isprime(q) and q%3==1]:
    m=p*p
    roots=[t for t in range(m) if (t*t+t+1)%m==0]
    least=None
    for t in sorted(roots):
        x=t
        while x < 4*10**5:
            if x>2 and isprime(x): break
            x+=m
        if x < 4*10**5 and (least is None or x<least): least=x
    print(f"{p:>6} {m:>9} {str(roots):>26} {str(least):>32}")
