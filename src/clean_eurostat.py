import pandas as pd


def clean_eurostat_tsv(filepath, value_name):
    """Clean a standard Eurostat TSV file into country-year long format.

    Expected input structure:
    - first column is a metadata column ending with geo/country code
    - remaining columns are year columns
    - values may include Eurostat flags like ':', 'p', 'e'
    """
    df = pd.read_csv(filepath, sep="	")
    df.columns = df.columns.str.strip()
    df = df.rename(columns={df.columns[0]: "metadata"})

    year_cols = [col for col in df.columns if str(col).strip().isdigit()]

    df_long = df.melt(
        id_vars="metadata",
        value_vars=year_cols,
        var_name="year",
        value_name=value_name,
    )

    df_long["country"] = df_long["metadata"].astype(str).str.split(",").str[-1]

    df_long[value_name] = (
        df_long[value_name]
        .astype(str)
        .str.replace(r"[^\d\.-]", "", regex=True)
    )

    df_long[value_name] = pd.to_numeric(df_long[value_name], errors="coerce")
    df_long["year"] = df_long["year"].astype(int)

    return df_long[["country", "year", value_name]]


def clean_government_expenditure(filepath):
    """Clean Eurostat COFOG government expenditure TSV to wide country-year format.

    Keeps:
    - unit = PC_GDP (% of GDP)
    - sector = S13 (general government)
    - na_item = TE (total expenditure)
    - selected COFOG functions used as public investment priority proxies
    """
    gov_raw = pd.read_csv(filepath, sep="	")
    gov_raw.columns = gov_raw.columns.str.strip()

    meta_col = gov_raw.columns[0]
    gov = gov_raw.copy()

    gov[["freq", "unit", "sector", "cofog99", "na_item", "country"]] = (
        gov[meta_col].str.split(",", expand=True)
    )
    gov = gov.drop(columns=[meta_col])

    gov_long = gov.melt(
        id_vars=["freq", "unit", "sector", "cofog99", "na_item", "country"],
        var_name="year",
        value_name="value",
    )

    gov_long["year"] = gov_long["year"].astype(int)
    gov_long["value"] = (
        gov_long["value"]
        .astype(str)
        .str.replace(":", "", regex=False)
        .str.replace(" p", "", regex=False)
        .str.replace(" e", "", regex=False)
        .str.strip()
    )
    gov_long["value"] = pd.to_numeric(gov_long["value"], errors="coerce")

    keep_cofog = [
        "TOTAL",  # total government expenditure
        "GF02",   # defence
        "GF04",   # economic affairs
        "GF0403", # fuel and energy
        "GF0406", # communication
        "GF05",   # environmental protection
        "GF07",   # health
        "GF09",   # education
        "GF10",   # social protection
    ]

    gov_long_filtered = gov_long[
        (gov_long["unit"] == "PC_GDP")
        & (gov_long["sector"] == "S13")
        & (gov_long["na_item"] == "TE")
        & (gov_long["cofog99"].isin(keep_cofog))
    ].copy()

    gov_wide = (
        gov_long_filtered
        .pivot_table(
            index=["country", "year"],
            columns="cofog99",
            values="value",
            aggfunc="first",
        )
        .reset_index()
    )
    gov_wide.columns.name = None

    gov_wide = gov_wide.rename(columns={
        "TOTAL": "total_gov_expenditure",
        "GF02": "defense_spending",
        "GF04": "economic_affairs_spending",
        "GF0403": "fuel_energy_spending",
        "GF0406": "communication_spending",
        "GF05": "environment_spending",
        "GF07": "health_spending",
        "GF09": "education_spending",
        "GF10": "social_protection_spending",
    })

    return gov_wide
