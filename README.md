# athanor-learning-theory

**Archived release v1.0:** Zenodo [10.5281/zenodo.24139696](https://doi.org/10.5281/zenodo.24139696) (all versions: [10.5281/zenodo.24139695](https://doi.org/10.5281/zenodo.24139695)).

Results on long-stalled open problems from learning theory (November 2026). Each folder holds the certificates and independent checkers.

| Folder | Question (source) | Result | Status |
|---|---|---|---|
| [`rtd-36/`](rtd-36/) | Recursive teaching dimension of (3,6) classes, gap 2..3 (Hu–Wu–Li–Wang, COLT 2017) | **f(3,6) = 2**: a structural proof plus a lower witness | Peer-reviewed: [rStation machine_learning_1](https://rstation.ai/problems/machine_learning/papers/1/v1); Zenodo [10.5281/zenodo.24120155](https://doi.org/10.5281/zenodo.24120155) |
| [`geodesic-kernels/`](geodesic-kernels/) | Probability that a geodesic exponential kernel is positive definite (Feragen–Hauberg, COLT 2016 open problem) | A partial answer: explicit sufficient and necessary bandwidth bounds on spheres, and a proof that PD on a training sample does not survive appended test points | Peer-reviewed: [rStation machine_learning_2](https://rstation.ai/problems/machine_learning/papers/2/v1); Zenodo [10.5281/zenodo.24122285](https://doi.org/10.5281/zenodo.24122285) |
| [`decision-stumps/`](decision-stumps/) | How many decision stumps survive dominance pruning (Belanich–Ortiz, arXiv:1505.06999, Problem 1) | Exact named maxima for all (m, d); complete distinct-set maxima for m ≤ 6; an expectation theorem | Peer-reviewed: [rStation machine_learning_3](https://rstation.ai/problems/machine_learning/papers/3/v1); Zenodo [10.5281/zenodo.24130061](https://doi.org/10.5281/zenodo.24130061) |
| [`lfv-exploration/`](lfv-exploration/) | LFV-v graph exploration on degree-3 graphs (Akash et al., JGAA 2017; Koenig, COLT 2010) | A polynomial bound T ≤ dD(n−1)² on regular graphs (O(n³) on cubic graphs) and an exact census of all connected subcubic graphs through n = 12 | Independently verified; the general max-degree-3 question remains open |

An exact SO(3) minimax-regret result (Kotłowski–Warmuth, COLT 2011: V₃ = √6) is under review at rStation and will be added after the decision.

## Provenance and credit

These results come from a programme on long-stalled published questions. AI research agents worked under the direction of the author of record (Aleksei Kudriashov, ORCID 0009-0006-8885-5338), who takes responsibility for the content:
- OpenAI GPT-6.1 "Sol" cores ran the searches, proofs and independent audits;
- Anthropic Claude orchestrated them.

Every result was checked by a separate session that did not run the solver's code. The checks are in each folder: certificates, stdlib checkers and audit reports. Downloaded third-party papers are not redistributed here.

We claim priority only as far as the dated literature searches recorded in each folder go. Corrections are welcome as issues or pull requests, from people and AI agents alike.

## License

Code: MIT. Data, certificates and text: CC BY 4.0. Third-party inputs (e.g. the Costas array catalogue) keep their original terms and are credited where used.
