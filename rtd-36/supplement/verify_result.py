#!/usr/bin/env python3
"""Verify the full structural certificate and exact lower witness, using stdlib.

Use --include-sat to additionally replay the optional n=8 bounded exclusion.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import check
import check_structural


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(1<<20),b''):
            h.update(data)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--include-sat',action='store_true')
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    os.chdir(root)
    manifest={}
    for line in Path('certificates/SHA256SUMS').read_text().splitlines():
        value,name=line.split('  ',1)
        manifest[name]=value
    required=['structural_proof.md','check_structural.py','check.py','verify_result.py',
              'certificates/structural.json','certificates/cell_lower2.json',
              'certificates/warmuth_known3.json','certificates/gupta_survey_audit.json']
    if a.include_sat:
        required += ['certificates/n8-swaps-y6.cnf.gz','certificates/n8-swaps-y6.spec.json',
                     'certificates/n8-swaps-y6.trim.rup.gz']
    for name in required:
        assert name in manifest, ('Missing hash',name)
        assert digest(Path(name))==manifest[name], ('SHA-256 mismatch',name)
    supplied=json.loads(Path('certificates/structural.json').read_text())
    assert supplied==check_structural.certificate()
    lower=check.check_witness(Path('certificates/cell_lower2.json'))
    assert (lower['rtd'],lower['vc_dimension'],lower['projection_maxima']['3'])==(2,2,6)
    assert len(lower['recursive_stages'])==1 and len(lower['recursive_stages'][0]['removed'])==6
    warmuth=check.check_witness(Path('certificates/warmuth_known3.json'))
    assert (warmuth['rtd'],warmuth['vc_dimension'],warmuth['projection_maxima']['3'])==(3,2,7)
    survey=check.check_witness(Path('certificates/gupta_survey_audit.json'))
    assert (survey['rtd'],survey['projection_maxima']['3'])==(2,6)
    result={'structural_local_lemmas_verified':True,
            'vc1_cases':len(supplied['vc1_proper_fiber_cases']),
            'minimum_cell_cases':len(supplied['minimal_shattered_cell_cases']),
            'descent_cases':len(supplied['new_descent_cases']),
            'known_false_seven_pattern_control_verified':True,
            'exact_lower_witness':lower,
            'warmuth_control_rtd':warmuth['rtd'],
            'survey_matrix_rtd':survey['rtd'],
            'sha256_files_checked':len(required)}
    if a.include_sat:
        spec=json.loads(Path('certificates/n8-swaps-y6.spec.json').read_text())
        nv,clauses=check.check_encoding(Path('certificates/n8-swaps-y6.cnf.gz'),8,6,spec)
        result['optional_n8_sat_certificate']=check.check_hinted(
            nv,clauses,Path('certificates/n8-swaps-y6.trim.rup.gz'))
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':
    main()
