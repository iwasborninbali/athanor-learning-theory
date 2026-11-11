# Mathematical statements and proofs

Throughout, **PD** for a finite real Gram matrix means *strictly* positive definite. This differs from the convention under which a “positive definite kernel” need only generate positive semidefinite finite matrices. Points are distinct, lambda>0, q>0, and S^d has radius one unless stated otherwise.

## 1. Existing exact answer for 0<q<=1 on spheres

For every d>=1, every finite set of distinct points on S^d, every lambda>0 and 0<q<=1, the matrix exp(-lambda theta_ij^q) is strictly PD. In particular P_N(lambda,q)=1 under any nonatomic sampling law, and every finite extension by independent nonatomic points remains strictly PD almost surely.

This is **prior art**: Gneiting (2013), Theorem 7 (nonconstant completely monotone functions restricted to [0,pi] are strictly PD on spheres of every dimension), and Example 1 (powered exponential). For q=1 the function exp(-lambda t) is completely monotone. The example supplies the full 0<q<=1 range. Feragen, Lauze & Hauberg (2015), Theorem 4 and their sphere example, also explain the CND-distance/Schoenberg route; CND alone should not be mistaken for strict CND of spherical distance. Antipodal configurations can obstruct strict CND while the exponential kernel is still strictly PD.

Sources: https://arxiv.org/html/1111.7077 ; https://openaccess.thecvf.com/content_cvpr_2015/papers/Feragen_Geodesic_Exponential_Kernels_2015_CVPR_paper.pdf . Primary sources are linked here. Source PDFs are not included in this compact supplement.

The chord-distance Gaussian exp(-lambda ||x-y||^2) is also strictly PD for distinct Euclidean vectors. One direct proof is its strictly positive Gaussian Fourier density: the quadratic form is an integral of |sum_j c_j exp(i omega.x_j)|^2 against a positive density. If it were zero the finite exponential sum would vanish identically, forcing all c_j=0. Thus this control also has exact append stability.

## 2. Elementary finite-sample sufficient condition, any metric

Let N>=2 and delta=min_{i<j} d(x_i,x_j)>0. If

    lambda > log(N-1)/delta^q,

then every off-diagonal row sum is <1, so Gershgorin's theorem gives strict PD. More generally, for independent samples and a pairwise small-ball bound Pr[d(X_i,X_j)<=r] <= F(r),

    Pr[K is PD] >= 1 - choose(N,2) F(r)

whenever lambda > log(N-1)/r^q. This is a sufficient bound, with no converse; the identity-matrix limit is already explicit in the 2016 problem paper.

## 3. A separation/packing improvement on S^2 (removes log N)

For q>=1, **lambda delta^q >= C = log(26) suffices**, uniformly in N and the configuration.

Proof. Put t=delta/4. Normalized cap area is A(r)=sin^2(r/2) for 0<=r<=pi. Open caps of radius delta/2 around all sample points are disjoint. For a fixed center x_i, consider other centers in the annulus [k delta,(k+1)delta), k>=1. Their caps, together with the cap about x_i, lie in a cap of radius min(pi,(k+3/2)delta). Write m=2k+3, an integer.

If the containing radius is <=pi, its area divided by A(delta/2) is sin^2(m t)/sin^2(t)<=m^2, using |sin(m t)|<=m sin(t). If the containing radius exceeds pi, then m t>pi/2, so m sin(t)>=m sin(pi/(2m))>=1; the same area-ratio bound holds. Thus the number of centers in the annulus is at most m^2-1=(2k+3)^2-1, where the subtraction accounts for x_i's own disjoint cap.

Every off-diagonal row sum is consequently at most

    sum_{k>=1} [(2k+3)^2-1] exp(-lambda delta^q k^q)
      <= sum_{k>=1} (4k^2+12k+8) 26^-k
       = 15608/15625 <1,

since k^q>=k for q>=1. The series identity is

    sum_{k>=1}(4k^2+12k+8) z^k
      = 8z(3-3z+z^2)/(1-z)^3.

Gershgorin gives strict PD (in fact lambda_min>=17/15625 under this conservative bound). The constant log(26) is convenient and very close to the best constant from this particular shell bound; optimizing it does not change the scaling. The proof is provided here in full; no originality claim is made for the general packing technique.

## 4. Explicit high-probability scaling on S^2

Put C=log(26). Suppose X_1,...,X_N are independent and each directional density is bounded by M>=1 relative to uniform spherical area (iid is unnecessary). For 0<epsilon<1 and N>=2 define

    r_epsilon = acos(1 - 4 epsilon/[M N(N-1)]).

The union bound gives Pr[delta<=r_epsilon] <= epsilon. Combining with statement 3, for q>=1,

    lambda >= C/r_epsilon^q  ==>  Pr[K is PD] >= 1-epsilon.

For fixed M, epsilon and N tending to infinity,

    C/r_epsilon^q ~ C (M/(8 epsilon))^(q/2) N^q.

The same single separation event guarantees PD simultaneously for every lambda above this threshold, and for every subset of the sampled points. Thus q=2 has the proved sufficient order **N^2/epsilon**, without a log N factor. For a sphere of radius R the right lambda threshold is divided by R^q. This is a constructive sufficient answer to part of Conjecture 1, deliberately not a sharp transition law. It is very conservative compared with the measured thresholds. For q=1 statement 1 is much stronger.

For uniform iid S^2 points the separation scale itself can be described more precisely:

    Pr[N delta > t] -> exp(-t^2/8),  t>=0.

Proof sketch with the needed counts. Let Z_N count unordered pairs at distance <=t/N. Its mean tends to t^2/8. For each fixed factorial moment order k, terms in E[(Z_N)_k] with k disjoint pairs factor and tend to (t^2/8)^k. An overlapping graph on v vertices and c connected components has O(N^v) labelings; imposing its spanning-forest edges costs O((t/N)^(2(v-c))). Its total contribution is O(N^(2c-v)), which vanishes if any component has at least three vertices. There are finitely many graph types for fixed k. The Poisson factorial-moment criterion yields Z_N -> Poisson(t^2/8), and hence the display. In particular, for lambda=c N^q,

    liminf_N Pr[K is PD] >= exp[-(C/c)^(2/q)/8].

This refines the sufficient confidence constant; it still does not identify the true PD transition scale.

## 5. Fixed-bandwidth failure and inevitable eventual append failure for q>1

Gneiting (2013), Example 1, proves that exp(-lambda theta^q) is not a globally positive semidefinite kernel on S^d for **every fixed lambda>0 and q>1**. (The restriction to an isometrically embedded great circle also suffices.) Therefore some finite configuration z_1,...,z_m and coefficient vector a satisfy a^T K(z) a<0. By continuity there are neighborhoods U_1,...,U_m such that the same strict inequality holds for any x_j in U_j.

If mu has full support, p=product_j mu(U_j)>0. Among N iid observations, divide the first m floor(N/m) observations into ordered, disjoint blocks of m. Each block lands in U_1 x ... x U_m with probability p, independently. A single such block makes the full Gram matrix non-PD by the principal-submatrix criterion. Thus

    P_N(lambda,q) <= (1-p)^floor(N/m) ->0.

This is a **proved qualitative probability consequence of existing global theory**, not a new quantitative transition rate: m and p may depend extremely badly on lambda. In particular any fixed-confidence high-probability bandwidth threshold must escape every bounded set as N grows (uniformity on compact intervals bounded away from zero follows by a finite subcover of robust negative-witness neighborhoods in lambda; the small-lambda square witness below handles approach to zero).

The same bound applies after appending M fresh iid test points, even conditional on any positive-probability event determined by the training points (including training PD). The test-only principal submatrix must be PD, and fresh blocks are independent of the training event:

    Pr[train+M test is PD | training event] <= (1-p)^floor(M/m).

For balanced samples from two full-support classes, apply the block argument to the subsequence of points of either class. A successful finite train-Gram check therefore cannot guarantee indefinite predictive extension. This does not prevent a useful finite training/test experiment.

## 6. Small explicit obstruction and two cautions

Four equally spaced equatorial points have, in direction (1,-1,1,-1), eigenvalue

    1 - 2 exp[-lambda (pi/2)^q] + exp[-lambda pi^q].

Its small-lambda expansion is lambda pi^q (2^(1-q)-1)+O(lambda^2), negative for q>1. For q=2, write t=exp(-lambda pi^2/4); negativity is 1-2t+t^4<0. The nontrivial root t in (0,1) supplies an explicit low-bandwidth interval of bad configurations, and neighborhoods give an explicit finite positive failure probability if their masses are bounded. This witness alone does not prove global failure at every lambda; statement 5 uses the cited full theorem.

For q=2 this obstruction is minimal in cardinality: every three-point metric space is isometric to three points in a Euclidean plane (including a degenerate triangle), and the Euclidean Gaussian is strictly PD for distinct points. Thus P_N(lambda,2)=1 for N<=3 under nonatomic sampling on any metric space, whereas four spherical points can fail at small lambda. A strictly PD three-point training matrix can therefore fail after appending just one point. This is a deterministic obstruction to using training PD as an extension guarantee.

The low-lambda witness also makes the divergence claim in statement 5 uniform down to zero. For a sum-zero coefficient vector, divide its quadratic form by lambda and extend continuously to lambda=0 using the derivative. The square has a strictly negative derivative for q>1. Small neighborhoods preserve this derivative inequality uniformly for 0<lambda<=lambda_s for some lambda_s>0. A finite subcover of [lambda_s,L] supplies finitely many further robust witnesses. With high probability a sufficiently large full-support sample contains a block realizing each witness, so there is no PD bandwidth anywhere in (0,L]. This argument gives no useful numerical rate as L grows.

A PD finite matrix at lambda_0 does not by itself establish PD for every real lambda>lambda_0. Our empirical thresholds are suffix thresholds on a declared grid, not a proof of monotonicity. Integer multiples do preserve PD by Schur products; arbitrary entrywise positive powers do not generally preserve it.

Finally, for fixed lambda>0 and distinct finite points, q down to zero yields

    K -> (1-exp(-lambda)) I + exp(-lambda) 11^T,

rather than a matrix of ones as loosely stated in the 2016 discussion. It is strictly PD; the off-sample similarities of the limiting kernel are constant. For a binary SVM fitted with that limiting kernel, the dual equality constraint sum(alpha_i y_i)=0 makes every off-sample decision equal to the same intercept, giving accuracy 1/2 on a balanced test set under a fixed tie rule. This is a statement about the limiting kernel itself, not a theorem that classification accuracy converges to 1/2 as positive q tends to zero: taking the sign of a decision that tends to zero need not commute with the limit. PD and predictive information are different properties.

## 7. Explicit four-point obstruction for every bandwidth, and a logarithmic necessary scale

The generic witness in statement 5 can be made completely explicit for q=2, with **only four points for every lambda>0**. This yields a quantitative finite-sample bound.

Put b=exp(-pi^2 lambda), and take equatorial angles 0, b, pi, pi+b. With the unit coefficient vector c=(1,-1,1,-1)/2, the Gram quadratic form is

    h = 1-exp(-lambda b^2)+b-exp[-lambda(pi-b)^2]
      <= lambda b^2 - b lambda(2pi b-b^2)
       = -lambda b^2 (2pi-1-b)
      <= -(2pi-2) lambda b^2 <0.

Here 1-exp(-s)<=s and exp(t)-1>=t were used. Thus N=4 is the smallest possible failing cardinality for the spherical geodesic Gaussian, for every bandwidth; statement 6 explains why N<=3 cannot fail. The four-point configuration varies with lambda.

This obstruction persists whenever each point is moved geodesically by at most **r=b/16**, including movements away from the equator. To verify this quantitatively, every pairwise distance changes by at most 2r=b/8. For the two near pairs, all relevant distances are <=9b/8, so |k'(d)|<=9lambda b/4 and the entry perturbation is <=9lambda b^2/32. For the four far pairs, d>=pi-9b/8 and d<=pi. Since lambda b<=1/(e pi^2),

    exp(-lambda d^2)
      <= b exp[(9pi/4)lambda b]
      <= b exp[9/(4e pi)] < (3/2)b.

Hence |k'(d)|<=3lambda pi b and the far-pair entry perturbation is <=3pi lambda b^2/8. The sum of |c_i c_j| over i!=j is 3. The total quadratic-form perturbation is at most 9pi lambda b^2/8, and therefore the perturbed quadratic form is at most

    -(7pi/8-2) lambda b^2 <0.

The four spherical caps of radius r are disjoint. If independent observations have directional densities bounded **below** by m>0 relative to uniform area, the probability that any particular cap is empty is at most (1-m A(r))^N. Occupying all four caps gives a bad principal submatrix. The union bound therefore gives the nonasymptotic upper bound

    P_N(lambda,2)
      <= min{1, 4[1-m sin^2(exp(-pi^2 lambda)/32)]^N}
      <= min{1, 4 exp[-m N exp(-2pi^2 lambda)/(256pi^2)]}.

For uniform iid S^2, m=1. This upper bound is conservative, but explicit. In particular, if P_N(lambda,2)>=1-epsilon is required, necessarily

    lambda >= [log N + log m
               - log(256pi^2 log(4/(1-epsilon)))]/(2pi^2)

whenever the right side is positive. Thus **a high-probability bandwidth must grow at least logarithmically in N** in this distribution class. More sharply as an asymptotic statement, for any eta>0,

    lambda_N <= (1-eta) log N/(2pi^2)  ==>  P_N(lambda_N,2) ->0.

The same explicit bound, with N replaced by the number M of fresh test points, holds conditional on any positive-probability event determined by the training sample, because the fresh test-only principal submatrix must also be PD. This is a quantitative append-failure theorem, not just existence of a bad configuration. An independent validation set may be included in the conditioning information by the same argument; for a bandwidth selected from a finite grid, apply the bound conditional on each selected value.

The projected Gaussian classes also satisfy a uniform lower-density condition. If a=||mu||=sqrt(3)/2, the directional density relative to uniform sphere area is

    f_mu(u)=sqrt(2/pi) exp(-a^2/2)
             integral_0^infinity s^2 exp(-s^2/2+s mu.u) ds.

Restricting the integral to 0<=s<=1 gives the explicit bound

    f_mu(u) >= m_0 = [sqrt(2/pi)/3] exp[-a^2/2-1/2-a] >0.

Both signs of mu have this bound, so the upper probability bound applies even to the independently sampled, fixed balanced class design. For a sufficient bound one instead needs an upper density bound as in statement 4; compactness and the displayed formula ensure that one exists.

For any full-support sampling distribution, these robust four-point caps have positive mass. Conversely, N distinct points on a sufficiently short great-circle arc have a strictly PD Gaussian matrix, since their distances are Euclidean line distances; by continuity their neighborhoods are also good. Consequently for **q=2, N>=4 and every fixed lambda>0**, one has

    0 < P_N(lambda,2) <1

under iid full-support sampling. A measured 100% finite success rate is therefore never an exact probability-one theorem in this setting. At N<=3 the exact probability is one.

Together, the proved explicit bounds leave a large gap: necessary order log N and sufficient order N^2 on uniform S^2. They do not prove the measured intermediate scaling. The limits do not commute: at each fixed N, P_N tends to 1 as lambda tends to infinity, while at each fixed lambda it tends to 0 as N tends to infinity; taking these two limits in opposite orders gives 1 and 0. For q=1 both limits are one.

This section is a self-contained derivation. The global obstruction itself is already known from Gneiting and related work; priority is not claimed for four-point witnesses or elementary occupancy bounds. No matching finite-sample scaling theorem was located in the bounded literature audit.

## 8. Dimension-dependent sufficient and necessary orders on S^d

The packing argument extends to every fixed d>=1. Normalized cap area is

    A_d(r) = [integral_0^r sin^(d-1)(theta) dtheta]
             / [integral_0^pi sin^(d-1)(theta) dtheta],
    kappa_d = Gamma((d+1)/2) / [d sqrt(pi) Gamma(d/2)].

Since sin(theta)/theta decreases on (0,pi), cap-volume ratios satisfy A_d(R)/A_d(r)<=(R/r)^d for 0<r<=R<=pi. Clamping an outer radius to pi preserves this bound. The annular count in statement 3 is consequently at most (2k+3)^d-1. Any C_d satisfying

    sum_{k>=1} [(2k+3)^d-1] exp(-C_d k) <1

gives deterministic PD when lambda delta^q>=C_d, q>=1. One fully explicit choice is C_d=log(2*5^d+2^d): using 2k+3<=5k and k<=2^(k-1), the row-sum bound is at most 1/2. The sharper C_2=log(26) is available from statement 3.

Also A_d(r)<=kappa_d r^d. Thus for independent density-upper-bounded (by M) observations, whenever the chosen r is <=pi,

    lambda >= C_d [M kappa_d N(N-1)/(2 epsilon)]^(q/d)
       ==> Pr[PD]>=1-epsilon.

For uniform S^d this proves the sufficient order **N^(2q/d)** at fixed confidence: N^2 for q=2 on S^2, N^(4/3) on S^3. This is not the measured transition order. For q<=1 the exact sphere theorem remains stronger than these sufficient bounds.

The four-point construction and its robust cap radius in statement 7 work on every S^d. For a lower density bound m>0,

    P_N(lambda,2) <= min{1, 4 exp[-m N A_d(exp(-pi^2 lambda)/16)]}.

On 0<=r<=pi/2, sin(theta)>=2theta/pi gives A_d(r)>=kappa_d (2/pi)^(d-1) r^d. Consequently the necessary growing-bandwidth order in dimension d is at least log N/(d pi^2), up to an additive constant depending on d, m, and the target confidence. This gives explicit geometry dependence in both bounds without claiming that either is sharp.

## 9. Exact spread constants for the paper's balanced Gaussian design

For the two projected N(+mu,I_3), N(-mu,I_3) classes, write a=||mu|| and t=mu.u. If J(t)=integral_0^infinity exp(-s^2/2+ts) ds, then J'(t)=tJ(t)+1 and J''(t)=(1+t^2)J(t)+t. Also J(t)+J(-t)=sqrt(2pi)exp(t^2/2). Averaging the two directional densities from statement 7 gives the especially simple mixture density, relative to uniform spherical area,

    f_mix(u) = (1+t^2) exp[(t^2-a^2)/2].

Hence its exact extrema are

    m_mix=exp(-a^2/2),   M_mix=1+a^2.

For the paper's mu=(1/2,1/2,1/2), these are exp(-3/8) and 7/4. They can be used even though the experiment fixes exactly N/2 points in each class:

- For any cap with class probabilities p_+ and p_-, the probability it is empty is [(1-p_+)(1-p_-)]^(N/2) <= [1-(p_++p_-)/2]^N <= [1-m_mix A(r)]^N, by AM-GM. Thus the necessary/append bounds of statement 7 apply with m=m_mix.
- Let I_same and I_cross denote pair-close probabilities for same and opposite classes. Symmetry makes the two same-class probabilities equal. The expected number of close unordered pairs is (N/2)(N/2-1)I_same+(N/2)^2 I_cross <= (N^2/2) Pr_mix[d(X,Y)<=r] <= (N^2/2) M_mix A(r).

Consequently the **balanced-design sufficient condition** is

    r=acos(1-4epsilon/[M_mix N^2]),
    lambda>=log(26)/r^q  ==>  Pr[PD]>=1-epsilon, q>=1.

The balanced-design necessary upper bound for q=2 is

    Pr[PD] <= min{1,4[1-m_mix sin^2(exp(-pi^2 lambda)/32)]^N}.

These are explicit geometry-and-spread bounds for the actual Fig.1 design, although they are far too conservative to locate its observed transition.

The Bayes decision boundary after projection remains sign(mu.u): the sign of the difference of the two radial integrals is the sign of t. Projection preserves the sign of mu.Z, and mu.Z under the positive class is N(a^2,a^2). Therefore the exact Bayes accuracy is Phi(a)=Phi(sqrt(3)/2), about 80.676%. This benchmark has no Monte Carlo or fitted-parameter uncertainty.

## 10. An explicit finite-N probability envelope for uniform S^2

For q=2, let C=log(26). If lambda>=C/pi^2, set r=sqrt(C/lambda). The separation/packing argument gives

    P_N(lambda,2) >= max{0,1-N(N-1)(1-cos r)/4}.

For smaller lambda use the trivial lower bound zero. This is an explicit sufficient-probability curve, not only a threshold formulation.

For an upper curve valid at every lambda>0, put A=sin^2(exp(-pi^2 lambda)/32). The four robust bad caps in statement 7 are disjoint and have equal normalized area A. Inclusion-exclusion gives the **exact probability that at least one cap is empty**:

    U_N = 4(1-A)^N - 6(1-2A)^N + 4(1-3A)^N - (1-4A)^N.

Therefore P_N(lambda,2)<=U_N. This is strictly below one for N>=4, although the gap can be extraordinarily small. It improves the union-bound upper curve when that bound is vacuous. The formula is an exact real expression; direct binary64 evaluation suffers cancellation for tiny A and should not be used to claim a resolved gap from one. It is not the exact P_N, because configurations other than these four-cap patterns can also fail.

Together these formulas form an explicit finite-N lower/upper envelope. In the empirically relevant lambda range it remains very wide; the measured transition is much more informative there. The conditional append probability for M independent uniform test points is at most U_M, by the test-only principal-submatrix argument.
