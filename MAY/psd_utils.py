from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import signal

RESOLUTION_SECONDS = 60


def load_master_data(path: Path | str) -> pd.DataFrame:
    """Load the cleaned May master CSV with datetime index."""
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = "datetime"
    df.index = pd.to_datetime(df.index, utc=False)
    return df


def prepare_array(series: pd.Series) -> np.ndarray:
    """Interpolate interior NaNs and fill edge NaNs before PSD estimation."""
    return (
        series.interpolate(method="linear")
        .fillna(0.0)
        .to_numpy(dtype=np.float64)
    )


def compute_welch_psd(arr: np.ndarray, *, resolution_seconds: int = RESOLUTION_SECONDS):
    """Compute two-sided Welch PSD and scale by 1/2 (legacy pipeline convention)."""
    n_samples = len(arr)
    centered = arr - np.mean(arr)
    window = signal.get_window("bartlett", n_samples)

    frequencies, psd = signal.welch(
        centered,
        fs=1.0 / resolution_seconds,
        window=window,
        nperseg=n_samples,
        nfft=n_samples,
        return_onesided=False,
    )
    return frequencies, psd / 2.0


def positive_frequency_view(frequencies: np.ndarray, psd: np.ndarray):
    """Return strictly positive-frequency portion to avoid two-sided mirror artifacts."""
    mask = frequencies > 0
    return frequencies[mask], psd[mask]
