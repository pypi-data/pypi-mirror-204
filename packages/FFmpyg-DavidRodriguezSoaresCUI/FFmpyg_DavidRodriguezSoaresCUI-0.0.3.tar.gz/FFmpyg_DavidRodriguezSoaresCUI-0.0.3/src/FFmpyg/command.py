""" Contains class Command, used to execute external programs
"""
import logging
from os import PathLike
from subprocess import PIPE, Popen
from typing import Any, Dict, List

from .utils import ensureQuoted, assertTrue


LOG = logging.getLogger(__file__)


class Command:
    """Represents a shell command as a list of parts, and
    handles execution"""

    def __init__(self, command: List[Any]) -> None:
        self._cmd = [
            c if isinstance(c, (str, bytes, PathLike)) else str(c) for c in command
        ]

    def __ensure_cmd_set(self) -> None:
        """Raises ValueError on command not set"""
        assertTrue(self._cmd is not None, "Command not set")

    def execute(self) -> Dict[str, str]:
        """Passes command to subprocess.Popen, retrieves stdout/stderr and performs
        error management.
        Returns a dictionnary containing stdX.
        Upon command failure, logs exception but doesn't catch it
        """
        self.__ensure_cmd_set()
        try:
            with Popen(self._cmd, stdout=PIPE, stderr=PIPE, shell=False) as process:
                # wait and retrieve stdout/err
                _stdout, _stderr = process.communicate()
                # handle text encoding issues and return stdX
                return {
                    "stdout": _stdout.decode("utf8", errors="backslashreplace"),
                    "stderr": _stderr.decode("utf8", errors="backslashreplace"),
                }
        except Exception as e:
            LOG.warning("Error while executing command '%s' : %s", self._cmd, e)
            raise

    def to_script(self) -> str:
        """Returns string compatible with SH/BAT scripts"""
        self.__ensure_cmd_set()
        return " ".join(
            ensureQuoted(x)
            for x in [c if isinstance(c, str) else str(c) for c in self._cmd]
        )

    def __str__(self) -> str:
        """String representation defaults to script representation"""
        return self.to_script()
