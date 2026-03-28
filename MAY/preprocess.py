from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "MAY_2024_Master_Cleaned.csv"


def _first_match(pattern: str, description: str) -> Path:
    matches = sorted(BASE_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No {description} file found in {BASE_DIR}")
    return matches[0]


def process_omni() -> pd.DataFrame:
    """Load OMNI minute-level drivers from *.lst + *.fmt and return a time-indexed frame."""
    print("[INFO] Processing OMNI drivers")
    lst_file = _first_match("*.lst*", "OMNI .lst")
    fmt_file = _first_match("*.fmt", "OMNI .fmt")

    raw = pd.read_csv(lst_file, sep=r"\s+", header=None)

    timestamps = pd.to_datetime(
        raw[0].astype(str) + raw[1].astype(str).str.zfill(3),
        format="%Y%j",
    ) + pd.to_timedelta(raw[2], unit="h") + pd.to_timedelta(raw[3], unit="m")

    df_omni = raw.drop(columns=[0, 1, 2, 3]).copy()
    df_omni.index = timestamps

    column_names: list[str] = []
    with fmt_file.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line = line.strip()
            if line and line[0].isdigit():
                column_names.append(" ".join(line.split()[1:-1]))

    if len(column_names) == len(df_omni.columns) + 4:
        df_omni.columns = column_names[4:]

    fill_values = [99.99, 999.9, 999.99, 9999.99, 99999.9, 9999999.0]
    df_omni = df_omni.replace(fill_values, np.nan)
    return df_omni


def process_goes() -> pd.DataFrame:
    """Load GOES electron/proton/alpha fluxes and return one merged frame."""
    print("[INFO] Processing GOES fluxes")

    electron_files = sorted((BASE_DIR / "ELECTRON").glob("*.nc"))
    proton_files = sorted((BASE_DIR / "PROTON").glob("*.nc"))

    if not electron_files:
        raise FileNotFoundError(f"No electron NetCDF files found in {BASE_DIR / 'ELECTRON'}")
    if not proton_files:
        raise FileNotFoundError(f"No proton NetCDF files found in {BASE_DIR / 'PROTON'}")

    with xr.open_mfdataset([str(path) for path in electron_files], combine="by_coords") as ds_e:
        electron_flux = ds_e["AvgDiffElectronFlux"].mean(dim="telescopes").to_pandas()
    electron_flux.columns = [f"Electron_Flux_E{i + 1}" for i in range(electron_flux.shape[1])]

    with xr.open_mfdataset([str(path) for path in proton_files], combine="by_coords") as ds_p:
        proton_flux = ds_p["AvgDiffProtonFlux"].mean(dim="sensor_units").to_pandas()
        alpha_flux = ds_p["AvgDiffAlphaFlux"].mean(dim="sensor_units").to_pandas()

    proton_flux.columns = [f"Proton_Flux_P{i + 1}" for i in range(proton_flux.shape[1])]
    alpha_flux.columns = [f"Alpha_Flux_A{i + 1}" for i in range(alpha_flux.shape[1])]

    goes = pd.concat([electron_flux, proton_flux, alpha_flux], axis=1)
    goes[goes < 0] = np.nan
    return goes


def main() -> None:
    df_omni = process_omni()
    df_goes = process_goes()

    print("[INFO] Merging OMNI and GOES on datetime index")
    master = df_omni.join(df_goes, how="outer")

    master.to_csv(OUTPUT_FILE)
    print(f"[OK] Saved: {OUTPUT_FILE}")
    print(f"[OK] Shape: {master.shape}")


if __name__ == "__main__":
    main()
