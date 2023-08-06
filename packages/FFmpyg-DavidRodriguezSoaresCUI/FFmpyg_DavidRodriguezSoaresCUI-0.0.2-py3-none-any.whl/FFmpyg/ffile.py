""" Supporting classes and logic for FFMPEG encode planning

Note : stream indexes exist in both Stream and MediaFile for
consistency checking and ease of use
"""


from collections import namedtuple
from pathlib import Path
from typing import List

from .enums import FfprobeInfoKey, StreamType
from .ffprobe import file_stream_info
from .stream import FutureStream, Stream
from .utils import assertTrue

StreamCriteria = namedtuple("StreamCriteria", "codec_type codec")


class MediaFile:
    """FFMPEG-focused media file representation; views a media file as a
    container for streams."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.streams = (
            {}
            if (path is None or not path.is_file())
            else {
                stream.get(FfprobeInfoKey.INDEX): stream
                for stream in [
                    Stream(stream_info) for stream_info in file_stream_info(path)
                ]
            }
        )

    def get_streams(self, criteria: StreamCriteria) -> List[Stream]:
        """Return list of streams that correspond to criteria"""
        d_criteria = criteria._asdict()
        return [
            stream
            for stream in self.streams.values()
            if all(
                d_criteria[c] is None
                or stream.get(c) == (
                    d_criteria[c].value
                    if isinstance(d_criteria[c], StreamType)
                    else d_criteria[c]
                )
                for c in d_criteria.keys()
            )  # fmt: skip
        ]

    @property
    def valid(self) -> bool:
        """Is valid if file has streams and stream indexes are contiguous"""
        return len(self.streams) > 0 and list(sorted(self.streams.keys())) == list(
            range(max(self.streams.keys()) + 1)
        )

    def __str__(self) -> str:
        """representation of self"""
        return f"<{self.__class__.__name__}: path={self.path} streams={self.streams}>"


class FutureMediaFile(MediaFile):
    """FFMPEG-focused future media file representation; views a media file
    as a container for streams."""

    def __init__(self, path: Path) -> None:
        assertTrue(
            path is not None and not path.exists(),
            "Path must be non-null and not exist: path={}",
            path,
        )
        super().__init__(path)

    def add_stream(self, stream: FutureStream) -> "FutureMediaFile":
        """Adds a stream; Call can be chained"""
        next_stream_idx = max(self.streams.keys()) + 1 if self.streams else 0
        assertTrue(
            stream.idx == next_stream_idx,
            "Expected FutureStream index to be {}, not {}",
            next_stream_idx,
            stream.idx,
        )
        self.streams[stream.idx] = stream
        return self

    def load_actual_file(self) -> MediaFile:
        """Requires the FutureMediaFile to have been produced"""
        return MediaFile(self.path)
