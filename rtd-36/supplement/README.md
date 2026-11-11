# Supplement: f(3,6) = 2 for recursive teaching dimension

All code uses the Python standard library only.

```sh
python3 verify_result.py          # checks the SHA-256 of the proof, the checkers and the certificates;
                                  # reruns the exhaustive local checks (check_structural.py);
                                  # computes the exact RTD of the six-row witness, of Warmuth's (3,7) class and of
                                  # the survey example (check.py)
cd independent-audit && python3 independent.py   # independent example calculations and exhaustive local trace checks
```

- `structural_proof.md` — the proof as written by the first agent (the manuscript's §2 is an edited version of it).
- `certificates/structural.json` — the exhaustive local cases (16, 3375 and 256 trace sets).
- `certificates/cell_lower2.json` — the six-row witness with RTD 2.
- `certificates/warmuth_known3.json` — Warmuth's class (control: RTD 3, seven patterns on a triple).
- `certificates/gupta_survey_audit.json` — the survey example recomputed: RTD 2.
- `independent-audit/` — written by a second agent that did not import or run the first agent's code.

The bounded SAT certificates mentioned in the manuscript (up to 8 coordinates; up to 13 concepts with the small-class reduction) and the associated encoding/reduction notes are not included. The SAT certificates are available on request. The full five-coordinate census program and logs are also not included. The retained --include-sat option in verify_result.py requires the optional n=8 CNF, specification and hinted proof, together with their SHA-256 entries; it cannot run from this bundle alone.
