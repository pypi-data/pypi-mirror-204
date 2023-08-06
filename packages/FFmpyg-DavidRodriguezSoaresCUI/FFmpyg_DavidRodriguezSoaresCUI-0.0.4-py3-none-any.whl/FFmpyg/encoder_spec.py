"""
Writes YAML-compliant description of given encoder by parsing FFMPEG help output

FFMPEG flag spec:
 D..... = Decoding supported
 .E.... = Encoding supported
 ..V... = Video codec
 ..A... = Audio codec
 ..S... = Subtitle codec
 ...I.. = Intra frame-only codec
 ....L. = Lossy compression
 .....S = Lossless compression
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .command import Command
from .enums import StreamType
from .utils import assertTrue

ENCODER_LINE = re.compile(r"\s+([AVS])[ADEILSV\.]{5} (\S+).*")
ENCODER_GENERAL_CAPABILITIES = re.compile(r"General capabilities: (.*)")
FFMPEG_CODEC = re.compile(r"\s*[ADEILSV\.]{6} (\S+).*")
FFMPEG_DESCRIPTION_VALUE_DEFAULT = re.compile(r"\(default (.+?)\)")
FFMPEG_DESCRIPTION_VALUE_RANGE = re.compile(r"\(from (.+?) to (.+?)\)")
FFMPEG_FLAGS = re.compile(r"[ADEILSV\.]{10}")
FFMPEG_OPTION = re.compile(r"\s+\-(\S+)\s+<(\S+)>\s+[ADEILSV\.]{10}(.*)")
FFMPEG_VALUE = re.compile(r"\s+(\S+)\s+(\S+)\s+[ADEILSV\.]{10}(.*)")
FFMPEG_VALUE_DEFAULT = re.compile(r"\s+default\s+[ADEILSV\.]{10} (.+)")
OPTION_TYPES = {
    "int": int,
    "boolean": bool,
    "float": float,
    "dictionary": dict,
}


def decode_ffmpeg_flag_stream_type(flags: List[str]) -> str:
    """Returns stream type as `video`, `audio`, `subtitle`"""
    if "V" in flags:
        return "ideo"
    return "audio" if "A" in flags else "subtitle"


def __execute_ffmpeg_command(command: List[Any]) -> str:
    """Executes command, validates returned stdout/stderr and returns stdout"""
    cmd = Command(command)
    stdX = cmd.execute()
    assertTrue(
        stdX["stderr"].startswith("ffmpeg version") and len(stdX["stdout"]) > 10,
        "Unexpected output when running '{}'; FFMPEG is not installed correctly or of an incompatible version",
        cmd,
    )
    return stdX["stdout"]


def get_codec_from_encoder(ffmpeg: Union[str, Path], encoder: str) -> str:
    """Read FFMPEG's supported encoders"""
    ffmpeg_stdout = __execute_ffmpeg_command([ffmpeg, "-codecs"])

    candidate_codecs = {
        codec_match.group(1)
        for codec_match in [
            re.match(FFMPEG_CODEC, line)
            for line in ffmpeg_stdout.splitlines()
            if encoder in line
        ]
        if codec_match
    }
    assertTrue(
        len(candidate_codecs) == 1,
        "Could not match a codec, found candidates: {}",
        candidate_codecs,
    )
    return candidate_codecs.pop()


def ffmpeg_supported_encoders(ffmpeg: Union[str, Path]) -> Dict[StreamType, List[str]]:
    """Read FFMPEG's supported encoders"""
    ffmpeg_stdout = __execute_ffmpeg_command([ffmpeg, "-encoders"])

    encoders = defaultdict(list)
    in_header = True
    for line in ffmpeg_stdout.splitlines():
        if in_header:
            if "------" in line:
                in_header = False
            continue
        encoder_match = re.match(ENCODER_LINE, line)
        if encoder_match:
            _stream_type = StreamType.from_ffmpeg_code(encoder_match.group(1))
            encoders[_stream_type].append(encoder_match.group(2))

    return encoders


def read_encoder_parameters(
    encoder: str, ffmpeg: Union[str, Path], type_as_str: bool = False
) -> dict:
    """Reads output of FFMPEG's help encoder message"""
    ffmpeg_stdout = __execute_ffmpeg_command([ffmpeg, "--help", f"encoder={encoder}"])

    flag_confs = set(re.findall(FFMPEG_FLAGS, ffmpeg_stdout))
    assertTrue(all("E" in flags for flags in flag_confs), "Not an encoder")
    stream_types = set(decode_ffmpeg_flag_stream_type(flags) for flags in flag_confs)
    assertTrue(
        len(stream_types) == 1,
        "Expected to find one stream type, found {}",
        stream_types,
    )
    stream_type = stream_types.pop()

    cap_match = re.search(ENCODER_GENERAL_CAPABILITIES, ffmpeg_stdout)
    capabilities: List[str] = []
    if cap_match:
        capabilities.extend(cap_match.group(1).strip().split())

    options_found = False
    options = {}
    last_option: Optional[str] = None
    for line in ffmpeg_stdout.splitlines():
        # Skip header
        if not options_found:
            if "Options:" in line:
                options_found = True
            continue

        # Skip empty lines
        if len(line.strip()) == 0:
            continue

        # Option entry
        option_line = re.match(FFMPEG_OPTION, line)
        if option_line:
            opt_parts = option_line.groups()
            opt_name = opt_parts[0]
            opt_type = OPTION_TYPES.get(opt_parts[1], str)
            options[opt_name] = {"type": opt_type.__name__ if type_as_str else opt_type}
            last_option = opt_name

            # Description
            if len(opt_parts) == 3:
                opt_descr = opt_parts[2].strip()
                if len(opt_descr) > 1:
                    options[opt_name]["description"] = opt_descr

                # Value range
                opt_range = re.search(FFMPEG_DESCRIPTION_VALUE_RANGE, opt_descr)
                if opt_range:
                    options[opt_name]["range"] = ":".join(opt_range.groups())

                # Value default
                opt_default = re.search(FFMPEG_DESCRIPTION_VALUE_DEFAULT, opt_descr)
                if opt_default:
                    options[opt_name]["default"] = opt_default.group(1)
            continue

        # Option value documentation
        option_value = re.match(FFMPEG_VALUE, line)
        if option_value:
            option_value_parts = option_value.groups()
            option_value_label: str = option_value_parts[0]
            option_value_value: str = option_value_parts[1]

            options[last_option].setdefault("values", {})
            options[last_option]["values"][option_value_label] = {  # type: ignore[index]
                "value": option_value_value
            }

            # Description
            if len(opt_parts) == 3:
                option_value_descr = option_value_parts[2].strip()
                if len(option_value_descr) > 1:
                    options[last_option]["values"][option_value_label][  # type: ignore[index]
                        "description"
                    ] = option_value_descr
            continue

        # Option default value documentation
        option_value = re.match(FFMPEG_VALUE_DEFAULT, line)
        if option_value:
            option_value_parts = option_value.groups()
            option_value_descr: str = option_value_parts[0]  # type: ignore[no-redef]
            if len(option_value_descr) > 1:
                options[last_option].setdefault("values", {})
                options[last_option]["values"]["default"] = {  # type: ignore[index]
                    "description": option_value_descr
                }
            continue

        raise ValueError(f"line '{line}' couldn't be parsed !")

    return {"capabilities": capabilities, "type": stream_type, "options": options}
