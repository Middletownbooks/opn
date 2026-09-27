"""
High-precision helpers for the audit, standard library only (decimal + ints).

Written independently of s3k2/39: arctan by argument halving + Taylor series,
pi by Machin, Eisenstein-prime splitting by brute force on a^2 - ab + b^2 = t.
"""
from decimal import Decimal as Dm, getcontext, localcontext
import math

def set_prec(digits):
    getcontext().prec = digits

def pi_dec():
    """Machin: pi = 16 atan(1/5) - 4 atan(1/239)."""
    with localcontext() as ctx:
        ctx.prec += 10
        def atan_inv(n):
            x = Dm(1) / n; x2 = x * x; s = x; term = x; k = 1
            eps = Dm(10) ** (-(ctx.prec + 2))
            while True:
                term = -term * x2
                k += 2
                d = term / k
                if abs(d) < eps: break
                s += d
            return s
        r = 16 * atan_inv(5) - 4 * atan_inv(239)
    return +r

def atan_dec(u):
    """arctan(u) for Decimal u, any sign."""
    with localcontext() as ctx:
        ctx.prec += 10
        u = Dm(u)
        if u < 0: return -atan_dec(-u)
        halvings = 0
        # atan(u) = 2 atan(u / (1 + sqrt(1+u^2)))
        while u > Dm("0.01"):
            u = u / (1 + (1 + u * u).sqrt()); halvings += 1
        x2 = u * u; s = u; term = u; k = 1
        eps = Dm(10) ** (-(ctx.prec + 2))
        while True:
            term = -term * x2; k += 2
            d = term / k
            if abs(d) < eps: break
            s += d
        r = s * (2 ** halvings)
    return +r

def atan2_dec(y, x):
    y = Dm(y); x = Dm(x); P = pi_dec()
    if x > 0: return atan_dec(y / x)
    if x < 0: return atan_dec(y / x) + (P if y >= 0 else -P)
    return P / 2 if y > 0 else -P / 2

def eisenstein_prime(t):
    """(a, b) with a^2 - a b + b^2 = t, i.e. N(a + b w) = t, w = e^{2 pi i/3}."""
    r = int(math.isqrt(4 * t // 3)) + 2
    for a in range(-r, r + 1):
        for b in range(-r, r + 1):
            if a * a - a * b + b * b == t:
                return a, b
    raise ValueError(t)

def arg_pi_over_pibar(t):
    """
    theta_t = principal Arg(pi_t / conj(pi_t)) in (-pi, pi], for the associate
    pi_t of smallest |theta| (units change theta by multiples of 2pi/3).
    pi = a + b w = (a - b/2) + i b sqrt3/2.
    """
    a, b = eisenstein_prime(t)
    s3 = Dm(3).sqrt(); P = pi_dec()
    best = None
    # the six associates: multiply by powers of -w
    z = (a, b)
    for _ in range(6):
        a1, b1 = z
        ang = 2 * atan2_dec(b1 * s3 / 2, Dm(a1) - Dm(b1) / 2)
        while ang > P: ang -= 2 * P
        while ang <= -P: ang += 2 * P
        if best is None or abs(ang) < abs(best[0]): best = (ang, z)
        # multiply a + b w by -w: -(a w + b w^2) = -(a w + b(-1 - w)) = b + (b - a) w
        z = (b1, b1 - a1)
    return best

def is_square(n):
    if n < 0: return False
    r = math.isqrt(n); return r * r == n
