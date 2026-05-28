"""Build the EU master datasets from cleaned KPI tables."""

from functools import reduce
from pathlib import Path
import pandas as pd

EU27 = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR",
    "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO",
    "SE", "SI", "SK",
]


def merge_kpis(kpi_frames: list[pd.DataFrame]) -> pd.DataFrame:
    """Outer-merge cleaned KPI dataframes on country/year."""
    return reduce(
        lambda left, right: left.merge(right, on=["country", "year"], how="outer"),
        kpi_frames,
    )


def filter_eu27_years(df: pd.DataFrame, start_year: int = 2014, end_year: int = 2025) -> pd.DataFrame:
    """Keep EU27 countries and selected years."""
    return (
        df[df["country"].isin(EU27) & df["year"].between(start_year, end_year)]
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )


def forward_fill_by_country(df: pd.DataFrame, exclude: tuple[str, ...] = ("country", "year")) -> pd.DataFrame:
    """Forward-fill missing values within each country."""
    df = df.sort_values(["country", "year"]).copy()
    value_cols = [c for c in df.columns if c not in exclude]
    df[value_cols] = df.groupby("country")[value_cols].ffill()
    return df


def save_table(df: pd.DataFrame, path: str | Path) -> None:
    """Save a dataframe and create parent folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
