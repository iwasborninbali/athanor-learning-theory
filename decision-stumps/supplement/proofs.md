All statements below concern $m\ge2,d\ge1$. Features have distinct
values; ranks are sufficient. Labels, permutations and stumps are
otherwise unrestricted. Write $P,N$ for the two label classes.
`A` permits all internal gaps, `T` only gaps between opposite labels;
both signs are present. `C` adds two shared constant classifiers to
either class. Dominance always means **proper** inclusion of error sets.
Let $e$ count named stumps, retaining duplicates, and $q$ count
distinct minimal error sets. Let $M_X,Q_X$ be their respective maxima.

**One feature.** In an order $i_1,\ldots,i_m$, a good transition stump
is the unique stump at an opposite-label gap which gets both adjacent
examples right. Every other stump on that feature, including constants,
gets at least one of those two examples wrong. Therefore each good
transition stump is minimal, and different good transition stumps have
incomparable error sets. This argument is about local minimality;
another feature can still dominate it.

Let $r$ be the number of transitions and $s,t$ the lengths of the
first and last monochromatic runs. Then the exact local counts are

$$
e_T=q_T=r,\qquad
e_A=q_A=r+\mathbf1[y_{i_1}=y_{i_m},s\ge2]
              +\mathbf1[y_{i_1}=y_{i_m},t\ge2],
$$

$$
e_C=q_C=r+\mathbf1[y_{i_1}=y_{i_m}]. \tag{1}
$$

To prove completeness, denote the right-positive stump's error set at
cut $k$ by

$$
A_k=(P\cap\{i_1,\ldots,i_k\})\cup
    (N\setminus\{i_1,\ldots,i_k\}).
$$

For $k<l$, $A_l\setminus A_k$ consists of the positive examples
between the cuts and $A_k\setminus A_l$ of the negative ones.
Moving through a monochromatic run therefore strictly improves one
orientation in one direction, until a good transition or an endpoint
is reached. A wrong-polarity transition is strictly dominated by the
same-polarity good stump at a neighboring transition if $r\ge2$.
If $r=1$, the good stump is perfect and dominates its inverse. If
$r=0$, class `T` is empty.

For `A`, an extra left-end candidate exists only when the first two
labels agree. It errs on the first example and on every example of
the opposite label. If the last label differs from the first, the
last good transition dominates it. If the last label agrees with the
first, any other same-orientation cut errs on the second example,
and every opposite-orientation cut errs on the last example; both
examples are outside the candidate's errors. It is therefore minimal.
The right-end argument is symmetric. These endpoint stumps are
different even for a constant-label sample with $m=2$. This proves
the `A` formula, including that case.

With constants, same-label internal cuts are strictly dominated by
a transition or a constant, so `A` and `T` have exactly the same
effective stumps after constants are added. A constant with error
class $P$ survives precisely when both endpoints are negative:
otherwise an end transition strictly dominates it; with negative
endpoints every nonconstant stump errs on one of them and cannot
have errors contained in $P$. The symmetric assertion holds for
error class $N$. If the sample is homogeneous, its correct constant
alone survives. This proves (1).

**Exact named maxima in every dimension.**

$$
M_T(m,d)=d(m-1),\quad M_A(m,d)=d\max(2,m-1),\tag{2}
$$

$$
M_C(m,d)=
\begin{cases}d(m-1)+1,&m\text{ odd},\\d(m-1),&m\text{ even}.\end{cases}\tag{3}
$$

A globally minimal stump is locally minimal on its own feature.
For `T` this gives the first bound. For `A`, if $r>0$, the extra
end-run indicators in (1) consume extra examples beyond the $r+1$
runs, giving count at most $m-1$; if $r=0$, the count is 2.
Copying an alternating feature $d$ times attains the bounds for
$m\ge3$. For `A`, $m=2$, use identical labels: both stumps per
feature survive. Copying features is legitimate: they are different
coordinates, and their named stumps remain different functions even
when their predictions on the sample coincide.

For `C`, at most one constant survives when both labels occur.
If none survives, at most $d(m-1)$ internal stumps survive. If one
survives, every feature must have both endpoints in the same opposite
label class, so all transition counts are even. The internal bound
is then $d(m-1)$ for odd $m$, or $d(m-2)$ for even $m$, plus
one shared constant. The homogeneous case has just one effective
constant. Alternating copied features attain (3).

For $d=1$, there are no identical error sets among the stumps of
any of these classes, so (2)–(3) are also the exact distinct-set maxima.
For general $d$, the universal bound is

$$
Q_X(m,d)\le \min\{M_X(m,d),\binom m{\lfloor m/2\rfloor}\}.\tag{4}
$$

For completeness, the antichain bound follows by counting uniformly
random maximal Boolean chains: a set of size $k$ lies on one with
probability $1/\binom mk$, and a chain meets an antichain at most
once. Hence $\sum_{S\in\mathcal E}1/\binom m{|S|}\le1$.

**Distinct-set lower bound with explicit markers.** Let $b\ge2$
be even with $\binom b{b/2}\ge2d$, and suppose $m\ge b+2$. Then

$$
Q_X(m,d)\ge d(m-b-1)\qquad(X=A,T,C).\tag{5}
$$

Take $b$ positive marker examples. Select $d$ distinct $b/2$-sets
$S_j$ containing marker 0. Their complements are different from
one another and from all selected sets. The remaining $L=m-b$
examples have alternating labels in a common order. Feature $j$
orders $S_j$, then all active examples, then the other markers.

Every active gap has one good stump. Its marker errors are $S_j$
or $S_j^c$, depending on polarity. All $2d$ tags have equal size
and are different. Thus a stump with a threshold inside the active
block on another feature, of either polarity, cannot dominate it.
On its own feature the good-stump argument above applies. Every
threshold outside the block predicts a constant on it and errs on
an entire active label class; the good stump correctly classifies
at least one active example in each class. Outside thresholds and
constants therefore cannot dominate it either. All $d(L-1)$ good
stumps have different error sets and survive.

The smallest such $b$ is $O(\log(d+1))$, since
$\binom b{b/2}\ge2^b/(b+1)$. Consequently, along any sequence
$m\to\infty$ with $\log d=o(m)$,

$$
Q_X(m,d)=(1+o(1))dm.\tag{6}
$$

This is a statement about the maximum over datasets, not every dataset.

There is also an exact explicit regime. For odd $m=2n+1\ge4d-1$,

$$
Q_A(m,d)=Q_T(m,d)=d(m-1),\qquad Q_C(m,d)=d(m-1)+1.\tag{6a}
$$

Use $n$ positives $P_0,\ldots,P_{n-1}$ in the same order in every
feature, and $n+1$ negatives indexed cyclically. Feature $j$,
$0\le j<d$, interleaves the cyclic negative order starting at
$2j+1$ with the fixed positive order, beginning and ending negative.
All good errors have size $n$. At each positive-error count
$1\le a<n$, the two polarities use respectively the fixed $a$-prefix
and $a$-suffix of the positive order, which differ; within a polarity,
different cyclic shifts give different negative subsets of sizes
$1,\ldots,n-1$. At $a=0$, the two pure-negative error sets omit the
first or last negative, indexed $2j+1,2j$. These $2d$ omitted
indices are all different because $2d\le n+1$. Thus all $d(m-1)$
good errors are distinct. With constants, $P$ is one further
size-$n$ error set. The upper bounds in (2)–(4) prove equality.

**Exact ceilings for odd sample sizes.** For $m=2n+1\ge3$,

$$
\sup_{d\ge1}Q_A(m,d)=\sup_{d\ge1}Q_C(m,d)=\binom mn,
\qquad
\sup_{d\ge1}Q_T(m,d)=\binom mn-1.\tag{7}
$$

For `T`, each effective stump is a good transition on its own feature,
so its errors contain neither full label class. In a mixed sample,
each full middle level contains a set including the smaller label
class. Thus neither full middle level is a permissible antichain.
Equality in the Boolean antichain bound for odd $m$ can only be
one of these two full levels. Here is a short justification: equality
forces all members to have sizes $n,n+1$. The containment graph
between these levels is connected and $(n+1)$-regular on both sides
(successive single-element replacements connect all (n)-sets).
For a nonempty proper subset of the lower level, its upper neighbor
set is strictly larger: equality in edge counting would disconnect
that subset and its neighbors. Hence a mixed-level antichain has
strictly fewer than $\binom mn$ members. A homogeneous `T` sample
has no stumps. This proves the `T` upper bound in (7).

For `T` attainment, use $n$ positives, $n+1$ negatives, and
features with alternating pattern $NPNP\cdots N$. At every internal
gap the two error sizes are $n,n+1$. All good errors have size $n$.
For any $n$-set $S\ne P$, put $a=|S\cap P|\le n-1$. A prefix
with positives $S\cap P$ and negatives $N\setminus S$ has size
$2a+1$, and fits the alternating pattern. The right-positive stump
there has exactly error set $S$. Use one such feature for each $S$.
This attains every middle set except $P$, with at most
$\binom mn-1$ features. Adding constants supplies $P$ itself and
proves `C` attainment with the same feature bound.

For `A` attainment, use $n-1$ positives and $n+2$ negatives,
in pattern $NN(PN)^{n-1}N$. The internal error sizes are again
$n,n+1$. For any $n$-set $S$, let $a=|S\cap P|\le n-1$.
A prefix with positives $S\cap P$ and negatives $N\setminus S$
has size $2a+2\le m-1$, fits that pattern, and realizes $S$.
One feature per middle set suffices. This includes $n=1$, when
there are no positive examples. No smaller errors are introduced.

For even $m\ge4$ and sufficiently many features, a useful partial
counterpart is

$$
Q_C(m,d)\ge\tfrac12\binom m{m/2},\qquad
Q_A(m,d),Q_T(m,d)\ge\tfrac12\binom m{m/2}-1,\tag{8}
$$

whenever $d\ge\binom{m-1}{(m-2)/2}-1$. Start from the odd
`C` construction on $m-1$ examples and duplicate one positive
example adjacently in every feature, with distinct ranks. No new
transition is introduced. Every old error set either contains both
copies or neither, preserving inclusion, so the effective distinct
count stays $\binom{m-1}{(m-2)/2}$. Classes `A+C` and `T+C` have
the same effective sets. Removing the constants preserves every
nonconstant minimal set, losing at most the one minimal constant.
Padding by repeated features extends the witnesses to larger $d$.
Equation (8) does not identify the exact even $m$ ceiling.

A stronger ceiling lower bound, with a larger sufficient feature
count, is

$$
\sup_d Q_X(2n,d)\ge\binom{2n}{n-1}\qquad(X=A,T,C).\tag{8a}
$$

Use $n$ positives and $n$ negatives, with every feature alternating
negative/positive. For every $(n-1)$-set $S$, let
$a=|S\cap P|$. A prefix with positives $S\cap P$ and negatives
$N\setminus S$ has size $2a+1\le2n-1$, fits the alternating
pattern, and its right-positive good stump errs exactly on $S$.
One feature per such $S$ suffices. All available errors have size
at least $n-1$. After all these sets are present, every larger error
contains a present $(n-1)$-set, so the effective family is exactly
that full level. Thus (8a) holds for
$d\ge\binom{2n}{n-1}$, by padding with repeated features.
Combined with (4), the ratio of this lower bound to the ceiling upper
bound is $n/(n+1)=m/(m+2)$. The closure certificates prove equality
in (8a) at $m=4,6$, for every cut convention, after maximizing over
all dimensions. Equality for general even $m$ is not established.

**Fair-label/random-order model.** Labels are independent uniform
signs, independent of $d$ independent uniform feature permutations.
There is no conditioning on weak learnability, nonseparability or
class balance. For one feature,

$$
\mathbb E q_T=(m-1)/2,\quad
\mathbb E q_A=m/2\ (m\ge3),\quad
\mathbb E q_C=m/2.\tag{9}
$$

For `A`, $m=2$, the expectation is $3/2$. These hold for named
counts too. Each transition indicator has expectation $1/2$.
Each `A` endpoint indicator is equality of three independent labels
and has expectation $1/4$ when $m\ge3$. The `C` endpoint equality
has probability $1/2$. Formula (1) proves (9).

For a quantitative general-$d$ lower bound, choose an integer
$1\le a\le\lfloor m/2\rfloor$, and put $K=m-2a+1$. For every
class $X=A,T,C$,

$$
\mathbb E q_X\ge {dK\over2}
-4d(d-1)K(m-1)(m+1)(3/4)^{2a}.\tag{10}
$$

It is harmless when this bound is negative. The respective upper
bounds are $d(m-1)/2,dm/2,dm/2$, with $m\ge3$ for `A`.

To prove (10), keep the good stumps at central cuts
$a\le k\le m-a$; their expected count is $dK/2$. They cannot be
dominated on their own feature or by a constant. Remove a candidate
if any stump on another feature has an error set contained in or
equal to its error set. The remaining candidates are distinct and
globally minimal. Conditional on two prediction vectors at Hamming
distance $D$, the probability of this non-strict inclusion over the
fair labels is $2^{-D}$: on every disagreeing coordinate the label
must equal the competitor prediction (so the competitor is correct and
the candidate is wrong).

Fix a candidate prediction vector with at least $a$ positive and
$a$ negative entries. An independent feature at any fixed gap and
polarity has a uniform $l$-subset as its positive predictions.
Generate it instead by independent Bernoulli $p=l/m$ bits and
condition on exactly $l$ ones. That binomial event has probability
at least $1/(m+1)$, because $l$ is a mode. Before conditioning,
the factor for one positive and one negative candidate coordinate is

$$
{1+p\over2}(1-p/2)\le9/16.
$$

Pair $a$ such coordinates; the other factors are at most 1.
Thus the inclusion probability is at most
$(m+1)(3/4)^{2a}$. There are $2dK$ possible signed candidates
and $2(d-1)(m-1)$ competing signed stumps. A union bound bounds
the expected number removed and yields (10); conditioning on being
a good candidate is unnecessary for this upper bound on losses.
The other feature's label-dependent gap restriction can only remove
competitors, so the bound applies to `T` as well.

Taking $a=o(m)$ but $a\gg\log(dm)$ gives, whenever
$m\to\infty$ and $\log d=o(m)$,

$$
\mathbb E q_X=(1+o(1))dm/2,
\qquad \mathbb E e_X=(1+o(1))dm/2.\tag{11}
$$

The second conclusion follows from $q_X\le e_X$ and the same local
upper bounds. These are expectations under the specified model,
not concentration bounds or a statement about real datasets.
