"""
project_reconstruction.py

Purpose:
Reload stable app exports after a notebook kernel restart.

Use this at the top of new notebooks or before continuing app/dashboard work.
"""

from pathlib import Path
import pandas as pd


APP_EXPORT_FILES = {
    "country_structural_summary_v2_dimensions": "country_structural_summary_v2_dimensions.csv",
    "country_dimension_profiles": "country_dimension_profiles.csv",
    "tradeoff_space_coordinates": "tradeoff_space_coordinates.csv",
    "pathway_dimension_signatures": "pathway_dimension_signatures.csv",
    "structural_family_metadata": "structural_family_metadata.csv",
    "tradeoff_space_classification": "tradeoff_space_classification.csv",
}


OPTIONAL_EXPORT_FILES = {
    "relative_adaptation_shift": "relative_adaptation_shift.csv",
    "investment_response_shifts": "investment_response_shifts.csv",
}


REQUIRED_STATIC_DIMENSIONS = [
    "dim_sustainability_capacity",
    "dim_innovation_capacity",
    "dim_social_stability",
    "dim_fiscal_flexibility",
    "dim_security_reprioritization",
    "dim_adaptive_transformation",
]


def load_app_exports(project_root, include_optional=True):
    """
    Load stable app export CSVs from data/app.
    """

    project_root = Path(project_root)
    app_data = project_root / "data" / "app"

    if not app_data.exists():
        raise FileNotFoundError(f"App data folder not found: {app_data}")

    tables = {}

    for table_name, filename in APP_EXPORT_FILES.items():
        path = app_data / filename

        if not path.exists():
            raise FileNotFoundError(f"Required app export missing: {path}")

        tables[table_name] = pd.read_csv(path)

    if include_optional:
        for table_name, filename in OPTIONAL_EXPORT_FILES.items():
            path = app_data / filename

            if path.exists():
                tables[table_name] = pd.read_csv(path)

    return tables


def verify_app_exports(tables):
    """
    Print basic diagnostics for loaded app exports.
    """

    print("Loaded app exports:")
    print("-" * 60)

    for table_name, df in tables.items():
        print(f"{table_name}: {df.shape}")

    print("\nCore table checks:")
    print("-" * 60)

    if "country_structural_summary_v2_dimensions" in tables:
        df = tables["country_structural_summary_v2_dimensions"]

        missing_dims = [
            col for col in REQUIRED_STATIC_DIMENSIONS
            if col not in df.columns
        ]

        if missing_dims:
            print("Missing static dimension columns:")
            print(missing_dims)
        else:
            print("All required static dimension columns found.")

        family_cols = [
            "structural_family",
            "structural_subfamily",
            "family_anchor_archetype",
            "family_color",
        ]

        missing_family_cols = [
            col for col in family_cols
            if col not in df.columns
        ]

        if missing_family_cols:
            print("Missing structural-family columns:")
            print(missing_family_cols)
        else:
            print("All structural-family columns found.")

        if "country_name" in df.columns:
            print(f"Countries loaded: {df['country_name'].nunique()}")

    print("\nVerification complete.")


def assign_common_tables_to_globals(tables, global_namespace):
    """
    Optional helper for notebooks.
    Assigns loaded tables into the notebook global namespace.
    """

    for table_name, df in tables.items():
        global_namespace[table_name] = df

    print("Assigned loaded tables to notebook globals.")
