from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from may_plot_utils import apply_matplotlib_theme
from psd_utils import (
    compute_welch_psd,
    load_master_data,
    positive_frequency_view,
    prepare_array,
)

try:
    import netCDF4 as nc
except ImportError:
    nc = None

apply_matplotlib_theme()

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "MAY_2024_Master_Cleaned.csv"
OUT_DIR = BASE_DIR

FIGURE_DPI = 300
FIG_WIDTH = 34
FIG_HEIGHT = 6
LINE_WIDTH = 0.85

SUPTITLE_FS = 11
PANEL_TITLE_FS = 10
XLABEL_FS = 11
YLABEL_FS = 11
TICK_FS = 8
LEGEND_FS = 7

COL_SYMH = "SYM/H, nT"
COLOR_SYMH = "blue"
COLOR_ELECTRON = "crimson"
COLOR_PROTON = "seagreen"
COLOR_ALPHA = "darkorchid"

GROUPS = [
    {
        "channels": list(range(1, 6)),
        "out_pdf": "PSD_Combined_Figure1_Ch1-5.pdf",
        "title": "PSD - Channels 1-5 | SYM/H & Particle Fluxes | May 10-13, 2024 Geomagnetic Superstorm",
    },
    {
        "channels": list(range(6, 11)),
        "out_pdf": "PSD_Combined_Figure2_Ch6-10.pdf",
        "title": "PSD - Channels 6-10 | SYM/H & Particle Fluxes | May 10-13, 2024 Geomagnetic Superstorm",
    },
]

SELECTED_CHANNELS = {
    "electron": [1, 2, 5, 6, 8],
    "proton": [2, 4, 5, 8, 12],
    "alpha": [1, 3, 4, 5, 6],
}


def _apply_psd_style() -> None:
    sns.set_style("ticks")
    sns.set_context("paper", font_scale=1.3, rc={"lines.linewidth": 2})


def _sample_colormap(cmap_name: str, count: int, low: float = 0.12, high: float = 0.90):
    cmap = plt.colormaps[cmap_name]
    return [cmap(low + (high - low) * idx / max(count - 1, 1)) for idx in range(count)]


def load_channel_energy_annotations() -> dict[int, str]:
    """Return channel-wise energy labels based on GOES NetCDF metadata."""
    if nc is None:
        return {}

    electron_files = sorted((BASE_DIR / "ELECTRON").glob("*.nc"))
    proton_files = sorted((BASE_DIR / "PROTON").glob("*.nc"))
    if not electron_files or not proton_files:
        return {}

    with nc.Dataset(str(electron_files[0])) as ds_e, nc.Dataset(str(proton_files[0])) as ds_p:
        e_eff = ds_e.variables["DiffElectronEffectiveEnergy"][:]
        p_lo = ds_p.variables["DiffProtonLowerEnergy"][:]
        p_hi = ds_p.variables["DiffProtonUpperEnergy"][:]
        a_lo = ds_p.variables["DiffAlphaLowerEnergy"][:]
        a_hi = ds_p.variables["DiffAlphaUpperEnergy"][:]

    e_eff = e_eff.mean(axis=0)[:10]
    p_lo = p_lo.mean(axis=0)[:10]
    p_hi = p_hi.mean(axis=0)[:10]
    a_lo = a_lo.mean(axis=0)[:10]
    a_hi = a_hi.mean(axis=0)[:10]

    annotations: dict[int, str] = {}
    for channel in range(1, 11):
        idx = channel - 1
        annotations[channel] = (
            f"E~{e_eff[idx]:.0f} keV | "
            f"P {p_lo[idx] / 1000:.2f}-{p_hi[idx] / 1000:.2f} MeV | "
            f"A {a_lo[idx] / 1000:.2f}-{a_hi[idx] / 1000:.2f} MeV"
        )
    return annotations


def _plot_single_psd_panel(ax, df, *, electron_channel: int, proton_channel: int, alpha_channel: int) -> None:
    arr_symh = prepare_array(df[COL_SYMH])
    arr_e = prepare_array(df[f"Electron_Flux_E{electron_channel}"])
    arr_p = prepare_array(df[f"Proton_Flux_P{proton_channel}"])
    arr_a = prepare_array(df[f"Alpha_Flux_A{alpha_channel}"])

    f_symh, psd_symh = positive_frequency_view(*compute_welch_psd(arr_symh))
    f_e, psd_e = positive_frequency_view(*compute_welch_psd(arr_e))
    f_p, psd_p = positive_frequency_view(*compute_welch_psd(arr_p))
    f_a, psd_a = positive_frequency_view(*compute_welch_psd(arr_a))

    ax.loglog(f_symh, psd_symh, lw=LINE_WIDTH, color=COLOR_SYMH, label="SYM/H")
    ax.loglog(f_e, psd_e, lw=LINE_WIDTH, color=COLOR_ELECTRON, label=f"E{electron_channel}")
    ax.loglog(f_p, psd_p, lw=LINE_WIDTH, color=COLOR_PROTON, label=f"P{proton_channel}")
    ax.loglog(f_a, psd_a, lw=LINE_WIDTH, color=COLOR_ALPHA, label=f"A{alpha_channel}")

    ax.set_xlim(f_symh.min(), f_symh.max())


def _style_psd_axis(ax, *, show_ylabel: bool, show_xlabel: bool) -> None:
    ax.grid(axis="y", linestyle="--", linewidth=0.4, color="lightgray")
    ax.grid(axis="x", linestyle=":", linewidth=0.3, color="lightgray", which="both")
    ax.tick_params(axis="both", which="both", direction="in", labelsize=TICK_FS)
    ax.tick_params(axis="x", which="both", top=True, bottom=True)
    ax.tick_params(axis="y", which="both", left=True, right=True)
    ax.tick_params(axis="y", which="minor", right=False)
    ax.tick_params(which="major", length=6, width=1.2)
    ax.tick_params(which="minor", length=3, width=0.8)
    ax.xaxis.set_tick_params(labelbottom=True)

    if show_xlabel:
        ax.set_xlabel("Frequency (Hz)", fontsize=XLABEL_FS, labelpad=10)
    else:
        ax.set_xlabel("")

    if show_ylabel:
        ax.set_ylabel("PSD\n(nT$^2$ / Hz)", fontsize=YLABEL_FS, labelpad=10)
    else:
        ax.set_ylabel("")
        ax.yaxis.set_tick_params(labelleft=True)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_edgecolor("dimgray")


def build_combined_figure(df, channels: list[int], title: str, out_pdf: str) -> None:
    channel_energy = load_channel_energy_annotations()
    fig, axes = plt.subplots(1, len(channels), figsize=(FIG_WIDTH, FIG_HEIGHT), sharex=False)

    for idx, (ax, channel) in enumerate(zip(axes, channels)):
        _plot_single_psd_panel(
            ax,
            df,
            electron_channel=channel,
            proton_channel=channel,
            alpha_channel=channel,
        )

        ax.set_title(f"Channel {channel}", fontsize=PANEL_TITLE_FS, fontweight="bold", loc="left", pad=4)
        ax.set_title(channel_energy.get(channel, ""), fontsize=PANEL_TITLE_FS - 2, loc="right", pad=4)
        _style_psd_axis(ax, show_ylabel=(idx == 0), show_xlabel=(idx == 2))
        ax.legend(loc="upper right", fontsize=LEGEND_FS, frameon=False)

    fig.suptitle(title, fontsize=SUPTITLE_FS, fontweight="bold", y=1.01)
    plt.tight_layout()

    pdf_path = OUT_DIR / out_pdf
    png_path = OUT_DIR / out_pdf.replace(".pdf", ".png")
    fig.savefig(pdf_path, format="pdf", dpi=FIGURE_DPI, bbox_inches="tight")
    fig.savefig(png_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Saved: {pdf_path}")
    print(f"[OK] Saved: {png_path}")


def build_selected_channels_figure(df) -> None:
    triplets = list(
        zip(
            SELECTED_CHANNELS["electron"],
            SELECTED_CHANNELS["proton"],
            SELECTED_CHANNELS["alpha"],
        )
    )

    e_colors = _sample_colormap("viridis", len(triplets))
    p_colors = _sample_colormap("plasma", len(triplets))
    a_colors = _sample_colormap("cividis", len(triplets))

    fig, axes = plt.subplots(1, len(triplets), figsize=(FIG_WIDTH, FIG_HEIGHT), sharex=False)

    arr_symh = prepare_array(df[COL_SYMH])
    f_symh, psd_symh = positive_frequency_view(*compute_welch_psd(arr_symh))

    for idx, (ax, (e_channel, p_channel, a_channel)) in enumerate(zip(axes, triplets)):
        arr_e = prepare_array(df[f"Electron_Flux_E{e_channel}"])
        arr_p = prepare_array(df[f"Proton_Flux_P{p_channel}"])
        arr_a = prepare_array(df[f"Alpha_Flux_A{a_channel}"])

        f_e, psd_e = positive_frequency_view(*compute_welch_psd(arr_e))
        f_p, psd_p = positive_frequency_view(*compute_welch_psd(arr_p))
        f_a, psd_a = positive_frequency_view(*compute_welch_psd(arr_a))

        ax.loglog(f_symh, psd_symh, lw=LINE_WIDTH, color=COLOR_SYMH, label="SYM/H")
        ax.loglog(f_e, psd_e, lw=LINE_WIDTH, color=e_colors[idx], label=f"E{e_channel}")
        ax.loglog(f_p, psd_p, lw=LINE_WIDTH, color=p_colors[idx], label=f"P{p_channel}")
        ax.loglog(f_a, psd_a, lw=LINE_WIDTH, color=a_colors[idx], label=f"A{a_channel}")

        panel_tag = f"({chr(ord('a') + idx)})"
        ax.text(
            0.92,
            1.02,
            panel_tag,
            transform=ax.transAxes,
            fontsize=PANEL_TITLE_FS,
            fontweight="bold",
            ha="left",
            va="bottom",
            clip_on=False,
        )

        _style_psd_axis(ax, show_ylabel=(idx == 0), show_xlabel=(idx == 2))
        ax.set_xlim(f_symh.min(), f_symh.max())
        ax.legend(loc="upper right", fontsize=LEGEND_FS, frameon=False)

    fig.suptitle("Power Spectral Density | May 10-13, 2024", fontsize=SUPTITLE_FS, fontweight="bold", y=1.01)
    plt.tight_layout()

    pdf_path = OUT_DIR / "PSD_Combined_SelectedChannels.pdf"
    png_path = OUT_DIR / "PSD_Combined_SelectedChannels.png"
    fig.savefig(pdf_path, format="pdf", dpi=FIGURE_DPI, bbox_inches="tight")
    fig.savefig(png_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Saved: {pdf_path}")
    print(f"[OK] Saved: {png_path}")


def main() -> None:
    print("=" * 58)
    print(" May 2024 Superstorm | Combined PSD Plot Pipeline")
    print("=" * 58)

    _apply_psd_style()
    df = load_master_data(DATA_PATH)
    print(f"[OK] Loaded {len(df):,} rows from {DATA_PATH.name}")

    for group in GROUPS:
        print(f"[INFO] Building {group['out_pdf']}")
        build_combined_figure(df, group["channels"], group["title"], group["out_pdf"])

    print("[INFO] Building PSD_Combined_SelectedChannels")
    build_selected_channels_figure(df)

    print(f"[OK] Finished. Outputs saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()
