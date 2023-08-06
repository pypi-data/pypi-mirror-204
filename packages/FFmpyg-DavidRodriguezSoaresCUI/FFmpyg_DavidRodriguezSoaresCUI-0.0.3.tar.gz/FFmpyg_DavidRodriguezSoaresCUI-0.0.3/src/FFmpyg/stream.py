""" Streams are the elementary components of a media file
"""
from typing import Any, Optional, Union

from .ffmpeg_encoder import Encoder
from .enums import FfprobeInfoKey, StreamType
from .utils import assertTrue, dict_difference, flatten_dict_join


StreamKeyType = Union[FfprobeInfoKey, StreamType, str]


class Stream:
    """Multimedia stream"""

    DEFAULT_VALUES = {
        "codec_tag": "0x0000",
        "codec_tag_string": "[0][0][0][0]",
        "disposition.attached_pic": 0,
        "disposition.clean_effects": 0,
        "disposition.comment": 0,
        "disposition.default": 0,
        "disposition.dub": 0,
        "disposition.forced": 0,
        "disposition.hearing_impaired": 0,
        "disposition.karaoke": 0,
        "disposition.lyrics": 0,
        "disposition.original": 0,
        "disposition.timed_thumbnails": 0,
        "disposition.visual_impaired": 0,
        "start_pts": 0,
        "start_time": "0.000000",
    }

    UNAVAILABLE_DATA = {
        "avg_frame_rate": "0/0",
        "codec_time_base": "0/1",
        "r_frame_rate": "0/0",
    }

    def __init__(self, ffprobe_info: dict):
        self.ffinfo = dict_difference(
            flatten_dict_join(ffprobe_info), Stream.UNAVAILABLE_DATA
        )
        self._particular_keys = list(self.particular_info.keys())

    @staticmethod
    def key_handling(key: StreamKeyType) -> str:
        """Handles key sanitization and type checking"""
        if isinstance(key, FfprobeInfoKey):
            return key.value
        if isinstance(key, StreamType):
            return FfprobeInfoKey.STREAM_TYPE.value
        assertTrue(
            isinstance(key, str), "Can't handle key '{}' of type {}", key, type(key)
        )
        return key

    @property
    def particular_info(self) -> dict:
        """Subset of ffinfo, without items with default value"""
        return dict_difference(self.ffinfo, Stream.DEFAULT_VALUES)

    @property
    def idx(self) -> int:
        """Stream's index"""
        return self.ffinfo[FfprobeInfoKey.INDEX.value]

    def is_default(self, key: StreamKeyType) -> bool:
        """Checks if a particular value in ffinfo is at default value. Only returns True
        if key is present AND value is default
        """
        k = Stream.key_handling(key)
        return (
            (k in self.ffinfo)
            and (k in Stream.DEFAULT_VALUES)
            and (Stream.DEFAULT_VALUES[k] == self.ffinfo[k])
        )

    def __convert_value(self, key: str) -> Any:
        """Attempts to convert values if possible"""
        v = self.ffinfo[key]
        # Case : disposition.* -> bool
        if key.startswith("disposition."):
            return v == 1
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                pass
            try:
                return float(v)
            except ValueError:
                pass
        return v

    def get(self, key: StreamKeyType, default: Any = None, convert: bool = True) -> Any:
        """Attempts to return the value associated in ffinfo. If info isn't available,
        `default` is returned if present/not None or an exception is raised.
        `convert`: perform automatic data type conversion (default: True)
        """
        k = Stream.key_handling(key)
        if k in self.ffinfo:
            return self.__convert_value(k) if convert else self.ffinfo[k]
        if default is not None:
            return default
        raise KeyError(f"{k} not in {set(self.ffinfo.keys())}")

    def __str__(self) -> str:
        kv = ", ".join(f"{k}={v}" for k, v in self.particular_info.items())
        return f"<Stream: {kv}>"


class FutureStream(Stream):
    """Used to plan a future stream"""

    def __init__(
        self,
        index: int,
        codec: Optional[str] = None,
        stream_type: Optional[StreamType] = None,
        encoder: Optional[Encoder] = None,
        **kwargs,
    ) -> None:
        """Initializing requires:
        - stream index
        - either an Encoder or a codec and stream type
        """
        if encoder is None and (codec is None or stream_type is None):
            raise ValueError(
                "Parameters required: either 'codec' and 'stream_type', or 'encoder' (can't all be None)"
            )

        super().__init__(
            {
                FfprobeInfoKey.INDEX.value: index,
                FfprobeInfoKey.CODEC.value: encoder.codec if codec is not None else codec,  # type: ignore[union-attr]
                FfprobeInfoKey.STREAM_TYPE.value: encoder.stream_type if stream_type is not None else stream_type,  # type: ignore[union-attr]
            }
        )
        self.encoder = encoder
        for k, v in kwargs.items():
            self.set(k, v)

    def set(self, key: StreamKeyType, value: Any) -> "FutureStream":
        """Sets value into ffinfo. Calls can be chained."""
        k = Stream.key_handling(key)
        self.ffinfo[k] = value
        return self
