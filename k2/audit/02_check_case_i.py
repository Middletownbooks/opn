#!/usr/bin/env python3
"""Audit step 2: the weighted fixed-support bound for case (i).
Everything recomputed in exact rationals."""
from fractions import Fraction as Fr
def F(s): return s*s+s+1
def isprime(n):
    if n<2: return False
    if n%2==0: return n==2
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True

print("A. The exclusion table: is F(u) < M < F(u+1) in every row?")
tab=[(217,14),(247,15),(259,15),(403,19),(589,23),(637,24),(1147,33),(1183,33),
     (1519,38),(1729,41),(2527,49),(2821,52),(3211,56),(4459,66),(5239,71),
     (6727,81),(12493,111),(15379,123)]
bad=[(M,u) for M,u in tab if not (F(u)<M<F(u+1))]
print(f"   rows checked {len(tab)}, failures {len(bad)} {bad if bad else ''}")
print("   composite-s exclusions: "
      f"91=F(9) s=9 composite {not isprime(9)}; 931=F(30) {F(30)==931 and not isprime(30)}; "
      f"4693=F(68) {F(68)==4693 and not isprime(68)}")
print(f"   8281 = 91^2 a square, and F(s) is never a square: "
      f"{F(90)<8281<F(91)}")

print("\nB. The X_r upper bounds for r^{-1/2}")
X={7:Fr(378,1000),13:Fr(278,1000),19:Fr(230,1000),31:Fr(180,1000),
   37:Fr(165,1000),43:Fr(153,1000),61:Fr(129,1000)}
okX=all(x*x*r>1 for r,x in X.items())
for r,x in X.items():
    print(f"   r={r:>3}: X={float(x):.3f},  r*X^2 = {float(r*x*x):.6f} > 1 ? {r*x*x>1}")
print(f"   all valid: {okX}")

def H(x,y,z): return (x*y+x*z+y*z-2*x*y*z)/((1-x)(1-y)(1-z)) if False else \
                     (x*y+x*z+y*z-2*x*y*z)/((1-x)*(1-y)*(1-z))
def H2(x,y,z): return x*y+x*z+y*z
def H3(x,y,z): return (x+y+z)*(x*y+x*z+y*z)-2*x*y*z

rows=[
 (1,"S={7,13,19}",(7,13,19),"H2+H3",Fr(11,10),Fr(18,100),True),
 (2,"S={7,13,31}",(7,13,31),"H2+H3",Fr(5,4),Fr(14,100),True),
 (3,"S={7,13,q>=37}",(7,13,37),"xy(1+x+y+x2+xy+y2)",Fr(17,16),Fr(35,100),False),
 (4,"S={7,19,p>=37}",(7,19,37),"xy(x+y)",Fr(59,58),Fr(42,100),False),
 (5,"S={7,31,37}",(7,31,37),"H2",Fr(5,4),Fr(19,100),False),
 (6,"S={7,31,p>=61}",(7,31,61),"xy(1+x+y)",Fr(5,4)*Fr(59,58),Fr(20,100),False),
 (7,"7 in S; 13,19,31 not",(7,37,43),"0",Fr(17,16)*Fr(59,58),Fr(33,100),False),
 (8,"7 not in S, 5 not ord",(13,19,31),"0",Fr(17,16)**2*Fr(59,58),Fr(34,100),False),
 (9,"7 not, 5 ord, S={13,19,31}",(13,19,31),"H2",Fr(5,4),Fr(16,100),False),
 (10,"7 not, 5 ord, S={13,31,q>=37}",(13,31,37),"xy",Fr(5,4)*Fr(17,16),Fr(19,100),False),
 (11,"7,13 not, 5 ord",(19,31,37),"0",Fr(5,4)*Fr(17,16)*Fr(59,58),Fr(20,100),False),
]
def E(t): return 1+t+t*t/(2*(1-t/3))

print("\nC. Per-row verification  (R = H - P,  d = 1-2xy or 1-2x^3y,  need R/d <= L)")
print(f"{'row':>3} {'R':>10} {'d':>10} {'R/d':>10} {'L':>6} {'R/d<=L':>7} "
      f"{'A*B':>8} {'E(L)':>7} {'product':>9} {'<2':>5}")
allok=True
for n,name,(r1,r2,r3),Pname,B,L,deg4 in rows:
    x,y,z=X[r1],X[r2],X[r3]
    h=H(x,y,z)
    if Pname=="H2+H3": P=H2(x,y,z)+H3(x,y,z)
    elif Pname=="H2": P=H2(x,y,z)
    elif Pname=="xy": P=x*y
    elif Pname=="xy(x+y)": P=x*y*(x+y)
    elif Pname=="xy(1+x+y)": P=x*y*(1+x+y)
    elif Pname=="xy(1+x+y+x2+xy+y2)": P=x*y*(1+x+y+x*x+x*y+y*y)
    else: P=Fr(0)
    R=h-P
    d=(1-2*x**3*y) if deg4 else (1-2*x*y)
    ok1 = R/d <= L
    AB=Fr(r1,r1-1)*Fr(r2,r2-1)*Fr(r3,r3-1)*B
    prod=AB*E(L)
    ok2 = prod<2
    allok &= ok1 and ok2
    print(f"{n:>3} {float(R):>10.5f} {float(d):>10.5f} {float(R/d):>10.5f} {float(L):>6.2f} "
          f"{str(ok1):>7} {float(AB):>8.4f} {float(E(L)):>7.4f} {float(prod):>9.5f} {str(ok2):>5}")
print(f"\n   every row satisfies R/d <= L and A*B*E(L) < 2 :  {allok}")
print(f"   largest product across rows: {max(float(Fr(r1,r1-1)*Fr(r2,r2-1)*Fr(r3,r3-1)*B*E(L)) for n,nm,(r1,r2,r3),Pn,B,L,dg in rows):.5f}")
