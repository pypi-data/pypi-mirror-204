""" Contains enums related to how FFMPEG/FFPROBE names/represents stuff
"""
from enum import Enum


class StreamType(Enum):
    """Represent the 4 types of streams"""

    # fmt: off
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"
    ATTACHMENT = "attachment"
    # fmt: on

    @staticmethod
    def from_ffmpeg_code(code: str) -> "StreamType":
        """FFMPEG encodes this information in one character (V,A,S)"""
        if code == "V":
            return StreamType.VIDEO
        if code == "A":
            return StreamType.AUDIO
        if code == "S":
            return StreamType.SUBTITLE
        raise ValueError(f"Can't decode '{code}'")


class FfprobeInfoKey(Enum):
    """Common FFPROBE info keys"""

    # fmt: off
    INDEX         = 'index'
    CODEC         = 'codec_name'
    CODEC_LONG    = 'codec_long_name'
    DURATION      = 'duration'
    IS_DEFAULT    = 'disposition.default'
    IS_FORCED     = 'disposition.forced'
    STREAM_TYPE   = 'codec_type'
    HEIGHT        = 'height'
    WIDTH         = 'width'
    AVG_FRAMERATE = 'avg_frame_rate'
    LANGUAGE      = 'tags.language'
    TITLE         = 'tags.title'
    # fmt: on
