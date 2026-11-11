# LFV-v on cubic graphs: a polynomial upper bound and a certified small census

**All independent audits passed.**

Date: 2026-11-11. This work addresses option **(ii)** of the brief. The finite
census is supporting evidence, not a claim that twelve vertices is the largest
feasible order.

## What is established

For every finite connected simple **d-regular** graph with n>=2 vertices and
diameter D, LFV-v started with zero counters, counting the initial vertex, obeys
the following bounds under arbitrary, history-dependent adversarial ties:

\[
 T_{\mathrm{first}}\le dD(n-1)^2,
 \qquad M_{\mathrm{before}}\le dD(n-1).
\]

In particular, on **cubic graphs** (every vertex has degree exactly three),

\[
 \boxed{T_{\mathrm{first}}\le3D(n-1)^2\le3(n-1)^3},\qquad
 \boxed{M_{\mathrm{before}}\le3D(n-1)\le3(n-1)^2}.
\]

This is a polynomial refinement of the source paper's exponential-in-diameter
upper bound for a meaningful restricted family. It applies to simple connected
duals of triangulations of closed surfaces. Triangulated polygonal regions have
boundary triangles of degree below three and are not covered by this theorem.
The result is independently proved here; the recorded search found no earlier
statement of this refinement, but does **not** establish bibliographic priority.

A sharper graph-specific bound is

\[
 T_{\mathrm{first}}\le
 \left\lfloor d\max_z\sum_{v\ne z}h_z(v)\right\rfloor,
 \quad h_z(z)=0,\quad (Lh_z)(v)=1\ (v\ne z),
\]

where L is the graph Laplacian. Also,
\(T_{\mathrm{first}}\le d n(n-1)/\lambda_2(L)\). Thus regular families with
a normalized spectral gap bounded below have **O(n²)** worst-case first
coverage. These are deterministic statements and hence also bound expectations.

The accompanying complete census covers all **27,525** isomorphism classes of
connected simple subcubic graphs of orders 1 through 12, all initial vertices,
and all legal adversarial tie choices. Producer and independent checker use
different state-search directions and different graph-isomorphism algorithms.

## Metrics and initialization

Let \(x_0,x_1,\ldots\) be the walk and
\(c_t(v)=|\{j:0\le j\le t,\ x_j=v\}|\). At time t, choose a neighbor w of
\(x_t\) minimizing \(c_t(w)\), move there, then increment its counter.
There is no waiting, stay-put action, self-loop, or counter reset.

* **(a) First coverage:** \(T=\min\{t:c_t(v)>0\ \forall v\}\), in edge moves.
  Worst case means maximum over starts and all legal tie choices.
* **(b) Frequency before coverage:**
  \(M=\max_{0\le t<T,v}c_t(v)\). For the singleton, T=M=0 by convention.
  M and T are separately maximized; their extremizers can differ.
* **(c) Average coverage:** we fix the concrete convention
  \(A(G)=\max_s\mathbb E[T\mid x_0=s]\), choosing independently and uniformly
  among tied minimum-counter neighbors at each step. The paper does not define
  a probability space for its concluding average-coverage conjecture, so no
  equivalence with its intended meaning is assumed. We prove the same upper
  bound for A by pathwise domination; we do not establish a linear expectation.

The replay checker additionally reports the **mean first-hit time over
vertices**, \(\bar H=n^{-1}\sum_v\min\{t:x_t=v\}\), for each fixed witness.
That quantity is neither T nor the random-tie expectation A. No latency or
perpetual-patrol theorem is asserted.

For example, the twelve-vertex T-witness has T=90, M=18 and
\(\bar H=43/3\). A different witness has M=22, T=83 and
\(\bar H=79/6\). These are independently replayed, not interchangeable metrics.

## Proof of the regular-graph bound

Put \(S_t=\sum_vc_t(v)=t+1\),
\(E_t=\sum_{uv\in E}(c_t(u)-c_t(v))^2\), and
\(B_t=\sum_{w\sim x_t}c_t(w)\). The LFV rule makes

\[
 q_t=\sum_{w\sim x_t}c_t(w)-d\,c_t(x_{t+1})\ge0.
\]

The exact identity

\[
 E_t-dS_t+2B_t=-2\sum_{j<t}q_j
\tag{1}
\]

holds initially and is preserved by every move: when u->v increments c(v),
the change in E is
\(2d c(v)-2\sum_{w\sim v}c(w)+d\); the changes in -dS+2B cancel all but
\(-2q_t\). Therefore \(E_t\le dS_t\).

Before coverage, choose an unvisited z. Along any shortest z-v path,
Cauchy--Schwarz gives \(c_t(v)^2\le D E_t\le dD S_t\). At most n-1
counters are positive, so
\(S_t\le(n-1)\sqrt{dD S_t}\), hence \(S_t\le dD(n-1)^2\) and
\(\max_vc_t(v)\le dD(n-1)\). This also proves finite coverage: an infinite
avoiding walk would make S grow beyond the bound. At t=T-1, S=T, proving
the stated first-cover inequality without an off-by-one loss.

For the sharper bound, the grounded Laplacian is positive definite by
connectedness. With \(K_z=\sum_vh_z(v)=h_z^TLh_z\), another
Cauchy--Schwarz application gives
\(S_t^2=(c_t^TLh_z)^2\le E_tK_z\le dS_tK_z\).
The spectral variant follows from
\(\sum_v(c_t(v)-S_t/n)^2\ge S_t^2/[n(n-1)]\).
See [regular_bound.md](regular_bound.md) for the expanded proof and scope.

Regularity is used in the energy increment and cannot be dropped. In an
irregular graph the quadratic term has deg(v) after a move u->v, whereas the
minimum-neighbor comparison averages over deg(u). That mismatch is the
specific obstruction left by this method, rather than an implicit extension
to all graphs of maximum degree three.

## Exact finite results

All graphs in this table are connected, simple, undirected, and have maximum
degree **at most** three. T_n and M_n are separate universal maxima.

| n | Isomorphism classes | T_n | M_n | Maximum T on trees | Cubic classes | Maximum T on cubic graphs |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 0 | — | — |
| 2 | 1 | 1 | 1 | 1 | — | — |
| 3 | 2 | 3 | 2 | 3 | — | — |
| 4 | 6 | 7 | 3 | 7 | 1 | 3 |
| 5 | 10 | 11 | 5 | 11 | — | — |
| 6 | 29 | 17 | 7 | 17 | 2 | 8 |
| 7 | 64 | 27 | 8 | 27 | — | — |
| 8 | 194 | 34 | 8 | 31 | 5 | 15 |
| 9 | 531 | 45 | 14 | 43 | — | — |
| 10 | 1,733 | 57 | 16 | 57 | 19 | 26 |
| 11 | 5,524 | 74 | 22 | 63 | — | — |
| 12 | 19,430 | 90 | 22 | 83 | 85 | 42 |

The smallest order where restricting to trees loses the overall first-cover
maximum is eight (31 versus 34). At twelve, a unicyclic graph attains 90, while
the cubic maximum is 42. These are finite structural conclusions; they do not
imply an asymptotic lower-bound family. The main uniform progress is (1).

Witnesses are `exact/witness_nN.json` and `exact/frequency_nN.json`, N=1,...,12.
Each contains a graph adjacency word, start, objective, value, and complete
vertex trajectory. Words list upper-triangle entries in row order, 0 before 1.
Machine-readable tables are [table.csv](table.csv) and [summary.json](summary.json).

## Search, completeness, and independent checking

The pilot generated all 194 eight-vertex classes in 0.13 seconds and searched
them in about 0.45 seconds using Python. At n=10 the Python pilot took 32.1
seconds. The C++ producer, sharing states across starts, took 1.38 seconds and
visited 10,992,758 nonterminal states. Its n=12 run took 76.2 seconds for
802,689,122 states, with only 224,085 states stored for its largest individual
graph. Independent forward checking was then run for the complete n<=12
target; actual logs are retained. Enumeration was stopped at this preselected
audit order after the uniform theorem was obtained, not because n=13 was
proved infeasible.

`generate_graphs.py` adds a new vertex with every possible nonempty neighbor
subset of size at most three among vertices with remaining degree capacity.
It removes isomorphs by exhaustive individualization/refinement. Completeness
is inductive: any connected graph has a vertex whose deletion leaves it
connected (take a leaf of a spanning tree), so every graph is an allowed
extension of a smaller representative.

`check.py` independently checks catalogue uniqueness and **every allowed
extension** using equitable colors plus explicit isomorphism backtracking,
without the producer's canonical labeling. It then explores reachable states
**forward by move count**, starting at every vertex, including every minimum
neighbor, and stopping a trajectory exactly at coverage. The producer instead
uses backward memoized longest-path recurrences. The checker imports no search
code and uses only the Python standard library.

The state graph has no cycles because each move increases the total counter
sum. A separate coarse finite bound justifies exhaustion without presupposing
the source theorem: if u~v, then
\(c(v)\le\deg(v)(c(u)+1)+1\). Indeed, while c(u)<=k, each neighbor can receive
at most k+1 minimum-counter departures from v, and visits differ from departures
by at most one. Along a path from an unvisited vertex this gives
\(c(v)\le2(3^{n-1}-1)\). Thus precoverage states have
\(S\le2n(3^{n-1}-1)\). The independent checker uses this bound to size exact
integer fields and treats any violation as failure; no horizon truncation is
accepted as an upper certificate. All positive witnesses are replayed separately.

`check_regular.py` independently verifies local identity (1) coefficient by
coefficient, explicit legal trajectories, exact rational grounded Poisson
equations, and automorphisms carrying the pinned vertex to every vertex.
The prism certificates include actual triangular faces of bipyramids, and the
checker reconstructs and verifies their dual adjacency. Its optional exhaustive
audit checks the energy inequality on every reachable state of every cubic
graph through twelve vertices. The universal theorem is an analytic proof,
not a claim of a machine-formal proof for all graph orders.

The prism trajectories are legal examples, not schedules claimed to maximize
coverage time. Their rational Poisson vectors, together with the proof, certify
upper bounds for every start and tie schedule on those graphs.

Run from this directory with Python 3; no packages or installations are needed:

```sh
python3 check.py --max-n 12
python3 check_regular.py --exhaustive --max-n 12
shasum -a 256 -c SHA256SUMS
```

`check.py --mode witnesses --max-n 12` is the quick witness-only check.
Full census exclusion checking is substantially slower; progress is printed
every 1,000 graphs. Source, witnesses, catalogues, and successful audit logs
are retained. No SAT solver was needed; the negative finite result is certified
by complete exhaustion with the completeness argument above, not an unchecked
UNSAT claim.


The completed independent forward audit checked **902,816,036**
nonterminal graph states in 1276.8 seconds across all orders;
the n=12 pass took 1143.7 seconds. Its largest
frontier layer contained 10,234 states. The
separate energy audit checked 4,837,317 reachable states
(including terminal states) on all 112 cubic graphs through n=12.
The readable tuple-state reference checker also passed every graph
through n=8. These are completed checks, not planned validation.

## Certificates and hashes

| Certificate | SHA-256 |
|---|---|
| [regular_bound.md](regular_bound.md) | `78e3bec00e0ec92ea9600ddc5e00a35e54fcf7a52a42de7c10b72c07cc7c97f6` |
| [regular_certificates.json](regular_certificates.json) | `28e5ca282824424c9031610362f5b743657b592ffd82b1c938bbb9279fe9f580` |
| [check_regular.py](check_regular.py) | `5fecc04d3bfaca9583ef0f222c6a254e00ddbc95d25e3db7a94f495735bbadc8` |
| [check.py](check.py) | `67e8e984d49203c3b444fa66717dfc1db2e5f2bd41a8c6921005fd3865b115bf` |
| [catalog/n12.txt](catalog/n12.txt) | `d3c25736658f2501679967aefc2c9da5f24105393adc4626211bcb97e9f3f7ae` |
| [exact/n12.jsonl](exact/n12.jsonl) | `1801aa4c1293b015a95ed53e5d27dae04ccd0ab1f8a4b9cff38a947cb4c1abe7` |
| [exact/witness_n12.json](exact/witness_n12.json) | `21136b9a0505d01d480d581fb6520c37a42939c30219ce96e1b9160768185739` |
| [exact/frequency_n12.json](exact/frequency_n12.json) | `ff48c41c17a39830257e4d0d0a15c0bdaefd286598cea4d53354e110902cfc26` |
| [checked_exclusions.log](checked_exclusions.log) | `cce656497f774444e3e5b5e90185f0be2b503cce5380130950ee01f9569c791e` |
| [checked_regular_exhaustive.log](checked_regular_exhaustive.log) | `49a06018cd26d9da179ef42ecde877d52427abe479221912b64f6575fb57d7ef` |

[SHA256SUMS](SHA256SUMS) lists all 121 immutable certificate/source files; its SHA-256 is `8e2da6c7019b8782847b2b1940e396e75bc8e32800f08227efc99a86968383cf`.


## Prior art and source issues

The starting source is [Akash et al., JGAA 21(3), 371–387 (2017)](https://doi.org/10.7155/jgaa.00421).
Its conclusion reads: “We conjecture that for graphs of maximum degree 3, the
performance of LFV-v is quadratic and its average coverage time is linear.”
Its general bound leaves exponential diameter dependence. Our polynomial
result concerns regular graphs and first coverage, not every subcubic graph or
patrol latency.

Two source issues matter under the explicit metrics above. Theorem 5 states a
quadratic **vertex-frequency** construction, but its proof counts total
component traversals. That argument does not establish the stated frequency
claim; this is a proof/metric mismatch, not a refutation of the existence
statement. Also Lemma 1, interpreted with counted arrivals including the current
vertex, needs an off-by-one correction: on a two-vertex graph the initial state
has counts (1,0). The corrected local departure inequality used above avoids
that convention issue. No conclusion here relies on treating those ambiguities
as proved frequency bounds.

[Koenig's COLT 2010 note](https://www.learningtheory.org/colt2010/conference-website/papers/OpenProblemKoenig.pdf)
asks about node counting on bounded-degree graphs and grids, distinguishing
adversarial and random ties. [Koenig and Szymanski (AAAI 1999)](https://cdn.aaai.org/AAAI/1999/AAAI99-102.pdf)
give a polynomial special case after subdividing directed edges of Eulerian
graphs; that construction has forced intermediate moves and does not transfer
directly to the undirected LFV rule here. The saved 2001 ant-coverage PDF has
corrupt text extraction; relevant indexed passages were available, but no full
searchable-text audit of that PDF is claimed.

[Avin and Krishnamachari (2006)](https://tzin.bgu.ac.il/~avin/papers/MSWiM06-CR.pdf)
study random neighbor sampling with a degree-normalized visit criterion. Their
regular-graph discussion is relevant background, but the sampled policy differs
from choosing a true minimum among all neighbors, and the retrieved paper
provides empirical rather than this adversarial energy bound.

## Already-solved search record

The required first search was completed in about three minutes, before the
first enumeration pilot. It found **no located resolution** of the exact
post-2017 degree-three target. This is bounded search evidence, not proof of
absence. The detailed reproducible record, queries, source URLs, retrieval
failures, and author-list limits are in [sources/search-record.md](sources/search-record.md).

A fresh OpenAlex DOI lookup and citing-work request returned three citing
works: Fekete's 2019 navigation chapter and two 2026 QKD relaying applications.
The chapter's saved full text did not give a new bound; the other records concern
different walks. Post-2017 lists were retrieved for all six authors, each below
the 200-work response limit. Targeted web, thesis, and OEIS searches did not
locate a resolution. A TU Delft thesis lead had no claimed degree-three result
in its indexed text; full PDF acquisition timed out. After discovering (1),
additional recorded searches for regular-graph/node-counting/least-visited-
neighbor bounds found no matching prior theorem. Identity disambiguation,
indexing gaps, inaccessible full texts, and different policy names remain
limits of the priority audit.

## What is not established

No superquadratic lower-bound family was found. No quadratic first-cover upper
bound for all subcubic graphs, no polynomial upper bound for arbitrary irregular
subcubic graphs, and no linear random-tie expectation are established. The
geometric claim covers closed triangulations with cubic duals, not polygonal
triangulation duals with boundary. The finite data do not refute or prove any
asymptotic polynomial conjecture. Bibliographic priority for the regular-graph
refinement remains unproved.

All work stayed in this directory. One heavy process ran at a time; no installs,
paid calls, VM, publication, or messages were used. Disk was monitored, with
about 15 GiB available and this folder well below the 1 GiB limit.
