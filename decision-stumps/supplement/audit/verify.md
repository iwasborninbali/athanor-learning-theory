**Overall verdict: HOLDS for the five mathematical claims in the brief, under the explicitly stated rank-data conventions. Priority remains a GAP.** I found no counterexample or invalid inference in `proofs.md`. I independently regenerated the entire extremal functions for every m = 2,…,6 and every feature dimension, matched all 30 supplied closure certificates including their depths, and checked every supplied witness. These are partial answers about effective stumps; they do not settle the full original Problem 1 or its selected-stump question.

This audit was performed independently on 11 November 2026. My code imports no candidate code. It uses the Python standard library, with one numerical process running at a time. The two completed numerical runs used 102.69 and 15.72 CPU seconds, respectively, comfortably below the 20 CPU-minute limit. All audit writes are in this folder; no installs, paid calls, external messages or publication were used.

| Claim | Verdict | Basis |
|---|---|---|
| Proper-subset effectiveness, equality handling, A/T/C definitions | **holds**, with the source interpretation explained below | Direct source reading and independent prediction evaluation |
| Exact one-feature identities, equation (1) | **holds** | Proof audit; all label words through m = 12; random instances |
| Named maxima M_T, M_A, M_C, equations (2)–(3) | **holds** | Local upper bounds, constant parity argument, attainable constructions |
| Universal distinct-set upper bound, equation (4) | **holds** | Global-to-local minimality and Boolean antichain inequality |
| Complete Q table for m ≤ 6, all d | **holds** | Independent exhaustive closure generation and shortest distances; raw permutation spot checks |
| Marker bound and asymptotic sharpness, equations (5)–(6) | **holds** | Distinct marker tags block inclusion; endpoint competitors are excluded |
| Exact cyclic regime, equation (6a) | **holds** | Cyclic-subset distinctness, disjoint endpoint omissions, equal error sizes |
| Odd ceilings, equation (7) | **holds** | Equality-case upper bound and explicit full-level constructions |
| Even lower bounds, equations (8), (8a) | **holds** | Duplication argument and realization of the whole (n−1)-level |
| Expectation identities, finite lower bound and asymptotic theorem, equations (9)–(11) | **holds** | Analytic audit and independent Monte Carlo checks |
| These effective-count results are absent from the specified Appendix H | **holds** | Read H.1–H.3; its results have different content |
| Novelty against all earlier work | **gap** | No matching theorem located; bounded retrieval cannot establish priority |

The scope is unrestricted binary labels and strict feature orders, including repeated orders across different coordinates and samples with a perfect stump. Shared constants are counted once. Exact maxima subject to additional AdaBoost assumptions are not established by this audit.

**Definitions and source correspondence.** Section 3 of the [2015 note](https://arxiv.org/pdf/1505.06999) restricts candidate gaps to adjacent examples “with different labels,” agreeing with T's gap rule. Its displayed error implication is nonstrict inclusion. Taken literally for different named stumps with equal errors, that rule could delete both. Proper inclusion, or deduplication followed by comparison of different patterns, is the coherent repair: equal errors have equal weighted error at every weight vector. The note explicitly displays one polarity; the report's two-polarity interpretation is consistent with the surrounding negation-closure assumption and factor-two bound. Constants are not inserted explicitly in that construction. A/T/C therefore need to remain separate declared conventions.

For a concrete equality check, two identical features with label order −,+,− have four named effective T stumps but only two effective error sets. Both named copies of either singleton error survive proper-subset pruning. Thus a named maximum is not automatically a maximum number of representatives.

**Audit of the analytic proofs.** Equation (1) is sound. A good transition stump is the only stump on its feature that classifies both adjacent examples correctly. Any dominator would have to do the same, proving its local minimality. Moving a cut within a monochromatic run strictly nests the same-polarity errors, so only transitions and the stated endpoint exceptions remain. The opposite-label endpoint case removes an endpoint candidate; equal endpoint labels protect it using the second example and the opposite endpoint. This includes homogeneous samples and m = 2. With constants, endpoint candidates at same-label gaps are dominated. In a mixed sample a constant survives locally exactly when both endpoints have its predicted label. The homogeneous case has only its correct constant. No equal errors occur between different stumps on a single feature.

For equations (2)–(3), global minimality implies local minimality. For A with at least one transition, each endpoint exception requires an additional example beyond the r+1 runs, so r plus the exceptions is at most m−1. A homogeneous feature contributes exactly two local minima. This proves the asserted A and T bounds. With constants, a surviving constant forces every feature's two endpoints into the same label class. Each transition count is then even: at most m−1 for odd m and m−2 for even m. The latter case contributes at most d(m−2)+1 ≤ d(m−1). The case with no surviving constant and the homogeneous case are covered separately. Repeating an alternating feature attains the bounds, including the odd-m shared constant; homogeneous m = 2 attains M_A = 2d. Repeated coordinates legitimately preserve named copies.

The chain-counting proof of equation (4) is the usual antichain inequality. A distinct minimal-error family is an antichain, and a set of cardinality k is hit by a uniformly random maximal chain with probability 1/binom(m,k). Named multiplicities are not included in this step.

For equations (5)–(6), there are enough half-marker sets containing marker 0 because their number is binom(b,b/2)/2. These sets and their complements give 2d different tags of equal cardinality. A competitor cutting within another feature's active block cannot have a marker tag contained in the candidate's. A competitor cutting outside the active block, including a constant, errs on an entire active label class, whereas a good active stump correctly classifies at least one example of each class. This closes both possible domination routes. Distinctness within a feature follows from the local argument. The central-binomial estimate makes b = O(log(d+1)); combined with the named upper bounds this gives Q_X/(dm) → 1 in the stated regime.

Equation (6a) also withstands the endpoint cases. Here n+1 ≥ 2d. Cyclic intervals of any fixed nonzero proper size in the n+1 negative examples have different sets for different starting points. When the positive-error count is between 1 and n−1, its fixed positive prefix and suffix distinguish the polarities. When it is zero, the 2d distinct omitted negative endpoints distinguish them. The constant adds the positive class, not already present. All retained errors have size n, so none properly contains another.

For equation (7), a good T stump's error set contains neither whole label class. Each complete middle level contains a set including the smaller label class, so neither middle level can be the T effective family. The proof correctly treats the possible mixed-level equality case: the bipartite containment graph between levels n and n+1 is connected and regular, giving strict neighborhood expansion for every nonempty proper part of one level. Hence equality in the antichain bound requires a whole middle level. Integrality yields the claimed one-set deficit. The balanced alternating construction realizes each n-set except P; adding a constant supplies P. For A, the pattern NN(PN)^(n−1)N realizes every n-set with a suitable prefix of size 2a+2. Its raw errors have sizes n or n+1, so extra cuts cannot introduce a smaller dominator. The n = 1 case works with no positive labels.

For equation (8), duplicating one positive example adjacently is an injective, inclusion-preserving map on the old error sets. It creates no new transition; equality of the A+C and T+C effective families handles the new same-label gap. Removing constants preserves the nonconstant minima and loses at most the single minimal constant. For equation (8a), any (n−1)-set S has a compatible alternating prefix with |S∩P| positives and |N\S| negatives. The resulting good stump errs on S. All raw errors have cardinality at least n−1, including the constants. Once the whole level is present, every larger error is dominated. The sufficient feature counts and repeated-feature padding are valid. These arguments supply lower bounds, not an unproved general even-m ceiling.

**Why the closure certificates prove all dimensions.** The operation min(A∪B) is associative, commutative and idempotent: deleting a nonminimal member before a later union cannot change the final minima. Every dataset is therefore a product of one-feature generators. Relabeling examples and globally reversing labels reduces the label assignments to p = 0,…,floor(m/2); every feature permutation is still allowed.

A finite family containing the empty state and closed under every generator contains every possible dataset state, by induction on feature count. The supplied inequality

    depth(A star F) ≤ depth(A) + 1,    depth(empty) = 0

has the correct direction. Along any d-feature realization it implies depth(state) ≤ d. Consequently the maximum state size among listed depths ≤ d is a valid upper bound, even if the supplied depths were not exact shortest distances. Taking maxima over all listed states bounds every larger d. Explicit witnesses, padded with repeated features, provide the matching lower bounds. There is no inference from an observed plateau alone.

I strengthened that check by rebuilding all reachable states from scratch. My state is the **upward closure** of an error family, encoded by its membership bits over the Boolean lattice. Combining features is simply bitwise OR of these states. Its minimal boundary recovers the effective error sets. Breadth-first search computes true shortest feature counts. This uses all m! feature orders at each label count, not the supplied search code or its pruning rules.

For all 30 supplied certificates at m = 4,5,6, the independently generated state set and every shortest depth exactly equal the supplied values after representation conversion. All 27,754,591 generator edges in those independent closures were traversed. The largest state family has 58,134 states. I also regenerated the m = 2,3 closures, where no certificates were needed. All global curves agree, including their infinite tails.

Each cell below is independently recovered Q_A/Q_T/Q_C. The last column gives the entire remaining tail.

| m | d = 1 | d = 2 | d = 3 | d = 4 | d = 5 | d = 6 | d = 7,8 | d ≥ 9 |
|---|---|---|---|---|---|---|---|---|
| 2 | 2/1/1 | 2/1/1 | 2/1/1 | 2/1/1 | 2/1/1 | 2/1/1 | 2/1/1 | 2/1/1 |
| 3 | 2/2/3 | 3/2/3 | 3/2/3 | 3/2/3 | 3/2/3 | 3/2/3 | 3/2/3 | 3/2/3 |
| 4 | 3/3/3 | 4/4/4 | 4/4/4 | 4/4/4 | 4/4/4 | 4/4/4 | 4/4/4 | 4/4/4 |
| 5 | 4/4/5 | 8/7/8 | 10/9/10 | 10/9/10 | 10/9/10 | 10/9/10 | 10/9/10 | 10/9/10 |
| 6 | 5/5/5 | 9/9/9 | 12/11/11 | 13/12/13 | 14/13/13 | 15/13/13 | 15/14/15 | 15/15/15 |

As a second enumeration, I fixed the first feature by row relabeling, evaluated all raw signed predictions, retained both same-label cuts and dominated errors when appropriate, and enumerated unordered later feature permutations with repetition, identifying reversals. The exact configuration count is 2^(m−1) binom(m!/2+d−2,d−1). Results were:

| (m,d) | Configurations, each checked in A/T/C | Maxima A/T/C |
|---|---:|---|
| (5,2) | 960 | 8/7/8 |
| (5,3) | 29,280 | 10/9/10 |
| (6,2) | 11,520 | 9/9/9 |
| (6,3) | 2,079,360 | 12/11/11 |

All 226 supplied witnesses also pass direct prediction evaluation, including their full minimal-mask lists, distinct counts and named multiplicities. The one-feature identities pass 24,564 exhaustive convention/label-word cases for m = 2,…,12, plus 6,000 random convention/instance checks with m up to 80. The supplementary m = 7,8 table has verified witnesses; I did not independently repeat its large upper-bound exclusions. Those additional cells should not be described as independently recertified here.

**Random-model theorem.** Equation (9) follows immediately from the checked local identities: each transition has probability 1/2; each A endpoint correction has probability 1/4 for m ≥ 3; endpoint equality for C has probability 1/2. The m = 2 exception for A is correctly separated.

The potential pitfall in equation (10) is conditioning on a candidate being good. The proof avoids it correctly. Conditional on two prediction vectors at distance D, the unconditional probability over fair labels that the competitor's errors are contained in the candidate's is 2^(−D). It is valid to bound losses using this larger event without imposing goodness. At a fixed competing cut, its positive predictions form an independent uniform l-subset. Conditioning Bernoulli(l/m) bits on exactly l positives costs at most m+1 because l is a binomial mode. Pairing a positive and negative candidate coordinate gives

    ((1+p)/2)(1−p/2) = 1/2 + p/4 − p²/4 ≤ 9/16.

There are a such pairs. The product bound is therefore (m+1)(3/4)^(2a). Multiplying the 2dK signed candidates by the 2(d−1)(m−1) signed competitors gives exactly the stated coefficient 4d(d−1)K(m−1)(m+1). Including equality in the rejection event prevents counting collisions as distinct survivors. Constants cannot dominate good transition candidates, and T's restricted competitors form a subset of those already counted. Summing local expected counts bounds both named and distinct global counts; repeated local copies of a shared constant only make that upper bound looser. Choosing a = o(m) with a/log(dm) → ∞ proves equation (11), including d = 1.

I simulated 35,960 independent datasets, reusing each dataset for its three convention counts, with fair labels and independent uniform feature orders. The exact one-feature means agree within sampling error. Illustrative means below are Q estimates ± one standard error; the asymptotic target is dm/2.

| m | d | Trials | A | T | C | dm/2 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 1 | 10,000 | 2.4875 ± .0101 | 1.9846 ± .0100 | 2.4840 ± .0113 | 2.5 |
| 12 | 1 | 10,000 | 5.9925 ± .0166 | 5.5052 ± .0166 | 6.0040 ± .0174 | 6 |
| 16 | 2 | 3,000 | 13.923 ± .062 | 13.611 ± .061 | 13.776 ± .061 | 16 |
| 64 | 2 | 600 | 63.445 ± .249 | 63.200 ± .248 | 63.327 ± .248 | 64 |
| 512 | 2 | 40 | 512.425 ± 2.263 | 512.100 ± 2.276 | 512.250 ± 2.274 | 512 |
| 64 | 4 | 300 | 124.273 ± .463 | 124.243 ± .467 | 124.250 ± .466 | 128 |
| 256 | 4 | 50 | 509.240 ± 2.850 | 509.240 ± 2.850 | 509.240 ± 2.850 | 512 |

For T the exact one-feature target is (m−1)/2, not m/2. Sample means can exceed an expectation upper bound by sampling noise, as in the m = 512 row. No observed deviation contradicts the theorem. The optimized finite lower bounds were also consistent with the data: for example, at (m,d) = (512,2), equation (10) gives 442.02; at (256,4), it gives 379.87. The inequality is conservative. Simulation supports the calculation; the analytic argument establishes the asymptotic theorem.

**Priority assessment.** [Belanich–Ortiz, arXiv:1212.1108v3, Appendix H](https://arxiv.org/html/1212.1108v3#A8) already contains the mistake-dichotomy definition, pruning of repeated/dominated patterns, empirical effective counts and bounds on generalization error using those counts. H.3's Theorems H.1–H.3 do not give these extremal formulas or the fair-label/random-order theorem. Remark 7 retains the loose midpoint bound 2(d(m−1)+1). Thus that appendix is essential prior context, but it does not settle the claims checked here. Its representative count corresponds to Q, rather than the report's duplicate-preserving M.

The appendix's asserted general bound on the number of representative patterns by 2^min(VC,m) is false: two-polarity thresholds with constants have VC dimension 2 and six prediction patterns on three ordered points. It should not be treated as an earlier valid solution. The present proofs do not depend on it.

The distinct-prediction-pattern bound

    sum over k = 1,…,m−1 of min(2d, binom(m,k))

is prior art, as the candidate correctly acknowledges. It is twice the nontrivial two-partition bound in [Leboeuf–LeBlanc–Marchand, NeurIPS 2020, Theorem 7](https://proceedings.neurips.cc/paper/2020/file/d2a10b0bd670e442b1d3caa3fbf9e695-Paper.pdf); their [2022 extension, §5.1, Theorem 7](https://arxiv.org/html/2210.10781v1) also states it and equality regimes including m ≤ 7. These count all patterns or partitions without pruning by errors relative to fixed labels. Their finite exactness does not imply the Q table. The antichain upper bound is classical too.

Targeted searches for effective/undominated/non-dominated stumps, minimal error sets, antichains, the problem title and its identifier found no earlier matching theorem. A fresh OpenAlex citation query returned only the authors' convergence manuscript and *Limit Cycles of AdaBoost*. The latter's inspected abstract/introduction concerns cycling, not extremal effective counts. I also screened the main statement of the [2026 noncycling-counterexample preprint](https://arxiv.org/html/2604.07055v1); it concerns a different question. These screens are not full audits of those dynamical results. Citation indexing and terminology searches can miss relevant work. **I would sign mathematical correctness in the stated model, but would not sign a claim of established priority.** Query details and retrieval limitations are in [sources/search-record.md](sources/search-record.md).

**Reproduction and provenance.** From this folder:

```sh
python3 independent_verify.py structure > independent-structure.log 2>&1
python3 independent_verify.py simulation > independent-simulation.log 2>&1
```

The independent script is [independent_verify.py](independent_verify.py). Full exact-search output is in [independent-structure.json](independent-structure.json); Monte Carlo means, standard errors, named means, optimized finite lower bounds and upper bounds are in [independent-simulation.json](independent-simulation.json). Seeds are fixed in the script. Downloaded primary sources and their SHA-256 values are recorded in [sources/provenance.json](sources/provenance.json).

Audited input hashes:

| File | SHA-256 |
|---|---|
| `../b03-stumps/proofs.md` | `f93ae59b579006c97f954a06bac238fe2c6d1332a581a5e4c7e6968c2133d88f` |
| `../b03-stumps/result.md` | `37d71f150e7f1bb702a81041cad878e71e179e632b83b507258e7f10fa3f4eec` |
| `independent_verify.py` | `70906301dcb2f4398ec2ae50a38ad88ecf5b849a35ab35cc74350578e55de6aa` |
