# %% [markdown]
# # 01 Data Loading & Cleaning
# Run this after placing raw Eurostat TSV files in `data/raw/eurostat/`.

# %%
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path.cwd().parent))

from src.config import RAW_DIR, CLEANED_KPI_DIR, PROCESSED_DIR, make_dirs
from src.clean_eurostat import clean_eurostat_tsv, clean_government_expenditure
from src.build_master import merge_kpis, filter_eu27_years, forward_fill_by_country, save_table

make_dirs()

# %% [markdown]
# ## Clean structural KPI files

# %%
# Edit filenames here to match the raw files you downloaded.
kpi_files = {
    "gdp_growth.tsv": "gdp_growth",
    "inflation.tsv": "inflation",
    "unemployment.tsv": "unemployment",
    "gini.tsv": "gini",
    "education.tsv": "education",
    "rnd.tsv": "rnd",
    "ict_specialists.tsv": "ict_specialists",
    "renewables.tsv": "renewables",
    "emissions.tsv": "emissions",
    "debt.tsv": "debt",
}

cleaned_frames = []

for filename, value_name in kpi_files.items():
    filepath = RAW_DIR / filename
    df = clean_eurostat_tsv(filepath, value_name)
    save_table(df, CLEANED_KPI_DIR / f"{value_name}.csv")
    cleaned_frames.append(df)
    print(value_name, df.shape)

# %% [markdown]
# ## Build EU27 master KPI table

# %%
eu_master = merge_kpis(cleaned_frames)
eu_master = filter_eu27_years(eu_master, 2014, 2025)
eu_master_filled = forward_fill_by_country(eu_master)

save_table(eu_master_filled, PROCESSED_DIR / "eu_master_filled.csv")

print(eu_master_filled.shape)
display(eu_master_filled.head())
display(eu_master_filled.isna().sum().sort_values(ascending=False))

# %% [markdown]
# ## Add government spending layer

# %%
gov_wide = clean_government_expenditure(RAW_DIR / "government_expenditure.tsv")

spending_cols = [c for c in gov_wide.columns if c not in ["country", "year"]]
gov_wide[spending_cols] = (
    gov_wide.sort_values(["country", "year"])
    .groupby("country")[spending_cols]
    .ffill()
)

save_table(gov_wide, PROCESSED_DIR / "government_spending_wide.csv")

print(gov_wide.shape)
display(gov_wide.head())
display(gov_wide.isna().sum().sort_values(ascending=False))

# %% [markdown]
# ## Final merged dataset

# %%
eu_master_plus = eu_master_filled.merge(gov_wide, on=["country", "year"], how="left")
eu_master_plus[spending_cols] = (
    eu_master_plus.sort_values(["country", "year"])
    .groupby("country")[spending_cols]
    .ffill()
)

save_table(eu_master_plus, PROCESSED_DIR / "eu_master_plus.csv")
eu_master_plus.to_excel(PROCESSED_DIR / "eu_master_plus.xlsx", index=False)

print(eu_master_plus.shape)
display(eu_master_plus.head())
display(eu_master_plus.isna().sum().sort_values(ascending=False))
