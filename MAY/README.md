# MAY Folder Guide

This folder contains the full May 10-13, 2024 superstorm pipeline: preprocessing, figure generation, and final exports.

## Python Scripts

- `preprocess.py`
  - Builds `MAY_2024_Master_Cleaned.csv` from OMNI + GOES NetCDF files.
- `plot_may_event.py`
  - Generates:
    - `Figure1_IMF_SolarWind.png`
    - `Figure2_Geomagnetic_Indices.png`
    - `Figure1_Figure2_Combined.png`
- `plot_flux_may_event.py`
  - Generates:
    - `Figure_Flux_Combined_SelectedChannels.png`
- `plot_psd.py`
  - Generates channel-by-channel PSD figures:
    - `PSD_Channel_1.png` ... `PSD_Channel_10.png`
- `plot_psd_combined.py`
  - Generates combined PSD outputs:
    - `PSD_Combined_Figure1_Ch1-5.pdf/.png`
    - `PSD_Combined_Figure2_Ch6-10.pdf/.png`
    - `PSD_Combined_SelectedChannels.pdf/.png`

## Shared Utility Modules

- `may_plot_utils.py`
  - Common plotting style, phase shading, axis formatting, and data loading.
- `psd_utils.py`
  - Shared PSD math helpers (Welch computation and preprocessing).

## Suggested Run Order

1. `python MAY/preprocess.py`
2. `python MAY/plot_may_event.py`
3. `python MAY/plot_flux_may_event.py`
4. `python MAY/plot_psd_combined.py`

Use `plot_psd.py` only when you need all 10 single-channel PSD figures.
