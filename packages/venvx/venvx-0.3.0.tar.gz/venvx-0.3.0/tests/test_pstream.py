
import sys

from venvx import pstream
from venvx.tools import is_windows


buffer_stderr = []
buffer_stdout = []

def capture_stderr(line):
    global stderr
    buffer_stderr.append(line)

def capture_stdout(line):
    global stdout
    buffer_stdout.append(line)


def test_pstream():
    version = f'Python {sys.version.split()[0]}'
    executable = f'{"python" if is_windows() else "python3"}'
    rc = pstream.execute([executable, '--version'],
                         stdout_cb=capture_stdout,
                         stderr_cb=capture_stderr)
    assert 0 == rc
    assert 0 == len(buffer_stderr)
    assert 1 == len(buffer_stdout)
    assert version == buffer_stdout[0].strip()
