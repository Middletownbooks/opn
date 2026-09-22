from fractions import Fraction
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
print("=== CERTIFIED MINIMAL-PRIME SUPPORT FLOOR  k0(q) ===")
print("If N is odd perfect and q=min{p:p|N}, then prod_{p|N} p/(p-1) > sigma(N)/N = 2.")
print("Maximising that product over omega(N)=k primes all >= q takes the k smallest such")
print("primes. So omega(N) >= k0(q) := least k with prod of k smallest primes >=q  > 2.")
print()
print(f"{'q':>4} {'k0(q)':>7} {'prod over k0-1 primes (<=2)':>30} {'prod over k0 primes (>2)':>28} {'largest prime':>14}")
for q in (3,5,7,11,13,17,19,23):
    v=Fraction(1);k=0;p=q;last=0
    prev=None
    while v<=2:
        while not isprime(p): p+=2
        prev=v
        v*=Fraction(p,p-1);k+=1;last=p;p+=2
    print(f"{q:>4} {k:>7} {float(prev):>30.10f} {float(v):>28.10f} {last:>14}")
print()
print("(Exact rational arithmetic; the k0-1 product is <=2 and the k0 product is >2.)")
print()
print("=== Independent check of the Phi_5(x)/5 forced-prime lemma used by the q=5 layer ===")
print("Claim: x prime, x==1 mod 5; every prime r | Phi_5(x)/5 satisfies r==1 mod 5, so r>=11.")
print("Hand proof: r | Phi_5(x) => x^5==1 mod r => ord_r(x) in {1,5}.")
print("  If ord_r(x)=1 then x==1 mod r so Phi_5(x)=x^4+x^3+x^2+x+1==5 mod r, forcing r=5.")
print("  So r!=5 => ord_r(x)=5 => 5 | r-1 => r==1 mod 5 => r>=11.")
print("  LTE: v_5(x^5-1)=v_5(x-1)+1 when x==1 mod 5, and Phi_5(x)=(x^5-1)/(x-1), so v_5(Phi_5(x))=1.")
print("Numerical spot check:")
def factor(n):
    f=[];d=2
    while d*d<=n:
        while n%d==0: f.append(d); n//=d
        d+=1
    if n>1: f.append(n)
    return f
bad=0
for x in [11,31,41,61,71,101,131,181,191,211,241,251,271,281,311,331,401,421,431,461,491,521,541,571,601,631,641,661,691,701,751,761,811,821,881,911,941,971,991,1021,1031,1051,1061,1091,1151,1171,1181,1201,1231,1291,1301,1321,1361,1381]:
    if not (isprime(x) and x%5==1): continue
    P=x**4+x**3+x**2+x+1
    assert P%5==0 and (P//5)%5!=0, f"v_5 wrong at x={x}"
    C=P//5
    for r in set(factor(C)):
        if r%5!=1 or r<11:
            bad+=1; print(f"   COUNTEREXAMPLE x={x} r={r}")
print(f"   checked 54 primes x==1 mod 5 up to 1381: violations = {bad}")
print("   also confirmed v_5(Phi_5(x))=1 in every case -> lemma holds as stated.")
