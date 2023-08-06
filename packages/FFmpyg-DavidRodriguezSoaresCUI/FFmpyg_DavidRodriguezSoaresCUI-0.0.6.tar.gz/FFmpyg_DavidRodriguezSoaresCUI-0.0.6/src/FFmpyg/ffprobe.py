""" Contains FFPROBE-calling method to get a file's stream info
"""
import json
import logging
from pathlib import Path
from typing import List

from .command import Command
from .exceptions import FfprobeExecutionError


LOG = logging.getLogger(__file__)


def file_stream_info(file_path: Path) -> List[dict]:
    """Returns a list of stream info
    Raises FfprobeExecutionError on runtime error
    """
    # fmt: off
    cmd = Command(
        [
            "ffprobe",
            "-loglevel", "error",  # disable most messages
            "-show_entries", "stream",  # output all streams
            "-of", "json",  # output format as json
            file_path,
        ]
    )
    # fmt: on
    stdX = cmd.execute()

    # Detect errors
    if stdX["stderr"] != "":
        raise FfprobeExecutionError(
            f"Something went wrong: command='{cmd}' stderr='{stdX['stderr']}'"
        )

    return json.loads(stdX["stdout"])["streams"]
