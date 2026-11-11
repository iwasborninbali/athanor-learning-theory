Independent literature audit, 2026-11-11. No paid retrieval service or model calls.

The search concerned the exact rule: counters count visits, increment by one on
every arrival (equivalently departure for decisions on a loop-free graph), choose
a minimum-counter neighbor among all neighbors, with arbitrary ties. A result
for another update, local edge counters, cyclic ports, or sampled neighbors was
not treated as a theorem about this rule.

Representative exact searches included:

- `Wagner Lindenbaum Bruckstein vertex ant walk regular graph cover time 1999`
- `Koenig Szymanski Liu 2001 node counting regular graphs cover time`
- `"Node Counting" "regular graphs"`
- `"node-counting" "regular" graph exploration`
- `"Vertex Ant Walk" "regular"`
- `"least frequently visited" "regular" graph bound`
- `"least-frequently-visited" "polynomial" "regular"`
- `"least-frequently-visited" "potential"`
- `"least visited" graph "energy"`
- `"least visited neighbor" "polynomial"`
- `"least-used" walk "regular" cover`
- `"node counting" "hitting time" regular`
- `"node counting" "cubic" graph`
- `"A distributed ant algorithm for efficiently patrolling a network" pdf`
- `"Efficiently searching a graph by a smell-oriented vertex process" pdf`
- `"Smell as a Computational Resource" "Theorem"`
- `"Distributed Covering by Ant-Robots" "regular"`
- `"rotor router" "node counting"`

Primary documents inspected:

1. Wagner, Lindenbaum, Bruckstein, ISTCS 1996, *Smell as a Computational
   Resource*. Author-hosted scanned PDF located, but no readable extraction;
   the related 1999 full paper was inspected directly. The 1997 paper also
   describes the earlier edge-rule result. Author PDF:
   https://freddy.cs.technion.ac.il/wp-content/uploads/2018/07/77.-smell-as-a-computational-resourse.pdf
2. Wagner, Lindenbaum, Bruckstein, AAAI workshop 1997, *On-Line Graph Searching
   by a Smell-Oriented Vertex Process*, pp. 122-125. Downloaded, text extracted;
   the update is conditional increment, not unconditional visit counting.
   https://cdn.aaai.org/Workshops/1997/WS-97-10/WS97-10-019.pdf
3. Wagner, Lindenbaum, Bruckstein, AMAI 24 (1998), *Efficiently Searching a
   Graph by a Smell-Oriented Vertex Process*, pp. 211-223. Primary indexed
   full-page passages inspected for p. 213 (algorithm) and p. 216 (Theorem 1).
   Direct local download failed; no local PDF is asserted.
   https://freddy.cs.technion.ac.il/wp-content/uploads/2018/01/Efficiently-searching-a-graph-by-a-smell-oriented-vertex.pdf
4. Wagner, Lindenbaum, Bruckstein, IEEE TRA 15(5) (1999), *Distributed Covering
   by Ant-Robots Using Evaporating Traces*, pp. 918-933. Primary web text
   inspected, particularly p. 927 (discussion), pp. 931-932 (Appendix II).
   Its vertex rule stores timestamps; its bound is exponential in diameter.
   https://freddy.cs.technion.ac.il/wp-content/uploads/2018/01/Distributed-Covering-by-Ant-Robots.pdf
5. Koenig and Szymanski, AAAI 1999, *Value-Update Rules for Real-Time Search*.
   Read supplied extracted primary text, particularly the Eulerian directed
   arc-subdivision construction on p. 722. No untransformed regular-graph
   theorem follows from the stated construction.
   https://cdn.aaai.org/AAAI/1999/AAAI99-102.pdf
6. Koenig, Szymanski, Liu, AMAI 31 (2001), *Efficient and Inefficient Ant
   Coverage Methods*, pp. 41-76. Author manuscript is 37 PDF pages, with
   unreadable font extraction. Downloaded anew, rendered all pages with existing
   pdftoppm and OCRed sequentially with installed tesseract. Read theoretical
   sections, special cases, Table 4, footnote, and conclusion. In particular:
   PDF pp. 11-13 (LRTA*), 23-25 (Node Counting lower bound and special case),
   25-28 (different update rules and general theorem), 35 (conclusion).
   Visually checked PDF p. 25 as well. OCR is a reading aid, not a new source.
   https://idm-lab.org/bib/abstracts/papers/amai01.pdf
7. Yanovski, Wagner, Bruckstein, Algorithmica 37 (2003), *A Distributed Ant
   Algorithm for Efficiently Patrolling a Network*, pp. 165-186. Primary web
   text inspected, particularly pp. 168 and 177-178. This is Edge Ant Walk /
   rotor-router, with directed exit ports. A local download returned a bot
   rejection HTML page, saved with an HTML extension, not accepted as a PDF.
   https://freddy.cs.technion.ac.il/wp-content/uploads/2018/02/A-Distributed-Ant-Algorithm-for.pdf
8. Koenig, COLT 2010, *Open Problem: Analyzing Ant Robot Coverage*. Downloaded
   and read. Defines the exact visit-counting rule and asks the bounded-degree
   and grid polynomial questions, with separate adversarial and random ties.
   https://www.learningtheory.org/colt2010/conference-website/papers/OpenProblemKoenig.pdf
9. Cooper, Ilcinkas, Klasing, Kosowski, Distributed Computing 24 (2011),
   *Derandomizing Random Walks in Undirected Graphs Using Locally Fair
   Exploration Strategies*, pp. 91-99. Downloaded and extracted primary author
   PDF. Least-Used-First counts undirected edge traversals, not vertex visits.
   https://www.labri.fr/perso/ilcinkas/publications/DisComp-ICALP09.pdf

Additional leads checked: Avin and Krishnamachari's 2006/2008 power-of-choice
walk samples neighbors and degree-normalizes counts; its general-graph
discussion reports simulations rather than an adversarial LFV-v theorem.
Friedrich and Sauerwald's deterministic-random-walk work concerns locally
balanced exits (rotor-router), not arbitrary LFV-v exits. A full local download
of its HPI PDF returned HTTP 503, so no full-source audit of it is asserted.
The 2011 grid-coverage literature's statement about regular graphs occurs in
its random-walk discussion, not an LFV-v theorem. None of these leads was used
to infer a missing theorem about the exact policy.

Outcome: no matching prior theorem for arbitrary-tie LFV-v on every connected
regular graph was located. Polynomial results for related VAW, LRTA*, rotor,
and edge-counting rules are known. This search does not establish novelty.

Downloaded-source hashes and audited-input hashes are recorded separately.
Partial raw primary web retrievals are in sources/web_retrieval_record.txt.
