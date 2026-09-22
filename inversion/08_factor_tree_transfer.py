#!/usr/bin/env python3
"""
What Ochem-Zelinsky's factor-tree prover (tree.cpp) does, why it closes
branches where my Lemma OC framework could not, and exactly why it does not
transfer to a general minimal-prime branch.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def order(a,l):
    a%=l; x,k=a,1
    while x!=1: x=(x*a)%l; k+=1
    return k
def factor(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f

print(__doc__)
print("="*74)
print("1. CORRECTION TO PROPOSITION D")
print("="*74)
print("""Proposition D showed Lemma OC can never block a SINGLE production.  I drew
the conclusion that the framework 'constrains but does not close'.  That was
too quick.  tree.cpp closes branches with the same kind of forcing, by
ITERATING it and terminating on one of three downstream contradictions:

  F t   a forced prime t is one already ruled out (in their driver: any prime
        smaller than the current root, valid because roots are processed in
        increasing order);
  XS t  three or more copies of a prime t are forced, while t is 'ordinary'
        (exponent 2) and can supply only two;
  a(.)>2  the partial product of EXACT component abundancies sigma(p^e)/p^e
        over the known components already exceeds 2.

So the correct statement is: no single production obligation is contradictory
(Proposition D stands), but the transitive closure of the obligations can be.
The framework of section 3 was missing the iteration and these three rules,
not the constraints.""")

print()
print("="*74)
print("2. THE TWO SOUND ABUNDANCY DIRECTIONS -- and Mantovanelli's is neither")
print("="*74)
print("""(i)  PARTIAL LOWER BOUND.  sigma(N)/N = prod_p sigma(p^{e_p})/p^{e_p} and every
     factor exceeds 1.  So if the partial product over KNOWN components
     already exceeds 2, N cannot be perfect.  Exact, finite, no classification
     needed.  This is tree.cpp's a(.) > 2 rule.

(ii) CLASSIFIED UPPER ENVELOPE.  Partition the unknown support into proved
     classes with proved per-class lower bounds that grow; if the resulting
     convergent product is < 2, contradiction.  This is Ochem-Zelinsky section 2.

Mantovanelli's tail envelope is neither: it is an upper bound over a FINITE
assumed slot count, which by Proposition A of the audit can hold only when the
branch is already empty.  Direction (i) would have been available to him for
free and needs no certificate at all.""")

print()
print("="*74)
print("3. WHY 17 SURVIVES AS A MINIMAL PRIME (and the tree's first step)")
print("="*74)
SMALL=[3,5,7,11,13]
print("Lower-prime avoidance at q=17 applied to the component 17^{e_17} itself.")
print("By Lemma 3.2, l | sigma(17^e) iff ord_l(17) | n (n = e+1), so with n odd:")
for l in SMALL:
    o=order(17,l)
    print(f"   ord_{l}(17) = {o:>2}  ({'even -> can never divide odd n' if o%2==0 else 'ODD -> binding'})")
print()
print("Every ord is even, so Forb(17) is empty: NO prime below 17 can ever divide")
print("sigma(17^{e_17}).  That is precisely why 17 is admissible as a least prime,")
print("and why the first-input split at q=17 has no extra constraint on e_17.")
print()
print("First step of the tree, taking the least admissible exponent e_17 = 2:")
s=17**2+17+1
print(f"   sigma(17^2) = {s}, prime? {isprime(s)}, and {s} mod 17 = {s%17}")
print(f"   so {s} | N.  Now the exponent of {s}:")
F=set()
for l in SMALL:
    o=order(s,l)
    if o==1: F.add(l)
    elif o%2==1: F.add(o)
    print(f"      ord_{l}({s}) = {o:>2}" + ("   -> forbids " + str(l if o==1 else o) if (o==1 or o%2==1) else ""))
print(f"   Forb({s}) = {sorted(F)}, so n_{s} is odd and not divisible by {sorted(F)}:")
n=3
while n%3==0 or n<3: n+=2
print(f"   least admissible n = {n}, i.e. e_{s} >= {n-1}.   (Corollary 2e in action.)")

print()
print("="*74)
print("4. WHY THE TREE DOES NOT TRANSFER TO A GENERAL MINIMAL-PRIME BRANCH")
print("="*74)
print("""tree.cpp branches on exactly two possibilities per prime x:
   ordinary:  e_x = 2, so sigma(x^2) = x^2 + x + 1, ONE number to factor;
   special:   the odd part of x+1, again ONE number.
That bounded branching is exactly what the RESTRAINED hypothesis buys: all
even exponents are 2 except one.

In a general minimal-prime branch no such bound exists.  e_x ranges over every
even number with n_x = e_x+1 odd and avoiding Forb(x), so sigma(x^{e_x}) is one
of infinitely many integers and the tree has infinite branching at every node.
Corollary 2e bounds e_x from BELOW, which makes the branching start later but
does not make it finite.

So the transfer needs an upper bound on exponents, which is the same missing
ingredient as everywhere else in this project: something that bounds the
support or the exponents from above.  Stated precisely, that is the obstruction.""")
