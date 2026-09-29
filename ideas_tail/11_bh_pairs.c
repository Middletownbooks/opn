/*
 * ideas_tail/11_bh_pairs.c -- how many Algorithm-1 survivors are "Bateman-Horn pairs":
 * primes r for which n = (r^2+r+1)/3^{[r = 1 mod 3]} is itself PRIME?
 *
 * Every such r is a survivor (n prime and > r, so no prime of M2 below r divides it),
 * and a survivor that is not a pair has a D-prime factor (a prime = 1 mod 3, > 3e6,
 * outside M2).  So  #pairs <= #survivors,  and the ratio says how close the survivor
 * set is to the pure 2-dimensional prime-pair problem (r, (r^2+r+1)/3^a).
 * Counts pairs and sum 1/r on (A, B]; compare with restrained/13's exact survivor counts.
 * Needs B^2 + B + 1 < 2^64.  Miller-Rabin with the first 12 prime bases is deterministic
 * below 3.18e23 (standard), so far beyond this range.
 *   gcc -O3 -o bh 11_bh_pairs.c -lm && ./bh A B
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 mulm(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powm(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulm(r, a, m); a = mulm(a, a, m); e >>= 1; } return r; }
static int isprime(u64 n) {
    static const u64 B[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    if (n < 2) return 0;
    for (int i = 0; i < 12; i++) if (n % B[i] == 0) return n == B[i];
    u64 d = n - 1; int s = 0; while (!(d & 1)) { d >>= 1; s++; }
    for (int i = 0; i < 12; i++) {
        u64 x = powm(B[i], d, n);
        if (x == 1 || x == n - 1) continue;
        int ok = 0;
        for (int j = 1; j < s; j++) { x = mulm(x, x, n); if (x == n - 1) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}
int main(int argc, char **argv) {
    u64 A = strtoull(argv[1], 0, 10), B = strtoull(argv[2], 0, 10);
    if ((long double)B * B + B + 1 > 1.8e19L) { fprintf(stderr, "B too large\n"); return 1; }
    u64 SQ = (u64)sqrtl((long double)B) + 2, SEG = 1 << 24;
    char *sm = calloc(SQ + 1, 1); for (u64 i = 2; i * i <= SQ; i++) if (!sm[i]) for (u64 j = i * i; j <= SQ; j += i) sm[j] = 1;
    char *seg = malloc(SEG); u64 np = 0, pairs = 0; long double s = 0;
    for (u64 lo = A + 1; lo <= B; lo += SEG) {
        u64 hi = lo + SEG - 1; if (hi > B) hi = B;
        memset(seg, 0, SEG);
        for (u64 p = 2; p <= SQ; p++) if (!sm[p]) {
            u64 st = (lo + p - 1) / p * p; if (st < p * p) st = p * p;
            for (u64 j = st; j <= hi; j += p) seg[j - lo] = 1;
        }
        for (u64 r = lo; r <= hi; r++) {
            if (seg[r - lo] || r < 2) continue;
            np++;
            u64 n = r * r + r + 1; if (r % 3 == 1) n /= 3;
            if (isprime(n)) { pairs++; s += 1.0L / r; }
        }
    }
    printf("(%llu, %llu]: primes %llu  pairs %llu (%.4f of primes)  sum 1/r over pairs %.12Lf\n",
           (unsigned long long)A, (unsigned long long)B, (unsigned long long)np, (unsigned long long)pairs,
           (double)pairs / np, s);
    return 0;
}
