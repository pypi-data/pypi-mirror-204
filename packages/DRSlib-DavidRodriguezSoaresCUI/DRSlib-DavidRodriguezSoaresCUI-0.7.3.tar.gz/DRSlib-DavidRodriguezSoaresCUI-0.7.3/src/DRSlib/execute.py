# pylint: disable=broad-except


"""
Shell command execution
=======================

Sometimes we just want to execute a shell command and possibly
retrieve stdout/stderr, without hassle.
"""

from os import PathLike
from typing import Dict, Sequence, Union
from subprocess import Popen, PIPE  # nosec


COMMAND_TYPE = Union[
    Union[str, bytes, PathLike[str], PathLike[bytes]],
    Sequence[Union[str, bytes, PathLike[str], PathLike[bytes]]],
]


def execute(command: COMMAND_TYPE, shell: bool = False) -> Dict[str, str]:
    """Passes command to subprocess.Popen, retrieves stdout/stderr and performs
    error management.
    Returns a dictionnary containing stdX.
    Upon command failure, prints exception and returns empty dict."""

    try:
        with Popen(command, stdout=PIPE, stderr=PIPE, shell=shell) as process:  # nosec
            # wait and retrieve stdout/err
            _stdout, _stderr = process.communicate()
            # handle text encoding issues and return stdX
            return {
                "stdout": _stdout.decode("utf8", errors="backslashreplace"),
                "stderr": _stderr.decode("utf8", errors="backslashreplace"),
            }
    except Exception as e:
        print(f"execute: Error while executing command '{command}' : {e}")  # type: ignore[str-bytes-safe]
        raise
