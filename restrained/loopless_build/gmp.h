/* Minimal stand-in for <gmp.h>, which is not installed in this container
   (only the runtime library libgmp.so.10 is).  It declares exactly the GMP
   entry points that sources/loopless.cpp uses, with GMP's real ABI (struct
   layout and the __gmpf_* / __gmp_* symbol names that <gmp.h> maps them to),
   so the authors' code is compiled UNMODIFIED and linked against the real
   library.  Not part of the authors' distribution. */
#ifndef OPN_GMP_SHIM_H
#define OPN_GMP_SHIM_H
#ifdef __cplusplus
extern "C" {
#endif
typedef unsigned long mp_limb_t;
typedef long mp_exp_t;
typedef unsigned long mp_bitcnt_t;
typedef struct { int _mp_prec; int _mp_size; mp_exp_t _mp_exp; mp_limb_t *_mp_d; } __mpf_struct;
typedef __mpf_struct mpf_t[1];
typedef __mpf_struct *mpf_ptr;
typedef const __mpf_struct *mpf_srcptr;
void __gmpf_set_default_prec(mp_bitcnt_t);
void __gmpf_inits(mpf_ptr, ...);
void __gmpf_set_ui(mpf_ptr, unsigned long);
void __gmpf_mul(mpf_ptr, mpf_srcptr, mpf_srcptr);
void __gmpf_sub_ui(mpf_ptr, mpf_srcptr, unsigned long);
void __gmpf_div(mpf_ptr, mpf_srcptr, mpf_srcptr);
int __gmp_printf(const char *, ...);
#ifdef __cplusplus
}
#endif
#define mpf_set_default_prec __gmpf_set_default_prec
#define mpf_inits __gmpf_inits
#define mpf_set_ui __gmpf_set_ui
#define mpf_mul __gmpf_mul
#define mpf_sub_ui __gmpf_sub_ui
#define mpf_div __gmpf_div
#define gmp_printf __gmp_printf
#endif
