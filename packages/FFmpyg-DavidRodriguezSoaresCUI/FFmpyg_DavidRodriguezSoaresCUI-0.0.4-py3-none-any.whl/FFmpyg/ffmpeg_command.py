""" Abstracts away some of the complexities about crafting a complex command
for FFMPEG, specifically regarding inputs, options, filters, stream mapping,
encoders and more
"""
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .command import Command
from .exceptions import FilterComputationFailed
from .ffile import (
    FfprobeInfoKey,
    FutureMediaFile,
    FutureStream,
    MediaFile,
    Stream,
    StreamCriteria,
    StreamType,
)
from .ffmpeg_encoder import Encoder
from .utils import assertTrue, random_words

LOG = logging.getLogger(__file__)


class FfmpegOptions:
    """Represents FFMPEG global options"""

    ACCEPTED_VALUES: Dict[str, set] = {
        "loglevel": {
            "quiet",
            "panic",
            "fatal",
            "error",
            "warning",
            "info",
            "verbose",
            "debug",
        },
        "hide_banner": {True, False},
        "y_overwrite": {True, False},
        "n_overwrite": {True, False},
        "nostats": {True, False},
    }

    def __init__(
        self,
        loglevel: str = "info",
        hide_banner: bool = False,
        y_overwrite: bool = False,
        n_overwrite: bool = False,
        no_stats: bool = False,
        more: Optional[List[str]] = None,
    ) -> None:
        # fmt: off
        self.cfg = {
            "loglevel"    : FfmpegOptions.assertValueInRange("loglevel", loglevel),
            "hide_banner" : FfmpegOptions.assertValueInRange("hide_banner", hide_banner),
            "y"           : FfmpegOptions.assertValueInRange("y_overwrite", y_overwrite),
            "n"           : FfmpegOptions.assertValueInRange("n_overwrite", n_overwrite),
            "nostats"     : FfmpegOptions.assertValueInRange("nostats", no_stats),
        }
        # fmt: on
        self._more = [] if more is None else more

    @classmethod
    def assertValueInRange(cls, name: str, value: Any) -> Any:
        """Ensures values passed are valid"""
        assertTrue(
            name in cls.ACCEPTED_VALUES,
            "No entry '{}' in FfmpegOptions.ACCEPTED_VALUES !",
            name,
        )
        assertTrue(
            value in cls.ACCEPTED_VALUES[name],
            "Value '{}' not in {} !",
            value,
            cls.ACCEPTED_VALUES[name],
        )
        return value

    def to_command_part(self) -> List[str]:
        """Returns list-based command"""
        cmd = []
        for key, val in self.cfg.items():
            if isinstance(val, bool):
                if val:
                    cmd.append("-" + key)
            else:
                cmd.append("-" + key)
                cmd.append(val)

        cmd.extend(self._more)
        return cmd


class FfmpegInput:
    """Represents an input for FFMPEG, with its modifiers"""

    def __init__(
        self,
        file: MediaFile,
        fix_fps: Union[int, float, None] = None,
        more: Optional[List[str]] = None,
    ) -> None:
        """Expects a file and modifiers; for now only fps fixing with"""
        self._file = file
        assertTrue(
            fix_fps is None or (isinstance(fix_fps, (int, float)) and fix_fps > 0),
            "Invalid value for fix_fps '{}' must be a int or float and be a non-zero positive value !",
            fix_fps,
        )
        self._fix_fps = fix_fps
        self._more = [] if more is None else more

    @property
    def path(self) -> Path:
        """Return path associated with input file"""
        return self._file.path

    def __str__(self) -> str:
        return f"<FfmpegInput: file={self.path}>"

    def to_command_part(self) -> List[Any]:
        """Returns Command object equivalent to self"""
        cmd: List[Any] = [] if self._fix_fps is None else ["-r", self._fix_fps]
        cmd.extend(self._more)
        cmd.append("-i")
        cmd.append(self._file.path)
        return cmd

    def contains_stream(self, stream: Union[Stream, FutureStream]) -> Union[int, None]:
        """Checks if stream is in this file"""
        return self._file.streams[stream.idx] == stream


class FilterComplexNode:
    """Makes writing FFMPEG complex filter programatically simpler

    Each node represents a filter (ex: scale, drawText, vstack, select, ..)
    """

    NAME_LEN = 3

    def __init__(
        self, inputs: List[Union["FilterComplexNode", str]], complex_filter: str
    ) -> None:
        self.inputs = inputs
        self.complex_filter = complex_filter
        self.next: Optional[FilterComplexNode] = None

    def add_filter(self, complex_filter: str) -> "FilterComplexNode":
        """Add filter step"""
        next_node = FilterComplexNode(inputs=[self], complex_filter=complex_filter)
        self.next = next_node
        return next_node

    def compute_filter(self, **kwargs) -> Union[str, None]:
        """This method should be called on last node to produce the whole filter
        This method uses recursion to first "descend" the graph to the last node, then
        use DFS to explore all nodes ("ascent") and produce filter.
        Note: During second step "ascent", returns None
        """
        # Case: descent => go to next
        if self.next is not None and not kwargs:
            return self.next.compute_filter()

        # Case: last node => switching to ascent and computing filter
        if self.next is None and not kwargs:
            used_names: Set[str] = set()
            _inputs = random_words(
                n=len(self.inputs),
                length=FilterComplexNode.NAME_LEN,
                used_words=used_names,
            )
            filters = [self.to_string(inputs=_inputs)]
            for idx, _in in enumerate(self.inputs):
                if isinstance(_in, FilterComplexNode):
                    _in.compute_filter(
                        filters=filters, used_names=used_names, output=_inputs[idx]
                    )
            return ";".join(reversed(filters))

        # Case: ascent => propagate
        _inputs = random_words(
            n=len(self.inputs),
            length=FilterComplexNode.NAME_LEN,
            used_words=kwargs["used_names"],
        )
        kwargs["filters"].append(
            self.to_string(inputs=_inputs, output=kwargs["output"])
        )
        for idx, _in in enumerate(self.inputs):
            if isinstance(_in, FilterComplexNode):
                _in.compute_filter(
                    filters=kwargs["filters"],
                    used_names=kwargs["used_names"],
                    output=_inputs[idx],
                )
        return None

    @staticmethod
    def make_tags(tags: List[str]) -> str:
        """joining with brackets"""
        return "".join(f"[{tag}]" for tag in tags)

    def to_string(self, inputs: List[str], output: Optional[str] = None) -> str:
        """FFMPEG-compatible representation"""
        _inputs = [
            _in if isinstance(_in, str) else inputs[idx]
            for idx, _in in enumerate(self.inputs)
        ]  # get actual self.inputs instead of generated if possible
        return (
            FilterComplexNode.make_tags(_inputs)
            + self.complex_filter
            + ("" if output is None else FilterComplexNode.make_tags([output]))
        )


def build_ffmpeg_command(
    inputs: List[FfmpegInput],
    ffmpeg: Union[str, Path] = "ffmpeg",
    options: Optional[FfmpegOptions] = None,
    output: Optional[Union[str, Path]] = None,
    stream_mapping: Optional[Dict[Stream, FutureStream]] = None,
    filter_complex: Optional[FilterComplexNode] = None,
    extra: Optional[list] = None,
) -> Tuple[Command, Optional[FutureMediaFile]]:
    """Builds FFMPEG-compatible command with given inputs, mapping, output file and options
    Returns command and output file as FutureMediaFile

    `ffmpeg` : executable as callable in a terminal
    `inputs` : input files and closely related parameters
    `options` : (optional) "global" FFMPEG parameters
    `output` : (optional) output file path
    `stream_mapping` : (optional) input-output stream mapping
    `filter_complex` : (optional) filter_complex
    `extra` : (optional) additional parameters
    """

    cmd = [ffmpeg]
    if options is not None:
        cmd.extend(options.to_command_part())
    for _input in inputs:
        cmd.extend(_input.to_command_part())

    out_file = FutureMediaFile(output) if isinstance(output, Path) else None

    # Compute mapping
    if stream_mapping is not None:
        in_stream_sorted_by_out_stream_idx = sorted(
            stream_mapping.keys(), key=lambda in_stream: stream_mapping[in_stream].idx  # type: ignore[index]
        )
        for in_stream in in_stream_sorted_by_out_stream_idx:
            out_stream = stream_mapping[in_stream]
            input_file_idx = min(
                idx
                for idx, i in enumerate(inputs)
                if i.contains_stream(in_stream) and idx is not None
            )
            stream_command = ["-map", f"{input_file_idx}:{in_stream.idx}"]
            if out_stream.encoder is not None:
                stream_command.extend(
                    [f"-c:{out_stream.idx}", out_stream.encoder.encoder]
                )
                stream_command.extend(out_stream.encoder.to_command_parts())
            cmd.extend(stream_command)
            if out_file is not None:
                out_file.add_stream(out_stream)

    if filter_complex is not None:
        actual_filter = filter_complex.compute_filter()
        if actual_filter is None:
            raise FilterComputationFailed(filter_complex)
        cmd.extend(["-filter_complex", actual_filter])

    if extra is not None:
        cmd.extend(extra)

    cmd.append("-" if output is None else output)

    return Command(cmd), out_file


def build_mapping(
    _input: MediaFile, rules: Dict[StreamCriteria, Encoder]
) -> Dict[Stream, FutureStream]:
    """Builds stream mapping from encoder rules"""

    def is_default_criteria(criteria: StreamCriteria) -> bool:
        return criteria.codec is None and criteria.codec_type is None

    # Ensure there is no more than one default criteria
    default_rules = [
        criteria for criteria in rules.keys() if is_default_criteria(criteria)
    ]
    assertTrue(
        len(default_rules) < 2,
        "More than one default rule is defined: {}",
        default_rules,
    )

    # Map streams by index in input file
    mapped_streams: Dict[int, StreamCriteria] = {}
    # Note: default criteria are visited last
    for stream_criteria in sorted(
        rules.keys(), key=lambda c: 1 if is_default_criteria(c) else 0
    ):
        before_count = len(mapped_streams)
        for in_stream in _input.get_streams(stream_criteria):
            if in_stream.idx in mapped_streams:
                if not is_default_criteria(stream_criteria):
                    LOG.warning(
                        "Warning: Stream %s matched non-default criteria %s but already matched previous criteria %s !",
                        in_stream,
                        stream_criteria,
                        mapped_streams[in_stream.idx],
                    )
                continue
            mapped_streams[in_stream.idx] = stream_criteria
            LOG.debug("Stream %s matched criteria %s", in_stream, stream_criteria)

        if before_count == len(mapped_streams):
            LOG.warning(
                "Info: criteria {stream_criteria} didn't match any stream for file {_input}"
            )
            sys.exit()

    mapping = {}
    for out_idx, in_idx in enumerate(sorted(mapped_streams.keys())):
        in_stream = _input.streams[in_idx]
        matched_criteria = mapped_streams[in_idx]
        encoder = rules[matched_criteria]
        codec = (
            in_stream.get(FfprobeInfoKey.CODEC) if encoder.is_copy else encoder.codec
        )
        stream_type = StreamType(in_stream.get(FfprobeInfoKey.STREAM_TYPE))
        mapping[in_stream] = FutureStream(
            index=out_idx, codec=codec, stream_type=stream_type, encoder=encoder
        )

    return mapping
