/*
 * restrained/13_sieve.c -- an independent, overflow-free run of Ochem-Zelinsky's
 * Algorithm 1 (sources/ochem_zelinsky_algorithm1.txt).
 *
 * C, standard library only (it uses GCC's unsigned __int128 for 64x64-bit modular
 * products; that is a compiler type, not a library).  It shares no code with
 * sources/loopless.cpp.  It never forms r^2+r+1, so nothing can overflow.
 *
 *   gcc -O3 -march=native -o sieve 13_sieve.c -lm
 *   ./sieve Z_END Q [progress]
 *
 * WHAT IT COMPUTES.  Algorithm 1 over the primes 3e6 < r <= Z_END, EXCEPT that a
 * prime q of M2 is used to exclude r only when q < Q.  Two cases:
 *   * Q >= Z_END: this is Algorithm 1 exactly.
 *   * Q <  Z_END: it is exact for r <= Q.  Above Q it keeps a SUPERSET of Algorithm
 *     1's survivors.  By induction on r: an r excluded here has a factor in
 *     M2' (restricted to q < Q), and M2' is inside M2, so r is excluded by
 *     Algorithm 1 too.  So the survivors S' contain S, M1' = non-survivors lies
 *     inside M1, and M2' (built from M1') lies inside M2.
 *   Either way S' contains every prime in (3e6, Z_END] that can be ordinary.
 *   That is all the section-4 count needs (restrained/10, item 5).
 *
 * HOW.
 *   * q in M2 divides r^2+r+1  <=>  r = rho or q-1-rho (mod q), where rho is a
 *     primitive cube root of unity mod q.  Each q in M2 marks its hits r > q.  It
 *     does so through a "small" list (q < SMALLQ: every chunk is swept with stride
 *     2q per root), or through buckets.  A bucket holds ONE entry per q: the
 *     smallest pending hit over both roots; the next hit is recomputed from the
 *     current one.
 *   * The test "some prime factor of r+1 other than 2, 3 lies in M1", for
 *     r = 1 (mod 12), is a single lookup.  Let s = (r+1)/2; it is = 1 (mod 6).  If
 *     s has a prime factor below 3e6, that factor is in M1 (the initial M1 is every
 *     prime 5 <= p < 3e6).  Otherwise, because s < 9e12, s is itself a prime > 3e6,
 *     and it is in M1 iff it did not survive.  So:
 *         r joins M2  <=>  r = 3 (mod 4), or s is not a survivor.
 *     Survivors = 1 (mod 6) up to Z_END/2 are kept in a FIFO queue; the queries
 *     (r+1)/2 only increase, so consumed entries are freed.
 *   * The primes r come from a segmented sieve of Eratosthenes over odd numbers.
 *   * ln A = sum over survivors of log1p(1/(r-1)), accumulated in long double with
 *     Neumaier compensation.
 *
 * OUTPUT.  Progress lines in loopless.cpp's format ("k: .. | r: .. | A: ..") every
 * 10000 survivors, if [progress] is 1.  "CP" checkpoint lines give (x, k(x),
 * ln A(x)) at every multiple of 1e9, at 2^32, at the paper's z = 216171986291, and
 * at Z_END.  Timing goes to stderr.
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
static u64 *sq, *sn1, *sn2; static size_t ns, cs;
static void small_push(u64 q, u64 t1, u64 t2) {
    if (ns == cs) { cs = cs ? 2 * cs : 1 << 16;
        sq = realloc(sq, cs * 8); sn1 = realloc(sn1, cs * 8); sn2 = realloc(sn2, cs * 8);
        if (!sq || !sn1 || !sn2) { fprintf(stderr, "oom small\n"); exit(2); } }
    sq[ns] = q; sn1[ns] = t1; sn2[ns] = t2; ns++;
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
static inline void bpush(u64 chunk, u64 q, u64 off) {
    Block **h = &BK[chunk % NB];
    if (!*h || (*h)->n == BLK) { Block *b = balloc(); b->next = *h; *h = b; }
    (*h)->v[(*h)->n++] = (q << CHLOG) | off;
}
/* next hit of q after the hit n (n = c mod q for one root c) */
static inline u64 advance(u64 n, u64 q) {
    u64 rho = n % q, other = q - 1 - rho;
    u64 a = n + 2 * q, b = next_odd_hit(n, other, q);
    return a < b ? a : b;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s Z_END Q [progress]\n", argv[0]); return 1; }
    ZEND = strtoull(argv[1], 0, 10); QLIM = strtoull(argv[2], 0, 10);
    PROGRESS = argc > 3 ? atoi(argv[3]) : 1;
    if (QLIM > (1ULL << (64 - CHLOG)) - 1) { fprintf(stderr, "Q too large for packing\n"); return 1; }
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

    SLIM = ZEND / 2 + 1;
    NB = QLIM / CH + 4; if (NB < 4) NB = 4;
    BK = calloc(NB, sizeof(Block *)); if (!BK) { fprintf(stderr, "oom BK\n"); return 2; }

    /* initial M2: primes 7 <= q < 3e6, q = 1 mod 3 */
    u64 m2 = 0, m2big = 0;
    for (u64 q = 7; q < LO; q++) if (ip[q] && q % 3 == 1) {
        u64 c = cube_root(q);
        small_push(q, next_odd_hit(LO, c, q), next_odd_hit(LO, q - 1 - c, q)); m2++;
    }
    free(ip);

    /* checkpoints */
    u64 *cps = malloc((ZEND / 1000000000ULL + 8) * 8); int ncp = 0;
    for (u64 x = 1000000000ULL; x < ZEND; x += 1000000000ULL) cps[ncp++] = x;
    cps[ncp++] = 4294967296ULL; cps[ncp++] = 216171986291ULL; cps[ncp++] = ZEND;
    for (int i = 0; i < ncp; i++) for (int j = i + 1; j < ncp; j++) if (cps[j] < cps[i]) { u64 t = cps[i]; cps[i] = cps[j]; cps[j] = t; }
    int icp = 0;

    uint8_t *comp = malloc(CH), *hit = malloc(CH);
    u64 k = 0; long double acc = 0.0L, cmp = 0.0L;
    u64 base = LO;                     /* chunk covers odd n = base+1, base+3, ..., base+SPAN-1 */
    u64 nchunks = (ZEND - LO) / SPAN + 1;
    for (u64 ci = 0; ci < nchunks; ci++, base += SPAN) {
        u64 end = base + SPAN;         /* exclusive */
        memset(comp, 0, CH); memset(hit, 0, CH);
        for (size_t j = 0; j < nsp; j++) {
            u64 m = spn[j], p2 = 2 * sp[j];
            for (; m < end; m += p2) comp[(m - base - 1) >> 1] = 1;
            spn[j] = m;
        }
        for (size_t j = 0; j < ns; j++) {
            u64 q2 = 2 * sq[j], t;
            for (t = sn1[j]; t < end; t += q2) hit[(t - base - 1) >> 1] = 1;
            sn1[j] = t;
            for (t = sn2[j]; t < end; t += q2) hit[(t - base - 1) >> 1] = 1;
            sn2[j] = t;
        }
        {   Block *b = BK[ci % NB]; BK[ci % NB] = 0;
            while (b) {
                for (u64 e = 0; e < b->n; e++) {
                    u64 q = b->v[e] >> CHLOG, off = b->v[e] & (CH - 1);
                    u64 n = base + 2 * off + 1;
                    for (;;) {
                        hit[(n - base - 1) >> 1] = 1;
                        n = advance(n, q);
                        if (n >= end) break;
                    }
                    u64 c2 = (n - LO - 1) / SPAN;
                    if (c2 % NB == ci % NB) { fprintf(stderr, "bucket wrap\n"); return 3; }
                    bpush(c2, q, ((n - LO - 1) % SPAN) >> 1);
                }
                Block *nx = b->next; b->next = FREE; FREE = b; b = nx;
            }
        }
        for (u64 i = 0; i < CH; i++) {
            u64 n = base + 2 * i + 1;
            if (n > ZEND) break;
            while (icp < ncp && cps[icp] < n) {
                printf("CP x=%llu k=%llu lnA=%.21Lg m2=%llu m2big=%llu\n",
                       (unsigned long long)cps[icp], (unsigned long long)k, acc + cmp,
                       (unsigned long long)m2, (unsigned long long)m2big);
                fflush(stdout);
                icp++;
            }
            if (comp[i]) continue;
            if (!hit[i]) {
                k++;
                long double term = log1pl(1.0L / (long double)(n - 1));
                long double t = acc + term;
                if (fabsl(acc) >= fabsl(term)) cmp += (acc - t) + term; else cmp += (term - t) + acc;
                acc = t;
                if (n % 6 == 1 && n <= SLIM) s_set(n);
                if (PROGRESS && k % 10000 == 0)
                    printf("k: %-8llu | r: %-10llu | A: %.12Lf\n", (unsigned long long)k,
                           (unsigned long long)n, expl(acc + cmp));
            } else if (n % 3 == 1 && (n % 4 == 3 || !s_get((n + 1) / 2))) {
                m2++;
                if (n >= QLIM) { m2big++; continue; }
                u64 c = cube_root(n), c2 = n - 1 - c;
                u64 t1 = next_odd_hit(n, c, n), t2 = next_odd_hit(n, c2, n);
                if (n < SMALLQ) {
                    u64 q2 = 2 * n;
                    for (; t1 < end; t1 += q2) hit[(t1 - base - 1) >> 1] = 1;
                    for (; t2 < end; t2 += q2) hit[(t2 - base - 1) >> 1] = 1;
                    small_push(n, t1, t2);
                } else {
                    u64 t = t1 < t2 ? t1 : t2;
                    while (t < end) { hit[(t - base - 1) >> 1] = 1; t = advance(t, n); }
                    bpush((t - LO - 1) / SPAN, n, ((t - LO - 1) % SPAN) >> 1);
                }
            }
        }
        if ((ci & 1023) == 1023) {
            fprintf(stderr, "[%lds] r ~ %.4e  k = %llu  lnA = %.12Lf  m2 = %llu  blocks = %llu (%.2f GB)\n", (long)(time(0) - t0),
                    (double)end, (unsigned long long)k, acc + cmp, (unsigned long long)m2,
                    (unsigned long long)NBLOCKS, NBLOCKS * (double)sizeof(Block) / 1e9);
            fflush(stdout);
        }
    }
    while (icp < ncp) {
        if (cps[icp] <= ZEND)
            printf("CP x=%llu k=%llu lnA=%.21Lg m2=%llu m2big=%llu\n", (unsigned long long)cps[icp],
                   (unsigned long long)k, acc + cmp, (unsigned long long)m2, (unsigned long long)m2big);
        icp++;
    }
    printf("SUMMARY ZEND=%llu Q=%llu k=%llu lnA=%.21Lg m2=%llu m2big=%llu seconds=%ld\n",
           (unsigned long long)ZEND, (unsigned long long)QLIM, (unsigned long long)k, acc + cmp,
           (unsigned long long)m2, (unsigned long long)m2big, (long)(time(0) - t0));
    return 0;
}
