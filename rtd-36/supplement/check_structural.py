#!/usr/bin/env python3
"""Independent finite verification of the structural proof's local lemmas.

Standard library only; no search code or SAT solver is imported. The
global minimality and hereditary arguments are written in structural_proof.md.
The certificate is a complete enumeration of the finite pattern cases,
not samples from concept classes of bounded dimension.
"""
import argparse
from itertools import product
import json
from pathlib import Path


def vc1_fiber_lemma():
    checked=[]
    # Patterns are (i,j), encoded i + 2*j. A split i-fiber has both j-values.
    for code in range(16):
        relation={p for p in range(4) if (code>>p)&1}
        if len(relation)==4:
            continue
        for b in (0,1):
            fiber={p for p in relation if (p&1)==b}
            if len(fiber)!=2:
                continue
            options=[]
            for q in (0,1):
                jfiber={p for p in relation if (p>>1)==q}
                if jfiber and jfiber < fiber:
                    options.append(q)
            assert options, ('VC1 proper-fiber lemma failed',relation,b)
            checked.append({'trace':sorted(relation),'i_value':b,'smaller_j_values':options})
    return checked


def minimal_shattered_cell_lemma():
    checked=[]
    # A=cell (u,v)=(0,0) is assumed to shatter a different pair (s,t).
    # The other three (u,v)-cells are nonempty. Their sets of (s,t)-patterns
    # are P01,P10,P11, each a nonempty subset of the four patterns.
    subsets=[{p for p in range(4) if (mask>>p)&1} for mask in range(1,16)]
    for p01,p10,p11 in product(subsets,repeat=3):
        # Since A has all four (s,t)-patterns, (u,s,t) and (v,s,t)
        # each having <=6 patterns imposes these two inequalities.
        if len(p10|p11)>2 or len(p01|p11)>2:
            continue
        outside=p01|p10|p11
        missing=set(range(4))-outside
        assert missing
        checked.append({'p01':sorted(p01),'p10':sorted(p10),'p11':sorted(p11),
                        'private_patterns':sorted(missing)})
    return checked


def descent_for_trace(trace):
    """New lemma, with pattern bits ordered (u,v,w), least significant first.

    Cell A has a unique w=1 row and at least one w=0 row. Absence of
    two-label teaching for that distinguished row requires patterns 5,6.
    """
    if not {0,4,5,6} <= trace:
        return None
    if {p&3 for p in trace} != set(range(4)):
        return None
    cases=[]
    for shared in (0,1):
        # shared=0: unsplit neighbor u=0,v=1, whose w=0 pattern is 2.
        # shared=1: unsplit neighbor u=1,v=0, whose w=0 pattern is 1.
        neighbor_zero = 2 if shared==0 else 1
        if neighbor_zero in trace:
            continue
        # The selected side (shared coordinate=0,w=0) lies entirely in A.
        small={p for p in trace if ((p>>shared)&1)==0 and (p>>2)==0}
        assert small == {0}
        projection={(((p>>shared)&1),(p>>2)) for p in trace}
        if len(projection)==4:
            conclusion='smaller_cell_of_shattered_pair'
        else:
            # Its three already present patterns are (0,0),(0,1),(1,1).
            assert projection == {(0,0),(0,1),(1,1)}
            assert {p for p in trace if (p>>2)==0} == {0}
            conclusion='w_zero_fiber_entirely_in_A'
        cases.append({'shared_coordinate':shared,'conclusion':conclusion})
    return cases


def new_descent_lemma():
    checked=[]
    for mask in range(256):
        trace={p for p in range(8) if (mask>>p)&1}
        if len(trace)>6:
            continue
        cases=descent_for_trace(trace)
        if cases is not None:
            assert cases, ('No descent in a <=6 trace',trace)
            checked.append({'trace':sorted(trace),'cases':cases})
    # A seven-pattern trace has both adjacent cells split: this proof
    # must fail there, consistently with the known (3,7) Warmuth example.
    false_control={0,1,2,4,5,6,7}
    assert descent_for_trace(false_control)==[]
    assert len(checked)==7
    return checked,sorted(false_control)


def certificate():
    vc1=vc1_fiber_lemma()
    minimum=minimal_shattered_cell_lemma()
    descent,control=new_descent_lemma()
    return {'format':'structural-local-enumeration-v1',
            'vc1_proper_fiber_cases':vc1,
            'minimal_shattered_cell_cases':minimum,
            'new_descent_cases':descent,
            'known_false_seven_pattern_control':control}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,default=Path('certificates/structural.json'))
    p.add_argument('--write',action='store_true')
    a=p.parse_args()
    computed=certificate()
    if a.write:
        a.certificate.write_text(json.dumps(computed,indent=2)+'\n')
    else:
        supplied=json.loads(a.certificate.read_text())
        assert supplied==computed, 'Certificate does not match the exhaustive enumeration'
    print(json.dumps({'verified':True,'vc1_cases':len(computed['vc1_proper_fiber_cases']),
                      'minimal_shattered_cell_cases':len(computed['minimal_shattered_cell_cases']),
                      'new_descent_cases':len(computed['new_descent_cases']),
                      'seven_pattern_control_fails_as_required':True}),flush=True)


if __name__=='__main__':
    main()
