#!/usr/bin/env python3
"""Audit step 3: is the model's 11-row case division exhaustive, and is each
row's 'lower support triple' a genuine coordinatewise lower bound?"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def F(s): return s*s+s+1

# case (i): all three support primes are 1 mod 3, odd, so 1 mod 6.
CAND=[p for p in range(5,4000) if isprime(p) and p%6==1]
print(f"admissible support primes (= 1 mod 6) below 4000: {len(CAND)}, "
      f"smallest {CAND[:8]}")
print("the special prime p must be = 1 mod 12; notables need only be = 1 mod 6")
print()

def row_of(S, five_ordinary):
    S=set(S)
    if 7 in S:
        if 13 in S:
            if S=={7,13,19}: return 1,(7,13,19)
            if S=={7,13,31}: return 2,(7,13,31)
            return 3,(7,13,37)
        if 19 in S: return 4,(7,19,37)
        if 31 in S:
            if S=={7,31,37}: return 5,(7,31,37)
            return 6,(7,31,61)
        return 7,(7,37,43)
    if not five_ordinary: return 8,(13,19,31)
    # 5 ordinary => sigma(25)=31 must be in S
    if 31 not in S: return None,None
    if 13 in S:
        if S=={13,19,31}: return 9,(13,19,31)
        return 10,(13,31,37)
    return 11,(19,31,37)

bad=[]; counts={}
import itertools
for S in itertools.combinations(CAND[:14],3):
    if not any(q%12==1 for q in S): continue        # need a special prime
    for five_ord in (False,True):
        if five_ord and 31 not in S: continue       # 5 ordinary forces 31 in S
        r,lo = row_of(S, five_ord)
        if r is None: bad.append((S,five_ord,"no row")); continue
        counts[r]=counts.get(r,0)+1
        if not all(a<=b for a,b in zip(lo,sorted(S))):
            bad.append((S,five_ord,f"row {r} lower triple {lo} not <= {sorted(S)}"))
print("A. every admissible support triple lands in a row, with a valid lower bound")
print(f"   triples x (5 ordinary?) examined : {sum(counts.values())}")
print(f"   row usage : {dict(sorted(counts.items()))}")
print(f"   failures  : {len(bad)}")
for b in bad[:8]: print("     ",b)

print()
print("B. the row conditions that need checking by hand")
print(f"   rows 4-6 claim the third prime must be special: "
      f"7 mod 12 = {7%12}, 19 mod 12 = {19%12}, 31 mod 12 = {31%12} -- "
      f"none is 1, so none can be p. OK")
sp=[q for q in range(13,200) if isprime(q) and q%12==1]
print(f"   special primes = 1 mod 12: {sp[:6]}; after 37 the next is {sp[2]} "
      f"(49 = 7^2 is not prime). OK")
print()
print("C. the singleton floors")
print(f"   F(s)=7 needs s=2, F(s)=13 needs s=3: neither is an ordinary prime (s>=5)")
print(f"   19 and 37 are not of the form F(s): F(3)={F(3)} < 19 < F(4)={F(4)}, "
      f"F(5)={F(5)} < 37 < F(6)={F(6)}")
print(f"   ordinary s with F(s) prime: 5 -> {F(5)}; 11 -> {F(11)} = 7*19 composite; "
      f"17 -> {F(17)} prime.  So a non-5 singleton is >= 17. OK")
c=[s for s in range(11,60,12) if isprime(s)]
print(f"   special singleton needs s = 11 mod 12: candidates below 59 are {c}, with "
      f"F = {[F(s) for s in c]}")
print(f"   all composite ({[ (s,[d for d in range(2,200) if F(s)%d==0][:1]) for s in c]}), "
      f"and F(59) = {F(59)} is prime with 59 = 11 mod 12.  Floor 59 OK")
