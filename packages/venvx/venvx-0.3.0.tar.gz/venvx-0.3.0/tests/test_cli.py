
import sys
from pathlib import Path

from pybrownies.testing import tmpdir
import pytest

from venvx.__main__ import DOTVENVX, VENVPREFIX, get_venv_path, main as runcli
from venvx.virtualenv import VenvError, VirtualEnv as Venv
from tests.fakevenv import FakeVenv


class Arguments:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@tmpdir
def test_get_venv_path():
    @get_venv_path
    def testfunc(venvpath, _):
        return venvpath

    args = Arguments(path=None)
    with pytest.raises(VenvError) as verr:
        testfunc(args)
    assert 'Please specify the virtual environment.' in str(verr)
    args.path = VENVPREFIX
    Path(VENVPREFIX).mkdir()
    assert VENVPREFIX == testfunc(args)
    args.path = None
    Path(DOTVENVX).write_text(VENVPREFIX + '\n')
    assert VENVPREFIX == testfunc(args)
    args.path = '3.11'
    venvname = VENVPREFIX + args.path
    Path(venvname).write_text(venvname + '\n')
    assert venvname == testfunc(args)


@tmpdir
def test_cli_fix(capsys):
    fe = FakeVenv('test_cli_fix')
    fe.create()
    # This:
    # with pytest.raises(VenvError):
    #    venvx('fix')
    # would not work because venvx.__main__:main snags the exception.
    # Instead capture the error message on stdout.
    if '''Confirm that we get the error message.''':
        venvx('fix')
        captured = capsys.readouterr()
        assert "Please specify the virtual environment" in captured.out
    if '''Confirm venvx fix works when receiving the venv as an argument.''':
        venvx('fix', 'test_cli_fix')
        captured = capsys.readouterr()
        assert "Checking if any scripts require patches" in captured.out
        assert "no" in captured.out
    if '''Confirm venvx fix works when getting the venv from the .venvx file.''':
        dot_venvx = Path('.venvx')
        dot_venvx.write_text('test_cli_fix\n')
        venvx('fix')
        dot_venvx.unlink()
        captured = capsys.readouterr()
        assert "Checking if any scripts require patches" in captured.out
        assert "no" in captured.out


@pytest.mark.slow
@tmpdir
def test_cli_upgrade_pip(capsys):
    venv = Venv('test_cli_upgrade_pip')
    venv.create(upgrade_pip=False, patch_scripts=False)
    if '''Confirm that we get the error message.''':
        venvx('upgrade-pip')
        captured = capsys.readouterr()
        assert "Please specify the virtual environment" in captured.out
    if '''Confirm venvx upgrade-pip works when receiving the venv as an
          argument.''':
        venvx('upgrade-pip', 'test_cli_upgrade_pip')
        captured = capsys.readouterr()
        assert "Checking if an upgrade is available" in captured.out
        # No further checks because an upgrade may or may not be available
        # i.e. the output is unpredictable.
    if '''Confirm venvx upgrade-pip works when getting the venv from
          the .venvx file.''':
        dot_venvx = Path('.venvx')
        dot_venvx.write_text('test_cli_upgrade_pip\n')
        venvx('upgrade-pip')
        assert "Checking if an upgrade is available" in captured.out
        # No further checks because an upgrade may or may not be available
        # i.e. the output is unpredictable.


@tmpdir
@pytest.mark.skipif(sys.platform == 'win32', reason='no "chmod" in Windows')
def test_cli_exception(capsys):
    fe = FakeVenv('test_cli_exception')
    fe.create()
    fe.path.chmod(0o644)
    try:
        venvx('fix', 'test_cli_exception')
    finally:
        fe.path.chmod(0o755)
    result = capsys.readouterr()
    assert 'PermissionError' in result.out


def venvx(*args):
    sys.argv = []
    sys.argv.append('venvx')
    for arg in args:
        sys.argv.append(arg)
    runcli()
