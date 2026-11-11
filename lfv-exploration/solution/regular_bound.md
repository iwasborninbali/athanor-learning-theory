# A polynomial bound for regular graphs (proof draft, independently auditable)

Let G be a finite connected simple d-regular graph, n>=2, with zero initial
counters and a counted initial vertex. Ties may depend on the full history.
Write x_t for position after t moves and c_t(v) for number of occurrences of v
in x_0,...,x_t. Put S_t=sum c_t=t+1 and

    E_t = sum_{uv in E(G)} (c_t(u)-c_t(v))^2,
    B_t = sum_{w adjacent to x_t} c_t(w).

## Exact energy identity

At step t define the nonnegative integer slack

    q_t = sum_{w adjacent to x_t} c_t(w) - d*c_t(x_{t+1}) >= 0.

Nonnegativity is precisely the LFV minimum-counter rule, averaged over the d
neighbors. The following is an identity, not an expectation:

    E_t - d*S_t + 2*B_t = -2*sum_{j=0}^{t-1} q_j.               (1)

Initially E_0=d, S_0=1, B_0=0. For a move u->v, increasing c(v) by one changes
E by 2*d*c(v)-2*sum_{w adjacent to v} c(w)+d. Subtracting d*delta(S)=d and
adding 2*delta(B)=2*sum_{w adjacent to v}c(w)-2*sum_{w adjacent to u}c(w)
leaves -2*q_t. Thus induction proves (1), hence E_t<=d*S_t for every t.

An equivalent summation proof pairs visits at opposite endpoints of each edge:
the sum, over all visits including the last, of the counters on the current
vertex's neighbors is exactly sum_{uv in E}c_t(u)c_t(v). The sum of destination
counters immediately before each arrival is sum_v c_t(v)(c_t(v)-1)/2.

## First coverage and maximum frequency

Before coverage choose an unvisited z, so c_t(z)=0. For every v, telescoping
along a shortest z-v path and Cauchy--Schwarz give

    c_t(v)^2 <= dist(z,v)*E_t <= D*d*S_t.

Only at most n-1 vertices have positive count. Therefore

    S_t <= (n-1)*sqrt(D*d*S_t),
    S_t <= d*D*(n-1)^2,
    max_v c_t(v) <= d*D*(n-1).

The number of moves to first coverage is at most d*D*(n-1)^2: apply the
preceding inequality at t=T-1, where S_{T-1}=T. It also proves coverage is
finite, without presupposing recurrence: an infinite avoiding walk would make
S_t unbounded while the same inequality held.

For connected cubic graphs this gives

    T <= 3*D*(n-1)^2 <= 3*(n-1)^3,
    M_before <= 3*D*(n-1) <= 3*(n-1)^2.             (2)

This improves the exponential-in-diameter bound to a polynomial for the
meaningful restricted family of regular cubic graphs. It covers simple cubic
duals of closed triangulated surfaces; it does not cover triangulated polygon
duals with boundary vertices of degree 1 or 2. No geometric realization is
claimed for an arbitrary subcubic witness.

## Sharper graph-specific bound

For each z solve the grounded Poisson equations

    h_z(z)=0,   (L h_z)(v)=1 for v!=z,
    K_z=sum_{v!=z}h_z(v).

The grounded Laplacian is positive definite: its quadratic form is edge
energy with a pinned zero, vanishing only on the all-zero vector by
connectedness. Thus the solution exists and is unique. At a state avoiding z,

    S_t = c_t^T L h_z,
    S_t^2 <= (c_t^T L c_t)*(h_z^T L h_z) = E_t*K_z <= d*S_t*K_z.

Consequently T<=floor(d*max_z K_z). This is a uniform adversarial bound.
Equivalently d*h_z(v) is the expected simple-random-walk hitting time of z
from v, so the bound is a sum of hitting times; no random LFV tie assumption
is needed. The theorem is proved by the equations above, without relying on
that probabilistic interpretation.

For combinatorial Laplacian second eigenvalue lambda_2, the pinned-zero
variance inequality gives

    T <= d*n*(n-1)/lambda_2 = n*(n-1)/(normalized spectral gap).

Thus cubic families with a uniform positive normalized spectral gap have
O(n^2) worst-case first coverage. For any tie distribution the expected first
coverage obeys the same deterministic bound; no linear expectation bound is
claimed.

## Scope and novelty

This is an independently derived bound, not a claim that the unrestricted
degree-three conjecture is settled. The targeted prior-art searches recorded under sources/search_regular*.json
and sources/search_energy_priorart.json found no matching prior theorem; this
does not establish priority. The 2017 paper's displayed general upper bound is exponential in
diameter and does not state this regular-graph refinement.
