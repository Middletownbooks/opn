#!/usr/bin/env python3
"""
Independent check of Zelinsky (arXiv:1706.07009v3) Theorem 1, case 3 does not
divide N:  Omega(N) >= (8/3) omega(N) - 7/3.

The paper derives it as an explicit nonnegative linear combination of its
numbered relations.  We reconstruct the combination symbolically and confirm
the resulting inequality.  Variables are counts; each relation is put in the
form  EXPR >= 0  (or EXPR = 0 for the definitional equalities).
"""
from fractions import Fraction as F
from collections import defaultdict

V = ['e','f3','f4','s','s1','s2','s3','s21','s22','s31','s32','t','om','OM','ONE']
def lin(**kw):
    d = defaultdict(F)
    for k,v in kw.items(): d[k] += F(v)
    return d
def add(a,b,c=1):
    c=F(c); out=defaultdict(F,a)
    for k,v in b.items(): out[k]+=c*v
    return out
def show(d):
    return ' + '.join(f"{v}*{k}" for k,v in sorted(d.items()) if v) or '0'

# Relations, each as EXPR >= 0 (ineq) or EXPR == 0 (eq).
R = {
 5:  lin(e=1, ONE=-1),                                    # 1 <= e
 6:  lin(s1=1, s2=1, s3=1, s=-1),                          # s = s1+s2+s3      (eq)
 7:  lin(s21=1, s22=1, s2=-1),                             # s2 = s21+s22      (eq)
 8:  lin(s31=1, s32=1, s3=-1),                             # s3 = s31+s32      (eq)
 9:  lin(OM=1, e=-1, f3=-1, s=-2, f4=-1),                  # e+f3+2s+f4 <= Om
 10: lin(t=1, s21=1, s31=1, ONE=1, s1=-1, s22=-1),         # s1+s22 <= t+s21+s31+1
 11: lin(t=1, s31=1, ONE=1, s1=-1),                        # s1 <= t+s31+1
 12: lin(f3=1, s21=-1, s31=-1),                            # s21+s31 <= f3
 13: lin(f4=1, e=1, s21=1, s1=-1, s22=-2, s32=-3),         # (13)
 14: lin(f4=1, t=-4),                                      # 4t <= f4
 15: lin(s=1, t=1, ONE=1, om=-1),                          # om = s+t+1        (eq)
}
COMB = {5:'7/9', 6:'2/3', 7:'2/3', 8:'2/3', 9:'1', 10:'4/9', 13:'2/9', 14:'7/9', 15:'8/3'}

print(__doc__)
print("Case 3 does not divide N: the paper sets f3 = 0, hence s21 = s31 = 0.")
print("Stated combination:", ' + '.join(f"{c} x ({n})" for n,c in COMB.items()))
print()
tot = defaultdict(F)
for n,c in COMB.items():
    tot = add(tot, R[n], c)
for z in ('f3','s21','s31'):          # zeroed in this case
    tot[z] = F(0)
tot = defaultdict(F, {k:v for k,v in tot.items() if v})
print("Sum of the combination:")
print("   ", show(tot))
print()
target = lin(OM=1, om=F(-8,3), ONE=F(7,3))   # Omega - (8/3)omega + 7/3 >= 0
print("Target  Omega - (8/3) omega + 7/3 >= 0, i.e.")
print("   ", show(target))
print()
# Correct test: does  target - combination  have only NONNEGATIVE coefficients on
# the (nonnegative) count variables?  If so, target >= combination >= 0.
gap = add(target, tot, -1)
gap = defaultdict(F, {k:v for k,v in gap.items() if v})
print("target - combination =", show(gap) or '0')
neg = {k:v for k,v in gap.items() if v < 0 and k != 'ONE'}
if not gap:
    print("=> combination reproduces the target exactly.  VERIFIED.")
elif not neg:
    print("=> every leftover term has a nonnegative coefficient on a nonnegative")
    print("   count, so target >= combination >= 0.  VERIFIED.")
    print("   In fact the combination proves the slightly STRONGER bound")
    print("   Omega >= (8/3) omega - 7/3 + " + show(gap) + ".")
else:
    print("=> MISMATCH: negative coefficients remain on", sorted(neg))

print()
print("="*72)
print("CASE 3 | N:  Omega >= (21/8) omega - 39/8")
print("="*72)
R[16] = lin(s=1, t=1, ONE=2, om=-1)          # om = s + t + 2
COMB2 = {5:'3/4', 6:'5/8', 7:'5/8', 8:'5/8', 9:'1', 10:'1/8', 11:'1/4',
         12:'1', 13:'1/4', 14:'3/4', 16:'21/8'}
print("Stated combination:", ' + '.join(f"{c} x ({n})" for n,c in COMB2.items()))
tot2 = defaultdict(F)
for n,c in COMB2.items(): tot2 = add(tot2, R[n], c)
tot2 = defaultdict(F, {k:v for k,v in tot2.items() if v})
print("Sum:", show(tot2))
target2 = lin(OM=1, om=F(-21,8), ONE=F(39,8))
print("Target:", show(target2))
gap2 = add(target2, tot2, -1)
gap2 = defaultdict(F, {k:v for k,v in gap2.items() if v})
print("target - combination =", show(gap2) or '0')
neg2 = {k:v for k,v in gap2.items() if v < 0 and k != 'ONE'}
const = gap2.get('ONE', F(0))
print()
if not neg2 and const >= 0:
    print("=> VERIFIED (target >= combination >= 0).")
elif not neg2 and const < 0:
    print(f"=> leftover constant {const} is negative; the paper also records 2 <= f3.")
    extra = add(gap2, lin(f3=1, ONE=-2), 0)
    need = -const / 2
    print(f"   Adding {need} x (2 <= f3), i.e. {need}*(f3 - 2) >= 0, requires an f3")
    print(f"   coefficient of at least {need}; available f3 coefficient is {gap2.get('f3',F(0))}.")
    if gap2.get('f3', F(0)) >= need:
        print("   => VERIFIED using 2 <= f3.")
    else:
        print("   => could not close with 2 <= f3 alone.")
else:
    print("=> MISMATCH: negative coefficients on", sorted(neg2))
