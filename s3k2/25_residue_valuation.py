#!/usr/bin/env python3
"""
The five level-5 sets that need the conditional step, and a valuation sharpening.

For each of them the closure condition of section 9 pins the roles completely,
which lets the valuation balance at an ORDINARY prime a be read off.  a has
exponent exactly 2, so

    2 = e_a = sum over all components C != a^2 of v_a(sigma(C)).

Two contributions are forced and computable:
  * the OTHER ordinary prime b: v_a(b^2+b+1), a plain integer;
  * the SPECIAL prime p: e = 1 (mod 4) is odd, so e+1 is even; if p = -1 (mod a)
    then ord_a(p) = 2 divides e+1 and a | sigma(p^e) for EVERY admissible e.
    (This is the same mechanism as 7 | sigma(13^e), used in section 8b.)

If those already account for both units, then sum over U of v_a(x^2+x+1) = 0,
i.e. NO ordinary prime x = 2 (mod 3) may have a | x^2+x+1.  That deletes members
of Sm(T) outright and shrinks the Thue-Mahler equation that remains.
"""
from itertools import combinations

def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; r=0
    while d%2==0: d//=2; r+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def fac(n):
    f={}; d=2
    while d*d<=n and d<10**8:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d += 1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f
def Fset(t): return frozenset(p for p in fac(t*t+t+1) if p%3==1)

RES = [(7,13,19,37,67), (7,13,19,37,127), (7,13,19,43,127),
       (7,13,19,127,409), (7,13,19,127,1723)]
SM  = {(7,13,19,37,67):[11,29,653], (7,13,19,37,127):[11,107,653],
       (7,13,19,43,127):[11,107,653], (7,13,19,127,409):[11,53,107,653],
       (7,13,19,127,1723):[11,41,107,653]}

for T in RES:
    Ts=set(T)
    print("="*70)
    print(f"T = {list(T)}    Sm(T) = {SM[T]}")
    # roles forced by closure
    cands=[o for o in combinations(T,2) if all(Fset(t)<=Ts for t in o)]
    for O in cands:
        rest=[t for t in T if t not in O]
        specs=[s for s in rest if s%12==1]
        for s in specs:
            ns=[t for t in rest if t!=s]
            print(f"   ordinary {list(O)}   special {s}   notable {ns}")
            for a in O:
                b=[x for x in O if x!=a][0]
                va_b=fac(b*b+b+1).get(a,0)
                forced_p = 1 if (s % a == a-1) else 0
                tot=va_b+forced_p
                note=[]
                if va_b: note.append(f"v_{a}(sigma({b}^2)) = {va_b}")
                if forced_p: note.append(f"{s} = -1 mod {a}, so {a} | sigma({s}^e) always")
                print(f"      e_{a} = 2 ; forced so far = {tot}"
                      + ("   [" + "; ".join(note) + "]" if note else ""))
                if tot>=2:
                    kill=[x for x in SM[T] if (x*x+x+1)%a==0]
                    print(f"         => no x in U may have {a} | x^2+x+1 ; "
                          f"that deletes {kill} from Sm(T)")
    # T survives if SOME admissible assignment leaves enough room, so take the
    # union over assignments of what that assignment allows.
    left=set()
    for O in cands:
        rest=[t for t in T if t not in O]
        for sp in [x for x in rest if x%12==1]:
            allowed=set(SM[T])
            for a in O:
                b=[x for x in O if x!=a][0]
                if fac(b*b+b+1).get(a,0) + (1 if sp%a==a-1 else 0) >= 2:
                    allowed -= {x for x in SM[T] if (x*x+x+1)%a==0}
            left |= allowed
    print(f"   surviving candidates for U, over all admissible assignments : "
          f"{sorted(left)}   (need |U| >= 4)")
print("="*70)
print("""
So for each of the five, the residual statement is a Thue-Mahler equation over a
SMALLER prime set than T: after the deletions above, U would have to be supplied
almost entirely by solutions of x^2+x+1 = T-smooth with x beyond the search
bound 10^12.  omega(N) >= 10 forces |U| >= 4.""")
