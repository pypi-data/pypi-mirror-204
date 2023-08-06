"""Defines FFMPEG-compliant encoder abstraction and manipulation facilities
"""
import logging
from pathlib import Path
import re

# import re
from typing import Any, Callable, Dict, List, Optional, Union

import yaml

from .encoder_spec import (
    ffmpeg_supported_encoders,
    get_codec_from_encoder,
    read_encoder_parameters,
)
from .utils import assertTrue, user_input, choose_from_list
from .enums import StreamType

LOG = logging.getLogger(__file__)
AVAILABLE_ENCODERS: Dict[Union[str, Path], List[str]] = {}


def is_available_encoder(encoder: str, ffmpeg: Union[str, Path]) -> bool:
    """Memoized function that check if encoder is available for given FFMPEG"""
    if ffmpeg not in AVAILABLE_ENCODERS:
        _available_encoders = []
        for _encoders in ffmpeg_supported_encoders(ffmpeg).values():
            _available_encoders.extend(_encoders)
        AVAILABLE_ENCODERS[ffmpeg] = _available_encoders
    return encoder in AVAILABLE_ENCODERS[ffmpeg]


class Encoder:
    """Validates encoder parameters and writes FFMPEG-compliant command parts
    Initialization requires calling ffmpeg to check for avaiability of given encoder

        h264_encoder = Encoder('libx264', threads=4)
        h264_encoder.set_parameters({
            'crf': 24,
            'preset': 'slow'
        })
    """

    def __init__(
        self,
        encoder: str,
        ffmpeg: Union[str, Path] = "ffmpeg",
        threads: Optional[int] = None,
    ) -> None:
        self.is_copy = encoder == "copy"
        assertTrue(
            self.is_copy or is_available_encoder(encoder, ffmpeg),
            "Encoder '{}' not available; available encoders: {}",
            encoder,
            AVAILABLE_ENCODERS[ffmpeg],
        )
        self.encoder = encoder
        self.parameters = {}
        self.spec = (
            read_encoder_parameters(self.encoder, ffmpeg) if encoder != "copy" else {}
        )
        self.codec = None if self.is_copy else get_codec_from_encoder(ffmpeg, encoder)
        self.stream_type = None if self.is_copy else self.spec["type"]
        # Set threads if supported
        if threads is not None:
            if "threads" not in self.spec.get("capabilities", {}):
                LOG.warning("Encoder '%s' doesn't support '-threads'", self.encoder)
            else:
                self.parameters["threads"] = threads

    @classmethod
    def build_interactively(cls, ffmpeg: Union[str, Path] = "ffmpeg") -> "Encoder":
        """Asks user to build encoder"""
        _type = StreamType.from_ffmpeg_code(
            user_input(
                "Encoder type [V=video,A=audio,S=subtitle]", accepted=["V", "A", "S"]
            )
        )
        _available_encoders = list(sorted(ffmpeg_supported_encoders(ffmpeg)[_type]))
        _encoder = choose_from_list(choices=_available_encoders)
        _encoder_info = read_encoder_parameters(_encoder, ffmpeg)
        _supports_threads = "threads" in _encoder_info.get("capabilities", {})
        _threads = None
        if _supports_threads:
            _threads = int(
                user_input(
                    "Threads",
                    accepted=lambda s: len(s) > 0 and s.isdigit(),
                    default="4",
                )
            )

        _supported_parameters = list(sorted(_encoder_info.get("options", {}).keys()))
        print(f"Valid parameters : {_supported_parameters}")
        _parameters = {}
        while True:
            _tmp = user_input(
                "Parameter (leave blank to stop)", accepted=lambda _: True, default=""
            ).strip()
            if len(_tmp) == 0:
                break
            _tmp2 = _tmp.split()
            if len(_tmp2) < 2:
                print(
                    f"Invalid input '{_tmp}' doesn't contain space-separated key-value"
                )
                continue
            _par, _val = _tmp.split()
            if _par not in _supported_parameters:
                print(f"Invalid parameter '{_par}'")
                continue
            _parameters[_par] = _val

        res = Encoder(encoder=_encoder, ffmpeg=ffmpeg, threads=_threads)
        res.set_parameters(**_parameters)

        _encoder_save_name = user_input(
            "Save encoder configuration with name (leve blank to skip)",
            accepted=lambda _: True,
        ).strip()
        if len(_encoder_save_name):
            res.save(_encoder_save_name, overwrite=True)

        return res

    def save(self, name: str, overwrite: bool) -> None:
        """Save to YAML file"""
        _param = dict(self.parameters)
        _threads = _param.pop("threads", None)
        _spec = {"encoder": self.encoder, "parameters": _param, "threads": _threads}
        _save_file = Encoder.yaml_file_path(name)
        if _save_file.exists() and not overwrite:
            LOG.info("Did not overwrite '%s'", _save_file)
            return
        with Encoder.yaml_file_path(name).open("w", encoding="utf8") as f:
            yaml.dump(_spec, f, encoding="utf8")

    @classmethod
    def load(cls, name: str, ffmpeg: Union[str, Path] = "ffmpeg") -> "Encoder":
        """Load from YAML file"""
        with Encoder.yaml_file_path(name).open("r", encoding="utf8") as f:
            _spec = yaml.safe_load(f)
            _encoder = Encoder(_spec["encoder"], ffmpeg, _spec["threads"])
            _encoder.set_parameters(**_spec["parameters"])
            return _encoder

    @staticmethod
    def yaml_file_path(name: str) -> Path:
        """Returns save YAML file path with given name"""
        return Path(__file__).with_suffix(f".{name}.yaml")

    @staticmethod
    def available_configs() -> Dict[str, Path]:
        """Returns list of save YAML files path that are available to be loaded"""
        extract_name_pattern = re.compile(r".+?\.(.+)\.yaml")
        _configs = {}
        for _item in Path(__file__).parent.glob(Path(__file__).stem + ".*.yaml"):
            if not _item.is_file():
                continue
            _match = re.match(extract_name_pattern, _item.name)
            if not _match:
                continue
            _configs[_match.group(1)] = _item

        return _configs

    def set_parameters(self, **kwargs) -> None:
        """Sets encoder-specific parameters. Check yaml files or run
        `ffmpeg --help encoder=<encoder>` for details."""
        available_parameters = {
            opt: spec.get("type") for opt, spec in self.spec.get("options", {}).items()
        }
        if "threads" in self.parameters:
            available_parameters["threads"] = int
        for p_name, p_value in kwargs.items():
            if p_name not in available_parameters:
                print(f"WARNING: Unknown parameter '{p_name}'")
                continue
            caster: Callable = available_parameters[p_name]
            try:
                self.parameters[p_name] = p_value if caster is None else caster(p_value)
            except ValueError as e:
                print(
                    f"WARNING: Couldn't cast value '{p_value}' to type {caster} for parameter {p_name} : {e}"
                )

    def to_command_parts(self) -> List[Any]:
        """FFMPEG-compatible CLI arguments for encoding stream"""
        command: List[Any] = []
        for k, v in self.parameters.items():
            command.append("-" + k)
            if v:
                command.append(v)
        return command
