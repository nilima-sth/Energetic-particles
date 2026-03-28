from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from may_plot_utils import (
    DATA_PATH,
    EVENT_END,
    EVENT_START,
    OUT_DIR,
    apply_matplotlib_theme,
    format_shared_xaxis,
    load_master_data,
    style_axes,
)

apply_matplotlib_theme()

FIGURE_DPI = 300
FIGURE_WIDTH = 14
FIGURE_HEIGHT = 11
LABEL_FONTSIZE = 11
TICK_FONTSIZE = 9
LABEL_PAD = 14
LINE_WIDTH = 1.0

SELECTED_CHANNELS = {
    "Electron": [1, 2, 5, 6, 8],
    "Proton": [2, 4, 5, 8, 12],
    "Alpha": [1, 3, 4, 5, 6],
}

PANEL_SPECS = [
    {
        "name": "Electron",
        "prefix": "Electron_Flux_E",
        "channels": SELECTED_CHANNELS["Electron"],
        "ylabel": "Electron Flux\n(particles cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$)",
        "cmap": "viridis",
    },
    {
        "name": "Proton",
        "prefix": "Proton_Flux_P",
        "channels": SELECTED_CHANNELS["Proton"],
        "ylabel": "Proton Flux\n(particles cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$)",
        "cmap": "plasma",
    },
    {
        "name": "Alpha",
        "prefix": "Alpha_Flux_A",
        "channels": SELECTED_CHANNELS["Alpha"],
        "ylabel": "Alpha Flux\n(particles cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$)",
        "cmap": "cividis",
    },
]


def _sample_colormap(cmap_name: str, count: int, low: float = 0.12, high: float = 0.90):
    cmap = plt.colormaps[cmap_name]
    return [cmap(low + (high - low) * idx / max(count - 1, 1)) for idx in range(count)]


def plot_combined_flux_figure(df: pd.DataFrame, out_dir: Path | str = OUT_DIR) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), sharex=True)
    fig.patch.set_facecolor("white")

    for ax, spec in zip(axes, PANEL_SPECS):
        colors = _sample_colormap(spec["cmap"], len(spec["channels"]))

        for channel, color in zip(spec["channels"], colors):
            column = f"{spec['prefix']}{channel}"
            if column not in df.columns:
                continue

            label = f"{spec['name'][0]}{channel}"
            ax.plot(df.index, df[column], color=color, linewidth=LINE_WIDTH, label=label)

        ax.set_yscale("log")
        style_axes(
            ax,
            spec["ylabel"],
            label_fontsize=LABEL_FONTSIZE - 1,
            tick_fontsize=TICK_FONTSIZE,
            label_pad=LABEL_PAD,
            show_log_minor_ticks=True,
            show_log_minor_grid=True,
        )

        if spec["name"] == "Electron":
            y_min, y_max = ax.get_ylim()
            ax.set_ylim(y_min, y_max * 2.5)
            ax.legend(
                loc="upper right",
                bbox_to_anchor=(0.995, 0.34),
                borderaxespad=0.1,
                fontsize=8,
                frameon=False,
                title="Channel",
                title_fontsize=8,
            )
        else:
            ax.legend(
                loc="best",
                fontsize=8,
                frameon=False,
                title="Channel",
                title_fontsize=8,
            )

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
        "Particle Flux Evolution: May 10-13, 2024",
        fontsize=12,
        fontweight="bold",
        y=0.968,
    )

    fig.align_ylabels(axes)
    fig.subplots_adjust(left=0.20, right=0.98, top=0.94, bottom=0.08, hspace=0.08)

    output_path = Path(out_dir) / "Figure_Flux_Combined_SelectedChannels.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Saved: {output_path}")


def main() -> None:
    print("=" * 66)
    print(" May 2024 Superstorm | Selected-Channel Particle Flux Figure")
    print("=" * 66)

    df = load_master_data(DATA_PATH, replace_omni_fill_values=False, mask_non_positive_flux=True)
    print(f"[OK] Loaded {len(df):,} rows from {DATA_PATH.name}")

    plot_combined_flux_figure(df, OUT_DIR)
    print(f"[OK] Finished. Output saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()
