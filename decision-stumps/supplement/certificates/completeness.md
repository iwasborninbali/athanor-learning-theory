The finite exclusions use two independent representations. Neither
relies on a solver's claim of optimality. `check.py` uses only the
Python standard library and does not import any search or builder code.

**Fixed dimension.** Relabel the examples along the first feature so
that it is the identity order. Global label reversal fixes its first
label to +1. This leaves all $2^{m-1}$ binary label words. Reverse
each later feature if needed so that its first example index is less
than its last; reversal exchanges cut positions and polarities and
preserves the full error family, including the transition restriction.
Order the later features arbitrarily by their permutation indices.
Every dataset is covered, possibly more than once. Repeated feature
orders are allowed. The independent enumeration covers exactly

$$
2^{m-1}\binom{m!/2+d-2}{d-1}
$$

configurations. It evaluates predictions example by example, at every
permitted gap and polarity, to generate raw error families. For a
family $F$, let $U(F)$ be every proper superset of a member, in the
full Boolean lattice. Then

$$
\min(\bigcup_j F_j)=(\bigcup_j F_j)\setminus\bigcup_j U(F_j).
$$

The checker implements this identity with Python integers. It keeps
all raw feature families in the enumeration, including locally
dominated stumps. The searcher instead generates errors by prefix XOR,
removes local strict supersets and deduplicates feature antichains.
This compression is valid because a local strict dominator remains
present in every union. These independent methods agree on all 64
targets in `exclusions.json`. `logs/independent-check.log` records every
target, exact raw-instance count and runtime.

**All dimensions, m=4,5,6.** A label assignment can first be relabeled
to put its $p$ positives first; global label reversal permits
$0\le p\le\lfloor m/2\rfloor$. Every possible feature permutation
is then available as a generator. Define the operation on antichains

$$
A\star B=\min(A\cup B).
$$

This operation is associative, commutative and idempotent. A dataset
with any number of features produces an iterated product of generator
antichains. Each gzip JSON certificate lists a finite family of
antichains containing the empty family and closed under adding every
possible generator. The checker regenerates **all** raw feature
families directly, verifies that every listed state is an antichain,
and checks every closure edge. Thus every reachable dataset state lies
in the listed family, by induction on its feature count. A maximum
over the listed family is a valid upper bound even without trusting
the generator's claim that every listed state was reached.

The certificates also assign a nonnegative integer `depth` to every
state, with depth(empty)=0 and

$$
\operatorname{depth}(A\star F)\le\operatorname{depth}(A)+1
$$

for every feature generator $F$. The checker verifies this inequality
on every edge. Therefore a dataset with at most $d$ features must
have a state assigned depth at most $d$, again by induction. Counting
the largest listed state at depth at most $d$ certifies an upper
bound at each $d$. This does **not** require the checker to trust
that assigned depths are shortest distances. The builder supplies a
separate explicit dataset attaining each claimed count, padding its
feature list with a repeated order when necessary. The direct witness
checker verifies all those lower bounds. Matching them proves the
entire maximum curve, not only a ceiling as $d\to\infty$.

There is one certificate for every $p$ and convention. The global
curve checker verifies that no label count is omitted, takes their
maxima, and checks the corresponding explicit witnesses. For $d$
past the final recorded depth, closure gives the same upper ceiling;
repeated-feature padding gives the same lower bound. This certifies
all $d\ge1$ at these sample sizes. `global-curves.json` contains the
aggregate curves. The old and new closure pilot rows in the log are
historical; the final certificate files include depths and are the
ones checked in `logs/final-certificate-check.log`.

**Witness normalization.** The builder considers each possible first
feature and both its orientations, renames rows to make that feature
the identity, flips all labels to make label 0 positive, chooses the
lexicographically smaller reversal of every remaining feature, sorts
those features, and takes the lexicographically smallest resulting
label/order tuple. This is canonical under row permutations, feature
permutations, per-feature reversals and global label reversal. It is
not a claim of equivalence under every possible accidental equality
of error families. The independent checker evaluates the actual
normalized witnesses without relying on this canonicalization claim.

`effective_error_masks` use bit $i$ for example $i$, numbered from
zero. Equal masks are retained once for the distinct-set count; all
their occurrences are retained for `named_count`. Constants occur
once each, shared between features. A mask is removed only if a
different strictly smaller error set is present. This avoids deleting
both members of an identical pair.
