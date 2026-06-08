"""
insight_rules.py

Purpose
-------
Reusable interpretation rules for the European Strategy Atlas.

This file converts technical analytical outputs into user-facing
interpretation labels.

Examples:
- z-score gap -> "slightly above reference"
- z-score gap -> "significantly below reference"

Why this file exists
--------------------
The Streamlit pages should not contain interpretation thresholds.

Keeping insight rules here makes the app:
- easier to maintain
- easier to validate
- easier to update after the validation notebook
- more transparent

Used by
-------
- P1 Country Explorer
- later P2 Tradeoff Explorer
- later P5 Reflection
"""

# =============================================================================
# GAP THRESHOLDS
# =============================================================================

# Gap thresholds are based on z-score-style dimension differences.
#
# These are not statistical significance thresholds.
# They are educational interpretation bands.
#
# The purpose is to help users understand whether a gap is:
# - negligible
# - small
# - moderate
# - large
#
# Validation note:
# These thresholds should be reviewed in the app-readiness validation notebook.

SIMILAR_THRESHOLD = 0.10
SLIGHT_THRESHOLD = 0.30
MODERATE_THRESHOLD = 0.60


# =============================================================================
# GAP INTERPRETATION
# =============================================================================

def categorize_gap(gap):
    """
    Categorize a dimension gap into a user-facing interpretation band.

    Parameters
    ----------
    gap : float
        Difference between country value and reference value.

        Example:
        Germany Innovation - Family Innovation = +0.63

    Returns
    -------
    dict
        Interpretation object.

    Returned structure
    ------------------
    {
        "level": str,
        "label": str,
        "direction": str,
        "tone": str
    }

    Notes
    -----
    Positive gap means:
    country is above the selected reference.

    Negative gap means:
    country is below the selected reference.

    This function does NOT decide whether the result is normatively good
    policy or bad policy.

    For MVP display:
    - above reference = positive tone
    - below reference = negative tone
    - similar = neutral tone
    """

    abs_gap = abs(gap)

    if abs_gap < SIMILAR_THRESHOLD:
        return {
            "level": "similar",
            "label": "Similar to reference",
            "direction": "similar",
            "tone": "neutral",
        }

    if gap > 0:
        direction = "above"
        tone = "positive"
    else:
        direction = "below"
        tone = "negative"

    if abs_gap < SLIGHT_THRESHOLD:
        strength = "Slightly"
        level = f"slightly_{direction}"
    elif abs_gap < MODERATE_THRESHOLD:
        strength = "Moderately"
        level = f"moderately_{direction}"
    else:
        strength = "Significantly"
        level = f"significantly_{direction}"

    return {
        "level": level,
        "label": f"{strength} {direction} reference",
        "direction": direction,
        "tone": tone,
    }


def format_gap(gap):
    """
    Format a numeric gap for display.

    Parameters
    ----------
    gap : float

    Returns
    -------
    str
        Gap formatted with sign and two decimals.

    Example
    -------
    +0.63
    -0.34
    """

    return f"{gap:+.2f}"





def generate_country_summary(
    country_profile,
    strengths_df,
    constraints_df
):
    """
    Generate a short structural summary.

    MVP version.
    """

    strongest_strength = strengths_df.iloc[0]["dimension"]

    strongest_constraint = constraints_df.iloc[0]["dimension"]

    country = country_profile["country"]

    return (
        f"{country} shows a structural advantage in "
        f"{strongest_strength}, while "
        f"{strongest_constraint} remains its main relative constraint."
    )




# =============================================================================
# STRENGTH / CONSTRAINT EXTRACTION
# =============================================================================

def get_key_strengths(gap_df, max_items=3):
    """
    Extract key strengths from a dimension gap dataframe.
    """

    strengths_df = gap_df.loc[
        gap_df["gap_direction"] == "above"
    ].copy()

    strengths_df = strengths_df.sort_values(
        by="gap",
        ascending=False
    )

    return strengths_df.head(max_items)


def get_key_constraints(gap_df, max_items=3):
    """
    Extract key constraints from a dimension gap dataframe.
    """

    constraints_df = gap_df.loc[
        gap_df["gap_direction"] == "below"
    ].copy()

    constraints_df = constraints_df.sort_values(
        by="gap",
        ascending=True
    )

    return constraints_df.head(max_items)

