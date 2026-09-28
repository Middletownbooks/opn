/* Auditor's own Algorithm 1, written from the paper's pseudocode.
   Direct factorisation of r^2+r+1 and r+1 (Pollard-Brent + Miller-Rabin).
   usage: mine ZEND Q SURVFILE(or -)   ; exclusion uses only M2 primes < Q
   M1 and M2 are byte arrays over [0, ZEND]. Requires ZEND < 2^32. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 mulm(u64 a, u64 b, u64 m){ return (u64)((u128)a*b%m); }
static u64 powm(u64 a, u64 e, u64 m){ u64 r=1; a%=m; while(e){ if(e&1) r=mulm(r,a,m); a=mulm(a,a,m); e>>=1;} return r; }
static int isprime(u64 n){
  static const u64 B[]={2,3,5,7,11,13,17,19,23,29,31,37};
  if(n<2) return 0;
  for(int i=0;i<12;i++){ if(n%B[i]==0) return n==B[i]; }
  u64 d=n-1; int s=0; while(!(d&1)){d>>=1;s++;}
  for(int i=0;i<12;i++){ u64 x=powm(B[i],d,n); if(x==1||x==n-1) continue; int ok=0;
    for(int j=1;j<s;j++){ x=mulm(x,x,n); if(x==n-1){ok=1;break;} } if(!ok) return 0; }
  return 1;
}
static u64 gcd(u64 a,u64 b){ while(b){u64 t=a%b;a=b;b=t;} return a; }
static u64 brent(u64 n){
  if(n%2==0) return 2;
  for(u64 c=1;;c++){
    u64 y=2,x,g=1,q=1,ys=0; u64 r=1,m=64;
    do{ x=y; for(u64 i=0;i<r;i++) y=(mulm(y,y,n)+c)%n;
      u64 k=0;
      do{ ys=y; for(u64 i=0;i<m && i<r-k;i++){ y=(mulm(y,y,n)+c)%n; q=mulm(q, x>y?x-y:y-x, n);} g=gcd(q,n); k+=m; } while(k<r && g==1);
      r<<=1; } while(g==1);
    if(g==n){ do{ ys=(mulm(ys,ys,n)+c)%n; g=gcd(x>ys?x-ys:ys-x,n);} while(g==1); }
    if(g!=n) return g;
  }
}
/* collect distinct prime factors of n into f[], return count */
static int factor(u64 n, u64 *f, int nf){
  for(u64 p=2;p<1000 && p*p<=n;p++){ if(n%p==0){ int dup=0; for(int i=0;i<nf;i++) if(f[i]==p) dup=1; if(!dup) f[nf++]=p; while(n%p==0) n/=p; } }
  if(n==1) return nf;
  if(isprime(n)){ int dup=0; for(int i=0;i<nf;i++) if(f[i]==n) dup=1; if(!dup) f[nf++]=n; return nf; }
  u64 d=brent(n);
  nf=factor(d,f,nf); nf=factor(n/d,f,nf); return nf;
}
int main(int argc,char**argv){
  u64 Z=strtoull(argv[1],0,10), Q=strtoull(argv[2],0,10);
  FILE *sf = strcmp(argv[3],"-") ? fopen(argv[3],"w") : 0;
  unsigned char *pr=malloc(Z+1), *M1=calloc(Z+1,1), *M2=calloc(Z+1,1);
  memset(pr,1,Z+1); pr[0]=pr[1]=0;
  for(u64 i=2;i*i<=Z;i++) if(pr[i]) for(u64 j=i*i;j<=Z;j+=i) pr[j]=0;
  for(u64 r=5;r<3000000;r++) if(pr[r]){ M1[r]=1; if(r>=7 && r%3==1) M2[r]=1; }
  u64 k=0; long double s=0, c=0; u64 f[64];
  for(u64 r=3000001;r<=Z;r++){ if(!pr[r]) continue;
    u64 v=r*r+r+1;  /* r < 2^32 so exact */
    int nf=factor(v,f,0), bad=0;
    for(int i=0;i<nf;i++){ u64 p=f[i]; if(p==2||p==3) continue; if(p<r && p<Q && M2[p]) { bad=1; break; } }
    if(!bad){ k++; long double t=log1pl(1.0L/(long double)(r-1)); volatile long double y=t-c; long double tt=s+y; c=(tt-s)-y; s=tt;
      if(sf) fprintf(sf,"%llu\n",(unsigned long long)r);
      if(k%10000==0) printf("k: %-8llu | r: %-10llu | A: %.12Lf\n",(unsigned long long)k,(unsigned long long)r,expl(s));
    } else {
      M1[r]=1;
      if(r%3==1){
        int join = (r%4==3);
        if(!join){ int ng=factor(r+1,f,0); for(int i=0;i<ng;i++){ u64 p=f[i]; if(p==2||p==3) continue; if(M1[p]) {join=1;break;} } }
        if(join) M2[r]=1;
      }
    }
  }
  printf("FINAL Z=%llu Q=%llu k=%llu lnA=%.21Lg\n",(unsigned long long)Z,(unsigned long long)Q,(unsigned long long)k,s);
  if(sf) fclose(sf);
  return 0;
}
