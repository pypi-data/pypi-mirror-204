
import os
from pybrownies.testing import tmpdir
# import pytest
import shutil
import sys
from copy import deepcopy
from pathlib import Path

from venvx.tools import (is_windows, PythonRunner,
                         VenvActivator, VEnvDescriptor, VenvScript)


BIN_DIR = 'bin' if not is_windows() else 'Scripts'
PY_EXE = 'python3' if not is_windows() else 'python'


# region Helpers amd recorators

def get_venv_dirs(path: Path):
    if sys.platform in ['cygwin', 'msys', 'win32']:
        bin = 'Scripts'
        pkg = 'Lib/site-packages'
    else:
        version = f'{sys.version_info.major}.{sys.version_info.minor}'
        bin = 'bin'
        pkg = f'lib/python{version}/site-packages'
    return path.resolve()/bin, path.resolve()/pkg


def no_active_venv(decorated_function):
    '''
    Test cases decorated with this will run without a venv.
    '''
    def decorator():
        curr_venv = VENV_HOME
        del os.environ['VIRTUAL_ENV']
        decorated_function()
        os.environ['VIRTUAL_ENV'] = curr_venv
    return decorator

# endregion


VENV_HOME = os.environ['VIRTUAL_ENV']
VENV_BIN, VENV_PKG = get_venv_dirs(Path(VENV_HOME))


def test_pyrunner():
    python = PythonRunner()
    if '''Test for failure: wrong argument''':
        rc = python.run('foobar')
        assert 2 == rc
        assert '[Errno 2] No such file or directory' in python.stderr
    if '''Test for success: getting the Py version''':
        rc = python.run('--version')
        version = f'Python {sys.version.split()[0]}'
        assert 0 == rc
        assert version == python.stdout.strip()
    if '''Test for success: pip list -h''':
        rc = python.run('-m', 'pip', 'list', '-h')
        assert 0 == rc
        assert not python.stderr
        assert 'Usage' in python.stdout
        assert 'Description' in python.stdout
        assert 'Options' in python.stdout
    # if '''Test for failure: executable does not exist''':
    #     with pytest.raises(ValueError) as err:
    #         python = PythonRunner(executable='This executable does not exist.')
    #     assert 'not found' in str(err)


@no_active_venv
def test_venvactivator_off():
    venv_copy = deepcopy(os.environ)
    venv_path = Path('abc123')
    with VenvActivator(str(venv_path)) as venv:
        assert str(venv_path.resolve()) == os.environ['VIRTUAL_ENV']
        pathvar = Path(os.environ['PATH']).as_posix()
        venvdir = venv_path.resolve().as_posix()
        assert pathvar.startswith(venvdir)
    assert os.environ == venv_copy


@tmpdir
def test_venvactivator_on():
    venv_copy = deepcopy(os.environ)
    venv_path = Path('abc123')
    with VenvActivator(str(venv_path)) as venv:
        assert str(venv_path.resolve()) == os.environ['VIRTUAL_ENV']
        pathvar = Path(os.environ['PATH']).as_posix()
        venvdir = venv_path.resolve().as_posix()
        assert pathvar.startswith(venvdir)
        # In an existing venv the Python executable would be at
        # Path('abc123').resolve()/'bin/python3'
        # Since there is no abc123/bin/python3 the VenvActivator returns
        # the python3 exe from the repo's venv.
        expected_py = Path(venv_copy['VIRTUAL_ENV']).resolve()/f'{BIN_DIR}/{PY_EXE}'
        actual_py = Path(venv.python3)
        assert expected_py.as_posix() == actual_py.as_posix().rstrip('.eExX')
    assert os.environ == venv_copy
    if '''Now create a fake python3 in the test venv and recheck binpath.''':
        bin_path = venv_path / BIN_DIR
        bin_path.mkdir(parents=True)
        python = shutil.which(PY_EXE)
        # py_path = bin_path / PY_EXE
        shutil.copy2(python, bin_path)
        # py_path.touch(mode=0o777)
        # py_path.write_text(f'#!{shutil.which(PY_EXE)}\n')
        with VenvActivator(str(venv_path)) as venv:
            py_expected = Path.cwd().resolve()/f'abc123/{BIN_DIR}/{PY_EXE}'
            py_actual = Path(venv.python3)
            assert py_expected.as_posix() == py_actual.as_posix().rstrip('.eExX')


@no_active_venv
def test_venvdescriptor_off():
    vd = VEnvDescriptor('abc123')
    binpath, pkgpath = get_venv_dirs(Path('abc123'))
    assert binpath == vd.binpath
    assert pkgpath == vd.pkgpath
    assert Path('abc123').resolve() == vd.path
    assert 'abc123' == vd.name
    version = f'{sys.version_info.major}.{sys.version_info.minor}'
    assert version == vd.get_version(Path('abc123'))


def test_venvdescriptor_on():
    vd = VEnvDescriptor(VENV_HOME)
    assert VENV_BIN == vd.binpath
    assert VENV_PKG == vd.pkgpath
    assert Path(VENV_HOME) == vd.path
    assert Path(VENV_HOME).name == vd.name
    version = f'{sys.version_info.major}.{sys.version_info.minor}'
    assert version == vd.get_version(Path(VENV_HOME))


@tmpdir
def test_venvscript():
    if is_windows():
        _check_venvscript_windows()
    else:
        _check_venvscript_unix()


def _check_venvscript_unix():
    current_venv = os.environ['VIRTUAL_ENV']
    vdesc = VEnvDescriptor(current_venv)
    if '''Verify that VenvScript will not process binaries.''':
        vscript = VenvScript(Path('/usr/bin/env'))
        assert vscript.path == Path('/usr/bin/env')
        assert vscript._text is None
        assert vscript.needs_shebang_fix is False
        assert vscript.needs_virtualenv_fix is False
    if '''Verify that VenvScript will not process directories.''':
        vscript = VenvScript(Path(current_venv))
        assert vscript._text is None
        assert vscript.needs_shebang_fix is False
        assert vscript.needs_virtualenv_fix is False
    if '''Verify that VenvScript will not process symbolic links.''':
        vscript = VenvScript(Path(f'{shutil.which("python3")}'))
        assert vscript._text is None
        assert vscript.needs_shebang_fix is False
        assert vscript.needs_virtualenv_fix is False
    if '''Verify that no scripts in the current venv need their shebang
          fixed.''':
        scripts = [s for s in vdesc.binpath.glob('*')]
        to_patch = [s for s in scripts if VenvScript(s).needs_shebang_fix]
        assert 0 == len(to_patch)
    if '''Verify that no scripts in the current venv need their
          VIRTUAL_ENV line fixed.''':
        scripts = [s for s in vdesc.binpath.glob('*')]
        to_patch = [s for s in scripts if VenvScript(s).needs_virtualenv_fix]
        assert 0 == len(to_patch)
    if '''Verify that copied activate scripts get their VIRTUAL_ENV
          line patched.''':
        for activate_script in ['activate', 'activate.csh', 'activate.fish']:
            # 1) Confirm that the script requires the patch:
            shutil.copy2(vdesc.binpath/activate_script, '.')
            script = VenvScript(Path(activate_script))
            assert script.needs_virtualenv_fix
            # 2) Next, confirm that the patch was successfully applied:
            mtime1 = script._path.stat().st_mtime
            script.patch()
            mtime2 = script._path.stat().st_mtime
            assert mtime2 > mtime1
            script = VenvScript(Path(activate_script))   # Re-read it.
            assert not script.needs_virtualenv_fix       # Confirm it's fixed.
    if '''Verify that copied pip scripts get the shebang patched.''':
        for pip_script in ['pip', 'pip3']:
            # 1) Confirm that the script requires the patch:
            shutil.copy2(vdesc.binpath/pip_script, '.')
            script = VenvScript(Path(pip_script))
            assert script.needs_shebang_fix
            # 2) Next, confirm that the patch was successfully applied:
            mtime1 = script._path.stat().st_mtime
            script.patch()
            mtime2 = script._path.stat().st_mtime
            assert mtime2 > mtime1
            script = VenvScript(Path(pip_script))   # Re-read it.
            assert not script.needs_shebang_fix     # Confirm it's been fixed.

def _check_venvscript_windows():
    # TODO: implement this test.
    pass


# how to test venvx upgrade-pip:
# copy the current venv to tests/tmp
# get name if pip dist info in <sitepackages>
# pip-21.0.3.dist-info/
# obtain version number from it
# decrement major version
# mv  <sitepackages>/pip-dist<current> <sitepackages>/pip-dist<old>
