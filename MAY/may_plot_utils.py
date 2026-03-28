from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "MAY_2024_Master_Cleaned.csv"
OUT_DIR = BASE_DIR
FINAL_PLOTS_DIR = BASE_DIR / "Final Plots"

EVENT_START = pd.Timestamp("2024-05-10 00:00")
EVENT_END = pd.Timestamp("2024-05-13 23:59")

STORM_PHASES = {
    "Pre-storm Phase": {
        "start": "2024-05-10 00:00",
        "end": "2024-05-10 17:00",
        "color": "#FDDFDB",
        "alpha": 0.55,
    },
    "Main Phase": {
        "start": "2024-05-10 17:00",
        "end": "2024-05-11 10:00",
        "color": "#FBF3D1",
        "alpha": 0.60,
    },
    "Recovery Phase": {
        "start": "2024-05-11 10:00",
        "end": "2024-05-13 23:59",
        "color": "#EDF6F9",
        "alpha": 0.75,
    },
}

OMNI_FILL_VALUES = {
    "Field magnitude average, nT": 9999.99,
    "BX, nT (GSE, GSM)": 9999.99,
    "BY, nT (GSM)": 9999.99,
    "BZ, nT (GSM)": 9999.99,
    "Speed, km/s": 99999.9,
    "Proton Density, n/cc": 999.999,
    "Flow pressure, nPa": 99.9999,
    "Electric field, mV/m": 999.99,
    "AE-index, nT": 9999.0,
    "SYM/H, nT": 9999.0,
    "ASY/H, nT": 9999.0,
}


def apply_matplotlib_theme() -> None:
    """Apply a single publication style across all MAY scripts."""
    plt.rcParams["font.family"] = "Times New Roman"


def load_master_data(
    path: Path | str = DATA_PATH,
    *,
    replace_omni_fill_values: bool = True,
    mask_non_positive_flux: bool = False,
) -> pd.DataFrame:
    """Load the cleaned May master CSV and apply optional masking rules."""
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = "datetime"
    df.index = pd.to_datetime(df.index, utc=False)

    if replace_omni_fill_values:
        for column, fill_value in OMNI_FILL_VALUES.items():
            if column in df.columns:
                threshold = fill_value * 0.99
                df[column] = df[column].where(df[column] < threshold, np.nan)

    if mask_non_positive_flux:
        flux_cols = [
            c
            for c in df.columns
            if c.startswith(("Electron_Flux_", "Proton_Flux_", "Alpha_Flux_"))
        ]
        df[flux_cols] = df[flux_cols].mask(df[flux_cols] <= 0)

    return df


def label_with_units(name: str, units: str) -> str:
    """Use a two-line y-label format: name on top, units below."""
    return f"{name}\n({units})"


def add_panel_tag(ax, tag: str, x: float = 0.0, y: float = 1.03) -> None:
    """Place panel tags just above the upper-left corner of the plot box."""
    ax.text(
        x,
        y,
        tag,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        ha="left",
        va="bottom",
        clip_on=False,
        zorder=6,
    )


def apply_storm_shading(
    ax,
    phases: dict,
    *,
    show_labels: bool = False,
    phase_label_y: float = 0.97,
) -> None:
    """Draw storm-phase background spans, with optional per-panel text labels."""
    for label, props in phases.items():
        t0 = pd.Timestamp(props["start"])
        t1 = pd.Timestamp(props["end"])
        ax.axvspan(
            t0,
            t1,
            facecolor=props["color"],
            alpha=props["alpha"],
            edgecolor="none",
            zorder=0,
        )

        if show_labels:
            midpoint = t0 + (t1 - t0) / 2
            ax.text(
                midpoint,
                phase_label_y,
                label,
                ha="center",
                va="top",
                fontsize=8,
                fontstyle="italic",
                color="dimgray",
                transform=ax.get_xaxis_transform(),
                zorder=5,
            )


def build_phase_legend_handles(
    phases: dict,
    *,
    label_overrides: dict[str, str] | None = None,
) -> list[mpatches.Patch]:
    """Build horizontal phase legend patches from a phase dictionary."""
    handles = []
    for label, props in phases.items():
        display_label = label_overrides.get(label, label) if label_overrides else label
        handles.append(
            mpatches.Patch(
                facecolor=props["color"],
                edgecolor="gray",
                linewidth=0.5,
                label=display_label,
            )
        )
    return handles


def style_axes(
    ax,
    ylabel: str,
    *,
    ycolor: str = "black",
    label_fontsize: int = 11,
    tick_fontsize: int = 9,
    label_pad: int = 12,
    show_log_minor_ticks: bool = False,
    show_log_minor_grid: bool = False,
) -> None:
    """Apply consistent panel style used across all MAY figures."""
    ax.set_ylabel(ylabel, fontsize=label_fontsize, color=ycolor, labelpad=label_pad)
    ax.tick_params(axis="y", labelsize=tick_fontsize, colors=ycolor, pad=7)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_edgecolor("dimgray")

    ax.set_facecolor("white")
    ax.tick_params(axis="x", which="both", direction="in", top=True, bottom=True)
    ax.tick_params(axis="y", which="both", direction="in", left=True, right=True)
    ax.tick_params(axis="y", which="major", length=6, width=0.9)
    ax.tick_params(axis="y", which="minor", length=3, width=0.8, left=True, right=False)

    ax.grid(axis="x", which="major", linestyle="--", linewidth=0.4, color="lightgray", zorder=0)
    ax.grid(axis="y", which="major", linestyle=":", linewidth=0.3, color="lightgray", zorder=0)

    if show_log_minor_ticks:
        ax.yaxis.set_minor_locator(mticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())

    if show_log_minor_grid:
        ax.grid(
            axis="y",
            which="minor",
            linestyle=":",
            linewidth=0.2,
            color="lightgray",
            zorder=0,
            alpha=0.5,
        )


def format_shared_xaxis(
    axes: Sequence,
    *,
    t_start: pd.Timestamp = EVENT_START,
    t_end: pd.Timestamp = EVENT_END,
    xlabel: str = "Universal Time ( UT )",
    tick_fontsize: int = 9,
    label_fontsize: int = 11,
    label_pad: int = 12,
    draw_day_separators: bool = True,
) -> None:
    """Apply unified UTC time formatting to a stacked subplot layout."""

    def format_day(x: float, _pos: int) -> str:
        dt = mdates.num2date(x)
        return dt.strftime("%b ") + str(dt.day)

    day_locator = mdates.DayLocator(interval=1)
    hour_locator = mdates.HourLocator(byhour=[0, 6, 12, 18])
    day_formatter = mticker.FuncFormatter(format_day)

    day_lines = pd.date_range(t_start.normalize(), t_end.normalize(), freq="D")

    for idx, ax in enumerate(axes):
        ax.set_xlim(t_start, t_end)
        ax.xaxis.set_major_locator(day_locator)
        ax.xaxis.set_minor_locator(hour_locator)
        ax.tick_params(axis="x", which="minor", length=3, color="gray")

        if draw_day_separators:
            for day in day_lines:
                ax.axvline(day, color="lightgray", linewidth=0.7, linestyle="-", zorder=0)

        if idx < len(axes) - 1:
            plt.setp(ax.get_xticklabels(), visible=False)
        else:
            ax.xaxis.set_major_formatter(day_formatter)
            ax.tick_params(axis="x", labelsize=tick_fontsize)
            ax.set_xlabel(xlabel, fontsize=label_fontsize, labelpad=label_pad)


def ensure_directory(path: Path | str) -> Path:
    """Create a directory if needed and return it as Path."""
    resolved = Path(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved
