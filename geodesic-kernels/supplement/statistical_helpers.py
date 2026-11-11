"""Verbatim helpers from the original checker.py; NumPy and stdlib only."""
import math, statistics, functools
import numpy as np
Z=statistics.NormalDist().inv_cdf(.975)

def wilson(k,n):
 if not n:return [None,None]
 p=k/n;den=1+Z*Z/n;mid=(p+Z*Z/(2*n))/den;rad=Z*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n))/den
 return [max(0,mid-rad),min(1,mid+rad)]

def beta_cf(a,b,x):
 qab=a+b;qap=a+1;qam=a-1;c=1.;d=1-qab*x/qap;tiny=1e-300
 if abs(d)<tiny:d=tiny
 d=1/d;h=d
 for m in range(1,500):
  m2=2*m;aa=m*(b-m)*x/((qam+m2)*(a+m2))
  d=1+aa*d;c=1+aa/c
  if abs(d)<tiny:d=tiny
  if abs(c)<tiny:c=tiny
  d=1/d;h*=d*c
  aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
  d=1+aa*d;c=1+aa/c
  if abs(d)<tiny:d=tiny
  if abs(c)<tiny:c=tiny
  d=1/d;delta=d*c;h*=delta
  if abs(delta-1)<1e-14:return h
 raise ArithmeticError('incomplete beta did not converge')

def beta_reg(x,a,b):
 if x<=0:return 0.
 if x>=1:return 1.
 bt=math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log1p(-x))
 return bt*beta_cf(a,b,x)/a if x<(a+1)/(a+b+2) else 1-bt*beta_cf(b,a,1-x)/b

@functools.lru_cache(None)
def t975(df):
 lo=0.;hi=1.
 def cdf(t):return 1-.5*beta_reg(df/(df+t*t),df/2,.5)
 while cdf(hi)<.975:hi*=2
 for _ in range(70):
  mid=(lo+hi)/2
  if cdf(mid)<.975:lo=mid
  else:hi=mid
 return (lo+hi)/2

def mean_ci(v):
 v=np.asarray(v,float);n=len(v)
 if not n:return dict(n=0,mean=None,ci95=[None,None])
 if n==1:return dict(n=n,mean=float(v.mean()),ci95=[None,None])
 t=t975(n-1)
 rad=t*float(v.std(ddof=1))/math.sqrt(n);m=float(v.mean())
 return dict(n=n,mean=m,ci95=[m-rad,m+rad])

def validate_decision(d,n):
 m=d.get('method')
 if m=='mpfr_interval_ldl':
  if d['status']==1:assert d['pivot_lo']>0 and d['min_positive_pivot_lo']>0
  elif d['status']==-1:assert d['pivot_hi']<0 and d['min_positive_pivot_lo']>0
 elif m=='mpfr_interval_rayleigh':assert d['status']==-1 and d['rayleigh_hi']<0
 elif m=='binary128_backward_bound':
  err=2*n*(d['initial_entry_error_upper']+16*(n+1)*2.**-112*d['max_intermediate_upper']*d['max_multiplier_upper']**2)
  tau=math.sqrt(n)*d['inverse_residual_bound'];assert tau<.5
  ell=.5*d['d_min_lower']*(1-tau)**2/d['inverse_frobenius_sq_upper']
  assert math.isclose(err,d['backward_error_norm_upper'],rel_tol=1e-13)
  assert math.isclose(ell,d['factor_eigenvalue_lower'],rel_tol=1e-13)
  assert d['status']==1 and d['lambda_min_lower']>0 and ell>err
