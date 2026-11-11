Independent bounded literature audit, 11 November 2026. No paid service or model calls.

Primary material read:

- Belanich and Ortiz, *Some Open Problems in Optimal AdaBoost and Decision Stumps*, arXiv:1505.06999, especially Section 3 and the earlier natural-class definition. Fresh PDF saved as `note2015.pdf`, extracted as `note2015.txt`.
- Belanich and Ortiz, *On the Convergence Properties of Optimal AdaBoost*, arXiv:1212.1108v3. Read Appendix H.1–H.3, including its definitions, empirical table, generalization theorems, Remark 7 and pattern-count claim. Fresh full HTML saved as `revision2023.html`; the extracted appendix is `appendix-H.txt`. This is source reading, not reliance on the candidate's summary.
- Leboeuf, LeBlanc and Marchand, NeurIPS 2020, *Decision trees as partitioning machines to characterize their generalization properties*, Section 5.1, Theorem 7. Fresh PDF saved as `partition2020.pdf`, with extracted text.
- Their 2022 extension arXiv:2210.10781v1, Section 5.1, Theorem 7 and Corollary 8, read through arXiv HTML. It bounds partitions/growth functions without fixed-label error pruning.
- Snedeker, arXiv:2209.06928v2: screened abstract and introduction. Its arXiv HTML conversion is incomplete; I do not claim to have read the whole paper.
- Wang, arXiv:2604.07055v1: screened abstract, introduction, Theorem 1 and Corollary 2. These address noncycling, not the extremal count problem. The mathematical counterexample itself was not audited.

Representative search queries actually used, including variants:

- `"effective stumps" bounds Belanich Ortiz`
- `"undominated" "decision stumps" count`
- `"Belanich" "stumps" bounds`
- `"decision stumps" "partitioning" Leboeuf`
- `"Some Open Problems in Optimal AdaBoost"` with mirror domains excluded
- `"dominated hypotheses" "stumps" bounds`
- `"effective" "stumps" "antichain"`
- `"minimal" "error sets" "decision stumps"`
- `"decision stumps" "number" "undominated"`
- `"decision stumps" "effective" "upper bound"`
- `"stumps" "Sperner"`
- `"stumps" "minimal error" count`
- `"decision stumps" "antichains"`
- `"decision stumps" "non-dominated" number`
- `"decision stumps" "undominated" Belanich`
- `"1505.06999"` with several mirror domains excluded
- `"Belanich" "effective" count theorem`
- `"effective decision stumps"`
- `"number of effective stumps"`
- `"Bounding the Number of Effective Stumps"`
- `"Belanich" "stumps" extremal`
- `"decision stumps" "random labels" "number"`
- `"decision stumps" "Sperner theorem"`
- `"Limit Cycles of AdaBoost"`
- `"AdaBoost Does Not Always Cycle"`

Most exact effective/undominated queries returned the original note, the authors' convergence work, or unrelated uses of “effective.” No matching extremal effective-error-set theorem was located. This is an observation about these retrievals, not an assertion that none exists.

Fresh citation check:

- `https://api.openalex.org/works/W404318071`
- `https://api.openalex.org/works?filter=cites:W404318071&per-page=100`

The browser tool could not open the first API URL. Direct standard-library HTTPS retrieval succeeded for both. Responses are saved verbatim as `openalex-note.json` and `openalex-citations.json`. Both report two citations: the authors' convergence manuscript and Snedeker's *Limit Cycles of AdaBoost*. That count is limited by this index's coverage; it does not include every potentially relevant work.

Conclusions: Appendix H does not contain the checked extremal formulas. The all-pattern bound and general Boolean antichain bound are known ingredients. No earlier matching result was found for the named maxima, full small-m effective-count curves, constructions or random-model theorem. Priority is unverified.
