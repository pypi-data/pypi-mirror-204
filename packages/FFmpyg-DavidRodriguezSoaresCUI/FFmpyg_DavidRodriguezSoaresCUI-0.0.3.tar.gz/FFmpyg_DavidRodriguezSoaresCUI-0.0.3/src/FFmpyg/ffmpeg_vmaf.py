"""
FFmpeg VMAF lib
===============

VMAF is a metric for the perceived quality of images and videos,
and this module is all about using FFmpeg to retrieve VMAF information
"""

import json
import logging
import math
from pathlib import Path
from typing import Dict, List, Union

import numpy as np
from DRSlib.utils import get_temporary_dir_name
from matplotlib import pyplot as plt

from .enums import FfprobeInfoKey, StreamType
from .ffile import MediaFile, StreamCriteria
from .ffmpeg_command import (
    FfmpegInput,
    FfmpegOptions,
    FilterComplexNode,
    build_ffmpeg_command,
)
from .ffmpeg_lib import assert_ffmpeg_supports_feature
from .utils import assertTrue
from .virtualfs import WorkingDirectory

LOG = logging.getLogger(__file__)
FFMPEG_FEATURE_VMAF = "libvmaf"


def assert_ffmpeg_supports_vmaf(ffmpeg: Union[str, Path]) -> None:
    """Raises exception on FFmpeg not being callable or not having VMAF support"""
    assert_ffmpeg_supports_feature(ffmpeg, FFMPEG_FEATURE_VMAF)


class VmafReport:
    """Object representing a VMAF computation, able to be"""

    FFMPEG_OPTIONS = FfmpegOptions(loglevel="warning", hide_banner=True, no_stats=True)
    VMAF_LOW = lambda frames: np.percentile(frames, 5) < 50
    FFMPEG_DRAW_TEXT = (
        lambda text: f"drawtext=text='{text}':fontfile=/Windows/Fonts/Arial.ttf:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2"
    )

    def __init__(
        self,
        reference: MediaFile,
        other: MediaFile,
        threads: int = 0,
        ffmpeg: Union[str, Path] = "ffmpeg",
    ) -> None:
        assert_ffmpeg_supports_vmaf(ffmpeg)
        self.ffmpeg = ffmpeg
        self.stat_file_name = f"{get_temporary_dir_name(reference.path)}-{get_temporary_dir_name(other.path)}.vmaf.json"
        self.plot_file_path = other.path.with_suffix(".vmaf_plot.svg")
        self.bad_frame_pattern = other.path.stem + "_frame%d.png"
        self.inputs = [FfmpegInput(i, fix_fps=24) for i in (reference, other)]
        self.vmaf_threads = threads if threads == 0 else max(1, threads - 1)
        self._stats: Dict[int, float]
        self._frames: np.ndarray
        self.working_directory = WorkingDirectory(reference.path)
        # checking video streams
        ref_v, other_v = reference.get_streams(
            StreamCriteria(StreamType.VIDEO, None)
        ), other.get_streams(StreamCriteria(StreamType.VIDEO, None))
        assertTrue(
            len(ref_v) == 1 and len(other_v) == 1,
            "Input videos have noncompliant number of video streams (ref={}, other={})",
            len(ref_v),
            len(other_v),
        )
        self.resize_ref = (
            ref_v[0].get(FfprobeInfoKey.HEIGHT) != 1080
            or ref_v[0].get(FfprobeInfoKey.WIDTH) != 1920
        )
        self.resize_other = (
            other_v[0].get(FfprobeInfoKey.HEIGHT) != 1080
            or other_v[0].get(FfprobeInfoKey.WIDTH) != 1920
        )

    @property
    def stats(self) -> dict:
        """Lazy property"""
        if self._frames is None:
            self.load_stats()
        return {
            "min": np.min(self._frames),
            "max": np.max(self._frames),
            "mean": np.mean(self._frames),
            "1%": np.percentile(self._frames, 1),
        }

    @property
    def frames(self) -> np.ndarray:
        """Lazy property; Warning: should be considered as unsorted; only use for stats"""
        if self._frames is None:
            self.load_stats()
        return self._frames

    def __str__(self) -> str:
        return (
            f"<VmafReport: inputs={[str(i) for i in self.inputs]} stats={self.stats}>"
        )

    def vmaf_percentile(self, percentile: int) -> float:
        """Computes nth percentile of vmaf values"""
        return np.percentile(self.frames, percentile)

    @property
    def stat_file_path(self) -> Path:
        """Returns stat file's path (in working directory) relative to cwd"""
        return self.working_directory.get_file(
            self.stat_file_name, relative_to_cwd=True
        )

    def load_stats(self, compatibility_mode: bool = False) -> None:
        """Execute and parse command, then load stats"""
        stat_file = self.stat_file_path
        if not (stat_file.exists() and stat_file.is_file()):
            # Compute VMAF stats
            LOG.debug(
                "Computing vmaf%s",
                " (compatibility mode)" if compatibility_mode else "",
            )
            vmaf_filter_complex = FilterComplexNode(
                inputs=[
                    FilterComplexNode(inputs=["0:v:0"], complex_filter="scale=hd1080")
                    if self.resize_ref
                    else "0:v:0",
                    FilterComplexNode(inputs=["1:v:0"], complex_filter="scale=hd1080")
                    if self.resize_ref
                    else "1:v:0",
                ],
                complex_filter="libvmaf=eof_action=endall"
                + (f":n_threads={self.vmaf_threads}" if self.vmaf_threads > 0 else "")
                + f":log_fmt=json:log_path={stat_file.as_posix()}",
            )
            cmd, _ = build_ffmpeg_command(
                inputs=self.inputs,
                ffmpeg=self.ffmpeg,
                options=self.__class__.FFMPEG_OPTIONS,
                filter_complex=vmaf_filter_complex,
                extra=[
                    "-vsync" if compatibility_mode else "-fps_mode",
                    "drop",
                    "-f",
                    "null",
                ],
            )
            LOG.debug("Executing command: %s", cmd.to_script())
            try:
                stdX = cmd.execute()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"Most likely wrong ffmpeg call '{self.ffmpeg}'"
                ) from e
            stderr = stdX["stderr"]
            if len(stderr) > 0 and "Unrecognized option 'fps_mode'" in stderr:
                LOG.info(
                    "This build of ffmpeg doesn't support 'fps_mode'. Retrying in compatibility mode .."
                )
                self.load_stats(compatibility_mode=True)
                return

            LOG.debug("Result: %s", stdX)
            LOG.info("VMAF computation completed; saved stats to file %s", stat_file)

        # Parsing stat file
        if not stat_file.is_file():
            raise IOError(
                f"Something went wrong, temporary file {stat_file} is missing."
            )

        self._stats = {
            frame["frameNum"]: frame["metrics"]["vmaf"]
            for frame in json.loads(stat_file.read_text(encoding="utf8"))["frames"]
        }
        self._frames = np.fromiter(self._stats.values(), dtype=float)
        if self.__class__.VMAF_LOW(self._frames):
            LOG.warning(
                "Very low VMAF values found. This may be a sign that VMAF computation encountered a problem, typically desynchronization. If so, please submit a bug report with attached files."
            )

    def export_plot(self) -> None:
        """Reads JSON-formatted vmaf stats file and write histogram plots. Output file is next to `other` file."""
        stats = self.stats
        if stats is None:
            LOG.warning(
                "Could not export plot because there was an error loading stats"
            )
            return

        s_min, s_max, s_1, s_25, s_mean = (
            stats["min"],
            stats["max"],
            stats["1%"],
            self.vmaf_percentile(25),
            stats["mean"],
        )
        l_1, l_25, l_mean = (
            f"1% = {s_1:0.1f}",
            f"25% = {s_25:0.1f}",
            f"mean = {s_mean:0.1f}",
        )
        fig, (ax1, ax2) = plt.subplots(nrows=2)
        fig.subplots_adjust(hspace=0.5)

        # Top figure : VMAF value plot over time
        ax1.plot(self.frames, linewidth=0.65)
        ax1.set_xlabel("frames")
        ax1.set_ylabel("VMAF value")
        ax1.set_title("VMAF frame values")
        ax1.set_ylim(0 if stats["1%"] < 80 else 80, 101)
        ax1.axhline(y=s_1, color="k", label=l_1)
        ax1.axhline(y=s_25, color="g", label=l_25)
        ax1.axhline(y=s_mean, color="r", label=l_mean)
        # ax1.legend()
        ax1.grid(True)

        # Bottom figure : Histogram or VMAF values
        _bins = [x / 2 for x in range(math.floor(s_min) * 2, math.ceil(s_max) * 2 + 1)]
        ax2.hist(self.frames, bins=_bins, color="b")
        ax2.set_xlabel("VMAF value")
        ax2.set_ylabel("frames")
        ax2.set_title("Histogram of VMAF frame values")
        ax2.set_xlim(0 if s_1 < 80 else 80, 101)
        ax2.set_yscale("log")
        ax2.axvline(x=s_1, color="k", label=l_1)
        ax2.axvline(x=s_25, color="g", label=l_25)
        ax2.axvline(x=s_mean, color="r", label=l_mean)
        ax2.legend()
        ax2.grid(True)

        # Saving figure to file
        if self.plot_file_path.is_file():
            print(f"Overwriting VMAF stat plot '{self.plot_file_path}'")
        fig.savefig(self.plot_file_path)
        fig.clf()

    def lowest_vmaf_frames(self, n: int) -> List[int]:
        """Returns a sorted list of the n lowest vmaf value frames"""
        idx = np.argpartition(self.frames, n)
        low_frames = list(sorted(idx[:n]))
        LOG.debug(
            "%s lowest VMAF value frames are %s with values in [%s, %s]",
            n,
            low_frames,
            np.min(self.frames[idx[:n]]),
            np.max(self.frames[idx[:n]]),
        )
        return low_frames

    def extract_bad_frames(self, n: int, compatibility_mode: bool = False) -> None:
        """Extracts n lowest vmaf value frames, with vertically stacked ori/other"""
        low_frames = self.lowest_vmaf_frames(n)
        low_frame_select = "+".join(f"eq(n\\,{low_frame})" for low_frame in low_frames)
        drawText = self.__class__.FFMPEG_DRAW_TEXT
        _filter_complex = FilterComplexNode(
            inputs=[
                FilterComplexNode(
                    inputs=["0:v:0"], complex_filter=drawText("reference")
                ),
                FilterComplexNode(inputs=["1:v:0"], complex_filter=drawText("encoded")),
            ],
            complex_filter="vstack=inputs=2",
        ).add_filter(f"select='{low_frame_select}'")
        cmd, _ = build_ffmpeg_command(
            inputs=self.inputs,
            stream_mapping=None,
            output=self.bad_frame_pattern,
            ffmpeg=self.ffmpeg,
            options=self.__class__.FFMPEG_OPTIONS,
            filter_complex=_filter_complex,
            extra=["-vsync" if compatibility_mode else "-fps_mode", "drop"],
        )
        LOG.debug("extract bad frame command: %s", cmd.to_script())
        stdX = cmd.execute()
        LOG.debug("stdX=%s", stdX)
        cwd = Path(".")
        for i in range(n):
            frame_path = cwd / self.bad_frame_pattern.replace("%d", str(i + 1))
            if not frame_path.is_file():
                LOG.warning(
                    "Could not find extracted frame %s at location %s", i, frame_path
                )
            else:
                # Rename file with more info
                _frame = low_frames[i]
                new_frame_path = self.working_directory.get_file(
                    self.bad_frame_pattern.replace(
                        "%d", f"{_frame}_(VMAF={self._stats[_frame]})"
                    )
                )
                if new_frame_path.is_file():
                    LOG.warning(
                        "Could not rename %s -> %s : target exists",
                        frame_path,
                        new_frame_path,
                    )
                else:
                    frame_path.rename(new_frame_path)
