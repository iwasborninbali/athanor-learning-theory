"""Independent audit. Standard library only; never imports candidate code.

Exact search uses upward-closed families of error sets, whose union is bitwise
OR. This is a different state representation from the supplied antichains.
All file writes are relative to this verifier's working directory.
"""
import argparse
from collections import Counter, deque
import gzip
import itertools
import json
import math
from pathlib import Path
import random
import time

START_CPU = time.process_time()
SOURCE = Path(__file__).resolve().parents[1] / 'certificates'
KINDS = ('A', 'T', 'C')
NAMES = {'A': 'all', 'T': 'transition', 'C': 'constants'}


def budget():
    if time.process_time() - START_CPU > 1000:
        raise RuntimeError('Conservative independent-audit CPU limit reached')


def raw_errors(labels, order, kind):
    """Evaluate each prediction on each example, retaining named copies."""
    m = len(labels)
    answer = []
    for cut in range(1, m):
        if kind == 'T' and labels[order[cut-1]] == labels[order[cut]]:
            continue
        for orientation in (-1, 1):
            error = 0
            for position, example in enumerate(order):
                prediction = orientation * (-1 if position < cut else 1)
                if prediction != labels[example]:
                    error |= 1 << example
            answer.append(error)
    return answer


def constants(labels):
    return [sum(1 << i for i, y in enumerate(labels) if y != sign)
            for sign in (-1, 1)]


def minimal(errors):
    kept = []
    for e in sorted(set(errors), key=lambda x: (x.bit_count(), x)):
        if not any(f & e == f for f in kept):
            kept.append(e)
    return tuple(sorted(kept))


def local_formula(labels, order, kind):
    word = [labels[i] for i in order]
    r = sum(x != y for x, y in zip(word, word[1:]))
    same_ends = word[0] == word[-1]
    if kind == 'T':
        return r
    if kind == 'C':
        return r + same_ends
    return r + (same_ends and word[0] == word[1]) + (same_ends and word[-1] == word[-2])


def upward_table(m):
    return [sum(1 << f for f in range(1 << m) if e & f == e)
            for e in range(1 << m)]


def upward(errors, table):
    state = 0
    for e in errors:
        state |= table[e]
    return state


def boundary(state, predecessors):
    total = 0
    while state:
        bit = state & -state
        e = bit.bit_length() - 1
        # The full family is retained separately: all immediate subsets suffice.
        total += not (boundary.family & predecessors[e])
        state ^= bit
    return total


def q_upward(state, predecessors):
    boundary.family = state
    return boundary(state, predecessors)


def exact_closures():
    results = []
    globals_ = {}
    certificates_checked = 0
    closure_edges = 0
    for m in range(2, 7):
        table = upward_table(m)
        predecessors = [sum(1 << (e ^ (1 << i)) for i in range(m) if e >> i & 1)
                        for e in range(1 << m)]
        permutations = list(itertools.permutations(range(m)))
        for kind in KINDS:
            aggregate = []
            for p in range(m // 2 + 1):
                tic = time.process_time()
                labels = [1] * p + [-1] * (m-p)
                shared = constants(labels) if kind == 'C' else []
                generators = sorted({upward(raw_errors(labels, order, kind) + shared, table)
                                     for order in permutations})
                distance = {0: 0}
                queue = deque([0])
                maxima = [0]
                edges = 0
                while queue:
                    state = queue.popleft()
                    depth = distance[state]
                    q = q_upward(state, predecessors)
                    while len(maxima) <= depth:
                        maxima.append(0)
                    maxima[depth] = max(maxima[depth], q)
                    for generator in generators:
                        child = state | generator
                        if child not in distance:
                            distance[child] = depth + 1
                            queue.append(child)
                        edges += 1
                    if edges % 10000 < len(generators):
                        budget()
                curve = list(itertools.accumulate(maxima, max))
                for d, q in enumerate(curve):
                    while len(aggregate) <= d:
                        aggregate.append(aggregate[-1] if aggregate else 0)
                    aggregate[d] = max(aggregate[d], q)
                if m >= 4:
                    filename = SOURCE / f'closure_{NAMES[kind]}_m{m}_p{p}.json.gz'
                    with gzip.open(filename, 'rt') as f:
                        certificate = json.load(f)
                    assert (certificate['m'], certificate['p']) == (m, p)
                    assert certificate['mode'] == ('all' if kind == 'A' else 'transition')
                    assert certificate['constants'] == (kind == 'C')
                    supplied = {}
                    for encoded, depth in zip(certificate['states'], certificate['depths']):
                        antichain_bits = int(encoded, 16)
                        antichain = [e for e in range(1 << m) if antichain_bits >> e & 1]
                        assert len(antichain) == len(minimal(antichain))
                        s = upward(antichain, table)
                        assert s not in supplied
                        supplied[s] = depth
                    assert len(certificate['states']) == len(certificate['depths'])
                    assert supplied == distance, (m, kind, p, 'state/depth discrepancy')
                    assert certificate['curve'] == curve
                    assert certificate['maximum'] == max(curve)
                    certificates_checked += 1
                    closure_edges += edges
                record = dict(m=m, kind=kind, positives=p, generators=len(generators),
                              states=len(distance), edges=edges, curve=curve,
                              cpu_seconds=round(time.process_time()-tic, 4))
                results.append(record)
                print(json.dumps(record), flush=True)
            globals_[f'{m}{kind}'] = list(itertools.accumulate(aggregate, max))
    for row in json.loads((SOURCE/'global-curves.json').read_text()):
        kind = next(k for k in KINDS if NAMES[k] == row['kind'])
        actual = globals_[f"{row['m']}{kind}"]
        expected = row['curve']
        for d in range(max(len(actual), len(expected))):
            assert actual[min(d, len(actual)-1)] == expected[min(d, len(expected)-1)]
    return dict(rows=results, global_curves=globals_, certificates_checked=certificates_checked,
                closure_edges=closure_edges)


def formulas_and_witnesses():
    rng = random.Random(20261111)
    checks = 0
    for m in range(2, 13):
        for word in itertools.product((-1, 1), repeat=m):
            for kind in KINDS:
                raw = raw_errors(word, tuple(range(m)), kind)
                if kind == 'C':
                    raw += constants(word)
                effective = minimal(raw)
                named = sum(e in effective for e in raw)
                assert len(effective) == named == local_formula(word, tuple(range(m)), kind)
                checks += 1
    random_checks = 0
    for _ in range(2000):
        m = rng.randrange(2, 81)
        labels = rng.choices((-1, 1), k=m)
        order = rng.sample(range(m), m)
        for kind in KINDS:
            raw = raw_errors(labels, order, kind)
            if kind == 'C':
                raw += constants(labels)
            assert len(minimal(raw)) == local_formula(labels, order, kind)
            random_checks += 1
    checked_witnesses = 0
    for witness in json.loads((SOURCE/'witnesses.json').read_text()):
        kind = 'C' if witness['constants'] else ('T' if witness['mode'] == 'transition' else 'A')
        labels = witness['labels']
        raw = []
        for order in witness['orders']:
            assert sorted(order) == list(range(witness['m']))
            raw.extend(raw_errors(labels, order, kind))
        if kind == 'C':
            raw.extend(constants(labels))
        effective = minimal(raw)
        assert list(effective) == witness['effective_error_masks'], witness['id']
        assert len(effective) == witness['count'], witness['id']
        assert sum(e in effective for e in raw) == witness['named_count'], witness['id']
        checked_witnesses += 1
        budget()
    return dict(exhaustive_formula_cases=checks, random_formula_cases=random_checks,
                supplied_witnesses_checked=checked_witnesses)


def raw_fixed_dimension(m, d):
    """No local-minimum compression; first order fixed by row relabeling."""
    tic = time.process_time()
    table = upward_table(m)
    pred = [sum(1 << (e ^ (1 << i)) for i in range(m) if e >> i & 1)
            for e in range(1 << m)]
    later = [o for o in itertools.permutations(range(m)) if o[0] < o[-1]]
    best = {k: 0 for k in KINDS}
    configurations = 0
    for tail in itertools.product((-1, 1), repeat=m-1):
        labels = (1,) + tail
        first = {}
        features = {}
        for kind in KINDS:
            shared = constants(labels) if kind == 'C' else []
            first[kind] = upward(raw_errors(labels, range(m), kind) + shared, table)
            features[kind] = [upward(raw_errors(labels, o, kind) + shared, table) for o in later]
        for indices in itertools.combinations_with_replacement(range(len(later)), d-1):
            for kind in KINDS:
                state = first[kind]
                for j in indices:
                    state |= features[kind][j]
                best[kind] = max(best[kind], q_upward(state, pred))
            configurations += 1
            if configurations % 10000 == 0:
                budget()
    return dict(m=m, d=d, maxima=best, configurations=configurations,
                cpu_seconds=round(time.process_time()-tic, 4))


def fast_features(labels, orders):
    """Raw errors for simulation, toggling one prediction at each cut."""
    m = len(labels)
    full = (1 << m)-1
    neg = sum(1 << i for i, y in enumerate(labels) if y == -1)
    families = {k: [] for k in KINDS}
    for order in orders:
        err = neg
        for j, example in enumerate(order[:-1]):
            err ^= 1 << example
            families['A'].extend((err, full ^ err))
            if labels[example] != labels[order[j+1]]:
                families['T'].extend((err, full ^ err))
    families['C'] = families['T'] + [neg, full ^ neg]
    return families


def simulate():
    rng = random.Random(777011)
    rows = []
    cases = [(2, 1, 10000), (5, 1, 10000), (12, 1, 10000),
             (16, 2, 3000), (32, 2, 1500), (64, 2, 600),
             (128, 2, 250), (256, 2, 100), (512, 2, 40),
             (64, 4, 300), (128, 4, 120), (256, 4, 50)]
    for m, d, samples in cases:
        sums = {k: [0., 0., 0., 0.] for k in KINDS}
        tic = time.process_time()
        for _ in range(samples):
            labels = rng.choices((-1, 1), k=m)
            orders = [rng.sample(range(m), m) for _ in range(d)]
            for kind, raw in fast_features(labels, orders).items():
                effective = minimal(raw)
                count = Counter(raw)
                named = sum(count[e] for e in effective)
                q = len(effective)
                sums[kind][0] += q
                sums[kind][1] += q*q
                sums[kind][2] += named
                sums[kind][3] += named*named
            budget()
        for kind in KINDS:
            s, s2, e, e2 = sums[kind]
            mean = s / samples
            sem = math.sqrt(max(0, (s2-s*s/samples)/(samples-1)/samples))
            named_mean = e/samples
            upper = d*(m-1)/2 if kind == 'T' else (1.5*d if m == 2 and kind == 'A' else d*m/2)
            bounds = [(d*(m-2*a+1)/2 -
                       4*d*(d-1)*(m-2*a+1)*(m-1)*(m+1)*(.75**(2*a)), a)
                      for a in range(1, m//2+1)]
            lower, a = max(bounds)
            row = dict(m=m, d=d, samples=samples, kind=kind,
                       q_mean=mean, q_sem=sem, named_mean=named_mean,
                       ratio_to_dm_over_2=mean/(d*m/2), upper=upper,
                       best_lower=lower, best_a=a,
                       cpu_seconds=round(time.process_time()-tic, 4))
            rows.append(row)
            print(json.dumps(row), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('structure', 'simulation'))
    args = parser.parse_args()
    if args.mode == 'structure':
        output = {'closures': exact_closures(), 'direct': []}
        for m, d in ((5, 2), (5, 3), (6, 2), (6, 3)):
            record = raw_fixed_dimension(m, d)
            output['direct'].append(record)
            print(json.dumps(record), flush=True)
        output['formulas_and_witnesses'] = formulas_and_witnesses()
    else:
        output = {'simulation': simulate()}
    output['cpu_seconds'] = time.process_time()-START_CPU
    Path(f'independent-{args.mode}.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'finished': args.mode, 'cpu_seconds': output['cpu_seconds']}), flush=True)


if __name__ == '__main__':
    main()
