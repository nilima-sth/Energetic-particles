from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from may_plot_utils import (
    DATA_PATH,
    OUT_DIR,
    STORM_PHASES,
    EVENT_START,
    EVENT_END,
    add_panel_tag,
    apply_matplotlib_theme,
    apply_storm_shading,
    build_phase_legend_handles,
    format_shared_xaxis,
    label_with_units,
    load_master_data,
    style_axes,
)

apply_matplotlib_theme()

FIGURE_DPI = 300
FIGURE_WIDTH = 12
FIGURE1_HEIGHT = 12
FIGURE2_HEIGHT = 9
COMBINED_HEIGHT = 20

LABEL_FONTSIZE = 11
TICK_FONTSIZE = 9
LABEL_PAD = 14

COL_B = "Field magnitude average, nT"
COL_BX = "BX, nT (GSE, GSM)"
COL_BY = "BY, nT (GSM)"
COL_BZ = "BZ, nT (GSM)"
COL_SPEED = "Speed, km/s"
COL_DENSITY = "Proton Density, n/cc"
COL_PDYN = "Flow pressure, nPa"
COL_EFIELD = "Electric field, mV/m"
COL_AE = "AE-index, nT"
COL_SYMH = "SYM/H, nT"
COL_ASYH = "ASY/H, nT"


def _add_phase_header_legend(fig: plt.Figure, *, y: float, pre_label: str = "Pre-storm Phase") -> None:
    label_overrides = {"Pre-storm Phase": pre_label}
    phase_handles = build_phase_legend_handles(STORM_PHASES, label_overrides=label_overrides)
    fig.legend(
        handles=phase_handles,
        loc="upper right",
        bbox_to_anchor=(0.985, y),
        ncol=3,
        frameon=False,
        fontsize=8,
        handlelength=1.4,
        columnspacing=1.0,
    )


def plot_figure1(df: pd.DataFrame, out_dir: Path | str = OUT_DIR) -> None:
    fig, axes = plt.subplots(4, 1, figsize=(FIGURE_WIDTH, FIGURE1_HEIGHT), sharex=True)
    fig.patch.set_facecolor("white")

    # (a) Magnetic field components
    ax = axes[0]
    ax.plot(df.index, df[COL_B], color="black", lw=1.2, label=r"$|B|$")
    ax.plot(df.index, df[COL_BX], color="royalblue", lw=0.9, label=r"$B_x$")
    ax.plot(df.index, df[COL_BY], color="darkorange", lw=0.9, label=r"$B_y$")
    ax.plot(df.index, df[COL_BZ], color="crimson", lw=1.0, label=r"$B_z$")
    ax.axhline(0, color="gray", lw=0.6, linestyle="--")
    style_axes(
        ax,
        label_with_units("Magnetic Field", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(a)")
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(0.995, 0.98),
        fontsize=8,
        ncol=4,
        frameon=False,
        borderaxespad=0.1,
    )

    # (b) Solar wind speed
    ax = axes[1]
    ax.plot(df.index, df[COL_SPEED], color="seagreen", lw=1.0, label=r"$V_{sw}$")
    style_axes(
        ax,
        label_with_units("Speed", r"km s$^{-1}$"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(b)")
    ax.legend(loc="upper right", fontsize=8, frameon=False)

    # (c) Proton density + dynamic pressure
    ax = axes[2]
    ax2 = ax.twinx()
    density_lines = ax.plot(df.index, df[COL_DENSITY], color="steelblue", lw=0.95, label=r"$n_p$")
    pressure_lines = ax2.plot(df.index, df[COL_PDYN], color="firebrick", lw=0.9, label=r"$P_{dyn}$")

    style_axes(
        ax,
        label_with_units("Density", r"cm$^{-3}$"),
        ycolor="steelblue",
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    style_axes(
        ax2,
        label_with_units("Flow Pressure", "nPa"),
        ycolor="firebrick",
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    ax2.spines["top"].set_visible(False)

    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(c)")
    combined_lines = density_lines + pressure_lines
    ax.legend(combined_lines, [line.get_label() for line in combined_lines], loc="upper right", fontsize=8, frameon=False)

    # (d) Interplanetary electric field
    ax = axes[3]
    ax.plot(df.index, df[COL_EFIELD], color="saddlebrown", lw=0.95, label=r"$E_y$")
    ax.axhline(0, color="gray", lw=0.6, linestyle="--")
    style_axes(
        ax,
        label_with_units("Electric Field", r"mV m$^{-1}$"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(d)")
    ax.legend(loc="upper right", fontsize=8, frameon=False)

    format_shared_xaxis(
        list(axes),
        t_start=EVENT_START,
        t_end=EVENT_END,
        xlabel="Universal Time ( UT )",
        tick_fontsize=TICK_FONTSIZE,
        label_fontsize=LABEL_FONTSIZE,
        label_pad=LABEL_PAD,
    )

    fig.suptitle(
        "Geomagnetic Superstorm: May 10-13, 2024",
        fontsize=12,
        fontweight="bold",
        y=0.992,
    )
    _add_phase_header_legend(fig, y=0.972)

    fig.align_ylabels(axes)
    fig.subplots_adjust(left=0.14, right=0.98, top=0.93, bottom=0.09, hspace=0.14)

    output_path = Path(out_dir) / "Figure1_IMF_SolarWind.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Saved: {output_path}")


def plot_figure2(df: pd.DataFrame, out_dir: Path | str = OUT_DIR) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(FIGURE_WIDTH, FIGURE2_HEIGHT), sharex=True)
    fig.patch.set_facecolor("white")

    # (a) SYM/H with Bz reference
    ax_symh = axes[0]
    ax_bz = ax_symh.twinx()

    line_symh = ax_symh.plot(df.index, df[COL_SYMH], color="navy", lw=1.1, label="SYM/H")
    line_bz = ax_bz.plot(df.index, df[COL_BZ], color="crimson", lw=0.6, alpha=0.65, label=r"$B_z$ (ref.)")
    ax_symh.axhline(0, color="gray", lw=0.5, linestyle="--")
    ax_bz.axhline(0, color="pink", lw=0.4, linestyle="--")

    style_axes(
        ax_symh,
        label_with_units("SYM/H", "nT"),
        ycolor="navy",
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    style_axes(
        ax_bz,
        label_with_units(r"$B_z$", "nT"),
        ycolor="crimson",
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    ax_bz.spines["top"].set_visible(False)

    minimum_time = df[COL_SYMH].idxmin()
    minimum_value = df[COL_SYMH].min()
    ax_symh.annotate(
        f"Min = {minimum_value:.0f} nT",
        xy=(minimum_time, minimum_value),
        xytext=(minimum_time + pd.Timedelta(hours=6), minimum_value + 40),
        fontsize=8,
        color="navy",
        arrowprops=dict(arrowstyle="->", color="navy", lw=0.8),
    )

    apply_storm_shading(ax_symh, STORM_PHASES, show_labels=False)
    add_panel_tag(ax_symh, "(a)")
    legend_lines = line_symh + line_bz
    ax_symh.legend(legend_lines, [line.get_label() for line in legend_lines], loc="upper right", fontsize=8, frameon=False)

    # (b) AE
    ax = axes[1]
    ax.fill_between(df.index, df[COL_AE], facecolor="darkorange", alpha=0.55, linewidth=0, label="AE")
    ax.plot(df.index, df[COL_AE], color="darkorange", lw=0.7)
    style_axes(
        ax,
        label_with_units("AE Index", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(b)")
    ax.legend(loc="upper right", fontsize=8, frameon=False)

    peak_time = df[COL_AE].idxmax()
    peak_value = df[COL_AE].max()
    ax.annotate(
        f"Peak = {peak_value:.0f} nT",
        xy=(peak_time, peak_value),
        xytext=(peak_time + pd.Timedelta(hours=4), peak_value * 0.85),
        fontsize=8,
        color="saddlebrown",
        arrowprops=dict(arrowstyle="->", color="saddlebrown", lw=0.8),
    )

    # (c) ASY/H
    ax = axes[2]
    ax.plot(df.index, df[COL_ASYH], color="purple", lw=0.95, label="ASY/H")
    ax.fill_between(df.index, df[COL_ASYH], facecolor="purple", alpha=0.18, linewidth=0)
    style_axes(
        ax,
        label_with_units("ASY/H", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(c)")
    ax.legend(loc="upper right", fontsize=8, frameon=False)

    format_shared_xaxis(
        list(axes),
        t_start=EVENT_START,
        t_end=EVENT_END,
        xlabel="Universal Time ( UT )",
        tick_fontsize=TICK_FONTSIZE,
        label_fontsize=LABEL_FONTSIZE,
        label_pad=LABEL_PAD,
    )

    fig.suptitle(
        "Geomagnetic Superstorm: May 10-13, 2024",
        fontsize=12,
        fontweight="bold",
        y=0.992,
    )
    _add_phase_header_legend(fig, y=0.972)

    fig.align_ylabels(axes)
    fig.subplots_adjust(left=0.14, right=0.98, top=0.93, bottom=0.09, hspace=0.14)

    output_path = Path(out_dir) / "Figure2_Geomagnetic_Indices.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Saved: {output_path}")


def combine_figure1_figure2(df: pd.DataFrame, out_dir: Path | str = OUT_DIR) -> None:
    fig, axes = plt.subplots(7, 1, figsize=(FIGURE_WIDTH, COMBINED_HEIGHT), sharex=True)
    fig.patch.set_facecolor("white")

    # (a) Magnetic field
    ax = axes[0]
    ax.plot(df.index, df[COL_B], color="black", lw=1.2, label=r"$|B|$")
    ax.plot(df.index, df[COL_BX], color="royalblue", lw=0.9, label=r"$B_x$")
    ax.plot(df.index, df[COL_BY], color="darkorange", lw=0.9, label=r"$B_y$")
    ax.plot(df.index, df[COL_BZ], color="crimson", lw=1.0, label=r"$B_z$")
    ax.axhline(0, color="gray", lw=0.6, linestyle="--")
    style_axes(
        ax,
        label_with_units("Magnetic Field", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(a)")
    ax.legend(loc="upper right", fontsize=7.5, ncol=4, frameon=False, bbox_to_anchor=(0.995, 0.98), borderaxespad=0.1)

    # (b) Speed
    ax = axes[1]
    ax.plot(df.index, df[COL_SPEED], color="seagreen", lw=1.0, label=r"$V_{sw}$")
    style_axes(
        ax,
        label_with_units("Speed", r"km s$^{-1}$"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(b)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    # (c) Density
    ax = axes[2]
    ax.plot(df.index, df[COL_DENSITY], color="steelblue", lw=0.95, label=r"$n_p$")
    style_axes(
        ax,
        label_with_units("Density", r"cm$^{-3}$"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(c)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    # (d) Electric field
    ax = axes[3]
    ax.plot(df.index, df[COL_EFIELD], color="saddlebrown", lw=0.95, label=r"$E_y$")
    ax.axhline(0, color="gray", lw=0.6, linestyle="--")
    style_axes(
        ax,
        label_with_units("Electric Field", r"mV m$^{-1}$"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(d)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    # (e) SYM/H
    ax = axes[4]
    ax.plot(df.index, df[COL_SYMH], color="navy", lw=1.05, label="SYM/H")
    ax.axhline(0, color="gray", lw=0.5, linestyle="--")
    style_axes(
        ax,
        label_with_units("SYM/H", "nT"),
        ycolor="navy",
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(e)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    # (f) AE
    ax = axes[5]
    ax.fill_between(df.index, df[COL_AE], facecolor="darkorange", alpha=0.55, linewidth=0, label="AE")
    ax.plot(df.index, df[COL_AE], color="darkorange", lw=0.7)
    style_axes(
        ax,
        label_with_units("AE Index", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(f)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    # (g) ASY/H
    ax = axes[6]
    ax.plot(df.index, df[COL_ASYH], color="purple", lw=0.95, label="ASY/H")
    ax.fill_between(df.index, df[COL_ASYH], facecolor="purple", alpha=0.18, linewidth=0)
    style_axes(
        ax,
        label_with_units("ASY/H", "nT"),
        label_fontsize=LABEL_FONTSIZE,
        tick_fontsize=TICK_FONTSIZE,
        label_pad=LABEL_PAD,
    )
    apply_storm_shading(ax, STORM_PHASES, show_labels=False)
    add_panel_tag(ax, "(g)")
    ax.legend(loc="upper right", fontsize=7.8, frameon=False)

    format_shared_xaxis(
        list(axes),
        t_start=EVENT_START,
        t_end=EVENT_END,
        xlabel="Universal Time ( UT )",
        tick_fontsize=TICK_FONTSIZE,
        label_fontsize=LABEL_FONTSIZE,
        label_pad=LABEL_PAD,
    )

    header_y = 0.992
    fig.text(
        0.5,
        header_y,
        "Geomagnetic Superstorm: May 10-13, 2024",
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
    )
    _add_phase_header_legend(fig, y=header_y, pre_label="Initial Phase")

    fig.align_ylabels(axes)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.955, bottom=0.055, hspace=0.18)

    output_path = Path(out_dir) / "Figure1_Figure2_Combined.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Saved: {output_path}")


def main() -> None:
    print("=" * 64)
    print(" May 2024 Superstorm | Solar Wind + Geomagnetic Plot Pipeline")
    print("=" * 64)

    df = load_master_data(DATA_PATH, replace_omni_fill_values=True)
    print(f"[OK] Loaded {len(df):,} rows from {DATA_PATH.name}")

    plot_figure1(df, OUT_DIR)
    plot_figure2(df, OUT_DIR)
    combine_figure1_figure2(df, OUT_DIR)

    print(f"[OK] Finished. Outputs saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()
