from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from may_plot_utils import apply_matplotlib_theme
from psd_utils import compute_welch_psd, load_master_data, prepare_array

apply_matplotlib_theme()

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "MAY_2024_Master_Cleaned.csv"
OUT_DIR = BASE_DIR

FIGURE_DPI = 300
FIGSIZE = (8, 8)
LINE_WIDTH = 0.8

TITLE_FONTSIZE = 20
XLABEL_FONTSIZE = 22
YLABEL_FONTSIZE = 22
LABEL_PAD = 20
TICK_LABELSIZE = 18
LEGEND_FONTSIZE = 16

COLOR_SYMH = "blue"
COLOR_ELECTRON = "crimson"
COLOR_PROTON = "seagreen"
COLOR_ALPHA = "darkorchid"

COL_SYMH = "SYM/H, nT"


def _apply_psd_style() -> None:
    sns.set_style("ticks")
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2})


def _format_axis(ax) -> None:
    ax.set_facecolor("white")
    ax.grid(axis="y", linestyle="--")

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_edgecolor("dimgray")

    ax.tick_params(axis="both", which="both", direction="in", labelsize=TICK_LABELSIZE)
    ax.tick_params(axis="x", which="both", top=True, bottom=True)
    ax.tick_params(axis="y", which="both", left=True, right=True)
    ax.tick_params(axis="y", which="minor", right=False)
    ax.tick_params(which="major", length=10, width=2)
    ax.tick_params(which="minor", length=6, width=2)

    ax.set_xlabel("Frequency (Hz)", fontsize=XLABEL_FONTSIZE, labelpad=LABEL_PAD)
    ax.set_ylabel("PSD\n(nT$^2$ / Hz)", fontsize=YLABEL_FONTSIZE, labelpad=LABEL_PAD)


def plot_all_psd(df, out_dir: Path | str = OUT_DIR) -> None:
    for channel in range(1, 11):
        column_e = f"Electron_Flux_E{channel}"
        column_p = f"Proton_Flux_P{channel}"
        column_a = f"Alpha_Flux_A{channel}"

        arr_symh = prepare_array(df[COL_SYMH])
        arr_e = prepare_array(df[column_e])
        arr_p = prepare_array(df[column_p])
        arr_a = prepare_array(df[column_a])

        f_symh, psd_symh = compute_welch_psd(arr_symh)
        f_e, psd_e = compute_welch_psd(arr_e)
        f_p, psd_p = compute_welch_psd(arr_p)
        f_a, psd_a = compute_welch_psd(arr_a)

        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.loglog(f_symh, psd_symh, lw=LINE_WIDTH, color=COLOR_SYMH, label="SYM/H")
        ax.loglog(f_e, psd_e, lw=LINE_WIDTH, color=COLOR_ELECTRON, label=f"Electron E{channel}")
        ax.loglog(f_p, psd_p, lw=LINE_WIDTH, color=COLOR_PROTON, label=f"Proton P{channel}")
        ax.loglog(f_a, psd_a, lw=LINE_WIDTH, color=COLOR_ALPHA, label=f"Alpha A{channel}")

        _format_axis(ax)
        ax.legend(loc="best", fontsize=LEGEND_FONTSIZE, frameon=False)
        ax.set_title(f"Channel {channel}", fontsize=TITLE_FONTSIZE, y=1.02)

        output_path = Path(out_dir) / f"PSD_Channel_{channel}.png"
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        plt.close(fig)
        print(f"[OK] Saved: {output_path}")


def main() -> None:
    print("=" * 52)
    print(" May 2024 Superstorm | PSD Channel Plots")
    print("=" * 52)

    _apply_psd_style()
    df = load_master_data(DATA_PATH)
    print(f"[OK] Loaded {len(df):,} rows from {DATA_PATH.name}")

    plot_all_psd(df, OUT_DIR)
    print(f"[OK] Finished. Outputs saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()
