#!/usr/bin/env python3
"""
Section 3 at k = 2, ALL sub-cases.

3 is ordinary, 3^2 || N, e_3 = 2.  The three "big" components are the special
p^e and the two notables n_1^{q_1}, n_2^{q_2}; each is either = 1 (mod 3) (and
then lies in T) or = 2 (mod 3) (and then lies in W).  With

    A = ordinary primes = 1 (mod 3)          |A| = alpha <= 2
    T = all primes = 1 (mod 3) dividing N    |T| = tau = alpha + beta,  13 in T
    W = big components = 2 (mod 3)           |W| = 3 - beta
    U = ordinary primes = 2 (mod 3)

the prime divisors of N are exactly {3} u T u W u U and

    (13/9) * PROD_T * PROD_W * PROD_U = 2,   i.e.  PROD_T*PROD_W*PROD_U = 18/13.

3-budget:  alpha + sum_{big in T} v_3 + sum_{w in W} d_w = 2, where d_w = 0 for
a notable = 2 (mod 3) and d_w = v_3(w+1) + v_3(e+1) >= 1 for the special.  Hence
    alpha + [special in W] <= 2.
Congruences: the special satisfies p = 1 (mod 4), so p = 1 (mod 12) if it is in
T and p = 5 (mod 12) if it is in W.

Exponent minima (sigma(t^k)/t^k increases with k):
    ordinary  exponent exactly 2        1 + 1/t + 1/t^2
    special   e >= 1                    1 + 1/t
    notable   q >= 4 even               1 + 1/t + ... + 1/t^4

TESTS (see 09_T5_unconditional.py for the tail lemma behind h):
  1  unconditional   minPROD_T * minPROD_W > 18/13
  2  unconditional   g(T) * h(T) * maxPROD_W <= 18/13,  g = prod t/(t-1)
  3  conditional     omega(N) >= 10 (Nielsen 2015) gives |U| >= 6 - alpha; U is inside
                     Sm(T) \ W and PROD_U <= R, so the (6-alpha) largest
                     members of Sm(T)\W must fit inside R.

W is enumerated over the primes = 2 (mod 3) below WB, each remaining slot being
an unknown prime >= WB (contributing 1 to minPROD_W and WB/(WB-1) to maxPROD_W).
A configuration survives only if NO test fires; a set T survives only if some
configuration survives.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import math, sys

def isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n-1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
WB   = 500
Y    = 10**24
TARGET = F(18, 13); TF = 18/13

def geom(t, k): return F(sum(t**i for i in range(k+1)), t**k)
f_ord  = lambda t: geom(t, 2)
f_spec = lambda t: geom(t, 1)
f_not  = lambda t: geom(t, 4)

def min_prod_T(T, alpha, sp_in_T, nt_in_T):
    """minimum of PROD_T over role assignments; None if none is admissible."""
    best = None
    roles = ['o']*alpha + (['s'] if sp_in_T else []) + ['n']*nt_in_T
    for perm in set(permutations(range(len(T)))):
        v = F(1); ok = True
        for r, i in zip(roles, perm):
            t = T[i]
            if r == 'o': v *= f_ord(t)
            elif r == 'n': v *= f_not(t)
            else:
                if t % 12 != 1: ok = False; break
                v *= f_spec(t)
        if ok and (best is None or v < best): best = v
    return best

def smooth_x(T):
    out = []; L = list(T)
    def rec(i, m):
        if i == len(L):
            d = 4*m - 3; r = math.isqrt(d)
            if r*r == d and r % 2 == 1:
                x = (r-1)//2
                if x >= 5 and x % 3 == 2 and isprime(x): out.append(x)
            return
        v = m
        while v <= Y:
            rec(i+1, v); v *= L[i]
    rec(0, 1)
    return sorted(set(out))

def tail_bound(T):
    best = None; lnY = math.log(Y)
    for k in range(1, 100):
        eps = 0.5*k/100.0
        if eps >= 0.5: break
        v = -eps*lnY
        for t in T: v -= math.log(1.0 - t**(eps-0.5))
        if best is None or v < best: best = v
    return math.exp(best)/(1 - Y**-0.5)

W_POOL = [p for p in range(5, WB) if isprime(p) and p % 3 == 2]
POOL   = [p for p in range(7, TMAX) if isprime(p) and p % 3 == 1]

def w_configs(m, sp_in_W):
    """(minPROD_W, maxPROD_W, explicit set) over W-configurations of size m."""
    out = []
    for k in range(m + 1):                      # k explicit, m-k unknown >= WB
        for combo in combinations(W_POOL, k):
            for sp_pos in (range(k) if sp_in_W else [None]):
                mn = F(1); mx = 1.0; bad = False
                for j, w in enumerate(combo):
                    if sp_in_W and j == sp_pos:
                        if w % 12 != 5: bad = True; break
                        mn *= f_spec(w)
                    else:
                        mn *= f_not(w)
                    mx *= w/(w-1.0)
                if bad: continue
                if sp_in_W and sp_pos is None and k == m: continue
                mx *= (WB/(WB-1.0)) ** (m - k)
                out.append((mn, mx, set(combo)))
            if sp_in_W and k < m:               # special is one of the unknowns
                mn = F(1); mx = 1.0
                for w in combo: mn *= f_not(w); mx *= w/(w-1.0)
                mx *= (WB/(WB-1.0)) ** (m - k)
                out.append((mn, mx, set(combo)))
    return out

print(f"pool T: primes = 1 mod 3 in [7,{TMAX}) : {len(POOL)}")
print(f"pool W: primes = 2 mod 3 in [5,{WB})   : {len(W_POOL)}   (slots above WB"
      f" cost {WB/(WB-1.0):.6f} each)")
print()
hdr = f"{'tau':>4} {'alpha':>6} {'sp':>3} {'#nt':>4} {'|W|':>4} {'sets':>7} " \
      f"{'uncond':>9} {'needs t3':>9} {'ALIVE':>7}"
print(hdr); print("-"*len(hdr))

smcache = {}
grand_alive = []
for alpha in (0, 1, 2):
    for sp_in_T in (0, 1):
        if alpha + (1 - sp_in_T) > 2: continue
        for nt_in_T in (0, 1, 2):
            tau = alpha + sp_in_T + nt_in_T
            if tau < 1 or tau > 5: continue
            m = 3 - sp_in_T - nt_in_T
            need_U = 6 - alpha
            wcfgs = w_configs(m, sp_in_W=(1 - sp_in_T))
            n_uncond = n_cond = 0; alive = []
            for rest in combinations([p for p in POOL if p != 13], tau - 1):
                T = tuple(sorted((13,) + rest))
                mp = min_prod_T(T, alpha, sp_in_T, nt_in_T)
                if mp is None: n_uncond += 1; continue
                if T not in smcache:
                    smcache[T] = (smooth_x(T), tail_bound(T))
                S, tb = smcache[T]
                g = 1.0
                for t in T: g *= t/(t-1.0)
                h0 = math.exp(1.000001*tb)
                survived = None; used_test3 = False
                for mn, mx, expl in wcfgs:
                    if mp * mn > TARGET: continue                      # test 1
                    Su = [x for x in S if x not in expl]
                    h = h0
                    for x in Su: h *= 1.0 + 1.0/x + 1.0/x**2
                    if g*h*mx <= TF: continue                          # test 2
                    used_test3 = True
                    R = TARGET/(mp*mn)
                    if len(Su) < need_U: continue                      # test 3
                    pr = F(1)
                    for x in Su[-need_U:]: pr *= f_ord(x)
                    if pr > R: continue                                # test 3
                    survived = (mn, mx, expl, Su, float(R)); break
                if survived is not None: alive.append((T, survived))
                elif used_test3: n_cond += 1
                else: n_uncond += 1
            tot = n_uncond + n_cond + len(alive)
            print(f"{tau:>4} {alpha:>6} {sp_in_T:>3} {nt_in_T:>4} {m:>4} {tot:>7} "
                  f"{n_uncond:>9} {n_cond:>9} {len(alive):>7}")
            for a in alive: grand_alive.append((tau, alpha, sp_in_T, nt_in_T, a))
print()
print(f"TOTAL surviving (T, configuration) pairs over the whole of section 3 "
      f"at k = 2 : {len(grand_alive)}")
for tau, alpha, sp, nt, (T, s) in grand_alive[:30]:
    print(f"   tau={tau} alpha={alpha} sp_in_T={sp} #nt_in_T={nt}  T={list(T)}  "
          f"W-explicit={sorted(s[2])}  Sm={s[3][:8]}  R={s[4]:.6f}")
