// RECOVERED SOURCE -- see sources/README.md.  Supplied as a single-line
// paste, so line breaks were reinserted mechanically at ';', '{', '}'.
// The TOKEN SEQUENCE is verbatim; the layout is not the authors'.
// g++ -O3 -o all all.cpp -lgmp #include <iostream>
#include <gmp.h>
using namespace std;

  int main() {
cout << "Looking for odd primes x where rad(x^2+x+1) | 3*7*13*19*31*61*127*331" << endl;
cout << "-------------------------------------------------------------------" << endl;
mpz_t x, v, limit;
mpz_t p3, p7, p13, p19, p31, p61, p127, p331;
mpz_inits(x, v, limit, p3, p7,p13, p19, p31, p61, p127, p331, NULL);
mpz_set_ui(p3, 3);
mpz_set_ui(p7, 7);
mpz_set_ui(p13, 13);
mpz_set_ui(p19, 19);
mpz_set_ui(p31, 31);
mpz_set_ui(p61, 61);
mpz_set_ui(p127, 127);
mpz_set_ui(p331, 331);
mpz_set_ui(x, 3);
mpz_set_str(limit, "10000000000", 10);
while (mpz_cmp(x, limit) <= 0) {
mpz_mul(v, x, x);
mpz_add(v, v, x);
mpz_add_ui(v, v, 1);
mpz_remove(v, v, p3);
mpz_remove(v, v, p7);
mpz_remove(v, v, p13);
mpz_remove(v, v, p19);
mpz_remove(v, v, p31);
mpz_remove(v, v, p61);
mpz_remove(v, v, p127);
mpz_remove(v, v, p331);
// If only 1 remains, the entire prime factorization consisted of the targets             if (mpz_cmp_ui(v, 1) == 0 && mpz_probab_prime_p(x, 25)) {
gmp_printf("x = %Zd\n", x);
}
mpz_add_ui(x, x, 2);
}
cout << "------------------------------------------------------------------" << endl;
cout << "Search complete." << endl;
mpz_clears(x, v, limit, p3, p7, p13, p19, p31, p61, p127, p331, NULL);
return 0;
}

