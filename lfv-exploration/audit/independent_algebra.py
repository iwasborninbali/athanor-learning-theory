"""Fresh exact arithmetic checks of the supplied regular examples and failure case."""
import json
from fractions import Fraction as Q
from pathlib import Path


def grounded_solution(adj, z):
    vertices = [v for v in range(len(adj)) if v != z]
    a = [[Q(len(adj[v]) if v == w else -int(w in adj[v])) for w in vertices]
         + [Q(1)] for v in vertices]
    for col in range(len(vertices)):
        pivot = next(i for i in range(col, len(vertices)) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [x / divisor for x in a[col]]
        for row in range(len(vertices)):
            if row != col:
                divisor = a[row][col]
                a[row] = [x - divisor * y for x, y in zip(a[row], a[col])]
    h = [Q(0)] * len(adj)
    for i, v in enumerate(vertices):
        h[v] = a[i][-1]
    return h


def energy(adj, c):
    return sum((c[u] - c[v]) ** 2 for u in range(len(adj)) for v in adj[u] if u < v)


def replay(adj, trajectory, regular):
    c = [0] * len(adj)
    c[trajectory[0]] = 1
    slack = 0
    rows = []
    for t, u in enumerate(trajectory):
        e, s, b = energy(adj, c), sum(c), sum(c[v] for v in adj[u])
        if regular:
            d = len(adj[0])
            assert e - d * s + 2 * b == -2 * slack
        rows.append(dict(t=t, position=u, counts=c.copy(), E=e, S=s, B=b))
        if t + 1 == len(trajectory):
            break
        v = trajectory[t + 1]
        assert not all(c)
        assert v in adj[u] and c[v] == min(c[w] for w in adj[u])
        slack += sum(c[w] for w in adj[u]) - len(adj[u]) * c[v]
        c[v] += 1
    return rows


cases = json.loads(Path('../b04-lfv/regular_certificates.json').read_text())['cases']
results = []
for case in cases:
    adj = case['adjacency']
    assert all(len(set(neighbors)) == 3 and u not in neighbors
               and all(u in adj[v] for v in neighbors) for u, neighbors in enumerate(adj))
    walk = replay(adj, case['path'], True)
    assert all(walk[-1]['counts'])
    assert len(walk) - 1 == case['first_cover']
    result = dict(name=case['name'], n=len(adj), T=len(walk) - 1, identity=True)
    if 'poisson' in case:
        p = case['poisson']
        sums = []
        for z in range(len(adj)):
            h = grounded_solution(adj, z)
            assert h[z] == 0
            if z == p['z']:
                assert h == list(map(Q, p['h']))
                assert sum(h) == Q(p['K'])
            sums.append(sum(h))
        assert min(sums) == max(sums)
        bound = 3 * max(sums)
        assert int(bound) == p['first_cover_bound']
        result.update(K=str(max(sums)), bound=int(bound), all_pins_solved=True)
    results.append(result)

claw = [[1, 2, 3], [0], [0], [0]]
failure = replay(claw, [0, 1, 0, 2, 0], False)
assert failure[-1]['E'] == 17 and 3 * failure[-1]['S'] == 15
report = dict(regular_examples=results, irregular_counterexample=failure)
Path('independent_algebra.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
