"""Summaries of exact producer records; values audited separately by check.py."""
from pathlib import Path
import csv
import json

summary = []
for n in range(1,13):
    stats = json.loads(Path(f'exact_n{n}.log').read_text())
    classes = {}
    for line in Path(f'exact/n{n}.jsonl').read_text().splitlines():
        record = json.loads(line); degree = [0]*n; pos = 0; edges = 0
        for u in range(n):
            for v in range(u+1,n):
                if record['word'][pos] == '1':
                    degree[u] += 1; degree[v] += 1; edges += 1
                pos += 1
        kinds = ['all']
        if edges == n-1: kinds.append('trees')
        if edges == n: kinds.append('unicyclic')
        if min(degree) >= 2: kinds.append('minimum_degree_two')
        if min(degree) == max(degree) == 3: kinds.append('cubic')
        for kind in kinds:
            row = classes.setdefault(kind, dict(graphs=0, worst_time=0, worst_frequency=0))
            row['graphs'] += 1
            row['worst_time'] = max(row['worst_time'], max(record['times']))
            row['worst_frequency'] = max(row['worst_frequency'], max(record['frequencies']))
    summary.append(dict(n=n, classes=classes, execution=stats))
Path('summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with Path('table.csv').open('w') as stream:
    writer = csv.writer(stream)
    writer.writerow(['n','connected_simple_subcubic_graphs','worst_first_cover_moves','worst_frequency_before_cover','tree_worst_first_cover','cubic_graphs','cubic_worst_first_cover'])
    for row in summary:
        c = row['classes']; regular = c.get('cubic',{})
        writer.writerow([row['n'],c['all']['graphs'],c['all']['worst_time'],c['all']['worst_frequency'],
                         c['trees']['worst_time'],regular.get('graphs',''),regular.get('worst_time','')])
print(Path('table.csv').read_text())
