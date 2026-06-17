"""
p1_country_explorer_v02_guided_learning.py

European Strategy Atlas — Page 1
Country Explorer / Guided Learning Refinement

Version:
P1 VERSION v07_TABLE_FLOW_CHART_LOG_FIX

Purpose
-------
Page 1 answers:

"Where is this country today?"

This version preserves the approved P1 concept and aligns the page with the
interaction grammar that emerged from P2–P4:

Observe
→ Interpret
→ Explore Further

Key refinements:
- Section 01: updated wording and observation-oriented cards
- Section 02A: structural evolution retained
- Section 02B: new investment profile multi-line chart
- Section 03: comparison table vs selected reference + always-visible EU context
- Section 04: interpretation / learning insight
- Section 05: guided next actions + journey log
- Right Mission Log simplified to match P2–P4
"""

# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.typography import (
    render_section_title,
    render_subsection_title,
)
from utils.chart_utils import (
    create_country_timeline_chart,
    create_dimension_radar_chart,
)
from utils.data_loader import (
    load_profiles,
    load_families,
    load_country_profile,
    create_country_story,
    load_country_year,
    build_country_timeline,
    build_family_reference_profile,
    build_dimension_gap_table,
    build_eu_reference_profile,
    build_country_reference_profile,
)
from utils.app_config import (
    PRIORITY_COUNTRIES,
    DEFAULT_COUNTRY,
    DEFAULT_REFERENCE_TYPE,
    DEFAULT_REFERENCE_COUNTRY,
)
from utils.insight_rules import (
    get_key_strengths,
    get_key_constraints,
)
from utils.atlas_state import init_atlas_state, update_atlas_context


# =============================================================================
# LOAD GLOBAL CSS
# =============================================================================

def load_css():
    """Load Atlas CSS theme."""
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.html("""
<style>
.p3-full-width-shell {
    max-width:1500px;
    margin: 0 auto;
}
</style>
""")


# =============================================================================
# PAGE-SPECIFIC CSS
# =============================================================================

st.html(
    """
    <style>
    .p1-version-badge {
        color:#94A3B8;
        font-size:0.72rem;
        font-weight:800;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin:0 0 8px 0;
    }

    .p1-intro-box {
        border:1px solid rgba(56,189,248,0.30);
        border-radius:16px;
        padding:16px 20px;
        background:linear-gradient(135deg, rgba(15,23,42,0.94), rgba(15,23,42,0.70));
        margin: 4px 0 16px 0;
    }
    .p1-intro-title {
        color:#38BDF8;
        font-size:0.76rem;
        font-weight:900;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:7px;
    }
    .p1-intro-text {
        color:#E2E8F0;
        font-size:1.02rem;
        line-height:1.48;
        font-weight:700;
    }

    .p1-observation-box {
        border:1px solid rgba(56,189,248,0.28);
        border-left:4px solid #38BDF8;
        border-radius:14px;
        padding:13px 15px;
        background:rgba(15,23,42,0.76);
        margin:10px 0;
    }
    .p1-observation-title {
        color:#38BDF8;
        font-size:0.72rem;
        font-weight:900;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:6px;
    }
    .p1-observation-text {
        color:#E2E8F0;
        font-size:0.92rem;
        line-height:1.40;
        font-weight:700;
    }

    .p1-guided-card {
        border:1px solid rgba(148,163,184,0.24);
        border-radius:16px;
        padding:15px 17px;
        background:rgba(15,23,42,0.80);
        min-height:126px;
        box-shadow:0 0 20px rgba(0,0,0,0.18);
    }
    .p1-guided-label {
        color:#94A3B8;
        font-size:0.68rem;
        font-weight:900;
        letter-spacing:0.09em;
        text-transform:uppercase;
        margin-bottom:8px;
    }
    .p1-guided-value {
        color:#F8FAFC;
        font-size:1.05rem;
        font-weight:950;
        line-height:1.20;
        margin-bottom:8px;
    }
    .p1-guided-text {
        color:#CBD5E1;
        font-size:0.84rem;
        line-height:1.35;
        font-weight:700;
    }

    .p1-table-card {
        border:1px solid rgba(56,189,248,0.34);
        border-radius:16px;
        padding:16px 18px;
        background:rgba(15,23,42,0.80);
        margin-top:8px;
        box-shadow:0 0 22px rgba(56,189,248,0.08);
    }
    .p1-table-title {
        color:#F8FAFC;
        font-size:1.08rem;
        font-weight:950;
        margin-bottom:5px;
    }
    .p1-table-subtitle {
        color:#CBD5E1;
        font-size:0.86rem;
        line-height:1.36;
        margin-bottom:12px;
    }
    .p1-compare-table {
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        color:#E5E7EB;
        font-size:0.90rem;
    }
    .p1-compare-table th {
        color:#38BDF8;
        font-size:0.72rem;
        font-weight:900;
        letter-spacing:0.06em;
        text-transform:uppercase;
        text-align:left;
        padding:9px 8px;
        border-bottom:1px solid rgba(56,189,248,0.32);
        white-space:nowrap;
    }
    .p1-compare-table td {
        padding:10px 8px;
        border-bottom:1px solid rgba(148,163,184,0.16);
        vertical-align:middle;
        line-height:1.28;
    }
    .p1-dim-name {
        color:#F8FAFC;
        font-size:0.92rem;
        font-weight:900;
        line-height:1.20;
    }
    .p1-table-score {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.92rem;
        font-weight:950;
        color:#F8FAFC;
        white-space:nowrap;
    }
    .p1-table-delta {
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:0.98rem;
        font-weight:950;
        white-space:nowrap;
    }
    .p1-table-reading {
        font-size:0.84rem;
        font-weight:900;
        line-height:1.20;
    }

    .p1-mini-eu-table {
        width:100%;
        border-collapse:collapse;
        color:#E5E7EB;
        font-size:0.82rem;
    }
    .p1-mini-eu-table th {
        color:#38BDF8;
        font-size:0.68rem;
        font-weight:900;
        letter-spacing:0.05em;
        text-transform:uppercase;
        text-align:left;
        padding:7px 6px;
        border-bottom:1px solid rgba(56,189,248,0.28);
    }
    .p1-mini-eu-table td {
        padding:8px 6px;
        border-bottom:1px solid rgba(148,163,184,0.15);
        line-height:1.25;
    }

    .p1-log-panel-v2 {
        position:sticky;
        top:210px;
        border:1px solid rgba(56,189,248,0.32);
        border-radius:16px;
        padding:17px;
        background:linear-gradient(135deg, rgba(15,23,42,0.94), rgba(15,23,42,0.72));
    }
    .p1-log-title {
        color:#38BDF8;
        font-size:0.76rem;
        font-weight:900;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:14px;
    }
    .p1-log-heading {
        color:#F8FAFC;
        font-size:0.94rem;
        font-weight:900;
        margin-top:12px;
        margin-bottom:7px;
    }
    .p1-log-text {
        color:#CBD5E1;
        font-size:0.86rem;
        line-height:1.42;
    }

    .p1-journey-table {
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        color:#E5E7EB;
        font-size:0.88rem;
    }
    .p1-journey-table th {
        color:#38BDF8;
        font-size:0.72rem;
        font-weight:900;
        text-transform:uppercase;
        letter-spacing:0.06em;
        padding:9px 8px;
        border-bottom:1px solid rgba(56,189,248,0.30);
        text-align:left;
    }
    .p1-journey-table td {
        padding:10px 8px;
        border-bottom:1px solid rgba(148,163,184,0.16);
        vertical-align:top;
    }
    </style>
    """
)


# =============================================================================
# LOAD BASE DATA
# =============================================================================

profiles_df = load_profiles()
families_df = load_families()
country_year_df = load_country_year()


# =============================================================================
# HELPERS
# =============================================================================

def safe_switch_page(page_path: str):
    try:
        st.switch_page(page_path)
    except Exception:
        st.info(f"Navigation target not found yet: {page_path}")


def order_countries(country_list, priority_countries):
    """Return countries in UX-friendly order."""
    priority = []
    for country in priority_countries:
        if country in country_list and country not in priority:
            priority.append(country)

    remaining = sorted([country for country in country_list if country not in priority])
    return priority + remaining


def get_delta_color(value):
    try:
        value = float(value)
    except Exception:
        return "#38BDF8"

    if value >= 0.20:
        return "#4ADE80"
    if value <= -0.20:
        return "#F472B6"
    return "#38BDF8"


def classify_gap(gap_value: float) -> tuple[str, str, str]:
    if gap_value >= 0.50:
        return "▲", "Strong advantage", "strength"
    if gap_value >= 0.20:
        return "▲", "Moderate advantage", "strength"
    if gap_value <= -0.50:
        return "▼", "Major constraint", "constraint"
    if gap_value <= -0.20:
        return "▼", "Moderate constraint", "constraint"
    return "→", "Similar to reference", "neutral"


def render_gap_html_card(
    title,
    value,
    delta_text="",
    status="",
    delta_color="#38BDF8",
    card_class="atlas-gap-card",
):
    st.markdown(
        f"""
<div class="{card_class}">
    <div class="atlas-gap-title">{title}</div>
    <div class="atlas-gap-score">{value}</div>
    <div class="atlas-gap-delta" style="color:{delta_color};">{delta_text}</div>
    <div class="atlas-gap-status">{status}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_guided_card(label: str, value: str, text: str, accent: str = "#38BDF8"):
    st.html(
        f"""
        <div class="p1-guided-card" style="border-left:5px solid {accent}; box-shadow:0 0 18px {accent}20;">
            <div class="p1-guided-label" style="color:{accent};">{label}</div>
            <div class="p1-guided-value">{value}</div>
            <div class="p1-guided-text">{text}</div>
        </div>
        """
    )


def render_observation_box(title: str, text: str, accent: str = "#38BDF8"):
    st.html(
        f"""
        <div class="p1-observation-box" style="border-left-color:{accent};">
            <div class="p1-observation-title" style="color:{accent};">{title}</div>
            <div class="p1-observation-text">{text}</div>
        </div>
        """
    )



# =============================================================================
# P1 RADAR — SELECTED COUNTRY + OPTIONAL REFERENCE COUNTRY
# =============================================================================

RADAR_DIMENSION_ORDER = [
    "Innovation Capacity",
    "Human Capital Capacity",
    "Sustainability Capacity",
    "Adaptive Transformation",
    "Security Reprioritization",
    "Fiscal Flexibility",
    "Social Stability",
]

RADAR_DIMENSION_ALIASES = {
    "Innovation Capacity": ["Innovation Capacity", "dim_innovation_capacity", "innovation_capacity"],
    "Human Capital Capacity": ["Human Capital Capacity", "dim_human_capital_capacity", "human_capital_capacity"],
    "Sustainability Capacity": ["Sustainability Capacity", "dim_sustainability_capacity", "sustainability_capacity"],
    "Adaptive Transformation": ["Adaptive Transformation", "dim_adaptive_transformation", "adaptive_transformation"],
    "Security Reprioritization": ["Security Reprioritization", "dim_security_reprioritization", "security_reprioritization"],
    "Fiscal Flexibility": ["Fiscal Flexibility", "dim_fiscal_flexibility", "fiscal_flexibility"],
    "Social Stability": ["Social Stability", "dim_social_stability", "social_stability"],
}


def _get_nested_dimension_value(profile, label: str) -> float:
    """Read one dimension score from a country profile dict/Series safely."""
    aliases = RADAR_DIMENSION_ALIASES.get(label, [label])

    # Preferred structure from load_country_profile: profile["dimensions"]
    try:
        dims = profile.get("dimensions", {})
    except Exception:
        dims = {}

    if isinstance(dims, dict):
        for key in aliases:
            if key in dims:
                try:
                    return float(dims[key])
                except Exception:
                    pass

    # Fallback: flat dict / pandas Series
    for key in aliases:
        try:
            if key in profile:
                return float(profile[key])
        except Exception:
            pass

    return 0.0


def _radar_values_from_profile(profile) -> list[float]:
    return [_get_nested_dimension_value(profile, dim) for dim in RADAR_DIMENSION_ORDER]



def create_p1_reference_radar_chart(
    country_profile,
    selected_country: str,
    reference_profile=None,
    reference_country: str | None = None,
):
    """P1 structural radar with direct labels and no Plotly legend.

    Final visual grammar:
    - selected country = purple filled radar polygon
    - selected country direct label = "<country> Structural performance"
    - EU baseline = cyan dotted zero contour
    - optional reference country = thin light-gray dotted contour
    - reference direct label = "<ref country> REF"
    - no Plotly legend, no old trace labels, no undefined placeholders
    """
    theta = RADAR_DIMENSION_ORDER + [RADAR_DIMENSION_ORDER[0]]

    def clean_label(value: object, fallback: str = "") -> str:
        label = str(value or "").strip()
        if label.lower() in {"", "none", "nan", "undefined", "null"}:
            return fallback
        return label

    selected_country_label = clean_label(selected_country, "Selected country")
    reference_country_label = clean_label(reference_country, "")

    has_reference = (
        reference_profile is not None
        and bool(reference_country_label)
        and reference_country_label != selected_country_label
    )

    selected_color = "#8B5CF6"
    reference_color = "#EAB308"
    eu_color = "#38BDF8"

    country_values = _radar_values_from_profile(country_profile)
    country_values_closed = country_values + [country_values[0]]
    eu_values_closed = [0.0 for _ in theta]

    fig = go.Figure()

    # EU baseline — cyan dotted zero contour.
    fig.add_trace(
        go.Scatterpolar(
            r=eu_values_closed,
            theta=theta,
            mode="lines",
            line=dict(
                color=eu_color,
                width=1.15,
                dash="dot",
            ),
            hoverinfo="skip",
            showlegend=False,
            name="",
            legendgroup="",
        )
    )

    # Optional reference country — light-gray dotted contour.
    if has_reference:
        reference_values = _radar_values_from_profile(reference_profile)
        reference_values_closed = reference_values + [reference_values[0]]

        fig.add_trace(
            go.Scatterpolar(
                r=reference_values_closed,
                theta=theta,
                mode="lines",
                line=dict(
                    color=reference_color,
                    width=1.15,
                    dash="dot",
                ),
                hovertemplate=(
                    f"<b>{reference_country_label} REF</b><br>"
                    "%{theta}: %{r:.2f}<extra></extra>"
                ),
                showlegend=False,
                name="",
                legendgroup="",
            )
        )

    # Selected country — main purple filled profile.
    fig.add_trace(
        go.Scatterpolar(
            r=country_values_closed,
            theta=theta,
            mode="lines",
            line=dict(
                color=selected_color,
                width=2.35,
            ),
            fill="toself",
            fillcolor="rgba(139,92,246,0.36)",
            hovertemplate=(
                f"<b>{selected_country_label}</b><br>"
                "%{theta}: %{r:.2f}<extra></extra>"
            ),
            showlegend=False,
            name="",
            legendgroup="",
        )
    )

    annotations = [
        # #1 selected country label — top-center above radar.
        dict(
            x=0.50,
            y=1.085,
            xref="paper",
            yref="paper",
            text=f"<b>{selected_country_label}</b> Structural performance",
            showarrow=False,
            font=dict(
                color=selected_color,
                size=15,
            ),
            align="center",
            xanchor="center",
            yanchor="bottom",
        ),
        # EU baseline label — center anchor.
        dict(
            x=0.50,
            y=0.50,
            xref="paper",
            yref="paper",
            text="EU = 0 baseline",
            showarrow=False,
            font=dict(
                color=eu_color,
                size=11,
            ),
            align="center",
            xanchor="center",
            yanchor="middle",
        ),
    ]

    # #2 reference country label — lower/right inside radar.
    if has_reference:
        annotations.append(
            dict(
                x=0.72,
                y=0.34,
                xref="paper",
                yref="paper",
                text=f"{reference_country_label} REF",
                showarrow=False,
                font=dict(
                    color=reference_color,
                    size=11,
                ),
                align="center",
                xanchor="center",
                yanchor="middle",
            )
        )

    fig.update_layout(
        title=dict(text=""),
        showlegend=False,
        legend=dict(
            visible=False,
            x=0,
            y=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=1, color="rgba(0,0,0,0)"),
        ),
        annotations=annotations,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#E5E7EB",
            size=12,
        ),
        height=455,
        margin=dict(
            l=38,
            r=38,
            t=74,
            b=56,
        ),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[-1.5, 1.6],
                tickvals=[-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5],
                tickfont=dict(
                    color="#CBD5E1",
                    size=10,
                ),
                gridcolor="rgba(148,163,184,0.26)",
                linecolor="rgba(148,163,184,0.30)",
            ),
            angularaxis=dict(
                tickfont=dict(
                    color="#F8FAFC",
                    size=11,
                ),
                gridcolor="rgba(148,163,184,0.18)",
                linecolor="rgba(148,163,184,0.22)",
            ),
        ),
    )

    # Final hard guard: remove all Plotly legend text, including "undefined".
    for trace in fig.data:
        trace.update(
            showlegend=False,
            name="",
            legendgroup="",
        )

    return fig

def format_score(value, view_mode: str = "Relative") -> str:
    if pd.isna(value):
        return "—"
    try:
        value = float(value)
    except Exception:
        return str(value)

    if view_mode == "Absolute":
        return f"{value:.2f}"
    return f"{value:+.2f}"


def build_comparison_table_rows(
    gap_df: pd.DataFrame,
    eu_gap_df: pd.DataFrame,
    view_mode: str,
    country_label: str,
    reference_label: str,
):
    """Build rows for the main comparison table.

    Column logic is intentionally separated:
    - Δ vs EU is computed from the EU reference profile.
    - Δ vs selected reference is computed from the selected reference profile.
    This prevents the two comparison colors/values from being mixed.
    """
    rows = []
    working = gap_df.copy()
    eu_lookup = {}

    if not eu_gap_df.empty and "dimension" in eu_gap_df.columns:
        eu_lookup = {row.get("dimension"): row for _, row in eu_gap_df.iterrows()}

    if "gap" in working.columns:
        working = working.sort_values("gap", ascending=False)

    for _, row in working.iterrows():
        dimension = row.get("dimension", "Dimension")
        country_value = row.get("country_value", np.nan)
        reference_value = row.get("reference_value", np.nan)
        ref_gap_value = row.get("gap", np.nan)

        eu_row = eu_lookup.get(dimension)
        if eu_row is not None:
            eu_value = eu_row.get("reference_value", 0.0)
            eu_gap_value = eu_row.get("gap", np.nan)
        else:
            eu_value = 0.0 if view_mode == "Relative" else np.nan
            eu_gap_value = np.nan

        eu_arrow, eu_reading, _ = classify_gap(float(eu_gap_value) if not pd.isna(eu_gap_value) else 0.0)
        ref_arrow, _ref_reading, _ = classify_gap(float(ref_gap_value) if not pd.isna(ref_gap_value) else 0.0)

        eu_accent = get_delta_color(eu_gap_value) if not pd.isna(eu_gap_value) else "#38BDF8"
        ref_accent = get_delta_color(ref_gap_value) if not pd.isna(ref_gap_value) else "#38BDF8"

        rows.append(
            f"""
            <tr>
                <td><span class="p1-dim-name">{dimension}</span></td>
                <td><span class="p1-table-score">{format_score(country_value, view_mode)}</span></td>
                <td><span class="p1-table-score">{format_score(eu_value, view_mode)}</span><br><span style="color:#94A3B8;font-size:0.74rem;">EU avg</span></td>
                <td><span class="p1-table-delta" style="color:{eu_accent};">{eu_arrow} {float(eu_gap_value):+.2f}</span></td>
                <td><span class="p1-table-reading" style="color:{eu_accent};">{eu_reading}</span></td>
                <td><span class="p1-table-score">{format_score(reference_value, view_mode)}</span><br><span style="color:#94A3B8;font-size:0.74rem;">{reference_label}</span></td>
                <td><span class="p1-table-delta" style="color:{ref_accent};">{ref_arrow} {float(ref_gap_value):+.2f}</span></td>
            </tr>
            """
        )

    return rows


def render_comparison_table(
    gap_df: pd.DataFrame,
    eu_gap_df: pd.DataFrame,
    country_label: str,
    reference_label: str,
    view_mode: str,
):
    rows = build_comparison_table_rows(
        gap_df=gap_df,
        eu_gap_df=eu_gap_df,
        view_mode=view_mode,
        country_label=country_label,
        reference_label=reference_label,
    )

    st.html(
        f"""
        <div class="p1-table-card">
            <div class="p1-table-title">{country_label} vs EU Average and {reference_label}</div>
            <div class="p1-table-subtitle">
                One full-width table keeps the European baseline and the selected reference visible together.
                The two delta columns are calculated and colored independently.
            </div>
            <table class="p1-compare-table" style="font-size:1.04rem;">
                <colgroup>
                    <col style="width:23%;">
                    <col style="width:11%;">
                    <col style="width:11%;">
                    <col style="width:13%;">
                    <col style="width:17%;">
                    <col style="width:13%;">
                    <col style="width:12%;">
                </colgroup>
                <thead>
                    <tr>
                        <th>Dimension</th>
                        <th>{country_label}</th>
                        <th>EU</th>
                        <th>Δ vs EU</th>
                        <th>Reading</th>
                        <th>{reference_label}</th>
                        <th>Δ vs {reference_label}</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )

def render_eu_context_table(eu_gap_df: pd.DataFrame, selected_country: str, view_mode: str):
    working = eu_gap_df.copy()
    if "gap" in working.columns:
        working = working.sort_values("gap", ascending=False)

    rows = []
    for _, row in working.iterrows():
        dimension = row.get("dimension", "Dimension")
        country_value = row.get("country_value", np.nan)
        gap_value = row.get("gap", np.nan)
        accent = get_delta_color(gap_value)
        rows.append(
            f"""
            <tr>
                <td>{dimension}</td>
                <td><span style="font-family:'IBM Plex Mono','Roboto Mono',monospace;font-weight:900;">{format_score(country_value, view_mode)}</span></td>
                <td><span style="color:{accent};font-family:'IBM Plex Mono','Roboto Mono',monospace;font-weight:900;">{float(gap_value):+.2f}</span></td>
            </tr>
            """
        )

    st.html(
        f"""
        <div class="p1-table-card">
            <div class="p1-table-title">EU Context</div>
            <div class="p1-table-subtitle">
                Always shown so selected references do not hide the European baseline.
            </div>
            <table class="p1-mini-eu-table">
                <thead>
                    <tr>
                        <th>Dimension</th>
                        <th>{selected_country}</th>
                        <th>vs EU</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """
    )


def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def create_investment_profile_chart(country_year_df: pd.DataFrame, selected_country: str, view_mode: str):
    """Create investment profile multi-line chart with vertical year gridlines.

    Relative mode:
        Shows each investment indicator as change versus the first available year.
        This avoids one large spending category hiding smaller but important trends.

    Absolute mode:
        Shows raw values from app dataset columns.
    """
    df = country_year_df[country_year_df["country_name"] == selected_country].copy()

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No country-year data available.",
            showarrow=False,
            font=dict(color="#E5E7EB", size=14),
        )
        return fig

    df = df.sort_values("year")

    metric_map = {
        "Education": ["education_spending", "education_spending_value"],
        "R&D": ["rnd", "rnd_spending", "research_development_spending"],
        "Social Protection": ["social_protection_spending"],
        "Environment": ["environment_spending"],
        "Defense": ["defense_spending"],
    }

    selected_cols = {}
    for label, candidates in metric_map.items():
        col = find_column(df, candidates)
        if col is not None:
            selected_cols[label] = col

    if not selected_cols:
        fig = go.Figure()
        fig.add_annotation(
            text="Investment columns not found in country-year table.",
            showarrow=False,
            font=dict(color="#E5E7EB", size=14),
        )
        return fig

    plot_df = df[["year"] + list(selected_cols.values())].copy()
    plot_df = plot_df.rename(columns={v: k for k, v in selected_cols.items()})

    labels = list(selected_cols.keys())
    for label in labels:
        plot_df[label] = pd.to_numeric(plot_df[label], errors="coerce")

    plot_df = plot_df.ffill().bfill().fillna(0)

    if view_mode == "Relative":
        # Show each investment line relative to its own country average.
        # This makes deviations from the country's normal investment profile visible.
        for label in labels:
            series = plot_df[label].astype(float)
            non_zero = series.replace(0, np.nan).dropna()
            if non_zero.empty:
                plot_df[label] = 0.0
            else:
                baseline = float(non_zero.mean())
                if baseline == 0:
                    plot_df[label] = 0.0
                else:
                    plot_df[label] = ((series / baseline) - 1.0) * 100.0
        y_title = f"Deviation vs {selected_country} average (%)"
        chart_title_suffix = "relative to country average"
        hover_suffix = "%"
    else:
        y_title = "Raw indicator value"
        chart_title_suffix = "raw values"
        hover_suffix = ""

    colors = {
        "Education": "#60A5FA",
        "R&D": "#F472B6",
        "Social Protection": "#F59E0B",
        "Environment": "#84CC16",
        "Defense": "#22D3EE",
    }

    fig = go.Figure()

    for label in labels:
        fig.add_trace(
            go.Scatter(
                x=plot_df["year"],
                y=plot_df[label],
                mode="lines+markers",
                name=label,
                line=dict(
                    width=3.0,
                    color=colors.get(label, "#38BDF8"),
                ),
                marker=dict(
                    size=7,
                    line=dict(width=1, color="rgba(15,23,42,0.95)"),
                ),
                hovertemplate=f"{label}<br>Year: %{{x}}<br>Value: %{{y:.2f}}{hover_suffix}<extra></extra>",
            )
        )

    years = sorted(plot_df["year"].dropna().unique().tolist())

    if years:
        for year in years:
            fig.add_vline(
                x=year,
                line_width=0.7,
                line_dash="dot",
                line_color="rgba(148,163,184,0.28)",
                layer="below",
            )

        if min(years) <= 2020 <= max(years):
            fig.add_vrect(
                x0=2020,
                x1=2022,
                fillcolor="rgba(239,68,68,0.08)",
                line_width=0,
                layer="below",
                annotation_text="COVID transition",
                annotation_position="top left",
            )
        if min(years) <= 2022 <= max(years):
            fig.add_vrect(
                x0=2022,
                x1=max(years),
                fillcolor="rgba(56,189,248,0.07)",
                line_width=0,
                layer="below",
            )

    if view_mode == "Relative":
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="rgba(226,232,240,0.55)",
            line_width=1,
        )

    fig.update_layout(
        title=dict(
            text=f"{selected_country} investment profile - relative to {selected_country} average" if view_mode == "Relative" else f"{selected_country} investment profile - {chart_title_suffix}",
            font=dict(color="#F8FAFC", size=19),
            x=0.0,
            xanchor="left",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.35)",
        font=dict(color="#E5E7EB", size=14),
        margin=dict(l=64, r=28, t=74, b=56),
        height=440,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=13, color="#E5E7EB"),
            bgcolor="rgba(15,23,42,0.20)",
        ),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=15, color="#CBD5E1")),
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="rgba(148,163,184,0.18)",
            tickfont=dict(size=13, color="#CBD5E1"),
            linecolor="rgba(148,163,184,0.35)",
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=15, color="#CBD5E1")),
            showgrid=True,
            gridcolor="rgba(148,163,184,0.16)",
            tickfont=dict(size=13, color="#CBD5E1"),
            zeroline=False,
            linecolor="rgba(148,163,184,0.35)",
        ),
        hovermode="x unified",
    )

    return fig


def align_timeline_chart_style(fig, selected_country: str):
    """Align imported structural evolution chart styling with the P1 investment chart."""
    try:
        fig.update_layout(
            height=440,
            font=dict(color="#E5E7EB", size=14),
            margin=dict(l=64, r=28, t=74, b=56),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.03,
                xanchor="left",
                x=0,
                font=dict(size=13, color="#E5E7EB"),
                bgcolor="rgba(15,23,42,0.20)",
            ),
            xaxis=dict(
                title=dict(text="Year", font=dict(size=15, color="#CBD5E1")),
                tickmode="linear",
                dtick=1,
                showgrid=True,
                gridcolor="rgba(148,163,184,0.18)",
                tickfont=dict(size=13, color="#CBD5E1"),
                linecolor="rgba(148,163,184,0.35)",
            ),
            yaxis=dict(
                title=dict(text="EU-relative score", font=dict(size=15, color="#CBD5E1")),
                showgrid=True,
                gridcolor="rgba(148,163,184,0.16)",
                tickfont=dict(size=13, color="#CBD5E1"),
                zeroline=False,
                linecolor="rgba(148,163,184,0.35)",
            ),
            hovermode="x unified",
        )
        years = []
        for trace in fig.data:
            if hasattr(trace, "x") and trace.x is not None:
                years.extend([int(x) for x in trace.x if str(x).isdigit()])
        if years:
            min_year = min(years)
            max_year = max(years)
            for year in sorted(set(years)):
                fig.add_vline(
                    x=year,
                    line_width=0.7,
                    line_dash="dot",
                    line_color="rgba(148,163,184,0.28)",
                    layer="below",
                )
            if min_year <= 2020 <= max_year:
                fig.add_vrect(
                    x0=2020,
                    x1=2022,
                    fillcolor="rgba(239,68,68,0.07)",
                    line_width=0,
                    layer="below",
                )
            if min_year <= 2022 <= max_year:
                fig.add_vrect(
                    x0=2022,
                    x1=max_year,
                    fillcolor="rgba(56,189,248,0.06)",
                    line_width=0,
                    layer="below",
                )
    except Exception:
        pass
    return fig


def get_investment_observation(country_year_df: pd.DataFrame, selected_country: str) -> tuple[str, str]:
    df = country_year_df[country_year_df["country_name"] == selected_country].copy()
    if df.empty or "year" not in df.columns:
        return "Investment data unavailable.", "Use structural evolution and comparison sections instead."

    metric_map = {
        "Education": ["education_spending"],
        "R&D": ["rnd"],
        "Social Protection": ["social_protection_spending"],
        "Environment": ["environment_spending"],
        "Defense": ["defense_spending"],
    }

    changes = []
    df = df.sort_values("year")
    for label, candidates in metric_map.items():
        col = find_column(df, candidates)
        if col is None:
            continue

        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(series) >= 2:
            country_avg = float(series.mean())
            latest = float(series.iloc[-1])
            changes.append((label, latest - country_avg))

    if not changes:
        return "Investment profile is available but too sparse for change detection.", "Review the investment line profile as a trajectory view."

    largest_increase = max(changes, key=lambda item: item[1])
    largest_decrease = min(changes, key=lambda item: item[1])

    observation = f"Largest latest-above-average signal: {largest_increase[0]} ({largest_increase[1]:+.2f})."
    question = f"Does {largest_increase[0]} help explain one of {selected_country}'s strongest structural dimensions?"
    if largest_decrease[1] < 0:
        observation += f" Largest latest-below-average signal: {largest_decrease[0]} ({largest_decrease[1]:+.2f})."

    return observation, question


def render_p1_mission_log(selected_country: str, largest_gain_dimension: str, largest_constraint_dimension: str, comparison_reference_name: str):
    st.html(
        f"""
        <div class="p1-log-panel-v2">
            <div class="p1-log-title">Mission Log</div>

            <div class="p1-log-heading">Current Mission</div>
            <div class="p1-log-text">
                Understand where {selected_country} stands structurally and what questions to investigate next.
            </div>

            <div class="p1-log-heading">Latest Learning</div>
            <div class="p1-log-text">
                Compared with {comparison_reference_name}, the clearest advantage is
                <b>{largest_gain_dimension}</b>, while the main constraint is
                <b>{largest_constraint_dimension}</b>.
            </div>

            <div class="p1-log-heading" style="color:#A3E635;">Suggested Next Step</div>
            <div class="p1-log-text">
                Continue to the Tradeoff Explorer to investigate which relationships may explain this profile.
            </div>
        </div>
        """
    )


def render_journey_table(selected_country: str, largest_gain_dimension: str, largest_constraint_dimension: str):
    """Full-width P3-style journey log table for P1."""
    rows = [
        {
            "step": "01",
            "page": "P1 Country Explorer",
            "country": selected_country,
            "learning": "Current position",
            "finding": f"{selected_country} has a distinct structural profile inside its family context.",
            "next_step": "Read evolution",
        },
        {
            "step": "02A",
            "page": "P1 Country Explorer",
            "country": selected_country,
            "learning": "Structural evolution",
            "finding": "The timeline shows how structural dimensions changed across COVID and energy-transition periods.",
            "next_step": "Read investment profile",
        },
        {
            "step": "02B",
            "page": "P1 Country Explorer",
            "country": selected_country,
            "learning": "Investment profile",
            "finding": "Investment trajectories show which priorities moved above or below the country average.",
            "next_step": "Compare to reference",
        },
        {
            "step": "03",
            "page": "P1 Country Explorer",
            "country": selected_country,
            "learning": "Comparison",
            "finding": f"Largest advantage: {largest_gain_dimension}. Main constraint: {largest_constraint_dimension}.",
            "next_step": "Interpret profile",
        },
        {
            "step": "05",
            "page": "P1 Country Explorer",
            "country": selected_country,
            "learning": "Suggested path",
            "finding": "Investigate tradeoffs, apply strategy, apply shock, adapt strategy, and summarize learning.",
            "next_step": "Open P2",
        },
    ]

    columns = ["step", "page", "country", "learning", "finding", "next_step"]
    headers = "".join(f"<th>{col.replace('_', ' ')}</th>" for col in columns)
    html_rows = []
    for row in rows:
        cells = "".join(f"<td>{row[col]}</td>" for col in columns)
        html_rows.append(f"<tr>{cells}</tr>")

    st.html(
        f"""
        <div style="
            width:100%;
            margin-top:12px;
            border-radius:16px;
            border:1px solid rgba(56,189,248,0.34);
            background:rgba(15,23,42,0.72);
            padding:16px;
            overflow-x:auto;
        ">
            <div style="color:#F8FAFC; font-size:1.08rem; font-weight:900; margin-bottom:6px;">
                Journey Log Table
            </div>
            <div style="color:#CBD5E1; font-size:0.88rem; margin-bottom:14px;">
                Full-width record of the P1 learning path. This becomes input for P2, P3, P4, and P5.
            </div>
            <table style="
                min-width:1250px;
                width:100%;
                border-collapse:collapse;
                table-layout:fixed;
                background:rgba(51,65,85,0.92);
                color:#F8FAFC;
                font-size:0.86rem;
            ">
                <colgroup>
                    <col style="width:7%;">
                    <col style="width:16%;">
                    <col style="width:10%;">
                    <col style="width:16%;">
                    <col style="width:39%;">
                    <col style="width:12%;">
                </colgroup>
                <thead><tr>{headers}</tr></thead>
                <tbody>{''.join(html_rows)}</tbody>
            </table>
        </div>
        <style>
            table th {{
                background:rgba(56,189,248,0.14);
                color:#E0F2FE;
                border:1px solid rgba(148,163,184,0.40);
                padding:10px 9px;
                text-align:left;
                font-size:0.74rem;
                font-weight:900;
                letter-spacing:0.04em;
                text-transform:uppercase;
            }}
            table td {{
                border:1px solid rgba(148,163,184,0.32);
                padding:11px 9px;
                vertical-align:top;
                line-height:1.36;
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
# HEADER / CONTEXT
# =============================================================================

all_countries = sorted(profiles_df["country_name"].unique())
country_options = order_countries(all_countries, PRIORITY_COUNTRIES)

reference_options = [
    "EU Average",
    "Family Average",
    "Another Country",
]

reference_country_options = order_countries(all_countries, PRIORITY_COUNTRIES)

st.html('<div class="p1-sticky-header-marker"></div>')

header_col1, header_col2, header_col3, header_col_ref_country, header_col4 = st.columns(
    [1.8, 1.05, 1.15, 1.15, 0.9],
    gap="medium",
)

with header_col1:
    st.html(
        """
        <div class="p1-brand">
            <div class="p1-logo">✦</div>
            <div>
                <div class="p1-brand-title">EUROPEAN<br>STRATEGY ATLAS</div>
                <div class="p1-brand-subtitle">Explore. Understand.<br>Shape Europe's future.</div>
            </div>
        </div>
        """
    )

with header_col2:
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        index=country_options.index(DEFAULT_COUNTRY) if DEFAULT_COUNTRY in country_options else 0,
    )

with header_col3:
    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        index=reference_options.index(DEFAULT_REFERENCE_TYPE) if DEFAULT_REFERENCE_TYPE in reference_options else 0,
    )

with header_col_ref_country:
    if selected_reference == "Another Country":
        filtered_reference_options = [
            country for country in reference_country_options if country != selected_country
        ]
        default_reference = (
            DEFAULT_REFERENCE_COUNTRY
            if DEFAULT_REFERENCE_COUNTRY in filtered_reference_options
            else filtered_reference_options[0]
        )
        reference_country = st.selectbox(
            "Reference Country",
            options=filtered_reference_options,
            index=filtered_reference_options.index(default_reference),
        )
    else:
        reference_country = None
        st.text_input("Reference Country", value="-----------", disabled=True)

with header_col4:
    view_mode = st.radio(
        "View Mode",
        options=["Relative", "Absolute"],
        horizontal=True,
        index=0,
    )

# Keep P1 selection available to P2-P5.
init_atlas_state()
update_atlas_context(
    country=selected_country,
    reference_type=selected_reference,
    reference_country=reference_country,
    view_mode=view_mode,
    source_page="P1 Country Explorer",
    log_context_change=False,
)


# =============================================================================
# DATA CONTEXT
# =============================================================================

country_profile = load_country_profile(selected_country)
country_story = create_country_story(country_profile)

if selected_reference == "Family Average":
    comparison_profile = build_family_reference_profile(
        country_profile=country_profile,
        profiles_df=profiles_df,
        families_df=families_df,
    )
elif selected_reference == "EU Average":
    comparison_profile = build_eu_reference_profile(
        country_profile=country_profile,
        profiles_df=profiles_df,
    )
else:
    comparison_profile = build_country_reference_profile(
        country_profile=country_profile,
        reference_country_name=reference_country,
        profiles_df=profiles_df,
    )

gap_df = build_dimension_gap_table(comparison_profile)
strengths_df = get_key_strengths(gap_df)
constraints_df = get_key_constraints(gap_df)

largest_gain = strengths_df.iloc[0]
largest_constraint = constraints_df.iloc[0]

largest_gain_dimension = largest_gain["dimension"]
largest_gain_value = largest_gain["gap"]

largest_constraint_dimension = largest_constraint["dimension"]
largest_constraint_value = largest_constraint["gap"]

comparison_reference_name = comparison_profile["reference_name"]

comparison_bottom_line = (
    f"{selected_country} performs relatively better in {largest_gain_dimension}, "
    f"but trails its reference in {largest_constraint_dimension}."
)

country_timeline = build_country_timeline(
    country_name=selected_country,
    country_year_df=country_year_df,
)

eu_reference_profile = build_eu_reference_profile(
    country_profile=country_profile,
    profiles_df=profiles_df,
)
eu_gap_df = build_dimension_gap_table(eu_reference_profile)


# =============================================================================
# VERSION + INTRO
# =============================================================================

st.html('<div class="p1-version-badge">P1 VERSION v07_TABLE_FLOW_CHART_LOG_FIX</div>')

st.html(
    f"""
    <div class="p1-intro-box">
        <div class="p1-intro-title">How to use this page</div>
        <div class="p1-intro-text">
            Start by locating {selected_country} structurally, then follow its evolution,
            investment profile, and comparison against your selected reference.
            This page builds the mental model needed before investigating tradeoffs or testing strategies.
        </div>
    </div>
    """
)


# =============================================================================
# SNAPSHOT RIBBON
# =============================================================================
# Hidden for graduation MVP: demographic/economic snapshot data is not included in the validated app dataset.


# =============================================================================
# KPI RIBBON
# =============================================================================

innovation_score = country_profile["dimensions"].get("Innovation Capacity", 0)
sustainability_score = country_profile["dimensions"].get("Sustainability Capacity", 0)
fiscal_score = country_profile["dimensions"].get("Fiscal Flexibility", 0)
security_score = country_profile["dimensions"].get("Security Reprioritization", 0)

innovation_color = get_delta_color(innovation_score)
sustainability_color = get_delta_color(sustainability_score)
fiscal_color = get_delta_color(fiscal_score)
security_color = get_delta_color(security_score)

st.html(
    f"""
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">ARCHETYPE</div>
            <div class="p1-kpi-main">{country_profile['archetype']}</div>
            <div class="p1-kpi-sub">Structural identity</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:{innovation_color};">INNOVATION CAPACITY</div>
            <div class="p1-kpi-number" style="color:{innovation_color};">{innovation_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:{sustainability_color};">SUSTAINABILITY</div>
            <div class="p1-kpi-number" style="color:{sustainability_color};">{sustainability_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:{fiscal_color};">FISCAL FLEXIBILITY</div>
            <div class="p1-kpi-number" style="color:{fiscal_color};">{fiscal_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:{security_color};">SECURITY</div>
            <div class="p1-kpi-number" style="color:{security_color};">{security_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">FAMILY</div>
            <div class="p1-kpi-main">{country_profile['family']}</div>
            <div class="p1-kpi-sub">Structural pathway</div>
        </div>
    </div>
    """
)


# =============================================================================
# PAGE FRAME
# =============================================================================

left_nav_col, main_col, right_log_col = st.columns(
    [0.85, 5.4, 1.15],
    gap="medium",
)

with left_nav_col:
    st.html(
        f"""
        <div class="p1-left-nav-test">
            <div class="p1-nav-label">YOUR JOURNEY<br>ON PAGE 1</div>

            <div class="p1-nav-item active">
                <div class="p1-nav-number">01</div>
                <div>
                    <div class="p1-nav-title">WHERE IS {selected_country.upper()}?</div>
                    <div class="p1-nav-sub">Structural position today.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">02</div>
                <div>
                    <div class="p1-nav-title">EVOLUTION</div>
                    <div class="p1-nav-sub">Structural + investment pathway.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">03</div>
                <div>
                    <div class="p1-nav-title">COMPARE</div>
                    <div class="p1-nav-sub">Reference and EU context.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">04</div>
                <div>
                    <div class="p1-nav-title">MEANING</div>
                    <div class="p1-nav-sub">Interpret profile.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">05</div>
                <div>
                    <div class="p1-nav-title">NEXT</div>
                    <div class="p1-nav-sub">Continue learning journey.</div>
                </div>
            </div>
        </div>
        """
    )


with main_col:

    # =========================================================================
    # SECTION 01 — WHERE IS COUNTRY TODAY?
    # =========================================================================

    render_section_title(
        number="01",
        title=f"Where is {selected_country} today?",
        subtitle="Start with structural position, family context, strongest capabilities, and main constraints.",
    )

    identity_cols = st.columns(3, gap="medium")
    with identity_cols[0]:
        render_guided_card(
            label="Structural Family",
            value=country_profile["family"],
            text="Family context helps interpret the country as part of a broader European pathway.",
            accent="#38BDF8",
        )
    with identity_cols[1]:
        render_guided_card(
            label="Strongest Capability",
            value=country_profile["strongest_dimension"],
            text=f"Current strongest EU-relative signal: {country_profile['strongest_value']:+.2f}.",
            accent="#4ADE80",
        )
    with identity_cols[2]:
        render_guided_card(
            label="Main Constraint",
            value=country_profile["weakest_dimension"],
            text=f"Current weakest EU-relative signal: {country_profile['weakest_value']:+.2f}.",
            accent="#F472B6",
        )

    render_subsection_title("Structural Snapshot")

    section_left, section_center, section_right = st.columns([1.15, 2.0, 1.15], gap="medium")

    with section_left:
        st.markdown("**Key strengths**")
        for _, row in strengths_df.head(2).iterrows():
            render_gap_html_card(
                title=row["dimension"],
                value=f"▲ Δ {row['gap']:+.2f}",
                delta_text=row.get("gap_label", "Advantage"),
                status="Compared with selected reference.",
                delta_color=get_delta_color(row["gap"]),
                card_class="atlas-gap-card atlas-s04-strength atlas-s01-compact",
            )

        render_gap_html_card(
            title="About this archetype",
            value=country_profile["archetype"],
            delta_text="Representative structural pathway.",
            status="Use evolution to understand whether this profile is stable or changing.",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top atlas-s01-info-compact",
        )

    with section_center:
        reference_profile_for_radar = None
        reference_country_for_radar = None
        if selected_reference == "Another Country" and reference_country:
            reference_profile_for_radar = load_country_profile(reference_country)
            reference_country_for_radar = reference_country

        radar_chart = create_p1_reference_radar_chart(
            country_profile=country_profile,
            selected_country=selected_country,
            reference_profile=reference_profile_for_radar,
            reference_country=reference_country_for_radar,
        )
        st.plotly_chart(
            radar_chart,
            use_container_width=True,
            key="p1_structural_radar_final",
            config={"displayModeBar": False},
        )

    with section_right:
        st.markdown("**Key constraints**")
        for _, row in constraints_df.head(2).iterrows():
            render_gap_html_card(
                title=row["dimension"],
                value=f"▼ Δ {row['gap']:+.2f}",
                delta_text=row.get("gap_label", "Constraint"),
                status="Compared with selected reference.",
                delta_color=get_delta_color(row["gap"]),
                card_class="atlas-gap-card atlas-s04-constraint atlas-s01-compact",
            )

        render_gap_html_card(
            title="Family context",
            value=country_profile["family"],
            delta_text="Shared investment patterns and structural tensions.",
            status="Families become important in P2 and P3.",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top atlas-s01-info-compact",
        )

    render_observation_box(
        title="Next observation",
        text=f"Now trace how {selected_country}'s structure and investment profile evolved over time.",
        accent="#38BDF8",
    )

    # =========================================================================
    # SECTION 02A — STRUCTURAL EVOLUTION
    # =========================================================================

    render_section_title(
        number="02A",
        title=f"How did {selected_country} become this way? — Structural Evolution",
        subtitle="Trace structural capacities relative to the EU average over time.",
    )

    evolution_chart_col, evolution_text_col = st.columns([2.25, 1], gap="medium")

    with evolution_chart_col:
        timeline_chart = create_country_timeline_chart(country_timeline, selected_country)
        timeline_chart = align_timeline_chart_style(timeline_chart, selected_country)
        st.plotly_chart(timeline_chart, use_container_width=True)

    with evolution_text_col:
        render_observation_box(
            title="How to read this",
            text=(
                "Scores are EU-relative structural indices. "
                "Zero indicates the EU average baseline; positive values indicate above-average structural position."
            ),
            accent="#38BDF8",
        )
        render_observation_box(
            title="Investigation question",
            text=(
                f"What changed after 2020? Use the timeline to see whether {selected_country}'s "
                "profile is stable, shifting, or volatile."
            ),
            accent="#A3E635",
        )

    # =========================================================================
    # SECTION 02B — INVESTMENT PROFILE
    # =========================================================================

    render_section_title(
        number="02B",
        title=f"How did {selected_country} become this way? — Investment Profile",
        subtitle="Explore investment trajectories behind the structural profile. Vertical year lines help compare each priority over time.",
    )

    inv_chart_col, inv_text_col = st.columns([2.25, 1], gap="medium")

    with inv_chart_col:
        investment_chart = create_investment_profile_chart(
            country_year_df=country_year_df,
            selected_country=selected_country,
            view_mode=view_mode,
        )
        st.plotly_chart(investment_chart, use_container_width=True)

    with inv_text_col:
        inv_observation, inv_question = get_investment_observation(country_year_df, selected_country)
        render_observation_box(
            title="What changed?",
            text=inv_observation,
            accent="#38BDF8",
        )
        render_observation_box(
            title="Guiding question",
            text=inv_question,
            accent="#A3E635",
        )
        render_observation_box(
            title="Why this matters",
            text=(
                "This connects P1 to the rest of the Atlas: investments become inputs, "
                "structural dimensions become outputs, and P3/P4 test changes to those priorities."
            ),
            accent="#F59E0B",
        )

    # =========================================================================
    # SECTION 03 — COMPARISON
    # =========================================================================

    render_section_title(
        number="03",
        title=f"How does {selected_country} compare?",
        subtitle="Compare against the selected reference while keeping the European baseline in the same table.",
    )

    summary_col1, summary_col2, summary_col3 = st.columns([0.9, 1.15, 1.15], gap="medium")

    with summary_col1:
        render_gap_html_card(
            title="Compared With",
            value=comparison_reference_name,
            delta_text="Selected reference",
            status=f"View mode: {view_mode}",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    with summary_col2:
        render_gap_html_card(
            title="Largest Advantage",
            value=largest_gain_dimension,
            delta_text=f"▲ Δ {largest_gain_value:+.2f}",
            status="Strongest relative gap.",
            delta_color=get_delta_color(largest_gain_value),
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    with summary_col3:
        render_gap_html_card(
            title="Largest Constraint",
            value=largest_constraint_dimension,
            delta_text=f"▼ Δ {largest_constraint_value:+.2f}",
            status="Largest relative pressure.",
            delta_color=get_delta_color(largest_constraint_value),
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    render_comparison_table(
        gap_df=gap_df,
        eu_gap_df=eu_gap_df,
        country_label=selected_country,
        reference_label=comparison_reference_name,
        view_mode=view_mode,
    )

    question_cols = st.columns(3, gap="medium")
    with question_cols[0]:
        render_observation_box(
            title="Guiding question 1",
            text=f"Which dimensions make {selected_country} most different from the EU baseline?",
            accent="#38BDF8",
        )
    with question_cols[1]:
        render_observation_box(
            title="Guiding question 2",
            text=f"Where does the selected reference ({comparison_reference_name}) change the story?",
            accent="#A3E635",
        )
    with question_cols[2]:
        render_observation_box(
            title="Guiding question 3",
            text="Which dimensions look similar, and which suggest a real structural specialization?",
            accent="#F59E0B",
        )

    render_observation_box(
        title="Learning insight",
        text=comparison_bottom_line,
        accent="#38BDF8",
    )

    # SECTION 04 — INTERPRETATION
    # =========================================================================

    render_section_title(
        number="04",
        title="What does this profile mean?",
        subtitle="Translate the comparison into strengths, limits, and a next investigation question.",
    )

    interp_cols = st.columns(3, gap="medium")

    with interp_cols[0]:
        render_guided_card(
            label="What helps?",
            value=largest_gain_dimension,
            text=f"This is the clearest advantage against {comparison_reference_name}.",
            accent="#4ADE80",
        )

    with interp_cols[1]:
        render_guided_card(
            label="What limits?",
            value=largest_constraint_dimension,
            text=f"This is the largest constraint against {comparison_reference_name}.",
            accent="#F472B6",
        )

    with interp_cols[2]:
        render_guided_card(
            label="Strategic interpretation",
            value="Uneven profile",
            text=(
                f"{selected_country} is not summarized by one score. "
                "It combines capabilities and constraints that create tradeoffs."
            ),
            accent="#38BDF8",
        )

    render_observation_box(
        title="Learning insight",
        text=(
            f"Observation: {selected_country}'s strongest relative advantage is {largest_gain_dimension}. "
            f"Interpretation: the profile is structurally uneven. "
            f"Question: which relationships explain why {largest_gain_dimension} is stronger than {largest_constraint_dimension}?"
        ),
        accent="#A855F7",
    )

    # =========================================================================

with right_log_col:
    render_p1_mission_log(
        selected_country=selected_country,
        largest_gain_dimension=largest_gain_dimension,
        largest_constraint_dimension=largest_constraint_dimension,
        comparison_reference_name=comparison_reference_name,
    )


# =============================================================================
# FULL-WIDTH CONTINUE + JOURNEY LOG
# =============================================================================

st.html("<div class='p3-full-width-shell'>")

render_section_title(
    number="05",
    title="What would you like to explore next?",
    subtitle="Continue from structural understanding toward tradeoffs, strategy, or comparison.",
)

render_observation_box(
    title="Suggested learning path",
    text=(
        f"You selected {selected_country} and {comparison_reference_name}. "
        "Suggested path: investigate tradeoffs → apply strategy → apply shock → adapt strategy → summarize learning."
    ),
    accent="#A3E635",
)

cta_tradeoff, cta_strategy, cta_compare, cta_reflect = st.columns(4, gap="medium")

with cta_tradeoff:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-navigation" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Next Page</div>
                <div style="color:#38BDF8; font-size:1.12rem; font-weight:900; margin:8px 0;">Tradeoff Explorer</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Investigate relationships behind the profile.</div>
            </div>
            """
        )
        if st.button("Open Tradeoff Explorer", key="p1_cta_tradeoff_full", use_container_width=True):
            safe_switch_page("pages/p2_tradeoff_explorer.py")

with cta_strategy:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-challenge" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Strategy</div>
                <div style="color:#F59E0B; font-size:1.12rem; font-weight:900; margin:8px 0;">Build a Strategy</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Experiment with investment priorities.</div>
            </div>
            """
        )
        if st.button("Open Strategy Choices", key="p1_cta_strategy_full", use_container_width=True):
            safe_switch_page("pages/p3_strategic_choices.py")

with cta_compare:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-compare" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Compare</div>
                <div style="color:#22D3EE; font-size:1.12rem; font-weight:900; margin:8px 0;">Compare Countries</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Use the reference selector above to compare another pathway.</div>
            </div>
            """
        )
        st.button("Use Reference Selector", key="p1_cta_compare_full", use_container_width=True)

with cta_reflect:
    with st.container(border=True):
        st.html(
            """
            <div class="atlas-cta-reflect" style="min-height:132px; padding:14px 16px;">
                <div style="color:#94A3B8; font-size:0.72rem; font-weight:900; letter-spacing:0.10em; text-transform:uppercase;">Reflect</div>
                <div style="color:#A855F7; font-size:1.12rem; font-weight:900; margin:8px 0;">Learning Summary</div>
                <div style="color:#CBD5E1; font-size:0.84rem; line-height:1.35;">Save the profile as a learning record for P5.</div>
            </div>
            """
        )
        st.button("Save Learning", key="p1_cta_save_learning", use_container_width=True, disabled=True)

st.markdown("---")
render_journey_table(
    selected_country=selected_country,
    largest_gain_dimension=largest_gain_dimension,
    largest_constraint_dimension=largest_constraint_dimension,
)

st.markdown("<br>", unsafe_allow_html=True)
footer_left, footer_right = st.columns([1.1, 0.9], gap="medium")

with footer_left:
    st.markdown(
        """
### European Strategy Atlas — MVP v0.1

Created by Gilad Gotesman.

Educational exploration of European structural pathways, strategic tradeoffs, and transformation patterns using public European data.
"""
    )

with footer_right:
    st.markdown("### Key assumptions & constraints")
    assump_col1, assump_col2 = st.columns([3, 2])
    with assump_col1:
        st.markdown(
            """
- Exploratory, not predictive.
- No causality claims.
- Composite indicators.
"""
        )
    with assump_col2:
        st.markdown(
            """
- Strategic lenses, not rankings.
- Not policy recommendations.
"""
        )

st.html("</div>")
