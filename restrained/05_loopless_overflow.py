#!/usr/bin/env python3
"""
Audit of loopless.cpp (Ochem-Zelinsky's Algorithm 1 implementation).

The sieve's central test is check_M2:

    bool check_M2(u64 r, const PrimeSet& M2) {
        u64 val = r * r + r + 1;          // <-- 64-bit arithmetic
        if (val % 3 == 0) val /= 3;
        std::vector<u64> factors;
        get_factors(val, factors);
        for (u64 p : factors) if (M2.count(p)) return false;
        return true;
    }

`r` and `val` are u64.  The file defines u128 and uses it inside power_mod and
pollard_rho for modular multiplication, but NOT here: `r * r` is evaluated in
64-bit arithmetic and wraps modulo 2^64.
"""
M = 1 << 64
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
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
import random, math
def rho(n):
    if n%2==0: return 2
    while True:
        x=random.randrange(2,n); y=x; c=random.randrange(1,n); d=1
        while d==1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n
            d=math.gcd(abs(x-y),n)
        if d!=n: return d
def factor(n,out=None):
    if out is None: out={}
    if n<=1: return out
    if isprime(n): out[n]=out.get(n,0)+1; return out
    d=rho(n); factor(d,out); factor(n//d,out); return out

print(__doc__)
print(f"2^64 = {M}")
print(f"r*r + r + 1 first reaches 2^64 at r = 2^32 = {1<<32}")
print()
print("The paper's run reaches z = 216,171,986,291, about 50x past that point.")
print("So the overflow affects essentially the whole sieve range.")
print()
print("Demonstration on the first few primes above 2^32:")
print(f"{'r':>14} {'true r^2+r+1':>26} {'as computed (mod 2^64)':>26} {'same?':>6}")
rs=[]
r=(1<<32)+1
while len(rs)<4:
    if isprime(r): rs.append(r)
    r+=2
for r in rs:
    t=r*r+r+1; w=t % M
    print(f"{r:>14} {t:>26} {w:>26} {str(t==w):>6}")
print()
print("Factorisations of the true value vs the wrapped value, and the effect on")
print("the sieve's verdict.  M2 at that stage contains every prime = 1 mod 3 up")
print("to 3,000,000 (plus primes added later); here we test membership against")
print("that initial set, which is enough to show the verdict can flip.")
print()
def m2_hit(v):
    if v % 3 == 0: v //= 3
    f = factor(v)
    return sorted(p for p in f if p < 3_000_000 and p % 3 == 1)
print(f"{'r':>14} {'verdict on TRUE value':>34} {'verdict on WRAPPED value':>34}")
flips=0
for r in rs:
    t=r*r+r+1; w=t % M
    ht, hw = m2_hit(t), m2_hit(w)
    vt = 'can be ordinary' if not ht else f'excluded by {ht[:2]}'
    vw = 'can be ordinary' if not hw else f'excluded by {hw[:2]}'
    if (not ht) != (not hw): flips += 1
    print(f"{r:>14} {vt:>34} {vw:>34}")
print()
print(f"verdict flips among these {len(rs)} primes: {flips}")
print("""
ASSESSMENT.  Separately from the wrap, get_factors takes a u64, so even with
correct arithmetic it could not hold r^2+r+1 ~ 4.7e22 for r ~ 2.2e11.  The
released file therefore cannot perform the advertised computation beyond
r = 2^32, whatever the wrap does.

Most likely explanations, in order: (a) the published run used a 128-bit or GMP
variant not in the released file; (b) the released file is an earlier draft;
(c) the reported z is affected.  I cannot distinguish these from the source
alone, and (a) is the most probable -- the file already defines u128 and links
GMP.  This should be checked with the authors rather than asserted as an error
in the paper.

Direction of risk, if the released file IS what was run: a wrapped value gives
essentially random factors, so verdicts flip both ways.  Wrongly INCLUDING a
prime as ordinary inflates the abundancy A and is conservative; wrongly
EXCLUDING one deflates A and would make the resulting bound unsound.  Both
occur, so the run could not be relied on as stated.""")
