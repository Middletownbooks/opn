#!/usr/bin/env python3
"""
Costing the 3-budget at k = 2 with 3 notable.

SETTING.  N is 2-restrained.  3 | N (the case 3 does not divide N is closed),
3 is not ordinary (section 3 is closed), and 3 cannot be special (p = 1 mod 4
while 3 = 3 mod 4).  So 3 is one of the two NOTABLE components: 3^q || N with
q even >= 4.  Write the other notable n_2^{q_2}, the special p^e, and let
o_1 = #{ordinary s : s = 1 (mod 3)}.

THE BUDGET.   q = e_3 = sum over components C != 3^q of v_3(sigma(C)), and

    ordinary s   :  v_3(s^2+s+1) = 1 if s = 1 mod 3, else 0
    notable n_2  :  v_3(sigma(n_2^{q_2})) = v_3(q_2+1) if n_2 = 1 mod 3, else 0
    special p    :  v_3(sigma(p^e))       = v_3(e+1)   if p = 1 mod 3,
                                          = v_3(p+1) + v_3(e+1) if p = 2 mod 3

so, writing  i = v_3(e+1),  j = v_3(q_2+1)*[n_2 = 1 mod 3],
             m = v_3(p+1)*[p = 2 mod 3],

    q = o_1 + m + i + j.

At k = 1 the term j is absent.  The question is whether j is FREE -- if it were,
q could be large with o_1 small and omega(N) small, and the k = 1 chain would
break at k = 2.

THE COSTING.  It is not free.  If 3^j | q_2 + 1 then for each k = 1..j the
divisor d = 3^k of q_2+1 gives, by Zsigmondy, a primitive prime divisor r_k of
n_2^{d} - 1 (no exception applies: the only exceptions for a^n - 1 are n = 2 with
a+1 a power of 2, and n = 6 with a = 2; here n = 3^k >= 3 and a = n_2 >= 5).
Then
    r_k = 1 (mod 3^k),  r_k odd,  r_k does not divide n_2 - 1,
    r_k | n_2^{3^k} - 1 | n_2^{q_2+1} - 1,   so   r_k | sigma(n_2^{q_2}),
and the r_k are pairwise distinct.  Each divides sigma(N) = 2N and is odd, so
each divides N.  The same applies to p with i in place of j.

This script verifies every step of that on explicit numbers.
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
    f={}; d=2
    while d*d<=n and d<3*10**6:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d += 1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f
def v3(n):
    k=0
    while n%3==0: n//=3; k+=1
    return k
def sigma(t,k): return sum(t**i for i in range(k+1))

def primitive(a, d):
    """primitive prime divisors of a^d - 1 (those not dividing a^c-1 for c<d)."""
    v = a**d - 1
    for c in range(1, d):
        if d % c: continue
        g = math.gcd(v, a**c - 1)
        while g > 1:
            v //= g
            g = math.gcd(v, a**c - 1)
    return sorted(factor(v)) if v > 1 else []

print("=" * 74)
print("STEP 1.  For d = 3^k, a primitive prime divisor of a^d - 1 always exists,")
print("         is = 1 (mod 3^k), is odd, and divides sigma(a^q) whenever d | q+1.")
print("=" * 74)
print(f"   {'a':>5} {'d=3^k':>7} {'primitive primes of a^d - 1':>34} "
      f"{'= 1 mod d':>10} {'odd':>5}")
bad = 0
for a in (5, 7, 11, 13, 17, 19, 23, 31):
    for k in (1, 2, 3):
        d = 3**k
        if a**d > 10**28: continue
        P = primitive(a, d)
        ok1 = all(r % d == 1 for r in P)
        ok2 = all(r % 2 == 1 for r in P)
        if not P or not ok1 or not ok2: bad += 1
        if k <= 2:
            print(f"   {a:>5} {d:>7} {str(P)[:34]:>34} {str(ok1):>10} {str(ok2):>5}")
print(f"   failures: {bad}")
print()

print("=" * 74)
print("STEP 2.  The j primitive primes really do divide sigma(n^q) and are")
print("         pairwise distinct, so v_3(sigma(n^q)) = j costs j prime divisors.")
print("=" * 74)
print(f"   {'n':>4} {'q':>6} {'j=v3(q+1)':>10} {'distinct primitive primes r_1..r_j':>44} {'all | sigma':>12}")
bad = 0; tot = 0
for n in (7, 13, 19, 31, 37, 43):
    for q in (8, 26, 80, 242):            # q+1 = 9, 27, 81, 243 : j = 2,3,4,5
        j = v3(q + 1)
        if n**(q+1) > 10**200: continue
        S = sigma(n, q)
        rs = []
        for k in range(1, j + 1):
            P = primitive(n, 3**k)
            if P: rs.append(P[0])
        ok = all(S % r == 0 for r in rs) and len(set(rs)) == len(rs)
        tot += 1
        if not ok or len(rs) < j: bad += 1
        print(f"   {n:>4} {q:>6} {j:>10} {str(rs)[:44]:>44} {str(ok):>12}")
print(f"   {tot} cases, {bad} failures")
print()

print("=" * 74)
print("STEP 3.  The counting bound")
print("=" * 74)
print("""   The primes r_k(p) (k = 1..i) and r_k(n_2) (k = 1..j) are all = 1 (mod 3)
   and divide N.  The ONLY primes = 1 (mod 3) dividing N that are not ordinary
   are n_2 and p themselves -- 3 is = 0 (mod 3) and there are no other
   non-ordinary components.  So the union of the two families, which has at
   least max(i, j) elements, contains at most 2 non-ordinary primes:

        o_1  >=  max(i, j) - 2   >=   (i + j)/2 - 2.

   Feeding that into  q = o_1 + m + i + j  with  S = i + j:

        q - m - S  =  o_1  >=  S/2 - 2      =>   S <= (2(q - m) + 4)/3
        o_1 >= (q - m) - (2(q - m) + 4)/3   =    (q - m - 4)/3

   and omega(N) >= 3 + o_1 (the three non-ordinary primes 3, n_2, p):

        >>>  omega(N)  >=  3 + (q - m - 4)/3,   m = v_3(p+1) if p = 2 mod 3.  <<<

   At k = 1 the family for n_2 is absent (j = 0), at most one non-ordinary prime
   can occur, and the same computation gives o_1 >= (q - m - 1)/2.""")
print()
print("   So the second notable does NOT give a free escape: every unit it")
print("   contributes to the 3-budget buys a distinct prime divisor of N.")
print("   The ONLY leak is m = v_3(p+1), and that leak is already present at")
print("   k = 1 -- it is not something the second notable creates.")
