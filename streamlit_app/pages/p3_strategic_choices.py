"""
p3_strategic_choices.py

EUROPEAN STRATEGY ATLAS — Page 3
Invest & Strategy / Sandbox current version Model 0 — v04 state/log polish

Implements:
- P2-style learning flow, right mission log, bottom journey log, CTA cards
- 5 allocation controls with +/- 5% step buttons: Education, Economic Affairs, Environment, Social Protection, Defense
- Run / Reset buttons
- Current baseline / Last run / New input
- KPI cards update only after Run Strategy Test
- Manual allocation package with total=100 validation; no hidden auto-balancing
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from components.typography import render_section_title
from components.cards import (
    render_atlas_card,
    render_hero_card,
    render_delta_card,
    render_ai_insight_panel,
)
from components.page_frame import (
    render_left_rail_placeholder,
    render_footer,
)

from utils.atlas_state import (
    init_atlas_state,
    update_atlas_context,
    add_journey_event,
    get_journey_log_df,
)
from utils.journey_progress import render_journey_progress



# =============================================================================
# LOAD GLOBAL CSS
# =============================================================================

def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# =============================================================================
# PAGE-SPECIFIC CSS
# =============================================================================

st.html(
    """
    <style>
    .p3-intro-box {
        border:1px solid rgba(56,189,248,0.34);
        border-radius:16px;
        padding:18px 22px;
        background:linear-gradient(135deg, rgba(15,23,42,0.94), rgba(15,23,42,0.70));
        margin: 2px 0 18px 0;
    }
    .p3-intro-title {
        color:#38BDF8;
        font-size:0.78rem;
        font-weight:900;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:8px;
    }
    .p3-intro-text {
        color:#E2E8F0;
        font-size:1.16rem;
        line-height:1.55;
        font-weight:700;
    }
    .p3-tension-card {
        min-height:150px;
        border-radius:16px;
        padding:17px 18px;
        background:rgba(15,23,42,0.84);
        border:1px solid rgba(148,163,184,0.22);
        box-shadow:0 0 24px rgba(0,0,0,0.20);
    }
    .p3-tension-label {
        font-size:0.76rem;
        font-weight:900;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-bottom:9px;
    }
    .p3-tension-delta {
        font-size:1.8rem;
        font-weight:950;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        line-height:1.05;
        margin:7px 0 7px 0;
    }
    .p3-tension-value {
        color:#F8FAFC;
        font-size:1.08rem;
        font-weight:900;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        line-height:1.15;
        margin-bottom:7px;
    }
    .p3-tension-sub {
        color:#E2E8F0;
        font-size:0.88rem;
        line-height:1.35;
        font-weight:800;
    }
    .p3-tension-note {
        color:#CBD5E1;
        font-size:0.84rem;
        line-height:1.34;
        margin-top:7px;
    }
    .p3-summary-card {
        min-height:230px;
        border:1px solid rgba(56,189,248,0.30);
        border-radius:16px;
        padding:16px 18px;
        background:linear-gradient(135deg, rgba(30,58,95,0.56), rgba(15,23,42,0.82));
    }
    .p3-summary-title {
        color:#38BDF8;
        font-size:0.76rem;
        font-weight:900;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:10px;
    }
    .p3-summary-row {
        display:grid;
        grid-template-columns: 1fr auto;
        gap:10px;
        padding:7px 0;
        border-bottom:1px solid rgba(148,163,184,0.13);
        color:#E2E8F0;
        font-size:0.88rem;
        line-height:1.25;
    }
    .p3-summary-value {
        color:#F8FAFC;
        font-weight:950;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
    }
    .p3-run-control-card {
        border:1px solid rgba(56,189,248,0.26);
        border-radius:16px;
        background:rgba(15,23,42,0.74);
        padding:16px 18px;
        margin:18px 0 8px 0;
    }
    .p3-allocation-table {
        width:100%;
        border-collapse:collapse;
        color:#E5E7EB;
        font-size:0.84rem;
        margin-top:12px;
        table-layout:fixed;
    }
    .p3-allocation-table th {
        color:#38BDF8;
        font-size:0.70rem;
        letter-spacing:0.08em;
        text-transform:uppercase;
        padding:9px 8px;
        border-bottom:1px solid rgba(56,189,248,0.28);
        text-align:left;
    }
    .p3-allocation-table td {
        padding:9px 8px;
        border-bottom:1px solid rgba(148,163,184,0.14);
        vertical-align:top;
    }
    .p3-allocation-card {
        border:1px solid rgba(56,189,248,0.28);
        border-radius:16px;
        padding:15px 17px;
        background:rgba(15,23,42,0.78);
        margin-top:10px;
    }
    .p3-section-hint {
        color:#CBD5E1;
        font-size:0.98rem;
        line-height:1.45;
        margin-bottom:12px;
    }
    .p3-log-panel {
        position:sticky;
        top:210px;
        border:1px solid rgba(56,189,248,0.32);
        border-radius:16px;
        padding:17px;
        background:linear-gradient(135deg, rgba(15,23,42,0.94), rgba(15,23,42,0.72));
    }
    .p3-log-title {
        color:#38BDF8;
        font-size:0.76rem;
        font-weight:900;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:14px;
    }
    .p3-log-heading {
        color:#F8FAFC;
        font-size:0.94rem;
        font-weight:900;
        margin-top:12px;
        margin-bottom:7px;
    }
    .p3-log-text {
        color:#CBD5E1;
        font-size:0.86rem;
        line-height:1.42;
    }
    .p3-run-state {
        border-radius:12px;
        padding:11px 14px;
        border:1px solid rgba(148,163,184,0.24);
        background:rgba(15,23,42,0.74);
        color:#E2E8F0;
        font-size:0.90rem;
        font-weight:750;
        line-height:1.35;
    }

    .p3-mission-explainer {
        border:1px solid rgba(168,85,247,0.32);
        border-radius:16px;
        padding:14px 17px;
        background:linear-gradient(135deg, rgba(88,28,135,0.24), rgba(15,23,42,0.72));
        margin: 0 0 14px 0;
    }
    .p3-mission-explainer-title {
        color:#C084FC;
        font-size:0.78rem;
        font-weight:900;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:7px;
    }
    .p3-mission-explainer-text {
        color:#E2E8F0;
        font-size:1.02rem;
        line-height:1.45;
        font-weight:700;
    }
    .p3-stepper-value {
        text-align:center;
        color:#F8FAFC;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:1.02rem;
        font-weight:950;
        padding-top:0.48rem;
        white-space:nowrap;
        min-width:44px;
    }
    .p3-row-delta {
        font-weight:950;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.92rem;
        text-align:right;
        padding-top:0.55rem;
        white-space:nowrap;
    }
    .p3-nowrap {
        white-space:nowrap;
    }
    .p3-choice-help {
        border:1px solid rgba(56,189,248,0.28);
        border-left:4px solid #38BDF8;
        border-radius:14px;
        padding:12px 13px;
        background:rgba(15,23,42,0.76);
        margin:0 0 12px 0;
    }
    .p3-choice-help-title {
        color:#38BDF8;
        font-size:0.70rem;
        font-weight:900;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:6px;
    }
    .p3-choice-help-text {
        color:#E2E8F0;
        font-size:0.86rem;
        line-height:1.34;
        font-weight:700;
    }
    .p3-run-ready-note {
        border-radius:12px;
        padding:10px 12px;
        margin:10px 0 12px 0;
        font-size:0.84rem;
        font-weight:850;
        line-height:1.32;
        border:1px solid rgba(148,163,184,0.22);
    }

    .p3-output-table-card {
        border:1px solid rgba(56,189,248,0.36);
        border-radius:16px;
        padding:17px 18px;
        background:rgba(15,23,42,0.80);
        margin-top:8px;
        box-shadow:0 0 22px rgba(56,189,248,0.08);
    }
    .p3-output-table-title {
        color:#F8FAFC;
        font-size:1.12rem;
        font-weight:950;
        margin-bottom:6px;
    }
    .p3-output-table-subtitle {
        color:#CBD5E1;
        font-size:0.88rem;
        line-height:1.36;
        margin-bottom:13px;
    }
    .p3-output-table {
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        color:#E5E7EB;
        font-size:0.92rem;
    }
    .p3-output-table th {
        color:#38BDF8;
        font-size:0.74rem;
        font-weight:900;
        letter-spacing:0.06em;
        text-transform:uppercase;
        text-align:left;
        padding:10px 8px;
        border-bottom:1px solid rgba(56,189,248,0.32);
        white-space:nowrap;
    }
    .p3-output-table td {
        padding:12px 8px;
        border-bottom:1px solid rgba(148,163,184,0.18);
        vertical-align:middle;
        line-height:1.28;
    }
    .p3-output-name {
        color:#F8FAFC;
        font-size:0.94rem;
        font-weight:900;
        line-height:1.2;
    }
    .p3-output-score {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.96rem;
        font-weight:950;
        color:#F8FAFC;
        white-space:nowrap;
    }
    .p3-output-delta {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:1.08rem;
        font-weight:950;
        white-space:nowrap;
    }
    .p3-output-reading {
        font-size:0.88rem;
        font-weight:900;
        line-height:1.22;
    }
    .p3-mini-summary-grid {
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:10px;
        margin:0 0 14px 0;
    }
    .p3-mini-summary-card {
        border:1px solid rgba(148,163,184,0.24);
        border-radius:12px;
        padding:12px 12px;
        background:rgba(2,6,23,0.36);
        min-height:94px;
    }
    .p3-mini-summary-label {
        color:#94A3B8;
        font-size:0.68rem;
        font-weight:900;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-bottom:7px;
    }
    .p3-mini-summary-value {
        color:#F8FAFC;
        font-size:0.98rem;
        font-weight:950;
        line-height:1.18;
    }
    .p3-mini-summary-delta {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.96rem;
        font-weight:950;
        margin-top:6px;
    }

    .p3-full-width-shell {
        max-width:1500px;
        margin: 0 auto;
    }
    .p3-allocation-card + div {
        margin-top: 4px;
    }


    /* P3 current version compact strategy workspace: simulate the successful 80% view only inside Section 02. */
    .st-key-p3_strategy_workspace {
        zoom: 0.90;
        transform-origin: top left;
    }
    .st-key-p3_strategy_workspace h3 {
        font-size: 1.02rem !important;
        margin: 0.15rem 0 0.35rem 0 !important;
    }
    .st-key-p3_strategy_workspace .p3-section-hint {
        font-size: 0.86rem;
        line-height: 1.32;
        margin-bottom: 8px;
    }
    .st-key-p3_strategy_workspace .p3-choice-help {
        padding: 10px 11px;
        margin-bottom: 8px;
    }
    .st-key-p3_strategy_workspace .p3-choice-help-text {
        font-size: 0.84rem;
        line-height: 1.26;
    }
    .st-key-p3_strategy_workspace .p3-allocation-card {
        padding: 12px 13px;
        margin-top: 6px;
    }
    .st-key-p3_strategy_workspace .p3-stepper-value {
        font-size: 0.94rem;
        padding-top: 0.38rem;
    }
    .st-key-p3_strategy_workspace .p3-row-delta {
        font-size: 0.86rem;
    }
    .st-key-p3_strategy_workspace .p3-output-table-card {
        padding: 13px 14px;
    }
    .st-key-p3_strategy_workspace .p3-output-table-title {
        font-size: 1.02rem;
    }
    .st-key-p3_strategy_workspace .p3-output-table-subtitle {
        font-size: 0.84rem;
        margin-bottom: 9px;
    }
    .st-key-p3_strategy_workspace .p3-mini-summary-grid {
        gap: 7px;
        margin-bottom: 9px;
    }
    .st-key-p3_strategy_workspace .p3-mini-summary-card {
        min-height: 76px;
        padding: 9px 9px;
    }
    .st-key-p3_strategy_workspace .p3-mini-summary-value {
        font-size: 0.86rem;
    }
    .st-key-p3_strategy_workspace .p3-mini-summary-delta {
        font-size: 0.84rem;
    }
    .st-key-p3_strategy_workspace .p3-output-table {
        font-size: 0.86rem;
    }
    .st-key-p3_strategy_workspace .p3-output-table td {
        padding: 8px 6px;
    }
    .st-key-p3_strategy_workspace .p3-output-table th {
        padding: 7px 6px;
        font-size: 0.70rem;
    }
    .st-key-p3_strategy_workspace div[data-testid="stButton"] button {
        min-height: 2.25rem;
        padding: 0.35rem 0.55rem;
        font-size: 0.86rem;
        line-height: 1.2;
    }

    </style>
    """
)


# =============================================================================
# NAVIGATION HELPER
# =============================================================================

def safe_switch_page(page_path: str):
    try:
        st.switch_page(page_path)
    except Exception:
        st.info(f"Navigation target not found yet: {page_path}")


# =============================================================================
# DATA LOADING
# =============================================================================

APP_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "app"
FALLBACK_DATA_DIR = Path("/mnt/data")


def read_app_csv(filename: str) -> pd.DataFrame:
    app_path = APP_DATA_DIR / filename
    fallback_path = FALLBACK_DATA_DIR / filename

    if app_path.exists():
        return pd.read_csv(app_path)
    if fallback_path.exists():
        return pd.read_csv(fallback_path)

    raise FileNotFoundError(f"Could not find {filename} in data/app or /mnt/data.")


@st.cache_data
def load_p3_data():
    country_year = read_app_csv("dashboard1_country_year_full_norm.csv")
    dimension_profiles = read_app_csv("country_dimension_profiles.csv")
    family_metadata = read_app_csv("structural_family_metadata.csv")
    response_matrix = read_app_csv("sandbox_response_matrix_v1.csv")
    family_weights = read_app_csv("sandbox_response_family_weights_v1.csv")
    interpretation_registry = read_app_csv("interpretation_registry_v1.csv")
    tradeoff_interpretation = read_app_csv("tradeoff_interpretation_registry_v1.csv")

    try:
        validation_registry = read_app_csv("sandbox_validation_registry_v1.csv")
    except FileNotFoundError:
        validation_registry = pd.DataFrame()

    country_profiles = dimension_profiles.merge(
        family_metadata[
            [
                "country_name",
                "structural_family",
                "structural_subfamily",
                "family_anchor_archetype",
                "family_color",
            ]
        ],
        on="country_name",
        how="left",
    )

    return {
        "country_year": country_year,
        "country_profiles": country_profiles,
        "response_matrix": response_matrix,
        "family_weights": family_weights,
        "interpretation_registry": interpretation_registry,
        "tradeoff_interpretation": tradeoff_interpretation,
        "validation_registry": validation_registry,
    }


DATA = load_p3_data()


# =============================================================================
# MODEL 0 REGISTRIES
# =============================================================================

SLIDER_NAMES = [
    "Education",
    "Economic Affairs",
    "Environment",
    "Social Protection",
    "Defense",
]

SPENDING_COLUMNS = {
    "Education": "education_spending",
    "Economic Affairs": "economic_affairs_spending",
    "Environment": "environment_spending",
    "Social Protection": "social_protection_spending",
    "Defense": "defense_spending",
}

DIMENSION_COLUMNS = {
    "Human Capital": "dim_human_capital_capacity",
    "Innovation": "dim_innovation_capacity",
    "Sustainability": "dim_sustainability_capacity",
    "Social Stability": "dim_social_stability",
    "Fiscal Flexibility": "dim_fiscal_flexibility",
    "Security": "dim_security_reprioritization",
    "Adaptive Transformation": "dim_adaptive_transformation",
}

STRATEGY_PRESETS = {
    "Balanced Development": {
        "Education": 20,
        "Economic Affairs": 20,
        "Environment": 20,
        "Social Protection": 25,
        "Defense": 15,
    },
    "Innovation First": {
        "Education": 30,
        "Economic Affairs": 30,
        "Environment": 15,
        "Social Protection": 15,
        "Defense": 10,
    },
    "Sustainability First": {
        "Education": 20,
        "Economic Affairs": 15,
        "Environment": 35,
        "Social Protection": 20,
        "Defense": 10,
    },
    "Social Stability First": {
        "Education": 20,
        "Economic Affairs": 15,
        "Environment": 15,
        "Social Protection": 40,
        "Defense": 10,
    },
    "Security Focus": {
        "Education": 20,
        "Economic Affairs": 15,
        "Environment": 15,
        "Social Protection": 20,
        "Defense": 30,
    },
}

STRATEGY_DESCRIPTIONS = {
    "Balanced Development": "Preserve equilibrium across competing objectives.",
    "Innovation First": "Strengthen future growth through knowledge and technology.",
    "Sustainability First": "Accelerate sustainability while preserving competitiveness.",
    "Social Stability First": "Prioritize cohesion, wellbeing, and social resilience.",
    "Security Focus": "Increase resilience under geopolitical pressure.",
}

STRATEGY_COLORS = {
    "Balanced Development": "#22D3EE",
    "Innovation First": "#A855F7",
    "Sustainability First": "#84CC16",
    "Social Stability First": "#F59E0B",
    "Security Focus": "#60A5FA",
}

SLIDER_COLORS = {
    "Education": "#60A5FA",
    "Economic Affairs": "#94A3B8",
    "Environment": "#84CC16",
    "Social Protection": "#F59E0B",
    "Defense": "#8B5CF6",
}

SLIDER_SHORT_LABELS = {
    "Education": "Education",
    "Economic Affairs": "Economic",
    "Environment": "Environment",
    "Social Protection": "Social",
    "Defense": "Defense",
}

# Transparent current version direction layer.
RESPONSE_DIRECTION = {
    ("Education", "Human Capital"): 1,
    ("Education", "Innovation"): 1,
    ("Education", "Social Stability"): 1,
    ("Education", "Sustainability"): 1,
    ("Education", "Fiscal Flexibility"): -1,
    ("Economic Affairs", "Innovation"): 1,
    ("Economic Affairs", "Sustainability"): 1,
    ("Economic Affairs", "Adaptive Transformation"): 1,
    ("Economic Affairs", "Fiscal Flexibility"): -1,
    ("Environment", "Sustainability"): 1,
    ("Environment", "Adaptive Transformation"): 1,
    ("Social Protection", "Social Stability"): 1,
    ("Social Protection", "Innovation"): 1,
    ("Social Protection", "Adaptive Transformation"): 1,
    ("Social Protection", "Fiscal Flexibility"): -1,
    ("Defense", "Security"): 1,
    ("Defense", "Adaptive Transformation"): 1,
    ("Defense", "Fiscal Flexibility"): -1,
}

OUTPUT_REGISTRY = {
    "Growth Potential": {
        "dimensions": ["Innovation", "Human Capital", "Adaptive Transformation"],
        "mode": "higher_is_better",
    },
    "Innovation Readiness": {
        "dimensions": ["Innovation"],
        "mode": "higher_is_better",
    },
    "Sustainability Performance": {
        "dimensions": ["Sustainability"],
        "mode": "higher_is_better",
    },
    "Social Cohesion": {
        "dimensions": ["Social Stability", "Human Capital"],
        "mode": "higher_is_better",
    },
    "Fiscal Pressure": {
        "dimensions": ["Fiscal Flexibility"],
        "mode": "lower_is_better",
    },
    "Resilience": {
        "dimensions": [
            "Adaptive Transformation",
            "Social Stability",
            "Sustainability",
            "Security",
        ],
        "mode": "higher_is_better",
    },
}

RESPONSE_SCALE = 0.45


# =============================================================================
# MODEL HELPERS
# =============================================================================

def normalize_to_100(values: dict[str, float]) -> dict[str, int]:
    total = sum(values.values())
    if total <= 0:
        return STRATEGY_PRESETS["Balanced Development"].copy()

    normalized = {
        key: int(round(value / total * 100 / 5) * 5)
        for key, value in values.items()
    }

    diff = 100 - sum(normalized.values())
    if diff != 0:
        largest_key = max(normalized, key=normalized.get)
        normalized[largest_key] += diff

    return normalized


def get_country_baseline_allocation(country_year: pd.DataFrame, country: str) -> dict[str, int]:
    country_rows = country_year[country_year["country_name"] == country].copy()
    if country_rows.empty:
        return STRATEGY_PRESETS["Balanced Development"].copy()

    latest_year = country_rows["year"].max()
    latest_row = country_rows[country_rows["year"] == latest_year].iloc[0]

    raw_values = {
        slider_name: float(latest_row.get(column_name, 0) or 0)
        for slider_name, column_name in SPENDING_COLUMNS.items()
    }

    return normalize_to_100(raw_values)


def get_country_profile(country_profiles: pd.DataFrame, country: str) -> pd.Series:
    rows = country_profiles[country_profiles["country_name"] == country]
    if rows.empty:
        return country_profiles.iloc[0]
    return rows.iloc[0]


def z_to_index(z_value: float) -> float:
    if pd.isna(z_value):
        return 50.0
    return float(np.clip(50 + 15 * float(z_value), 0, 100))


def get_baseline_dimensions(country_profile: pd.Series) -> dict[str, float]:
    return {
        dim_name: z_to_index(country_profile.get(col_name, 0))
        for dim_name, col_name in DIMENSION_COLUMNS.items()
    }


def get_baseline_dimension_z(country_profile: pd.Series) -> dict[str, float]:
    return {
        dim_name: float(country_profile.get(col_name, 0) or 0)
        for dim_name, col_name in DIMENSION_COLUMNS.items()
    }


def get_effective_weight(source: str, target: str, family: str, family_weights: pd.DataFrame) -> float:
    rows = family_weights[
        (family_weights["layer"] == "Investment")
        & (family_weights["source"] == source)
        & (family_weights["target"] == target)
    ].copy()

    if rows.empty:
        return 0.0

    family_rows = rows[rows["structural_family"] == family]
    if not family_rows.empty:
        return float(family_rows.iloc[0]["effective_weight"])

    generic_rows = rows[rows["structural_family"].isna()]
    if not generic_rows.empty:
        return float(generic_rows.iloc[0]["effective_weight"])

    return float(rows.iloc[0]["effective_weight"])


def calculate_dimension_after(
    baseline_dimensions: dict[str, float],
    baseline_allocation: dict[str, int],
    proposed_allocation: dict[str, int],
    family: str,
    family_weights: pd.DataFrame,
) -> tuple[dict[str, float], dict[str, float]]:
    dimension_delta = {dim_name: 0.0 for dim_name in baseline_dimensions.keys()}

    for source in SLIDER_NAMES:
        allocation_change = proposed_allocation[source] - baseline_allocation[source]
        for target in dimension_delta.keys():
            direction = RESPONSE_DIRECTION.get((source, target), 0)
            if direction == 0:
                continue

            effective_weight = get_effective_weight(source, target, family, family_weights)
            dimension_delta[target] += allocation_change * (effective_weight / 100) * direction * RESPONSE_SCALE

    after_dimensions = {
        dim_name: float(np.clip(baseline_dimensions[dim_name] + dimension_delta[dim_name], 0, 100))
        for dim_name in baseline_dimensions.keys()
    }

    return after_dimensions, dimension_delta


def calculate_outputs(dimensions: dict[str, float]) -> dict[str, float]:
    outputs = {}
    for output_name, config in OUTPUT_REGISTRY.items():
        raw_score = float(np.mean([dimensions[dim] for dim in config["dimensions"]]))
        outputs[output_name] = 100 - raw_score if config["mode"] == "lower_is_better" else raw_score
    return outputs


def get_largest_gain_cost(output_before: dict[str, float], output_after: dict[str, float]):
    deltas = {name: output_after[name] - output_before[name] for name in output_before.keys()}
    gain_name = max(deltas, key=deltas.get)
    cost_name = min(deltas, key=deltas.get)
    return gain_name, deltas[gain_name], cost_name, deltas[cost_name], deltas


def classify_delta(delta: float, output_name: str) -> str:
    if output_name == "Fiscal Pressure":
        if delta > 4:
            return "Pressure increased."
        if delta < -4:
            return "Pressure decreased."
        return "Mostly stable."
    if delta > 4:
        return "Meaningful gain."
    if delta < -4:
        return "Visible tradeoff."
    return "Mostly stable."


def get_delta_color_by_value(delta: float, output_name: str = "") -> str:
    if output_name == "Fiscal Pressure":
        if delta > 1:
            return "#F472B6"
        if delta < -1:
            return "#4ADE80"
        return "#38BDF8"
    if delta > 1:
        return "#4ADE80"
    if delta < -1:
        return "#F472B6"
    return "#38BDF8"


def get_evidence_summary(response_matrix: pd.DataFrame, proposed_allocation: dict[str, int], baseline_allocation: dict[str, int]) -> str:
    changed_sources = [s for s in SLIDER_NAMES if proposed_allocation[s] != baseline_allocation[s]]
    rows = response_matrix[
        (response_matrix["layer"] == "Investment")
        & (response_matrix["source"].isin(changed_sources))
    ]
    if rows.empty:
        return "No active change"

    counts = rows["evidence_level"].value_counts().to_dict()
    return " · ".join(f"{level}:{count}" for level, count in sorted(counts.items()))



def get_evidence_confidence(response_matrix: pd.DataFrame, proposed_allocation: dict[str, int], baseline_allocation: dict[str, int]) -> tuple[int, str, str]:
    """Collapse A/B/C/D evidence into one readable confidence score."""
    changed_sources = [s for s in SLIDER_NAMES if proposed_allocation[s] != baseline_allocation[s]]
    rows = response_matrix[
        (response_matrix["layer"] == "Investment")
        & (response_matrix["source"].isin(changed_sources))
    ]

    if rows.empty:
        return 0, "No active change", "Run a strategy change to activate evidence relationships."

    score_map = {"A": 100, "B": 75, "C": 50, "D": 25}
    evidence_scores = [score_map.get(str(level), 25) for level in rows["evidence_level"]]
    confidence_score = int(round(float(np.mean(evidence_scores))))

    if confidence_score >= 75:
        confidence_label = "Strong"
        confidence_text = "Most activated relationships are supported by stronger evidence classes."
    elif confidence_score >= 55:
        confidence_label = "Moderate"
        confidence_text = "The strategy combines stronger and exploratory relationships."
    elif confidence_score >= 35:
        confidence_label = "Exploratory"
        confidence_text = "Many activated relationships are exploratory; read results as directional signals."
    else:
        confidence_label = "Low"
        confidence_text = "Most activated relationships are weak or highly exploratory."

    return confidence_score, confidence_label, confidence_text


def allocation_to_text(allocation: dict[str, int]) -> str:
    return " | ".join(f"{key}: {value}%" for key, value in allocation.items())


# =============================================================================
# UI HELPERS
# =============================================================================

def render_page_intro():
    st.html(
        """
        <div class="p3-intro-box">
            <div class="p3-intro-title">How to use this page</div>
            <div class="p3-intro-text">
                This page compares the selected country’s current investment profile with predefined or custom strategy packages.
                Choose a package, adjust the five priority shares in 5% steps, run the test, and observe how output dimensions change.
                Outputs update only after <b>Run Strategy Test</b>, so this remains an educational sandbox — not a forecast or live dashboard.
            </div>
        </div>
        """
    )


def render_tension_card(title: str, index_value: float, z_value: float, body: str, accent: str, reference_label: str = "Europe"):
    """Strategic tension card: comparison first, raw index second."""
    distance = index_value - 50

    if abs(distance) < 0.5:
        delta_text = f"≈ 0 vs {reference_label}"
        position_text = f"Near {reference_label} baseline"
        delta_symbol = "≈"
    elif distance > 0:
        delta_text = f"▲ +{distance:.0f} vs {reference_label}"
        position_text = f"Above {reference_label} baseline"
        delta_symbol = "▲"
    else:
        delta_text = f"▼ -{abs(distance):.0f} vs {reference_label}"
        position_text = f"Below {reference_label} baseline"
        delta_symbol = "▼"

    st.html(
        f"""
        <div class="p3-tension-card" style="border-left:5px solid {accent}; box-shadow:0 0 18px {accent}22;">
            <div class="p3-tension-label" style="color:{accent};">{title}</div>
            <div class="p3-tension-delta" style="color:{accent};">{delta_text}</div>
            <div class="p3-tension-value">{index_value:.0f} / 100</div>
            <div class="p3-tension-sub">{position_text}</div>
            <div class="p3-tension-note">{body}</div>
        </div>
        """
    )


def render_allocation_table(current: dict[str, int], last_run: dict[str, int], new: dict[str, int]):
    rows = []
    for name in SLIDER_NAMES:
        change = new[name] - current[name]
        color = "#4ADE80" if change > 0 else "#F472B6" if change < 0 else "#CBD5E1"
        rows.append(
            f"""
            <tr>
                <td><span style="color:{SLIDER_COLORS[name]}; font-weight:900;">{name}</span></td>
                <td>{current[name]}%</td>
                <td>{last_run[name]}%</td>
                <td>{new[name]}%</td>
                <td style="color:{color}; font-weight:900;">{change:+d}%</td>
            </tr>
            """
        )

    st.html(
        f"""
        <div class="p3-allocation-card">
            <div style="color:#F8FAFC; font-size:1rem; font-weight:900; margin-bottom:4px;">Allocation Comparison</div>
            <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">
                Current = country baseline. Last Run = last executed test. New = editable allocation waiting for Run.
            </div>
            <table class="p3-allocation-table">
                <thead>
                    <tr>
                        <th>Lever</th>
                        <th>Current</th>
                        <th>Last Run</th>
                        <th>New</th>
                        <th>Δ vs Current</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )


def render_strategy_summary(
    current: dict[str, int],
    mission: dict[str, int],
    last_run: dict[str, int],
    new: dict[str, int],
    strategy_name: str,
    total: int,
):
    """Right-side summary for Section 03. It explains the package before results."""
    changes = {name: new[name] - current[name] for name in SLIDER_NAMES}
    largest_increase = max(changes.items(), key=lambda item: item[1])
    largest_decrease = min(changes.items(), key=lambda item: item[1])

    if total == 100:
        readiness = "✓ Ready to Run"
        readiness_color = "#4ADE80"
        readiness_text = "The new package totals 100%. Press Run Strategy Test when ready."
    elif total < 100:
        readiness = f"Add {100 - total}%"
        readiness_color = "#F59E0B"
        readiness_text = "The package is under-allocated. Add the remaining share before running."
    else:
        readiness = f"Reduce {total - 100}%"
        readiness_color = "#F472B6"
        readiness_text = "The package is over-allocated. Reduce priorities before running."

    st.html(
        f"""
        <div class="p3-summary-card">
            <div class="p3-summary-title">Strategy Package Summary</div>
            <div class="p3-summary-row">
                <span>Selected mission</span>
                <span class="p3-summary-value">{strategy_name}</span>
            </div>
            <div class="p3-summary-row">
                <span>New package total</span>
                <span class="p3-summary-value" style="color:{readiness_color};">{total}%</span>
            </div>
            <div class="p3-summary-row">
                <span>Largest increase</span>
                <span class="p3-summary-value" style="color:#4ADE80;">{largest_increase[0]} {largest_increase[1]:+d}%</span>
            </div>
            <div class="p3-summary-row">
                <span>Largest decrease</span>
                <span class="p3-summary-value" style="color:#F472B6;">{largest_decrease[0]} {largest_decrease[1]:+d}%</span>
            </div>
            <div style="margin-top:14px; color:{readiness_color}; font-size:1.05rem; font-weight:950;">
                {readiness}
            </div>
            <div style="margin-top:6px; color:#CBD5E1; font-size:0.86rem; line-height:1.35;">
                {readiness_text}<br>
                Current = baseline · Mission = preset · Last = last executed run · New = waiting package.
            </div>
        </div>
        """
    )


def render_output_card(title: str, before: float, after: float):
    delta = after - before
    accent = get_delta_color_by_value(delta, title)
    arrow = "↑" if delta > 1 else "↓" if delta < -1 else "→"
    st.html(
        f"""
        <div style="
            min-height:132px;
            border-radius:16px;
            border:1px solid {accent}88;
            background:rgba(15,23,42,0.82);
            padding:16px 17px;
            box-shadow:0 0 18px {accent}18;
        ">
            <div style="color:{accent}; font-size:0.78rem; font-weight:900; letter-spacing:0.07em; text-transform:uppercase; margin-bottom:10px;">{title}</div>
            <div style="color:#F8FAFC; font-family:'IBM Plex Mono','Roboto Mono',monospace; font-size:1.55rem; font-weight:950; line-height:1.1; margin-bottom:8px;">{before:.0f} → {after:.0f}</div>
            <div style="color:{accent}; font-size:1.05rem; font-weight:950; margin-bottom:6px;">Δ {delta:+.1f} {arrow}</div>
            <div style="color:#CBD5E1; font-size:0.78rem; line-height:1.28; margin-bottom:4px;">Scale: 0–100 structural index</div>
            <div style="color:#E2E8F0; font-size:0.86rem; line-height:1.32; font-weight:700;">{classify_delta(delta, title)}</div>
        </div>
        """
    )




def render_p3_result_card(title: str, value: str, detail: str, status: str, accent: str):
    """Compact result card with visible feeling color in the main value."""
    st.html(
        f"""
        <div style="
            min-height:116px;
            border-radius:16px;
            border:1px solid {accent}66;
            border-left:5px solid {accent};
            background:rgba(30,58,95,0.58);
            padding:14px 16px;
            box-shadow:0 0 18px {accent}18;
        ">
            <div style="color:#F8FAFC; font-size:0.88rem; font-weight:900; margin-bottom:8px;">{title}</div>
            <div style="color:{accent}; font-family:'IBM Plex Mono','Roboto Mono',monospace; font-size:1.34rem; font-weight:950; line-height:1.12; margin-bottom:7px;">{value}</div>
            <div style="color:{accent}; font-size:0.88rem; font-weight:900; line-height:1.28; margin-bottom:6px;">{detail}</div>
            <div style="color:#E2E8F0; font-size:0.82rem; line-height:1.32; font-weight:700;">{status}</div>
        </div>
        """
    )


def render_strategy_test_results_table(last_outputs: dict[str, float], test_outputs: dict[str, float], gain_name: str, gain_delta: float, cost_name: str, cost_delta: float, confidence_score: int, confidence_label: str):
    """Compact table replacing the 2×3 output cards in the strategy workspace."""
    rows = []
    for output_name in OUTPUT_REGISTRY.keys():
        last_value = last_outputs[output_name]
        test_value = test_outputs[output_name]
        delta = test_value - last_value
        accent = get_delta_color_by_value(delta, output_name)
        arrow = "▲" if delta > 1 else "▼" if delta < -1 else "→"
        reading = classify_delta(delta, output_name).replace(".", "")
        rows.append(
            f"""
            <tr>
                <td><span class="p3-output-name">{output_name}</span></td>
                <td><span class="p3-output-score">{last_value:.0f}</span></td>
                <td><span class="p3-output-score">{test_value:.0f}</span></td>
                <td><span class="p3-output-delta" style="color:{accent};">{arrow} {delta:+.1f}</span></td>
                <td><span class="p3-output-reading" style="color:{accent};">{reading}</span></td>
            </tr>
            """
        )

    gain_color = get_delta_color_by_value(gain_delta, gain_name)
    cost_color = get_delta_color_by_value(cost_delta, cost_name)
    confidence_color = "#4ADE80" if confidence_score >= 75 else "#EAB308" if confidence_score >= 55 else "#F59E0B" if confidence_score >= 35 else "#F472B6"

    st.html(
        f"""
        <div class="p3-output-table-card">
            <div class="p3-output-table-title">Strategy Test Results</div>
            <div class="p3-output-table-subtitle">
                <b>Last</b> = country baseline before the test · <b>Test</b> = last executed strategy package · scale: 0–100 structural index.
            </div>

            <div class="p3-mini-summary-grid">
                <div class="p3-mini-summary-card">
                    <div class="p3-mini-summary-label">Largest Gain</div>
                    <div class="p3-mini-summary-value">{gain_name}</div>
                    <div class="p3-mini-summary-delta" style="color:{gain_color};">{gain_delta:+.1f}</div>
                </div>
                <div class="p3-mini-summary-card">
                    <div class="p3-mini-summary-label">Largest Cost</div>
                    <div class="p3-mini-summary-value">{cost_name}</div>
                    <div class="p3-mini-summary-delta" style="color:{cost_color};">{cost_delta:+.1f}</div>
                </div>
                <div class="p3-mini-summary-card">
                    <div class="p3-mini-summary-label">Evidence</div>
                    <div class="p3-mini-summary-value" style="color:{confidence_color};">{confidence_score} / 100</div>
                    <div class="p3-mini-summary-delta" style="color:{confidence_color};">{confidence_label}</div>
                </div>
            </div>

            <table class="p3-output-table">
                <colgroup>
                    <col style="width:32%;">
                    <col style="width:12%;">
                    <col style="width:12%;">
                    <col style="width:18%;">
                    <col style="width:26%;">
                </colgroup>
                <thead>
                    <tr>
                        <th>Output</th>
                        <th>Last</th>
                        <th>Test</th>
                        <th>Δ</th>
                        <th>Reading</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )

def render_p3_mission_log_panel(entry: dict):
    st.html(
        f"""
        <div class="p3-log-panel">
            <div class="p3-log-title">Mission Log</div>
            <div class="p3-log-heading">Current Mission</div>
            <div class="p3-log-text">{entry.get('strategy', 'No strategy selected')}</div>
            <div class="p3-log-heading">Latest Learning</div>
            <div class="p3-log-text">{entry.get('learning', 'Run a strategy test to record the first learning.')}</div>
            <div class="p3-log-heading">Key Changes</div>
            <div class="p3-log-text">{entry.get('allocation', 'No run yet')}</div>
            <div class="p3-log-heading">Evidence</div>
            <div class="p3-log-text">{entry.get('evidence', 'Evidence appears after Run.')}</div>
            <div class="p3-log-heading" style="color:#A3E635;">Suggested Next Step</div>
            <div class="p3-log-text">{entry.get('next_step', 'Run Strategy Test')}</div>
        </div>
        """
    )


def render_journey_log_html(log_df: pd.DataFrame):
    """Compact shared Atlas journey log: newest actions first, P2/P3/P4 compatible."""
    if log_df is None or log_df.empty:
        display_df = pd.DataFrame(
            columns=["Step", "Page", "Country", "Reference", "Topic", "Observation", "Next"]
        )
    else:
        display_df = log_df.copy()
        if "step" in display_df.columns:
            display_df = display_df.sort_values("step", ascending=False)
        display_df = display_df.head(8)

        # Shared atlas_state schema.
        rename_map = {
            "step": "Step",
            "page": "Page",
            "country": "Country",
            "reference": "Reference",
            "topic": "Topic",
            "observation": "Observation",
            "next_step": "Next",
        }
        keep_cols = [col for col in rename_map if col in display_df.columns]
        display_df = display_df[keep_cols].rename(columns=rename_map)

        for col in ["Step", "Page", "Country", "Reference", "Topic", "Observation", "Next"]:
            if col not in display_df.columns:
                display_df[col] = ""
        display_df = display_df[["Step", "Page", "Country", "Reference", "Topic", "Observation", "Next"]]

    column_widths = {
        "Step": "5%",
        "Page": "13%",
        "Country": "9%",
        "Reference": "12%",
        "Topic": "18%",
        "Observation": "34%",
        "Next": "9%",
    }
    colgroup = "".join(
        f'<col style="width:{column_widths.get(col, "120px")};">'
        for col in display_df.columns
    )
    headers = "".join(f"<th>{col}</th>" for col in display_df.columns)

    rows = []
    for _, row in display_df.iterrows():
        cells = "".join(f"<td>{row[col]}</td>" for col in display_df.columns)
        rows.append(f"<tr>{cells}</tr>")

    st.html(
        f"""
        <div style="
            width:100%;
            margin-top:12px;
            border-radius:16px;
            border:1px solid rgba(56,189,248,0.34);
            background:rgba(15,23,42,0.72);
            padding:14px;
            overflow-x:auto;
        ">
            <div style="color:#F8FAFC; font-size:1rem; font-weight:900; margin-bottom:4px;">
                Journey Log
            </div>
            <div style="color:#CBD5E1; font-size:0.82rem; margin-bottom:12px;">
                Latest actions first. Full details remain stored for P5/export.
            </div>
            <table style="
                width:100%;
                border-collapse:collapse;
                table-layout:fixed;
                background:rgba(51,65,85,0.92);
                color:#F8FAFC;
                font-size:0.82rem;
            ">
                <colgroup>{colgroup}</colgroup>
                <thead><tr>{headers}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        <style>
            table th {{
                background:rgba(56,189,248,0.14);
                color:#E0F2FE;
                border:1px solid rgba(148,163,184,0.40);
                padding:9px 8px;
                text-align:left;
                font-size:0.74rem;
                font-weight:900;
                letter-spacing:0.04em;
                text-transform:uppercase;
            }}
            table td {{
                border:1px solid rgba(148,163,184,0.32);
                padding:9px 8px;
                vertical-align:top;
                line-height:1.34;
                background:rgba(51,65,85,0.78);
                word-wrap:break-word;
            }}
            table tbody tr:nth-child(even) td {{
                background:rgba(71,85,105,0.68);
            }}
        </style>
        """
    )


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.markdown("## P3 — Invest & Strategy")


# =============================================================================
# TOP CONTEXT
# =============================================================================

country_options = sorted(DATA["country_profiles"]["country_name"].dropna().unique().tolist())

init_atlas_state(
    default_country="Germany",
    default_reference="Family Average",
    default_reference_country="Sweden",
    default_view_mode="Relative",
)

atlas_country = st.session_state.get("atlas_country", "Germany")
atlas_reference_type = st.session_state.get("atlas_reference_type", "Family Average")
atlas_reference_country = st.session_state.get("atlas_reference_country", "Sweden")
atlas_view_mode = st.session_state.get("atlas_view_mode", "Relative")

if atlas_country not in country_options:
    atlas_country = "Germany" if "Germany" in country_options else country_options[0]
if atlas_reference_country not in country_options:
    atlas_reference_country = "Sweden" if "Sweden" in country_options else country_options[0]

reference_options = ["EU Average", "Family Average", "Another Country"]
if atlas_reference_type not in reference_options:
    atlas_reference_type = "Family Average"
view_options = ["Relative", "Absolute"]
if atlas_view_mode not in view_options:
    atlas_view_mode = "Relative"

top_col1, top_col2, top_col3, top_col_ref_country, top_col4 = st.columns(
    [1.8, 1.05, 1.15, 1.15, 0.9],
    gap="medium",
)

with top_col1:
    st.html(
        """
        <div class="p1-brand">
            <div class="p1-logo">🎯</div>
            <div>
                <div class="p1-brand-title">STRATEGIC<br>CHOICES</div>
                <div class="p1-brand-subtitle">Choose priorities.<br>Observe tradeoffs.</div>
            </div>
        </div>
        """
    )

with top_col2:
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        index=country_options.index(atlas_country),
        key="p3_global_country_v01",
    )

with top_col3:
    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        index=reference_options.index(atlas_reference_type),
        key="p3_global_reference_v01",
    )

with top_col_ref_country:
    if selected_reference == "Another Country":
        reference_country = st.selectbox(
            "Reference Country",
            options=country_options,
            index=country_options.index(atlas_reference_country),
            key="p3_global_reference_country_v01",
        )
    else:
        reference_country = None
        st.text_input("Reference Country", value="-----------", disabled=True)

with top_col4:
    view_mode = st.radio(
        "View Mode",
        options=view_options,
        horizontal=True,
        index=view_options.index(atlas_view_mode),
        key="p3_global_view_mode_v01",
    )

update_atlas_context(
    country=selected_country,
    reference_type=selected_reference,
    reference_country=reference_country if selected_reference == "Another Country" else atlas_reference_country,
    view_mode=view_mode,
    source_page="P3 Invest & Strategy",
    log_context_change=True,
)


# =============================================================================
# STATE INITIALIZATION
# =============================================================================

country_profile = get_country_profile(DATA["country_profiles"], selected_country)
selected_family = country_profile.get("structural_family", "Unknown")
selected_archetype = country_profile.get("archetype_label", "Other EU country")
baseline_allocation = get_country_baseline_allocation(DATA["country_year"], selected_country)
country_state_key = f"p3_country_{selected_country}"

if st.session_state.get("p3_country_state_key") != country_state_key:
    st.session_state["p3_country_state_key"] = country_state_key
    st.session_state["p3_selected_strategy"] = "Balanced Development"
    st.session_state["p3_current_allocation"] = baseline_allocation.copy()
    st.session_state["p3_last_run_allocation"] = baseline_allocation.copy()
    st.session_state["p3_last_run_strategy"] = "No run yet"
    st.session_state["p3_run_outputs"] = None
    st.session_state["p3_has_run"] = False
    for slider_name, value in baseline_allocation.items():
        st.session_state[f"p3_slider_{slider_name}"] = int(value)

st.session_state.setdefault("p3_mission_log", [])
st.session_state.setdefault("p3_selected_strategy", "Balanced Development")
st.session_state.setdefault("p3_current_allocation", baseline_allocation.copy())
st.session_state.setdefault("p3_last_run_allocation", baseline_allocation.copy())
st.session_state.setdefault("p3_last_run_strategy", "No run yet")
st.session_state.setdefault("p3_run_outputs", None)
st.session_state.setdefault("p3_has_run", False)

for slider_name, value in st.session_state["p3_current_allocation"].items():
    st.session_state.setdefault(f"p3_slider_{slider_name}", int(value))


def apply_strategy_preset(strategy_name: str):
    """Load a new strategy package into the editable draft.

    current version rule: selecting a different predefined strategy starts a new test,
    so old P3 results are cleared. The shared journey log is not deleted.
    """
    previous_strategy = st.session_state.get("p3_selected_strategy", "Balanced Development")
    strategy_changed = previous_strategy != strategy_name

    st.session_state["p3_selected_strategy"] = strategy_name
    for slider_name, value in STRATEGY_PRESETS[strategy_name].items():
        st.session_state[f"p3_slider_{slider_name}"] = int(value)

    if strategy_changed:
        st.session_state["p3_last_run_allocation"] = st.session_state["p3_current_allocation"].copy()
        st.session_state["p3_last_run_strategy"] = "No run yet"
        st.session_state["p3_run_outputs"] = None
        st.session_state["p3_has_run"] = False
        st.session_state["p3_mission_log"] = []


def reset_to_country_baseline():
    for slider_name, value in st.session_state["p3_current_allocation"].items():
        st.session_state[f"p3_slider_{slider_name}"] = int(value)


def reset_p3_workspace():
    """Reset the current P3 workspace, but keep the shared Atlas journey log."""
    st.session_state["p3_selected_strategy"] = "Balanced Development"
    st.session_state["p3_last_run_allocation"] = st.session_state["p3_current_allocation"].copy()
    st.session_state["p3_last_run_strategy"] = "No run yet"
    st.session_state["p3_run_outputs"] = None
    st.session_state["p3_has_run"] = False
    st.session_state["p3_mission_log"] = []
    for slider_name, value in st.session_state["p3_current_allocation"].items():
        st.session_state[f"p3_slider_{slider_name}"] = int(value)


def load_last_run_allocation():
    for slider_name, value in st.session_state["p3_last_run_allocation"].items():
        st.session_state[f"p3_slider_{slider_name}"] = int(value)


def clear_new_allocation():
    for slider_name in SLIDER_NAMES:
        st.session_state[f"p3_slider_{slider_name}"] = 0


def adjust_new_allocation(slider_name: str, delta: int):
    current_value = int(st.session_state.get(f"p3_slider_{slider_name}", 0))
    st.session_state[f"p3_slider_{slider_name}"] = int(
        np.clip(current_value + delta, 0, 100)
    )


current_allocation = st.session_state["p3_current_allocation"]
last_run_allocation = st.session_state["p3_last_run_allocation"]

baseline_dimensions = get_baseline_dimensions(country_profile)
baseline_z = get_baseline_dimension_z(country_profile)
current_outputs = calculate_outputs(baseline_dimensions)

# Calculate last-run output for displayed KPI cards.
last_run_dimensions, _ = calculate_dimension_after(
    baseline_dimensions=baseline_dimensions,
    baseline_allocation=current_allocation,
    proposed_allocation=last_run_allocation,
    family=selected_family,
    family_weights=DATA["family_weights"],
)
last_run_outputs = calculate_outputs(last_run_dimensions)

gain_name, gain_delta, cost_name, cost_delta, output_deltas = get_largest_gain_cost(
    current_outputs,
    last_run_outputs,
)

evidence_summary = get_evidence_summary(
    DATA["response_matrix"],
    last_run_allocation,
    current_allocation,
)
evidence_confidence_score, evidence_confidence_label, evidence_confidence_text = get_evidence_confidence(
    DATA["response_matrix"],
    last_run_allocation,
    current_allocation,
)


# =============================================================================
# RIBBON + INTRO
# =============================================================================

st.html(
    f"""
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">CURRENT PAGE</div>
            <div class="p1-kpi-main">P3 Invest & Strategy</div>
            <div class="p1-kpi-sub">Choose stage</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#38BDF8;">COUNTRY</div>
            <div class="p1-kpi-main">{selected_country}</div>
            <div class="p1-kpi-sub">{selected_family}</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#A3E635;">CURRENT MISSION</div>
            <div class="p1-kpi-main">{st.session_state['p3_selected_strategy']}</div>
            <div class="p1-kpi-sub">Strategy template</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#4ADE80;">LARGEST GAIN</div>
            <div class="p1-kpi-main">{gain_name}</div>
            <div class="p1-kpi-sub">{gain_delta:+.1f} after last run</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F472B6;">LARGEST COST</div>
            <div class="p1-kpi-main">{cost_name}</div>
            <div class="p1-kpi-sub">{cost_delta:+.1f} after last run</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">REFERENCE</div>
            <div class="p1-kpi-main">{selected_reference}</div>
            <div class="p1-kpi-sub">Comparison context</div>
        </div>
    </div>
    """
)

render_journey_progress(3)

st.html(
    """
    <div style="color:#38BDF8; font-size:0.96rem; font-weight:850; line-height:1.45; margin:6px 0 14px 0;">
        Choose a strategy package → adjust investment shares → run the strategy test → read the output changes.
    </div>
    """
)

render_page_intro()


# =============================================================================
# PAGE FRAME
# =============================================================================

left_col, main_col, right_col = st.columns([0.85, 5.4, 1.15], gap="medium")

sections = [
    ("01", "TENSIONS", "Understand the situation."),
    ("02", "STRATEGY", "Choose, build, run."),
    ("03", "RESULTS", "Observe consequences."),
    ("04", "LEARN", "What did we learn?"),
    ("05", "CHALLENGE", "What if something happens?"),
]

with left_col:
    render_left_rail_placeholder(page_number=3, page_title="Invest & Strategy", sections=sections)

with main_col:

    # =========================================================================
    # SECTION 01 — STRATEGIC TENSIONS
    # =========================================================================

    render_section_title(
        number="01",
        title=f"{selected_country}'s strategic tensions",
        subtitle="Each card shows the gap versus Europe first, with the 0–100 index as context. EU baseline = 50; this is structural position, not a quality ranking.",
    )

    tension_cols = st.columns(4, gap="medium")
    with tension_cols[0]:
        render_tension_card(
            "Sustainability",
            baseline_dimensions["Sustainability"],
            baseline_z["Sustainability"],
            "Indicates current sustainability capacity relative to Europe.",
            "#84CC16",
        )
    with tension_cols[1]:
        render_tension_card(
            "Fiscal Flexibility",
            baseline_dimensions["Fiscal Flexibility"],
            baseline_z["Fiscal Flexibility"],
            "Lower flexibility can create pressure when priorities expand.",
            "#F97316",
        )
    with tension_cols[2]:
        render_tension_card(
            "Security Capacity",
            baseline_dimensions["Security"],
            baseline_z["Security"],
            "Shows security reprioritization capacity in the current structure.",
            "#60A5FA",
        )
    with tension_cols[3]:
        render_tension_card(
            "Human Capital",
            baseline_dimensions["Human Capital"],
            baseline_z["Human Capital"],
            "Capability foundation for innovation, cohesion, and adaptation.",
            "#F59E0B",
        )

    with st.container(key="p3_strategy_workspace"):
        # =========================================================================
        # SECTION 02 — FOUR-COLUMN STRATEGY ROOM
        # =========================================================================

        render_section_title(
            number="02",
            title="Build and test one strategy package",
            subtitle=(
                "Choose a predefined package or build your own allocation. "
                "Edit the New package in 5% steps, run the test, then read the latest executed result. "
                "Inputs and outputs stay together."
            ),
        )

        # Free allocation input: do not constrain while editing.
        # The learning point is that the strategy package must total exactly 100% before it can run.
        new_allocation = {
            slider_name: int(st.session_state[f"p3_slider_{slider_name}"])
            for slider_name in SLIDER_NAMES
        }
        total_allocation = sum(new_allocation.values())
        mission_allocation = STRATEGY_PRESETS[st.session_state["p3_selected_strategy"]]

        st.html(
            """
            <div style="
                border:1px solid rgba(56,189,248,0.28);
                border-radius:16px;
                padding:12px 16px;
                background:rgba(15,23,42,0.72);
                margin-bottom:16px;
            ">
                <div style="color:#38BDF8; font-size:0.74rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:5px;">
                    How this workspace works
                </div>
                <div style="color:#E2E8F0; font-size:0.98rem; line-height:1.45; font-weight:700;">
                    <b>1 Choose</b> a package → <b>2 Edit</b> the New allocation → <b>3 Run</b> the strategy test → <b>4 Observe</b> the latest result.
                    The country column is the baseline; Last is the executed strategy; New is the draft waiting for Run.
                </div>
            </div>
            """
        )

        strategy_col, package_col, controls_col, result_col = st.columns(
            [1.0, 1.95, 0.78, 1.82],
            gap="medium",
        )

        # -------------------------------------------------------------------------
        # COLUMN 1 — PREDEFINED STRATEGY PACKAGES
        # -------------------------------------------------------------------------

        with strategy_col:
            st.markdown("### 1 · Choose")
            st.html(
                """
                <div class="p3-choice-help">
                    <div class="p3-choice-help-title">Predefined packages</div>
                    <div class="p3-choice-help-text">
                        Choose one starting package. It loads the <b>New</b> draft. You can still adjust every priority before Run.
                    </div>
                </div>
                """
            )

            for strategy_name in STRATEGY_PRESETS.keys():
                selected = st.session_state["p3_selected_strategy"] == strategy_name
                label = f"✓ {strategy_name}" if selected else strategy_name

                # The button is the selection object. No duplicate card under each button.
                if st.button(
                    label,
                    key=f"p3_strategy_button_{strategy_name}",
                    use_container_width=True,
                ):
                    apply_strategy_preset(strategy_name)
                    st.rerun()

            selected_strategy = st.session_state["p3_selected_strategy"]
            selected_color = STRATEGY_COLORS[selected_strategy]
            selected_package_text = allocation_to_text(STRATEGY_PRESETS[selected_strategy])

            st.html(
                f"""
                <div style="
                    margin-top:14px;
                    border:1px solid {selected_color};
                    border-left:5px solid {selected_color};
                    border-radius:14px;
                    padding:14px 15px;
                    background:rgba(15,23,42,0.82);
                    box-shadow:0 0 18px {selected_color}33;
                ">
                    <div style="color:{selected_color}; font-size:0.72rem; font-weight:900; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:7px;">
                        Selected package
                    </div>
                    <div style="color:#F8FAFC; font-size:1.02rem; font-weight:950; margin-bottom:7px;">
                        {selected_strategy}
                    </div>
                    <div style="color:#E2E8F0; font-size:0.84rem; line-height:1.36; margin-bottom:9px;">
                        {STRATEGY_DESCRIPTIONS[selected_strategy]}
                    </div>
                    <div style="color:#CBD5E1; font-size:0.76rem; line-height:1.35;">
                        {selected_package_text}
                    </div>
                </div>
                """
            )

        # -------------------------------------------------------------------------
        # COLUMN 2 — ALLOCATION TABLE
        # -------------------------------------------------------------------------

        with package_col:
            st.markdown("### 2 · Build")
            st.markdown(
                "<div class='p3-section-hint'>Adjust the <b>New</b> package in ±5% steps. <b>Country</b> is the current profile; <b>Last</b> is the last executed run.</div>",
                unsafe_allow_html=True,
            )

            st.html(
                """
                <div class="p3-allocation-card">
                    <div style="color:#F8FAFC; font-size:1rem; font-weight:900; margin-bottom:4px;">Strategy Allocation Table</div>
                    <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.34; margin-bottom:4px;">
                        <b>Country</b> = current investment profile · <b>Last</b> = last executed strategy · <b>New</b> = draft waiting for Run.
                    </div>
                </div>
                """
            )

            header_cols = st.columns([1.42, 0.60, 0.60, 1.60, 0.72])
            headers = ["Priority", "Country", "Last", "New", "Δ vs Country"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"<span class='p3-nowrap'><b>{header}</b></span>", unsafe_allow_html=True)

            for slider_name in SLIDER_NAMES:
                current_new_value = int(st.session_state[f"p3_slider_{slider_name}"])
                row_cols = st.columns([1.42, 0.60, 0.60, 1.60, 0.72])

                row_cols[0].markdown(
                    f"<span class='p3-nowrap' style='color:{SLIDER_COLORS[slider_name]}; font-weight:900;'>{SLIDER_SHORT_LABELS[slider_name]}</span>",
                    unsafe_allow_html=True,
                )
                row_cols[1].markdown(f"<span class='p3-nowrap'>{current_allocation[slider_name]}%</span>", unsafe_allow_html=True)
                row_cols[2].markdown(f"<span class='p3-nowrap'>{st.session_state['p3_last_run_allocation'][slider_name]}%</span>", unsafe_allow_html=True)

                minus_col, value_col, plus_col = row_cols[3].columns([0.48, 0.92, 0.48], gap="small")
                if minus_col.button("−", key=f"p3_minus_{slider_name}", use_container_width=True):
                    adjust_new_allocation(slider_name, -5)
                    st.rerun()
                value_col.markdown(
                    f"<div class='p3-stepper-value'>{current_new_value}%</div>",
                    unsafe_allow_html=True,
                )
                if plus_col.button("+", key=f"p3_plus_{slider_name}", use_container_width=True):
                    adjust_new_allocation(slider_name, 5)
                    st.rerun()

                row_delta = current_new_value - current_allocation[slider_name]
                delta_color = "#4ADE80" if row_delta > 0 else "#F472B6" if row_delta < 0 else "#CBD5E1"
                row_cols[4].markdown(
                    f"<div class='p3-row-delta' style='color:{delta_color};'>{row_delta:+d}%</div>",
                    unsafe_allow_html=True,
                )

            # Re-read after controls.
            new_allocation = {
                slider_name: int(st.session_state[f"p3_slider_{slider_name}"])
                for slider_name in SLIDER_NAMES
            }
            total_allocation = sum(new_allocation.values())

            if total_allocation == 100:
                st.success("✓ New allocation totals 100%. This package can be tested.")
            elif total_allocation < 100:
                st.warning(f"New allocation totals {total_allocation}%. Add {100 - total_allocation}% before running.")
            else:
                st.error(f"New allocation totals {total_allocation}%. Reduce {total_allocation - 100}% before running.")

        # -------------------------------------------------------------------------
        # COLUMN 3 — EXECUTION CONTROLS
        # -------------------------------------------------------------------------

        with controls_col:
            st.markdown("### 3 · Run")
            st.markdown(
                "<div class='p3-section-hint'>Use helper actions, then run only when New totals 100%.</div>",
                unsafe_allow_html=True,
            )

            if st.button("Load Current", key="p3_load_current", use_container_width=True):
                reset_to_country_baseline()
                st.rerun()

            if st.button("Load Package", key="p3_load_mission", use_container_width=True):
                apply_strategy_preset(st.session_state["p3_selected_strategy"])
                st.rerun()

            if st.button("Load Last", key="p3_load_last_run", use_container_width=True):
                load_last_run_allocation()
                st.rerun()

            st.html("<div style='height:10px;'></div>")

            if st.button("↺ Reset Workspace", key="p3_reset_workspace", use_container_width=True):
                reset_p3_workspace()
                st.rerun()

            st.html(
                """
                <div style="
                    height:1px;
                    background:rgba(148,163,184,0.20);
                    margin:14px 0;
                "></div>
                """
            )

            if total_allocation == 100:
                st.html(
                    """
                    <div class="p3-run-ready-note" style="background:rgba(20,83,45,0.36); color:#BBF7D0; border-color:rgba(74,222,128,0.36);">
                        ✓ Ready: New package totals 100%.
                    </div>
                    """
                )
            elif total_allocation < 100:
                st.html(
                    f"""
                    <div class="p3-run-ready-note" style="background:rgba(120,53,15,0.30); color:#FDE68A; border-color:rgba(245,158,11,0.42);">
                        Add {100 - total_allocation}% before running.
                    </div>
                    """
                )
            else:
                st.html(
                    f"""
                    <div class="p3-run-ready-note" style="background:rgba(127,29,29,0.30); color:#FECACA; border-color:rgba(239,68,68,0.42);">
                        Reduce {total_allocation - 100}% before running.
                    </div>
                    """
                )

            run_clicked = st.button(
                "▶ RUN STRATEGY TEST",
                key="p3_run_strategy",
                use_container_width=True,
                disabled=(total_allocation != 100),
            )

            if run_clicked:
                st.session_state["p3_last_run_allocation"] = new_allocation.copy()
                st.session_state["p3_last_run_strategy"] = st.session_state["p3_selected_strategy"]
                run_dimensions, _ = calculate_dimension_after(
                    baseline_dimensions=baseline_dimensions,
                    baseline_allocation=current_allocation,
                    proposed_allocation=new_allocation,
                    family=selected_family,
                    family_weights=DATA["family_weights"],
                )
                run_outputs = calculate_outputs(run_dimensions)
                run_gain_name, run_gain_delta, run_cost_name, run_cost_delta, _ = get_largest_gain_cost(current_outputs, run_outputs)
                run_evidence = get_evidence_summary(DATA["response_matrix"], new_allocation, current_allocation)
                run_confidence_score, run_confidence_label, _ = get_evidence_confidence(DATA["response_matrix"], new_allocation, current_allocation)

                mission_entry = {
                    "step": 3,
                    "page": "P3 Invest & Strategy",
                    "country": selected_country,
                    "strategy": st.session_state["p3_selected_strategy"],
                    "allocation": allocation_to_text(new_allocation),
                    "largest_gain": f"{run_gain_name} ({run_gain_delta:+.1f})",
                    "largest_cost": f"{run_cost_name} ({run_cost_delta:+.1f})",
                    "evidence": f"{run_confidence_score}/100 ({run_confidence_label})",
                    "family_context": selected_family,
                    "learning": f"Largest gain: {run_gain_name}. Main tradeoff/pressure: {run_cost_name}.",
                    "next_step": "Challenge Strategy",
                }
                st.session_state["p3_mission_log"].append(mission_entry)

                add_journey_event(
                    page="P3 Invest & Strategy",
                    action_type="strategy test",
                    country=selected_country,
                    reference=(
                        f"Another Country: {reference_country}"
                        if selected_reference == "Another Country" and reference_country
                        else selected_reference
                    ),
                    topic=st.session_state["p3_selected_strategy"],
                    observation=(
                        f"Input allocation: {allocation_to_text(new_allocation)}. "
                        f"Output result: largest gain = {run_gain_name} ({run_gain_delta:+.1f}); "
                        f"main cost/pressure = {run_cost_name} ({run_cost_delta:+.1f}); "
                        f"evidence = {run_confidence_score}/100 ({run_confidence_label})."
                    ),
                    evidence=f"{run_confidence_score}/100 ({run_confidence_label})",
                    confidence=run_confidence_label,
                    family_context=selected_family,
                    next_step="Open Challenge Mode",
                    dedupe_key=(
                        f"p3_strategy::{selected_country}::"
                        f"{st.session_state['p3_selected_strategy']}::"
                        f"{allocation_to_text(new_allocation)}"
                    ),
                )

                st.session_state["p3_has_run"] = True
                st.rerun()

        # -------------------------------------------------------------------------
        # COLUMN 4 — STRATEGY TEST RESULTS TABLE
        # -------------------------------------------------------------------------

        with result_col:
            st.markdown("### 4 · What Happened?")
            if st.session_state["p3_has_run"]:
                st.markdown(
                    "<div class='p3-section-hint'>The table shows the last executed strategy test against the baseline.</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='p3-section-hint'>No strategy has been run yet. The table shows baseline vs baseline until the first test.</div>",
                    unsafe_allow_html=True,
                )

            render_strategy_test_results_table(
                last_outputs=current_outputs,
                test_outputs=last_run_outputs,
                gain_name=gain_name,
                gain_delta=gain_delta,
                cost_name=cost_name,
                cost_delta=cost_delta,
                confidence_score=evidence_confidence_score,
                confidence_label=evidence_confidence_label,
            )

    # =========================================================================
    # SECTION 04 — CONSEQUENCE SUMMARY
    # =========================================================================

    render_section_title(
        number="03",
        title="Observe the consequences",
        subtitle="Compare the country baseline, the last executed strategy, and the new allocation waiting to run.",
    )

    summary_cols = st.columns(3, gap="medium")
    with summary_cols[0]:
        render_p3_result_card(
            title="Current Country Baseline",
            value=selected_country,
            detail=allocation_to_text(current_allocation),
            status="Country spending mix normalized to the five strategy levers.",
            accent="#38BDF8",
        )
    with summary_cols[1]:
        last_strategy_label = st.session_state.get("p3_last_run_strategy", "No run yet") if st.session_state["p3_has_run"] else "No run yet"
        last_strategy_accent = "#F59E0B" if st.session_state["p3_has_run"] else "#94A3B8"
        render_p3_result_card(
            title="Last Executed Strategy",
            value=last_strategy_label,
            detail=allocation_to_text(st.session_state["p3_last_run_allocation"]),
            status="Executed strategy currently shown in the results table above." if st.session_state["p3_has_run"] else "No test has been run for the current selected strategy.",
            accent=last_strategy_accent,
        )
    with summary_cols[2]:
        waiting_accent = "#A3E635" if total_allocation == 100 else "#F472B6"
        render_p3_result_card(
            title="New Allocation Waiting",
            value=f"{total_allocation}%",
            detail=allocation_to_text(new_allocation),
            status="Ready for Run Strategy Test." if total_allocation == 100 else "Adjust until the package totals 100%.",
            accent=waiting_accent,
        )

    # SECTION 05 — LEARN
    # =========================================================================

    render_section_title(
        number="04",
        title="What did we learn?",
        subtitle="Translate the last run into an educational strategy insight.",
    )

    learn_cols = st.columns(3, gap="medium")
    with learn_cols[0]:
        gain_accent = get_delta_color_by_value(gain_delta, gain_name)
        render_p3_result_card(
            title="Largest Gain",
            value=gain_name,
            detail=f"{gain_delta:+.1f} after last run",
            status="Primary positive movement.",
            accent=gain_accent,
        )
    with learn_cols[1]:
        cost_accent = get_delta_color_by_value(cost_delta, cost_name)
        render_p3_result_card(
            title="Largest Cost / Pressure",
            value=cost_name,
            detail=f"{cost_delta:+.1f} after last run",
            status="Main tradeoff or pressure point.",
            accent=cost_accent,
        )
    with learn_cols[2]:
        evidence_accent = "#4ADE80" if evidence_confidence_score >= 75 else "#EAB308" if evidence_confidence_score >= 55 else "#F59E0B" if evidence_confidence_score >= 35 else "#F472B6"
        render_p3_result_card(
            title="Evidence Confidence",
            value=f"{evidence_confidence_score} / 100",
            detail=evidence_confidence_label,
            status=evidence_confidence_text,
            accent=evidence_accent,
        )

    render_ai_insight_panel(
        title="Strategy Interpretation",
        observation=f"The last executed strategy shows the strongest positive movement in {gain_name}.",
        interpretation=f"The main tradeoff or pressure appears in {cost_name}. This reflects the selected allocation and the {selected_family} family response profile.",
        limitation=f"Evidence confidence: {evidence_confidence_score}/100 ({evidence_confidence_label}). This is a transparent educational sandbox and does not forecast outcomes.",
        next_question="Would this strategy remain robust under an energy crisis, pandemic shock, or fiscal stress scenario?",
    )

with right_col:
    latest_entry = st.session_state["p3_mission_log"][-1] if st.session_state["p3_mission_log"] else {
        "strategy": st.session_state["p3_selected_strategy"],
        "learning": "Run a strategy test to record the first learning.",
        "allocation": allocation_to_text(st.session_state["p3_last_run_allocation"]),
        "evidence": f"{evidence_confidence_score}/100 ({evidence_confidence_label})",
        "next_step": "Run Strategy Test",
    }
    render_p3_mission_log_panel(latest_entry)


# =============================================================================
# FULL-WIDTH CONTINUE + JOURNEY LOG
# =============================================================================

st.html("<div class='p3-full-width-shell'>")
# =========================================================================
# SECTION 06 — CTA
# =========================================================================

render_section_title(
    number="06",
    title="Ready for a challenge?",
    subtitle="Move from strategy building toward stress-testing.",
)

cta_challenge, cta_tradeoff, cta_country, cta_assume = st.columns(4, gap="medium")

with cta_challenge:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-challenge" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Next Page</div>
                <div style="color:#F59E0B; font-size:1.12rem; font-weight:900; margin:8px 0;">Challenge Strategy</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Test whether this strategy survives disruption.</div>
            </div>
            """
        )
        if st.button("Open Challenge Mode", key="p3_cta_challenge", use_container_width=True):
            safe_switch_page("pages/p4_challenge.py")

with cta_tradeoff:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-navigation" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Back</div>
                <div style="color:#38BDF8; font-size:1.12rem; font-weight:900; margin:8px 0;">Tradeoff Explorer</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Return to the structural relationships behind strategy choices.</div>
            </div>
            """
        )
        if st.button("Open Tradeoff Explorer", key="p3_cta_tradeoff", use_container_width=True):
            safe_switch_page("pages/p2_tradeoff_explorer.py")

with cta_country:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-compare" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Start New Country</div>
                <div style="color:#22D3EE; font-size:1.12rem; font-weight:900; margin:8px 0;">Country Explorer</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Begin from another structural profile.</div>
            </div>
            """
        )
        if st.button("Open Country Explorer", key="p3_cta_country", use_container_width=True):
            safe_switch_page("pages/p1_country_explorer.py")

with cta_assume:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-reflect" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Learn</div>
                <div style="color:#A855F7; font-size:1.12rem; font-weight:900; margin:8px 0;">Assumptions</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Review evidence limits and model assumptions.</div>
            </div>
            """
        )
        if st.button("Review Assumptions", key="p3_cta_assumptions", use_container_width=True):
            st.info("Assumptions page/link will be wired during global framework cleanup.")

# =========================================================================
# JOURNEY LOG
# =========================================================================

st.markdown("---")
st.html(
    """
    <div style="border:1px solid rgba(56,189,248,0.30); border-radius:14px; background:rgba(30,58,95,0.55); padding:12px 16px; margin-bottom:10px;">
        <div style="color:#38BDF8; font-size:0.76rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:4px;">Journey Log</div>
        <div style="color:#E2E8F0; font-size:0.92rem; line-height:1.4;">Shared record from P1 onward. Latest actions first; full details remain stored for P5/export.</div>
    </div>
    """
)

mission_log_df = get_journey_log_df()

with st.expander("View Full Journey Log", expanded=False):
    render_journey_log_html(mission_log_df)

render_footer()

st.html("</div>")
