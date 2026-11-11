"""Binary C-SVM dual with deterministic second-order SMO and explicit KKT audit."""
import numpy as np

def fit(K,y,C=1.,tol=1e-5,maxiter=100000,initial=None):
 y=np.asarray(y,dtype=float);n=len(y)
 a=np.zeros(n) if initial is None else np.clip(initial.copy(),0,C)
 f=y-K@(a*y);diag=np.diag(K);tiny=1e-12
 for it in range(maxiter):
  up=((y>0)&(a<C-tiny))|((y<0)&(a>tiny))
  low=((y>0)&(a>tiny))|((y<0)&(a<C-tiny))
  i=int(np.argmax(np.where(up,f,-np.inf)));lo=float(np.min(f[low]));gap=float(f[i]-lo)
  if gap<tol:break
  diff=f[i]-f;eta=np.maximum(diag[i]+diag-2*K[i],1e-14)
  improve=np.where(low&(diff>0),diff**2/eta,-np.inf);improve[i]=-np.inf
  j=int(np.argmax(improve));step=min(float(diff[j]/eta[j]),float(C-a[i] if y[i]>0 else a[i]),float(a[j] if y[j]>0 else C-a[j]))
  if step<1e-15:
   j=int(np.argmin(np.where(low,f,np.inf)));step=min(float((f[i]-f[j])/max(diag[i]+diag[j]-2*K[i,j],1e-14)),float(C-a[i] if y[i]>0 else a[i]),float(a[j] if y[j]>0 else C-a[j]))
  a[i]+=y[i]*step;a[j]-=y[j]*step;f-=step*(K[i]-K[j])
 else:raise RuntimeError('SMO did not converge')
 # Recompute the gradient to make the stopping certificate independent of incremental drift.
 f=y-K@(a*y);up=((y>0)&(a<C-tiny))|((y<0)&(a>tiny));low=((y>0)&(a>tiny))|((y<0)&(a<C-tiny))
 gap=float(np.max(f[up])-np.min(f[low]));free=(a>tiny)&(a<C-tiny)
 b=float(np.mean(f[free])) if np.any(free) else float((np.max(f[up])+np.min(f[low]))/2)
 assert gap<tol*1.01+1e-10,(gap,tol)
 assert abs(y@a)<1e-8
 return dict(alpha=a,b=b,kkt_gap=gap,iterations=it+1,equality_residual=float(abs(y@a)))

def predict(model,Ktest,ytrain):return np.where(Ktest@(model['alpha']*ytrain)+model['b']>=0,1,-1)
