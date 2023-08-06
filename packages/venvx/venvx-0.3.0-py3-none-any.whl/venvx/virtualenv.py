# pylint: disable = invalid-name

from functools import wraps
from pathlib import Path

from cozyconsole import Activity

from .console import console
from .tools import (PipUpgrader, PythonRunner, CommandRunner,
                    VenvActivator, VEnvDescriptor, VenvScript)


def venv_exists(decorated_function):
    @wraps(decorated_function)
    def decorator(venv: "VirtualEnv"):
        if not venv.path.is_dir():
            raise VenvError(f'The venv {str(venv.path)} does not exist.')
        decorated_function(venv)
    return decorator


class VenvError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    def __str__(self):
        return console.swrite(self._message, highlight=False)


class VirtualEnv(VenvActivator, VEnvDescriptor):
    def __init__(self, path: str):
        VenvActivator.__init__(self, path)
        VEnvDescriptor.__init__(self, path)

    def create(self,
               python_version: str = '3',
               upgrade_pip: bool = True,
               patch_scripts: bool = True):
        # python_cmd = f'python{python_version}'
        # self._python3 = shutil.which(python_cmd)
        # Shorten the venv path if it is a relative path.
        venv_path = self._path
        try:
            curr_dir = Path.cwd().resolve()
            venv_path = self._path.relative_to(curr_dir)
        except ValueError:
            # Not a relative path.
            pass
        with Activity(f'Creating virtual environment [b]{venv_path}[/]',
                      handle_exceptions=False) as act:
            if self._path.is_dir():
                msg = f'The folder [b]{venv_path}[/] already exists.'
                raise VenvError(msg)
            python = PythonRunner(py_version=python_version)
            rc = python.run('-m', 'venv', self._path)
            # Note: Python 3.7 requires str(self._path), above, but then
            # fails very badly in pytest. The exception is:
            # "RuntimeError: Cannot add child handler, the child watcher
            # does not have a l.."
            # It works in Python 3.8 and up. Removing support for Python 3.7.
            act.success = rc == 0
            if rc:
                raise RuntimeError(python.stderr)
        if upgrade_pip:
            self.upgrade_pip()
        if patch_scripts:
            self.fix()

    @venv_exists
    def info(self):
        # Info on venv including:
        # path
        # currently active?
        # python versio
        # pip version
        # pip update available?
        # locally installed packages
        pass

    @venv_exists
    def fix(self):
        with Activity('Checking if any scripts require patches') as act:
            scripts = [VenvScript(p) for p in self.binpath.glob('*')]
            need_shebang_fix = [s for s in scripts if s.needs_shebang_fix]
            need_venv_fix = [s for s in scripts if s.needs_virtualenv_fix]
            if need_shebang_fix or need_venv_fix:
                num_fixes = len(need_shebang_fix) + len(need_venv_fix)
                act.warning = f'yes ({num_fixes})'
            else:
                act.result = 'no'
            act.success = True
        # with Activity('Checking locally installed packages (-e)') as act:
        if not need_shebang_fix and not need_venv_fix:
            return
        for script in need_shebang_fix:
            with Activity('Fixing the shebang in '
                          f'[b]{script.path.name}[/]') as act:
                script.patch()
                act.success = True
        for script in need_venv_fix:
            with Activity('Fixing the VIRTUAL_ENV setting in '
                          f'[b]{script.path.name}[/]') as act:
                script.patch()
                act.success = True

    # TODO: Update the venv_exists decorator to take arguments.
    # Right now it does not, and that is why it cannot be used here.
    def run(self, command_line):
        with self:
            tr = CommandRunner(echo=True)
            tr.run(*command_line)

    # @venv_exists
    # def install_packages(self, update: bool,
    #                      packages: list[str] = [],
    #                      requirements: list[Path] = []):
    #     pass

    @venv_exists
    def upgrade_pip(self):
        with self:
            pip = PipUpgrader()
        with Activity('Checking if an upgrade is available for '
                      '[b]pip[/]') as act:
            rc = pip.check_upgrade()
            act.result = 'yes' if pip.upgrade_exists else 'no'
            act.success = rc == 0
        if not act.success:
            console.print('[b]An error occurred:[/]')
            console.print(pip.stderr)
            raise VenvError('Aborting')
        if not pip.upgrade_exists:
            return
        with Activity('Updating [b]pip[/] from '
                     f'[b]v{pip.current_version}[/] to '      # noqa: E128
                     f'[b]v{pip.newer_version}[/]') as act:   # noqa: E128
            rc = pip.perform_upgrade()
            act.success = rc == 0
        if not act.success:
            pass
            # figure out what to do

    @venv_exists
    def copy(self):
        pass
        # copy, then self.fix()

    @venv_exists
    def install(self):
        pass
