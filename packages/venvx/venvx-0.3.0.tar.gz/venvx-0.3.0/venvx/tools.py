
'''
happy happy pylint :)
'''

import os
import re
import shutil
import stat
import sys
from pathlib import Path
from typing import Optional

from venvx import pstream


def is_windows() -> bool:
    '''Returns True on Windows, False elsewhere.'''
    return sys.platform in ['cygwin', 'msys', 'win32']
    # return platform.uname().system == 'Windows'


def unix_path(path: Path) -> str:
    if is_windows():
        path = path.as_posix().replace(f'{path.drive}',
                                       f'/{path.drive.rstrip(":")}')
    else:
        path = str(path)
    return path


PY_EXE_NAME = 'python' if is_windows() else 'python3'


# Unix:
# python<version> <args>
# Windows
# py -<version> <args>

# On Windows, consider using option --no-warn-script-location.
# Else pip will warn: The scripts pip.exe, pip3.11.exe and pip3.exe are
# installed in 'C:\Users\ralf\AppData\Roaming\Python\Python311\Scripts'
# which is not on PATH.


class VenvActivator:
    '''
    VenvActivator is a context manager for running child processes of
    current Python instance in a virtual environment.

    Example usage:
    with VenvActivator('myvenv'):
        result = subprocess.run(<command>, <arguments...>)

    It activates a virtual environment for other processes to run in.
    It is not designed to make the currently running Python instance
    believe that it is running in a new environment. As such it does not
    modify sys.base_prefex, sys.exec_prefix, sys.path, nor site.PREFIXES,
    nor any other related internal state.
    '''

    @property
    def python3(self) -> Optional[str]:
        '''
        Return the path to the Python3 executable. This path changes
        when the Venv is activated or deactivated.
        '''
        return self._python3

    def __init__(self, venv_path: str):
        '''Constructor. It does constructive things. Yeah.'''
        self._venv = VEnvDescriptor(venv_path)
        self._envbackup = {
            'PATH': None,
            'VIRTUAL_ENV': None
        }
        self._python3 = shutil.which(PY_EXE_NAME)

    def __enter__(self):
        '''Activate the venv.'''
        for var in self._envbackup:
            self._envbackup[var] = os.environ.get(var)
        os.environ['VIRTUAL_ENV'] = str(self._venv.path)
        pathsep = ':' if not is_windows() else ';'
        pathitems = os.environ['PATH'].split(pathsep)
        pathitems.insert(0, str(self._venv.binpath))
        os.environ['PATH'] = pathsep.join(pathitems)
        self._python3 = shutil.which(PY_EXE_NAME)
        return self

    # def __exit__(self, exc_type, exc_value, exc_traceback):
    def __exit__(self, _, __, ___):
        '''Deactivate the venv, restore the pre-activation environment.'''
        os.environ['PATH'] = self._envbackup['PATH']
        self._python3 = shutil.which(PY_EXE_NAME)
        if self._envbackup['VIRTUAL_ENV']:
            # Restore the previous venv setting.
            os.environ['VIRTUAL_ENV'] = self._envbackup['VIRTUAL_ENV']
        else:
            # The was no active venv prior to __enter__.
            del os.environ['VIRTUAL_ENV']
        # handle or not any exceptions
        return False


class VEnvDescriptor:
    '''
    A VEnvDescriptor describes the structure and version of a virtual
    environment. The venv may or may not exist and it may or may not be
    activated.
    '''

    # exists(), is_active()
    # home, bin, site_packages : str

    _version_rex = re.compile(r'^(\d)\.(\d+)\..+$')

    @staticmethod
    def get_version(venv_path: Path) -> str:
        '''
        Returns the Python version for the venv. If the venv already
        exists the version will be read from the pyvenv.cfg file. The
        result will be the same whether the venv is activated or not.
        If the venv has not yet been created the version of the currently
        running Python instance will be used.
        '''
        major = sys.version_info.major
        minor = sys.version_info.minor
        pyconfig = venv_path / 'pyvenv.cfg'
        if pyconfig.exists():
            config = {}
            for line in pyconfig.read_text().splitlines():   # split('\n'):
                line = line.strip()
                if not line:
                    continue
                key, value = line.split('=')
                # equivalent: key, _, value = line.partition('=')
                config[key.strip()] = value.strip()
            # Now, Tox does not include a "version" key in the pyvenv.cfg
            # files it creates. It writes a "version_info" key instead.
            # Support both. Should a pyvenv.cfg file contain both keys,
            # "version" wins. version_info is of the form 3.9.10.final.0.
            for key in ['version_info', 'version']:
                if key in config:
                    match = VEnvDescriptor._version_rex.match(config[key])
                    if match:
                        major = int(match.group(1))
                        minor = int(match.group(2))
        return f'{major}.{minor}'

    @property
    def name(self) -> str:
        '''Returns the folder name of the virtual environment'''
        return self._path.name

    @property
    def path(self) -> Path:
        '''Returns the directory path to the virtual environment'''
        return self._path

    @property
    def binpath(self) -> Path:
        '''
        Returns the path containing the Python an Pip executables
        and the activate scripts.
        '''
        return self._path / ('Scripts' if is_windows() else 'bin')

    @property
    def pkgpath(self) -> Path:
        '''Returns the path of the venv's site packages.'''
        version = VEnvDescriptor.get_version(self._path)
        # return self._site_packages
        return self._path / (f'lib/python{version}/site-packages'
                             if not is_windows()
                             else 'Lib/site-packages')

    def __init__(self, path: str):
        '''Constructor.'''
        self._path = Path(path).resolve()
        #
        # self._version = VEnvDescriptor.get_version(self._path)
        # bindir = 'Scripts' if not is_windows() else 'bin'
        # libdir = 'Lib' if not is_windows() else
        # if is_windows():
        #     self._binpath = self._path / 'Scripts'
        #     self._site_packages = self._path / 'Lib/site-packages'
        # else:
        #     self._binpath = self._path / 'bin'
        #     self._site_packages = \
        #         self._path / f'lib/python{self._version}/site-packages'


class VenvScript:
    '''
    Instances of this class can detect and correct incorrect settings
    in a virtual environments scripts.
    '''
    # TODO: Support Windows DOS Command and Power Shells.

    shebang_rex = re.compile(r'^#!(.+)')
    venv_rex = {
        'activate': re.compile(r'VIRTUAL_ENV=["\'](.+)["\']'),
        'activate.csh': re.compile(r'setenv VIRTUAL_ENV ["\'](.+)["\']'),
        'activate.fish': re.compile(r'set -gx VIRTUAL_ENV ["\'](.+)["\']')
    }

    @property
    def needs_shebang_fix(self):
        '''
        Returns True if the script's shebang is incorrect and needs
        fixing.
        '''
        return not self._shebang_ok

    @property
    def needs_virtualenv_fix(self) -> bool:
        '''
        Returns True if the script's VIRTUAL_ENV definition is
        incorrect and needs fixing.
        '''
        return not self._virtualenv_ok

    @property
    def path(self) -> Path:
        '''Returns the path to the script file.'''
        return self._path

    def __init__(self, script_path: Path):
        self._path = script_path.resolve()
        self._text = None
        self._shebang_ok = True
        self._virtualenv_ok = True
        self._modified = False
        if script_path.is_file() and not script_path.is_symlink():
            try:
                with script_path.open('rt', encoding='utf-8') as fid:
                    self._text = fid.read()   # Fails if the file is binary.
                    self._shebang_ok = not self._needs_shebang_fix()
                    self._virtualenv_ok = not self._needs_virtualenv_fix()
            except UnicodeDecodeError:
                # OK, so this file is binary. Just ignore it.
                pass

    def __del__(self):
        self.save()

    def patch(self):
        '''Applies the patches and stores the file.'''
        if self.needs_shebang_fix:
            self._patch_shebang()
        if self.needs_virtualenv_fix:
            self._patch_virtualenv()
        self.save()

    def save(self):
        '''Saves any script patches back into the file.'''
        if not self._modified:
            return
        current_mode = self._path.stat().st_mode
        self._path.chmod(current_mode | stat.S_IWUSR)   # ensure write permission
        self._path.write_text(self._text, encoding='utf-8')
        self._modified = False

    def _needs_shebang_fix(self):
        if not self._text.startswith('#!/'):
            return False
        binpath = self._path.parent
        expected_shebang1 = f'#!{str(binpath / "python")}'
        expected_shebang2 = f'#!{str(binpath / "python3")}'
        return not (self._text.startswith(expected_shebang1)
                    or
                    self._text.startswith(expected_shebang2))

    def _needs_virtualenv_fix(self):
        script = self._path.name
        if script not in VenvScript.venv_rex:
            return False
        pattern = VenvScript.venv_rex[script]
        match = pattern.search(self._text)
        currently_set_to = match.group(1)
        what_it_needs_to_be = unix_path(self._path.parent.parent)   # .as_posix()
        return currently_set_to != what_it_needs_to_be

    def _patch_shebang(self):
        match = VenvScript.shebang_rex.search(self._text)
        binpath = self._path.parent
        old_shebang = f'#!{match.group(1)}'
        new_shebang = f'#!{str(binpath / "python3")}'
        self._text = self._text.replace(old_shebang, new_shebang)
        self._modified = True

    def _patch_virtualenv(self):
        script = str(self._path.name)
        pattern = VenvScript.venv_rex[script]
        match = pattern.search(self._text)
        old_venv = match.group(1)                        # venv path in the file
        new_venv = unix_path(self._path.parent.parent)   # correct venv path
        old_str = match.group(0)                         # line in the file
        new_str = old_str.replace(old_venv, new_venv)    # line to replace it
        self._text = self._text.replace(old_str, new_str)
        self._modified = True


# class VenvFixer:
#     def __init__(self, vdesc: VEnvDescriptor):
#         self._vdesc = vdesc


class CommandRunner:
    '''
    Runs an external commandline asynchronuously.
    '''

    @property
    def stderr(self) -> str:
        '''Returns the stderr output of the previous run().'''
        return '\n'.join(self._bufferr)

    @property
    def stdout(self) -> str:
        '''Returns the stdout output of the previous run().'''
        return '\n'.join(self._buffout)

    def __init__(self, echo: bool = False):
        self._bufferr: list[str] = []
        self._buffout: list[str] = []
        self._echo = echo

    def run(self, *args):
        '''
        Spawns python3 - or the executable passed to the constructor.
        Collects the sub-process' stdout and stderr, returns its exit
        code.
        '''
        self._bufferr = []
        self._buffout = []
        return pstream.execute(args,
                               stderr_cb=self._capture_stderr,
                               stdout_cb=self._capture_stdout)

    def _capture_stderr(self, line: str):
        self._bufferr.append(line)
        if self._echo:
            print(line, end='')

    def _capture_stdout(self, line: str):
        self._buffout.append(line)
        if self._echo:
            print(line, end='')


class PythonRunner(CommandRunner):
    '''
    An instance of this class encapsulates ...
    '''

    def __init__(self, echo: bool = False, py_version: str = None):
        '''Behold the constructor.'''
        super().__init__(echo)
        if py_version:
            self._executable = (
                ['py', f'-{py_version}']
                if is_windows() else
                [f'python{py_version}']
            )
        else:
            self._executable = [shutil.which(PY_EXE_NAME)]
        if not is_windows():
            return
        # On Unix and Unix-like systems, check if the requested Python version
        # is installed.
        if not shutil.which(self._executable[0]):
            error_msg = f"Can't find {self._executable[0]}. "
            # Show a helpful hint if asdf is installed.
            if shutil.which('asdf'):
                error_msg += (f'asdf is installed. Does your .tool-versions '
                              f'file list "python {py_version}"?')
                ValueError(error_msg)
            # Note: Consider supporting pyenv in a similar way.
        # A similar check for Windows involves calling
        # py -<version>> --list-paths
        # then parse the output to see if the requested version is listed.

    def run(self, *args):
        cmdline = [item for item in self._executable]
        cmdline.extend(args)
        return super().run(*cmdline)


class PipUpgrader(PythonRunner):
    '''
    Checks if a newer version is available for pip; upgrades the
    installed pip if so instructed.
    '''

    # pip3.9 and older
    search_pattern_old = re.compile('You are using pip version (.+); '
                                    'however, version (.+) is available')
    # pip3.10 and newer
    search_pattern_new = re.compile('A new release of pip .*available: (.+) -> (.+)')

    @property
    def current_version(self) -> str:
        '''
        Returns the version of the currently installed pip package,
        or None if check_upgrade has not yet been performed.
        '''
        return self._current_version

    @property
    def newer_version(self) -> str:
        '''
        Returns the latest available version of the pip package,
        or None if check_upgrade has not yet been performed.
        '''
        return self._newer_version

    @property
    def upgrade_exists(self) -> bool:
        '''Returns True if a newer version of pip is available.'''
        return self._newer_version is not None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_version = None
        self._newer_version = None

    def check_upgrade(self) -> int:
        '''
        Checks if a newer version of pip is available.
        Returns the exit code.
        '''
        # "pip list -e" does not reach out to PyPI so it probably is the
        # quickest way to detect if an update for pip is available.
        self._current_version = None
        self._newer_version = None
        return super().run('-m', 'pip', 'list', '-e')

    def perform_upgrade(self) -> int:
        '''
        Upgrades the installed pip package to the latest version.
        Returns the exit code.
        '''
        return super().run('-m', 'pip', 'install', '--upgrade', 'pip')

    def _capture_stderr(self, line: str):
        # Overloads PythonRunner._capture_stderr()
        match = PipUpgrader.search_pattern_new.search(line)
        if not match:
            match = PipUpgrader.search_pattern_old.search(line)
        if match:
            self._current_version = match.group(1)
            self._newer_version = match.group(2)
