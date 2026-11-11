"""Independent exact teaching calculations and local implication audits.

No imports from the claimed proof's directory. Integers encode binary rows;
coordinate 0 is the rightmost printed bit. All teaching sets are enumerated.
"""
import itertools as it
import json
from pathlib import Path


def projections(rows, coords):
    return {tuple((r >> i) & 1 for i in coords) for r in rows}


def is_xy(rows, n, x=3, y=6):
    return all(len(projections(rows, a)) <= y
               for k in range(min(x, n) + 1)
               for a in it.combinations(range(n), k))


def td(rows, row, n):
    for k in range(n + 1):
        for a in it.combinations(range(n), k):
            mask = sum(1 << i for i in a)
            if all(other == row or (row ^ other) & mask for other in rows):
                return k, list(a)
    raise AssertionError("duplicate or malformed rows")


def rtd(rows, n):
    remaining = set(rows)
    levels = []
    while remaining:
        teachings = {r: td(remaining, r, n) for r in remaining}
        minimum = min(t[0] for t in teachings.values())
        removed = sorted(r for r, t in teachings.items() if t[0] == minimum)
        levels.append({"minimum": minimum, "removed": [format(r, f"0{n}b") for r in removed],
                       "teaching_sets": {format(r, f"0{n}b"): teachings[r][1] for r in removed}})
        remaining.difference_update(removed)
    return {"rtd": max((l["minimum"] for l in levels), default=0), "levels": levels}


def audit(rows, n):
    return {"n": n, "rows": [format(r, f"0{n}b") for r in sorted(rows)],
            "vc": max((k for k in range(n + 1) for a in it.combinations(range(n), k)
                       if len(projections(rows, a)) == 2 ** k), default=0),
            "max_triple_patterns": max((len(projections(rows, a))
                                        for a in it.combinations(range(n), 3)), default=0),
            "is_3_6": is_xy(rows, n), "individual_td": [td(rows, r, n)[0] for r in sorted(rows)],
            **rtd(rows, n)}


def local_audits():
    # Exhaust all possible triple traces; bits 2,1,0 are u,v,w.
    descent = []
    split_violations = []
    for trace_bits in range(256):
        trace = [r for r in range(8) if trace_bits >> r & 1]
        cells = [{r & 1 for r in trace if r >> 1 == uv} for uv in range(4)]
        if not all(cells) or cells[0] != {0, 1}:
            continue
        if len(trace) <= 6:
            assert sum(len(cell) == 2 for cell in cells) <= 2
            assert not (cells[1] == cells[2] == {0, 1})
        # TD(c)>=3 requires a 1 in both adjacent cells.
        if 1 not in cells[1] or 1 not in cells[2]:
            continue
        if len(trace) <= 6:
            # Independently consider both choices of which adjacent cell is constant.
            choices = []
            for swap in (False, True):
                oriented = [((r & 1) | ((r & 2) << 1) | ((r & 4) >> 1))
                            if swap else r for r in trace]
                if {r & 1 for r in oriented if r >> 1 == 1} != {1}:
                    continue
                # Within u=0, w=0 there is just the A-minus-c trace 000.
                assert {r for r in oriented if (r & 5) == 0} == {0}
                uw = {(r >> 2, r & 1) for r in oriented}
                assert {(0, 0), (0, 1), (1, 1)} <= uw
                outcome = "smaller_shattered_cell" if (1, 0) in uw else "VC1_global_fiber"
                if outcome == "VC1_global_fiber":
                    assert {r for r in oriented if r & 1 == 0} == {0}
                choices.append({"swapped": swap, "outcome": outcome})
            assert choices
            descent.append({"trace": [format(r, "03b") for r in trace], "choices": choices})
        elif len(trace) == 7 and cells[1] == cells[2] == {0, 1}:
            split_violations.append([format(r, "03b") for r in trace])

    # Model the three outside cells' projections as arbitrary nonempty subsets.
    minimum_cell_cases = 0
    for masks in it.product(range(1, 16), repeat=3):
        p01, p10, p11 = masks
        if (p10 | p11).bit_count() > 2 or (p01 | p11).bit_count() > 2:
            continue
        outside = p01 | p10 | p11
        assert outside.bit_count() <= 3
        minimum_cell_cases += 1

    # Check the VC1 minimum-fiber step in every non-shattering pair trace.
    vc1_cases = 0
    for trace_bits in range(16):
        trace = [r for r in range(4) if trace_bits >> r & 1]
        if {r for r in trace if r >> 1 == 0} != {0, 1} or len(trace) == 4:
            continue
        for absent_outside_bit in (0, 1):
            if any(r >> 1 == 1 and (r & 1) == absent_outside_bit for r in trace):
                continue
            assert {r for r in trace if (r & 1) == absent_outside_bit} == {absent_outside_bit}
            vc1_cases += 1
    return {"minimum_cell_admissible": minimum_cell_cases,
            "vc1_implications": vc1_cases, "descent": descent,
            "seven_pattern_failed_split_controls": split_violations}


if __name__ == "__main__":
    # Transcribed afresh from the stated lower example and CCT Figure 2.
    examples = {
        "six_row_lower": audit([int(s, 2) for s in ("001", "010", "011", "100", "101", "110")], 3),
        "square": audit(list(range(4)), 2),
        "warmuth": audit([int(s, 2) for s in ("00011", "00110", "01100", "11000", "10001",
                                                     "01011", "10110", "01101", "11010", "10101")], 5),
        "gupta_survey": audit([int(s, 2) for s in ("00110", "01110", "10010", "11100",
                                                         "00111", "01111", "10100", "11010")], 5),
        "nonminimum_cell_control": audit([int(s, 2) for s in
                                           ("0000", "0001", "0010", "0011", "0100", "1000", "1100")], 4),
        "local_audits": local_audits(),
    }
    assert examples["six_row_lower"]["rtd"] == 2
    assert examples["warmuth"]["rtd"] == 3 and not examples["warmuth"]["is_3_6"]
    Path("independent-results.json").write_text(json.dumps(examples, indent=2) + "\n")
    print(json.dumps(examples, indent=2))
