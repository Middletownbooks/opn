// RECOVERED SOURCE -- see sources/README.md.  Supplied as a single-line
// paste, so line breaks were reinserted mechanically at ';', '{', '}'.
// The TOKEN SEQUENCE is verbatim; the layout is not the authors'.
// ============================================================================ // tree.cpp (With checkfacts.txt Database Injection) // Compile: g++ -O3 -o tree -std=c++17 tree.cpp -lgmpxx -lgmp // Run: ./tree_search 11 // ============================================================================  #include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <map>
#include <string>
#include <cstdlib>
#include <algorithm>
#include <gmpxx.h>
// ---------------------------------------------------------------------------- // Global Configuration & Database // ---------------------------------------------------------------------------- bool verbose = false;
// Maps {
root x, type}
-> list of prime factors // type 3 = ordinary (x^2+x+1), type 2 = special (x+1) std::map<std::pair<mpz_class, int>, std::vector<mpz_class>> db;
void load_database(const std::string& filename) {
std::ifstream file(filename);
if (!file.is_open()) {
if (verbose) std::cout << "No '" << filename << "' found. Running pure Pollard's rho.\n";
return;
}
std::string x_str, f_str;
int type;
size_t count = 0;
while (file >> x_str >> type >> f_str) {
if (type == 2 || type == 3) {
mpz_class x(x_str);
mpz_class f(f_str);
db[{
x, type}
].push_back(f);
count++;
}
}
std::cout << "Loaded " << count << " known factors from " << filename << ".\n\n";
}
// ---------------------------------------------------------------------------- // Mathematical Utilities // ---------------------------------------------------------------------------- static gmp_randclass gmp_rng(gmp_randinit_default);
static bool rng_seeded = false;
void init_rng() {
if (!rng_seeded) {
gmp_rng.seed(time(NULL));
rng_seeded = true;
}
}
bool miller_rabin(const mpz_class& n, int iters = 25) {
init_rng();
mpz_class d = n - 1;
int s = 0;
while (d % 2 == 0) {
d /= 2;
s++;
}
for (int i = 0;
i < iters;
++i) {
mpz_class a = gmp_rng.get_z_range(n - 3) + 2;
mpz_class x;
mpz_powm(x.get_mpz_t(), a.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());
if (x == 1 || x == n - 1) continue;
bool composite = true;
for (int r = 1;
r < s;
++r) {
mpz_powm_ui(x.get_mpz_t(), x.get_mpz_t(), 2, n.get_mpz_t());
if (x == n - 1) {
composite = false;
break;
}
}
if (composite) return false;
}
return true;
}
mpz_class pollard_rho(const mpz_class& n) {
if (n % 2 == 0) return 2;
init_rng();
mpz_class x = 2, y = 2, d = 1, c = 1;
auto f = [&](const mpz_class& val, const mpz_class& mod, const mpz_class& constant) {
mpz_class res;
mpz_powm_ui(res.get_mpz_t(), val.get_mpz_t(), 2, mod.get_mpz_t());
res = (res + constant) % mod;
return res;
}
;
while (d == 1) {
x = f(x, n, c);
y = f(f(y, n, c), n, c);
mpz_class diff = abs(x - y);
mpz_gcd(d.get_mpz_t(), diff.get_mpz_t(), n.get_mpz_t());
if (d == n) {
x = gmp_rng.get_z_range(n - 2) + 2;
y = x;
c = gmp_rng.get_z_range(n - 1) + 1;
d = 1;
}
}
return d;
}
bool factorize_with_early_abort(mpz_class n, const mpz_class& root, std::vector<mpz_class>& factors) {
std::vector<mpz_class> queue;
std::set<mpz_class> distinct_primes;
if (n > 1) queue.push_back(n);
const std::vector<unsigned long> small_primes = {
5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,         43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97     }
;
while (!queue.empty()) {
mpz_class v = queue.back();
queue.pop_back();
if (v <= 1) continue;
if (miller_rabin(v)) {
if (v < root) {
factors.clear();
factors.push_back(v);
return true;
}
distinct_primes.insert(v);
}
else {
bool found_small = false;
for (unsigned long p : small_primes) {
if (v % p == 0) {
mpz_class p_mpz = p;
if (p_mpz < root) {
factors.clear();
factors.push_back(p_mpz);
return true;
}
distinct_primes.insert(p_mpz);
while (v % p == 0) v /= p;
if (v > 1) queue.push_back(v);
found_small = true;
break;
}
}
if (!found_small) {
mpz_class d = pollard_rho(v);
mpz_class v_d = v / d;
// Push the larger piece first, so the smaller piece is popped next                 if (d > v_d) {
queue.push_back(d);
queue.push_back(v_d);
}
else {
queue.push_back(v_d);
queue.push_back(d);
}
}
}
}
factors.assign(distinct_primes.begin(), distinct_primes.end());
return false;
}
void print_indent(int depth) {
for (int i = 0;
i < depth;
++i) std::cout << " ";
}
// ---------------------------------------------------------------------------- // Core Recursion Logic // ---------------------------------------------------------------------------- bool prove(const mpz_class& root, const mpz_class& x, bool special_used, std::set<mpz_class>& path, int depth = 0) {
path.insert(x);
// ========================================================================     // Special Branch     // ========================================================================     bool special_eligible = (!special_used && (x % 12 == 1));
bool sp_contradicted = false;
if (special_eligible) {
mpz_class S = (x + 1) / 2;
std::vector<mpz_class> factors_sp;
bool early_sp = false;
auto key_sp = std::make_pair(x, 2);
// Database injection         if (db.count(key_sp)) {
for (const auto& f : db[key_sp]) {
if (f < 5) continue;
if (S % f == 0) {
while (S % f == 0) S /= f;
if (f < root) {
factors_sp.clear();
factors_sp.push_back(f);
early_sp = true;
break;
}
factors_sp.push_back(f);
}
}
}
if (!early_sp && S > 1) {
std::vector<mpz_class> rem_factors;
if (factorize_with_early_abort(S, root, rem_factors)) {
factors_sp.clear();
factors_sp.push_back(rem_factors.back());
early_sp = true;
}
else {
factors_sp.insert(factors_sp.end(), rem_factors.begin(), rem_factors.end());
}
}
if (verbose) {
print_indent(depth);
std::cout << x << "^e => 2";
for (const auto& f : factors_sp) std::cout << " " << f;
if (early_sp) std::cout << "    F " << factors_sp.back();
std::cout << std::endl;
}
sp_contradicted = early_sp;
if (!sp_contradicted) {
for (const auto& f : factors_sp) {
if (path.count(f)) {
if (verbose) {
print_indent(depth + 1);
std::cout << "Cycle: root=" << root << " repeated=" << f << std::endl;
}
continue;
}
if (prove(root, f, true, path, depth + 1)) {
sp_contradicted = true;
break;
}
}
}
}
// ========================================================================     // Ordinary Branch     // ========================================================================     mpz_class G = x * x + x + 1;
bool div3 = (x % 3 == 1);
if (div3) G /= 3;
std::vector<mpz_class> factors_ord;
bool early_ord = false;
auto key_ord = std::make_pair(x, 3);
// Database injection     if (db.count(key_ord)) {
for (const auto& f : db[key_ord]) {
if (f < 5) continue;
// Skip 2 and 3             if (G % f == 0) {
while (G % f == 0) G /= f;
// Divide out the known factor                  if (f < root) {
factors_ord.clear();
factors_ord.push_back(f);
early_ord = true;
break;
}
factors_ord.push_back(f);
}
}
}
// Factor whatever is left (if anything)     if (!early_ord && G > 1) {
std::vector<mpz_class> rem_factors;
if (factorize_with_early_abort(G, root, rem_factors)) {
factors_ord.clear();
factors_ord.push_back(rem_factors.back());
early_ord = true;
}
else {
factors_ord.insert(factors_ord.end(), rem_factors.begin(), rem_factors.end());
}
}
if (verbose) {
print_indent(depth);
std::cout << x << "^2 =>";
if (div3) std::cout << " 3";
for (const auto& f : factors_ord) std::cout << " " << f;
if (early_ord) std::cout << "    F " << factors_ord.back();
std::cout << std::endl;
}
bool ord_contradicted = early_ord;
if (!ord_contradicted) {
for (const auto& f : factors_ord) {
if (path.count(f)) {
if (verbose) {
print_indent(depth + 1);
std::cout << "Cycle: root=" << root << " repeated=" << f << std::endl;
}
continue;
}
if (prove(root, f, special_used, path, depth + 1)) {
ord_contradicted = true;
break;
}
}
}
path.erase(x);
if (special_eligible) return (ord_contradicted && sp_contradicted);
else return ord_contradicted;
}
// ---------------------------------------------------------------------------- // Main // ---------------------------------------------------------------------------- int main(int argc, char* argv[]) {
if (argc < 2) {
std::cerr << "Usage: " << argv[0] << " [-v] [-db filename.txt] <Bound>\n";
return 1;
}
std::string db_file = "checkfacts.txt";
// Defaults to local checkfacts.txt     mpz_class bound = 0;
for (int i = 1;
i < argc;
++i) {
std::string arg = argv[i];
if (arg == "-v") {
verbose = true;
}
else if (arg == "-db" && i + 1 < argc) {
db_file = argv[++i];
}
else {
bound = mpz_class(arg);
}
}
load_database(db_file);
if (!verbose) std::cout << "Testing roots up to " << bound << "...\n" << std::endl;
std::vector<mpz_class> unresolved_roots;
unsigned long ruled_out_count = 0;
//mpz_class r = 1009;
//while (r <= bound) {
mpz_class r = bound;
while (1) {
if (verbose) {
std::cout << "\n";
}
std::set<mpz_class> path;
if (prove(r, r, false, path)) {
ruled_out_count++;
//if (verbose) std::cout << "\n[SUCCESS] Root " << r << " successfully ruled out.\n\n";
}
else {
unresolved_roots.push_back(r);
if (verbose) std::cout << "\n[FAILED] Root " << r << " remains unresolved.\n\n";
}
mpz_nextprime(r.get_mpz_t(), r.get_mpz_t());
}
std::cout << "========================================================\n";
std::cout << "SUMMARY\n";
std::cout << "========================================================\n";
std::cout << "Ruled out:  " << ruled_out_count << std::endl;
std::cout << "Unresolved: " << unresolved_roots.size() << std::endl;
if (!unresolved_roots.empty()) {
std::cout << "\nUnresolved roots: ";
for (size_t i = 0;
i < unresolved_roots.size();
++i) {
std::cout << unresolved_roots[i] << (i < unresolved_roots.size() - 1 ? ", " : "");
}
std::cout << std::endl;
}
return 0;
}

