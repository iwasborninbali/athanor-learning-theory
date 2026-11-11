# Already-solved audit

Audit started 2026-11-10 23:31 UTC; concluded 23:36 UTC, within the
20-minute allowance. Read scout C3, the complete 2015 note, and
2023 Appendix H.1–H.2 before experimental search; the full H.3 was
read during the proof audit (a deviation from the requested reading order).
No located later work settles
the exact target. This is a bounded search, not proof of novelty.

Fresh OpenAlex queries (unauthenticated public endpoint; saved JSON):

- `works?filter=referenced_works:W404318071&per_page=200`: two results,
  *On the Convergence Properties of Optimal AdaBoost* and *Limit Cycles
  of AdaBoost* (2022). The former's metadata date is 2012 but the source
  revision inspected is January 2023.
- `works?filter=author.id:A5048197562,from_publication_date:2015-01-01&per_page=200&sort=publication_date:desc`:
  four results, no additional count theorem identified.
- Corresponding query for `A5081273303`: sixteen results, no additional
  count theorem identified. Author identity matching is imperfect.
- Read Ortiz's publication list at
  <https://www-personal.umd.umich.edu/~leortiz/papers.html>; its listed
  stumps work points back to the source papers. His PhD thesis predates
  the question and concerns approximately optimal actions.

Targeted web queries (complete saved responses for batches 2–5 in
`search2.json` through `search5.json`; batch 1 queries recorded here):

1. `"Some Open Problems in Optimal AdaBoost and Decision Stumps"`;
   `"effective" "decision stumps" bounds Belanich`;
   `Belanich Ortiz undominated stumps thesis`.
2. `"Generalization Properties of Decision Trees on Real-valued" stumps`;
   `"decision stumps" "dominated" bounds`;
   `"Belanich" "Ortiz" thesis stumps`; `site:oeis.org "stumps"`.
3. `"effective decision stumps" antichain`;
   `"dominated" "stumps" "Belanich" -site:arxiv.org -site:alphaxiv.org -site:catalyzex.com`;
   `"Joshua Belanich" publications`; `"stumps" "Sperner"`.
4. `"effective stumps" bounds after:2015-01-01`;
   `"undominated" "decision stumps"`;
   `"decision stumps" "dominance" "thesis"`;
   `site:oeis.org "antichains" "permutations"`.
5. `"decision stumps" "effective" extremal count`;
   `"Belanich" "thesis" "AdaBoost"`;
   `"Ortiz" "effective" "stumps" bound`;
   `site:oeis.org "decision" "stump"`.

OEIS direct search for `decision stumps` returned JSON `null`; targeted
site searches found no applicable entry. General Boolean antichain entries
do not settle this constrained family.

Related primary source inspected: Leboeuf, LeBlanc and Marchand,
*Decision trees as partitioning machines to characterize their
generalization properties*, NeurIPS 2020, §5.1, Theorem 7 and Corollary 8.
Their theorem bounds all partitions / growth functions, independently of
labels and domination; it is not an extremal theorem for minimal error
sets. Saved PDF and extracted text. Its 2022 extended manuscript is
arXiv:2210.10781; attempted `/html/2210.10781v3` returned 404. The 2022
AdaBoost cycle paper addresses dynamics, not the target count. No new
settling paper requiring an exact-quote stop was found. Search results
and abstracts, rather than full texts of every later author paper, were
used for most exclusion of unrelated work.
