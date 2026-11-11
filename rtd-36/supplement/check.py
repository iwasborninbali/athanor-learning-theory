#!/usr/bin/env python3
"""Independent certificate checker (Python standard library only).

No solver or search module is imported. CNF verification reconstructs the
mathematical constraints. Every added proof clause must be RUP (the stronger
DRUP subset of DRAT); RAT-only steps are deliberately rejected. Witnesses
are checked by the literal recursive teaching definition.
"""
import argparse
from collections import Counter, defaultdict
import gzip
from itertools import combinations, product
import json
from pathlib import Path
import time


def read_cnf(path):
    header = None
    clauses = []
    pending = []
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path,'rt') as f:
        for line in f:
            if not line.strip() or line.startswith('c'):
                continue
            if line.startswith('p '):
                assert header is None
                p, kind, nv, nc = line.split()
                assert kind == 'cnf'
                header = int(nv), int(nc)
                continue
            for token in line.split():
                x = int(token)
                if x:
                    assert header is not None and abs(x) <= header[0]
                    pending.append(x)
                else:
                    assert len(set(pending)) == len(pending), 'Duplicate literal in input clause'
                    assert not any(-x in pending for x in pending), 'Tautological input clause'
                    clauses.append(tuple(pending))
                    pending = []
    assert not pending and header is not None
    assert len(clauses) == header[1]
    return header[0], clauses


def check_encoding(path, n, y, variant=None):
    """Exact multiset comparison; extra restricting clauses are not allowed."""
    nv, cs = read_cnf(path)
    universe = list(product((0, 1), repeat=n))
    # The search uses least-significant-bit coordinate numbering.
    labels = {tuple(reversed(bits)): i + 1 for i, bits in enumerate(universe)}
    triples = list(combinations(range(n), 3))
    base_nv = len(universe) + 8 * len(triples)
    if variant is None:
        assert nv == base_nv
    else:
        assert variant['n'] == n and variant['y'] == y and variant['zero'] is True
    remaining = Counter(tuple(sorted(c)) for c in cs)

    def require(c):
        key = tuple(sorted(c))
        assert remaining[key] > 0, ('Missing required encoding clause', c)
        remaining[key] -= 1
        if not remaining[key]:
            del remaining[key]

    require([labels[(0,) * n]])
    for coords in combinations(range(n), 2):
        for bits, label in labels.items():
            other_labels = [other for word, other in labels.items()
                            if word != bits and all(word[i] == bits[i] for i in coords)]
            require([-label] + other_labels)
    for ti, coords in enumerate(triples):
        pattern_labels = {}
        for pattern in product((0, 1), repeat=3):
            index = pattern[0] + 2 * pattern[1] + 4 * pattern[2]
            pattern_labels[pattern] = len(universe) + 8 * ti + index + 1
        for bits, label in labels.items():
            require([-label, pattern_labels[tuple(bits[i] for i in coords)]])
        for too_many in combinations(pattern_labels.values(), y + 1):
            require([-i for i in too_many])
        if variant is not None and variant['exact']:
            for pattern, pl in pattern_labels.items():
                matching = [lab for word, lab in labels.items()
                            if tuple(word[i] for i in coords) == pattern]
                require([-pl] + matching)
    if variant is not None:
        allocated = base_nv
        for tr in variant['transformations']:
            permutation = tr['permutation']
            shift = tr['xor']
            assert sorted(permutation) == list(range(n))
            assert 0 <= shift < 2 ** n
            compared = []
            for bits, lab in labels.items():
                transformed = tuple(bits[permutation[j]] ^ ((shift >> j) & 1)
                                    for j in range(n))
                if transformed != bits:
                    compared.append((lab, labels[transformed]))
            compared.sort()
            prev = []
            for position, (left, right) in enumerate(compared):
                require(prev + [left, -right])
                if position + 1 < len(compared):
                    allocated += 1
                    require(prev + [-left, -right, allocated])
                    require(prev + [left, right, allocated])
                    if variant.get('full_prefix',False):
                        if prev:
                            require([-allocated,-prev[0]])
                        require([-allocated,-left,right])
                        require([-allocated,left,-right])
                    prev = [-allocated]
        assert nv == allocated
    assert not remaining, ('Extra or repeated encoding clauses', len(remaining))
    return nv, cs


class RUPDatabase:
    """Two watched literals, fully rebuilt assignments on each RUP query."""
    def __init__(self, nv, initial):
        self.nv = nv
        self.clauses = []
        self.keys = defaultdict(list)
        self.watched = defaultdict(list)
        self.units = set()
        self.empty = set()
        for c in initial:
            self.add(c)

    def add(self, raw):
        c = list(dict.fromkeys(raw))
        assert all(0 < abs(x) <= self.nv for x in c), 'Out of range proof literal'
        cid = len(self.clauses)
        self.clauses.append(c)
        self.keys[tuple(sorted(c))].append(cid)
        if not c:
            self.empty.add(cid)
        elif len(c) == 1:
            self.units.add(cid)
        else:
            self.watched[c[0]].append(cid)
            self.watched[c[1]].append(cid)

    def delete(self, raw):
        key = tuple(sorted(set(raw)))
        ids = self.keys.get(key)
        if not ids:
            # DRAT deletions of absent clauses have no semantic effect.
            return False
        cid = ids.pop()
        if not ids:
            del self.keys[key]
        self.units.discard(cid)
        self.empty.discard(cid)
        self.clauses[cid] = None
        return True

    def rup(self, clause):
        if self.empty:
            return True
        values = bytearray(self.nv + 1)  # 0 unset, 1 true, 2 false
        queue = []

        def assign(lit):
            v = abs(lit)
            wanted = 1 if lit > 0 else 2
            if values[v]:
                return values[v] == wanted
            values[v] = wanted
            queue.append(lit)
            return True

        def val(lit):
            a = values[abs(lit)]
            if not a:
                return 0
            return a if lit > 0 else 3 - a

        for lit in clause:
            assert 0 < abs(lit) <= self.nv
            if not assign(-lit):
                return True
        for cid in self.units:
            if not assign(self.clauses[cid][0]):
                return True
        head = 0
        while head < len(queue):
            false_lit = -queue[head]
            head += 1
            watching = self.watched[false_lit]
            i = 0
            while i < len(watching):
                cid = watching[i]
                c = self.clauses[cid]
                if c is None:
                    watching[i] = watching[-1]
                    watching.pop()
                    continue
                if c[0] != false_lit:
                    assert c[1] == false_lit, 'Broken watched-literal invariant'
                    c[0], c[1] = c[1], c[0]
                other = c[1]
                if val(other) == 1:
                    i += 1
                    continue
                for j in range(2, len(c)):
                    if val(c[j]) != 2:
                        c[0], c[j] = c[j], c[0]
                        self.watched[c[0]].append(cid)
                        watching[i] = watching[-1]
                        watching.pop()
                        break
                else:
                    if val(other) == 2:
                        return True
                    assert assign(other)
                    i += 1
        return False


def check_proof(nv, initial, path, heartbeat=30):
    db = RUPDatabase(nv, initial)
    added = deleted = absent_deletions = 0
    empty_derived = False
    last = time.monotonic()
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            words = line.split()
            if not words or words[0] == 'c':
                continue
            is_delete = words[0] == 'd'
            if is_delete:
                words = words[1:]
            ints = [int(x) for x in words]
            assert ints and ints[-1] == 0 and 0 not in ints[:-1], ('Bad DRUP syntax', lineno)
            c = ints[:-1]
            if is_delete:
                deleted += 1
                absent_deletions += not db.delete(c)
            else:
                assert db.rup(c), ('Non-RUP proof step', lineno, c)
                db.add(c)
                added += 1
                if not c:
                    empty_derived = True
            if time.monotonic() - last > heartbeat:
                print(json.dumps({'checking':str(path), 'line':lineno, 'additions':added}), flush=True)
                last = time.monotonic()
    assert empty_derived, 'Proof does not derive the empty clause'
    return dict(additions=added, deletions=deleted,
                absent_deletions=absent_deletions, empty_clause_verified=True)


def check_hinted(nv, initial, path, heartbeat=30):
    """Check explicit unit-resolution reasons; no propagation search needed.

    The hint producer is untrusted. Each active reason clause must be unit
    under the current assignment, or be the final falsified clause.
    """
    db = {i+1:c for i,c in enumerate(initial)}
    next_id = len(initial) + 1
    additions = deletions = hints_total = 0
    empty_derived = False
    last = time.monotonic()
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as f:
        for lineno,line in enumerate(f,1):
            tokens = line.split()
            if not tokens or tokens[0] == 'c':
                continue
            if tokens[0] == 'd':
                assert len(tokens)==3 and tokens[2]=='0'
                cid = int(tokens[1])
                assert cid in db, ('Deleting inactive clause',lineno,cid)
                del db[cid]
                deletions += 1
                continue
            assert tokens[0]=='a', ('Invalid hinted record',lineno)
            values = [int(x) for x in tokens[1:]]
            cid = values[0]
            assert cid >= next_id, ('Nonmonotone or repeated fresh clause id',lineno)
            next_id = cid + 1
            split = values.index(0)
            assert values[-1]==0 and 0 not in values[split+1:-1]
            clause = tuple(values[1:split])
            hints = values[split+1:-1]
            assert all(0 < abs(lit) <= nv for lit in clause)
            assignment = {}
            conflict = False
            for lit in clause:
                var = abs(lit)
                want = lit < 0  # assume the negation of each target literal
                if var in assignment and assignment[var] != want:
                    conflict = True
                assignment[var] = want
            if conflict:
                assert not hints, ('Tautology must use no hints',lineno)
            for hi,hint in enumerate(hints):
                assert not conflict, ('Hints after conflict',lineno)
                assert hint in db, ('Inactive or unknown reason',lineno,hint)
                unknown = set()
                satisfied = False
                for lit in db[hint]:
                    var = abs(lit)
                    if var not in assignment:
                        unknown.add(lit)
                    elif assignment[var] == (lit>0):
                        satisfied = True
                        break
                assert not satisfied, ('Satisfied reason is not a unit step',lineno,hint)
                assert len(unknown)<=1, ('Reason is not unit',lineno,hint)
                if unknown:
                    lit = next(iter(unknown))
                    assignment[abs(lit)] = lit>0
                else:
                    conflict = True
                    assert hi+1==len(hints)
            assert conflict, ('No unit-resolution conflict',lineno)
            db[cid] = clause
            additions += 1
            hints_total += len(hints)
            if not clause:
                empty_derived = True
            if time.monotonic()-last > heartbeat:
                print(json.dumps({'checking_hinted':str(path),'line':lineno,'additions':additions}),flush=True)
                last = time.monotonic()
    assert empty_derived, 'No empty clause derived'
    return dict(additions=additions,deletions=deletions,unit_resolution_hints=hints_total,
                empty_clause_verified=True)


def check_cut_encoding(path, m, minimum, pinned, graph=False):
    """Validate a sound fixed-m overapproximation, allowing lazy triples."""
    assert 6 <= minimum <= m // 2
    universe = (1 << m) - 1
    # Construct bipartitions directly as subsets of the nonzero row labels.
    by_mask = {}
    for k in range(minimum, m-minimum+1):
        for ones in combinations(range(1,m),k):
            mask = sum(1 << r for r in ones)
            by_mask[mask] = ones
    pinned_mask = sum(1 << r for r in range(1,minimum+1))
    if graph:
        assert pinned, 'The graph reduction requires a pinned cut'
        allowed = {}
        for mask,ones in by_mask.items():
            counts = [(mask & pinned_mask).bit_count(),
                      (mask & (universe ^ pinned_mask)).bit_count(),
                      ((universe ^ mask) & pinned_mask).bit_count(),
                      ((universe ^ mask) & (universe ^ pinned_mask)).bit_count()]
            if 1 not in counts:
                allowed[mask] = ones
        by_mask = allowed
    cuts = sorted(by_mask)
    nv, cs = read_cnf(path)
    assert nv == len(cuts)
    positive = Counter()
    expected = Counter()
    for a,b in combinations(range(m),2):
        expected[tuple(i+1 for i,s in enumerate(cuts) if ((s >> a) ^ (s >> b)) & 1)] += 1
    if pinned:
        expected[(cuts.index(pinned_mask)+1,)] += 1
    forbidden_pairs = forbidden_triples = 0
    for c in cs:
        if all(lit>0 for lit in c):
            positive[tuple(sorted(c))] += 1
            continue
        assert len(c) in (2,3) and all(lit<0 for lit in c), 'Unsupported cut restriction'
        partitions = [universe]
        for lit in c:
            cut = cuts[-lit-1]
            pieces = []
            for cell in partitions:
                for side in (cut, universe ^ cut):
                    part = cell & side
                    if part:
                        pieces.append(part)
            partitions = pieces
        if len(c)==2:
            valid = any(cell.bit_count()==1 for cell in partitions)
            if not valid and graph:
                trace_size = sum(bool(cell & pinned_mask) + bool(cell & (universe ^ pinned_mask))
                                 for cell in partitions)
                valid = trace_size > 6
            assert valid, 'Unsound forbidden pair'
            forbidden_pairs += 1
        else:
            assert len(partitions)>6, 'Unsound forbidden triple'
            forbidden_triples += 1
    assert positive == expected, 'Incorrect row separation / normalization clauses'
    return nv, cs, dict(m=m,minimum_side=minimum,pinned=pinned,
                        graph_reduction=graph,
                        forbidden_pairs=forbidden_pairs,forbidden_triples=forbidden_triples)


def check_witness(path):
    d = json.loads(path.read_text())
    rows = d['rows']
    n = d['n']
    assert rows and all(len(r) == n and set(r) <= {'0', '1'} for r in rows)
    assert len(set(rows)) == len(rows)
    # Triple bounds below imply VC<=2, so larger projections are unnecessary
    # for exact VC computation, even for witnesses with many coordinates.
    assert d.get('max_triple_patterns',6) < 8
    counts = {str(k): max(len({tuple(r[i] for i in a) for r in rows})
                              for a in combinations(range(n), k)) for k in range(1, min(n,3) + 1)}
    vc = max([0] + [k for k in range(1, min(n,3) + 1) if counts[str(k)] == 2 ** k])
    assert n < 3 or counts['3'] <= d.get('max_triple_patterns', 6)
    current = rows[:]
    stages = []
    while current:
        dimensions = {}
        for r in current:
            for k in range(n + 1):
                found = False
                for a in combinations(range(n), k):
                    if all(s == r or any(s[i] != r[i] for i in a) for s in current):
                        dimensions[r] = k
                        found = True
                        break
                if found:
                    break
        m = min(dimensions.values())
        removed = [r for r in current if dimensions[r] == m]
        stages.append({'remaining':len(current), 'minimum_td':m, 'removed':removed})
        current = [r for r in current if r not in removed]
    rtd = max(s['minimum_td'] for s in stages)
    if 'expected_rtd' in d:
        assert rtd == d['expected_rtd']
    if 'expected_vc' in d:
        assert vc == d['expected_vc']
    return dict(n=n, size=len(rows), vc_dimension=vc, rtd=rtd,
                projection_maxima=counts, recursive_stages=stages)


def check_antipodal():
    """Exhaust the local trace implication used in the structural proof."""
    admissible = 0
    for mask in range(256):
        patterns = {p for p in range(8) if (mask >> p) & 1}
        if len(patterns) > 6 or {p ^ 7 for p in patterns} != patterns:
            continue
        admissible += 1
        for center in patterns:
            star = {center, center ^ 1, center ^ 2, center ^ 4}
            assert not star <= patterns
    assert admissible == 15
    lower = check_witness(Path(__file__).resolve().parent / 'certificates/antipodal_lower2.json')
    rows = set(lower['recursive_stages'][0]['removed'])
    assert {''.join('1' if bit == '0' else '0' for bit in r) for r in rows} == rows
    return dict(local_pattern_sets_checked=256,
                complement_closed_sets_of_size_at_most_6=admissible,
                forbidden_three_star_traces=0, lower_witness=lower)


def check_slice_counting():
    checked = []
    for sizes in product(range(1,6), repeat=4):
        if sum(sizes)<=5:
            singletons = sizes.count(1)
            assert singletons >= 3
            assert 4 + singletons >= 7
            checked.append(sizes)
    assert len(checked)==5
    return dict(positive_four_cell_distributions_total_at_most_5=len(checked),
                minimum_singletons=3, minimum_total_triple_patterns=7)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='mode', required=True)
    exc = sub.add_parser('exclude')
    exc.add_argument('--n', type=int, required=True)
    exc.add_argument('--y', type=int, default=6)
    exc.add_argument('--variant', type=Path)
    exc.add_argument('--hinted', action='store_true')
    exc.add_argument('cnf', type=Path)
    exc.add_argument('proof', type=Path)
    wit = sub.add_parser('witness')
    wit.add_argument('file', type=Path)
    sub.add_parser('antipodal')
    sub.add_parser('slice')
    cuts = sub.add_parser('cuts')
    cuts.add_argument('--m',type=int,required=True)
    cuts.add_argument('--minimum-side',type=int,default=6)
    cuts.add_argument('--pin',action='store_true')
    cuts.add_argument('--hinted',action='store_true')
    cuts.add_argument('--graph',action='store_true')
    cuts.add_argument('cnf',type=Path)
    cuts.add_argument('proof',type=Path)
    a = p.parse_args()
    t = time.monotonic()
    if a.mode == 'exclude':
        assert a.n >= 3 and 0 <= a.y <= 7
        variant = json.loads(a.variant.read_text()) if a.variant else None
        nv, cs = check_encoding(a.cnf, a.n, a.y, variant)
        result = (check_hinted if a.hinted else check_proof)(nv, cs, a.proof)
        result.update(n=a.n, y=a.y, encoding_verified=True,
                      variables=nv, input_clauses=len(cs))
    elif a.mode == 'witness':
        result = check_witness(a.file)
    elif a.mode == 'cuts':
        check_slice_counting()
        nv, cs, details = check_cut_encoding(a.cnf,a.m,a.minimum_side,a.pin,a.graph)
        result = (check_hinted if a.hinted else check_proof)(nv,cs,a.proof)
        result.update(details, encoding_verified=True,variables=nv,input_clauses=len(cs))
    elif a.mode == 'slice':
        result = check_slice_counting()
    else:
        result = check_antipodal()
    result['checker_seconds'] = time.monotonic() - t
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
