"""Explicit cubic triangulation-dual examples and exact Poisson certificates."""
from collections import deque
from fractions import Fraction as F
import json
from pathlib import Path


def poisson(a, z):
    vertices = [v for v in range(len(a)) if v != z]
    matrix = [[F(len(a[v]) if v == w else -int(w in a[v])) for w in vertices] + [F(1)]
              for v in vertices]
    for i in range(len(vertices)):
        pivot = next(j for j in range(i, len(vertices)) if matrix[j][i])
        matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
        div = matrix[i][i]; matrix[i] = [x/div for x in matrix[i]]
        for j in range(len(vertices)):
            if j != i and matrix[j][i]:
                multiplier = matrix[j][i]
                matrix[j] = [x-multiplier*y for x, y in zip(matrix[j], matrix[i])]
    h = [F(0)]*len(a)
    for i, v in enumerate(vertices):
        h[v] = matrix[i][-1]
    return h


cases = []
for k in (3, 4, 5, 8, 12, 32, 64, 128):
    # Faces of the k-gonal bipyramid; their dual is C_k Cartesian-product K_2.
    faces = [[k, i, (i+1) % k] for i in range(k)] + [[k+1, (i+1) % k, i] for i in range(k)]
    a = [sorted({(v//k)*k+(v+1) % k, (v//k)*k+(v-1) % k, (v+k) % (2*k)})
         for v in range(2*k)]
    target = k-1
    dist = {target: 0}; queue = deque([target])
    while queue:
        for w in a[queue.popleft()]:
            if w not in dist:
                dist[w] = 1+min(dist[u] for u in a[w] if u in dist)
                queue.append(w)
    c = [0]*(2*k); v = 0; c[v] = 1; path = [v]
    while min(c) == 0:
        least = min(c[w] for w in a[v])
        v = max((w for w in a[v] if c[w] == least), key=lambda w: (dist[w], w))
        c[v] += 1; path.append(v)
        assert len(path) <= 3*(2*k-1)**3+1
    case = dict(name=f'bipyramid_dual_{k}', k=k, triangles=faces, adjacency=a,
                root=0, path=path, first_cover=len(path)-1,
                universal_first_cover_bound=3*(k//2+1)*(2*k-1)**2)
    if k <= 12:
        h = poisson(a, 0)
        case['poisson'] = dict(z=0, h=list(map(str, h)), K=str(sum(h)),
                               first_cover_bound=(3*sum(h)).numerator//(3*sum(h)).denominator)
    cases.append(case)

out = dict(schema='lfv_regular_bound_certificate_v1',
           statement='Every connected simple d-regular graph has T <= d*D*(n-1)^2 and M_before <= d*D*(n-1).',
           hypotheses=['zero counters before counted initial position', 'no self-loops',
                       'move to a minimum-counter neighbor', 'arbitrary history-dependent ties'],
           identity='E_t - d*S_t + 2*B_t + 2*sum(q_j for j<t) = 0',
           cases=cases)
Path('regular_certificates.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps([dict(name=x['name'], n=len(x['adjacency']), T=x['first_cover'],
                       poisson_bound=x.get('poisson', {}).get('first_cover_bound')) for x in cases]))
