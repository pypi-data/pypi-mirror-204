# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.0 - 2023-04-23

### Added

- Ubuntu and Windows (Git Bash) are now supported. (Only MacOS was supported
  prior to this version.)
- The new `venvx shellext` command may be used to review and install the venvx
  shell extension.
- THe `venv new` command is an alias for `venv create`.
- The `venv run` command executes a command in a venv without having to
  activate the venv, first. Example: `venv run 3.10 <command> <args>`.

### Removed

- Due to a [bug in pathlib](https://github.com/python/cpython/issues/82852),
  which was fixed in 3.10, support for Python 3.8 and 3.9 was dropped.

## 0.2.0 - 2023-03-11

### Added

- Support for Python 3.10 and 3.11 and the lastest Pip versions.
- bash and zsh integration: The file `shfuncs.sh` defines a `venv` command
  which can activate, deactivate, and switch between virtual environments.

## 0.1.0 - 2022-03-13

V0.1.0 is the first internal version. `venvx` is a convenience layer over the pip and venv modules. It can create new virtual environments and upgrade the `pip` inside. It can also update the shebangs of the scripts in a virtual environment's bin folder. This is useful e.g. after copying or moving a virtual environment.
