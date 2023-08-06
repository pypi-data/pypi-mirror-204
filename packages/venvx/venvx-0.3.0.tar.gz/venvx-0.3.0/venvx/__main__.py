#!/usr/bin/env python3

'''
This module provides a command line interface for the venvx package.

Usage:

% venvx create
Creates a virtual environment ".venv" in the current working directory,
and upgrades "pip" if a newer version is available.

% venvx create myenv
Creates a virtual environment "myenv" in the current working directory,
and upgrades "pip" if a newer version is available.

% venvx create --no-upgrade
Creates a virtual environment ".venv" in the current working directory.

% venvx fix
Checks the shebangs of the scripts in the venv's bin folder and
Fixes the .venv/Scripts/activate script for Git Bash in Windows
Without this the PATH will be invalid.

% venvx upgrade
Upgrades "pip" in the existing virtual environment .venv if a newer
version is available

% venvx upgrade myenv
Upgrades "pip" in the existing virtual environment myenv if a newer
version is available.
'''

# % venv install
# Installs Python packages in a virtual environment - this is not ready yet.


import argparse
import shutil
from functools import wraps
from pathlib import Path

from rich_argparse_plus import RichHelpFormatterPlus

from venvx.tools import is_windows
from venvx.virtualenv import VenvError, VirtualEnv as Venv

from .console import console


DOTVENVX = '.venvx'
VENVPREFIX = '.venv'


def _path_arg(new: bool = False):
    return f'path to the {"new " if new else ""}virtual environment'

def configure_cmdline():
    RichHelpFormatterPlus.choose_theme('black_and_white')
    RichHelpFormatterPlus.styles['argparse.args'] = 'default'
    RichHelpFormatterPlus.styles['argparse.groups'] = 'bold'
    RichHelpFormatterPlus.styles['argparse.help'] = 'default'
    RichHelpFormatterPlus.styles['argparse.metavar'] = 'default'
    RichHelpFormatterPlus.styles['argparse.syntax'] = 'bold'
    RichHelpFormatterPlus.styles['argparse.text'] = 'default'
    RichHelpFormatterPlus.group_name_formatter = str.title

    main_parser = argparse.ArgumentParser(
        formatter_class=RichHelpFormatterPlus,
        description='Create and manage virtual Python environments.',
        epilog='It is safe to run these commands while another virtual '
               'environment is active, or if no virtual environment is '
               'active.',
    )
    subparsers = main_parser.add_subparsers(
        metavar='COMMAND',
        help='[u]Description[/u]',
        dest='subcommand'
    )

    # region create command
    def add_create_parser(name: str, help: str):
        parser = subparsers.add_parser(
            formatter_class=main_parser.formatter_class,
            name=name,
            description='Create virtual Python environments.',
            help=help,
        )
        parser.add_argument(
            'path', nargs='?',
            default=VENVPREFIX,
            help=_path_arg(True),
        )
        parser.add_argument(
            '--no-fix',
            action='store_true',
            help="do not correct the path settings in the venv's scripts",
        )
        parser.add_argument(
            '--no-upgrade',
            action='store_true',
            help="do not update the venv's pip package to the latest version",
        )
        parser.add_argument(
            '-v', '--versions',
            nargs='*',
            default=None,
            type=str,
            choices=['3.8', '3.9', '3.10', '3.11'],
            help='create venvs for the specified Python version(s)'
        )
        return parser

    create_parser = add_create_parser('create',
                                      'create a new virtual environment')
    # endregion -----------

    # region fix command
    fix_parser = subparsers.add_parser(
        formatter_class=main_parser.formatter_class,
        name='fix',
        description="Fix the paths in the activate script's VIRTUAL_ENV "
                    "definition as well as in the shebangs of the various "
                    "scripts.",
        epilog='This command corrects the weird mix of Windows- and '
               'POSIX-style paths that occurs in Git Bash on Windows.\nIt '
               'is also useful after copying/moving a venv to a new location.',
        help="fix the path settings in the venv's scripts",
    )
    fix_parser.add_argument(
        'path', nargs='?',
        default=None,
        help=_path_arg() + '\n(default: the path stored in the .venvx) file',
    )
    # endregion --------

    # new_parser = subparsers.add_parser(
    #     name='new',
    #     parents=[create_parser],
    #     add_help=False,
    # )
    new_parser = add_create_parser('new',
                                   'this is an alias for the create command')

    # region install command
    # endregion --------

    run_parser = subparsers.add_parser(
        formatter_class=main_parser.formatter_class,
        name='run',
        description="Run commands within a specified venv.",
        help="run",
    )
    run_parser.add_argument(
        'path',
        help='the venv to run in',
    )
    run_parser.add_argument(
        'command', nargs='+',
        help='command to execute in the venv',
    )

    # region upgrade-pip command
    upgrade_parser = subparsers.add_parser(
        formatter_class=main_parser.formatter_class,
        name='upgrade-pip',
        description="Upgrade the venv's [i]pip[/i] package if a newer "
                    "version is available.",
        help='upgrade [i]pip[/i] if a newer version is available',
    )
    upgrade_parser.add_argument(
        'path', nargs='?',
        default=None,
        help=_path_arg() + '\n(default: the path stored in the .venvx) file',
    )
    # newupgrade_parser = subparsers.add_parser(
    #     name='update',
    #     description="tbd",
    #     help='tbd',
    #     formatter_class=main_parser.formatter_class,
    # )
    # newupgrade_parser.add_argument(
    #     'path', nargs='?',
    #     default=None,
    #     help=_path_arg() + '\n(default: the path stored in the .venvx) file',
    # )
    # newupgrade_parser.add_argument(
    #     '-n', '--no-pip',
    #     action='store_true',
    #     help="do not upgrade the venv's pip package to the latest version",
    # )
    # newupgrade_parser.add_argument(
    #     '-p', '--packages',
    #     nargs='*',
    #     help='package(s) to update',
    # )
    # newupgrade_parser.add_argument(
    #     '-r', '--requirements',
    #     nargs='*',
    #     help='requirements file(s) containing the packages to update',
    # )
    # This will be superceded by venvx update [--pip-only] [--pkg-only].
    # Without options, venvx update will update the pip package, the run
    # pip install --upgrade on all of the installed packages.
    # Wait: Really? Including all those dependencies. INcluding those that
    # after the update will case dependency conflicts. No, Let's try that
    # again. venvx update [--no-pip] [requirements-file]. Option --no-pip
    # will not upgrade the pip package. Subsequently, if a requirements-file is
    # specified, pip install --upgrade -r requirements-file. Yep, that's
    # better.
    # Or: venvx upgrade [--no-pip] [pkgname-or-req-file] ...
    # venv update alias for venv upgrade
    # endregion --------

    # region shell command
    shell_parser = subparsers.add_parser(
        name='shellext',
        description='Display the venvx shell extensions.',
        help='display the venvx shell extensions',
        formatter_class=main_parser.formatter_class,
    )
    # endregion --------

    create_parser.set_defaults(func=handle_create_command)
    new_parser.set_defaults(func=handle_create_command)
    fix_parser.set_defaults(func=handle_fix_command)
    run_parser.set_defaults(func=handle_run_command)
    upgrade_parser.set_defaults(func=handle_upgrade_command)
    # newupgrade_parser.set_defaults(func=handle_newupgrade_command)
    shell_parser.set_defaults(func=handle_shell_command)

    return main_parser


# region Decorators

def get_venv_path(decorated_function):
    @wraps(decorated_function)
    def decorator(args):
        venv_path = args.path
        if not venv_path:
            # Obtain the venv's path from the .venvx file.
            dot_venvx = Path(DOTVENVX)
            if dot_venvx.exists():
                venv_path = dot_venvx.read_text(encoding='utf-8').strip()
        else:
            if not Path(venv_path).exists():
                venv_path = None
            test = Path(f'{VENVPREFIX}{args.path}')
            if test.exists():
                venv_path = str(test)
        if not venv_path:
            raise VenvError('Please specify the virtual environment.')
        return decorated_function(venv_path, args)
    return decorator

# endregion


def handle_create_command(args):
    if not args.versions:
        venv = Venv(Path(args.path))
        venv.create()
    else:
        for ver in args.versions:
            if not is_windows():
                python = f'python{ver}'
                if not shutil.which(python):
                    console.warning(f'Cannot find Python {ver}.')
                    continue
            venv = Venv(Path(f'{args.path}{ver}'))
            venv.create(python_version=ver)
    # TODO: Fix this for the case when the venv_prefix points to another
    # directory.
    dot_venvx = Path(DOTVENVX)
    if not dot_venvx:
        dot_venvx.write_text(venv.path)


@get_venv_path
def handle_fix_command(venv_path: str, _):
    venv = Venv(venv_path)
    venv.fix()


@get_venv_path
def handle_info_command(venv_path: str, _):
    venv = Venv(venv_path)
    venv.info()


@get_venv_path
def handle_run_command(venv_path: str, args):
    venv = Venv(venv_path)
    venv.run(args.command)


@get_venv_path
def handle_upgrade_command(venv_path: str, _):
    venv = Venv(venv_path)
    venv.upgrade_pip()


@get_venv_path
def handle_newupgrade_command(venv_path: str, args):
    print(f'{venv_path=}')
    print(f'{args.no_pip=}')
    print(f'{args.packages=}')
    print(f'{args.requirements=}')


def handle_shell_command(args):
    from venvx import shellext
    console.print(shellext.__doc__)


def main():
    parser = configure_cmdline()
    args   = parser.parse_args()
    # merge_configuration(arguments)
    if not args.subcommand:
        parser.print_help()
        return

    # pylint: disable = bare-except
    # because console.print_exception() handles the exception by printing
    # the stack trace
    try:
        args.func(args)
    except VenvError as err:
        print(err)
    except:   # noqa: E722
        console.print_exception()


if __name__ == "__main__":
    main()
