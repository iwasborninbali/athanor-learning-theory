# Independent adversarial verification of the LFV-v result

Date: 2026-11-11. Target: [result.md](../b04-lfv/result.md), [regular_bound.md](../b04-lfv/regular_bound.md), and their proof and census files. All verification code here is newly written. None of the target's programs was executed.

**Overall verdict: HOLDS for the stated regular-graph theorem and finite census; GAP as a solution of the unrestricted maximum-degree-3 conjecture; priority remains unestablished.** I found no error in the energy proof or its Poisson and spectral consequences. Known polynomial results for other ant walks do not establish that this exact LFV-v theorem is already known. The target itself distinguishes its restricted theorem from the source's conjecture correctly.

| Claim | Verdict | Finding |
|---|---|---|
| Exact regular-graph energy identity | **holds** | Initialization and every transition are correct. |
| $T\le dD(n-1)^2$, $M\le dD(n-1)$ under arbitrary ties | **holds** | Includes finite coverage and the correct final pre-coverage time index. |
| Grounded-Poisson bound and spectral corollary | **holds** | Correct Laplacian Cauchy–Schwarz argument; rational examples independently recomputed. |
| Simple connected cubic duals of closed triangulated surfaces | **holds** | Boundary triangulations need separate treatment. |
| Polynomial exploration by related VAW, rotor and least-used rules | **known** | The named literature proves these bounds for different update or selection rules. |
| Worldwide priority of the exact regular LFV-v theorem | **gap** | No matching antecedent located; this does not establish novelty. |
| Exact census through $n=12$ | **holds** | Fresh graph generation and exact search reproduce 27,525 classes and maxima $T=90,M=22$. |
| The two twelve-vertex witness paths | **holds** | Every move independently simulated, including all tie decisions. |
| Resolution of the source's unrestricted degree-three conjecture | **gap** | Irregular subcubic graphs and the quadratic/linear asymptotics remain outside the theorem. |

**Priority and the named literature.** I searched for the actual rule: increment a visit counter at every visit, choose a neighbor with the smallest counter, and allow any history-dependent tie choice. The older departure-count convention leaves the current counter smaller by one, but on a simple loop-free graph this changes no neighbor comparison. That convention difference would not invalidate a genuine antecedent.

1. **Wagner–Lindenbaum–Bruckstein, 1996 and 1999.** In the 1999 journal development, the vertex rule stores the **time** of a visit and moves to the oldest neighboring timestamp. Appendix II, pp. 931–932, says: “The theorem provides a worst case bound which is exponential in the graph diameter.” Its polynomial results concern the edge-based ANT-WALK-1 and ANT-WALK-2 rules. Thus this VERTEX-ANT-WALK is neither ordinary visit counting nor a polynomial regular-graph theorem. The author-hosted 1996 scan was located but did not yield readable extraction; this conclusion uses the directly inspected 1999 rule and statement. [1996 author PDF](https://freddy.cs.technion.ac.il/wp-content/uploads/2018/07/77.-smell-as-a-computational-resourse.pdf), [1999 primary paper](https://freddy.cs.technion.ac.il/wp-content/uploads/2018/01/Distributed-Covering-by-Ant-Robots.pdf).

2. **Wagner–Lindenbaum–Bruckstein, 1997 and 1998: known polynomial VAW results.** Theorem 1 of the 1998 paper, p. 216, states: “after at most nd steps the graph G is covered,” with its $d$ denoting diameter. This is an $O(nD)$ bound for all connected undirected graphs. However, its rule on p. 213 assigns $\sigma(u):=\sigma(v)+1$, where $v$ minimizes the neighboring pair $(\sigma,\tau)$. These are search labels, not unconditional visit counts. The 1997 workshop version increments the current label only when it is a local minimum; it also proves $O(nD)$. Both results are **known**, but neither proves the submitted theorem for ordinary LFV-v. Equal graph degrees do not equate these updates. [1997 algorithm and Theorem 1](https://cdn.aaai.org/Workshops/1997/WS-97-10/WS97-10-019.pdf), [1998 primary paper, pp. 213 and 216](https://freddy.cs.technion.ac.il/wp-content/uploads/2018/01/Efficiently-searching-a-graph-by-a-smell-oriented-vertex.pdf).

3. **Koenig–Szymanski–Liu, 2001.** I downloaded the author manuscript anew, rendered and OCRed all 37 PDF pages, read its theoretical sections and conclusion, and visually checked p. 25. Theorem 4 bounds LRTA* goal hitting by $2\sum_s gd(s)\le n^2-n$; Corollary 5 gives polynomial coverage. Theorem 11 and Corollary 13 give superpolynomial Node Counting examples on planar undirected trees with growing degrees. Its polynomial Node Counting special case, pp. 24–25, subdivides every directed arc of an Eulerian digraph, making intermediate counts represent edge counts. It is not a theorem on an untransformed regular undirected graph. Koenig–Szymanski (1999), p. 722, gives the same construction. The 2001 footnote warns: “they call one real-time search method Vertex-Ant Walk in [29] and a different one Vertex-Ant Walk in [30].” I found no regular-graph LFV-v polynomial theorem in this manuscript. [2001 author manuscript](https://idm-lab.org/bib/abstracts/papers/amai01.pdf), [1999 primary paper](https://cdn.aaai.org/AAAI/1999/AAAI99-102.pdf).

4. **Yanovski–Wagner–Bruckstein, 2003.** Theorem 3, p. 177, proves an $O(|E|D)$ bound on a connected directed Eulerian network: “the agent will traverse all edges of the graph and enter an Eulerian cycle.” Its proof uses $t>2|E|D$. The rule on p. 168 cyclically advances a **next-exit pointer** at each vertex, treating the two directions of an undirected edge separately. This is Edge Ant Walk / rotor-router. It does not select the least-visited neighboring vertex. The theorem is **known**, but supplies no antecedent for arbitrary-tie LFV-v on regular graphs. [Primary paper, pp. 168 and 177](https://freddy.cs.technion.ac.il/wp-content/uploads/2018/02/A-Distributed-Ant-Algorithm-for.pdf).

5. **Later least-used walks.** Cooper–Ilcinkas–Klasing–Kosowski (2011), Theorem 4, proves that any undirected Least-Used-First exploration “achieves a cover time of $O(D|E|)$.” Least-used here means the incident **edge** with the smallest traversal count. Their discussion also gives $O(D|E|)$ bounds for locally balanced directed exits and rotor walks. A vertex counter sums arrivals from several neighbors; minimizing it does not enforce the local exit balancing these results require. Regularity alone gives no transfer. [Primary author PDF](https://www.labri.fr/perso/ilcinkas/publications/DisComp-ICALP09.pdf).

6. **The older open problem.** Koenig's COLT 2010 note defines the same Node Counting policy and asks whether its cover times are polynomial on bounded-degree undirected graphs, then grids, allowing adversarial ties and separately random ties. It gives no theorem for all regular graphs. [Primary note](https://www.learningtheory.org/colt2010/conference-website/papers/OpenProblemKoenig.pdf).

My bibliographic verdict is **not “known” for the exact regular LFV-v theorem**. The inspected polynomial VAW, LRTA*, rotor and edge-counting theorems are known results for other rules. The target's disclaimer of unproved priority is warranted. Queries, retrieval limitations and source locations are recorded in [literature_search.md](literature_search.md). The unreadable-font 2001 PDF is now recoverable locally through [its OCR text](sources/koenig2001_ocr.txt) and page images; OCR was a reading aid, not a replacement source.

**Proof audit, line by line.** Line references below refer to regular_bound.md. The shorter proof in result.md uses the same steps.

| Lines | Audit |
|---|---|
| 3–9 | Connectedness and $n\ge2$ imply $d\ge1$. The counted initial visit gives $S_t=t+1$. Energy counts each undirected edge once. Definitions are consistent. |
| 13–18 | $q_t=B_t-dc_t(x_{t+1})\ge0$ follows by summing the $d$ minimum-neighbor inequalities. No random or fixed tie assumption is used. |
| 20–22 | Initially precisely $d$ edges have squared difference 1. Hence $E_0=d,S_0=1,B_0=0$, and both sides of (1) vanish. |
| 22–25 | The energy increment and cancellation are correct; see the explicit calculation below. Simplicity matters because the destination is not its own neighbor. |
| 25 | $E_t=dS_t-2B_t-2\sum_{j<t}q_j\le dS_t$: both subtracted terms are nonnegative. |
| 27–30 | The alternative visit-pairing argument also works. Each adjacent-endpoint occurrence-pair contributes once, at its later occurrence. Destination pre-arrival counters sum to $\sum_v\binom{c_t(v)}2$. The final neighbor sum is the endpoint correction. |
| 34–37 | With unvisited $z$, telescoping gives $c_t(v)^2\le\operatorname{dist}(z,v)E_t\le dDS_t$. This includes $v=z$. |
| 39–43 | At most $n-1$ counters are positive. Since $S_t\ge1$, dividing by $\sqrt{S_t}$ is valid; the stated $S_t$ and maximum-counter bounds follow. |
| 45–48 | There is no circular assumption of coverage. Infinite avoidance contradicts the uniform bound on $S_t=t+1$. At $t=T-1$, $S_t=T$, giving the edge-move bound without an off-by-one loss. |
| 50–59 | Set $d=3$ and $D\le n-1$ to obtain $O(n^3)$. A simple connected dual of a closed triangular surface is cubic. A region with boundary need not satisfy this hypothesis. |
| 63–73 | The grounded Laplacian is positive definite. The equations apply off $z$; actually $Lh_z(z)=-(n-1)$. Since $c_t(z)=0$, $c_t^TLh_z=S_t$ and $h_z^TLh_z=\sum_{v\ne z}h_z(v)=K_z>0$. Laplacian Cauchy–Schwarz applies. |
| 75–79 | $S_t^2\le dS_tK_z$ gives $S_t\le dK_z$. Maximizing over the possible last unvisited vertex and taking an integer floor are valid. The random-walk interpretation has the correct factor $d$. |
| 81–89 | The spectral inequality and expectation statement are correct; details below. The deterministic bound applies to every distribution of tie choices. It proves no linear expectation. |
| 93–97 | Scope is stated correctly; the search statement establishes no priority. |

For an explicit transition calculation, let $c$ be the pre-move counters, $u\to v$ the move, and $A_w=\sum_{y\sim w}c(y)$. Then

$$
\Delta E=2d\,c(v)-2A_v+d,\qquad
\Delta S=1,\qquad
\Delta B=A_v-A_u.
$$

There is **no missing $+1$** in $\Delta B$: the increment is at $v$, which is not a neighbor of itself. Therefore

$$
\Delta(E-dS+2B)=2d\,c(v)-2A_u=-2q_t.
$$

The spectral step uses

$$
\left\lVert c-\frac Sn\mathbf1\right\rVert_2^2
=\sum_v c(v)^2-\frac{S^2}{n}
\ge \frac{S^2}{n-1}-\frac{S^2}{n}
=\frac{S^2}{n(n-1)}.
$$

Together with $E\ge\lambda_2(L)\lVert c-(S/n)\mathbf1\rVert^2$ and $E\le dS$, this yields $T\le dn(n-1)/\lambda_2(L)$. The normalized gap here is $\lambda_2(L)/d$, not an absolute-eigenvalue mixing gap. The Poisson bound is at least as good as the diameter bound: applying path Cauchy–Schwarz to $h_z$, whose energy and sum both equal $K_z$, gives $K_z\le D(n-1)^2$. Also $H_z=dh_z$ satisfies the ordinary random-walk hitting equations $H_z(v)=1+d^{-1}\sum_{w\sim v}H_z(w)$ off $z$.

**Exactly where non-regular subcubic graphs fail.** Write $\delta(w)=\deg(w)$, choose a putative fixed degree constant $a$, and put $q_u=A_u-\delta(u)c(v)\ge0$. The actual transition is

$$
\Delta(E-aS+2B)
=-2q_u+2\bigl(\delta(v)-\delta(u)\bigr)c(v)+\delta(v)-a.
$$

Initially the same expression is $\delta(x_0)-a$, not necessarily zero. More seriously, its extra transition term has no required sign, even for $a=\Delta(G)=3$. The energy increment uses the **destination's** degree; the minimum-neighbor comparison uses the **source's** degree. Equality of those degrees across every edge of a connected graph is precisely regularity. The later path and grounded-Laplacian inequalities remain valid on irregular graphs; the LFV energy estimate feeding them fails.

For a concrete legal failure, take the claw with edges $01,02,03$, start at 0, and follow

$$
0,1,0,2,0.
$$

Vertex 3 remains unvisited. Counters are $(3,1,1,0)$, $S=5$, and $E=4+4+9=17>3S=15$. Even this four-vertex subcubic graph invalidates the extension of the **invariant**. It does not refute the subcubic cover-time conjecture.

**Independent finite verification.** [independent_census.py](independent_census.py) uses only the standard library. It adds a vertex with every nonempty neighbor subset of size at most three among vertices with spare degree capacity. Color refinement only buckets candidates; exact adjacency-preserving bijection search rejects isomorphs. No identification rests on a color hash alone. Completeness follows because deleting a leaf of a spanning tree leaves the remaining induced graph connected. It then memoizes exact states $(x,c)$, expands every minimum-counter neighbor, and stops exactly at coverage. There is no search horizon, counter normalization, small-counter packing or chosen tie policy. This first implementation was written before inspecting the target's search programs.

The independent Python sample reproduces every entry through order nine:

| $n$ | Subcubic classes | Maximum $T$ | Maximum $M$ | Tree maximum $T$ | Cubic maximum $T$ |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 0 | — |
| 2 | 1 | 1 | 1 | 1 | — |
| 3 | 2 | 3 | 2 | 3 | — |
| 4 | 6 | 7 | 3 | 7 | 3 |
| 5 | 10 | 11 | 5 | 11 | — |
| 6 | 29 | 17 | 7 | 17 | 8 |
| 7 | 64 | 27 | 8 | 27 | — |
| 8 | 194 | 34 | 8 | 31 | 15 |
| 9 | 531 | 45 | 14 | 43 | — |

[compare_sample.py](compare_sample.py) additionally matches each of the 838 independently generated graphs to exactly one supplied graph by isomorphism and compares both per-graph extrema. All comparisons passed. Outputs: [independent_results.json](independent_results.json), [sample_comparison.json](sample_comparison.json).

Because the sample was inexpensive, I extended verification to the **entire census**. [independent_catalogue.py](independent_catalogue.py) generates fresh representatives through twelve vertices. [independent_full.cpp](independent_full.cpp) ports the independent search to C++, using full 32-bit counters and caching absolute terminal move counts. Its key stores the complete counter array and position; it uses no fixed search horizon. The fresh generation and search reproduce all 27,525 classes and these further extrema:

| $n$ | Subcubic classes | Maximum $T$ | Maximum $M$ |
|---:|---:|---:|---:|
| 10 | 1,733 | 57 | 16 |
| 11 | 5,524 | 74 | 22 |
| 12 | 19,430 | **90** | **22** |

The search processed **902,816,036 distinct nonterminal graph states**, including 802,689,122 at order twelve. This independently establishes the upper exclusions as well as the witness lower bounds. A further isomorphism comparison matched **every one of the 27,525 graphs** to the supplied census: both extrema and the number of reachable nonterminal states agree for each graph. See [full_comparison.json](full_comparison.json) and [full_summary.json](full_summary.json). The latter also reproduces all tree and cubic columns, including the twelve-vertex cubic maximum $T=42$. Logs and per-graph outputs are retained in [independent_catalogue.log](independent_catalogue.log), [independent_full.log](independent_full.log), and [independent_full_results.jsonl](independent_full_results.jsonl).

The termination justification is sound without regularity. For adjacent $u,v$, while $c(u)\le k$, each departure from $v$ goes to a neighbor with counter at most $k$. Each neighbor receives at most $k+1$ such departures. Arrivals and departures at $v$ differ by at most one, so

$$
c(v)\le\deg(v)\bigl(c(u)+1\bigr)+1.
$$

Propagation from an unvisited vertex gives $c(v)\le2(3^{n-1}-1)$ before coverage. Thus the state space is finite. At $n\le12$ this and the corresponding total-move bound fit comfortably in the independent C++ program's 32-bit fields. Acyclicity alone would not prove finiteness; this separate bound does. I found no omitted extension in the target's generation argument or omitted successor in its forward exclusion recurrence.

**Twelve-vertex witness simulations.** The independent simulator reconstructs the graph from its adjacency word, counts the initial vertex, checks every move and minimum-neighbor choice, and rejects continuation after coverage.

| Supplied path | First coverage $T$ | Pre-coverage maximum $M$ | Sum of first-hit times | Result |
|---|---:|---:|---:|---|
| time witness | 90 | 18 | 172 | Every move legal; coverage occurs at the final move. |
| frequency witness | 83 | 22 | 158 | Every move legal; coverage occurs at the final move. |

The first graph has 12 edges and is unicyclic; the second has 11 edges and is a tree. Mean first-hit times are respectively $43/3$ and $79/6$. The two objectives are separately maximized. Raw final counters and first-hit arrays are in independent_results.json; the supplied inputs are [witness_n12.json](../b04-lfv/exact/witness_n12.json) and [frequency_n12.json](../b04-lfv/exact/frequency_n12.json).

**Regular certificates and integrity.** [independent_algebra.py](independent_algebra.py) replays all eight regular certificate paths and checks the identity at every step. It solves a new grounded system in exact rational arithmetic for **every pin** on the five Poisson examples, rather than trusting the supplied automorphism shortcut. Upper bounds are 28, 58, 103, 362 and 1107, exactly as supplied; see [independent_algebra.json](independent_algebra.json). All 121 hashes in the target's manifest match. Audited input hashes, including the target's result.md, are in [input_integrity.json](input_integrity.json); downloaded-source and OCR hashes are in [sources/manifest.json](sources/manifest.json). Hash agreement checks integrity, not mathematical truth.

**Framing against the 2017 source.** Its conclusion, p. 385, says: “We conjecture that for graphs of maximum degree 3, the performance of LFV-v is quadratic and its average coverage time is linear.” This includes degrees 1 and 2. The uniform theorem here covers equal degrees and gives a cubic, rather than quadratic, worst-case first-cover bound. It also does not prove a linear random-tie expectation. The source does not specify the probability space of its average claim. These are separate outstanding obligations. [Akash et al., JGAA 21(3), 371–387](https://doi.org/10.7155/jgaa.00421).

The target expressly distinguishes cubic from subcubic, excludes boundary triangulations from the theorem, and distinguishes first coverage, pre-coverage frequency and expected coverage. That framing **holds**. Calling this a solution of the entire degree-three gap would be **wrong**, but the qualified result does not do so. The source's Theorem 5 has the reported metric mismatch: totaling component traversals alone does not establish a quadratic counter at one vertex. This is a gap in that source argument, not a refutation of its existence claim.

Reproduce the independent checks from this directory:

~~~sh
python3 independent_census.py --max-n 9
python3 compare_sample.py
python3 independent_algebra.py
python3 independent_catalogue.py
mkdir -p tmp
TMPDIR="$PWD/tmp" clang++ -std=c++17 -O3 independent_full.cpp -o independent_full
./independent_full
python3 compare_sample.py --full
~~~

The three main additional computations used about 235, 102 and 63 CPU seconds respectively (catalogue generation, full search and full comparison). The initial Python sample took 4.1 seconds and OCR took 71.4 seconds wall time; total local computation was comfortably below the 30-CPU-minute allowance. The audit finished in about 20 minutes wall time.

All writes stayed in this folder. One heavy local computation ran at a time. No installs, paid calls, VM, publication, messages to others, or execution of the target's code were used.
