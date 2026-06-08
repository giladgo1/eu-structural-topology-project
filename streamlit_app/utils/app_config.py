"""
app_config.py

Purpose
-------
Central app-level defaults for the European Strategy Atlas.

This file stores UI and exploration defaults.

It does NOT store dimension formulas.
Those belong in dimension_config.py.
"""



# ===============================# =============================================================================
# DEFAULT APP STATE
# =============================================================================

# Starting country shown when the application loads.
# Used across P1–P5 unless overridden by user interaction.
DEFAULT_COUNTRY = "Germany"


# =============================================================================
# DEFAULT COMPARISON SETTINGS
# =============================================================================

# Initial comparison mode shown in the Country Explorer.
#
# Available options:
# - "Family Average"
# - "EU Average"
# - "Another Country"
# Family comparison remains available as a deeper exploration layer.
DEFAULT_REFERENCE_TYPE = "EU Average"


# Default comparison country.
#
# Used only when:
# DEFAULT_REFERENCE_TYPE == "Another Country"
#
# Should normally differ from DEFAULT_COUNTRY.
DEFAULT_REFERENCE_COUNTRY = "Sweden"


# =============================================================================
# VALUE DISPLAY MODE
# =============================================================================

# MVP uses EU-relative structural dimension scores.
#
# Current implementation:
# 0      = EU average
# > 0    = Above EU average
# < 0    = Below EU average
#
# Future options may include:
# - Raw values
# - Country-relative
# - Percentile ranking
DEFAULT_VALUE_MODE = "EU-relative"
#==============================================
# PAGE LABELS
# =============================================================================

PAGE_LABELS = {
    "p0": "Landing",
    "p1": "Country Explorer",
    "p2": "Tradeoff Explorer",
    "p3": "Strategic Choices",
    "p4": "Challenge",
    "p5": "Reflection",
}


# =============================================================================
# P1 DEFAULTS
# =============================================================================

P1_TIMELINE_DIMENSIONS = [
    "dim_innovation_capacity",
    "dim_sustainability_capacity",
    "dim_social_stability",
    "dim_fiscal_flexibility",
    "dim_security_reprioritization",
]



# =============================================================================
# COUNTRY DROPDOWN ORDER
# =============================================================================

# Priority countries appear first in country selectors.
#
# Order logic:
# 1. Core archetypes
# 2. Secondary archetypes
# 3. All remaining countries alphabetically
#
# This same order is used for:
# - selected country
# - reference country

PRIORITY_COUNTRIES = [
    "Germany",
    "Sweden",
    "Netherlands",
    "Poland",
    "Spain",
    "Italy",
    "Estonia",
    "Finland",
    "Greece",
    "Romania",
]



# =============================================================================
# COUNTRY COLORS
# =============================================================================

# Country colors are used for country-specific visuals:
# - radar chart
# - timeline emphasis
# - country identity cards
#
# These are NOT family colors.
# Family colors should only be used for family overlays / grouping views.

COUNTRY_COLORS = {
    "Germany": "#A855F7",
    "Sweden": "#22C55E",
    "Netherlands": "#38BDF8",
    "Poland": "#EF4444",
    "Spain": "#F59E0B",
    "Italy": "#A855F7",
    "Estonia": "#06B6D4",
    "Finland": "#14B8A6",
    "Greece": "#FB7185",
    "Romania": "#EAB308",
}

DEFAULT_COUNTRY_COLOR = "#CBD5E1"