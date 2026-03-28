# Flux Plot Design Requirements (Final)

Use this file as the single source of truth for generating the May 10-13, 2024 particle-flux figure.

## 1. Scope

- Event: May 10-13, 2024 geomagnetic storm
- Data file: `MAY_2024_Master_Cleaned.csv`
- Script target: `plot_flux_may_event.py`
- Output figure file: `Figure_Flux_Combined_SelectedChannels.png`

## 2. Data Rules

- Parse datetime from column 0 (unnamed index) and use as DataFrame index.
- Time window:
  - `T_START = 2024-05-10 00:00`
  - `T_END   = 2024-05-13 23:59`
- Before plotting on log scale, mask non-positive flux values:
  - all columns starting with `Electron_`, `Proton_`, `Alpha_`
  - apply: `df[flux_cols] = df[flux_cols].mask(df[flux_cols] <= 0)`

## 3. Channel Selection (Required)

Use exactly these channels:

- Electron: `E1, E2, E5, E6, E8`
- Proton: `P2, P4, P5, P8, P12`
- Alpha: `A1, A3, A4, A5, A6`

Column names:
- Electron: `Electron_Flux_E{ch}`
- Proton: `Proton_Flux_P{ch}`
- Alpha: `Alpha_Flux_A{ch}`

## 4. Figure Layout

- Single figure with 3 vertically stacked subplots (3x1), shared x-axis:
  1. Electron Flux (top)
  2. Proton Flux (middle)
  3. Alpha Flux (bottom)
- Use white figure and axes background.
- Keep visible panel borders (all spines visible) to separate panels.
- Keep compact spacing without overlap (`hspace` small, around `0.08`).

## 5. Title and Labels

- Global title text (exact):
  - `Particle Flux Evolution: May 10-13, 2024`
- Title placement used in final accepted style:
  - `x=0.56`, `y=0.968`, bold, fontsize around 12
- Y labels must be multiline:
  - Top: `Electron Flux\n(particles cm^-2 s^-1 sr^-1 keV^-1)`
  - Middle: `Proton Flux\n(particles cm^-2 s^-1 sr^-1 keV^-1)`
  - Bottom: `Alpha Flux\n(particles cm^-2 s^-1 sr^-1 keV^-1)`
- Bottom x-label only:
  - `Time (UTC), May 2024`

## 6. Ticks and Axes Styling

- Font family for full figure: `Times New Roman`
- X-axis ticks:
  - mirrored major/minor ticks (`top=True`, `bottom=True`)
  - inward direction (`direction='in'`)
- Y-axis ticks:
  - major ticks mirrored left and right
  - minor ticks visible on left only (right-side minor ticks OFF)
  - inward direction
- Log y-axis for all 3 subplots.
- Keep subtle grid:
  - y major dotted, y minor lighter dotted
  - x major dashed

## 7. X-axis Date Formatting

- Major ticks: daily (`DayLocator(interval=1)`)
- Minor ticks: every 6 hours
- Date labels shown only on bottom subplot and formatted like `May 10`.
- Draw vertical day-separator lines through all panels at daily boundaries.

## 8. Legends (Required Final Behavior)

- Legends must be fully transparent and blended with plot background:
  - `frameon=False`
  - `framealpha=0.0`
  - `facecolor='none'`
  - `edgecolor='none'`
- Legends must be inside plotting area.
- Critical rule: legend text should NOT touch or overlap the plotted curves.
- Electron panel legend:
  - place in upper-right region but shifted down to avoid touching data
  - current accepted placement: `loc='upper right', bbox_to_anchor=(0.995, 0.34)`
- Proton and Alpha legends:
  - use `loc='best'` to avoid data overlap

## 9. Colormaps

- Electron panel: `viridis`
- Proton panel: `plasma`
- Alpha panel: `cividis`
- Use evenly spaced colors per panel based on number of selected channels.

## 10. Output Settings

- Save at publication quality:
  - `dpi=300`
  - `facecolor='white'`
  - `bbox_inches='tight'`
- Output filename:
  - `Figure_Flux_Combined_SelectedChannels.png`

## 11. Must-NOT Rules

- Do NOT add storm phase shading.
- Do NOT add storm-phase legend.
- Do NOT split into odd/even figures.
- Do NOT plot all channels.
- Do NOT use legend boxes.

## 12. Prompt Template for Other AI

Use this exact instruction block:

"""
Update `plot_flux_may_event.py` to generate one 3x1 combined flux figure from `MAY_2024_Master_Cleaned.csv`.
Use channels:
- Electron: E1,E2,E5,E6,E8
- Proton: P2,P4,P5,P8,P12
- Alpha: A1,A3,A4,A5,A6

Requirements:
- Shared x-axis, bottom labels only
- Log y-axis on all panels
- Mask values <= 0 before plotting
- White background, full panel borders visible
- Times New Roman font
- Inward mirrored ticks; y minor ticks only on left
- Daily vertical separator lines
- Title exactly: "Particle Flux Evolution: May 10-13, 2024" at x=0.56, y=0.968
- Multiline y-axis labels with units on second line
- Legend inside each panel, fully transparent, and non-overlapping
  - `frameon=False, framealpha=0.0, facecolor='none', edgecolor='none'`
  - Electron legend: `loc='upper right', bbox_to_anchor=(0.995, 0.34)`
  - Proton/Alpha legend: `loc='best'`
- Save `Figure_Flux_Combined_SelectedChannels.png` with dpi=300
- No storm-phase shading or storm-phase legend
"""
