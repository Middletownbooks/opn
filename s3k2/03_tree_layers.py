#!/usr/bin/env python3
"""
The section 3 opening tree, done correctly.

SEMANTICS.  Assume 3 is ordinary, so e_3 = 2 and at most two copies of 3 may be
produced; each ordinary prime = 1 (mod 3) produces exactly one.  A forced prime
takes a role: ordinary (forcing the factors of sigma(x^2)), special (only once,
needs x = 1 mod 4, forcing the odd part (x+1)/2), or NOTABLE -- in which case
the chain STOPS there, since sigma(n^q) is not determined.

If we assume NO prime is notable, the tree must close by XS 3.  The primes it
reaches are exactly the candidates for the notable prime.  At k = 1 that IS the
paper's set S.

At k = 2 a second layer is needed: fix one candidate as the first notable, stop
the chain there, and re-run.  If the tree still closes, a SECOND notable is
forced, and it lies in the set the re-run reaches.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def factor(n):
    f=set(); d=2
    while d*d<=n:
        while n%d==0: f.add(d); n//=d
        d+=1
    if n>1: f.add(n)
    return f

LIM=10**18
def explore(stopped=frozenset()):
    """primes reachable assuming every prime outside `stopped` is ordinary or
    special; returns (reached, closed) where closed means every branch died."""
    reached=set(); open_branches=[0]
    def go(x, spec_used, threes, path):
        reached.add(x)
        if x in stopped: return True        # notable: chain stops, branch alive
        alive=False
        t=threes+(1 if x%3==1 else 0)
        if t<=2:                            # ordinary role admissible
            v=x*x+x+1
            while v%3==0: v//=3
            if v>LIM: open_branches[0]+=1; alive=True
            else:
                for r in sorted(factor(v)):
                    if r==3 or r in path: continue
                    if go(r, spec_used, t, path|{x}): alive=True
                if not factor(v)-{3}-path: alive=True
        if not spec_used and x%4==1:        # special role admissible
            w=(x+1)//2
            if w>LIM: open_branches[0]+=1; alive=True
            else:
                fs=sorted(r for r in factor(w) if r not in (2,3) and r not in path)
                if not fs: alive=True
                for r in fs:
                    if go(r, True, threes, path|{x}): alive=True
        return alive
    alive=go(13, False, 0, frozenset({3}))
    return reached, (not alive), open_branches[0]

S,closed,op = explore()
print("LAYER 1  (no notable anywhere)")
print(f"   primes reached : {sorted(S)}")
print(f"   tree closes    : {closed}   (open branches: {op})")
print(f"   paper's set S  : [7, 13, 19, 31, 61, 97, 127, 331]")
print(f"   reproduced     : {sorted(S)==[7,13,19,31,61,97,127,331]}")
print()
print("So at ANY k >= 1, at least one of these eight primes is notable.")
print()
print("LAYER 2  (one candidate fixed as the first notable, chain stopped there)")
print(f"{'first notable':>14} {'tree still closes?':>20} {'second-notable candidates':>46}")
layer2={}
for s in sorted(S):
    R,cl,o = explore(frozenset({s}))
    layer2[s]=(R,cl)
    cand = sorted(R-{s})
    print(f"{s:>14} {str(cl):>20} {str(cand)[:46]:>46}")
print()
allclosed=all(cl for _,cl in layer2.values())
print(f"   every layer-2 tree still closes: {allclosed}")
if allclosed:
    print("""
   => at k = 2, for EACH choice of the first notable from S, the tree still
   dies, so a SECOND notable is forced, and it must lie in the listed set.
   That gives an explicit finite list of admissible notable PAIRS.""")
    pairs=sorted((s,t) for s in S for t in sorted(layer2[s][0]-{s}) if t>s or True)
    uniq=sorted({tuple(sorted((s,t))) for s in S for t in layer2[s][0]-{s}})
    print(f"   distinct unordered pairs {{n_1, n_2}} admissible: {len(uniq)}")
    print(f"   {uniq}")
