"""
data_loader.py

Purpose
-------
Centralized data loading and preparation utilities for the
European Strategy Atlas Streamlit application.

This module converts exported capstone CSV tables into clean,
app-ready Python objects.

Why this file exists
--------------------
Streamlit pages should not repeatedly filter raw CSV tables.
Instead, each page should request prepared objects such as:

- country profile
- family profile
- dimension values
- strongest / weakest dimensions

Used by
-------
- P1 Country Explorer
- P2 Tradeoff Explorer
- P3 Strategic Choices
- P4 Challenge
- P5 Reflection

Project
-------
European Structural Topology & Strategic Pathway Explorer

Author
------
Gilad Gotesman
"""

# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path

import pandas as pd


# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# This file lives in:
# streamlit_app/utils/data_loader.py
#
# Therefore:
# Path(__file__).parent        -> streamlit_app/utils
# Path(__file__).parent.parent -> streamlit_app
# / "data"                    -> streamlit_app/data
#
# All app-ready CSV files should be stored in streamlit_app/data/

DATA_DIR = Path(__file__).parent.parent / "data"


# =============================================================================
# DIMENSION CONFIGURATION
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path
import pandas as pd

from utils.dimension_config import (
    DIMENSION_LABELS,
    DIMENSION_FORMULAS,
    COMPOSITE_DIMENSION_FORMULAS,
    DIMENSION_ORDER,
)

from utils.insight_rules import categorize_gap


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_profiles():
    """
    Load country dimension profiles.

    Source file
    -----------
    country_dimension_profiles.csv

    Expected structure
    ------------------
    One row per EU country.

    Contains:
    - country code
    - country name
    - archetype label
    - archetype type
    - core / secondary archetype flags
    - seven structural dimension scores

    Returns
    -------
    pd.DataFrame
        Country-level structural dimension profile table.

    Used by
    -------
    - P1 Country Explorer
    - P3 Strategic Choices
    - P5 Reflection
    """
    return pd.read_csv(DATA_DIR / "country_dimension_profiles.csv")


def load_families():
    """
    Load structural family metadata.

    Source file
    -----------
    structural_family_metadata.csv

    Expected structure
    ------------------
    One row per EU country.

    Contains:
    - country name
    - structural family
    - structural subfamily
    - family anchor archetype
    - family color

    Returns
    -------
    pd.DataFrame
        Country-to-family metadata table.

    Used by
    -------
    - P1 Country Explorer
    - P2 Tradeoff Explorer
    - P5 Reflection
    """
    return pd.read_csv(DATA_DIR / "structural_family_metadata.csv")


def load_country_year():
    """
    Load full country-year dataset.

    Source file
    -----------
    dashboard1_country_year_full_norm.csv

    Expected structure
    ------------------
    One row per country-year.

    Contains:
    - raw KPI values
    - period labels
    - EU-long z-scores
    - EU-year z-scores
    - country-relative z-scores

    Returns
    -------
    pd.DataFrame
        Country-year app table.

    Used by
    -------
    - P1 evolution chart
    - P2 tradeoff scatter plots
    - later dynamic pathway views
    """
    return pd.read_csv(DATA_DIR / "dashboard1_country_year_full_norm.csv")


def load_archetypes():
    """
    Load archetype reference table.

    Source file
    -----------
    dashboard1_archetypes.csv

    Expected structure
    ------------------
    One row per archetype country.

    Contains:
    - country
    - archetype label
    - archetype type

    Returns
    -------
    pd.DataFrame
        Archetype metadata table.

    Used by
    -------
    - P1 archetype cards
    - P2 archetype comparisons
    - P5 reflection summaries
    """
    return pd.read_csv(DATA_DIR / "dashboard1_archetypes.csv")


def load_signatures():
    """
    Load dynamic pathway signature table.

    Source file
    -----------
    pathway_dimension_signatures.csv

    Expected structure
    ------------------
    One row per country.

    Contains:
    - shock response signatures
    - adaptation transition signatures
    - relative adaptation shifts
    - adaptation shift flags

    Returns
    -------
    pd.DataFrame
        Dynamic pathway signature table.

    Used by
    -------
    - P1 dynamic story cards
    - P4 challenge / resilience logic later
    """
    return pd.read_csv(DATA_DIR / "pathway_dimension_signatures.csv")


def load_summary():
    """
    Load structural summary table.

    Source file
    -----------
    country_structural_summary_v2_dimensions.csv

    Expected structure
    ------------------
    One row per country.

    Contains:
    - KPI positions
    - 2014–2025 changes
    - shock shifts
    - transition shifts
    - peak / trough years
    - archetype metadata
    - seven structural dimensions

    Returns
    -------
    pd.DataFrame
        Rich country structural summary table.

    Notes
    -----
    This table is powerful but large.

    It should be used carefully in the app to avoid
    overcomplicating the MVP.

    Used by
    -------
    - later insight cards
    - validation checks
    - deeper country explanations
    """
    return pd.read_csv(DATA_DIR / "country_structural_summary_v2_dimensions.csv")


# =============================================================================
# COUNTRY PROFILE CONSTRUCTION
# =============================================================================

def build_country_profile(country_name, profiles_df, families_df):
    """
    Build a clean app-ready country profile object.

    Parameters
    ----------
    country_name : str
        Full country name, for example "Germany".

    profiles_df : pd.DataFrame
        Output of load_profiles().
        Must contain country-level dimension scores.

    families_df : pd.DataFrame
        Output of load_families().
        Must contain structural family metadata.

    Returns
    -------
    dict
        App-ready country profile object.

    Returned structure
    ------------------
    {
        "country": str,
        "country_code": str,
        "archetype": str,
        "archetype_type": str,
        "family": str,
        "subfamily": str,
        "family_anchor": str,
        "family_color": str,
        "dimensions": dict,
        "strongest_dimension": str,
        "strongest_value": float,
        "weakest_dimension": str,
        "weakest_value": float
    }

    Purpose
    -------
    This function creates a simple object that can power:

    - context ribbon
    - country story card
    - archetype card
    - family card
    - dimension snapshot
    - strengths / constraints
    - reflection page

    Notes
    -----
    This was first prototyped in:

    notebooks/09_streamlit_development.ipynb

    The Germany prototype confirmed that this object works
    for the initial P1 Country Explorer data model.
    """

    # -------------------------------------------------------------------------
    # Select country row from the profiles table
    # -------------------------------------------------------------------------

    profile_match = profiles_df.loc[
        profiles_df["country_name"] == country_name
    ]

    if profile_match.empty:
        raise ValueError(
            f"Country '{country_name}' was not found in profiles_df."
        )

    profile_row = profile_match.iloc[0]

    # -------------------------------------------------------------------------
    # Select country row from the families table
    # -------------------------------------------------------------------------

    family_match = families_df.loc[
        families_df["country_name"] == country_name
    ]

    if family_match.empty:
        raise ValueError(
            f"Country '{country_name}' was not found in families_df."
        )

    family_row = family_match.iloc[0]

    # -------------------------------------------------------------------------
    # Convert raw dimension columns into user-facing labels
    # -------------------------------------------------------------------------

    dimensions = {}

    for raw_col, display_label in DIMENSION_LABELS.items():
        dimensions[display_label] = float(profile_row[raw_col])

    # -------------------------------------------------------------------------
    # Identify strongest and weakest dimensions
    # -------------------------------------------------------------------------

    strongest_dimension = max(
        dimensions,
        key=dimensions.get
    )

    weakest_dimension = min(
        dimensions,
        key=dimensions.get
    )

    # -------------------------------------------------------------------------
    # Return app-ready dictionary
    # -------------------------------------------------------------------------

    return {
        "country": profile_row["country_name"],
        "country_code": profile_row["country"],
        "archetype": profile_row["archetype_label"],
        "archetype_type": profile_row["archetype_type"],
        "family": family_row["structural_family"],
        "subfamily": family_row["structural_subfamily"],
        "family_anchor": family_row["family_anchor_archetype"],
        "family_color": family_row["family_color"],
        "dimensions": dimensions,
        "strongest_dimension": strongest_dimension,
        "strongest_value": dimensions[strongest_dimension],
        "weakest_dimension": weakest_dimension,
        "weakest_value": dimensions[weakest_dimension],
    }








# =============================================================================
# REFERENCE / COMPARISON PROFILE CONSTRUCTION
# =============================================================================

def build_family_reference_profile(
    country_profile,
    profiles_df,
    families_df
):
    """
    Build a family-average reference profile for the selected country.

    Purpose
    -------
    Powers P1 Section 03:

    "How does this country compare?"

    This function compares the selected country to the average profile
    of its structural family.

    Parameters
    ----------
    country_profile : dict
        Output of build_country_profile().

    profiles_df : pd.DataFrame
        Output of load_profiles().

    families_df : pd.DataFrame
        Output of load_families().

    Returns
    -------
    dict
        App-ready comparison object.

    Returned structure
    ------------------
    {
        "country": str,
        "reference_type": "Family Average",
        "reference_name": str,
        "comparison": {
            dimension_label: {
                "country_value": float,
                "reference_value": float,
                "difference": float
            }
        }
    }
    """

    selected_family = country_profile["family"]
    selected_country = country_profile["country"]

    # Find all countries that belong to the same structural family.
    family_countries = families_df.loc[
        families_df["structural_family"] == selected_family,
        "country_name"
    ].tolist()

    # Keep only profile rows for countries in the same family.
    family_profiles = profiles_df.loc[
        profiles_df["country_name"].isin(family_countries)
    ].copy()

    if family_profiles.empty:
        raise ValueError(
            f"No family profiles found for family '{selected_family}'."
        )

    comparison = {}

    for raw_col, display_label in DIMENSION_LABELS.items():
        country_value = country_profile["dimensions"][display_label]

        reference_value = float(
            family_profiles[raw_col].mean()
        )

        comparison[display_label] = {
            "country_value": country_value,
            "reference_value": reference_value,
            "difference": country_value - reference_value,
        }

    return {
        "country": selected_country,
        "reference_type": "Family Average",
        "reference_name": selected_family,
        "comparison": comparison,
    }

def build_eu_reference_profile(
    country_profile,
    profiles_df
):
    """
    Build an EU-average reference profile for the selected country.

    Purpose
    -------
    Supports P1 Section 03:

    "How does this country compare?"

    This compares the selected country to the average profile
    across all EU countries in the app dataset.
    """

    selected_country = country_profile["country"]

    comparison = {}

    for raw_col, display_label in DIMENSION_LABELS.items():
        country_value = country_profile["dimensions"][display_label]

        reference_value = float(
            profiles_df[raw_col].mean()
        )

        comparison[display_label] = {
            "country_value": country_value,
            "reference_value": reference_value,
            "difference": country_value - reference_value,
        }

    return {
        "country": selected_country,
        "reference_type": "EU Average",
        "reference_name": "EU Average",
        "comparison": comparison,
    }


def build_country_reference_profile(
    country_profile,
    reference_country_name,
    profiles_df
):
    """
    Build a country-to-country reference profile.

    Purpose
    -------
    Supports P1 comparison mode:

    selected country
    vs
    another country
    """

    selected_country = country_profile["country"]

    reference_row = profiles_df.loc[
        profiles_df["country_name"] == reference_country_name
    ]

    if reference_row.empty:
        raise ValueError(
            f"Reference country '{reference_country_name}' not found."
        )

    reference_row = reference_row.iloc[0]

    comparison = {}

    for raw_col, display_label in DIMENSION_LABELS.items():
        country_value = country_profile["dimensions"][display_label]
        reference_value = float(reference_row[raw_col])

        comparison[display_label] = {
            "country_value": country_value,
            "reference_value": reference_value,
            "difference": country_value - reference_value,
        }

    return {
        "country": selected_country,
        "reference_type": "Country",
        "reference_name": reference_country_name,
        "comparison": comparison,
    }



# =============================================================================
# STORY / INSIGHT HELPERS
# =============================================================================

def create_country_story(profile):
    """
    Create a minimal country story from a country profile object.

    Parameters
    ----------
    profile : dict
        Output of build_country_profile().

    Returns
    -------
    dict
        Short story object for display in P1.

    Purpose
    -------
    Converts the technical profile object into a concise
    narrative structure.

    This can later power:
    - country story card
    - mission log summary
    - reflection page
    """

    return {
        "Country": profile["country"],
        "Family": profile["family"],
        "Archetype": profile["archetype"],
        "Strongest Dimension": profile["strongest_dimension"],
        "Main Constraint": profile["weakest_dimension"],
    }


# =============================================================================
# CONVENIENCE LOADER
# =============================================================================

def load_country_profile(country_name):
    """
    Convenience function for loading a single country profile.

    Parameters
    ----------
    country_name : str
        Full country name, for example "Germany".

    Returns
    -------
    dict
        App-ready country profile object.

    Why this exists
    ---------------
    Useful for simple Streamlit pages where we do not yet need
    full control over all loaded tables.

    Example
    -------
    germany = load_country_profile("Germany")

    Notes
    -----
    Later, when performance matters, Streamlit caching should be added
    around table loading in the Streamlit app layer using:

    @st.cache_data
    """

    profiles_df = load_profiles()
    families_df = load_families()

    return build_country_profile(
        country_name=country_name,
        profiles_df=profiles_df,
        families_df=families_df,
    )






# =============================================================================
# YEARLY DIMENSION CONSTRUCTION
# =============================================================================

def add_yearly_dimensions(country_year_df):
    """
    Reconstruct yearly structural dimensions using configured formulas.

    Purpose
    -------
    The static profile table gives one current profile per country.

    Page 1 also needs an evolution view:
    "How did this country become this way?"

    Therefore, yearly dimensions are reconstructed from:
    dashboard1_country_year_full_norm.csv

    The formulas are imported from:
    utils/dimension_config.py

    This keeps weights centralized and validation-friendly.

    Parameters
    ----------
    country_year_df : pd.DataFrame
        Country-year table containing KPI z-score columns.

    Returns
    -------
    pd.DataFrame
        Copy of input table with yearly dimension columns added.
    """

    df = country_year_df.copy()

    # -------------------------------------------------------------------------
    # Build direct KPI-based dimensions
    # -------------------------------------------------------------------------

    for output_col, formula in DIMENSION_FORMULAS.items():
        df[output_col] = 0.0

        for input_col, weight in formula.items():
            df[output_col] += weight * df[input_col]

    # -------------------------------------------------------------------------
    # Build composite dimensions from already-created dimensions
    # -------------------------------------------------------------------------

    for output_col, formula in COMPOSITE_DIMENSION_FORMULAS.items():
        df[output_col] = 0.0

        for input_col, weight in formula.items():
            df[output_col] += weight * df[input_col]

    return df


def build_country_timeline(country_name, country_year_df):
    """
    Build an app-ready yearly dimension timeline for one country.

    Purpose
    -------
    Powers P1 Section 02:

    "How did this country become this way?"

    Parameters
    ----------
    country_name : str
        Full country name, for example "Germany".

    country_year_df : pd.DataFrame
        Output of load_country_year().

    Returns
    -------
    pd.DataFrame
        Yearly dimension table for the selected country.

    Columns
    -------
    - country_name
    - year
    - seven structural dimensions
    """

    df = add_yearly_dimensions(country_year_df)

    timeline = df.loc[
        df["country_name"] == country_name,
        ["country_name", "year"] + DIMENSION_ORDER
    ].copy()

    if timeline.empty:
        raise ValueError(
            f"Country '{country_name}' was not found in country_year_df."
        )

    return timeline





def build_dimension_gap_table(comparison_profile):
    """
    Convert a comparison profile into a clean gap-analysis table.

    Keeps the approved dimension order from dimension_config.py.

    Purpose
    -------
    Powers P1 Section 03:

    "How does this country compare?"

    Notes
    -----
    gap = country - reference

    Positive gap:
        country is above reference

    Negative gap:
        country is below reference
    """

    rows = []

    for raw_col in DIMENSION_ORDER:
        dimension = DIMENSION_LABELS[raw_col]

        values = comparison_profile["comparison"][dimension]

        gap = values["difference"]

        gap_info = categorize_gap(gap)

        rows.append(
            {
                "dimension": dimension,
                "country_value": values["country_value"],
                "reference_value": values["reference_value"],
                "gap": gap,
                "gap_label": gap_info["label"],
                "gap_level": gap_info["level"],
                "gap_direction": gap_info["direction"],
                "gap_tone": gap_info["tone"],
            }
        )

    return pd.DataFrame(rows)


















