"""
dimension_config.py

Purpose
-------
Central configuration for structural dimension definitions.

This file stores:
- user-facing dimension labels
- KPI weight formulas
- display order

Why this file exists
--------------------
Dimension weights may change during validation.

Keeping formulas here prevents hardcoding them across multiple app files.

Used by
-------
- data_loader.py
- future chart utilities
- validation/debug helpers
"""

# =============================================================================
# DIMENSION LABELS
# =============================================================================

DIMENSION_LABELS = {
    "dim_sustainability_capacity": "Sustainability Capacity",
    "dim_human_capital_capacity": "Human Capital Capacity",
    "dim_innovation_capacity": "Innovation Capacity",
    "dim_social_stability": "Social Stability",
    "dim_fiscal_flexibility": "Fiscal Flexibility",
    "dim_security_reprioritization": "Security Reprioritization",
    "dim_adaptive_transformation": "Adaptive Transformation",
}


# =============================================================================
# DIMENSION FORMULAS
# =============================================================================

# Each dimension is defined as:
#
# output_dimension_column: {
#     input_kpi_zscore_column: weight
# }
#
# Positive weights increase the dimension.
# Negative weights reduce the dimension.
#
# These formulas use EU-long z-score KPI columns.

DIMENSION_FORMULAS = {
    "dim_sustainability_capacity": {
        "renewables_eu_long_zscore": 0.40,
        "environment_spending_eu_long_zscore": 0.30,
        "emissions_eu_long_zscore": -0.30,
    },
    "dim_human_capital_capacity": {
        "education_eu_long_zscore": 0.60,
        "education_spending_eu_long_zscore": 0.40,
    },
    "dim_innovation_capacity": {
        "rnd_eu_long_zscore": 0.45,
        "ict_specialists_eu_long_zscore": 0.35,
        "economic_affairs_spending_eu_long_zscore": 0.20,
    },
    "dim_social_stability": {
        "social_protection_spending_eu_long_zscore": 0.30,
        "health_spending_eu_long_zscore": 0.25,
        "unemployment_eu_long_zscore": -0.25,
        "gini_eu_long_zscore": -0.20,
    },
    "dim_fiscal_flexibility": {
        "debt_eu_long_zscore": -0.60,
        "total_gov_expenditure_eu_long_zscore": -0.40,
    },
    "dim_security_reprioritization": {
        "defense_spending_eu_long_zscore": 0.80,
        "fuel_energy_spending_eu_long_zscore": 0.20,
    },
}


# =============================================================================
# COMPOSITE DIMENSIONS
# =============================================================================

# Adaptive Transformation is currently a composite dimension.
#
# IMPORTANT:
# This dimension is already flagged for validation because it may dominate
# static profile rankings.
#
# It is therefore kept separate from direct KPI formulas.

COMPOSITE_DIMENSION_FORMULAS = {
    "dim_adaptive_transformation": {
        "dim_innovation_capacity": 0.50,
        "dim_sustainability_capacity": 0.50,
    }
}


# =============================================================================
# DISPLAY ORDER
# =============================================================================

DIMENSION_ORDER = [
    "dim_human_capital_capacity",
    "dim_innovation_capacity",
    "dim_sustainability_capacity",
    "dim_social_stability",
    "dim_fiscal_flexibility",
    "dim_security_reprioritization",
    "dim_adaptive_transformation",
]