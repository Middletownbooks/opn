# Auditor's own prover for "prime r in [11,3e6] cannot divide a restrained OPN with notable prime 3".
# Written from the paper's description (sec. 1, 4), not from tree.cpp or 15_tree_pilot.py.
import sys, math, random, time
LIM = 3_000_000
sv = bytearray([1])*(LIM+1); sv[:2]=b"\0\0"
for i in range(2, math.isqrt(LIM)+1):
    if sv[i]: sv[i*i::i] = bytearray(len(range(i*i, LIM+1, i)))
SMALL = [p for p in range(2, 2000) if sv[p]]
def isprime(n):
    if n <= LIM: return n >= 2 and bool(sv[n])
    for p in SMALL[:15]:
        if n % p == 0: return False
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
class GiveUp(Exception): pass
def rho(n, budget=3_000_000):
    rng = random.Random(n ^ 12345)
    it = 0
    while True:
        c = rng.randrange(1, n); x = y = rng.randrange(2, n); d = 1; q = 1
        while d == 1:
            ys = []
            for _ in range(100):
                x = (x*x + c) % n; y = (y*y + c) % n; y = (y*y + c) % n
                q = q * abs(x - y) % n
            it += 100
            d = math.gcd(q, n)
            if it > budget: raise GiveUp(n)
        if d != n: return d
def primes_of(n):
    out = set()
    for p in SMALL:
        if n % p == 0:
            out.add(p)
            while n % p == 0: n //= p
    st = [n]
    while st:
        v = st.pop()
        if v == 1: continue
        if isprime(v): out.add(v); continue
        d = rho(v); st += [d, v//d]
    return out
def refuted(root, x, path, special_taken, cnt):
    """True iff 'x | N' is impossible given that every prime on path divides N and
    (if special_taken) the special prime is on the path."""
    cnt[0] += 1
    if cnt[0] > 5000: raise GiveUp("nodes")
    branches = []
    if not special_taken and x % 12 == 1:          # x special: p = 1 mod 4 (Euler), p = 1 mod 3 (Lemma 6)
        branches.append(((x + 1) // 2, True))       # e odd => x+1 | sigma(x^e) | 2N
    G = x*x + x + 1                                 # x ordinary => x^2+x+1 | 2N
    if G % 3 == 0: G //= 3                          # 3 = notable prime, not a contradiction
    branches.append((G, special_taken))
    newpath = path | {x}
    for val, sp in branches:
        fs = [f for f in primes_of(val) if f >= 5]
        if any(f < root for f in fs): continue      # f already ruled out
        if any(f not in newpath and refuted(root, f, newpath, sp, cnt) for f in sorted(fs)): continue
        return False                                # this status of x is not contradicted
    return True
if __name__ == "__main__":
    seed, n = int(sys.argv[1]), int(sys.argv[2]); extra = [int(a) for a in sys.argv[3:]]
    allp = [p for p in range(11, LIM) if sv[p]]
    roots = sorted(set(random.Random(seed).sample(allp, n)) | set(extra))
    ok = 0; gave = []; opn = []; t0 = time.time()
    for r in roots:
        try:
            if refuted(r, r, frozenset(), False, [0]): ok += 1
            else: opn.append(r)
        except GiveUp as g: gave.append(r)
    print(f"my prover: roots={len(roots)} ruled_out={ok} open={opn} gave_up={gave} secs={time.time()-t0:.0f}")
