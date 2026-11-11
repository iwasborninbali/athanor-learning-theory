"""Render and OCR the unreadable-font author PDF using existing Mac tools."""
import os
import subprocess
import time
from pathlib import Path

folder = Path('sources/koenig2001_pages')
folder.mkdir(exist_ok=True)
started = time.monotonic()
subprocess.run(['pdftoppm', '-r', '135', '-gray', '-png',
                'sources/koenig2001.pdf', str(folder / 'page')], check=True)
env = dict(os.environ, OMP_THREAD_LIMIT='1')
with Path('sources/koenig2001_ocr.txt').open('w') as out:
    for p in sorted(folder.glob('page-*.png')):
        r = subprocess.run(['tesseract', str(p), 'stdout'], check=True,
                           capture_output=True, text=True, env=env)
        out.write('\n\n===== PDF PAGE ' + p.stem.split('-')[-1] + ' =====\n\n')
        out.write(r.stdout)
        out.flush()
        print(p.name, round(time.monotonic() - started, 1), flush=True)
