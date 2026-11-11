# LFV-v degree-three research progress

2026-11-11 00:14 UTC. Read scout C4 and the 2017 paper (saved extracted text); checking subsequent literature before computation. Initial searches have not located a resolution. The source mixes latency, visit frequency and first coverage, so these will be defined separately. All files remain in this directory; no paid calls or installations.

2026-11-11 00:28 UTC. Derived the exact regular-graph energy identity in regular_bound.md, proving T <= d D (n-1)^2 and maximum pre-coverage frequency <= d D (n-1). For cubic graphs these are O(n^3) and O(n^2), respectively. Literature searches have not located this refinement; priority is not established. Exhaustive C++ production through n=12 finished (19,430 connected subcubic graphs at n=12, candidate worst T=90, M=22). Independent stdlib Python catalogue-completeness check passed through n=12; its forward-state exclusion audit passed through n=11 and is running n=12. The main intended outcome is option (ii), with the finite table as supporting evidence. One heavy process at a time; disk use remains small.

2026-11-11T00:34:08.028400+00:00: still running ['python3', 'check.py', '--mode', 'exclusions', '--min-n', '1', '--max-n', '12']; elapsed 600s; free disk 15.2 GiB.

2026-11-11T00:44:08.459574+00:00: still running ['python3', 'check.py', '--mode', 'exclusions', '--min-n', '1', '--max-n', '12']; elapsed 1201s; free disk 15.4 GiB.

2026-11-11T00:46:03.301698+00:00: complete. Proved the regular-graph polynomial bound; catalogue completeness, all n<=12 forward exclusions, all witnesses, tuple reference through n=8, and the complete small-cubic energy audit passed. Certificates and SHA-256 manifest finalized. General irregular subcubic gap remains open.
