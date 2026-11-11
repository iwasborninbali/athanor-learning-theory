"""Free primary-source acquisition; all writes stay under sources/."""
from pathlib import Path
import json, urllib.request, datetime, shutil

OUT = Path(__file__).resolve().parent / 'sources'
OUT.mkdir(exist_ok=True)
SCOUT = Path('../../stalled-scout/ml/sources')
for name in ('lfv2017.txt', 'lfv2019chapter_full.txt',
             'original_Challenge_Problem_Analyzing_Ant_Robot_Coverage_Sven_Koenig.txt',
             'search_lfv_final_gap.txt', 'lfv2026_author_work_web.txt'):
    shutil.copyfile(SCOUT / name, OUT / name)
authors = json.loads((SCOUT / 'authors.json').read_text())
jobs = [
 ('paper2017.pdf', 'https://www.ibr.cs.tu-bs.de/users/fekete/hp/publications/PDF/2017-Lower_bounds_for_graph_exploration.pdf'),
 ('hop_thesis2021.pdf', 'https://repository.tudelft.nl/file/File_19d5694e-6b38-40fb-a724-8c01df51b293?preview=1'),
]
for aid, a in authors.items():
    if 'lfv' in a['candidates']:
        jobs.append(('author_' + aid.rsplit('/', 1)[-1] + '.json',
                     'https://api.openalex.org/works?filter=author.id:' +
                     aid.rsplit('/', 1)[-1] + ',from_publication_date:2017-01-01&per-page=200&sort=publication_date:desc'))
with (OUT / 'access.jsonl').open('a') as log:
    for name, url in jobs:
        record = dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(), url=url, file=name)
        try:
            data = urllib.request.urlopen(url, timeout=15).read()
            (OUT / name).write_bytes(data)
            record['bytes'] = len(data)
            if name.endswith('.json'):
                o = json.loads(data)
                print(name, o.get('meta', {}).get('count'),
                      [x['title'] for x in o.get('results', []) if any(w in x['title'].lower() for w in ('explor','patrol','triang','coverage','local polic'))], flush=True)
            else:
                print(name, len(data), flush=True)
        except Exception as exc:
            record['error'] = repr(exc)
            print(name, repr(exc), flush=True)
        log.write(json.dumps(record) + '\n'); log.flush()
