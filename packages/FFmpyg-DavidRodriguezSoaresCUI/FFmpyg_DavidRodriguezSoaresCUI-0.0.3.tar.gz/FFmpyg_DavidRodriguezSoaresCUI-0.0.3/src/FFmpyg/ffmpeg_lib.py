"""
FFmpeg lib
==========

Some convenient methods to retrieve simple info about FFmpeg
"""
import logging
import re
from pathlib import Path
from typing import Dict, List, Union

from .command import Command
from .utils import assertTrue

FFMPEG_VERSION = re.compile(r"ffmpeg version (\S+) Copyright \(c\) \d{4}\-(\d{4})")
FFMPEG_FEATURE = re.compile(r"--enable-(\S+)")
LOG = logging.getLogger(__file__)


def get_ffmpeg_info(ffmpeg: Union[str, Path]) -> Dict[str, Union[List[str], str]]:
    """Parses the output from command `ffmpeg -version` and returns useful information"""
    try:
        stdX = Command([ffmpeg, "-version"]).execute()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Most likely wrong ffmpeg call '{ffmpeg}'") from e
    assertTrue(
        stdX["stdout"].startswith("ffmpeg version") and len(stdX["stderr"]) == 0,
        "Couldn't parse ffmpeg info (invalid ffmpeg path?) : {}",
        stdX,
    )

    res: Dict[str, Union[List[str], str]] = {}
    version_match = re.search(FFMPEG_VERSION, stdX["stdout"])
    LOG.debug("version_match : %s", version_match)
    if version_match:
        res["version"] = version_match.group(1)
        res["year"] = version_match.group(2)

    res["features"] = [
        x for x in re.findall(FFMPEG_FEATURE, stdX["stdout"]) if x != "nonfree"
    ]

    LOG.debug("FFMPEG info from %s : %s", ffmpeg, res)
    return res


def assert_ffmpeg_supports_feature(ffmpeg: Union[str, Path], feature: str) -> None:
    """Raises exception on FFmpeg not being callable or not having feature support"""
    assertTrue(
        feature in get_ffmpeg_info(ffmpeg)["features"],
        "FFMPEG at '{}' doesn't support {}! Please install/use a compatible version.",
        ffmpeg,
        feature,
    )
