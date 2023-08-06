
from copy import deepcopy
import os
from pathlib import Path
import shutil
import sys

from pybrownies.testing import tmpdir
import pytest

from venvx.console import console
from venvx.tools import is_windows, PythonRunner, VEnvDescriptor
from venvx.virtualenv import venv_exists, VenvError, VirtualEnv

from .test_tools import get_venv_dirs


from .fakevenv import FakeVenv


# test case skip examples
# @pytest.mark.skipif(sys.platform == 'win32')


@tmpdir
def test_virtualenv_core():
    venv_copy = deepcopy(os.environ)
    venv_path = Path('abc123')
    with VirtualEnv(str(venv_path)) as venv:
        binpath, pkgpath = get_venv_dirs(venv_path)
        assert binpath == venv.binpath
        assert pkgpath == venv.pkgpath
        assert Path('abc123').resolve() == venv.path
        assert Path('abc123').name == venv.name
        assert str(venv_path.resolve()) == os.environ['VIRTUAL_ENV']
        env_path = Path(os.environ['PATH'])
        assert env_path.as_posix().startswith(venv.binpath.as_posix())
        #assert os.environ['PATH'].startswith(str(venv_path.resolve()/'bin'))
    assert os.environ == venv_copy


def test_venv_copy():
    venv = VirtualEnv('test_venv_copy')
    with pytest.raises(VenvError):
        venv.copy()


@tmpdir
@pytest.mark.slow
def test_venv_create():
    #
    # Create venvs with the default Python version.
    #
    venv = VirtualEnv('test_venv_create')
    venv.create()
    assert venv.name == 'test_venv_create'
    assert venv.path.exists()
    assert venv.binpath.exists()
    assert venv.pkgpath.exists()
    with pytest.raises(VenvError) as err:
        venv.create()
        assert 'already exists' in str(err)
    #
    # Test creation of a venv using a different Python version than
    # the default.
    #
    major = sys.version_info.major
    minor = sys.version_info.minor
    current = f'{major}.{minor}'
    other   = f'{major}.{minor-1}' if minor > 7 else f'{major}.{minor+1}'
    #
    for ver in [other, current]:
        if not is_windows() and not shutil.which(f'python{ver}'):
            console.warning(f'\n\nPython {ver} not found, skipping test\n')
            continue
        name = f'test_venv_create_notox_{ver}'
        venv = VirtualEnv(name)
        venv.create(python_version=ver, upgrade_pip=False,patch_scripts=False)
        assert venv.name == name
        assert venv.path.exists()
        assert venv.pkgpath.exists()
        assert venv.binpath.exists()
        with venv:
            py = PythonRunner()
            py.run('--version')
            assert ver in py.stdout


def test_venv_exists():
    @venv_exists
    def dummy(venv):
        pass
    with pytest.raises(VenvError):
        venv = VEnvDescriptor('does not exist')
        dummy(venv)


def test_venv_error():
    try:
        raise VenvError('test message')
    except VenvError as err:
        assert 'test message' == str(err)


@tmpdir
def test_venv_fix(capsys):
    fenv = FakeVenv('venv')
    fenv.create(use_incorrect_path=True)
    venv = VirtualEnv('venv')
    venv.fix()
    result = capsys.readouterr()
    assert not result.err
    assert 'Checking if any scripts require patches' in result.out
    assert 'yes' in result.out
    if not is_windows():
        assert 'Fixing the shebang' in result.out
    #assert 'Fixing the VIRTUAL_ENV setting in activate' in result.out
    version = venv.get_version(venv.path)
    for test in ['Checking if any scripts require patches', 'yes',
                 'Fixing the VIRTUAL_ENV setting in ',
                 'activate', 'activate.csh', 'activate.fish']:
        assert test in result.out
    if not is_windows():
        for test in ['pip', 'pip3', f'pip{version}', 'done']:
            assert test in result.out
    venv.fix()
    result = capsys.readouterr()
    assert not result.err
    #assert 3 == len(result.out.splitlines())
    for test in ['Checking if any scripts require patches', 'no']:
        assert test in result.out
    for test in ['Fixing the shebang',
                 'Fixing the VIRTUAL_ENV setting in',
                 'activate', 'activate.csh', 'activate.fish']:
        assert test not in result.out
    if not is_windows():
        for test in ['pip', 'pip3', f'pip{version}', 'done']:
            assert test not in result.out



# def test_venv_install():
#     venv = VirtualEnv('test_venv_install')
#     with pytest.raises(VenvError):
#         venv.install()


def test_venv_info():
    venv = VirtualEnv('test_venv_install')
    with pytest.raises(VenvError):
        venv.info()


def test_venv_upgradepip():
    pass
