#!/usr/bin/env python3
"""
Why p = 1 (mod 3) is forced at k = 1, and why the second notable breaks that.

The leak in the costing of script 01 is m = v_3(p+1), which is non-zero only
when p = 2 (mod 3).  At k = 1 that case cannot occur -- this is Ochem-Zelinsky's
Lemma 6 -- and here is the mechanism, which is exactly what the second notable
undoes.

Suppose p = 2 (mod 3).  With p = 1 (mod 4) that is p = 5 (mod 12).  Ask what can
produce p, i.e. who contributes to  e_p = sum over C != p^e of v_p(sigma(C)):

  * an ORDINARY component s^2 has sigma(s^2) = s^2+s+1, whose prime factors are
    3 or = 1 (mod 3).  p = 2 (mod 3), so no.
  * sigma(p^e) itself is = 1 (mod p), so no.
  * sigma(3^q) = (3^{q+1} - 1)/2 with q EVEN, so q+1 is odd.  If r | sigma(3^q)
    then ord_r(3) divides q+1 and is therefore odd, so 3 is a quadratic residue
    mod r, and by quadratic reciprocity r = +-1 (mod 12).  p = 5 (mod 12) is
    neither, so no.

At k = 1 that exhausts the components and gives e_p = 0, a contradiction: hence
p = 1 (mod 3).  At k = 2 there is one more component, the second notable, and it
is under no such restriction.  So

    >>> p = 5 (mod 12) is possible at k = 2, and then p^e divides
    >>> sigma(n_2^{q_2}) EXACTLY -- the second notable alone must supply every
    >>> one of the e copies of p. <<<

That is the door the second notable opens, and it is not the one I first
guessed: the new term v_3(q_2+1) is fully paid for (script 01), but the second
notable's mere existence removes the obstruction that forced p = 1 (mod 3).
"""
import math

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
def factor(n):
    f=set(); d=2
    while d*d<=n and d<2*10**6:
        while n%d==0: f.add(d); n//=d
        d += 1 if d==2 else 2
    if n>1: f.add(n)
    return f

print("=" * 74)
print("CHECK 1.  prime factors of sigma(3^q), q even : all = +-1 (mod 12)")
print("=" * 74)
bad = 0; shown = 0
for q in range(4, 90, 2):
    v = (3**(q+1) - 1)//2
    F = factor(v)
    ok = all(r % 12 in (1, 11) for r in F)
    if not ok: bad += 1
    if shown < 8:
        print(f"   q = {q:>3}  sigma(3^q) factors {str(sorted(F))[:46]:46s} "
              f"all +-1 mod 12: {ok}")
        shown += 1
print(f"   q = 4..88 even : {bad} failures")
print()

print("=" * 74)
print("CHECK 2.  prime factors of s^2+s+1 : all are 3 or = 1 (mod 3)")
print("=" * 74)
bad = 0; n = 0
for s in range(2, 6000):
    if not isprime(s): continue
    n += 1
    if not all(r == 3 or r % 3 == 1 for r in factor(s*s+s+1)): bad += 1
print(f"   every prime s < 6000 : {n} checked, {bad} failures")
print()

print("=" * 74)
print("CHECK 3.  is 5 (mod 12) really excluded from sigma(3^q)?")
print("=" * 74)
hits = set()
for q in range(4, 120, 2):
    for r in factor((3**(q+1) - 1)//2):
        hits.add(r % 12)
print(f"   residues mod 12 actually seen among those prime factors : "
      f"{sorted(hits)}")
print(f"   5 (mod 12) seen: {5 in hits}     7 (mod 12) seen: {7 in hits}")
print()

print("=" * 74)
print("CONSEQUENCE")
print("=" * 74)
print("""   k = 1 :  nothing can produce a special prime p = 5 (mod 12), so p = 1
            (mod 3), m = v_3(p+1) = 0, and the costing of script 01 gives

                omega(N) >= 2 + (q - 1)/2.

   k = 2 :  the second notable can produce p, so p = 5 (mod 12) survives as a
            case.  In it, p^e || sigma(n_2^{q_2}) exactly, and m = v_3(p+1) is
            unpaid, so the bound degrades to

                omega(N) >= 3 + (q - m - 4)/3,      m = v_3(p+1).

            Since every prime factor of p+1 divides N and p = 1 (mod 4) forces
            p + 1 = 2 mod 4, we have p + 1 = 2 * 3^m * w with w odd and coprime
            to 3, every prime factor of w dividing N.  Taking w = 1 gives
            p = 2*3^m - 1, which costs nothing in omega -- so the leak is real
            and is a condition on the SHAPE of p, not on omega.""")
print()
print("   primes of the form p = 2*3^m - 1 (the zero-cost shape):")
ms = [m for m in range(1, 200) if isprime(2*3**m - 1)]
print(f"      m = {ms}")
for m in ms[:6]:
    p = 2*3**m - 1
    print(f"      m = {m:>3}  p = {p:<22} p mod 12 = {p%12}  "
          f"v_3(p+1) = {m}")
