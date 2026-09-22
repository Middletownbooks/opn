#!/usr/bin/env python3
"""
Removing the pool restriction from the section-3 profiles closed by counting.

Scripts 27-29 eliminated the thirteen profiles other than (alpha=2, |W|=0,
tau=5) by the count |Sm(T)| < 6 - alpha, but drew T from a finite pool.  The
closure condition can replace the pool wherever it determines T outright.

KEY OBSERVATION.  Let A be the set of ordinary primes of T, |A| = alpha.  Closure
says F(a) is inside T for each a in A, where F(a) = the prime factors of
a^2+a+1 that are = 1 (mod 3).  Hence

        B  :=  A  u  {13}  u  (union of F(a) over a in A)     is inside T,

and every element of B is DETERMINED BY A -- it is a member of A, or 13, or a
prime factor of some a^2+a+1.  So T = B together with (tau - |B|) further primes
that closure says nothing about.  Therefore

    tau = |B|  =>  T is completely determined by A   (no pool needed)
    tau > |B|  =>  T has free slots                  (pool restriction stands)

and the question becomes whether A itself can be enumerated exactly.  It can
whenever the closure condition confines F(a) to a FIXED finite set of primes,
because then

        (a^2 + a + 1)/3   is S-smooth          (v_3(a^2+a+1) = 1 for a = 1 mod 3)

is solved exactly by running over S-smooth M and testing whether 4(3M) - 3 is a
perfect square -- the same device that settled the single-prime equations in
script 26, and usable to bounds far beyond any pool.
"""
import math, sys
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
    while d*d<=n and d<3*10**6:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d += 1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f
def Fset(t): return frozenset(p for p in fac(t*t+t+1) if p%3==1)
def F_inside(t, S):
    """True iff every prime factor of t^2+t+1 that is = 1 (mod 3) lies in S.
       Done by stripping, so it never factors a large number."""
    v = t*t + t + 1
    while v % 3 == 0: v //= 3
    for q in S:
        while v % q == 0: v //= q
    return v == 1
def prime_power_base(M):
    """if M = r^c with r prime, return r; else None."""
    if M < 2: return None
    for c in range(1, 64):
        r = round(M ** (1.0/c)) if M < 10**300 else 0
        for cand in (r-1, r, r+1):
            if cand > 1 and cand**c == M:
                return cand if isprime(cand) else None
        if 2**c > M: break
    return None

def closure_solutions(S, Y):
    """all primes a = 1 (mod 3), a not in S, with (a^2+a+1)/3 S-smooth <= Y."""
    out=[]; L=sorted(S)
    def rec(i,M):
        if i==len(L):
            V=3*M; d=4*V-3; r=math.isqrt(d)
            if r*r==d and r%2==1:
                a=(r-1)//2
                if a>=7 and a%3==1 and isprime(a) and a not in S: out.append(a)
            return
        v=M
        while v<=Y: rec(i+1,v); v*=L[i]
    rec(0,1); return sorted(set(out))

def smooth(T, Y):
    out=[]; L=sorted(T)
    def rec(i,m):
        if i==len(L):
            d=4*m-3; r=math.isqrt(d)
            if r*r==d and r%2==1:
                x=(r-1)//2
                if x>=5 and x%3==2 and isprime(x): out.append(x)
            return
        v=m
        while v<=Y: rec(i+1,v); v*=L[i]
    rec(0,1); return sorted(set(out))

print("="*76)
print("1.  Profiles that were never pool-limited")
print("="*76)
print(f"   F(13) = {sorted(Fset(13))}")
print("""   alpha=0, tau=1  (profiles with |W|=2): T = {13} is FORCED, not chosen.
        Sm({13}) is empty (script 26, exact for every c <= 1200), and the count
        needs |U| >= 6.  Dead, pool-free.
   alpha=1, tau=1  (|W|=3): T = {13} with 13 ordinary, but F(13) = {61} would
        put 61 in T.  No admissible A at all.  Dead, pool-free -- this is the
        three-line lemma of NOTES_S3_K2 section 11b.""")
print()

print("="*76)
print("2.  tau = 2, alpha = 1  (profiles 7 and 9, |W| = 2, need |U| >= 5)")
print("="*76)
print("""   T = {13, t}, one element ordinary.
     * 13 ordinary  -> F(13) = {61} inside T  ->  t = 61, T = {13, 61}.
     * t ordinary   -> F(t) inside {13, t}, and t does not divide t^2+t+1,
                       so (t^2+t+1)/3 = 13^c.  Solved exactly below.""")
Y1 = 10**300
sols = closure_solutions({13}, Y1)
print(f"   (t^2+t+1)/3 = 13^c, searched for every c with 3*13^c <= 10^300 "
      f"(c <= {int(300/math.log10(13))}):")
print(f"      solutions t : {sols}")
cands = [(13,61)] + [tuple(sorted((13,t))) for t in sols]
cands = sorted(set(cands))
print(f"   complete list of admissible T : {[list(c) for c in cands]}")
for T in cands:
    S = smooth(T, 10**160)
    print(f"      T = {str(list(T)):14s} Sm(T) = {str(S):22s} |Sm| = {len(S)}"
          f"   need 5 -> {'ALIVE' if len(S)>=5 else 'DEAD'}")
print()

print("="*76)
print("3.  tau = 3, alpha = 2  (profile 12, |W| = 2, need |U| >= 4)")
print("="*76)
print("""   T = {a1, a2, special}, special = 1 (mod 12).  Two sub-cases.""")
print("   (i) 13 is ordinary.  Then 61 is in T, and the second ordinary a2 needs")
print("       F(a2) inside {13, 61}:  (a2^2+a2+1)/3 is {13,61}-smooth.")
s2 = closure_solutions({13,61}, 10**150)
print(f"       solutions a2 (a2 != 61) : {s2}")
caseI = [tuple(sorted((13,61,a))) for a in s2 if a != 61]
# a2 = 61 is its own branch: then F(61) supplies the third slot.
B61 = {13, 61} | Fset(13) | Fset(61)
print(f"       a2 = 61 branch: B = {{13,61}} u F(13) u F(61) = {sorted(B61)}, "
      f"|B| = {len(B61)}")
if len(B61) == 3:
    T61 = tuple(sorted(B61))
    third = [t for t in T61 if t not in (13,61)][0]
    print(f"       -> T = {list(T61)} with 13, 61 ordinary and {third} special;"
          f" {third} mod 12 = {third%12}"
          f" {'(valid special)' if third%12==1 else '(INVALID special)'}")
    if third % 12 == 1: caseI.append(T61)
print("   (ii) 13 is NOT ordinary, so 13 is the special (13 = 1 mod 12) and")
print("        a1, a2 are ordinary with F(a1) inside {13,a2}, F(a2) inside {13,a1}.")
print("        If F(a1) is inside {13} alone, a1 comes from the list of part 2;")
print("        then a2 comes from an exact {13,a1}-smooth solve.")
caseII = []
for a1 in sols:
    for a2 in closure_solutions({13, a1}, 10**150):
        if F_inside(a1, {13, a2}) and F_inside(a2, {13, a1}):
            caseII.append(tuple(sorted((13, a1, a2))))
print(f"        uncoupled solutions : {sorted(set(caseII))}")
print("        the coupled branch (a2 | a1^2+a1+1 AND a1 | a2^2+a2+1) is searched")
print("        directly over a1 below.")
COUP_MAX = 2*10**6
coupled=[]
for a1 in range(7, COUP_MAX):
    if a1 % 3 != 1 or not isprime(a1): continue
    M = (a1*a1+a1+1)//3
    while M % 13 == 0: M //= 13
    if M == 1: continue                      # that is the uncoupled branch
    a2 = prime_power_base(M)
    if a2 is None or a2 == a1 or a2 % 3 != 1: continue
    if F_inside(a2, {13, a1}): coupled.append(tuple(sorted((13,a1,a2))))
print(f"        coupled solutions with a1 < {COUP_MAX} : {sorted(set(coupled))}")
allT = sorted(set(caseI) | set(caseII) | set(coupled))
print(f"   complete list of admissible T : {[list(t) for t in allT]}")
for T in allT:
    S = smooth(T, 10**60)
    print(f"      T = {str(list(T)):18s} Sm(T) = {str(S)[:26]:26s} |Sm| = {len(S)}"
          f"   need 4 -> {'ALIVE' if len(S)>=4 else 'DEAD'}")
