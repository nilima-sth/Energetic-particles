# Figure 1 & Figure 2 Plot Requirements (Final)

## Scope
- Script: `plot_may_event.py`
- Data: `MAY_2024_Master_Cleaned.csv`
- Outputs:
  - `Figure1_IMF_SolarWind.png`
  - `Figure2_Geomagnetic_Indices.png`

## Shared Styling
- Font family: Times New Roman (`plt.rcParams["font.family"] = "Times New Roman"`)
- White axes background
- Panel border visible on all sides (all spines on, dim gray, linewidth ~0.9)
- Inward mirrored ticks:
  - x ticks on top and bottom
  - y major ticks on left and right
  - y minor ticks only on left (right minor off)
- Daily vertical separator lines at major day ticks through all panels
- Shared x-axis:
  - major ticks daily
  - minor ticks every 6 hours
  - only bottom subplot shows date labels
  - bottom x-label: `Time (UTC), May 2024`
- Label padding around 12
- Legends: no box (`frameon=False`)
- DPI: 300

## Figure 1 (IMF & Solar Wind)
- 4 stacked panels (shared x):
  1) `|B|, Bx, By, Bz`
  2) Solar wind speed
  3) Proton density + dynamic pressure (`twinx`)
  4) Interplanetary electric field `Ey`
- Keep storm-phase shading and phase labels
- Keep phase legend in panel (a)
- Global title (suptitle):
  - `Figure 1 — Interplanetary Magnetic Field and Solar Wind Conditions`
  - `May 10-13, 2024 Geomagnetic Superstorm`
  - position: roughly `x=0.56, y=0.975`

## Figure 2 (Geomagnetic Indices)
- 3 stacked panels (shared x):
  1) SYM/H + thin Bz reference (`twinx`)
  2) AE index
  3) ASY/H index
- Keep storm-phase shading and phase legend
- Keep annotations (SYM/H minimum and AE peak)
- Global title (suptitle):
  - `Figure 2 — Geomagnetic Indices Response`
  - `May 10-13, 2024 Geomagnetic Superstorm`
  - position: roughly `x=0.56, y=0.975`

## Keep / Do Not Change
- Keep all existing scientific data content and channel/index definitions.
- Keep storm-phase windows exactly as currently defined.
- Do not remove panel (a)(b)(c)(d) labels.
