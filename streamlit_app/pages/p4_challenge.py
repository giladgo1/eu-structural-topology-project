"""
p4_challenge_v08_apply_shock_commit_fix.py

European Strategy Atlas — Page 4
Challenge Mode / Shock + Recovery Test Room

VERSION: v08_APPLY_SHOCK_COMMIT_FIX

Architecture:
01 Explain challenge mode
02 Challenge Test: choose challenge -> run shock -> observe damage
03 Recovery Test: modify response -> run adaptation -> observe recovery
03 Learning summary + interpretation
04 Continue CTA
05 Journey Log

Design rule:
P4 reuses P3 grammar, but splits the learning into two rows:
- Row 1A: What did the shock do?
- Row 1B: Can I improve / recover with a response package?
"""

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

from components.typography import render_section_title
from components.cards import render_atlas_card, render_ai_insight_panel
from components.page_frame import render_left_rail_placeholder, render_footer


# =============================================================================
# GLOBAL CSS
# =============================================================================

def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# =============================================================================
# PAGE-SPECIFIC CSS
# =============================================================================

st.html(
    """
    <style>
    .p4-version {
        color:#64748B;
        font-size:0.72rem;
        text-align:right;
        margin-top:-10px;
        margin-bottom:4px;
    }
    .p4-intro-box {
        border:1px solid rgba(245,158,11,0.46);
        border-radius:16px;
        padding:18px 22px;
        background:linear-gradient(135deg, rgba(120,53,15,0.18), rgba(15,23,42,0.78));
        margin: 18px 0 24px 0;
        box-shadow:0 0 24px rgba(245,158,11,0.08);
    }
    .p4-intro-title {
        color:#F59E0B;
        font-size:0.78rem;
        font-weight:950;
        letter-spacing:0.14em;
        text-transform:uppercase;
        margin-bottom:9px;
    }
    .p4-intro-text {
        color:#F8FAFC;
        font-size:1.05rem;
        line-height:1.52;
        font-weight:800;
    }
    .p4-workspace-help {
        border:1px solid rgba(245,158,11,0.38);
        border-radius:14px;
        padding:12px 16px;
        background:rgba(15,23,42,0.74);
        margin:0 0 16px 0;
    }
    .p4-help-title {
        color:#F59E0B;
        font-size:0.72rem;
        font-weight:950;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:6px;
    }
    .p4-help-text {
        color:#E2E8F0;
        font-size:0.92rem;
        line-height:1.42;
        font-weight:800;
    }
    .p4-panel {
        border:1px solid rgba(245,158,11,0.36);
        border-radius:16px;
        padding:15px 16px;
        background:rgba(15,23,42,0.74);
        min-height:100px;
    }
    .p4-panel-muted {
        border:1px solid rgba(100,116,139,0.28);
        border-radius:14px;
        padding:12px 13px;
        background:rgba(15,23,42,0.42);
        color:#64748B;
        margin-top:12px;
    }
    .p4-small-label {
        color:#F59E0B;
        font-size:0.69rem;
        font-weight:950;
        letter-spacing:0.11em;
        text-transform:uppercase;
        margin-bottom:7px;
    }
    .p4-panel-title {
        color:#F8FAFC;
        font-size:1.02rem;
        font-weight:950;
        line-height:1.18;
        margin-bottom:7px;
    }
    .p4-panel-text {
        color:#E2E8F0;
        font-size:0.84rem;
        line-height:1.36;
        font-weight:750;
    }
    .p4-panel-meta {
        color:#CBD5E1;
        font-size:0.76rem;
        line-height:1.34;
        margin-top:9px;
    }
    .p4-section-hint {
        color:#CBD5E1;
        font-size:0.88rem;
        line-height:1.4;
        margin-bottom:12px;
    }
    .p4-run-ready-note {
        border-radius:12px;
        padding:10px 12px;
        margin:12px 0;
        font-size:0.84rem;
        font-weight:850;
        line-height:1.32;
        border:1px solid rgba(245,158,11,0.42);
        background:rgba(120,53,15,0.30);
        color:#FDE68A;
    }
    .p4-table-card {
        border:1px solid rgba(245,158,11,0.42);
        border-radius:16px;
        padding:15px 16px;
        background:rgba(15,23,42,0.78);
        box-shadow:0 0 22px rgba(245,158,11,0.08);
        margin: 0 0 12px 0;
    }
    .p4-table-title {
        color:#F8FAFC;
        font-size:1.06rem;
        font-weight:950;
        margin-bottom:5px;
    }
    .p4-table-subtitle {
        color:#CBD5E1;
        font-size:0.80rem;
        line-height:1.34;
        margin-bottom:12px;
    }
    .p4-table {
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        color:#E5E7EB;
        font-size:0.83rem;
    }
    .p4-table th {
        color:#FBBF24;
        background:rgba(120,53,15,0.28);
        font-size:0.66rem;
        font-weight:950;
        letter-spacing:0.07em;
        text-transform:uppercase;
        text-align:left;
        padding:8px 7px;
        border:1px solid rgba(148,163,184,0.26);
        white-space:nowrap;
    }
    .p4-table td {
        padding:10px 7px;
        border:1px solid rgba(148,163,184,0.22);
        vertical-align:middle;
        line-height:1.25;
        background:rgba(51,65,85,0.62);
    }
    .p4-table tbody tr:nth-child(even) td {
        background:rgba(51,65,85,0.78);
    }
    .p4-name {
        color:#F8FAFC;
        font-size:0.84rem;
        font-weight:950;
        line-height:1.18;
    }
    .p4-score {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.88rem;
        font-weight:950;
        color:#F8FAFC;
        white-space:nowrap;
    }
    .p4-delta {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.92rem;
        font-weight:950;
        white-space:nowrap;
    }
    .p4-reading {
        font-size:0.80rem;
        font-weight:900;
        line-height:1.18;
    }
    .p4-mini-summary-grid {
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:10px;
        margin:0 0 13px 0;
    }
    .p4-mini-summary-card {
        border:1px solid rgba(148,163,184,0.24);
        border-radius:12px;
        padding:11px 11px;
        background:rgba(2,6,23,0.38);
        min-height:88px;
    }
    .p4-mini-summary-label {
        color:#94A3B8;
        font-size:0.64rem;
        font-weight:950;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-bottom:7px;
    }
    .p4-mini-summary-value {
        color:#F8FAFC;
        font-size:0.94rem;
        font-weight:950;
        line-height:1.18;
    }
    .p4-mini-summary-delta {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.90rem;
        font-weight:950;
        margin-top:6px;
    }
    .p4-stepper-value {
        text-align:center;
        color:#F8FAFC;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.94rem;
        font-weight:950;
        padding-top:0.45rem;
        white-space:nowrap;
        min-width:40px;
    }
    .p4-row-delta {
        font-weight:950;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.88rem;
        text-align:right;
        padding-top:0.54rem;
        white-space:nowrap;
    }
    .p4-log-panel {
        position:sticky;
        top:160px;
        border:1px solid rgba(245,158,11,0.42);
        border-radius:16px;
        padding:17px;
        background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(15,23,42,0.76));
        box-shadow:0 0 20px rgba(245,158,11,0.08);
    }
    .p4-log-title {
        color:#FBBF24;
        font-size:0.76rem;
        font-weight:950;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:14px;
    }
    .p4-log-heading {
        color:#F8FAFC;
        font-size:0.90rem;
        font-weight:950;
        margin-top:12px;
        margin-bottom:6px;
    }
    .p4-log-text {
        color:#CBD5E1;
        font-size:0.84rem;
        line-height:1.38;
    }
    .p4-summary-band {
        display:grid;
        grid-template-columns: repeat(3, 1fr);
        gap:12px;
        margin: 8px 0 18px 0;
    }
    .p4-results-table-wide {
        font-size:0.78rem;
    }
    .p4-results-table-wide th {
        font-size:0.60rem;
        padding:7px 5px;
    }
    .p4-results-table-wide td {
        padding:8px 5px;
    }
    </style>
    """
)


# =============================================================================
# PATHS + DATA LOADING
# =============================================================================

APP_DATA_DIR = Path(__file__).parent.parent / "data"
ALT_APP_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "app"
FALLBACK_DATA_DIR = Path("/mnt/data")


def read_app_csv(filename: str, required: bool = True) -> pd.DataFrame:
    paths = [APP_DATA_DIR / filename, ALT_APP_DATA_DIR / filename, FALLBACK_DATA_DIR / filename]
    for path in paths:
        if path.exists():
            return pd.read_csv(path)
    if required:
        raise FileNotFoundError(
            f"Could not find {filename}. Checked: " + " | ".join(str(path) for path in paths)
        )
    return pd.DataFrame()


@st.cache_data
def load_p4_data():
    shock_registry = read_app_csv("shock_registry_v1.csv")
    shock_interpretation = read_app_csv("shock_interpretation_registry_v1.csv", required=False)
    dimension_profiles = read_app_csv("country_dimension_profiles.csv", required=False)
    family_metadata = read_app_csv("structural_family_metadata.csv", required=False)

    if not dimension_profiles.empty and not family_metadata.empty and "country_name" in dimension_profiles.columns:
        keep_cols = [
            c for c in [
                "country_name",
                "structural_family",
                "structural_subfamily",
                "family_anchor_archetype",
                "family_color",
            ]
            if c in family_metadata.columns
        ]
        if "country_name" in keep_cols:
            country_profiles = dimension_profiles.merge(family_metadata[keep_cols], on="country_name", how="left")
        else:
            country_profiles = dimension_profiles.copy()
    else:
        country_profiles = pd.DataFrame()

    return {
        "shock_registry": shock_registry,
        "shock_interpretation": shock_interpretation,
        "country_profiles": country_profiles,
    }


DATA = load_p4_data()


# =============================================================================
# REGISTRIES
# =============================================================================

DIMENSION_COLUMNS = {
    "Human Capital": "dim_human_capital_capacity",
    "Innovation": "dim_innovation_capacity",
    "Sustainability": "dim_sustainability_capacity",
    "Social Stability": "dim_social_stability",
    "Fiscal Flexibility": "dim_fiscal_flexibility",
    "Security": "dim_security_reprioritization",
    "Adaptive Transformation": "dim_adaptive_transformation",
}

DISPLAY_DIMENSIONS = [
    "Sustainability",
    "Innovation",
    "Fiscal Flexibility",
    "Social Stability",
    "Security",
    "Adaptive Transformation",
]

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
        "dimensions": ["Adaptive Transformation", "Social Stability", "Sustainability", "Security"],
        "mode": "higher_is_better",
    },
}

ACTIVE_CHALLENGES = {
    "Energy Crisis": {
        "registry_key": "Energy",
        "description": "A spike in energy costs pressures households, industry, fiscal support, and transition capacity.",
        "affected": "Security · Fiscal Flexibility · Sustainability · Social Stability · Innovation",
        "accent": "#F59E0B",
    },
    "Pandemic Pressure": {
        "registry_key": "Recession",
        "description": "A broad disruption weakens growth, raises fiscal pressure, and tests social and adaptive capacity.",
        "affected": "Social Stability · Fiscal Flexibility · Innovation · Adaptive Transformation",
        "accent": "#A855F7",
    },
}

COMING_SOON_CHALLENGES = {
    "Fiscal Stress": "Debt pressure and reduced fiscal room.",
    "Security Shock": "Defense needs and geopolitical exposure.",
    "Technology Disruption": "Digital acceleration and capability displacement.",
}

STRENGTH_FACTORS = {"Low": 0.50, "Medium": 0.75, "High": 1.00}

RESPONSE_AREAS = ["Environment", "Economic Affairs", "Social Protection", "Defense", "Fiscal Reserve"]
DEFAULT_RESPONSE = {
    "Environment": 25,
    "Economic Affairs": 25,
    "Social Protection": 20,
    "Defense": 10,
    "Fiscal Reserve": 20,
}
RESPONSE_COLORS = {
    "Environment": "#84CC16",
    "Economic Affairs": "#94A3B8",
    "Social Protection": "#F59E0B",
    "Defense": "#8B5CF6",
    "Fiscal Reserve": "#22D3EE",
}

# How P4 response levers partially overcome the shock.
RESPONSE_EFFECTS = {
    ("Environment", "Sustainability"): 0.45,
    ("Environment", "Adaptive Transformation"): 0.20,
    ("Economic Affairs", "Innovation"): 0.35,
    ("Economic Affairs", "Adaptive Transformation"): 0.25,
    ("Economic Affairs", "Human Capital"): 0.10,
    ("Social Protection", "Social Stability"): 0.45,
    ("Social Protection", "Human Capital"): 0.12,
    ("Defense", "Security"): 0.50,
    ("Defense", "Adaptive Transformation"): 0.15,
    ("Fiscal Reserve", "Fiscal Flexibility"): 0.55,
    ("Fiscal Reserve", "Social Stability"): 0.10,
}


# =============================================================================
# MODEL HELPERS
# =============================================================================

def safe_switch_page(page_path: str):
    try:
        st.switch_page(page_path)
    except Exception:
        st.info(f"Navigation target not found yet: {page_path}")


def z_to_index(z_value: float) -> float:
    if pd.isna(z_value):
        return 50.0
    return float(np.clip(50 + 15 * float(z_value), 0, 100))


def get_country_profile(country_profiles: pd.DataFrame, country: str) -> pd.Series:
    if country_profiles.empty or "country_name" not in country_profiles.columns:
        return pd.Series(dtype="object")
    rows = country_profiles[country_profiles["country_name"] == country]
    if rows.empty:
        return country_profiles.iloc[0]
    return rows.iloc[0]


def get_country_options(country_profiles: pd.DataFrame) -> list[str]:
    if not country_profiles.empty and "country_name" in country_profiles.columns:
        return sorted(country_profiles["country_name"].dropna().unique().tolist())
    return ["Germany", "Sweden", "Romania", "Italy", "Poland", "Spain", "Netherlands"]


def get_baseline_dimensions(country_profile: pd.Series) -> dict[str, float]:
    # Fallback approximates the P3 test state if no profile file is available.
    fallback = {
        "Human Capital": 56,
        "Innovation": 59,
        "Sustainability": 42,
        "Social Stability": 59,
        "Fiscal Flexibility": 50,
        "Security": 50,
        "Adaptive Transformation": 68,
    }
    if country_profile.empty:
        return fallback
    dims = {}
    for dim_name, col_name in DIMENSION_COLUMNS.items():
        if col_name in country_profile.index:
            dims[dim_name] = z_to_index(country_profile.get(col_name, 0))
        else:
            dims[dim_name] = fallback.get(dim_name, 50)
    return dims


def calculate_outputs(dimensions: dict[str, float]) -> dict[str, float]:
    outputs = {}
    for output_name, config in OUTPUT_REGISTRY.items():
        raw_score = float(np.mean([dimensions.get(dim, 50) for dim in config["dimensions"]]))
        outputs[output_name] = 100 - raw_score if config["mode"] == "lower_is_better" else raw_score
    return outputs


def get_shock_impacts(challenge_name: str, strength: str, shock_registry: pd.DataFrame) -> dict[str, float]:
    registry_key = ACTIVE_CHALLENGES[challenge_name]["registry_key"]
    factor = STRENGTH_FACTORS[strength]
    rows = shock_registry[shock_registry["shock_type"].astype(str) == registry_key].copy()
    impacts = {dim: 0.0 for dim in DIMENSION_COLUMNS.keys()}
    for _, row in rows.iterrows():
        dim = str(row.get("dimension", ""))
        if dim in impacts:
            impacts[dim] += float(row.get("base_impact", 0)) * factor
    return impacts


def apply_shock(current_dimensions: dict[str, float], impacts: dict[str, float]) -> dict[str, float]:
    return {
        dim: float(np.clip(current_dimensions.get(dim, 50) + impacts.get(dim, 0), 0, 100))
        for dim in current_dimensions.keys()
    }


def apply_response(shock_dimensions: dict[str, float], response: dict[str, int]) -> tuple[dict[str, float], dict[str, float]]:
    deltas = {dim: 0.0 for dim in shock_dimensions.keys()}
    for area in RESPONSE_AREAS:
        change = response[area] - DEFAULT_RESPONSE[area]
        for dim in shock_dimensions.keys():
            effect = RESPONSE_EFFECTS.get((area, dim), 0)
            if effect:
                deltas[dim] += change * effect
    response_dimensions = {
        dim: float(np.clip(shock_dimensions.get(dim, 50) + deltas.get(dim, 0), 0, 100))
        for dim in shock_dimensions.keys()
    }
    return response_dimensions, deltas


def get_delta_color(delta: float, output_name: str = "") -> str:
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


def get_reading(delta: float, output_name: str = "") -> str:
    if output_name == "Fiscal Pressure":
        if delta > 4:
            return "Pressure increased"
        if delta < -4:
            return "Pressure reduced"
        return "Mostly stable"
    if delta > 4:
        return "Recovery / improved"
    if delta < -4:
        return "Visible impact"
    return "Mostly stable"


def classify_resilience(score: float) -> str:
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Moderate"
    if score >= 40:
        return "Vulnerable"
    return "Fragile"


def get_largest_damage(current_outputs: dict[str, float], shock_outputs: dict[str, float]) -> tuple[str, float]:
    deltas = {name: shock_outputs[name] - current_outputs[name] for name in current_outputs.keys()}
    # For Fiscal Pressure, increase is damage; for other outputs, decrease is damage.
    damage_scores = {}
    for name, delta in deltas.items():
        damage_scores[name] = delta if name == "Fiscal Pressure" else -delta
    damage_name = max(damage_scores, key=damage_scores.get)
    return damage_name, deltas[damage_name]


def get_largest_recovery(shock_outputs: dict[str, float], response_outputs: dict[str, float]) -> tuple[str, float]:
    deltas = {name: response_outputs[name] - shock_outputs[name] for name in shock_outputs.keys()}
    recovery_scores = {}
    for name, delta in deltas.items():
        recovery_scores[name] = -delta if name == "Fiscal Pressure" else delta
    recovery_name = max(recovery_scores, key=recovery_scores.get)
    return recovery_name, deltas[recovery_name]


def response_to_text(response: dict[str, int]) -> str:
    return " | ".join(f"{k}: {v}%" for k, v in response.items())


def response_modified(response: dict[str, int]) -> bool:
    return any(response[k] != DEFAULT_RESPONSE[k] for k in RESPONSE_AREAS)


# =============================================================================
# UI HELPERS
# =============================================================================

def render_intro_box():
    st.html(
        """
        <div class="p4-intro-box">
            <div class="p4-intro-title">What is Challenge Mode?</div>
            <div class="p4-intro-text">
                Challenge Mode introduces an external disruption and tests how the selected strategy responds.
                First run the challenge to observe damage. Then adjust a response package to see whether the strategy can recover.
                This is an educational stress test — not a forecast, prediction, or policy recommendation.
            </div>
        </div>
        """
    )


def render_challenge_description(challenge_name: str, strength: str):
    cfg = ACTIVE_CHALLENGES[challenge_name]
    st.html(
        f"""
        <div class="p4-panel">
            <div class="p4-small-label">Selected Challenge</div>
            <div class="p4-panel-title">{challenge_name}</div>
            <div class="p4-panel-text">{cfg['description']}</div>
            <div class="p4-panel-meta">
                <b>Strength:</b> {strength}<br>
                <b>Affected:</b> {cfg['affected']}
            </div>
        </div>
        """
    )


def render_coming_soon_panel():
    items = "".join(
        f"""
        <div class="p4-coming-soon-item">
            <div class="p4-coming-soon-name">{name}</div>
            <div class="p4-coming-soon-desc">{desc}</div>
        </div>
        """
        for name, desc in COMING_SOON_CHALLENGES.items()
    )
    st.html(
        f"""
        <div class="p4-panel-muted">
            <div class="p4-coming-soon-title">Coming Soon</div>
            {items}
        </div>
        """
    )


def render_dimension_damage_table(current_dimensions: dict[str, float], shock_dimensions: dict[str, float]):
    rows = []
    for dim in DISPLAY_DIMENSIONS:
        current = current_dimensions.get(dim, 50)
        shock = shock_dimensions.get(dim, 50)
        delta = shock - current
        accent = get_delta_color(delta)
        arrow = "▲" if delta > 1 else "▼" if delta < -1 else "→"
        rows.append(
            f"""
            <tr>
                <td><span class="p4-name">{dim}</span></td>
                <td><span class="p4-score">{current:.0f}</span></td>
                <td><span class="p4-score">{shock:.0f}</span></td>
                <td><span class="p4-delta" style="color:{accent};">{arrow} {delta:+.1f}</span></td>
            </tr>
            """
        )
    st.html(
        f"""
        <div class="p4-table-card">
            <div class="p4-table-title">Shock Impact</div>
            <div class="p4-table-subtitle">
                <b>Current</b> = selected strategy state · <b>Shock</b> = challenge-adjusted state.
            </div>
            <table class="p4-table">
                <colgroup><col style="width:42%;"><col style="width:17%;"><col style="width:17%;"><col style="width:24%;"></colgroup>
                <thead><tr><th>Dimension</th><th>Current</th><th>Shock</th><th>Δ</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )

def render_shock_observation_box(damage_name: str, damage_delta: float, shock_resilience: float, selected_challenge: str, selected_strength: str):
    shock_label = classify_resilience(shock_resilience)
    damage_color = get_delta_color(damage_delta, damage_name)
    if selected_challenge == "No Shock":
        text = (
            "No shock has been applied. The table shows the selected strategy reference state. "
            "Choose a challenge and press <b>Apply Shock</b> to create the disrupted state."
        )
    else:
        text = (
            f"<b>{selected_challenge}</b> at <b>{selected_strength}</b> strength creates the largest movement in "
            f"<b>{damage_name}</b> <span style='color:{damage_color}; font-weight:950;'>({damage_delta:+.1f})</span>. "
            f"Shock resilience is <b>{shock_resilience:.0f}/100</b> ({shock_label}). "
            "This is the disrupted state used as the starting point for recovery."
        )
    st.html(
        f"""
        <div class="p4-panel" style="margin-top:10px; min-height:unset;">
            <div class="p4-small-label">Shock Observation</div>
            <div class="p4-panel-text">{text}</div>
        </div>
        """
    )


def render_response_table(current_response: dict[str, int]):
    st.html(
        """
        <div class="p4-panel" style="padding-bottom:10px;">
            <div class="p4-small-label">Response Builder</div>
            <div class="p4-panel-text">
                Adjust the response package in ±5% steps. Total must equal 100% before running.
            </div>
        """
    )

    header_cols = st.columns([1.25, 0.50, 1.70, 0.45], gap="small")
    headers = ["Priority", "Current", "Test", "Δ"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"<b>{header}</b>", unsafe_allow_html=True)

    for area in RESPONSE_AREAS:
        value = int(st.session_state[f"p4_response_{area}"])
        row_cols = st.columns([1.25, 0.50, 1.70, 0.45], gap="small")
        row_cols[0].markdown(
            f"<span style='color:{RESPONSE_COLORS[area]}; font-weight:950;'>{area}</span>",
            unsafe_allow_html=True,
        )
        row_cols[1].markdown(f"{current_response[area]}%")
        minus_col, value_col, plus_col = row_cols[2].columns([0.42, 0.86, 0.42], gap="small")
        if minus_col.button("−", key=f"p4_minus_{area}", use_container_width=True):
            adjust_response(area, -5)
            st.rerun()
        value_col.markdown(f"<div class='p4-stepper-value'>{value}%</div>", unsafe_allow_html=True)
        if plus_col.button("+", key=f"p4_plus_{area}", use_container_width=True):
            adjust_response(area, 5)
            st.rerun()
        row_delta = value - current_response[area]
        color = "#4ADE80" if row_delta > 0 else "#F472B6" if row_delta < 0 else "#CBD5E1"
        row_cols[3].markdown(f"<div class='p4-row-delta' style='color:{color};'>{row_delta:+d}%</div>", unsafe_allow_html=True)

    st.html("</div>")


def render_recovery_dimension_table(shock_dimensions: dict[str, float], response_dimensions: dict[str, float]):
    rows = []
    for dim in DISPLAY_DIMENSIONS:
        shock = shock_dimensions.get(dim, 50)
        response = response_dimensions.get(dim, 50)
        delta = response - shock
        accent = get_delta_color(delta)
        arrow = "▲" if delta > 1 else "▼" if delta < -1 else "→"
        rows.append(
            f"""
            <tr>
                <td><span class="p4-name">{dim}</span></td>
                <td><span class="p4-score">{shock:.0f}</span></td>
                <td><span class="p4-score">{response:.0f}</span></td>
                <td><span class="p4-delta" style="color:{accent};">{arrow} {delta:+.1f}</span></td>
            </tr>
            """
        )
    st.html(
        f"""
        <div class="p4-table-card">
            <div class="p4-table-title">Recovery Preview</div>
            <div class="p4-table-subtitle">
                <b>Shock</b> = disrupted state · <b>Response</b> = draft response package.
            </div>
            <table class="p4-table">
                <colgroup><col style="width:42%;"><col style="width:18%;"><col style="width:20%;"><col style="width:20%;"></colgroup>
                <thead><tr><th>Dimension</th><th>Shock</th><th>Response</th><th>Δ</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )


def render_recovery_output_table(current_outputs: dict[str, float], shock_outputs: dict[str, float], response_outputs: dict[str, float], recovery_name: str, recovery_delta: float, resilience_score: float, resilience_label: str, remaining_risk_name: str, remaining_risk_value: float):
    rows = []
    for output_name in OUTPUT_REGISTRY.keys():
        ref_value = current_outputs[output_name]
        shock_value = shock_outputs[output_name]
        response_value = response_outputs[output_name]
        delta = response_value - shock_value
        accent = get_delta_color(delta, output_name)
        arrow = "▲" if delta > 1 else "▼" if delta < -1 else "→"
        reading = get_reading(delta, output_name)
        rows.append(
            f"""
            <tr>
                <td><span class="p4-name">{output_name}</span></td>
                <td><span class="p4-score">{ref_value:.0f}</span></td>
                <td><span class="p4-score">{shock_value:.0f}</span></td>
                <td><span class="p4-score">{response_value:.0f}</span></td>
                <td><span class="p4-delta" style="color:{accent};">{arrow} {delta:+.1f}</span></td>
                <td><span class="p4-reading" style="color:{accent};">{reading}</span></td>
            </tr>
            """
        )

    recovery_color = get_delta_color(recovery_delta, recovery_name)
    resilience_color = "#4ADE80" if resilience_score >= 70 else "#FBBF24" if resilience_score >= 55 else "#F97316" if resilience_score >= 40 else "#F472B6"

    st.html(
        f"""
        <div class="p4-table-card">
            <div class="p4-table-title">Recovery Test Results</div>
            <div class="p4-table-subtitle">
                <b>Ref</b> = selected strategy before shock · <b>Shock</b> = disrupted state · <b>Response Test</b> = last executed recovery response.
            </div>
            <div class="p4-mini-summary-grid">
                <div class="p4-mini-summary-card">
                    <div class="p4-mini-summary-label">Largest Recovery</div>
                    <div class="p4-mini-summary-value">{recovery_name}</div>
                    <div class="p4-mini-summary-delta" style="color:{recovery_color};">{recovery_delta:+.1f}</div>
                </div>
                <div class="p4-mini-summary-card">
                    <div class="p4-mini-summary-label">Remaining Risk</div>
                    <div class="p4-mini-summary-value">{remaining_risk_name}</div>
                    <div class="p4-mini-summary-delta" style="color:#F472B6;">{remaining_risk_value:.0f}</div>
                </div>
                <div class="p4-mini-summary-card">
                    <div class="p4-mini-summary-label">Final Resilience</div>
                    <div class="p4-mini-summary-value" style="color:{resilience_color};">{resilience_score:.0f} / 100</div>
                    <div class="p4-mini-summary-delta" style="color:{resilience_color};">{resilience_label}</div>
                </div>
            </div>
            <table class="p4-table p4-results-table-wide">
                <colgroup>
                    <col style="width:26%;">
                    <col style="width:11%;">
                    <col style="width:11%;">
                    <col style="width:16%;">
                    <col style="width:14%;">
                    <col style="width:22%;">
                </colgroup>
                <thead><tr><th>Output</th><th>Ref</th><th>Shock</th><th>Response Test</th><th>Δ</th><th>Reading</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )


def render_shock_summary_cards(damage_name: str, damage_delta: float, shock_resilience: float):
    damage_color = get_delta_color(damage_delta, damage_name)
    shock_label = classify_resilience(shock_resilience)
    shock_color = "#4ADE80" if shock_resilience >= 70 else "#FBBF24" if shock_resilience >= 55 else "#F97316" if shock_resilience >= 40 else "#F472B6"
    cols = st.columns(3, gap="medium")
    with cols[0]:
        render_atlas_card(
            title="Largest Damage",
            value=damage_name,
            delta_text=f"{damage_delta:+.1f} after shock",
            status="Largest movement caused by the challenge.",
            delta_color=damage_color,
            card_class="atlas-gap-card atlas-gap-card-top",
        )
    with cols[1]:
        render_atlas_card(
            title="Main Vulnerability",
            value=damage_name,
            delta_text="Shock exposure",
            status="Primary place where the current strategy was stressed.",
            delta_color="#F472B6",
            card_class="atlas-gap-card atlas-gap-card-top",
        )
    with cols[2]:
        render_atlas_card(
            title="Shock Resilience",
            value=f"{shock_resilience:.0f} / 100",
            delta_text=shock_label,
            status="Resilience after applying the disruption, before response.",
            delta_color=shock_color,
            card_class="atlas-gap-card atlas-gap-card-top",
        )


def render_recovery_summary_cards(recovery_name: str, recovery_delta: float, remaining_risk_name: str, final_resilience: float):
    recovery_color = get_delta_color(recovery_delta, recovery_name)
    final_label = classify_resilience(final_resilience)
    final_color = "#4ADE80" if final_resilience >= 70 else "#FBBF24" if final_resilience >= 55 else "#F97316" if final_resilience >= 40 else "#F472B6"
    cols = st.columns(3, gap="medium")
    with cols[0]:
        render_atlas_card(
            title="Largest Recovery",
            value=recovery_name,
            delta_text=f"{recovery_delta:+.1f} after response",
            status="Largest improvement created by the response package.",
            delta_color=recovery_color,
            card_class="atlas-gap-card atlas-gap-card-top",
        )
    with cols[1]:
        render_atlas_card(
            title="Remaining Risk",
            value=remaining_risk_name,
            delta_text="After response",
            status="Main unresolved pressure point.",
            delta_color="#F472B6",
            card_class="atlas-gap-card atlas-gap-card-top",
        )
    with cols[2]:
        render_atlas_card(
            title="Final Resilience",
            value=f"{final_resilience:.0f} / 100",
            delta_text=final_label,
            status="Resilience after shock and response.",
            delta_color=final_color,
            card_class="atlas-gap-card atlas-gap-card-top",
        )


def render_p4_mission_log_panel(entry: dict):
    st.html(
        f"""
        <div class="p4-log-panel">
            <div class="p4-log-title">Mission Log</div>
            <div class="p4-log-heading">Challenge</div>
            <div class="p4-log-text">{entry.get('challenge', 'Energy Crisis')}</div>
            <div class="p4-log-heading">Strength</div>
            <div class="p4-log-text">{entry.get('strength', 'Medium')}</div>
            <div class="p4-log-heading">Largest Damage</div>
            <div class="p4-log-text">{entry.get('largest_damage', 'No challenge run yet')}</div>
            <div class="p4-log-heading">Largest Recovery</div>
            <div class="p4-log-text">{entry.get('largest_recovery', 'No recovery run yet')}</div>
            <div class="p4-log-heading">Final Resilience</div>
            <div class="p4-log-text">{entry.get('resilience', 'Run challenge and response')}</div>
            <div class="p4-log-heading" style="color:#A3E635;">Suggested Next Step</div>
            <div class="p4-log-text">{entry.get('next_step', 'Run Challenge Test')}</div>
        </div>
        """
    )


def render_journey_log_html(log_df: pd.DataFrame):
    display_df = log_df.copy()
    preferred_cols = ["step", "page", "country", "challenge", "strength", "response", "largest_damage", "largest_recovery", "resilience", "learning", "next_step"]
    display_cols = [col for col in preferred_cols if col in display_df.columns]
    display_df = display_df[display_cols]

    headers = "".join(f"<th>{col.replace('_', ' ')}</th>" for col in display_df.columns)
    rows = []
    for _, row in display_df.iterrows():
        cells = "".join(f"<td>{row[col]}</td>" for col in display_df.columns)
        rows.append(f"<tr>{cells}</tr>")

    st.html(
        f"""
        <div style="width:100%; margin-top:12px; border-radius:16px; border:1px solid rgba(245,158,11,0.34); background:rgba(15,23,42,0.72); padding:16px; overflow-x:auto;">
            <div style="color:#F8FAFC; font-size:1.05rem; font-weight:900; margin-bottom:6px;">Journey Log Table</div>
            <div style="color:#CBD5E1; font-size:0.86rem; margin-bottom:14px;">Full-width record of P4 challenge and recovery tests. This becomes input for P5 Reflection.</div>
            <table style="min-width:1300px; width:100%; border-collapse:collapse; table-layout:fixed; background:rgba(51,65,85,0.92); color:#F8FAFC; font-size:0.82rem;">
                <thead><tr>{headers}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        <style>
            table th {{ background:rgba(245,158,11,0.16); color:#FDE68A; border:1px solid rgba(148,163,184,0.40); padding:10px 9px; text-align:left; font-size:0.72rem; font-weight:900; letter-spacing:0.04em; text-transform:uppercase; }}
            table td {{ border:1px solid rgba(148,163,184,0.32); padding:11px 9px; vertical-align:top; line-height:1.36; background:rgba(51,65,85,0.78); word-wrap:break-word; }}
            table tbody tr:nth-child(even) td {{ background:rgba(71,85,105,0.68); }}
        </style>
        """
    )


# =============================================================================
# STATE HELPERS
# =============================================================================

def set_challenge(challenge_name: str):
    st.session_state["p4_selected_challenge"] = challenge_name


def set_strength(strength: str):
    st.session_state["p4_strength"] = strength


def reset_response():
    for area, value in DEFAULT_RESPONSE.items():
        st.session_state[f"p4_response_{area}"] = int(value)


def adjust_response(area: str, delta: int):
    current_value = int(st.session_state.get(f"p4_response_{area}", DEFAULT_RESPONSE[area]))
    st.session_state[f"p4_response_{area}"] = int(np.clip(current_value + delta, 0, 100))


# =============================================================================
# PAGE CONFIG + STATE
# =============================================================================

st.markdown("## P4 — Challenge Mode")
st.caption("P4 VERSION v08_APPLY_SHOCK_COMMIT_FIX · Shock and recovery outputs update only after their Run buttons.")
st.html("<div class='p4-version'>P4 VERSION v08_APPLY_SHOCK_COMMIT_FIX</div>")

st.session_state.setdefault("p4_selected_challenge", "Energy Crisis")
st.session_state.setdefault("p4_strength", "Medium")
st.session_state.setdefault("p4_has_challenge_run", False)
st.session_state.setdefault("p4_has_response_run", False)
st.session_state.setdefault("p4_applied_challenge", "No Shock")
st.session_state.setdefault("p4_applied_strength", "None")
st.session_state.setdefault("p4_committed_response", DEFAULT_RESPONSE.copy())
st.session_state.setdefault("p4_journey_log", [])
for area, value in DEFAULT_RESPONSE.items():
    st.session_state.setdefault(f"p4_response_{area}", int(value))

selected_challenge = st.session_state["p4_selected_challenge"]
selected_strength = st.session_state["p4_strength"]
applied_challenge = st.session_state.get("p4_applied_challenge", "No Shock")
applied_strength = st.session_state.get("p4_applied_strength", "None")
current_response = DEFAULT_RESPONSE.copy()
draft_response = {area: int(st.session_state[f"p4_response_{area}"]) for area in RESPONSE_AREAS}
committed_response = st.session_state.get("p4_committed_response", DEFAULT_RESPONSE.copy())
total_response = sum(draft_response.values())

# =============================================================================
# TOP CONTEXT
# =============================================================================

country_options = get_country_options(DATA["country_profiles"])

top_col1, top_col2, top_col3, top_col_ref_country, top_col4 = st.columns([1.8, 1.05, 1.15, 1.15, 0.9], gap="medium")

with top_col1:
    st.html(
        """
        <div class="p1-brand">
            <div class="p1-logo">⚡</div>
            <div>
                <div class="p1-brand-title">CHALLENGE<br>MODE</div>
                <div class="p1-brand-subtitle">Stress-test strategy.<br>Explore resilience.</div>
            </div>
        </div>
        """
    )

with top_col2:
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        index=country_options.index("Germany") if "Germany" in country_options else 0,
    )

with top_col3:
    selected_reference = st.selectbox("Reference", options=["EU Average", "Family Average", "Another Country"], index=1)

with top_col_ref_country:
    if selected_reference == "Another Country":
        reference_country = st.selectbox(
            "Reference Country",
            options=country_options,
            index=country_options.index("Sweden") if "Sweden" in country_options else 0,
        )
    else:
        reference_country = None
        st.text_input("Reference Country", value="-----------", disabled=True)

with top_col4:
    view_mode = st.radio("View Mode", options=["Relative", "Absolute"], horizontal=True, index=0)

country_profile = get_country_profile(DATA["country_profiles"], selected_country)
selected_family = country_profile.get("structural_family", "Industrial / Transition Systems") if not country_profile.empty else "Industrial / Transition Systems"
selected_archetype = country_profile.get("family_anchor_archetype", "Selected Strategy") if not country_profile.empty else "Selected Strategy"

current_dimensions = get_baseline_dimensions(country_profile)
current_outputs = calculate_outputs(current_dimensions)

# Draft shock = what the user selected. Applied shock = what was committed with APPLY SHOCK.
# Tables use the applied state only, so selecting a challenge/strength does not change results until Run.
if st.session_state["p4_has_challenge_run"] and applied_challenge in ACTIVE_CHALLENGES:
    active_shock_impacts = get_shock_impacts(applied_challenge, applied_strength, DATA["shock_registry"])
    active_shock_dimensions = apply_shock(current_dimensions, active_shock_impacts)
else:
    active_shock_impacts = {dim: 0.0 for dim in DIMENSION_COLUMNS.keys()}
    active_shock_dimensions = current_dimensions.copy()
    applied_challenge = "No Shock"
    applied_strength = "None"

active_shock_outputs = calculate_outputs(active_shock_dimensions)

# Recovery output also updates only after RUN RECOVERY TEST. Draft controls do not change the results table.
if st.session_state["p4_has_response_run"]:
    committed_response_dimensions, _ = apply_response(active_shock_dimensions, committed_response)
else:
    committed_response_dimensions = active_shock_dimensions.copy()

committed_response_outputs = calculate_outputs(committed_response_dimensions)

shock_damage_name, shock_damage_delta = get_largest_damage(current_outputs, active_shock_outputs)
shock_resilience = active_shock_outputs["Resilience"]
recovery_name, recovery_delta = get_largest_recovery(active_shock_outputs, committed_response_outputs)
final_resilience = committed_response_outputs["Resilience"]
final_resilience_label = classify_resilience(final_resilience)
remaining_risk_name = "Fiscal Pressure"
remaining_risk_value = committed_response_outputs["Fiscal Pressure"]

# Ribbon
st.html(
    f"""
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">CURRENT PAGE</div>
            <div class="p1-kpi-main">P4 Challenge Mode</div>
            <div class="p1-kpi-sub">Stress-test stage</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#38BDF8;">COUNTRY</div>
            <div class="p1-kpi-main">{selected_country}</div>
            <div class="p1-kpi-sub">{selected_family}</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#84CC16;">CURRENT STRATEGY</div>
            <div class="p1-kpi-main">Selected Strategy</div>
            <div class="p1-kpi-sub">From P3 or baseline fallback</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F59E0B;">CHALLENGE</div>
            <div class="p1-kpi-main">{selected_challenge}</div>
            <div class="p1-kpi-sub">{selected_strength} strength</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F472B6;">VULNERABILITY</div>
            <div class="p1-kpi-main">{shock_damage_name}</div>
            <div class="p1-kpi-sub">After shock</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">REFERENCE</div>
            <div class="p1-kpi-main">{selected_reference}</div>
            <div class="p1-kpi-sub">Comparison context</div>
        </div>
    </div>
    """
)

render_intro_box()


# =============================================================================
# PAGE FRAME
# =============================================================================

left_col, main_col, right_col = st.columns([0.85, 5.4, 1.15], gap="medium")

sections = [
    ("01", "EXPLAIN", "What is this?"),
    ("02", "SHOCK", "What happened?"),
    ("03", "RECOVER", "Can I improve it?"),
    ("04", "LEARN", "Interpret result."),
    ("05", "CONTINUE", "Next step."),
    ("06", "LOG", "Journey record."),
]

with left_col:
    render_left_rail_placeholder(page_number=4, page_title="Challenge Mode", sections=sections)

with main_col:
    # =========================================================================
    # SECTION 02 — CHALLENGE TEST
    # =========================================================================
    render_section_title(
        number="02",
        title="What did the challenge do?",
        subtitle="First apply the disruption and observe how the selected strategy is affected before trying to recover.",
    )

    st.html(
        """
        <div class="p4-workspace-help">
            <div class="p4-help-title">Challenge Test Flow</div>
            <div class="p4-help-text">
                1 Choose a challenge and strength → 2 Read the scenario → 3 Run the challenge → 4 Observe Current → Shock damage.
            </div>
        </div>
        """
    )

    choose_col, scenario_col, damage_col = st.columns([1.25, 1.45, 3.40], gap="medium")

    with choose_col:
        st.markdown("### 1 · Choose Challenge")
        st.html(
            """
            <div class="p4-panel" style="min-height:unset;">
                <div class="p4-small-label">Active Scenarios</div>
                <div class="p4-panel-text">Only Energy Crisis and Pandemic Pressure are active in the MVP.</div>
            </div>
            """
        )
        for challenge_name in ACTIVE_CHALLENGES.keys():
            label = f"✓ {challenge_name}" if selected_challenge == challenge_name else challenge_name
            if st.button(label, key=f"p4_challenge_{challenge_name}", use_container_width=True):
                set_challenge(challenge_name)
                # Selection changes the draft shock only. Results stay committed until Apply Shock.
                st.rerun()

        st.markdown("### Strength")
        selected_strength_radio = st.radio(
            "Challenge Strength",
            options=["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(selected_strength),
            key="p4_strength_radio_v08",
            label_visibility="collapsed",
        )
        if selected_strength_radio != selected_strength:
            set_strength(selected_strength_radio)
            # Strength changes the draft shock only. Results stay committed until Apply Shock.
            st.rerun()

        if st.button("Reset / No Shock", key="p4_reset_no_shock", use_container_width=True):
            st.session_state["p4_has_challenge_run"] = False
            st.session_state["p4_has_response_run"] = False
            st.session_state["p4_applied_challenge"] = "No Shock"
            st.session_state["p4_applied_strength"] = "None"
            st.session_state["p4_committed_response"] = DEFAULT_RESPONSE.copy()
            reset_response()
            st.rerun()

        render_coming_soon_panel()

    with scenario_col:
        st.markdown("### 2 · Scenario & Apply")
        render_challenge_description(selected_challenge, selected_strength)
        st.html("<div style='height:10px;'></div>")
        st.html(
            """
            <div class="p4-panel" style="min-height:unset; border-color:rgba(245,158,11,0.62);">
                <div class="p4-small-label">Apply Shock</div>
                <div class="p4-panel-text">
                    Apply the selected disruption before trying to recover. This commits the shock state used in the damage table.
                </div>
            </div>
            """
        )
        if st.button("Load Current", key="p4_load_current_shock", use_container_width=True):
            st.session_state["p4_has_challenge_run"] = False
            st.session_state["p4_has_response_run"] = False
            st.session_state["p4_applied_challenge"] = "No Shock"
            st.session_state["p4_applied_strength"] = "None"
            st.session_state["p4_committed_response"] = DEFAULT_RESPONSE.copy()
            reset_response()
            st.rerun()

        if st.button("⚡ APPLY SHOCK", key="p4_run_challenge", use_container_width=True):
            st.session_state["p4_has_challenge_run"] = True
            st.session_state["p4_has_response_run"] = False
            st.session_state["p4_applied_challenge"] = selected_challenge
            st.session_state["p4_applied_strength"] = selected_strength
            st.session_state["p4_committed_response"] = DEFAULT_RESPONSE.copy()
            reset_response()
            st.rerun()

        if st.session_state["p4_has_challenge_run"]:
            run_state = f"Applied:<br>{applied_challenge}<br>{applied_strength} strength"
        else:
            run_state = "Current reference state:<br>No shock applied"
        st.html(f"""
            <div class="p4-run-ready-note">
                {run_state}
            </div>
        """)

    with damage_col:
        st.markdown("### 3 · Observe Damage")
        if not st.session_state["p4_has_challenge_run"]:
            st.markdown(
                "<div class='p4-section-hint'>No shock is applied yet. The table shows the current reference state until you press Apply Shock.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='p4-section-hint'>This is the applied shock result. This becomes the starting point for recovery.</div>",
                unsafe_allow_html=True,
            )
        render_dimension_damage_table(current_dimensions, active_shock_dimensions)
        render_shock_observation_box(shock_damage_name, shock_damage_delta, shock_resilience, applied_challenge, applied_strength)

    # =========================================================================
    # SECTION 03 — RECOVERY TEST
    # =========================================================================
    render_section_title(
        number="03",
        title="Can I improve it with a response package?",
        subtitle="Now respond to the disrupted state. This reuses the P3 table logic: adjust, run, observe correction.",
    )

    st.html(
        """
        <div class="p4-workspace-help">
            <div class="p4-help-title">Recovery Test Flow</div>
            <div class="p4-help-text">
                1 Start from the shock result → 2 Build a response package → 3 Run recovery test → 4 Observe Shock → Response recovery.
            </div>
        </div>
        """
    )

    top_status_col, top_flow_col = st.columns([1.15, 4.45], gap="medium")
    with top_status_col:
        st.html(
            f"""
            <div class="p4-panel" style="min-height:unset;">
                <div class="p4-small-label">Starting Point</div>
                <div class="p4-panel-title">{applied_challenge}</div>
                <div class="p4-panel-text">
                    Strength: <b>{applied_strength}</b><br>
                    Largest damage: <b>{shock_damage_name}</b><br>
                    Shock resilience: <b>{shock_resilience:.0f}/100</b>
                </div>
            </div>
            """
        )
    with top_flow_col:
        st.html("""
            <div class="p4-panel" style="min-height:unset;">
                <div class="p4-small-label">Recovery Logic</div>
                <div class="p4-panel-text">
                    Recovery starts from the applied shock state. Build a response package, run the recovery test, then compare
                    <b>Ref → Shock → Response Test</b> in the output table.
                </div>
            </div>
        """)

    response_col, recovery_run_col, results_col = st.columns([2.75, 0.85, 2.10], gap="medium")

    with response_col:
        st.markdown("### 1 · Build Response")
        render_response_table(current_response)
        draft_response = {area: int(st.session_state[f"p4_response_{area}"]) for area in RESPONSE_AREAS}
        total_response = sum(draft_response.values())
        if total_response == 100:
            st.success("✓ Response package totals 100%. Ready to run.")
        elif total_response < 100:
            st.warning(f"Response package totals {total_response}%. Add {100 - total_response}% before running.")
        else:
            st.error(f"Response package totals {total_response}%. Reduce {total_response - 100}% before running.")

    # Refresh draft controls only. The results table below uses committed_response_outputs,
    # so +/- edits do not change outputs until RUN RECOVERY TEST is pressed.
    draft_response = {area: int(st.session_state[f"p4_response_{area}"]) for area in RESPONSE_AREAS}
    total_response = sum(draft_response.values())

    with recovery_run_col:
        st.markdown("### 2 · Run")
        st.markdown(
            "<div class='p4-section-hint'>Run only after the response totals 100%.</div>",
            unsafe_allow_html=True,
        )
        if st.button("Load Last Test", key="p4_load_last_response", use_container_width=True):
            st.info("Last response is already loaded in the draft controls.")

        if st.button("Reset Response", key="p4_reset_response", use_container_width=True):
            reset_response()
            st.session_state["p4_has_response_run"] = False
            st.rerun()

        modified_text = "Response Modified" if response_modified(draft_response) else "Baseline Response"
        if total_response == 100:
            st.html(
                f"""
                <div class="p4-run-ready-note">
                    Ready:<br>{applied_challenge}<br>{applied_strength} strength<br>{modified_text}
                </div>
                """
            )
        else:
            st.html(
                f"""
                <div class="p4-run-ready-note" style="color:#FECACA; border-color:rgba(239,68,68,0.42); background:rgba(127,29,29,0.24);">
                    Response total: {total_response}%<br>Must equal 100%.
                </div>
                """
            )

        if st.button("🛠 RUN RECOVERY TEST", key="p4_run_recovery", use_container_width=True, disabled=(total_response != 100 or not st.session_state["p4_has_challenge_run"])):
            # Commit the draft response. Results update only after this button.
            st.session_state["p4_committed_response"] = draft_response.copy()
            st.session_state["p4_has_response_run"] = True
            committed_preview_dimensions, _ = apply_response(active_shock_dimensions, draft_response)
            committed_preview_outputs = calculate_outputs(committed_preview_dimensions)
            committed_recovery_name, committed_recovery_delta = get_largest_recovery(active_shock_outputs, committed_preview_outputs)
            committed_final_resilience = committed_preview_outputs["Resilience"]
            committed_final_label = classify_resilience(committed_final_resilience)
            entry = {
                "step": 4,
                "page": "P4 Challenge Mode",
                "country": selected_country,
                "challenge": applied_challenge,
                "strength": applied_strength,
                "response": response_to_text(draft_response),
                "largest_damage": f"{shock_damage_name} ({shock_damage_delta:+.1f})",
                "largest_recovery": f"{committed_recovery_name} ({committed_recovery_delta:+.1f})",
                "resilience": f"{committed_final_resilience:.0f}/100 ({committed_final_label})",
                "learning": f"Shock stressed {shock_damage_name}; response mainly improved {committed_recovery_name}.",
                "next_step": "Reflect or test another challenge",
            }
            st.session_state["p4_journey_log"].append(entry)
            st.rerun()

    with results_col:
        st.markdown("### 3 · Observe Recovery")
        if not st.session_state["p4_has_response_run"]:
            st.markdown(
                "<div class='p4-section-hint'>No recovery test has been run yet. The table shows Shock = Response until you run recovery.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='p4-section-hint'>This table shows the last executed recovery result.</div>",
                unsafe_allow_html=True,
            )
        render_recovery_output_table(
            current_outputs,
            active_shock_outputs,
            committed_response_outputs,
            recovery_name,
            recovery_delta,
            final_resilience,
            final_resilience_label,
            remaining_risk_name,
            remaining_risk_value,
        )

    # =========================================================================
    # SECTION 04 — LEARNING SUMMARY
    # =========================================================================
    render_section_title(
        number="04",
        title="What did we learn?",
        subtitle="Read the two-step story: what the shock damaged, what the response recovered, and what still remains vulnerable.",
    )

    st.markdown("#### Shock Summary")
    render_shock_summary_cards(shock_damage_name, shock_damage_delta, shock_resilience)

    st.markdown("#### Recovery Summary")
    render_recovery_summary_cards(recovery_name, recovery_delta, remaining_risk_name, final_resilience)

    render_ai_insight_panel(
        title="Challenge Reflection",
        observation=f"{applied_challenge} created the largest damage in {shock_damage_name}. The response package mainly improved {recovery_name}.",
        interpretation=f"The strategy shows {final_resilience_label.lower()} final resilience after applying the response. The remaining risk is {remaining_risk_name}, which should be read as a tradeoff rather than a failure.",
        limitation="This is an educational stress test based on simplified registry assumptions. It is not a forecast, prediction, or policy recommendation.",
        next_question="Would a different P3 strategy, country, or family recover differently under the same challenge?",
    )

    # =========================================================================
    # SECTION 05 — CTA
    # =========================================================================
    render_section_title(
        number="05",
        title="Where should we go next?",
        subtitle="Continue the learning journey, revise the strategy, or test another disruption.",
    )

    cta1, cta2, cta3, cta4, cta5 = st.columns(5, gap="medium")
    with cta1:
        with st.container(border=True):
            render_atlas_card(
                title="Adjust",
                value="Return to Strategy",
                delta_text="Back to P3.",
                status="Revise the starting strategy.",
                delta_color="#38BDF8",
                card_class="atlas-gap-card atlas-gap-card-top atlas-cta-navigation",
            )
            if st.button("Adjust Strategy", key="p4_cta_adjust", use_container_width=True):
                safe_switch_page("pages/p3_strategic_choices.py")
    with cta2:
        with st.container(border=True):
            render_atlas_card(
                title="Try Again",
                value="Another Challenge",
                delta_text="Stay on P4.",
                status="Test another active scenario.",
                delta_color="#F59E0B",
                card_class="atlas-gap-card atlas-gap-card-top atlas-cta-challenge",
            )
            if st.button("Try Another", key="p4_cta_another", use_container_width=True):
                st.session_state["p4_has_challenge_run"] = False
                st.session_state["p4_has_response_run"] = False
                st.session_state["p4_applied_challenge"] = "No Shock"
                st.session_state["p4_applied_strength"] = "None"
                st.session_state["p4_committed_response"] = DEFAULT_RESPONSE.copy()
                reset_response()
                st.rerun()
    with cta3:
        with st.container(border=True):
            render_atlas_card(
                title="Compare",
                value="Countries",
                delta_text="Change exposure.",
                status="Select another country at the top.",
                delta_color="#22D3EE",
                card_class="atlas-gap-card atlas-gap-card-top atlas-cta-compare",
            )
            st.button("Compare", key="p4_cta_compare", use_container_width=True, disabled=True)
    with cta4:
        with st.container(border=True):
            render_atlas_card(
                title="Explore",
                value="Families",
                delta_text="Family-level resilience.",
                status="Future feature.",
                delta_color="#84CC16",
                card_class="atlas-gap-card atlas-gap-card-top atlas-cta-explore",
            )
            st.button("Explore", key="p4_cta_families", use_container_width=True, disabled=True)
    with cta5:
        with st.container(border=True):
            render_atlas_card(
                title="Reflect",
                value="Learning Summary",
                delta_text="Move to P5.",
                status="Turn this into a learning record.",
                delta_color="#A855F7",
                card_class="atlas-gap-card atlas-gap-card-top atlas-cta-reflect",
            )
            if st.button("Reflect & Learn", key="p4_cta_reflect", use_container_width=True):
                safe_switch_page("pages/p5_reflection.py")

with right_col:
    latest_entry = st.session_state["p4_journey_log"][-1] if st.session_state["p4_journey_log"] else {
        "challenge": applied_challenge,
        "strength": applied_strength,
        "largest_damage": f"{shock_damage_name} ({shock_damage_delta:+.1f})" if st.session_state["p4_has_challenge_run"] else "Run Challenge Test",
        "largest_recovery": f"{recovery_name} ({recovery_delta:+.1f})" if st.session_state["p4_has_response_run"] else "Run Recovery Test",
        "resilience": f"{final_resilience:.0f}/100 ({final_resilience_label})" if st.session_state["p4_has_response_run"] else f"Shock: {shock_resilience:.0f}/100",
        "next_step": "Reflect or test another challenge" if st.session_state["p4_has_response_run"] else "Run Challenge Test",
    }
    render_p4_mission_log_panel(latest_entry)

# =============================================================================
# FULL-WIDTH JOURNEY LOG + FOOTER
# =============================================================================

st.markdown("---")
st.html(
    """
    <div style="border:1px solid rgba(245,158,11,0.30); border-radius:14px; background:rgba(120,53,15,0.20); padding:12px 16px; margin-bottom:10px;">
        <div style="color:#FBBF24; font-size:0.76rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:4px;">Journey Log</div>
        <div style="color:#E2E8F0; font-size:0.92rem; line-height:1.4;">Full-width record of challenge and recovery tests created during this page.</div>
    </div>
    """
)

if st.session_state["p4_journey_log"]:
    journey_log_df = pd.DataFrame(st.session_state["p4_journey_log"])
else:
    journey_log_df = pd.DataFrame([
        {
            "step": 4,
            "page": "P4 Challenge Mode",
            "country": selected_country,
            "challenge": applied_challenge,
            "strength": applied_strength,
            "response": response_to_text(draft_response),
            "largest_damage": f"{shock_damage_name} ({shock_damage_delta:+.1f})",
            "largest_recovery": "Run Recovery Test",
            "resilience": f"Shock: {shock_resilience:.0f}/100",
            "learning": "Run challenge and recovery tests to create the first mission entry.",
            "next_step": "Run Challenge Test",
        }
    ])

with st.expander("View Full Journey Log", expanded=False):
    render_journey_log_html(journey_log_df)

render_footer()
