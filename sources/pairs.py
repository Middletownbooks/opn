# RECOVERED SOURCE -- see sources/README.md.  Supplied as a single-line
paste, so line breaks were reinserted mechanically at ';', '{', '}'.
The TOKEN SEQUENCE is verbatim; the layout is not the authors'.
import sys from fractions import Fraction import math import random  # ----------------------------------------------------------------------------- # 1. Fast Bitset Sieve for Primes up to Limit # ----------------------------------------------------------------------------- def sieve_primes(limit):     """Returns a bytearray bitset where bit p is 1 if p is prime."""     print(f"Pre-sieving primes up to {
limit}
...")     is_prime_bit = bytearray([1]) * ((limit // 2) + 1)     is_prime_bit[0] = 0 # 1 is not prime          for i in range(3, int(math.sqrt(limit)) + 1, 2):         if is_prime_bit[i // 2]:             is_prime_bit[(i*i) // 2 :: i] = b'\x00' * len(is_prime_bit[(i*i) // 2 :: i])                  return is_prime_bit  # ----------------------------------------------------------------------------- # 2. 64-bit Integer Utilities (Miller-Rabin & Pollard's Rho) # ----------------------------------------------------------------------------- def power_mod(base, exp, mod):     res = 1     base %= mod     while exp > 0:         if exp % 2 == 1: res = (res * base) % mod         base = (base * base) % mod         exp //= 2     return res  def gcd(a, b):     while b:         a, b = b, a % b     return a  def miller_rabin_64(n):     if n < 2: return False     if n in (2, 3): return True     if n % 2 == 0: return False     d = n - 1     s = 0     while d % 2 == 0:         d //= 2         s += 1     # Deterministic bases for up to 2^64     for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:         if n <= a: break         x = power_mod(a, d, n)         if x == 1 or x == n - 1: continue         composite = True         for _ in range(s - 1):             x = (x * x) % n             if x == n - 1:                 composite = False                 break         if composite: return False     return True  def pollard_rho_64(n):     if n % 2 == 0: return 2     x, y, d, c = 2, 2, 1, 1     f = lambda val: (val * val + c) % n     while d == 1:         x = f(x)         y = f(f(y))         d = gcd(abs(x - y), n)         if d == n:             x = random.randint(2, n - 1)             y = x             c = random.randint(1, n - 1)             d = 1     return d  def get_large_factors(n, factors_dict):     """Decomposes a large residual composite using Pollard's Rho."""     if n <= 1: return     if miller_rabin_64(n):         factors_dict[n] = factors_dict.get(n, 0) + 1         return     d = pollard_rho_64(n)     get_large_factors(d, factors_dict)     get_large_factors(n // d, factors_dict)  # ----------------------------------------------------------------------------- # 3. Main Sieve Engine # ----------------------------------------------------------------------------- def fast_search_minimum_x(limit):     is_prime_bit = sieve_primes(limit)          # Pre-calculate primes up to limit for trial divisions     primes = [2, 3]     for p_val in range(5, limit + 1, 2):         if is_prime_bit[p_val // 2]:             primes.append(p_val)                  print(f"Allocating tracking tables for polynomial factors...")     # Arrays to store the remaining unfactored part of (x^2 + x + 1)     # We only initialize entries where x = 5 mod 6 and x is prime     V_rem = {
}
factors_store = {
}
for x in range(5, limit + 1, 6):         if is_prime_bit[x // 2]:             V_rem[x] = x * x + x + 1             factors_store[x] = {
}
print("Sifting small prime divisors through the polynomial...")     # Sieve every prime q up to limit     for q in primes:         if q == 3:             continue # x^2+x+1 is never 0 mod 3 when x = 5 mod 6                      # We only care about primes q = 1 mod 3 (since x^2+x+1 = 0 mod q has roots iff q = 1 mod 3)         # Note: 2 is not 1 mod 3, so it naturally gets skipped here.         if q % 3 != 1:             continue                      # Find the two roots of x^2 + x + 1 = 0 mod q         # Expressed as x^2 + x + 1 = 0 -> (2x+1)^2 = -3 mod q         # We can find the modular square root of -3 mod q via power_mod since q = 1 mod 3         # However, it's faster to find valid coordinates across our active array using a direct scan          # for tiny primes, and fall back to algebraic roots for large primes.                  # Performance shortcut: Calculate starting points         # For small primes, direct stepping is faster         if q < 5000:             for x_start in range(5, limit + 1, 6):                 if (x_start * x_start + x_start + 1) % q == 0:                     # Found a root sequence offset, step by 6q                     step = 6 * q                     # Adjust first hit to line up with our sparse structure                     for x in range(x_start, limit + 1, q):                         if x in V_rem:                             count = 0                             while V_rem[x] % q == 0:                                 V_rem[x] //= q                                 count += 1                             if count > 0:                                 factors_store[x][q] = count                     break         else:             # For larger primes, dynamically check hits as they appear during structural loops             pass      print("Cleaning up cofactors and processing large prime residuals...")     min_x_dict = {
}
def register(a, b, x, p, n):         sig = (a, b)         if sig not in min_x_dict:             min_x_dict[sig] = (x, p, n)      # Final pass: check entries, run Pollard's rho on huge residual components     for x in sorted(V_rem.keys()):         rem = V_rem[x]         factors = factors_store[x]                  # If there is an unfactored large prime tail left over         if rem > 1:             get_large_factors(rem, factors)                      # Process signature rules exactly like the original script         if len(factors) == 1:             q, e = list(factors.items())[0]             if q % 12 == 1:                 register(e, 0, x, q, None)                 register(0, e, x, None, q)             elif q % 12 == 7:                 register(0, e, x, None, q)          elif len(factors) == 2:             (q1, e1), (q2, e2) = list(factors.items())             if q1 % 12 == 1: register(e1, e2, x, q1, q2)             if q2 % 12 == 1: register(e2, e1, x, q2, q1)      return min_x_dict  if __name__ == "__main__":     if len(sys.argv) != 2:         print(f"Usage: python3 {
sys.argv[0]}
<search_limit>")         sys.exit(1)      search_limit = int(sys.argv[1])     results = fast_search_minimum_x(search_limit)      print(f"\n{
'Sig (a,b)':<12}
| {
'Min x':<8}
| {
'p':<12}
| {
'n':<12}
| {
'Abundancy H(x^2)'}
")     print("-" * 65)      sorted_sigs = sorted(results.keys(), key=lambda k: (k[0]+k[1], k[0]))     total_abundancy = Fraction(13, 12) * Fraction(7, 6)      for a, b in sorted_sigs:         if (a > 1 and b == 0) or (a == 0 and b > 1):             continue          x, p, n = results[(a, b)]         h_x_exact = Fraction(x, x-1)         total_abundancy *= h_x_exact          p_str = str(p) if p else "-"         n_str = str(n) if n else "-"         print(f"p^{
a}
* n^{
b:<5}
| {
x:<8}
| {
p_str:<12}
| {
n_str:<12}
| {
float(h_x_exact):.6f}
")      print("-" * 65)     base_abundancy = Fraction(13, 12) * Fraction(7, 6)     print(f"Base H(p)*H(n): {
float(base_abundancy):.6f}
(Exact: {
base_abundancy}
)")     print(f"Cumulative max: {
float(total_abundancy):.6f}
(Exact: {
total_abundancy}
)")
