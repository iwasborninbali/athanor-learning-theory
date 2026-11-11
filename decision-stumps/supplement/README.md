# Effective decision stumps: replay supplement

Prepared 11 November 2026. Python 3.10 or later; standard library only.
No downloads, installation, network access, search software, or paid calls are
needed. Run commands from the directory containing `check.py`, without Python's
`-O` option: the checker uses assertions.

## Main replay

```sh
python3 check.py --hashes --formulas --closures
python3 check.py --exclusions
```

The first command checks the bundle manifest, all 226 explicit datasets and their
full effective-error masks and named counts, every one-feature label word for
sample sizes 2 through 12, all 30 finite closure/depth certificates, and the
all-dimension maximum curves for sample sizes 4, 5, and 6. The sample-size-2 and
sample-size-3 rows follow analytically; the optional independent audit below also
regenerates them. The second command freshly enumerates all 64 fixed-dimension
targets, including the reported sample-size-7 and sample-size-8 upper bounds.
It evaluates raw predictions, retaining locally dominated errors, without
importing the research search code. Allow roughly ten minutes for the second
command on the research machine; other machines may differ.

For a shorter raw-enumeration check:

```sh
python3 check.py --exclusions --ids all_m6_d3 transition_m5_d2
```

`--ids` restricts only raw exclusions. Witnesses are checked on every invocation.
Run numerical checks sequentially. An exclusion target contains its parameters
and claimed maximum, not a trusted optimality proof: fresh enumeration establishes
its upper bound. Explicit witnesses establish the matching lower bounds.

## Contents and conventions

- `proofs.md`: the audited analytic proofs, with one corrected sentence in the
  proof of (10): on disagreeing coordinates, inclusion requires the label to
  match the competitor, rather than the candidate. The bound is unchanged.
- `check.py`: the original independent certificate checker, unchanged.
- `certificates/witnesses.json`: 226 datasets. Error-mask bit i is example i,
  numbered from zero; `count` counts distinct minimal masks; `named_count` counts
  every named stump with a minimal mask. The triples in the paper are A/T/C.
  `mode=all, constants=false` means A; `mode=transition, constants=false` means T;
  either gap mode with `constants=true` means C. Constants are shared, counted
  once each. Dominance means proper error-set inclusion.
- `certificates/closure_*.json.gz`: all 30 original closure certificates, kept in
  their supplied gzip format; the checker decompresses them in memory. Zip member
  sizes include these gzip files as stored, not their expanded in-memory JSON.
- `certificates/global-curves.json`: complete all-dimension rows for m=4,5,6.
- `certificates/exclusions.json`: all 64 original fixed-dimension targets.
- `certificates/completeness.md`: coverage, closure/depth reasoning and witness
  normalization. Its references to research builders describe the original run;
  those builders are unnecessary for replay and are omitted.
- `logs/`: original check logs and environment record. These document the research
  run; the commands above perform fresh checks.
- `audit/verify.md`: the independent audit of 11 November 2026, preserved verbatim.
  It confirmed the analytic results and rebuilt every all-dimension row through
  m=6, but did not repeat the large m=7,8 exclusions. Its historical relative
  paths and input hashes refer to the original research workspaces.
- `audit/independent_verify.py`, `independent-structure.json` and
  `independent-simulation.json`: independent code and original results. The sole
  code adaptation is replacing its original sibling-workspace certificate path
  by the bundled certificate directory resolved relative to the script. Original
  script SHA-256: `70906301dcb2f4398ec2ae50a38ad88ecf5b849a35ab35cc74350578e55de6aa`.
- `sources/` and `audit/sources/`: dated literature-search records and source
  provenance. Their file lists document the original source collections; full
  downloaded papers, HTML, and search-response archives are omitted. No
  mathematical certificate or fixed-dimension exclusion target is omitted.

## Optional independent regeneration

From the supplement root:

```sh
cd audit
python3 independent_verify.py structure
python3 independent_verify.py simulation
```

The first command rebuilds reachable upward-closed error families independently,
matches every closure state and shortest depth, checks all m=2,...,6 curves and
selected raw-permutation exclusions, and evaluates formulas and witnesses. The
second reruns the fixed-seed simulations. These commands overwrite the bundled
historical result JSON files in `audit/`; run them on a separate clean unzip if
the manifest is to remain valid afterward. Simulations are supporting checks,
not the proof of the expectation theorem. The audit script has a conservative
1,000 CPU-second limit per invocation.

`certificates/SHA256SUMS` is a manifest for this replay bundle, regenerated during
packaging rather than copied from the larger research workspace. It covers every
bundled file except itself. The main checker and mathematical certificates retain their
original bytes; the proof wording correction is disclosed above. The research searchers/builders and
full source-download archive are not required for any main replay command.
