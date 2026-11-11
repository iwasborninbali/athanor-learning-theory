**Adversarial verification — Feragen–Hauberg finite geodesic Gram matrices**

Verifier: fresh independent gpt-6.1-sol, Athanor. Audit date: 11 November 2026 (Asia/Makassar). All mathematics below concerns strict PD, unit-radius spheres, positive bandwidth, and distinct points. Probability statements additionally retain the sampling assumptions stated beside them.

**Overall verdict: holds as a conservative partial result.** The central proofs survived the audit. Independent directed-interval calculations reproduce the full `297/300` headline training count and support the append-failure measurements. No central theorem or headline number was found wrong. The report does not resolve the sharp transition law or the general learning conjecture. There are **gaps** in priority coverage and in identifying the original figure's protocol; neither undermines the proved bounds.

| Claim | Verdict | Scope |
|---|---|---|
| `lambda delta^q >= log(26)` on `S^2`, `q>=1` | holds | Deterministic strict PD, including equality. |
| Sufficient `N^q` and `N^(2q/d)` thresholds | holds | Orders of the constructed sufficient thresholds; no matching necessity. |
| Four-point obstruction and logarithmic necessary bandwidth | holds | Correct at every positive bandwidth for `q=2`, under the stated density conditions. |
| Fixed-bandwidth eventual append failure | holds | Fresh independent points and the stated conditioning assumptions are essential. |
| `0<P_N(lambda,2)<1` for `N>=4` | holds | Full-support iid sampling; the probability-one small-N comparison assumes no ties. |
| Projected-Gaussian spread and Bayes constants | holds | The balanced-design arguments justify using mixture constants. |
| Gneiting attribution for `0<q<=1` | holds | Explicit prior art, including strictness. |
| `0.1664 sqrt(N)-0.1884` transition fit | holds | Descriptive fit on five finite-N brackets; an asymptotic interpretation remains a gap. |
| `297/300`, `0/297` append survival, about `79.2%` accuracy | holds | Training count fully independently certified; append and classifier independently sampled, complete record totals also checked. |
| Numerical certificates | holds | Selected exact signs independently confirmed; the complete production grid was not recertified. Separated floating screens retain their stated qualification. |
| Original Fig.1 discrepancy | holds | Under the standard uniform `S^2`, unnormalized angular-kernel interpretation. Its actual cause remains a gap. |
| Novelty/priority | gap | Relevant 2019/2020 empirical predecessor omitted; priority for the particular bounds is unestablished. |

**Proof audit.** I read every argument in `../b02-geokernel/theory.md`, including the auxiliary statements, against the following line ranges. I found no algebraic or logical error in its principal bounds.

| Lines | Verdict | Check |
|---|---|---|
| 3–13 | holds | The strict/semidefinite distinction is necessary and correctly maintained. Gneiting's Theorem 7 gives strict PD, not merely semidefiniteness; his Example 1 gives exactly the stated powered-exponential range. The Euclidean Gaussian Fourier argument gives strictness for distinct points. |
| 17–25 | holds | Each off-diagonal entry is at most `exp(-lambda delta^q)`, so strict row dominance follows from the displayed strict inequality. Conditional on one sample point, a pair-close probability bound and the union bound give the probability statement; independence of different pairs is unnecessary. |
| 29–46 | holds | The cap packing count, saturation at radius pi, geometric series, and strict eigenvalue margin all check. Details below. |
| 50–62 | holds | `Pr[d(X_i,X_j)<=r] <= M sin^2(r/2)`. Multiplying by `N(N-1)/2` and solving gives the stated `r_epsilon`. Its asymptotic expansion is `sqrt(8 epsilon/M)/N`, yielding sufficient order `N^q`. The same separation event works for every larger bandwidth and every subset. Radius scaling is `R^-q`. |
| 64–72 | holds | The factorial-moment argument correctly counts distinct unordered edges. A connected component with at least three vertices gives `v>2c`; a spanning forest suffices for the small-ball upper bound. Disjoint edges give the Poisson factorial moments with mean `t^2/8`. This establishes the separation limit and the displayed liminf bound, not a PD transition law. |
| 76–88 | holds | Gneiting's global failure at each fixed bandwidth provides a strict finite negative witness. Coincident witness locations can be merged before choosing disjoint neighborhoods. Continuity, independent ordered blocks, and the principal-submatrix criterion give the exponential upper bound. Fresh test-only blocks are independent of a training event, so conditioning does not invalidate it. |
| 92–100 | holds | The equatorial square has the displayed alternating eigenvalue. Its derivative at zero is `pi^q(2^(1-q)-1)<0`. For `q=2`, `1-2t+t^4` is the correct polynomial. Every distinct three-point metric embeds in the plane, including degenerate triangles, so three points cannot fail. Dividing a sum-zero quadratic form by lambda extends continuously to zero. The finite-cover argument then handles all bandwidths in `(0,L]` simultaneously. |
| 102–108 | holds | Integer entrywise powers preserve PD by Schur products; a finite PD check does not justify arbitrary real powers. The `q -> 0` limit retains diagonal one and off-diagonal `exp(-lambda)`. The SVM equality constraint makes the limiting off-sample prediction constant. The text correctly declines to interchange a sign operation and a zero limit. |
| 114–121 | holds | Direct expansion of the quadratic form gives exactly `h=1-exp(-lambda b^2)+b-exp[-lambda(pi-b)^2]`. Both exponential inequalities have the correct direction and give the claimed negative bound for every lambda. |
| 123–131 | holds | All six unordered pairs are accounted for: two near and four far. The derivative estimates, perturbation weight sum, and final negative margin are valid. Details below. |
| 133–148 | holds | Occupying the four disjoint caps forces a negative principal submatrix. Each cap-empty probability is bounded separately; no independence between cap occupancy events is assumed. The sine bound, exponential relaxation, inversion for lambda, and the conditional append argument are all valid. |
| 150–159 | holds | Radial integration of the three-dimensional Gaussian gives the displayed density relative to normalized spherical area. Restricting the radial integral to `[0,1]` gives the stated positive lower bound. The two fixed classes are independent observations with possibly different densities, which is sufficient here. |
| 161–169 | holds | Short arcs give good finite configurations, continuity gives open good neighborhoods, and full support gives their positive probability. The bad neighborhoods give probability strictly below one for `N>=4`. The two iterated limits differ as stated. The probability-one assertion for `N<=3` requires nonatomic sampling or an explicit distinctness condition, as supplied in `result.md`; full support alone does not exclude ties. |
| 173–190 | holds | The cap-volume comparison, explicit `C_d`, small-ball constant, and sufficient order `N^(2q/d)` are correct, including `d=1`. These are sufficient upper bounds on a required bandwidth, not matching asymptotic orders. |
| 192–196 | holds | The same four-point witness lies on a great circle in every `S^d`. Integrating `sin(theta)>=2theta/pi` gives the stated cap lower bound and necessary leading term `log N/(d pi^2)`. |
| 200–222 | holds | The mixture density and its extrema are correct. AM–GM correctly handles fixed balanced class counts for cap emptiness. The pair-close expectation has `N(N-2)/4` same-class pairs and `N^2/4` cross-class pairs, giving the stated conservative sufficient bound. |
| 224 | holds | The projected likelihood ratio has the sign of `mu.u`. Since `mu.Z` in the positive class is `N(a^2,a^2)`, the exact Bayes accuracy is `Phi(a)`. |
| 228–240 | holds | The lower envelope is the separation union bound. The four caps are disjoint, so the inclusion–exclusion formula is exactly the probability that at least one is empty. For `N>=4` the complementary occupancy event has positive probability. Cancellation in binary64 can conceal its small gap from one, as the text explicitly warns. |

The strict-PD attribution is directly supported by [Gneiting (2013), Theorem 7 and Example 1](https://arxiv.org/html/1111.7077). His notation `Psi_d^+` means strict PD on distinct points. Setting his scale `c=lambda^(-1/q)` gives the claimed kernel. Example 1 also excludes **every** positive scale for `q>1`, by Theorem 8. This is established prior theory.

For the packing step, let `t=delta/4`, `m=2k+3`. The shell caps of radius `delta/2`, together with the cap centered at the row's point, are pairwise disjoint and lie inside radius `(k+3/2)delta`. Below saturation, the area ratio is `sin^2(mt)/sin^2(t)<=m^2`. Above saturation, `mt>pi/2` and `m sin(t)>=m sin(pi/(2m))>=1`, so the total-sphere ratio is still at most `m^2`. Subtracting the row center's cap justifies the `-1`. No sharper annular-area estimate is needed; overcounting each shell is harmless. Independently using rational arithmetic,

```
sum_{k>=1} (4k^2+12k+8) z^k = 8z(3-3z+z^2)/(1-z)^3,
z=1/26: sum=15608/15625; 1-sum=17/15625.
```

Thus equality in `lambda delta^q >= log(26)` still gives a strictly positive Gershgorin margin. There is no lost strict inequality at the boundary.

For the four-point witness, `0<b=exp(-pi^2 lambda)<1`. The exact form is

```
h = (1-exp(-lambda b^2)) - b*(exp(lambda*(2pi b-b^2))-1)
  <= lambda b^2 - lambda b*(2pi b-b^2)
   = -lambda b^2*(2pi-1-b)
  <= -(2pi-2)*lambda b^2.
```

Moving each point by `b/16` changes a pair distance by at most `b/8`. Near-pair entry errors are at most `9 lambda b^2/32`. On the far-pair interval, `lambda b<=1/(e pi^2)` gives `exp(-lambda d^2)<(3/2)b`; hence far-pair entry errors are at most `3pi lambda b^2/8`. Every coefficient has magnitude `1/2`, so the sum of ordered off-diagonal absolute coefficient products is `12/4=3`. Bounding all errors by the far-pair maximum gives `9pi lambda b^2/8`. The remaining upper bound is `-(7pi/8-2)lambda b^2<0`. The construction is robust in all spherical directions, not only along the equator.

The four cap radii are `r=b/16` and their minimum center separation is `b`, so the caps are disjoint. Their `S^2` area is `A=sin^2(b/32) >= b^2/(256pi^2)`. Therefore

```
P_N <= min(1, 4(1-m A)^N)
    <= min(1, 4 exp[-m N exp(-2pi^2 lambda)/(256pi^2)]).
```

If `P_N>=1-epsilon`, the second upper bound must also be at least `1-epsilon`. Taking logarithms gives precisely the displayed necessary bandwidth inequality. This reasoning does **not** infer sufficiency from the obstruction. Replacing N by the fresh-test count is legitimate because the test-only matrix is a principal submatrix of the combined matrix. The resulting fixed-bandwidth limit is zero even conditional on training PD. The constants are so conservative that this theorem alone does not predict failure after 100 points at lambda 2.5.

For the dimension extension, write the cap integral after the substitution `theta=r u`. The decreasing function `sin(theta)/theta` implies `A_d(R)/A_d(r)<=(R/r)^d`. Clamping to pi also preserves the comparison. With `z=exp(-C_d)` and `C_d=log(2*5^d+2^d)`,

```
sum [(2k+3)^d-1] z^k
 <= 5^d sum k^d z^k
 <= 5^d z/(1-2^d z) = 1/2.
```

Also `A_d(r)<=kappa_d r^d`, where `kappa_d=Gamma((d+1)/2)/(d sqrt(pi) Gamma(d/2))`. Combining this with the pair union bound gives the stated sufficient threshold. The lower cap bound at `r=exp(-pi^2 lambda)/16` gives `N exp(-d pi^2 lambda)` in the necessary bound. Both exponents and all factors of two check.

For the spread calculation, differentiation of `J(t)` gives `J''(t)=(1+t^2)J(t)+t`. Adding the two signs cancels t and uses `J(t)+J(-t)=sqrt(2pi) exp(t^2/2)`. The mixture density is therefore `(1+t^2)exp((t^2-a^2)/2)`, increasing in `t^2`. Its minimum is `exp(-a^2/2)`, its maximum `1+a^2`. These are mixture constants; the text correctly supplies separate arguments before using them with exactly balanced classes. For that design the sufficient radius uses `N^2`, not `N(N-1)`.

**Priority audit.** The correct separation is between a kernel being PSD on **every** finite configuration and the probability that a **particular random finite** Gram matrix is strictly PD.

| Primary source | What it establishes or already does | Effect on the present claims |
|---|---|---|
| [Feragen, Lauze & Hauberg (CVPR 2015)](https://openaccess.thecvf.com/content_cvpr_2015/papers/Feragen_Geodesic_Exponential_Kernels_2015_CVPR_paper.pdf), Theorems 1–4 | Restrictions on global validity for all bandwidths; the CND route for the Laplacian. | Prior art for the global obstruction framework and sphere Laplacian. Its quantifiers do not imply `P_N=0` at finite N. I did not find the stated finite-sample probability bounds there. |
| [Gneiting (2013)](https://arxiv.org/html/1111.7077), Theorem 7, Example 1 | Exact powered-exponential strict-PD range on spheres, and exclusion at every bandwidth above that range. | The entire `q<=1` control and fixed-bandwidth global failure are prior art. The iid eventual-failure argument is an elementary consequence, rather than a new global theorem. |
| [Da Costa, Mostajeran & Ortega (2023)](https://arxiv.org/html/2302.10623v1), Theorem 4.1 | A circulant, equally spaced circle construction with a negative eigenvalue once its size is sufficiently large, and extensions via circle embeddings. | Directly relevant obstruction prior art. Its displayed proof uses growing cardinality; it is not the present four-point construction or its random cap-occupancy bound. |
| [Li (2023 preprint; BLMS 2024)](https://arxiv.org/html/2303.06558v1), Main Theorem | Global Gaussian failure on non-simply-connected closed manifolds. | `S^2` does not satisfy the topological hypothesis. This does not resolve finite random PD probabilities; circle/sphere failure was already known independently. |
| [Da Costa et al. (2023/2024)](https://arxiv.org/html/2310.19270v2), Section 5; [Azangulov et al. (JMLR 2024)](https://jmlr.org/papers/volume25/22-1434/22-1434.pdf), p.5 | Global non-PD results on compact symmetric spaces, with broader harmonic-analysis results and some numerical low-dimensional cases. | Statements about solving the open problem use global-kernel quantifiers. They do not contradict finite good neighborhoods or supply the claimed `P_N` law. |
| [Jaquier et al. (CoRL 2019; PMLR 2020)](https://proceedings.mlr.press/v100/jaquier20a/jaquier20a.pdf), Section 4.1, Figure 2, Appendix A | Repeated finite-sample PD-frequency/eigenvalue experiments and a selected minimum admissible coefficient, including a table for several spheres. Uses 500 points and ten repetitions; reports `beta_min=6.5` on `S^2`. | A material omission from the target's priority discussion. Empirical admissible-bandwidth calibration and dimension comparisons predate 2026. Different sampling and numerical precision prevent direct comparison of its coefficient with the present uniform-sphere fit. This source does not supply the present rigorous probability bounds. |
| [Dalle Vedove et al. (2026)](https://arxiv.org/html/2610.01910), Section IV-C, Algorithm 3 | Sample-dependent length-scale bisection and a Monte Carlo calibration suggestion. | Further prior art for the experimental procedure. Bisection itself is not a proof of finite-matrix monotonicity. |

**Priority verdict: gap.** No matching explicit `log N` necessary bound or `N^(2q/d)` sufficient probability theorem was located in the primary sources reviewed or targeted searches. That is not a priority proof. The target already declines priority for its elementary techniques and four-point witnesses, appropriately. Its account of experimental predecessors should add Jaquier et al.; numerical bandwidth calibration and useful finite learning experiments are established approaches. The new report may be described as a self-contained quantitative partial answer, but not as the first finite-sample empirical investigation after 2016.

**Independent numerical audit.** I wrote [independent_interval.cpp](independent_interval.cpp), [independent_audit.py](independent_audit.py), and [independent_postcheck.py](independent_postcheck.py). None imports or calls the target's Python, C++, shared libraries, classifier, or certificate routines. Saved coordinates and recorded decisions are treated as data. The independent generator uses seed `60261111`.

The independent certificate uses MPFR-directed interval **Cholesky with square roots**, rather than the target's interval LDL or binary128 certificate. It encloses the exact normalized directions of the raw dyadic coordinates and the exact stored binary64 bandwidth, including norms, dot products, acos, and exp. Every previous pivot has a strictly positive lower endpoint before elimination continues. All positive pivots prove strict PD; a strictly negative pivot after positive pivots proves a negative eigenvalue by the Schur-complement inertia identity. Pivot intervals in the records are **not** claimed to be eigenvalue bounds. Generic four-corner interval multiplication provides a different arithmetic implementation from the target's sign-specialized product code.

For well-separated low-N cases I used a binary64 spectrum with an explicitly reported margin. These are numerical checks, not formal interval certificates. All 300 headline training signs, the sampled append signs, and the selected hard 400-point signs are independently interval-certified. [independent_decisions.jsonl](independent_decisions.jsonl) retains every decision and the final pivot enclosure. The two summary JSON files retain aggregates, source hashes, convention checks, and CPU use.

**Numerical certification verdict: holds within the audited scope.** The target's full interval algorithm uses valid directed enclosures and symmetric pivoting. Its negative fast path verifies a dyadic Rayleigh witness against exact-kernel intervals, so correctness does not rely on its approximate negative pivot. The positive fast path's structure is also sound: a backward-error bound, a verified inverse residual, a Frobenius upper bound, and Weyl's inequality. The coarse factors in its stated bounds dominate ordinary dot-product and conversion errors at the recorded sizes. This retains the documented assumptions on IEEE basic arithmetic and the installed BLAS; it is not a formal proof of the vendor's implementation. The independent full interval checks avoid dependence on that BLAS certificate. The target explicitly says that separated binary64 screens are not formal interval certificates, and that qualification must be retained. I did not independently recertify its entire production grid.

**Figure conventions.** The [original 2016 paper](https://proceedings.mlr.press/v49/feragen16.pdf), equation (1) and Figure 1, declares the exponential with a shortest-path metric on a unit sphere. Its rendered horizontal axes explicitly say `x=log10(lambda)`. The left axis runs from -0.2 to 1.2 and the negative trough is shallow. There is no declared eigenvalue normalization. The left caption itself does not state the ambient dimension; `S^2` is the natural interpretation in conjunction with the three-coordinate right-panel design, rather than an explicit separate left-panel parameter specification.

Changing radius, radians to normalized angles, or a constant in the Gaussian exponent changes the effective bandwidth `lambda_eff=lambda R^2` and translates a log-bandwidth curve horizontally. Changing log base reparameterizes the horizontal axis. None changes the trough depth over the full positive bandwidth range. Degrees move the negative region far left and would also move the PD/identity transition, contrary to the published horizontal scale. The chord Gaussian and `q=1` kernels are globally strictly PD, so their exact spectra cannot produce a substantial negative trough.

A bandwidth-dependent normalization is a different possibility: `D^-1/2 K D^-1/2`, with `D_ii=sum_j K_ij`, or `K/lambda_max(K)` preserves inertia and still approaches I as bandwidth tends to infinity. Such a normalization can substantially shrink the negative trough while retaining the identity limit. It is not the matrix `[exp(-lambda d_ij^2)]` declared in the paper, and I found no source establishing that it was used. Alternative sampling can also alter the curve.

I independently downloaded the original PDF from PMLR and rendered page 3. Its SHA-256 is `ec4c8644ed58f0469f07570a61f825bb9b5c99abce8294f5c1bd40d04028c50a`, exactly matching the target's saved original. The local files are [original_feragen2016.pdf](original_feragen2016.pdf) and [original_page3.png](original_page3.png).

The independent **100 fresh uniform `S^2` samples**, each with N=100, give at lambda 0.1:

```
mean minimum eigenvalue = -1.0776660
sample standard deviation = 0.0627980
standard error of the mean = 0.0062798
2.5%, 50%, 97.5% sample quantiles = [-1.214678, -1.065051, -0.988473]
```

This independently supports the target's mean `-1.0808` and the scale discrepancy. These eigenvalues are separated from zero by roughly a unit, so interval subtleties cannot explain it.

The convention sweep uses one new N=100 cloud over 201 log-spaced coefficients from `10^-4` to `10^6`; these are illustrative numerical comparisons, not fits to digitized original data.

| Computation | Minimum over the sweep | Coefficient at that minimum | Interpretation |
|---|---:|---:|---|
| Unit-sphere angular distance | -1.07749 | 0.08913 | Standard stated interpretation. |
| Angular distance divided by pi | -1.07790 | 0.89125 | Trough moves horizontally, retains its depth. |
| Radius one half | -1.07728 | 0.35481 | Same conclusion. |
| Angles in degrees | -0.04627 at the left endpoint | 0.0001 | Deep trough has moved outside the plotted interval; the PD transition also moves far left. |
| Symmetric row normalization | -0.01408 | 0.11220 | Can suppress the negative scale and retain the identity limit, but is undeclared. |
| Divide by largest eigenvalue | -0.01404 | 0.11220 | Another undeclared normalization with that property. |
| Normalize `Uniform([0,1]^3)` vectors | -0.03094 | 0.08913 | A concrete sampling-error hypothesis: points occupy only the positive octant and are not uniform on `S^2`. |

The positive-cube example is particularly suggestive: at lambda 0.1 its eigenvalue is `-0.03012`, and the eigenvalue first exceeds 0.99 near lambda `7.94e4`. This resembles both the published trough and its late identity plateau. It **does not establish that the authors used this generator**. A uniform sphere in `R^100` can also have a shallow trough (`-0.03036` in one trial), but reaches 0.99 by lambda about 3.55, inconsistent with the original late plateau. Thus an unspecified higher dimension does not explain both features in this check. No declared radius, log-base, or ordinary distance convention recovered the original curve. Original experiment code would be needed to distinguish normalization from a different sampling implementation or another cause.

**Recomputed frequencies and accuracy.** Counts below are from my code, not imported target computations.

| Sampling / dataset | N | lambda | Independently recomputed PD count | Arithmetic |
|---|---:|---:|---:|---|
| Saved uniform `S^2` clouds | 25 | 0.625 | 147/300 | Separated binary64 spectra. |
| Same | 25 | 0.65 | 196/300 | Separated binary64 spectra. |
| Same | 25 | 0.75 | 296/300 | Separated binary64 spectra. |
| Saved uniform `S^2` clouds | 50 | 0.975 | 129/300 | Separated binary64 spectra. |
| Same | 50 | 1.0 | 186/300 | Separated binary64 spectra. |
| Same | 50 | 1.1 | 293/300 | Separated binary64 spectra. |
| All saved balanced projected-Gaussian training sets | 200 | 2.5 | **297/300** | All 300 signs certified with independent 256-bit directed intervals. |
| Predetermined saved subset, appending 100 balanced test points | 300 combined | 2.5 | **0/29**, conditional on training PD | All 29 combined signs independently certified. |
| Fresh balanced projected-Gaussian training sets | 200 | 2.5 | **19/20** | Independent generator and directed-interval signs. |
| Fresh successful training sets plus 100 fresh points | 300 combined | 2.5 | **0/19** | Independent directed-interval signs. |

There are no disagreements with the recorded decisions in the six low-N frequency checks or the full training check. The three independently confirmed negative training repetitions are 110, 244, and 256, using zero-based indices. The fixed append audit selected repetitions `0,10,...,290` before examining extension certificates; repetition 110 is excluded by its negative training sign, leaving 29. Appends take the first 50 test points from each class.

Directly tallying all saved headline records gives 297 successful training sets, zero append-100 survivors among them, and `94081/(297*400)=79.1927609%` test accuracy. This checks the aggregate arithmetic; it is **not** an independent recertification of all 297 extensions or a refit of all classifiers. My separate C-SVM dual optimization uses SciPy SLSQP, C=1, an intercept recovered from free support vectors, and repetitions `0,30,...,270`. All ten optimizations succeed. Their individual test-correct counts agree exactly with the saved classifier counts, and their average accuracy is **79.025%**. The largest dual equality-constraint residual is `8.3e-11`.

For the transition fit, I independently rebuilt every saved all-PD suffix and its median bracket from the raw JSONL decisions. The five median brackets are `[0.625,0.65]`, `[0.975,1]`, `[1.475,1.5]`, `[2.15,2.175]`, and `[3.125,3.15]`. Least squares on their midpoints gives

```
lambda_50 = 0.166407773258253 sqrt(N) - 0.188362802286152,
raw-scale RMSE = 0.006151411109487.
```

Thus the reported arithmetic holds. This recomputation uses recorded decisions at the larger sizes; the independent hard-sign sample below checks only selected entries there. I did not rerun the bootstrap. Neither five brackets nor bootstrap uncertainty proves a square-root asymptotic law; the target correctly describes the fit as finite-range and exploratory.

**Hard sign checks.** All four following decisions resolve at 256 bits with the independent interval implementation:

| N | Saved repetition | lambda | Own binary64 minimum eigenvalue | Exact sign from independent intervals |
|---:|---:|---:|---:|---|
| 400 | 0 | 3.25 | `9.44e-16` | positive |
| 400 | 1 | 3.25 | `7.07e-16` | positive |
| 400 | 12 | 3.25 | `-9.94e-18` | negative |
| 400 | 0 | 3.075 | `-2.71e-15` | negative |

For example, the final pivot for repetition 0 at 3.25 is enclosed in `[1.9902137595036009e-16, 1.9902137595036010e-16]`, after all prior pivots are certified positive. The final pivot for repetition 12 is enclosed in `[-3.967407095724442e-15,-3.967407095724441e-15]`. The saved negative binary64 value for repetition 1 is about `-2.63e-15`; my algebraically equivalent floating evaluation gives the positive value in the table, while both independent interval calculations establish PD. Floating expression evaluation order can affect an unresolved raw sign.

Rebuilding **all 80** N=400 matrices at lambda 3.25 with the target's stated exponent evaluation order, but my own code, reproduces **31/80 raw positive eigenvalues** and **0/80 above the declared binary64 tolerance**. The full record tally is 77/80 certified PD. Only the selected cases in the table were independently recertified here; I do not claim a fresh 80-case interval audit.

Additional independent 512-bit four-point tests at lambda `0.01, 1, 2.5, 10` all certify a negative eigenvalue, including the exponentially tiny-angle case at lambda 10. Radial quadrature independently matches the Gaussian mixture density at `t=0,a/2,a`, giving respectively `0.687289278791`, `0.896372027362`, and `1.75`. The exact Bayes benchmark evaluates to `80.6761884614%`. The sufficient thresholds at N=200, epsilon=0.05 recompute as `324180.3340` for uniform sampling and `570166.6226` for the balanced Gaussian design.

**Audit limits and reproducibility.** Main computation: `854.081` CPU seconds. Postchecks: `2.880` CPU seconds. Together with the initial benchmark, compilation, and PDF rendering, the work used about **14.4 CPU-minutes**, comfortably below 20; only one numerical process ran at a time. Wall time was well below two hours. No installations, paid calls, VM, publication, or messages to other people were used. All new artifacts are inside this folder. Core outputs are [independent_summary.json](independent_summary.json), [independent_postcheck.json](independent_postcheck.json), and [independent_decisions.jsonl](independent_decisions.jsonl). Source hashes in the postcheck JSON identify the files audited. The code header records the local compilation command.
