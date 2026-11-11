# Finite-sample geodesic kernels: compact replay supplement

This accompanies a **partial** answer to Feragen–Hauberg's COLT 2016 open problem.
The independent audit's verdict is “holds as a conservative partial result.”
The proofs and empirical observations have different evidential status.

## Quick replay

Use Python 3 and NumPy. The original environment used Python 3.14.6 and NumPy
2.5.2; `data/environment.json` retains its detailed versions. No installation,
network access, SciPy, native libraries, or original experiment folder is needed
for the default replay. From the directory containing this README, run:

```sh
python3 checker.py --hashes
```

The checker recomputes:

- training PD 297/300 and conditional append-100 survival 0/297, with Wilson
  intervals, from per-repetition decision records;
- the headline C=1 accuracy, 94,081/118,800 = 79.1927609%, directly from all
  individual predictions and labels, with a repetition-level Student interval;
- validation-selected accuracies from all individual predictions, and their
  recorded full-test append counts;
- the displayed Gaussian classification table from per-repetition counts;
- transition brackets, observed grid reversals, and the descriptive square-root
  fit from every retained cohort's grid of signs;
- the 77/80 versus 31/80 versus 0/80 precision comparison, and agreement with
  the original full-interval decision records;
- the original reconstruction's Fig. 1 discrepancy mean and interval;
- the cap-packing series exactly as a rational number and the analytic Bayes rate.

The statistical and certificate-bound consistency helpers are taken verbatim
from the source `checker.py`. The compact entry point is an adaptation for the
size-limited paper supplement. It checks recorded pivot/error-bound consistency;
**reading a stored sign or endpoint is not fresh numerical certification**.
The default does not refit SVMs, recompute kernel signs, revalidate parameter
selection, or rerun the bootstrap. `data/reference.json` contains reference
outputs to compare against; it is not the sole input to the replay.

## Optional fresh SVM and input replay

The raw coordinates need not be stored: the exact original NumPy seed procedure
regenerates them. Every training/test array was compared element by element with
the source arrays during extraction. Per-repetition SHA-256 hashes of the raw
little-endian float64 arrays prevent a changed generator from silently changing
the numerical object. Generator replay requires compatible NumPy behavior;
a mismatch stops with an error.

```sh
python3 checker.py --hashes --refit-reps 0,30,60,90,120,150,180,210,240,270
python3 checker.py --refit-reps all
```

This uses the bundled original `svm.py`, reconstructs its C=1 warm-start sequence
through coefficient 2.5 using recorded training-PD eligibility, and requires all
400 headline predictions to match for each successful repetition. It does not
independently establish that the recorded eligibility signs are correct. Other
validation-selected models are aggregated, not refitted. Thread counts are set
to one before importing NumPy.

## Optional fresh directed-interval signs

`independent_interval.cpp` is the independent auditor's directed MPFR interval
Cholesky implementation. The original production code instead used interval LDL
and faster checked bounds. This source encloses the exact normalized directions
of the regenerated dyadic Gaussian inputs, with the exact binary64 coefficient
2.5. It includes norm and projection error. It requires a C++17 compiler and
MPFR/GMP development libraries already installed. No binary is bundled.

For example, on macOS with Homebrew libraries:

```sh
clang++ -O2 -std=c++17 -dynamiclib independent_interval.cpp -I/opt/homebrew/include -L/opt/homebrew/lib -lmpfr -lgmp -o independent_interval.dylib
python3 checker.py --certify-reps 0,110 --interval-library ./independent_interval.dylib
```

On Linux with libraries in the default search path:

```sh
c++ -O2 -std=c++17 -shared -fPIC independent_interval.cpp -lmpfr -lgmp -o independent_interval.so
python3 checker.py --certify-reps 0,110 --interval-library ./independent_interval.so
```

`--certify-reps all` recomputes all 300 training signs and, for each of the 297
successful training sets, the sign after appending the first 100 independent test
points. It can take tens of minutes. Each case tries 256, 512, then 1024 bits and
fails if it remains unresolved or disagrees. A negative pivot after previous
positive pivots establishes negative inertia; pivot bounds are not eigenvalue
bounds. This optional route provides fresh sign certification rather than
aggregation. It does not recertify the full uniform-sphere transition grids.

## Contents and provenance

- `theory.md`: complete original mathematical statements and proofs, with one
  packaging-only correction about source-PDF availability.
- `numerical-certification.md`: original numerical method and assumptions.
- `independent-audit.md`: complete independent audit, including the Jaquier
  predecessor and the unexplained original-figure discrepancy. Links to its
  original companion files describe the larger audit, whose full dataset and
  scripts are not all packaged here.
- `data/classification.json`: original headline decision records, compact
  classification-grid counts, selection outcomes, input hashes, and seeds.
- `data/*predictions.npy`, `test_labels.npy`: all individual headline and
  selected-method predictions plus the common balanced labels. Zero prediction
  rows at failed headline training repetitions are placeholders and are excluded.
- `data/uniform.json`: verbatim signs for all grid points of the five main S²
  cohorts and three S³ cohorts. Survey data superseded by refinement are omitted.
- `data/precision.json`, `headline_full_interval.json`: the 80 difficult-matrix
  records used for the precision comparison.
- `data/source_manifest.json`: hashes of original inputs, including all 300
  prediction shards and the original checker. Original inputs named here are
  provenance identifiers, not runtime dependencies.
- `SHA256SUMS`: hashes of every packaged file except the manifest itself.

The paper folder's `build_supplement.py` records the extraction recipe. No
assertion of priority is made beyond the bounded search dated 10–11 November
2026. The problem was selected and the work done and checked by OpenAI GPT-6.1
“Sol” cores, with Anthropic Claude as orchestrator and Aleksei Kudriashov as the
responsible author of record.
