"""Independent, standard-library checker for the regular-graph certificates.

Checks every explicit walk, exact Poisson equations and graph symmetries;
also checks the local energy identity as a polynomial in arbitrary counters.
Optional --exhaustive independently audits energy on every reachable state of
every cubic graph in the supplied small-graph catalogue.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
import argparse
import itertools
import json
from pathlib import Path
import time


def validate_graph(a):
    n = len(a); d = len(a[0])
    assert n > 1 and d > 0
    assert all(len(x) == d and len(set(x)) == d for x in a)
    for v in range(n):
        assert v not in a[v] and all(0 <= w < n and v in a[w] for w in a[v])
    seen, queue = {0}, deque([0])
    while queue:
        for w in a[queue.popleft()]:
            if w not in seen:
                seen.add(w); queue.append(w)
    assert len(seen) == n
    return d


def polynomial_identity(a):
    """Delta(E-dS+2B)+2q=0 coefficient by coefficient, for every edge."""
    d = validate_graph(a); n = len(a)
    for u in range(n):
        for v in a[u]:
            # Coefficients of c(0),...,c(n-1),constant.
            coefficients = [0]*(n+1)
            coefficients[v] += 2*d
            for w in a[v]: coefficients[w] -= 2
            coefficients[-1] += d                 # delta E
            coefficients[-1] -= d                 # -d delta S
            for w in a[v]: coefficients[w] += 2
            for w in a[u]: coefficients[w] -= 2    # 2 delta B
            for w in a[u]: coefficients[w] += 2
            coefficients[v] -= 2*d                # 2q
            assert not any(coefficients)


def energy(a, c):
    return sum((c[v]-c[w])**2 for v in range(len(a)) for w in a[v] if v < w)


def check_case(o):
    a = o['adjacency']; n = len(a); k = o['k']; assert n == 2*k
    d = validate_graph(a); assert d == 3
    polynomial_identity(a)
    # Combinatorial triangulation certificate: each edge has two incident
    # triangular faces and its face adjacency is precisely the supplied graph.
    faces = o['triangles']; assert len(faces) == n
    incidence = defaultdict(list)
    for i, tri in enumerate(faces):
        assert len(tri) == len(set(tri)) == 3
        for edge in itertools.combinations(tri, 2):
            incidence[tuple(sorted(edge))].append(i)
    dual = [set() for _ in faces]
    for incident in incidence.values():
        assert len(incident) == 2
        u, v = incident; dual[u].add(v); dual[v].add(u)
    assert all(set(a[v]) == dual[v] for v in range(n))
    assert len(set(itertools.chain.from_iterable(faces))) - len(incidence) + n == 2
    # The explicit bipyramid form establishes a sphere, not just its Euler
    # characteristic. Verify that form as well.
    assert faces == [[k,i,(i+1)%k] for i in range(k)] + [[k+1,(i+1)%k,i] for i in range(k)]
    diameter = 0
    for start in range(n):
        dist = {start: 0}; queue = deque([start])
        while queue:
            v = queue.popleft()
            for w in a[v]:
                if w not in dist:
                    dist[w] = dist[v]+1; queue.append(w)
        diameter = max(diameter, max(dist.values()))
    assert diameter == k//2+1
    assert o['universal_first_cover_bound'] == d*diameter*(n-1)**2
    c = [0]*n; position = o['root']; c[position] = 1; slack_sum = 0
    assert o['path'][0] == position
    peak = 0
    for step, following in enumerate(o['path'][1:]):
        assert 0 in c
        peak = max(peak, max(c))
        assert following in a[position] and c[following] == min(c[w] for w in a[position])
        q = sum(c[w] for w in a[position])-d*c[following]; assert q >= 0
        slack_sum += q
        c[following] += 1; position = following
        assert energy(a,c)-d*sum(c)+2*sum(c[w] for w in a[position])+2*slack_sum == 0
    assert min(c) > 0 and len(o['path'])-1 == o['first_cover'] <= o['universal_first_cover_bound']
    poisson_bound = None
    if 'poisson' in o:
        p = o['poisson']; z = p['z']; h = list(map(F,p['h'])); assert len(h) == n and h[z] == 0
        assert sum(h) == F(p['K'])
        for v in range(n):
            if v != z:
                assert d*h[v]-sum(h[w] for w in a[v]) == 1
        # Explicit automorphisms take 0 to every possible last unvisited
        # vertex, making this one grounded solution a certificate for all z.
        assert z == 0
        for shift in range(k):
            for flip in range(2):
                permutation = [((v//k)^flip)*k+(v%k+shift)%k for v in range(n)]
                assert len(set(permutation)) == n
                assert all({permutation[w] for w in a[v]} == set(a[permutation[v]]) for v in range(n))
        poisson_bound = (d*sum(h)).numerator//(d*sum(h)).denominator
        assert poisson_bound == p['first_cover_bound'] and o['first_cover'] <= poisson_bound
    return dict(case=o['name'], n=n, diameter=diameter, T=o['first_cover'], M=peak,
                universal_bound=o['universal_first_cover_bound'], poisson_bound=poisson_bound)


def cubic_graphs(max_n, folder):
    for n in range(4,max_n+1,2):
        for word in (folder/f'n{n}.txt').read_text().splitlines():
            a = [[] for _ in range(n)]; p = 0
            for i in range(n):
                for j in range(i+1,n):
                    if word[p]=='1': a[i].append(j); a[j].append(i)
                    p += 1
            if all(len(x)==3 for x in a):
                yield n, a


def exhaustive_energy(max_n, folder):
    started = time.monotonic(); graphs = 0; states = 0
    for n,a in cubic_graphs(max_n,folder):
        polynomial_identity(a)
        layer = {(root, tuple(int(v==root) for v in range(n))) for root in range(n)}
        while layer:
            following = set()
            for v,c in layer:
                assert energy(a,c) <= 3*sum(c)-2*sum(c[w] for w in a[v])
                states += 1
                if 0 not in c: continue
                least = min(c[w] for w in a[v])
                for w in a[v]:
                    if c[w]==least:
                        updated = c[:w]+(c[w]+1,)+c[w+1:]
                        following.add((w,updated))
            layer = following
        graphs += 1
    print(json.dumps(dict(check='all_cubic_reachable_energy', graphs=graphs,
                          states=states, max_n=max_n, seconds=time.monotonic()-started)),flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,default=Path('regular_certificates.json'))
    p.add_argument('--catalog',type=Path,default=Path('catalog'))
    p.add_argument('--max-n',type=int,default=12)
    p.add_argument('--exhaustive',action='store_true')
    args=p.parse_args()
    certificate=json.loads(args.certificate.read_text())
    assert certificate['schema']=='lfv_regular_bound_certificate_v1'
    for case in certificate['cases']:
        print(json.dumps(check_case(case)),flush=True)
    if args.exhaustive:
        exhaustive_energy(args.max_n,args.catalog)
