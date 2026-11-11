"""Small exact state DP to estimate the full experiment; not the checker."""
import argparse, functools, json, time
from pathlib import Path
from generate_graphs import decode, canonical


def solve(adj, root):
    n = len(adj)
    neighbors = [[w for w in range(n) if adj[v] >> w & 1] for v in range(n)]
    @functools.lru_cache(None)
    def dp(v, counts):
        if min(counts):
            return 0
        least = min(counts[w] for w in neighbors[v])
        best = 0
        for w in neighbors[v]:
            if counts[w] == least:
                c = list(counts); c[w] += 1
                best = max(best, 1 + dp(w, tuple(c)))
        return best
    c = [0] * n; c[root] = 1
    value = dp(root, tuple(c))
    return value, dp.cache_info().currsize


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--max-n', type=int, default=7)
    args = ap.parse_args()
    for n in range(1, args.max_n + 1):
        t = time.monotonic(); states = 0; worst = -1; record = None; starts = 0
        for word in Path(f'catalog/n{n}.txt').read_text().splitlines():
            adj = decode(word, n); seen = set()
            for root in range(n):
                key = canonical(adj, root)
                if key in seen: continue
                seen.add(key); starts += 1
                value, size = solve(adj, root); states += size
                if value > worst:
                    worst = value; record = dict(word=word, root=root)
        print(json.dumps(dict(n=n, starts=starts, states=states, worst=worst,
                              witness=record, seconds=time.monotonic()-t)), flush=True)
