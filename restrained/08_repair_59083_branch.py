#!/usr/bin/env python3
"""
Repair of the one broken cut in 3p2.txt.

The file's line

    59083^2 => 3 19 6604392133    F 19

cuts the branch because 19 is forced and 19 was ruled out earlier.  But 19 does
not divide sigma(59083^2): the true value is 3 * 18433 * 63127.  So that cut is
unjustified as written.

CLAIM.  The branch closes anyway, by XS 3 rather than F 19, so the conclusion
of 3p2.txt (that 659 is ruled out) survives.

SETTING.  Section 3 of the paper: N restrained odd perfect, 3 ordinary, so
3^2 || N and e_3 = 2 exactly.  The opening factor tree of section 3 shows the
notable prime lies in S = {7, 13, 19, 31, 61, 97, 127, 331}.  On this branch
the special prime is 33457.

ARGUMENT.
  1. Along the path, two copies of 3 are already forced, and e_3 = 2, so the
     budget is exactly exhausted: no further copy of 3 may be produced.
  2. 18433 and 63127 both divide N.  Neither is in S, so neither is notable;
     the special prime on this branch is 33457, so neither is special.  Hence
     both are ORDINARY.
  3. Both are 1 mod 3, so each contributes a further copy of 3.
  4. That is a third (and fourth) copy against a budget of 2.  XS 3.
"""
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True
def v3(n):
    v=0
    while n%3==0: n//=3; v+=1
    return v
def sig2(x): return x*x+x+1

S_NOTABLE = {7, 13, 19, 31, 61, 97, 127, 331}
print(__doc__)
print("Step 0 - the path, re-derived from scratch:")
chain = [("659^2", sig2(659), "13 * 33457"),
         ("33457+1 (special)", 33457+1, "2 * 16729"),
         ("16729^2", sig2(16729), "3 * 1579 * 59083"),
         ("59083^2", sig2(59083), "3 * 18433 * 63127")]
vals = {"13 * 33457": 13*33457, "2 * 16729": 2*16729,
        "3 * 1579 * 59083": 3*1579*59083, "3 * 18433 * 63127": 3*18433*63127}
for name, got, claim in chain:
    print(f"   {name:<22} = {got:>12}   = {claim:<22} {'OK' if got==vals[claim] else 'MISMATCH'}")
print()
print("Step 1 - copies of 3 forced along the path (e_3 = 2, since 3 is ordinary):")
tot=0
for x in (659, 16729, 59083):
    v = v3(sig2(x))
    tot += v
    print(f"   v_3(sigma({x}^2)) = {v}     ({x} = {x%3} mod 3)")
print(f"   total so far = {tot}, budget e_3 = 2  ->  budget exactly exhausted")
print()
print("Step 2 - status of the two new primes:")
for x in (18433, 63127):
    print(f"   {x}: prime = {isprime(x)}, in notable set S = {x in S_NOTABLE}, "
          f"is the branch's special prime (33457) = {x == 33457}")
print("   => neither can be notable or special, so BOTH are ordinary.")
print()
print("Step 3 - each ordinary one forces another copy of 3:")
for x in (18433, 63127):
    print(f"   {x} = {x%3} mod 3, so v_3(sigma({x}^2)) = {v3(sig2(x))}")
print()
extra = v3(sig2(18433)) + v3(sig2(63127))
print(f"Step 4 - total copies of 3 forced = {tot} + {extra} = {tot+extra}, against e_3 = 2.")
print(f"         {tot+extra} > 2  ->  XS 3.  The branch closes.")
print()
print("""CONCLUSION.  The cut at this line is valid, but the reason is XS 3, not
F 19.  659 remains ruled out and 3p2.txt's conclusion is unaffected.  Only one
marker in the file needs changing -- assuming the file really reads as the
transcription does, which remains the likelier thing to check first.""")
