#!/usr/bin/env python3
"""Independent stdlib-only witness and exhaustive exclusion checker.

Does not import search.py. Predictions are evaluated directly, rather than
using the searcher's prefix-XOR or local-antichain compression. Exclusion
enumerates every raw order (modulo reversal), with no antichain deduplication.
"""
import argparse
import hashlib
import gzip
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path


def errors_direct(labels, orders, mode, constants):
    m = len(labels)
    errors = []
    for order in orders:
        assert sorted(order) == list(range(m))
        rank = {point: j for j, point in enumerate(order)}
        for gap in range(1, m):
            if mode == 'transition' and labels[order[gap-1]] == labels[order[gap]]:
                continue
            for sign in (1, -1):
                err = frozenset(i for i in range(m)
                                if sign * (1 if rank[i] >= gap else -1) != labels[i])
                errors.append(err)
    if constants:
        for sign in (1, -1):
            errors.append(frozenset(i for i, y in enumerate(labels) if y != sign))
    return errors


def check_witness(w):
    assert w['m'] == len(w['labels']) and w['d'] == len(w['orders'])
    assert all(y in (-1, 1) for y in w['labels'])
    errors = errors_direct(w['labels'], w['orders'], w['mode'], w['constants'])
    distinct = set(errors)
    effective = {a for a in distinct if not any(b < a for b in distinct)}
    masks = sorted(sum(1 << i for i in a) for a in effective)
    assert masks == sorted(w['effective_error_masks']), (w.get('id'), masks)
    assert len(effective) == w['count']
    if 'named_count' in w:
        assert sum(a in effective for a in errors) == w['named_count']
    return len(effective)


def check_all_witnesses(path):
    data = json.loads(Path(path).read_text())
    for w in data:
        check_witness(w)
    print(f'PASS {len(data)} explicit witnesses', flush=True)


def exclusion(m, d, mode, constants):
    """Return the exact maximum by a complete, separately implemented search.

    A family F is represented by a Python integer whose bit number a records
    error set a. U is the union of all proper upper sets of its members.
    Minimal members of union_i F_i are (OR F_i) & ~(OR U_i).
    All raw stump errors, including dominated ones, enter F_i and U_i.
    """
    assert m >= 2 and 1 <= d <= 4
    universe = list(range(1 << m))
    proper_upper = [sum(1 << b for b in universe if a != b and (a & b) == a)
                    for a in universe]
    orders = [order for order in itertools.permutations(range(m)) if order[0] < order[-1]]
    identity = tuple(range(m))
    maximum = 0
    checked = 0
    for bits in range(1, 1 << m, 2):  # Global label flip fixes label 0 to +1.
        labels = [1 if bits & (1 << i) else -1 for i in range(m)]
        raw = []
        for order in orders:
            errsets = errors_direct(labels, [order], mode, constants)
            masks = {sum(1 << i for i in a) for a in errsets}
            f = sum(1 << a for a in masks)
            u = 0
            for a in masks:
                u |= proper_upper[a]
            raw.append((f, u))
        root_index = orders.index(identity)
        f0, u0 = raw[root_index]
        if d == 1:
            maximum = max(maximum, (f0 & ~u0).bit_count())
            checked += 1
        elif d == 2:
            for f1, u1 in raw:
                maximum = max(maximum, ((f0 | f1) & ~(u0 | u1)).bit_count())
                checked += 1
        elif d == 3:
            for j, (f1, u1) in enumerate(raw):
                f01, u01 = f0 | f1, u0 | u1
                for k in range(j, len(raw)):
                    f2, u2 = raw[k]
                    maximum = max(maximum, ((f01 | f2) & ~(u01 | u2)).bit_count())
                    checked += 1
        else:
            for j, (f1, u1) in enumerate(raw):
                f01, u01 = f0 | f1, u0 | u1
                for k in range(j, len(raw)):
                    f2, u2 = raw[k]
                    f012, u012 = f01 | f2, u01 | u2
                    for l in range(k, len(raw)):
                        f3, u3 = raw[l]
                        maximum = max(maximum, ((f012 | f3) & ~(u012 | u3)).bit_count())
                        checked += 1
    expected = (1 << (m-1)) * math.comb(math.factorial(m)//2+d-2, d-1)
    assert checked == expected, (checked, expected)
    return maximum, checked


def check_exclusions(path, keys=None):
    entries = json.loads(Path(path).read_text())
    for entry in entries:
        key = entry['id']
        if keys and key not in keys:
            continue
        start = time.perf_counter()
        got, count = exclusion(entry['m'], entry['d'], entry['mode'], entry['constants'])
        assert got == entry['maximum'], (key, got, entry['maximum'])
        print(json.dumps({'id': key, 'maximum': got, 'raw_instances': count,
                          'seconds': round(time.perf_counter()-start, 6), 'status': 'PASS'}), flush=True)


def check_one_feature(max_m=12):
    """Check closed formulas and exact fair-label expectations by direct sets."""
    for m in range(2, max_m+1):
        sums = [0, 0, 0]
        for labels in itertools.product((-1, 1), repeat=m):
            r = sum(labels[i] != labels[i+1] for i in range(m-1))
            same = labels[0] == labels[-1]
            predicted = [r, r + int(same and labels[0] == labels[1])
                         + int(same and labels[-2] == labels[-1]), r + int(same)]
            for j, (mode, constants) in enumerate([('transition', False), ('all', False), ('all', True)]):
                errsets = set(errors_direct(labels, [list(range(m))], mode, constants))
                count = sum(not any(b < a for b in errsets) for a in errsets)
                assert count == predicted[j], (m, labels, mode, constants, count, predicted[j])
                sums[j] += count
        means = [Fraction(s, 1 << m) for s in sums]
        assert means[0] == Fraction(m-1, 2)
        assert means[1] == (Fraction(3, 2) if m == 2 else Fraction(m, 2))
        assert means[2] == Fraction(m, 2)
    print(f'PASS one-feature formulas and expectations, all labels for m=2..{max_m}', flush=True)


def check_hashes(path):
    for line in Path(path).read_text().splitlines():
        expected, filename = line.split('  ', 1)
        got = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
        assert got == expected, filename
    print('PASS artifact SHA-256 manifest', flush=True)


def check_closures():
    """Verify static finite closed-set upper-bound certificates, not the BFS."""
    results = {}
    for path in sorted(Path('certificates').glob('closure_*.json.gz')):
        start = time.perf_counter()
        with gzip.open(path, 'rt') as stream:
            data = json.load(stream)
        m, p = data['m'], data['p']
        labels = [1]*p + [-1]*(m-p)
        states = {int(x, 16) for x in data['states']}
        assert len(states) == len(data['states']) and 0 in states
        depths = dict(zip([int(x, 16) for x in data['states']], data['depths']))
        assert len(data['depths']) == len(states) and depths[0] == 0
        assert all(isinstance(d, int) and d >= 0 for d in depths.values())
        curve = [0] * (max(depths.values())+1)
        domain = range(1 << m)
        upper = [sum(1 << b for b in domain if a != b and (a & b) == a) for a in domain]
        generators = set()
        for order in itertools.permutations(range(m)):
            if order[0] > order[-1]:
                continue
            errors = errors_direct(labels, [order], data['mode'], data['constants'])
            masks = {sum(1 << i for i in a) for a in errors}
            f = sum(1 << a for a in masks)
            u = 0
            for a in masks:
                u |= upper[a]
            # Keep raw error families, including their dominated members.
            generators.add((f, u))
        maximum = 0
        for state in states:
            assert state >= 0 and state >> (1 << m) == 0
            u = 0
            remaining = state
            while remaining:
                bit = remaining & -remaining
                u |= upper[bit.bit_length()-1]
                remaining -= bit
            assert state & u == 0  # Every listed family is an antichain.
            maximum = max(maximum, state.bit_count())
            curve[depths[state]] = max(curve[depths[state]], state.bit_count())
            for f, uf in generators:
                target = (state | f) & ~(u | uf)
                assert target in states, (path, state, f)
                assert depths[target] <= depths[state] + 1, (path, 'depth', state, target)
        for d in range(1, len(curve)):
            curve[d] = max(curve[d], curve[d-1])
        assert curve == data['curve']
        results[str(path)] = data
        assert maximum == data['maximum']
        print(json.dumps({'closure': path.name, 'maximum': maximum, 'states': len(states),
                          'raw_generators': len(generators), 'seconds': round(time.perf_counter()-start, 6),
                          'status': 'PASS'}), flush=True)
    witnesses = {w['id']: w for w in json.loads(Path('certificates/witnesses.json').read_text())}
    for row in json.loads(Path('certificates/global-curves.json').read_text()):
        records = [results[path] for path in row['certificates']]
        m = row['m']
        assert {r['p'] for r in records} == set(range(m//2+1))
        assert len(records) == m//2+1
        for r in records:
            assert r['m'] == m
            assert ('constants' if r['constants'] else r['mode']) == row['kind']
        expected = [max(r['curve'][min(d, len(r['curve'])-1)] for r in records)
                    for d in range(max(len(r['curve']) for r in records))]
        assert row['curve'] == expected
        assert len(row['witness_ids']) == len(expected)-1
        for d, wid in enumerate(row['witness_ids'], 1):
            w = witnesses[wid]
            assert w['m'] == m and w['d'] == d and w['count'] == expected[d]
            check_witness(w)
        print(json.dumps({'global_curve': row['kind'], 'm': m, 'counts_by_d_including_zero': expected,
                          'status': 'PASS'}), flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--witnesses', default='certificates/witnesses.json')
    p.add_argument('--exclusions', action='store_true')
    p.add_argument('--ids', nargs='*')
    p.add_argument('--formulas', action='store_true')
    p.add_argument('--hashes', action='store_true')
    p.add_argument('--closures', action='store_true')
    a = p.parse_args()
    if a.hashes:
        check_hashes('certificates/SHA256SUMS')
    check_all_witnesses(a.witnesses)
    if a.formulas:
        check_one_feature()
    if a.exclusions:
        check_exclusions('certificates/exclusions.json', a.ids)
    if a.closures:
        check_closures()


if __name__ == '__main__':
    main()
