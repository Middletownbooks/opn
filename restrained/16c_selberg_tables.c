/* Error term with |lambda_d| <= min(1, h(d) G(xi/d) / G(xi)), h(d) = prod_{p|d} (1 + g(p)).
   omega(p) = 3 iff M2[p] (exact Algorithm-1 M2 below N), else 1.
   Prints: xi, G(xi), W(xi) = sum omega(d), E1(xi) = sum omega(d) min(1, h(d) G(xi/d)/G(xi)). */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc, char **argv) {
    long N = atol(argv[1]);
    unsigned char *M2 = malloc(N + 1); FILE *f = fopen(argv[2], "rb");
    if (fread(M2, 1, N + 1, f) != (size_t)(N + 1)) return 1; fclose(f);
    int *spf = calloc(N, sizeof(int));
    for (long i = 2; i < N; i++) if (!spf[i]) for (long j = i; j < N; j += i) if (!spf[j]) spf[j] = (int)i;
    float *g = malloc(N * sizeof(float)), *h = malloc(N * sizeof(float)), *om = malloc(N * sizeof(float));
    double *Gc = malloc(N * sizeof(double));
    g[1] = 1; h[1] = 1; om[1] = 1; Gc[0] = 0; Gc[1] = 1;
    for (long d = 2; d < N; d++) {
        long p = spf[d], m = d / p; int w = M2[p] ? 3 : 1;
        if (m % p == 0 || g[m] == 0) { g[d] = 0; h[d] = 0; om[d] = 0; }
        else { double gp = (double)w / (p - w); g[d] = g[m] * gp; h[d] = h[m] * (1 + gp); om[d] = om[m] * w; }
        Gc[d] = Gc[d-1] + g[d];
    }
    for (double xi = 1000; xi <= N; xi *= 1.25) {
        long X = (long)xi; double G = Gc[X-1], W = 0, E1 = 0;
        for (long d = 1; d < X; d++) {
            if (om[d] == 0) continue;
            double lam = h[d] * Gc[(X - 1) / d] / G; if (lam > 1) lam = 1;
            W += om[d]; E1 += om[d] * lam;
        }
        printf("%ld %.10g %.10g %.10g\n", X, G, W, E1); fflush(stdout);
    }
    return 0;
}
