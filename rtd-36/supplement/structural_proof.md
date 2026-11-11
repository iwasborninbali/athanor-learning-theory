# The maximum RTD of finite (3,6) classes is 2

## Definitions and the statement

Let C be a finite set of distinct binary functions on a finite domain X.
It is a (3,6) class if every restriction to at most three coordinates has
at most six distinct patterns. The domain size and the number of concepts
are arbitrary. Such classes have VC dimension at most 2, but the converse
is false: VC dimension 2 permits seven patterns on a triple.

A teaching set for c in C is a set of coordinates on which no other
concept agrees with c. TD(c;C) is its smallest size; TD_min(C) is the minimum
over c. RTD recursively removes all concepts attaining TD_min at the
current stage, and takes the largest minimum encountered.

**Theorem.** Every finite (3,6) class has RTD at most 2. The bound is
attained by the four functions on a two-point domain. Thus the maximum
in the (3,6) cell is exactly 2, including if VC dimension is required to
be exactly 2.

The proof below proves the stronger existence statement TD_min(C)<=2.
Every subclass remains a (3,6) class, so this bounds every recursive stage.

## Elementary VC-1 fact

Every nonempty finite class D of VC dimension at most 1 has TD_min(D)<=1.
For a singleton this means TD=0. Otherwise choose a smallest nonempty
one-coordinate fiber D_(i,b). If it has at least two distinct concepts,
some coordinate j splits it. The pair (i,j) is not shattered. If the
opposite i-fiber is nonempty, it must be constant on j; the opposite
j-value then defines a nonempty proper subfiber of D_(i,b), contradicting
minimality. If the opposite i-fiber is empty, either part of the j-split
is already a smaller one-coordinate fiber. Hence a minimum fiber is a
singleton and teaches one concept with one label.

The sixteen two-coordinate pattern sets, with the shattered set omitted,
exhaustively verify the proper-subfiber implication in `check_structural.py`.

## Minimum shattered-pair cell (Moran et al.'s argument)

Assume for a contradiction that C is nonempty and TD_min(C)>=3. By the
VC-1 fact, a pair of coordinates is shattered. Among **all four cells of
all shattered coordinate pairs**, choose a cell A of minimum size k.
Flip coordinate labels and write

    A = C_(u=0,v=0).

The other three (u,v)-cells are nonempty. Also k>=2, since a singleton
cell would teach its concept with two labels.

We first show VC(A)<=1. Suppose instead that A shatters another pair s,t.
These coordinates are distinct from u,v, which are constant on A. Let
P01,P10,P11 be the nonempty sets of (s,t)-patterns occurring in the other
three (u,v)-cells. Since A contributes all four (s,t)-patterns on the
u=0 side, the (3,6) condition on (u,s,t) gives

    |P10 union P11| <= 2.

Likewise (v,s,t) gives |P01 union P11|<=2. As P11 is nonempty, their total
union has at most three patterns. Some (s,t)-pattern therefore occurs in
A and nowhere outside A. Its global (s,t)-cell is a nonempty proper
subset of A. The pair s,t is shattered by C, contradicting the definition
of k. Thus VC(A)<=1. This is the argument underlying Moran et al. (2015),
Lemma 1.7; its finite set implication is checked exhaustively over all
15^3 triples of nonempty subsets of a four-pattern universe.

## The descent that improves three labels to two

By the VC-1 fact and k>=2, some c in A is identified within A by a single
coordinate w. Flip w so c(w)=1 and every other row of A has w=0. In
particular w is distinct from u and v.

On the triple (u,v,w), the four nonempty (u,v)-cells contribute one
pattern each, and every cell split by w contributes one additional
pattern. At most two cells can split, because there are at most six
patterns. A is split, so at least one of its two adjacent cells, C01 and
C10, is not split. Interchange u,v if necessary so C01 is not split.

C01 must have w=1: otherwise the two labels (u=0,w=1) would teach c in C.
Consequently

    C_(u=0,w=0) = A minus {c},

a nonempty cell of size k-1. Also C10 must contain a row with w=1;
otherwise (v=0,w=1) would teach c. Hence the (u,w)-patterns (0,0), (0,1)
and (1,1) all occur.

If (1,0) also occurs, the pair (u,w) is shattered, and its (0,0)-cell has
size k-1. This contradicts the minimality of A among cells of shattered
pairs.

If (1,0) does not occur, then the entire w=0 fiber is A minus {c}. It has
VC dimension at most 1, being a subclass of A. Some concept d in that
fiber is therefore identified within it by at most one label. Adjoining
the label w=0 teaches d in C with at most two labels, contradicting
TD_min(C)>=3.

Both alternatives are impossible. Therefore every nonempty (3,6) class
has a concept with a teaching set of size at most two. Heredity finishes
the recursive-teaching claim. On the full two-coordinate cube, every
concept needs both coordinates; all four are removed at the first stage,
so its exact RTD is 2.

## What is independently checked

`check_structural.py` imports only the Python standard library and no
search code. It enumerates all local Boolean pattern cases for the VC-1
proper-fiber implication, the minimum shattered-cell lemma, and the new
descent. The new descent has seven admissible trace sets; all satisfy
one of the two alternatives above. Its seven-pattern control fails, as
required: the argument does not incorrectly prove the false VC-2/(3,7)
bound. The standard finite minimality and hereditary steps are the
written mathematical proof, rather than a claimed Lean formalization.

`check.py` independently computes the exact recursive teaching hierarchy
of the square and of Warmuth's known RTD-3 (3,7) class. The already checked
n<=8 SAT exclusion is additional independent bounded-case evidence; it
is not needed for the structural theorem.
