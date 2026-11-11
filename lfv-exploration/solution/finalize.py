"""Refuse to finalize unless the complete independent audits passed."""
import datetime
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

base = pathlib.Path(__file__).resolve().parent
records = [json.loads(line) for line in (base/'checked_exclusions.log').read_text().splitlines()]
completed = [r for r in records if r.get('check') == 'exclusion']
assert [r['n'] for r in completed] == list(range(1,13))
assert sum(r['states'] for r in completed) == 902816036
assert completed[-1]['worst_time'] == 90 and completed[-1]['worst_frequency'] == 22
catalogues = [json.loads(x) for x in (base/'checked_catalogues.log').read_text().splitlines()]
assert [r['n'] for r in catalogues] == list(range(1,13))
assert sum(r['graphs'] for r in catalogues) == 27525
witnesses = [json.loads(x) for x in (base/'checked_witnesses.log').read_text().splitlines()]
assert len(witnesses) == 24
regular = [json.loads(x) for x in (base/'checked_regular_exhaustive.log').read_text().splitlines()]
assert regular[-1]['check'] == 'all_cubic_reachable_energy'
assert regular[-1]['max_n'] == 12 and regular[-1]['graphs'] == 112
reference = [json.loads(x) for x in (base/'checked_reference.log').read_text().splitlines()]
assert [r['n'] for r in reference if r.get('check') == 'exclusion'] == list(range(1,9))

environment = dict(python=sys.version, platform=platform.platform(),
                   clang=subprocess.check_output(['clang++','--version'],text=True))
(base/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
files = []
for pattern in ('catalog/*.txt','exact/*.json','exact/*.jsonl','sources/*',
                '*.py','*.cpp','*.csv','summary.json','regular_certificates.json',
                'regular_bound.md','environment.json','exact_n*.log','checked_*.log',
                'pilot*.log','cpp_pilot.log','catalog_generation.log','regular_generation.log'):
    files.extend(p for p in base.glob(pattern) if p.is_file())
files = sorted(set(files))
hashes = {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(base/'SHA256SUMS').write_text(''.join(f'{digest}  {name}\n' for name,digest in hashes.items()))
manifest_hash = hashlib.sha256((base/'SHA256SUMS').read_bytes()).hexdigest()
key_files = ['regular_bound.md','regular_certificates.json','check_regular.py','check.py',
             'catalog/n12.txt','exact/n12.jsonl','exact/witness_n12.json',
             'exact/frequency_n12.json','checked_exclusions.log','checked_regular_exhaustive.log']
table = '| Certificate | SHA-256 |\n|---|---|\n'
table += ''.join(f'| [{name}]({name}) | `{hashes[name]}` |\n' for name in key_files)
table += f'\n[SHA256SUMS](SHA256SUMS) lists all {len(hashes)} immutable certificate/source files; its SHA-256 is `{manifest_hash}`.\n'
report = (base/'result.md').read_text()
report = report.replace('**Draft: the final n=12 forward exclusion audit is still running.**',
                        '**All independent audits passed.**')
old = ('Final hashes will be inserted after all audits finish. `SHA256SUMS` will list\n'
       'the complete immutable certificate corpus, including all catalogue, per-graph,\n'
       'witness, proof, checker, and audit-log files.')
assert old in report
report = report.replace(old,table)
seconds = sum(r['seconds'] for r in completed)
validation = (f'\nThe completed independent forward audit checked **{sum(r["states"] for r in completed):,}**\n'
              f'nonterminal graph states in {seconds:.1f} seconds across all orders;\n'
              f'the n=12 pass took {completed[-1]["seconds"]:.1f} seconds. Its largest\n'
              f'frontier layer contained {completed[-1]["largest_layer"]:,} states. The\n'
              f'separate energy audit checked {regular[-1]["states"]:,} reachable states\n'
              f'(including terminal states) on all 112 cubic graphs through n=12.\n'
              'The readable tuple-state reference checker also passed every graph\n'
              'through n=8. These are completed checks, not planned validation.\n')
report = report.replace('## Certificates and hashes\n',validation+'\n## Certificates and hashes\n')
(base/'result.md').write_text(report)
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (base/'progress.md').open('a') as stream:
    stream.write(f'\n{stamp}: complete. Proved the regular-graph polynomial bound; catalogue completeness, all n<=12 forward exclusions, all witnesses, tuple reference through n=8, and the complete small-cubic energy audit passed. Certificates and SHA-256 manifest finalized. General irregular subcubic gap remains open.\n')
print(json.dumps(dict(status='complete',files=len(hashes),manifest_sha256=manifest_hash,
                      finite_states=sum(r['states'] for r in completed),
                      energy_states=regular[-1]['states'])))
