# Eigenvalue decisions and certificates

## Exact object and floating screen

Saved coordinates are the actual binary64 Gaussian draws before projection. The mathematical points used for signs are the **exact normalized directions of these dyadic coordinates**. MPFR evaluates dot products, norms, acos and exp with directed rounding, so projection and kernel-entry error are included. The coefficient lambda is the exact binary64 value stored in JSON and passed to MPFR; this fixes the decimal-to-binary convention as well. The main binary64 matrix uses the equivalent stable half-angle formula `2 atan2(||u-v||,||u+v||)` after binary64 normalization. Its diagonal is set to exactly one.

SciPy `eigh`, driver `evr`, computes the smallest eigenvalue. The installed wrapper uses LAPACK DSYEVR with its default internal `abstol=0.0` (no user override); the tolerance below is the decision threshold, not an asserted eigenvalue error returned by LAPACK. The local SciPy wrapper documentation and call path were inspected. With eps64=2^-52, the declared screen is

    tau = 32 N eps64 max_i sum_j |K_ij|.

Values below -tau are separated negative; above tau are separated positive; values within [-tau,tau] are numerically uncertain **before** further checking. This deliberately conservative screen is not a machine-checked theorem about the vendor eigensolver or libm. We do not represent every separated screen decision as a formal interval certificate. Every borderline q=2 sign is separately resolved by one of the following rigorous entry/error-bound calculations; unresolved cases, if any, retain status zero. q=1 and Euclidean Gaussian signs are instead fixed by strict-PD theorems, even if their numerical matrix is poorly conditioned. There is no diagonal jitter, eigenvalue clipping, or replacement of a tiny negative eigenvalue by zero.

## Full directed interval LDL

`interval_kernel.cpp`, compiled against the already-installed MPFR and GMP, encloses all entries and performs symmetric-diagonal-pivoted LDL elimination entirely with directed intervals. Every previous pivot must have positive lower endpoint. A pivot with negative upper endpoint proves non-PD; all positive lower endpoints prove PD. An interval containing zero triggers increased precision (128, 256, then 512 bits). The exact pivot order can depend on precision; each chosen order is a valid congruence and does not affect the proof. Multiplication handles all sign combinations, squaring has a separate interval formula, and divisors must have strictly positive lower endpoint.

The source, compilation command and recorded endpoints are retained. Raw sample arrays and lambda determine every input exactly. Replaying the code is an audit; it is distinct from the independent statistical checker.

## Faster certificate, cross-checked against full interval LDL

The full method above resolved the pilot and the first production repetitions. It was slow on 300- and 400-point matrices. A faster, independently checkable a posteriori bound was then added without changing samples, grids, classifiers, or selection. It uses the same MPFR-directed geometry, cached by exact input coordinates and precision, and `__float128` elimination from the already-installed GCC/libquadmath. No package was installed. `fast_kernel.cpp` is compiled with `-ffp-contract=off -fno-fast-math`.

### Negative certificate

An approximate LDL negative pivot proposes a vector. A triangular solve constructs it, it is scaled, rounded to binary64 and returned in the original point order. This is only a candidate witness. MPFR directed intervals then enclose **the exact quadratic form of that dyadic vector and the exact geodesic kernel**. Only a strictly negative upper bound authorizes a negative result (`mpfr_interval_rayleigh`). Failure to obtain this bound invokes full interval LDL. Thus the correctness of the approximate factorization is not needed for negative certification.

### Positive certificate: backward error plus verified inverse bound

Let B be the point matrix given to binary128 elimination, and K the exact kernel. An initial entrywise bound eta_0 on |K-B| includes the MPFR entry interval widths and a conservative 2^-100 allowance for conversion using two binary64 chunks. This allowance is larger than the conversion error: the first chunk has 53 significant bits, the residual supplies another 53, and binary128 has 113. K's entries are in [0,1].

Use u=2^-112, conservatively twice the binary128 unit roundoff. Let A_max>=1 bound every stored elimination entry and L_max>=1 bound every computed multiplier. Both are recorded and rounded upwards. All computed pivots D_j must be positive. The point elimination performs

    l_i = fl(b_ki / d_k),
    p_ij = fl(l_i b_kj),
    b_ij(new) = fl(b_ij - p_ij).

The division relation gives |b_ki-l_i d_k| <= u A_max, allowing a still smaller absolute underflow error. Each update differs from b_ij-l_i l_j d_k by at most

    u A_max (1+4 L_max),

by bounding the product, subtraction and the substitution b_kj=l_j d_k plus its division error. Telescoping at most N updates, including the final off-diagonal division, gives an entrywise bound on K-LDL^T. We use the larger, convenient bound

    eta = eta_0 + 16 (N+1) u A_max L_max^2,
    ||K-LDL^T||_2 <= N eta.

The implementation doubles the last bound to cover binary64 evaluation of these positive expressions. Nonfinite factorization values or inconclusive tests fall back to full MPFR interval LDL. Subnormal absolute arithmetic errors are smaller than the allowances here because A_max and L_max are at least one. No claim is made for unchecked arbitrary extreme inputs.

To bound the smallest eigenvalue of F=LDL^T, round L to binary64 L64, compute R approximately equal to L64^-1, and check the inverse residual. Put eps=2^-52, S=fl(|L64||R|), and use

    tau_inf = computed ||I-fl(L64 R)||_inf
              +64 N eps (1+computed ||S||_inf).

The second term dominates the usual gamma_N dot-product errors, rounding L, subtraction, and positive row summation, including their evaluation errors. Thus ||I-LR||_inf <= tau_inf. With tau_2=sqrt(N) tau_inf<1/2, the Neumann-series bound gives

    ||L^-1||_2 <= ||R||_F /(1-tau_2).

The saved `inverse_frobenius_sq_upper` inflates the positive sum of squares by 1+64 N^2 eps. The minimum D is rounded down. We additionally halve the resulting eigenvalue lower bound to absorb evaluation rounding, obtaining

    lambda_min(F) >= ell = (1/2) D_min (1-tau_2)^2 / ||R||_F,upper^2.

Only ell > 2 N eta authorizes PD (`binary128_backward_bound`). By Weyl's inequality, `lambda_min_lower=ell-2 N eta` is then a positive lower bound on the exact lambda_min(K). This certificate does not rely on a binary64 eigenvalue sign. The conservative factors are not optimized.

The error bounds assume the standard IEEE nearest-rounding behavior of binary64 and libquadmath basic arithmetic and the standard dot-product error bound for the installed NumPy/SciPy BLAS. MPFR interval LDL is the alternative certificate that avoids this BLAS-bound dependence. The code and assumptions are explicit rather than hidden in an eigensolver tolerance.

## Independent validation

`extra_checks.py` compares interval signs with well-separated independent spectra, checks the explicit equatorial-square eigenvalue, and audits the SMO solver against SciPy SLSQP on separate small problems. `replay_certificates.py` re-runs recorded certificates, and selected fast decisions are additionally checked by the original full MPFR interval algorithm. `audit_headline.py` checks every one of the 80 independently refined N=400 matrices at lambda=3.25 with full interval LDL, so this precision comparison has no dependence on the faster positive certificate's BLAS assumptions. `checker.py --audit` independently rebuilds selected kernel matrices and predictions with NumPy only, verifies the raw prediction counts and validation-only parameter choices, and recomputes all statistical summaries.

Strict PD alone is not a conditioning guarantee. Already a two-point matrix has condition number (1+exp(-lambda delta^q))/(1-exp(-lambda delta^q)), which diverges as the distinct points approach each other. The sign audit therefore does not by itself establish stable ordinary-precision matrix inversion for every kernel method.
