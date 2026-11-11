#!/usr/bin/env python3
"""Compact adaptation of the original statistical checker.

Default: replay saved per-repetition signs, predictions, intervals, and fits.
Optional --certify-reps: regenerate exact raw inputs and independently recertify.
Optional --refit-reps: refit the original C=1 headline SVM on regenerated inputs.
No network or parent-directory access; stdlib and NumPy for the default replay.
"""
import os
for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS']:
    os.environ[key] = '1'
import argparse
import ctypes
import hashlib
import json
import math
import statistics
from pathlib import Path
from fractions import Fraction
import numpy as np
from statistical_helpers import wilson, mean_ci, validate_decision

P = Path(__file__).resolve().parent

def load(name):
    return json.loads((P / 'data' / name).read_text())

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def close(a, b):
    return np.allclose(a, b, rtol=2e-11, atol=1e-13)

def regenerate(record, seed):
    out = []
    for stream, split, count in [(0, 'train', 100), (2, 'test', 200)]:
        y = np.tile([-1, 1], count)
        x = np.random.default_rng(np.random.SeedSequence([seed, 20, stream, record['rep']])).normal(size=(len(y), 3)) + .5 * y[:, None]
        digest = hashlib.sha256(np.asarray(x, dtype='<f8').tobytes(order='C')).hexdigest()
        require(digest == record['input_hashes'][split], f'Generator input mismatch: {split}, repetition {record["rep"]}; recorded NumPy 2.5.2')
        out.append(np.ascontiguousarray(x))
    return out

def ids(spec, size):
    return list(range(size)) if spec == 'all' else [int(x) for x in spec.split(',')]

def certify(spec, library, data):
    ptr = ctypes.POINTER(ctypes.c_double)
    fn = ctypes.CDLL(str(Path(library).resolve())).certify
    fn.argtypes = [ptr, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_int, ptr]
    fn.restype = ctypes.c_int
    for rep in ids(spec, len(data['records'])):
        r = data['records'][rep]
        x, z = regenerate(r, data['master_seed'])
        cases = [('train', x, r['train']['status'])]
        if r['train']['status'] == 1:
            cases.append(('append100', np.concatenate([x, z[:100]]), r['append100']['status']))
        for label, raw, expected in cases:
            for bits in [256, 512, 1024]:
                diagnostic = np.zeros(4)
                sign = fn(raw.ctypes.data_as(ptr), len(raw), 3, 2.5, 2, bits, diagnostic.ctypes.data_as(ptr))
                if sign:
                    break
            require(sign == expected, f'Interval replay disagreement: {rep}, {label}, {sign}')
            print('fresh interval replay', rep, label, 'sign', sign, 'bits', bits, 'pivot', diagnostic.tolist(), flush=True)

def distances(x, z=None):
    x = x / np.linalg.norm(x, axis=1)[:, None]
    z = x if z is None else z / np.linalg.norm(z, axis=1)[:, None]
    return 2 * np.arctan2(np.linalg.norm(x[:, None] - z[None, :], axis=2), np.linalg.norm(x[:, None] + z[None, :], axis=2))

def refit(spec, data, predictions):
    from svm import fit, predict
    y = np.tile([-1, 1], 100)
    for rep in ids(spec, len(data['records'])):
        r = data['records'][rep]
        if r['train']['status'] != 1:
            continue
        x, z = regenerate(r, data['master_seed'])
        dd, dz = distances(x), distances(z, x)
        warm = None
        for lam, g in zip(data['lambdas'], r['grid']):
            if lam > 2.5:
                break
            if g[0] != 1:
                continue
            kernel = np.exp(-lam * dd**2)
            np.fill_diagonal(kernel, 1.)
            model = fit(kernel, y, C=1., initial=warm)
            warm = model['alpha']
        actual = predict(model, np.exp(-2.5 * dz**2), y)
        require(np.array_equal(actual, predictions[rep]), f'Refit prediction disagreement: {rep}')
        print('fresh C=1 SVM refit', rep, 'all 400 predictions match', flush=True)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hashes', action='store_true')
    ap.add_argument('--certify-reps', help='comma-separated zero-based repetitions, or all')
    ap.add_argument('--interval-library', help='compiled independent_interval shared library')
    ap.add_argument('--refit-reps', help='comma-separated repetitions, or all')
    args = ap.parse_args()
    if args.hashes:
        for line in (P / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ', 1)
            require(hashlib.sha256((P / name).read_bytes()).hexdigest() == digest, 'Hash mismatch: ' + name)
        print('SHA-256 manifest verified')
    data = load('classification.json')
    rr = data['records']
    require([r['rep'] for r in rr] == list(range(300)), 'Classification repetitions')
    yt = np.load(P / 'data/test_labels.npy', allow_pickle=False)
    pred = np.load(P / 'data/headline_predictions.npy', allow_pickle=False)
    selected = np.load(P / 'data/selected_predictions.npy', allow_pickle=False)
    require(pred.shape == (300, 400) and selected.shape == (300, 3, 400), 'Prediction shapes')
    require(np.array_equal(yt, np.tile([-1, 1], 200)), 'Balanced test labels')
    pd = [r for r in rr if r['train']['status'] == 1]
    for r in rr:
        validate_decision(r['train'], 200)
        validate_decision(r['append100'], 300)
        require(r['train']['status'] in [-1, 1], 'Unresolved training sign')
        if r['train']['status'] == 1:
            require(int(np.sum(pred[r['rep']] == yt)) == r['headline_correct'], 'Headline prediction count')
        else:
            require(r['headline_correct'] is None and not np.any(pred[r['rep']]), 'Failed training placeholder')
        for mi, s in enumerate(r['selected']):
            require(int(np.sum(selected[r['rep'], mi] == yt)) == s['correct'], 'Selected prediction count')
    survivors = sum(r['append100']['status'] == 1 for r in pd)
    require(len(pd) == 297 and survivors == 0, 'Headline PD/append counts')
    correct = sum(r['headline_correct'] for r in pd)
    require(correct == 94081, 'Headline correct total')
    accuracy = mean_ci([r['headline_correct'] / 400 for r in pd])
    reference = load('reference.json')
    require(close(accuracy['ci95'], reference['headline']['accuracy_given_train_pd']['ci95']), 'Accuracy interval replay')
    print('headline training PD', f'{len(pd)}/300', 'Wilson 95%', wilson(len(pd), 300))
    print('headline append100 given training PD', f'{survivors}/{len(pd)}', 'Wilson 95%', wilson(survivors, len(pd)))
    print('headline accuracy', correct, '/', 297 * 400, accuracy)
    for mi, name in enumerate(['sphere_q1', 'sphere_q2', 'chord_q2']):
        stats = mean_ci([r['selected'][mi]['correct'] / 400 for r in rr])
        require(close(stats['mean'], reference['selected'][name]['mean']) and close(stats['ci95'], reference['selected'][name]['ci95']), 'Selected statistics: ' + name)
        print(name, 'selected accuracy', stats, 'append400 survivors', sum(r['selected'][mi]['append400'] == 1 for r in rr))
    j = data['lambdas'].index(2.5)
    for r in rr:
        require(r['grid'][j][0] == r['train']['status'] and r['grid'][j][3] == r['append100']['status'], 'Grid/headline correspondence')
    for lam in [2.25, 2.5, 2.75, 3., 3.5, 5.]:
        jj = data['lambdas'].index(lam)
        good = [r['grid'][jj] for r in rr if r['grid'][jj][0] == 1]
        print('q2 grid', lam, 'train', len(good), 'append100', sum(g[3] == 1 for g in good), 'append400', sum(g[5] == 1 for g in good), 'C1 accuracy', mean_ci([g[1] / 400 for g in good]))
    uniform = load('uniform.json')
    nn, medians = [], []
    for cohort in uniform:
        signs = np.asarray(cohort['signs'])
        ls = cohort['lambdas']
        require(np.all(np.isin(signs, [-1, 1])), 'Unresolved uniform sign')
        brackets = []
        for signs_r in signs:
            suffix = [k for k in range(len(ls)) if np.all(signs_r[k:] == 1)]
            require(bool(suffix), 'No finite suffix threshold')
            k = suffix[0]
            brackets.append([ls[k - 1] if k else 0., ls[k]])
        median = np.quantile(brackets, .5, axis=0)
        q90 = np.quantile(brackets, .9, axis=0)
        reversals = int(np.sum((signs[:, :-1] == 1) & (signs[:, 1:] == -1)))
        require(reversals == 0, 'Observed grid reversal')
        print('S' + str(cohort['dim']), 'N', cohort['n'], 'repetitions', len(signs), 'median', median.tolist(), '90%', q90.tolist(), 'reversals', reversals)
        if cohort['dim'] == 2:
            nn.append(cohort['n'])
            medians.append(float(np.mean(median)))
    affine = np.polyfit(np.sqrt(nn), medians, 1)
    require(close(affine, [reference['scaling']['affine_sqrt']['slope'], reference['scaling']['affine_sqrt']['intercept']]), 'Descriptive fit')
    print('descriptive sqrt fit', affine.tolist(), 'RMSE', float(np.sqrt(np.mean((np.polyval(affine, np.sqrt(nn)) - medians)**2))))
    precision = load('precision.json')
    full = load('headline_full_interval.json')
    require(len(precision) == len(full) == 80, 'Precision cohort length')
    for d, f in zip(precision, full):
        validate_decision(d, 400)
        validate_decision(f['full_interval'], 400)
        require(d['status'] == f['full_interval']['status'], 'Precision full-interval comparison')
    require(sum(d['status'] == 1 for d in precision) == 77, 'Precision PD count')
    require(sum(d['eig'] > 0 for d in precision) == 31, 'Raw floating PD count')
    require(sum(d['screen'] == 1 for d in precision) == 0, 'Separated floating PD count')
    print('N400 lambda3.25: PD 77/80, raw positive 31/80, separated positive 0/80')
    eigenvalues = load('figure1_eigenvalues.json')
    require(close(mean_ci(eigenvalues)['mean'], reference['left_panel']['uniform_n100_lambda_point1_mean_min_eigenvalue']['mean']), 'Figure discrepancy mean')
    print('Fig1 lambda0.1', mean_ci(eigenvalues))
    z = Fraction(1, 26)
    shell = 8 * z * (3 - 3 * z + z * z) / (1 - z)**3
    require(shell == Fraction(15608, 15625), 'Exact cap-packing series')
    print('exact shell sum', str(shell), 'margin', str(1 - shell), 'Bayes accuracy', statistics.NormalDist().cdf(math.sqrt(3) / 2))
    print('Saved headline statistics reproduced. Stored sign consistency is not fresh numerical certification.', flush=True)
    if args.refit_reps:
        refit(args.refit_reps, data, pred)
    if args.certify_reps:
        if not args.interval_library:
            ap.error('--certify-reps requires --interval-library; see README.md')
        certify(args.certify_reps, args.interval_library, data)

if __name__ == '__main__':
    main()
