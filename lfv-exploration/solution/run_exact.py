"""One heavy child at a time, with disk and progress monitoring."""
import argparse, datetime, json, pathlib, shutil, subprocess, time

base = pathlib.Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--max-n', type=int, default=12)
parser.add_argument('--min-n', type=int, default=1)
parser.add_argument('--generate', action='store_true')
parser.add_argument('--check', action='store_true')
args = parser.parse_args()


def run(command, log):
    assert shutil.disk_usage(base).free >= 3*1024**3
    started = time.monotonic(); last = started
    with (base / log).open('w') as output:
        p = subprocess.Popen(command, cwd=base, stdout=output, stderr=subprocess.STDOUT)
        while p.poll() is None:
            time.sleep(1)
            now = time.monotonic()
            if shutil.disk_usage(base).free < 3*1024**3:
                p.terminate(); p.wait(); raise RuntimeError('free disk below 3 GiB')
            if now-last >= 600:
                stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
                with (base / 'progress.md').open('a') as progress:
                    progress.write(f'\n{stamp}: still running {command!r}; elapsed {now-started:.0f}s; free disk {shutil.disk_usage(base).free/1024**3:.1f} GiB.\n')
                last = now
        if p.returncode:
            raise RuntimeError((command, p.returncode, log))
    print(json.dumps(dict(command=command, log=log, seconds=time.monotonic()-started)), flush=True)


if args.generate:
    run(['python3', 'generate_graphs.py', '--max-n', str(args.max_n)], 'catalog_generation.log')
for n in range(args.min_n, args.max_n+1):
    run(['./search', str(n), f'catalog/n{n}.txt', 'exact'], f'exact_n{n}.log')
if args.check:
    run(['python3', 'check.py', '--mode', 'catalogues', '--max-n', str(args.max_n)], 'checked_catalogues.log')
    run(['python3', 'check.py', '--mode', 'exclusions', '--min-n', str(args.min_n), '--max-n', str(args.max_n)], 'checked_exclusions.log')
    run(['python3', 'check.py', '--mode', 'witnesses', '--max-n', str(args.max_n)], 'checked_witnesses.log')
