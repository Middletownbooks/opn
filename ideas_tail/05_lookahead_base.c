/*
 * ideas_tail/05_lookahead_base.c -- exact Algorithm 1 PLUS the depth-1 look-ahead
 * without the special branch, applied to every survivor in a range [LA_LO, LA_HI).
 *
 * Derived from restrained/13_sieve.c (a copy; the original is unchanged).  The
 * Algorithm-1 part (M1, M2, survivors, k, ln A) is IDENTICAL to 13 in exact mode
 * (Q = Z_END): the look-ahead never feeds back into M2.  Added:
 *
 *  (a) D-primes.  A prime q = 1 (mod 3), q > 3e6, that does NOT join M2 (a survivor,
 *      or a special candidate) is a "D-prime".  Its two root classes are tracked like
 *      M2's, but a hit multiplies a per-position product dprod[] instead of marking.
 *  (b) The big factor.  For a survivor r, every prime factor of n = r^2+r+1 below r is
 *      3 or a D-prime (M2 primes cannot divide it; primes = 2 mod 3 never divide it;
 *      primes < 3e6 that are = 1 mod 3 are in M2).  Divide n by 3^{[r=1 mod 3]} and by
 *      every power of the D-primes in dprod.  The cofactor C has no prime factor < r,
 *      and C <= n < (r+1)^2, so C = 1 or C is a prime P > r.  No factoring needed.
 *  (c) The test.  P ordinary  =>  no prime of M2 divides P^2+P+1.  We test against the
 *      M2 primes q < YS (from a file written by 03_state.py, or the initial M2 below
 *      3e6 if no file is given): P^2+P+1 = 0 (mod q) iff P = rho_q or q-1-rho_q.
 *      If some q hits, r is not ordinary unless P is the special prime -- which is
 *      possible for at most TWO r in all (RESULT.md, Idea 3).  Such r are dropped
 *      from the look-ahead set; the two exceptions are added back in the bound.
 *
 *   gcc -O3 -march=native -o la 05_lookahead_base.c -lm
 *   ./la Z_END LA_LO LA_HI [M2FILE YS]
 *
 * OUTPUT.  "CP" lines: x, k(x) and ln A(x) of Algorithm 1 (compare with 13), and
 * kLA, lnALA: the same over survivors in [LA_LO, min(x, LA_HI)) that pass the test,
 * plus nsurv/nP/nfail in the range.  C, standard library only.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

#define LO 3000000ULL
#define CHLOG 22
#define CH (1ULL << CHLOG)             /* odd numbers per chunk */
#define SPAN (2 * CH)                  /* integers per chunk */
#define SMALLQ SPAN                    /* q < SMALLQ: swept directly */

static u64 ZEND, QLIM;
static int PROGRESS;

static u64 powmod(u64 a, u64 e, u64 m) {
    u64 r = 1; a %= m;
    while (e) { if (e & 1) r = (u64)((u128)r * a % m); a = (u64)((u128)a * a % m); e >>= 1; }
    return r;
}
static u64 cube_root(u64 q) {          /* a primitive cube root of unity mod q, q = 1 mod 3 */
    for (u64 g = 2;; g++) { u64 x = powmod(g, (q - 1) / 3, q); if (x != 1) return x; }
}
/* smallest odd t > n with t = c (mod q) */
static u64 next_odd_hit(u64 n, u64 c, u64 q) {
    u64 t = n - n % q + c;
    if (t <= n) t += q;
    if (!(t & 1)) t += q;
    return t;
}

/* ---- survivors s = 1 (mod 6), s <= ZEND/2+1, as a FIFO queue ----
   They are pushed in increasing order, and queried in increasing order of
   s = (r+1)/2, which always lies below the current r.  So a queue with a forward-only
   read pointer answers "is s a survivor?" exactly, and consumed blocks are freed.
   Memory is the survivors in (r/2, r], not all of them up to ZEND/2. */
#define QB (1 << 20)
typedef struct QBlk { struct QBlk *next; u64 n; u64 v[QB]; } QBlk;
static QBlk *QH, *QT; static u64 QHI; static u64 SLIM;
static inline void s_set(u64 s) {
    if (!QT || QT->n == QB) {
        QBlk *b = malloc(sizeof(QBlk)); if (!b) { fprintf(stderr, "oom queue\n"); exit(2); }
        b->next = 0; b->n = 0;
        if (QT) QT->next = b; else QH = b;
        QT = b;
    }
    QT->v[QT->n++] = s;
}
static inline int s_get(u64 s) {
    for (;;) {
        if (!QH) return 0;
        if (QHI < QH->n) {
            if (QH->v[QHI] < s) { QHI++; continue; }
            return QH->v[QHI] == s;
        }
        if (QH == QT) return 0;                  /* all consumed; more may come later */
        QBlk *nx = QH->next; free(QH); QH = nx; QHI = 0;
    }
}

/* ---- small M2 list ---- */
static u64 *sq, *sn1, *sn2; static uint8_t *sdf; static size_t ns, cs;
static void small_push(u64 q, u64 t1, u64 t2, int dflag) {
    if (ns == cs) { cs = cs ? 2 * cs : 1 << 16;
        sq = realloc(sq, cs * 8); sn1 = realloc(sn1, cs * 8); sn2 = realloc(sn2, cs * 8); sdf = realloc(sdf, cs);
        if (!sq || !sn1 || !sn2) { fprintf(stderr, "oom small\n"); exit(2); } }
    sq[ns] = q; sn1[ns] = t1; sn2[ns] = t2; sdf[ns] = (uint8_t)dflag; ns++;
}

/* ---- buckets: entry = (q << CHLOG) | offset; bucket index = chunk mod NB ----
   A bucket is a linked list of fixed-size blocks drawn from a shared free pool, so
   memory tracks the live entries (one per q), not each slot's historical peak. */
#define BLK 8190
typedef struct Block { struct Block *next; u64 n; u64 v[BLK]; } Block;
static Block **BK; static u64 NB; static Block *FREE; static u64 NBLOCKS;
static inline Block *balloc(void) {
    Block *b = FREE;
    if (b) FREE = b->next;
    else { b = malloc(sizeof(Block)); if (!b) { fprintf(stderr, "oom block\n"); exit(2); } NBLOCKS++; }
    b->next = 0; b->n = 0; return b;
}
#define DFLAG (1ULL << 63)
static inline void bpush(u64 chunk, u64 q, u64 off) {
    Block **h = &BK[chunk % NB];
    if (!*h || (*h)->n == BLK) { Block *b = balloc(); b->next = *h; *h = b; }
    (*h)->v[(*h)->n++] = (q << CHLOG) | off;
}
static inline void bpushd(u64 chunk, u64 q, u64 off) {   /* a D-prime entry */
    Block **h = &BK[chunk % NB];
    if (!*h || (*h)->n == BLK) { Block *b = balloc(); b->next = *h; *h = b; }
    (*h)->v[(*h)->n++] = DFLAG | (q << CHLOG) | off;
}
static u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }

/* static M2 list for the look-ahead test: q, rho_q, 2^64 mod q, and Lemire-Kaser-Kurz
   "direct remainder" multipliers (Software: Practice and Experience 49, 2019):
   for d < 2^32,  a mod d = floor(((M*a mod 2^F) * d) / 2^F)  with M = floor((2^F-1)/d) + 1,
   exact for all a < 2^(F/2).  F = 128 for 64-bit a, F = 64 for 32-bit a. */
static u64 *tq, *trho, *t64, *tm32; static u128 *tm64; static size_t ntq;
static inline u64 fmod64(u64 a, u128 M, u64 d) {
    u128 low = M * a; u64 lo = (u64)low, hi = (u64)(low >> 64);
    u128 t = (u128)lo * d; u128 u = (u128)hi * d + (t >> 64);
    return (u64)(u >> 64);
}
static inline u64 fmod32(u64 a, u64 M, u64 d) { return (u64)(((u128)(M * a) * d) >> 64); }
static int la_fails_slow(u128 P) {           /* reference: plain division */
    u64 hi = (u64)(P >> 64), lo = (u64)P;
    for (size_t j = 0; j < ntq; j++) {
        u64 q = tq[j];
        u64 r = ((hi % q) * t64[j] % q + lo % q) % q;
        if (r == trho[j] || r == q - 1 - trho[j]) return 1;
    }
    return 0;
}
static int la_fails(u128 P) {                /* 1 if some listed q divides P^2+P+1 */
    u64 hi = (u64)(P >> 64), lo = (u64)P;    /* P < 2^70, q < 2^24: hi*t64 + r1 < 2^31 */
    for (size_t j = 0; j < ntq; j++) {
        u64 q = tq[j];
        u64 r = fmod32(hi * t64[j] + fmod64(lo, tm64[j], q), tm32[j], q);
        if (r == trho[j] || r == q - 1 - trho[j]) return 1;
    }
    return 0;
}
static int LA_CHECK;

/* next hit of q after the hit n (n = c mod q for one root c) */
static inline u64 advance(u64 n, u64 q) {
    u64 rho = n % q, other = q - 1 - rho;
    u64 a = n + 2 * q, b = next_odd_hit(n, other, q);
    return a < b ? a : b;
}


int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s Z_END LA_LO LA_HI [M2FILE YS]\n", argv[0]); return 1; }
    ZEND = strtoull(argv[1], 0, 10); QLIM = ZEND + 1;          /* exact mode only */
    u64 LA_LO = strtoull(argv[2], 0, 10), LA_HI = strtoull(argv[3], 0, 10);
    PROGRESS = 0; LA_CHECK = getenv("LA_CHECK") != 0;
    if (QLIM > (1ULL << (63 - CHLOG)) - 1) { fprintf(stderr, "Z_END too large for packing\n"); return 1; }
    if (ZEND > 4000000000000ULL) { fprintf(stderr, "Z_END too large: P must stay below 2^128\n"); return 1; }
    time_t t0 = time(0);

    /* sieving primes up to sqrt(ZEND), and primes below LO */
    u64 SQ = (u64)sqrtl((long double)ZEND) + 2, PL = LO > SQ ? LO : SQ;
    uint8_t *ip = calloc(PL + 1, 1); for (u64 i = 2; i <= PL; i++) ip[i] = 1;
    for (u64 i = 2; i * i <= PL; i++) if (ip[i]) for (u64 j = i * i; j <= PL; j += i) ip[j] = 0;
    u64 *sp = 0, *spn = 0; size_t nsp = 0;
    for (u64 p = 3; p <= SQ; p++) if (ip[p]) nsp++;
    sp = malloc(nsp * 8); spn = malloc(nsp * 8); nsp = 0;
    for (u64 p = 3; p <= SQ; p++) if (ip[p]) {
        u64 m = p * p; u64 lo1 = LO + 1;
        if (m < lo1) { m = (lo1 + p - 1) / p * p; if (!(m & 1)) m += p; }
        sp[nsp] = p; spn[nsp] = m; nsp++;
    }

    /* the static M2 list for the test */
    {   u64 YS = LO; uint8_t *st = 0;
        if (argc > 5) {
            YS = strtoull(argv[5], 0, 10);
            FILE *f = fopen(argv[4], "rb"); if (!f) { fprintf(stderr, "no M2 file\n"); return 1; }
            st = malloc(YS); if (fread(st, 1, YS, f) != YS) { fprintf(stderr, "short M2 file\n"); return 1; }
            fclose(f);
        }
        if (YS > (1ULL << 24)) { fprintf(stderr, "YS must be below 2^24 for the fast remainder\n"); return 1; }
        tq = malloc(YS / 3 * 8 + 64); trho = malloc(YS / 3 * 8 + 64); t64 = malloc(YS / 3 * 8 + 64);
        tm32 = malloc(YS / 3 * 8 + 64); tm64 = malloc(YS / 3 * 16 + 64);
        for (u64 q = 7; q < YS; q++) {
            if (q % 3 != 1) continue;
            int in = st ? (st[q] == 4 || st[q] == 1) : (q < LO && ip[q]);
            if (!in) continue;
            tq[ntq] = q; trho[ntq] = cube_root(q); t64[ntq] = (u64)(((u128)1 << 64) % q);
            tm32[ntq] = UINT64_MAX / q + 1; tm64[ntq] = (~(u128)0) / q + 1; ntq++;
        }
        free(st);
        fprintf(stderr, "static M2 test list: %zu primes below %llu\n", ntq, (unsigned long long)YS);
    }

    SLIM = ZEND / 2 + 1;
    NB = QLIM / CH + 4; if (NB < 4) NB = 4;
    BK = calloc(NB, sizeof(Block *)); if (!BK) { fprintf(stderr, "oom BK\n"); return 2; }

    /* initial M2: primes 7 <= q < 3e6, q = 1 mod 3 */
    u64 m2 = 0, m2big = 0, nd = 0;
    for (u64 q = 7; q < LO; q++) if (ip[q] && q % 3 == 1) {
        u64 c = cube_root(q);
        small_push(q, next_odd_hit(LO, c, q), next_odd_hit(LO, q - 1 - c, q), 0); m2++;
    }
    free(ip);

    /* checkpoints: every 1e8 below 1e9, every 1e9 above */
    u64 *cps = malloc((ZEND / 100000000ULL + 16) * 8); int ncp = 0;
    for (u64 x = 100000000ULL; x < ZEND && x < 1000000000ULL; x += 100000000ULL) cps[ncp++] = x;
    for (u64 x = 1000000000ULL; x < ZEND; x += 1000000000ULL) cps[ncp++] = x;
    cps[ncp++] = ZEND;
    int icp = 0;

    uint8_t *comp = malloc(CH), *hit = malloc(CH);
    u128 *dprod = malloc(CH * sizeof(u128));
    u64 k = 0; long double acc = 0.0L, cmp = 0.0L;
    u64 kla = 0, nsurv = 0, nP = 0, nfail = 0; long double la = 0.0L, lcmp = 0.0L;
    u64 base = LO;
    u64 nchunks = (ZEND - LO) / SPAN + 1;
#define ADDLOG(A, C, term) do { long double t_ = (A) + (term); \
        if (fabsl(A) >= fabsl(term)) (C) += ((A) - t_) + (term); else (C) += ((term) - t_) + (A); (A) = t_; } while (0)
#define PRINTCP(x) printf("CP x=%llu k=%llu lnA=%.21Lg kLA=%llu lnALA=%.21Lg nsurv=%llu nP=%llu nfail=%llu m2=%llu nd=%llu\n", \
        (unsigned long long)(x), (unsigned long long)k, acc + cmp, (unsigned long long)kla, la + lcmp, \
        (unsigned long long)nsurv, (unsigned long long)nP, (unsigned long long)nfail, (unsigned long long)m2, (unsigned long long)nd)
    for (u64 ci = 0; ci < nchunks; ci++, base += SPAN) {
        u64 end = base + SPAN;
        memset(comp, 0, CH); memset(hit, 0, CH); memset(dprod, 0, CH * sizeof(u128));
        for (size_t j = 0; j < nsp; j++) {
            u64 m = spn[j], p2 = 2 * sp[j];
            for (; m < end; m += p2) comp[(m - base - 1) >> 1] = 1;
            spn[j] = m;
        }
        for (size_t j = 0; j < ns; j++) {
            u64 q2 = 2 * sq[j], t;
            if (!sdf[j]) {
                for (t = sn1[j]; t < end; t += q2) hit[(t - base - 1) >> 1] = 1;
                sn1[j] = t;
                for (t = sn2[j]; t < end; t += q2) hit[(t - base - 1) >> 1] = 1;
                sn2[j] = t;
            } else {
                u64 q = sq[j]; u128 *d;
                for (t = sn1[j]; t < end; t += q2) { d = &dprod[(t - base - 1) >> 1]; *d = *d ? *d * q : q; }
                sn1[j] = t;
                for (t = sn2[j]; t < end; t += q2) { d = &dprod[(t - base - 1) >> 1]; *d = *d ? *d * q : q; }
                sn2[j] = t;
            }
        }
        {   Block *b = BK[ci % NB]; BK[ci % NB] = 0;
            while (b) {
                for (u64 e = 0; e < b->n; e++) {
                    u64 v = b->v[e]; int isd = (v & DFLAG) != 0; v &= ~DFLAG;
                    u64 q = v >> CHLOG, off = v & (CH - 1);
                    u64 n = base + 2 * off + 1;
                    for (;;) {
                        if (isd) { u128 *d = &dprod[(n - base - 1) >> 1]; *d = *d ? *d * q : q; }
                        else hit[(n - base - 1) >> 1] = 1;
                        n = advance(n, q);
                        if (n >= end) break;
                    }
                    u64 c2 = (n - LO - 1) / SPAN;
                    if (c2 % NB == ci % NB) { fprintf(stderr, "bucket wrap\n"); return 3; }
                    if (isd) bpushd(c2, q, ((n - LO - 1) % SPAN) >> 1);
                    else bpush(c2, q, ((n - LO - 1) % SPAN) >> 1);
                }
                Block *nx = b->next; b->next = FREE; FREE = b; b = nx;
            }
        }
        for (u64 i = 0; i < CH; i++) {
            u64 n = base + 2 * i + 1;
            if (n > ZEND) break;
            while (icp < ncp && cps[icp] < n) { PRINTCP(cps[icp]); fflush(stdout); icp++; }
            if (comp[i]) continue;
            int joins_m2 = 0;
            if (!hit[i]) {
                k++;
                long double term = log1pl(1.0L / (long double)(n - 1));
                ADDLOG(acc, cmp, term);
                if (n % 6 == 1 && n <= SLIM) s_set(n);
                if (n >= LA_LO && n < LA_HI) {
                    nsurv++;
                    u128 N = (u128)n * n + n + 1;
                    if (n % 3 == 1) N /= 3;
                    u128 m = dprod[i];
                    if (m) for (;;) { u128 g = gcd128(N, m); if (g == 1) break; N /= g; }
                    int keep = 1;
                    if (N > 1) {
                        if (N <= n) { fprintf(stderr, "cofactor <= r at r=%llu\n", (unsigned long long)n); return 4; }
                        nP++;
                        if (N >> 70) { fprintf(stderr, "P too large at r=%llu\n", (unsigned long long)n); return 4; }
                        int f = la_fails(N);
                        if (LA_CHECK && f != la_fails_slow(N)) { fprintf(stderr, "fast/slow mismatch at r=%llu\n", (unsigned long long)n); return 5; }
                        if (f) { keep = 0; nfail++; }
                    }
                    if (keep) { kla++; ADDLOG(la, lcmp, term); }
                }
            } else if (n % 3 == 1 && (n % 4 == 3 || !s_get((n + 1) / 2))) {
                joins_m2 = 1;
                m2++;
                u64 c = cube_root(n), c2 = n - 1 - c;
                u64 t1 = next_odd_hit(n, c, n), t2 = next_odd_hit(n, c2, n);
                if (n < SMALLQ) {
                    u64 q2 = 2 * n;
                    for (; t1 < end; t1 += q2) hit[(t1 - base - 1) >> 1] = 1;
                    for (; t2 < end; t2 += q2) hit[(t2 - base - 1) >> 1] = 1;
                    small_push(n, t1, t2, 0);
                } else {
                    u64 t = t1 < t2 ? t1 : t2;
                    while (t < end) { hit[(t - base - 1) >> 1] = 1; t = advance(t, n); }
                    bpush((t - LO - 1) / SPAN, n, ((t - LO - 1) % SPAN) >> 1);
                }
            }
            if (n % 3 == 1 && !joins_m2 && n < LA_HI) {       /* a D-prime: track its root classes */
                nd++;
                u64 c = cube_root(n), c2 = n - 1 - c;
                u64 t1 = next_odd_hit(n, c, n), t2 = next_odd_hit(n, c2, n);
                if (n < SMALLQ) {
                    u64 q2 = 2 * n; u128 *d;
                    for (; t1 < end; t1 += q2) { d = &dprod[(t1 - base - 1) >> 1]; *d = *d ? *d * n : n; }
                    for (; t2 < end; t2 += q2) { d = &dprod[(t2 - base - 1) >> 1]; *d = *d ? *d * n : n; }
                    small_push(n, t1, t2, 1);
                } else {
                    u64 t = t1 < t2 ? t1 : t2;
                    while (t < end) { u128 *d = &dprod[(t - base - 1) >> 1]; *d = *d ? *d * n : n; t = advance(t, n); }
                    bpushd((t - LO - 1) / SPAN, n, ((t - LO - 1) % SPAN) >> 1);
                }
            }
        }
        if ((ci & 1023) == 1023) {
            fprintf(stderr, "[%lds] r ~ %.4e  k = %llu  lnA = %.12Lf  kLA = %llu lnALA = %.12Lf  blocks = %llu (%.2f GB)\n",
                    (long)(time(0) - t0), (double)end, (unsigned long long)k, acc + cmp, (unsigned long long)kla, la + lcmp,
                    (unsigned long long)NBLOCKS, NBLOCKS * (double)sizeof(Block) / 1e9);
        }
    }
    while (icp < ncp) { if (cps[icp] <= ZEND) PRINTCP(cps[icp]); icp++; }
    printf("SUMMARY ZEND=%llu LA=[%llu,%llu) YS_list=%zu k=%llu lnA=%.21Lg kLA=%llu lnALA=%.21Lg nsurv=%llu nP=%llu nfail=%llu seconds=%ld\n",
           (unsigned long long)ZEND, (unsigned long long)LA_LO, (unsigned long long)LA_HI, ntq, (unsigned long long)k, acc + cmp,
           (unsigned long long)kla, la + lcmp, (unsigned long long)nsurv, (unsigned long long)nP, (unsigned long long)nfail,
           (long)(time(0) - t0));
    return 0;
}
