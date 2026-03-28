# Energetic Particle Dynamics During Major Geomagnetic Storms

> **Status:** Active — Case Study Visualisation Phase  
> **Target Journal:** AGU *Space Weather* (Q1)  
> **Authors:** Nilima Shrestha and Shreeyan Rijal (nili373ma@gmail.com and shreeyanrijal7@gmail.com)

---

## 1. Scientific Objective

This study investigates the behaviour of **energetic particles** (electrons, protons, and alpha particles) measured by the GOES-16 SEISS instrument during four major geomagnetic storm events spanning Solar Cycle 25. The overarching scientific goals are:

1. **Characterise** storm-time particle flux dynamics across multiple energy channels for each event.
2. **Compare** the four events statistically to identify common signatures and outliers.
3. **Build and evaluate ML models** that predict particle flux from upstream solar wind and geomagnetic index drivers.

The four storm events currently in scope are:

| Event | Date Range | Peak Storm Index (SYM/H) |
|-------|-----------|--------------------------|
| August 2022 | Aug 03–04, 2022 | ~ −70 nT |
| November 2021 | Nov 04–05, 2021 | ~ −110 nT |
| April 2023 | Apr 23–24, 2023 | ~ −210 nT |
| **May 2024 Superstorm** | **May 10–13, 2024** | **~ −518 nT** |

The May 2024 event is one of the strongest geomagnetic storms since the Halloween storms of 2003 and serves as the primary case study for in-depth analysis.

---

## 2. Repository Structure

```
Energetic-particles/
│
├── README.md                          ← This file
├── EnergyParticles_Plotting_BluePrint.pdf  ← Full figure plan (9 figures)
│
├── APRIL/
│   ├── APRIL_2023_Master_Cleaned.csv  ← 1-min merged dataset
│   ├── preprocess.py                  ← Event-specific preprocessing
│   ├── omni_min_*.fmt / *.lst         ← Raw OMNI HTTPS download files
│   ├── ELECTRON/                      ← GOES-16 MPSH electron NetCDF files
│   └── PROTON/                        ← GOES-16 SGPS proton NetCDF files
│
├── AUGUST/
│   ├── AUGUST_2022_Master_Cleaned.csv
│   ├── preprocess.py
│   ├── omni_min_*.fmt / *.lst
│   ├── ELECTRON/
│   └── PROTON/
│
├── MAY/                               ← PRIMARY EVENT (superstorm)
│   ├── MAY_2024_Master_Cleaned.csv    ← 1-min merged dataset (5 760 rows)
│   ├── plot_may_event.py              ← Figures 1 & 2: solar wind + indices
│   ├── plot_flux_may_event.py         ← Figures 3, 5, 6: electron/proton/alpha flux
│   ├── preprocess.py                  ← Data merging / cleaning pipeline
│   ├── omni_min_*.fmt / *.lst         ← Raw OMNI HTTPS download files
│   ├── ELECTRON/                      ← GOES-16 MPSH electron NetCDF files
│   └── PROTON/                        ← GOES-16 SGPS proton NetCDF files
│
└── NOVEMBER/
    ├── NOVEMBER_2021_Master_Cleaned.csv
    ├── preprocess.py
    ├── omni_min_*.fmt / *.lst
    ├── ELECTRON/
    └── PROTON/
```

---

## 3. Data Description

### 3.1 Master CSV (`MAY_2024_Master_Cleaned.csv`)

A pre-processed, 1-minute-resolution flat file covering **May 10 00:00 UTC – May 13 23:59 UTC, 2024** (5 760 rows × 47 columns).

| Column (index / name) | Source | Description |
|-----------------------|--------|-------------|
| *(index)* — `datetime` | Merged | UTC timestamp, parsed as `DatetimeIndex` |
| `Field magnitude average, nT` | OMNI | Total IMF magnitude \|B\| |
| `BX, nT (GSE, GSM)` | OMNI | IMF Bx component (GSE = GSM for this component) |
| `BY, nT (GSM)` | OMNI | IMF By component in GSM coordinates |
| `BZ, nT (GSM)` | OMNI | IMF Bz component — key driver of storm intensity |
| `Speed, km/s` | OMNI | Solar wind bulk speed |
| `Proton Density, n/cc` | OMNI | Solar wind proton number density |
| `Proton Temperature, K` | OMNI | Solar wind proton temperature |
| `Flow pressure, nPa` | OMNI | Dynamic pressure $P_{dyn} = \frac{1}{2}m_p n_p V^2$ |
| `Electric field, mV/m` | OMNI | Interplanetary Ey = −Vx × Bz (Kan–Lee coupling) |
| `Plasma beta` | OMNI | Ratio of plasma to magnetic pressure |
| `AE-index, nT` | OMNI | Auroral electrojet amplitude (ring of stations) |
| `SYM/H, nT` | OMNI | Symmetric ring-current index (≈ Dst at 1-min) |
| `ASY/H, nT` | OMNI | Asymmetric ring-current variation |
| `Electron_Flux_E1` … `E10` | GOES-16 MPSH | Differential electron flux, energy channels E1–E10 |
| `Proton_Flux_P1` … `P13` | GOES-16 SGPS | Differential proton flux, energy channels P1–P13 |
| `Alpha_Flux_A1` … `A11` | GOES-16 SGPS | Differential alpha-particle flux, channels A1–A11 |

**Data gaps:** OMNI magnetic-field columns have ~764 NaN rows; solar wind bulk parameters have ~1 867 NaN rows (data-quality-flagged minutes). Particle columns are continuous. NaN periods appear as gaps in line plots — this is intentional and scientifically correct.

---

## 4. Visualisation Script — `plot_may_event.py`

### 4.1 What it does

| Script | Output files | Content |
|--------|-------------|---------|
| `plot_may_event.py` | `Figure1_IMF_SolarWind.png` | IMF components, solar wind speed, density + pressure, electric field |
| `plot_may_event.py` | `Figure2_Geomagnetic_Indices.png` | SYM/H (with Bz overlay), AE index, ASY/H index |
| `plot_flux_may_event.py` | `Figure3_Electron_Flux.png` | Electron flux E1–E10 (odd / even channel panels, log scale, viridis) |
| `plot_flux_may_event.py` | `Figure5_Proton_Flux.png` | Proton flux P1–P13 (odd / even channel panels, log scale, plasma) |
| `plot_flux_may_event.py` | `Figure6_Alpha_Flux.png` | Alpha flux A1–A11 (odd / even channel panels, log scale, cividis) |

Both figures share the following design principles drawn from `EnergyParticles_Plotting_BluePrint.pdf`:

- **Shared UTC x-axis** spanning May 10–13, 2024 with major ticks at midnight and minor ticks every 6 hours.
- **Storm-phase shading** via `ax.axvspan()` with phase labels written at the top of every panel:
  - `Initial Phase` — May 10 00:00–17:00 UTC (SSC to onset of southward Bz) — *gold*
  - `Main Phase` — May 10 17:00 – May 11 10:00 UTC (southward Bz, SYM/H plummeting to −518 nT) — *salmon*
  - `Recovery Phase` — May 11 10:00 – May 13 23:59 UTC (northward Bz, ring-current decay) — *light blue*
- Zero-gap stacking: `plt.subplots_adjust(hspace=0)` — no white space between panels.
- Clean date labels: custom cross-platform formatter outputs `"May 10"`, `"May 11"`, etc.
- Particle flux panels (future figures) use `ax.set_yscale('log')` as mandated by the blueprint.

### 4.2 Code structure

#### `plot_may_event.py` — Solar Wind & Index Figures (1 & 2)

```
plot_may_event.py
│
├── Section 0 – Configuration
│   ├── DATA_PATH          path to MAY_2024_Master_Cleaned.csv
│   ├── OUT_DIR            output directory for saved figures
│   ├── STORM_PHASES       dict: phase name → {start, end, color, alpha}
│   └── column aliases     (COL_B, COL_BZ, COL_SYMH, …)
│
├── Section 1 – Helper Functions
│   ├── load_data()            reads CSV, masks OMNI fill values, returns DataFrame
│   ├── apply_storm_shading()  draws axvspan + phase label on any Axes
│   ├── format_shared_xaxis()  sets xlim, tick locators, hides all but bottom labels
│   └── style_axes()           uniform y-label / grid / spine styling
│
├── Section 2 – plot_figure1()
│   ├── Panel (a)  |B|, Bx, By, Bz
│   ├── Panel (b)  Solar wind speed
│   ├── Panel (c)  Proton density (left) + dynamic pressure (twinx, right)
│   └── Panel (d)  Interplanetary electric field Ey
│
├── Section 3 – plot_figure2()
│   ├── Panel (a)  SYM/H + thin Bz reference (twinx)
│   ├── Panel (b)  AE index (filled area)
│   └── Panel (c)  ASY/H index
│
└── Section 4 – main()
    ├── load_data()
    ├── plot_figure1()
    └── plot_figure2()
```

### 4.3 How to run

#### Prerequisites

Python ≥ 3.9 with the following packages:

```bash
pip install matplotlib pandas numpy
```

#### Execution — solar wind & geomagnetic index figures

```bash
cd MAY
python plot_may_event.py
```

#### Execution — particle flux figures (Figures 3, 5, 6)

```bash
cd MAY
python plot_flux_may_event.py
```

Both scripts print a confirmation line for each figure and save PNGs in the `MAY/` directory.

#### `plot_flux_may_event.py` — Particle Flux Figures (3, 5, 6)

```
plot_flux_may_event.py
│
├── Section 0 – Configuration
│   ├── DATA_PATH, OUT_DIR, T_START, T_END
│   ├── STORM_PHASES          (identical to plot_may_event.py)
│   └── SPECIES dict          {Electron, Proton, Alpha} → {prefix, n_channels,
│                              fig_num, cmap, ylabel, fig_title, fig_fname}
│
├── Section 1 – Helper Functions
│   ├── load_data()              reads CSV; masks flux ≤ 0 → NaN (log safety)
│   ├── apply_storm_shading()    axvspan + phase labels (identical logic)
│   ├── format_shared_xaxis()    shared UTC x-axis, cross-platform formatter
│   ├── style_axes()             y-label, log minor grid, spine styling
│   ├── build_channel_groups()   splits channels into odd/even lists
│   ├── get_cmap_colors()        samples n colours from a named colormap
│   └── build_phase_legend_patches()  mpatches for phase legend
│
├── Section 2 – plot_flux_figure()
│   ├── Calls build_channel_groups() → odd_group, even_group
│   ├── Assigns colormap colours spanning the full channel range
│   ├── Creates 2-panel figure (sharex, hspace=0)
│   │   ├── Panel (a) – _draw_flux_panel(odd_group)
│   │   └── Panel (b) – _draw_flux_panel(even_group)
│   └── Saves PNG
│
├── _draw_flux_panel()  (internal)
│   ├── Plots each channel with its colormap colour
│   ├── ax.set_yscale('log')
│   ├── apply_storm_shading()
│   └── Outside legend  bbox_to_anchor=(1.02, 1.0)
│
└── Section 3 – main()
    └── Loops over SPECIES dict → plot_flux_figure() × 3
```

**Odd / Even Channel Splitting Logic:**  
Channels are numbered 1-based. Splitting by parity (`i % 2`) halves the line
count per panel while preserving spectral order within each panel, so the
colormap gradient still runs monotonically from low → high energy.

**Colormap Scheme:**  
| Species | Colormap | Rationale |
|---------|----------|-----------|
| Electrons | `viridis` | Perceptually uniform, widely used in space physics |
| Protons | `plasma` | Warm tones contrast with viridis in multi-species comparisons |
| Alphas | `cividis` | CVD-safe, distinguishable from both viridis and plasma |

#### Changing the output DPI

Edit the `FIGURE_DPI` constant at the top of either script:

```python
FIGURE_DPI = 300   # for print-ready publication quality
```

#### Adjusting storm-phase boundaries

Phase boundaries are defined in the `STORM_PHASES` dictionary in Section 0 of each script. Adjust the ISO-format strings as needed:

```python
STORM_PHASES = {
    "Initial\nPhase": {"start": "2024-05-10 00:00", "end": "2024-05-10 17:00", ...},
    ...
}
```

---

## 5. Machine Learning Roadmap (Upcoming)

The visualisation phase (current) feeds into a supervised ML pipeline:

1. **Feature engineering** — storm-phase flags, lagged solar wind parameters, rolling statistics.
2. **Target variables** — electron flux channels (E1–E10), proton flux channels (P1–P13).
3. **Models under evaluation** — Random Forest, XGBoost, LSTM, and Transformer-based architectures.
4. **Multi-event generalisation** — train on three events, test on the held-out fourth (leave-one-event-out cross-validation).
5. **Evaluation metrics** — RMSE (log-flux), skill score vs. persistence model, prediction efficiency (PE).

---

## 6. Data Sources

| Dataset | URL / Instrument |
|---------|-----------------|
| OMNI 1-min solar wind | https://omniweb.gsfc.nasa.gov/ |
| GOES-16 MPSH (electrons) | https://www.ngdc.noaa.gov/stp/satellite/goes/ |
| GOES-16 SGPS (protons/alphas) | https://www.ngdc.noaa.gov/stp/satellite/goes/ |

---

## 7. Planned Figures (per Blueprint)

| Figure | Description | Status |
|--------|-------------|--------|
| **Figure 1** | IMF & Solar Wind Conditions | ✅ Done |
| **Figure 2** | Geomagnetic Indices Response | ✅ Done |
| **Figure 3** | Electron Flux Evolution (E1–E10) | ✅ Done |
| Figure 4 | Electron Energy Spectra (3 phases) | 🔲 Upcoming |
| **Figure 5** | Proton Flux Evolution (P1–P13) | ✅ Done |
| **Figure 6** | Alpha Particle Flux & Composition | ✅ Done |
| Figure 7 | Coupling & Correlation Analysis | 🔲 Upcoming |
| Figure 8 | Electron Energy-Time Spectrogram | 🔲 Upcoming |
| Figure 9 | Phase-wise Statistical Summary | 🔲 Upcoming |
| Multi-event | Four-event comparative figures | 🔲 Upcoming |

---

*Last updated: May 2024 case study — visualisation phase.*
