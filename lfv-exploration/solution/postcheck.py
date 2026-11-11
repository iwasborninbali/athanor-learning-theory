"""Run the remaining independent checks only after the census child exits."""
import json
from pathlib import Path
import subprocess
import time

deadline = time.monotonic()+1800
while True:
    log = Path('pipeline_n12.log').read_text().splitlines()
    if log and 'checked_witnesses.log' in log[-1]:
        break
    assert time.monotonic() < deadline, 'census did not finish in allotted wait'
    time.sleep(1)

for command, filename in [
    (['python3','check_regular.py','--exhaustive','--max-n','12'], 'checked_regular_exhaustive.log'),
    (['python3','check.py','--mode','exclusions','--reference','--max-n','8'], 'checked_reference.log'),
]:
    print(json.dumps(dict(starting=command)),flush=True)
    with Path(filename).open('w') as stream:
        subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=True)
subprocess.run(['python3','finalize.py'],check=True)
result = subprocess.run(['shasum','-a','256','-c','SHA256SUMS'],capture_output=True,text=True)
Path('hashcheck.log').write_text(result.stdout+result.stderr)
assert result.returncode == 0, result.stdout+result.stderr
print(json.dumps(dict(hash_verification='passed', files=len(result.stdout.splitlines()))),flush=True)
