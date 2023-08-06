
'''
This module implements the FakeVenv class. Instances help in testing by
creating the typical files and folders which make up a virtual environment.
'''

import shutil
import sys

from pathlib import Path

from venvx.tools import (PY_EXE_NAME, is_windows, unix_path,
                         PipUpgrader, VenvActivator, VEnvDescriptor)


class FakeVenv(VenvActivator, VEnvDescriptor):
        def __init__(self, path: str):
            VenvActivator.__init__(self, path)
            VEnvDescriptor.__init__(self, path)

        def create(self, use_incorrect_path=False, use_old_pip_version=True):
            for dir in [self.binpath, self.pkgpath]:
                dir.mkdir(parents=True)
            self._create_pyconfig()
            self._install_python(use_incorrect_path)
            self._install_site_packages(use_old_pip_version)
            self._install_scripts(use_incorrect_path)

        def _create_pyconfig(self):
            home_py = shutil.which(PY_EXE_NAME)
            ver = sys.version_info
            with open(self._path / 'pyconfig.cfg', 'w') as fid:
                fid.write(f'home = {Path(home_py).parent}\n')
                fid.write('include-system-site-packages = false\n')
                fid.write(f'version = {ver.major}.{ver.minor}.{ver.micro}\n')

        def _install_python(self, use_incorrect_path: bool):
            ver = self.get_version(self.path)
            exe_files = (
                ['python', 'python3', f'python{ver}']
                if not is_windows() else
                ['python.exe', 'pip.exe', 'pip3.exe', f'pip{ver}.exe']
            )
            for exe in exe_files:
                shutil.copy2(shutil.which(exe), self.binpath)
                # (self.binpath/python).symlink_to(shutil.which(python))
            if not is_windows():
                extra = '/extra' if use_incorrect_path else ''
                shebang = f'#!{self.binpath}{extra}/{PY_EXE_NAME}'
                for pip in ['pip', 'pip3', f'pip{ver}']:
                    pip = self.binpath/pip
                    pip.touch(mode=0o755)
                    pip.write_text(f'{shebang}\n')

        def _install_site_packages(self, use_old_pip_version):
            use_old_pip_version = True   # See comment in else branch below.
            if use_old_pip_version:
                pip_version = '20.0.0'
            else:
                # This works in that it obtains the latest version
                # number as intended. However, since our fake venv
                # does not deploy workable site packages, including
                # a workable pip package, pip list -e will fall back
                # on another pip site package, and that version may
                # or may not be current.
                with self:
                    pup = PipUpgrader()
                    pup.check_upgrade()
                pip_version = pup.newer_version or pup.current_version
            for folder in ['pip', f'pip-{pip_version}.dist-info']:
                dir = self.pkgpath/folder
                dir.mkdir()

        def _install_scripts(self, use_incorrect_path: bool):
            bindir = 'bin' if not is_windows() else 'Scripts'
            extra = '/extra' if use_incorrect_path else ''
            venvpath = f'{self.path.as_posix()}{extra}'
            venvpath = unix_path(self.path) + extra
            script = self.binpath/'activate'
            with open(script, 'w', encoding='utf-8') as fp:
                fp.write(f'VIRTUAL_ENV="{venvpath}"\n')
                fp.write(f'PATH="$VIRTUAL_ENV/{bindir}:$PATH"\n')
                fp.write('export VIRTUAL_ENV\n')
                fp.write('export PATH\n')
            script = self.binpath/'activate.csh'
            with open(script, 'w', encoding='utf-8') as fp:
                fp.write(f'setenv VIRTUAL_ENV "{venvpath}"\n')
                fp.write(f'setenv PATH "$VIRTUAL_ENV/{bindir}:$PATH"\n')
            script = self.binpath/'activate.fish'
            with open(script, 'w', encoding='utf-8') as fp:
                fp.write(f'set -gx VIRTUAL_ENV "{venvpath}"\n')
                fp.write(f'set -gx PATH "$VIRTUAL_ENV/{bindir} $PATH"\n')
