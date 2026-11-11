// Independent verifier: directed MPFR interval Cholesky, no project code imported.
// Build: clang++ -O2 -std=c++17 -dynamiclib independent_interval.cpp
//   -I/opt/homebrew/include -L/opt/homebrew/lib -lmpfr -lgmp
//   -o independent_interval.dylib
#include <mpfr.h>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>

struct Box {
    mpfr_t lo, hi;
    Box() { mpfr_init(lo); mpfr_init(hi); mpfr_set_zero(lo, 1); mpfr_set_zero(hi, 1); }
    explicit Box(double x): Box() { mpfr_set_d(lo,x,MPFR_RNDD); mpfr_set_d(hi,x,MPFR_RNDU); }
    Box(const Box& x): Box() { mpfr_set(lo,x.lo,MPFR_RNDD); mpfr_set(hi,x.hi,MPFR_RNDU); }
    Box& operator=(const Box& x) { if(this!=&x) { mpfr_set(lo,x.lo,MPFR_RNDD); mpfr_set(hi,x.hi,MPFR_RNDU); } return *this; }
    ~Box() { mpfr_clear(lo); mpfr_clear(hi); }
};
static Box plus(const Box& a,const Box& b) {
    Box z; mpfr_add(z.lo,a.lo,b.lo,MPFR_RNDD); mpfr_add(z.hi,a.hi,b.hi,MPFR_RNDU); return z;
}
static Box minus(const Box& a,const Box& b) {
    Box z; mpfr_sub(z.lo,a.lo,b.hi,MPFR_RNDD); mpfr_sub(z.hi,a.hi,b.lo,MPFR_RNDU); return z;
}
static Box times(const Box& a,const Box& b) {
    Box z; mpfr_t w; mpfr_init(w);
    mpfr_srcptr aa[2]={a.lo,a.hi},bb[2]={b.lo,b.hi};
    mpfr_set_inf(z.lo,1); mpfr_set_inf(z.hi,-1);
    for(int i=0;i<2;i++) for(int j=0;j<2;j++) {
        mpfr_mul(w,aa[i],bb[j],MPFR_RNDD); if(mpfr_less_p(w,z.lo)) mpfr_set(z.lo,w,MPFR_RNDD);
        mpfr_mul(w,aa[i],bb[j],MPFR_RNDU); if(mpfr_greater_p(w,z.hi)) mpfr_set(z.hi,w,MPFR_RNDU);
    }
    mpfr_clear(w); return z;
}
static Box square(const Box& a) {
    Box z;
    if(mpfr_sgn(a.lo)>=0) {mpfr_sqr(z.lo,a.lo,MPFR_RNDD);mpfr_sqr(z.hi,a.hi,MPFR_RNDU);}
    else if(mpfr_sgn(a.hi)<=0) {mpfr_sqr(z.lo,a.hi,MPFR_RNDD);mpfr_sqr(z.hi,a.lo,MPFR_RNDU);}
    else {mpfr_t w;mpfr_init(w);mpfr_set_zero(z.lo,1);mpfr_sqr(z.hi,a.lo,MPFR_RNDU);mpfr_sqr(w,a.hi,MPFR_RNDU);if(mpfr_greater_p(w,z.hi))mpfr_set(z.hi,w,MPFR_RNDU);mpfr_clear(w);}
    return z;
}
static Box root(const Box& a) {Box z;mpfr_sqrt(z.lo,a.lo,MPFR_RNDD);mpfr_sqrt(z.hi,a.hi,MPFR_RNDU);return z;}
static Box divide(const Box& a,const Box& b) {
    // Positive denominator, reciprocal is monotone decreasing.
    Box inv;mpfr_ui_div(inv.lo,1,b.hi,MPFR_RNDD);mpfr_ui_div(inv.hi,1,b.lo,MPFR_RNDU);return times(a,inv);
}
static Box kernel(const Box& cosine,double bandwidth,int power) {
    Box d;mpfr_acos(d.lo,cosine.hi,MPFR_RNDD);mpfr_acos(d.hi,cosine.lo,MPFR_RNDU);
    Box s=power==2?square(d):d, t=times(Box(bandwidth),s), z;
    mpfr_neg(z.lo,t.hi,MPFR_RNDD);mpfr_neg(z.hi,t.lo,MPFR_RNDU);
    mpfr_exp(z.lo,z.lo,MPFR_RNDD);mpfr_exp(z.hi,z.hi,MPFR_RNDU);return z;
}
extern "C" int certify(const double* raw,int n,int dim,double bandwidth,int power,int bits,double* diagnostic) {
    mpfr_set_default_prec(bits);
    std::vector<Box> coordinates(n*dim), norms(n), matrix(n*n), column(n);
    std::vector<int> permutation(n);std::iota(permutation.begin(),permutation.end(),0);
    for(int i=0;i<n;i++) {
        Box norm2;
        for(int j=0;j<dim;j++) {coordinates[i*dim+j]=Box(raw[i*dim+j]);norm2=plus(norm2,square(coordinates[i*dim+j]));}
        norms[i]=root(norm2);
        if(mpfr_sgn(norms[i].lo)<=0)return 0;
    }
    auto at=[&](int i,int j)->Box& {return matrix[std::min(i,j)*n+std::max(i,j)];};
    for(int i=0;i<n;i++) {
        at(i,i)=Box(1);
        for(int j=i+1;j<n;j++) {
            Box dot;
            for(int k=0;k<dim;k++)dot=plus(dot,times(coordinates[i*dim+k],coordinates[j*dim+k]));
            Box c=divide(dot,times(norms[i],norms[j]));
            if(mpfr_cmp_si(c.lo,-1)<0)mpfr_set_si(c.lo,-1,MPFR_RNDD);
            if(mpfr_cmp_si(c.hi,1)>0)mpfr_set_si(c.hi,1,MPFR_RNDU);
            at(i,j)=kernel(c,bandwidth,power);
        }
    }
    double minpivot=1;
    for(int k=0;k<n;k++) {
        int choice=k;
        for(int j=k+1;j<n;j++)if(mpfr_greater_p(at(permutation[j],permutation[j]).lo,at(permutation[choice],permutation[choice]).lo))choice=j;
        std::swap(permutation[k],permutation[choice]);
        const int p=permutation[k];Box diagonal=at(p,p);
        diagnostic[0]=k;diagnostic[1]=mpfr_get_d(diagonal.lo,MPFR_RNDD);diagnostic[2]=mpfr_get_d(diagonal.hi,MPFR_RNDU);
        diagnostic[3]=minpivot;
        if(mpfr_sgn(diagonal.hi)<0)return -1;
        if(mpfr_sgn(diagonal.lo)<=0)return 0;
        minpivot=std::min(minpivot,diagnostic[1]);
        Box pivotroot=root(diagonal);
        for(int j=k+1;j<n;j++)column[j]=divide(at(p,permutation[j]),pivotroot);
        for(int i=k+1;i<n;i++) {
            int a=permutation[i];at(a,a)=minus(at(a,a),square(column[i]));
            for(int j=i+1;j<n;j++) {int b=permutation[j];at(a,b)=minus(at(a,b),times(column[i],column[j]));}
        }
    }
    diagnostic[3]=minpivot;return 1;
}
