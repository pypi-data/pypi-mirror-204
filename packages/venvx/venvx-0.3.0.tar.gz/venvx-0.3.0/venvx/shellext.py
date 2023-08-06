
'''
# This module provides functions which can activate, deactivate, and
# switch between, virtual Python environments. bash and zsh are supported.
# Review the code below. If you approve, store it in a file e.g.
# venvx shellext > ~/.venvx.sh
# and source it into your bash or zsh profile
# [[ -f ~/.venvx.sh ]] && source ~/.venvx.sh
#
#
# And now, the code:

# Some ANSI escape codes for colorful/styled output.
# (Remember to use "echo -e".)
BOLD="\033[1m"
# DIM="\033[2m"
ITALIC="\033[3m"
# UNDERLINE="\033[4m"
# BLINKSLOW="\033[5m"
# BLINKFAST="\033[6m"
# STRIKETHRU="\033[9m"
RED='\033[0;31m'
YELLOW="\033[0;33m"
# green is 32m, blue is 34m, cyan is 36m
OFF="\033[0m"   # Resets everything.


# Source a venv's activate script. The venv is selected by either passing it
# as an argument or by reading it from a file named .venvx in the current
# working directory. A warning is emitted when trying to activate a venv
# while another is still active.
function __venv_activate {
    if [ -n "$VIRTUAL_ENV" ]; then
        curr_venv_parent=$(dirname $VIRTUAL_ENV)
        if [ "$curr_venv_parent" != "$(pwd)" ]; then
            echo -e -n "${YELLOW}The virtual environment in this folder has "
            echo -e    "not been activated because the virtual environment"
            echo -e    "${BOLD}$VIRTUAL_ENV$OFF"
            echo -e    "${YELLOW}is still active.$OFF"
        fi
        return
    fi
    venvpath=${1:-$(cat .venvx)}
    if [ -d $venvpath ]
    then
        sysname="$(uname -s)"
        case "${sysname}" in
            Darwin|Linux*)
                source $venvpath/bin/activate;;
            MINGW*|MSYS_NT*)
                source $venvpath/Scripts/activate;;
            *)
                echo -e "${RED}${BOLD}Unsupported OS:$OFF ${BOLD}$sysname$OFF"
        esac
        #source $venvpath/$bindirname/activate
    else
        echo -e "${RED}${BOLD}The folder$OFF ${BOLD}$venvpath ${RED}${BOLD}does not exist.$OFF"
    fi
}

# Convenience wrapper around virtual Python environments. Some features
# require the venvx package to be installed.
function venv {
    case "$1" in
        help)
            echo -e "usage: $0 command ..."
            echo    ""
            echo    "venv on           activates the venv stored in .venvx"
            echo    "venv off          deactivates the currently active venv"
            echo -e "venv use ${ITALIC}venv${OFF}     stores ${BOLD}${ITALIC}venv${OFF} in .venvx and activates it"
            echo -e "venv switch ${ITALIC}venv${OFF}  same as ${BOLD}use${OFF}"
            echo    "venv which        displays the currently active venv"
            echo    ""
            echo -e "Any other arguments are passed through to ${BOLD}venvx${OFF}."
            echo -e "See ${BOLD}venvx -h${OFF} for more information."
            ;;
        on)
            __venv_activate
            ;;
        off)
            [ -n "${VIRTUAL_ENV}" ] && deactivate
            ;;
        use|switch)
            if [ "$#" != 2 ]; then
                echo "usage: $0 $1 venvpath"
                return
            fi
            [ -n "${VIRTUAL_ENV}" ] && deactivate
            venvpath=$2
            # Undocumented feature: If the argument is a Python version
            # number, prefix it with .venv. So
            # venv use 3.9
            # is short-hand for
            # venv use .venv3.9
            [[ $venvpath =~ ^3\.?[0-9]+$ ]] && venvpath=".venv$2"
            if [ -d $venvpath ]; then
                echo $venvpath > .venvx
                __venv_activate
            else
                echo -e "${RED}${BOLD}The folder$OFF ${BOLD}$venvpath ${RED}${BOLD}does not exist.$OFF"
            fi
            ;;
        which)
            echo ${VIRTUAL_ENV:-""}
            ;;
        *)
            venvx $@
            ;;
    esac
}


# When changing into a directory that contains a .venvx file, try
# activating it.
function cd {
    builtin cd "$@"
    rc=$?
    [[ -f .venvx ]] && venv on
    return $rc
}
'''
