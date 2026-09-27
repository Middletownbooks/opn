// RECOVERED SOURCE -- see sources/README.md
// Ochem & Zelinsky, arXiv:2607.19746, implementation of their Algorithm 1.
// Supplied by the user as a single-line paste; newlines below were reinserted
// mechanically at ';', '{' and '}', so INDENTATION AND LINE BREAKS ARE NOT THE
// AUTHORS'.  The token sequence is verbatim.  Audited in restrained/05 and
// NOTES_RESTRAINED.md 4b (64-bit overflow in r*r past r = 2^32).
// g++ -O3 -o loopless loopless.cpp -lgmp
#include <iostream>
#include <vector>
#include <gmp.h>
#include <stdlib.h>
#include <time.h>
#include <cstdint>
using namespace std;

  typedef unsigned __int128 u128;
typedef uint64_t u64;
// --------------------------------------------------------- // Fast Bitset for storing primes (O(1) lookup) // --------------------------------------------------------- class PrimeSet {
std::vector<u64> bitset;
public:     void insert(u64 p) {
u64 idx = p / 64;
if (idx >= bitset.size()) bitset.resize(idx + 10000, 0);
// dynamically grow         bitset[idx] |= (1ULL << (p % 64));
}
bool count(u64 p) const {
u64 idx = p / 64;
if (idx >= bitset.size()) return false;
return (bitset[idx] & (1ULL << (p % 64))) != 0;
}
}
;
// --------------------------------------------------------- // Math & Factoring Utility Functions // --------------------------------------------------------- u64 power_mod(u64 base, u64 exp, u64 mod) {
u64 res = 1;
base %= mod;
while (exp > 0) {
if (exp % 2 == 1) res = (u64)((u128)res * base % mod);
base = (u64)((u128)base * base % mod);
exp /= 2;
}
return res;
}
bool miller_rabin(u64 n) {
u64 d = n - 1;
int s = 0;
while (d % 2 == 0) {
d /= 2;
s++;
}
// Bases for deterministic primality test up to 2^64     static const u64 bases[] = {
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
;
for (u64 a : bases) {
if (n <= a) break;
u64 x = power_mod(a, d, n);
if (x == 1 || x == n - 1) continue;
bool composite = true;
for (int r = 1;
r < s;
r++) {
x = (u64)((u128)x * x % n);
if (x == n - 1) {
composite = false;
break;
}
}
if (composite) return false;
}
return true;
}
u64 my_gcd(u64 a, u64 b) {
while (b) {
a %= b;
std::swap(a, b);
}
return a;
}
// Fast 64-bit factorization using Pollard's Rho u64 pollard_rho(u64 n) {
u64 x = 2, y = 2, d = 1, c = 1;
auto f = [&](u64 x, u64 n, u64 c) {
return (u64)(((u128)x * x + c) % n);
}
;
while (d == 1) {
x = f(x, n, c);
y = f(f(y, n, c), n, c);
d = my_gcd(x > y ? x - y : y - x, n);
if (d == n) {
x = rand() % (n - 2) + 2;
y = x;
c = rand() % (n - 1) + 1;
d = 1;
}
}
return d;
}
void get_factors(u64 n, std::vector<u64>& factors) {
if (n <= 1) return;
// Trial division for speed on small components     static const u64 small_primes[] = {
5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97}
;
for (u64 p : small_primes) if (n % p == 0) {
factors.push_back(p);
while (n % p == 0) n /= p;
}
if (n == 1) return;
if (miller_rabin(n)) {
factors.push_back(n);
return;
}
u64 divisor = pollard_rho(n);
get_factors(divisor, factors);
get_factors(n / divisor, factors);
}
u64 next_prime(u64 n) {
n += (n % 2 == 0) ? 1 : 2;
while (!miller_rabin(n)) n += 2;
return n;
}
// --------------------------------------------------------- // Sieve Check Logic  // --------------------------------------------------------- bool check_M1(u64 r, const PrimeSet& M1) {
if (r % 4 == 3) return true;
u64 val = (r + 1)/2;
std::vector<u64> factors;
get_factors(val, factors);
for (u64 p : factors) if (M1.count(p)) return true;
return false;
}
bool check_M2(u64 r, const PrimeSet& M2) {
u64 val = r * r + r + 1;
if(val%3 == 0) val /= 3;
std::vector<u64> factors;
get_factors(val, factors);
for (u64 p : factors) if (M2.count(p)) return false;
// Found a forbidden factor     return true;
}
// --------------------------------------------------------- // Main Sieve  // --------------------------------------------------------- int main(int argc, char* argv[]) {
srand(time(NULL));
mpf_set_default_prec(300);
// Maintained for flawless precision of 'A'      PrimeSet M1, M2;
mpf_t A, term;
mpf_inits(A, term, NULL);
// Initialize M1 and M2     for(u64 q = 5;
q <= 3000000;
q = next_prime(q)){
M1.insert(q);
if(q % 3 == 1) M2.insert(q);
}
unsigned long long k = 0;
u64 r = next_prime(3000000);
u64 last_r = r;
mpf_set_ui(A, 1);
for(;
;
r = next_prime(r)) if (check_M2(r, M2)) {
// r can be ordinary, update A and k         mpf_set_ui(term, r);
mpf_mul(A, A, term);
mpf_sub_ui(term, term, 1);
mpf_div(A, A, term);
k++;
last_r = r;
if (k % 10000 == 0) gmp_printf("k: %-8llu | r: %-10llu | A: %.12Ff\n", k, r, A);
}
else {
// r is not ordinary, so either r \nmid N or r is special.         M1.insert(r);
if (r % 3 == 1 && check_M1(r, M1)) M2.insert(r);
// r is ruled out, so r is added to M2     }
return 0;
}

