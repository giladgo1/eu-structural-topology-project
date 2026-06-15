"""
p2_tradeoff_explorer.py

Purpose
-------
Page 2 of the EUROPEAN STRATEGY ATLAS.

This page answers:

"What tradeoffs shape this country?"

Current development stage
-------------------------
P2 skeleton only.

Goal:
- reuse the validated P9 shared Atlas frame
- test page structure before data/charts
- avoid new CSS/layout systems
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.typography import render_section_title
from components.cards import (
    render_atlas_card,
    render_hero_card,
    render_delta_card,
)
from components.page_frame import (
    render_left_rail_placeholder,
    render_mission_log_placeholder,
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
    css_file = (
        Path(__file__)
        .parent.parent
        / "styles"
        / "atlas_theme.css"
    )

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()


# =============================================================================
# SMALL NAVIGATION HELPER
# =============================================================================

def safe_switch_page(page_path: str):
    """Try Streamlit page navigation without breaking the current version if a page path differs."""
    try:
        st.switch_page(page_path)
    except Exception:
        st.info(f"Navigation target not found yet: {page_path}")


# =============================================================================
# DATA LOADING
# =============================================================================

APP_DATA_DIR = (
    Path(__file__)
    .parent.parent.parent
    / "data"
    / "app"
)


@st.cache_data
def load_p2_tradeoff_data():
    dimension_profiles = pd.read_csv(
        APP_DATA_DIR / "country_dimension_profiles.csv"
    )

    family_metadata = pd.read_csv(
        APP_DATA_DIR / "structural_family_metadata.csv"
    )

    tradeoff_df = dimension_profiles.merge(
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

    return tradeoff_df


tradeoff_df = load_p2_tradeoff_data()


# =============================================================================
# SHARED ATLAS MEMORY HELPERS
# =============================================================================

DEFAULT_COUNTRY = "Germany"
DEFAULT_REFERENCE_TYPE = "EU Average"
DEFAULT_REFERENCE_COUNTRY = "Germany"
DEFAULT_VIEW_MODE = "Relative"

init_atlas_state(
    default_country=DEFAULT_COUNTRY,
    default_reference=DEFAULT_REFERENCE_TYPE,
    default_reference_country=DEFAULT_REFERENCE_COUNTRY,
    default_view_mode=DEFAULT_VIEW_MODE,
)


def _valid_or_default(value, options, fallback):
    if value in options:
        return value
    if fallback in options:
        return fallback
    return options[0] if options else fallback


def initialize_p2_from_atlas_state(country_options, reference_options, view_options):
    """Initialize P2 controls from the shared Atlas journey state.

    P1 writes the selected country/reference into atlas_* keys before navigation.
    P2 must read those keys before rendering widgets; otherwise the app resets to
    Germany / EU Average and breaks the learning journey.
    """
    atlas_country = _valid_or_default(
        st.session_state.get("atlas_country", st.session_state.get("selected_country", DEFAULT_COUNTRY)),
        country_options,
        DEFAULT_COUNTRY,
    )
    atlas_reference = _valid_or_default(
        st.session_state.get("atlas_reference_type", st.session_state.get("selected_reference", DEFAULT_REFERENCE_TYPE)),
        reference_options,
        DEFAULT_REFERENCE_TYPE,
    )
    atlas_reference_country = _valid_or_default(
        st.session_state.get("atlas_reference_country", st.session_state.get("reference_country", DEFAULT_REFERENCE_COUNTRY)),
        country_options,
        DEFAULT_REFERENCE_COUNTRY,
    )
    atlas_view_mode = _valid_or_default(
        st.session_state.get("atlas_view_mode", st.session_state.get("view_mode", DEFAULT_VIEW_MODE)),
        view_options,
        DEFAULT_VIEW_MODE,
    )

    atlas_tuple = (atlas_country, atlas_reference, atlas_reference_country, atlas_view_mode)

    if st.session_state.get("p2_last_synced_atlas_tuple") != atlas_tuple:
        st.session_state["p2_selected_country"] = atlas_country
        st.session_state["p2_selected_reference"] = atlas_reference
        st.session_state["p2_reference_country"] = atlas_reference_country
        st.session_state["p2_view_mode"] = atlas_view_mode
        st.session_state["p2_last_synced_atlas_tuple"] = atlas_tuple


def sync_p2_to_atlas_state(log_context_change: bool = True):
    """Persist current P2 controls back into the shared Atlas journey state."""
    selected_country = st.session_state.get("p2_selected_country", DEFAULT_COUNTRY)
    selected_reference = st.session_state.get("p2_selected_reference", DEFAULT_REFERENCE_TYPE)
    reference_country = st.session_state.get("p2_reference_country", DEFAULT_REFERENCE_COUNTRY)
    view_mode = st.session_state.get("p2_view_mode", DEFAULT_VIEW_MODE)

    update_atlas_context(
        country=selected_country,
        reference_type=selected_reference,
        reference_country=reference_country,
        view_mode=view_mode,
        source_page="P2 Tradeoff Explorer",
        log_context_change=log_context_change,
    )
    st.session_state["p2_last_synced_atlas_tuple"] = (
        selected_country,
        selected_reference,
        reference_country,
        view_mode,
    )


# =============================================================================
# P2 TRADEOFF REGISTRY
# =============================================================================

DIMENSION_REGISTRY = {
    "Human Capital": "dim_human_capital_capacity",
    "Innovation": "dim_innovation_capacity",
    "Sustainability": "dim_sustainability_capacity",
    "Social Stability": "dim_social_stability",
    "Fiscal Flexibility": "dim_fiscal_flexibility",
    "Security": "dim_security_reprioritization",
    "Adaptive Transformation": "dim_adaptive_transformation",
}

CURATED_TRADEOFFS = {
    "Innovation ↔ Fiscal Flexibility": {
        "x_col": "dim_fiscal_flexibility",
        "y_col": "dim_innovation_capacity",
        "x_label": "Fiscal Flexibility",
        "y_label": "Innovation Capacity",
        "question": "Do countries that innovate more have more or less fiscal flexibility?",
        "evidence": "A",
        "confidence": "High",
    },
    "Sustainability ↔ Fiscal Flexibility": {
        "x_col": "dim_sustainability_capacity",
        "y_col": "dim_fiscal_flexibility",
        "x_label": "Sustainability Capacity",
        "y_label": "Fiscal Flexibility",
        "question": "Can sustainability capacity coexist with fiscal flexibility?",
        "evidence": "B",
        "confidence": "Medium",
    },
    "Innovation ↔ Social Stability": {
        "x_col": "dim_innovation_capacity",
        "y_col": "dim_social_stability",
        "x_label": "Innovation Capacity",
        "y_label": "Social Stability",
        "question": "Do more innovative countries also show stronger social stability?",
        "evidence": "B",
        "confidence": "Medium",
    },
    "Security ↔ Sustainability": {
        "x_col": "dim_security_reprioritization",
        "y_col": "dim_sustainability_capacity",
        "x_label": "Security Reprioritization",
        "y_label": "Sustainability Capacity",
        "question": "Do countries that reprioritize security also sustain green transition capacity?",
        "evidence": "C",
        "confidence": "Exploratory",
    },
    "Adaptive Transformation ↔ Fiscal Flexibility": {
        "x_col": "dim_adaptive_transformation",
        "y_col": "dim_fiscal_flexibility",
        "x_label": "Adaptive Transformation",
        "y_label": "Fiscal Flexibility",
        "question": "Does adaptive transformation depend on fiscal flexibility?",
        "evidence": "B",
        "confidence": "Medium",
    },
}


def build_all_tradeoff_registry():
    registry = dict(CURATED_TRADEOFFS)

    for left_name, right_name in combinations(DIMENSION_REGISTRY.keys(), 2):
        label = f"{left_name} ↔ {right_name}"

        if label in registry:
            continue

        registry[label] = {
            "x_col": DIMENSION_REGISTRY[left_name],
            "y_col": DIMENSION_REGISTRY[right_name],
            "x_label": left_name,
            "y_label": right_name,
            "question": f"How do {left_name.lower()} and {right_name.lower()} relate across European systems?",
            "evidence": "C",
            "confidence": "Exploratory",
        }

    return registry


TRADEOFF_REGISTRY = build_all_tradeoff_registry()

CURATED_TRADEOFF_NAMES = list(CURATED_TRADEOFFS.keys())

ADVANCED_TRADEOFF_NAMES = [
    name
    for name in TRADEOFF_REGISTRY.keys()
    if name not in CURATED_TRADEOFF_NAMES
]


FAMILY_COLORS = {
    "Innovation-Core Systems": "#38BDF8",
    "Industrial / Transition Systems": "#8B5CF6",
    "Adaptive / Peripheral Systems": "#F59E0B",
    "Other / Transitional": "#64748B",
}


EVIDENCE_COLORS = {
    "A": "#22C55E",
    "B": "#EAB308",
    "C": "#F97316",
    "D": "#EF4444",
}


def describe_correlation(correlation: float) -> tuple[str, str]:
    if pd.isna(correlation):
        return "No visible pattern", "Pattern unavailable"

    direction = "Positive" if correlation > 0 else "Negative"

    abs_corr = abs(correlation)

    if abs_corr >= 0.65:
        strength = "Strong"
    elif abs_corr >= 0.35:
        strength = "Moderate"
    elif abs_corr >= 0.15:
        strength = "Weak"
    else:
        strength = "Very weak"

    return f"{strength} {direction}", f"{'↗' if correlation > 0 else '↘'} {strength} {direction}"


def render_p2_info_card(title: str, value: str, body: str, accent: str = "#38BDF8"):
    st.html(
        f"""
        <div style="
            padding: 14px 15px 13px 15px;
            border-radius: 18px;
            border: 1px solid rgba(148,163,184,0.22);
            border-left: 5px solid {accent};
            background: linear-gradient(145deg, rgba(15,23,42,0.94), rgba(15,23,42,0.72));
            margin-bottom: 14px;
            box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        ">
            <div style="
                color: {accent};
                font-size: 0.76rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                margin-bottom: 8px;
            ">{title}</div>

            <div style="
                color: #F8FAFC;
                font-size: 1.18rem;
                font-weight: 900;
                margin-bottom: 8px;
            ">{value}</div>

            <div style="
                color: #CBD5E1;
                font-size: 0.96rem;
                line-height: 1.42;
            ">{body}</div>
        </div>
        """
    )


def get_pattern_strength(correlation: float) -> str:
    """Convert correlation magnitude into a readable evidence label."""
    if pd.isna(correlation):
        return "Unavailable"

    abs_corr = abs(correlation)

    if abs_corr >= 0.65:
        return "Strong"
    if abs_corr >= 0.35:
        return "Moderate"
    if abs_corr >= 0.15:
        return "Weak"
    return "Very Weak"


def get_pattern_direction(correlation: float) -> str:
    """Convert correlation sign into a readable direction label."""
    if pd.isna(correlation):
        return "Unavailable"
    return "Positive" if correlation >= 0 else "Negative"


def get_direction_arrow(correlation: float) -> str:
    """Visual arrow for the main pattern card.

    Weak / very weak relationships use a horizontal arrow in the card only.
    The graph still shows trendlines only when abs(r) >= 0.60.
    """
    if pd.isna(correlation):
        return "→"

    if abs(correlation) < 0.35:
        return "→"

    return "↗" if correlation >= 0 else "↘"


def add_fit_line(
    fig,
    x_values,
    y_values,
    color: str,
    name: str,
    dash: str = "dash",
    width: float = 0.65,
):
    """Add a fitted thin dashed trend line only after evidence gating."""
    clean = pd.DataFrame({"x": x_values, "y": y_values}).dropna()

    if len(clean) < 3:
        return

    slope, intercept = np.polyfit(clean["x"].astype(float), clean["y"].astype(float), 1)

    x_min = clean["x"].min()
    x_max = clean["x"].max()

    line_x = np.array([x_min, x_max])
    line_y = slope * line_x + intercept

    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            name=name,
            line=dict(color=color, width=width, dash=dash),
            hovertemplate=f"<b>{name}</b><extra></extra>",
            showlegend=True,
        )
    )

    # Add an arrowhead at the trend direction endpoint.
    fig.add_annotation(
        x=float(line_x[-1]),
        y=float(line_y[-1]),
        ax=float(line_x[-2]),
        ay=float(line_y[-2]),
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",
        showarrow=True,
        arrowhead=5,
        arrowsize=1.8,
        arrowwidth=1.4,
        arrowcolor=color,
        opacity=0.85,
    )


def render_pattern_summary_card(
    pattern_strength: str,
    direction: str,
    correlation: float,
    sample_size: int,
    pattern_comment: str,
):
    """Compact right-side card replacing the duplicated graph annotation."""
    arrow = get_direction_arrow(correlation)

    st.html(
        f"""
        <div style="
            border: 1px solid rgba(56,189,248,0.46);
            border-radius: 18px;
            padding: 14px 15px 13px 15px;
            background:
                linear-gradient(135deg, rgba(30,58,95,0.78), rgba(15,23,42,0.86));
            margin-bottom: 12px;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position:absolute;
                right:16px;
                top:22px;
                color:#38BDF8;
                font-size:2.6rem;
                font-weight:900;
                opacity:0.35;
                line-height:1;
            ">{arrow}</div>

            <div style="
                color:#F8FAFC;
                font-size:0.78rem;
                font-weight:900;
                text-transform:uppercase;
                letter-spacing:0.08em;
                margin-bottom:8px;
            ">Pattern First</div>

            <div style="
                color:#F8FAFC;
                font-size:1.08rem;
                font-weight:900;
                line-height:1.2;
                margin-bottom:10px;
                padding-right:56px;
            ">{pattern_strength} {direction}</div>

            <div style="
                color:#38BDF8;
                font-size:0.95rem;
                font-weight:850;
                margin-bottom:8px;
            ">Correlation r = {correlation:.2f} · n = {sample_size}</div>

            <div style="
                color:#E2E8F0;
                font-size:0.9rem;
                line-height:1.45;
                font-weight:650;
            ">
                {pattern_comment}
                <br><span style="color:#CBD5E1; font-weight:500;">Do not infer causality.</span>
            </div>
        </div>
        """
    )


def render_guided_questions(title: str, questions: list[str], accent: str = "#38BDF8"):
    """Reusable compact guided-question block for P2 and later pages."""
    question_items = "".join(
        [
            f"""
            <div style="
                display:flex;
                gap:8px;
                align-items:flex-start;
                color:#E2E8F0;
                font-size:0.88rem;
                line-height:1.35;
                margin-bottom:6px;
            ">
                <span style="color:{accent}; font-weight:900;">?</span>
                <span>{question}</span>
            </div>
            """
            for question in questions
        ]
    )

    st.html(
        f"""
        <div style="
            border:1px solid rgba(148,163,184,0.22);
            border-left:4px solid {accent};
            border-radius:14px;
            padding:12px 14px;
            background:rgba(15,23,42,0.74);
            margin:8px 0 14px 0;
        ">
            <div style="
                color:{accent};
                font-size:0.72rem;
                font-weight:900;
                letter-spacing:0.1em;
                text-transform:uppercase;
                margin-bottom:8px;
            ">{title}</div>
            {question_items}
        </div>
        """
    )


def render_page_intro():
    """Short reusable page instruction block."""
    st.html(
        """
        <div style="
            border:1px solid rgba(56,189,248,0.30);
            border-radius:16px;
            padding:14px 18px;
            background:
                linear-gradient(135deg, rgba(15,23,42,0.92), rgba(15,23,42,0.68));
            margin: 2px 0 16px 0;
        ">
            <div style="
                color:#38BDF8;
                font-size:0.72rem;
                font-weight:900;
                letter-spacing:0.12em;
                text-transform:uppercase;
                margin-bottom:6px;
            ">How to use this page</div>
            <div style="color:#E2E8F0; font-size:1.08rem; line-height:1.55; font-weight:600;">
                This page helps you investigate structural tradeoffs across European countries.
                Start by choosing one investigation question. First observe the pattern,
                then check whether structural families explain it, and finally inspect exceptions.
                Use the chart to ask better questions — not as a recommendation.
            </div>
        </div>
        """
    )


def render_compact_lens_block(
    question_title: str,
    questions: list[str],
    lens_title: str,
    lens_value: str,
    lens_body: str,
    next_step: str,
    accent: str = "#38BDF8",
):
    """Compact symmetric horizontal lens block: questions left, lens/answer right."""
    question_items = "".join(
        [
            f"""
            <div style="display:flex; gap:8px; align-items:flex-start; margin-bottom:3px;">
                <span style="color:{accent}; font-weight:900;">?</span>
                <span>{question}</span>
            </div>
            """
            for question in questions
        ]
    )

    st.html(
        f"""
        <div style="
            display:grid;
            grid-template-columns: 1fr 1fr;
            gap:0;
            align-items:stretch;
            border:1px solid rgba(148,163,184,0.24);
            border-radius:15px;
            background:rgba(15,23,42,0.74);
            margin:8px 0 12px 0;
            overflow:hidden;
        ">
            <div style="
                border-left:5px solid {accent};
                padding:10px 14px;
                color:#E2E8F0;
                font-size:0.86rem;
                line-height:1.28;
                min-height:92px;
            ">
                <div style="
                    color:{accent};
                    font-size:0.70rem;
                    font-weight:900;
                    letter-spacing:0.10em;
                    text-transform:uppercase;
                    margin-bottom:6px;
                ">{question_title}</div>
                {question_items}
            </div>

            <div style="
                border-left:1px solid rgba(148,163,184,0.20);
                padding:10px 14px;
                color:#E2E8F0;
                font-size:0.86rem;
                line-height:1.28;
                min-height:92px;
            ">
                <div style="
                    color:{accent};
                    font-size:0.70rem;
                    font-weight:900;
                    letter-spacing:0.10em;
                    text-transform:uppercase;
                    margin-bottom:6px;
                ">{lens_title}</div>
                <span style="color:#F8FAFC; font-weight:900;">{lens_value}</span>
                <span style="color:#CBD5E1;"> — {lens_body}</span>
                <div style="color:{accent}; font-weight:900; margin-top:5px;">{next_step}</div>
            </div>
        </div>
        """
    )

def make_tradeoff_scatter(df, selected_country, tradeoff_config, correlation=None, reference_country=None):
    x_col = tradeoff_config["x_col"]
    y_col = tradeoff_config["y_col"]
    x_label = tradeoff_config["x_label"]
    y_label = tradeoff_config["y_label"]

    plot_df = df.dropna(subset=[x_col, y_col]).copy()

    fig = go.Figure()

    for family_name, family_df in plot_df.groupby("structural_family"):
        fig.add_trace(
            go.Scatter(
                x=family_df[x_col],
                y=family_df[y_col],
                mode="markers",
                name=family_name,
                marker=dict(
                    size=13,
                    color=FAMILY_COLORS.get(family_name, "#94A3B8"),
                    opacity=0.78,
                    line=dict(width=1, color="rgba(248,250,252,0.42)"),
                ),
                text=family_df["country_name"],
                customdata=np.stack(
                    [
                        family_df["country"],
                        family_df["structural_subfamily"].fillna(""),
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Code: %{customdata[0]}<br>"
                    "Subfamily: %{customdata[1]}<br>"
                    f"{x_label}: " + "%{x:.2f}<br>"
                    f"{y_label}: " + "%{y:.2f}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    # Trendline hierarchy:
    # 1. Strong overall trend wins.
    # 2. If overall is weak, show only strong family-specific trends.
    # 3. If no strong trend exists, show no trendline.
    show_overall_trend = correlation is not None and not pd.isna(correlation) and abs(correlation) >= 0.60

    if show_overall_trend:
        add_fit_line(
            fig=fig,
            x_values=plot_df[x_col],
            y_values=plot_df[y_col],
            color="#2563EB",
            name="EU-wide trend",
            dash="dash",
            width=0.65,
        )
    else:
        for family_name, family_df in plot_df.groupby("structural_family"):
            if len(family_df) < 3:
                continue

            family_r = family_df[x_col].corr(family_df[y_col])

            if pd.notna(family_r) and abs(family_r) >= 0.60:
                add_fit_line(
                    fig=fig,
                    x_values=family_df[x_col],
                    y_values=family_df[y_col],
                    color=FAMILY_COLORS.get(family_name, "#94A3B8"),
                    name=f"{family_name} trend",
                    dash="dash",
                    width=0.65,
                )

    selected_df = plot_df[plot_df["country_name"] == selected_country]
    reference_df = pd.DataFrame()
    if reference_country and reference_country != selected_country:
        reference_df = plot_df[plot_df["country_name"] == reference_country]

    # If the user selected "Another Country" as reference, show it on the same
    # tradeoff map as a smaller diamond. The main selected country remains the
    # large star. This keeps P2 aligned with the P1 comparison context without
    # adding a new analysis layer.
    if not reference_df.empty:
        reference_family_name = reference_df.iloc[0].get("structural_family", None)
        reference_family_color = FAMILY_COLORS.get(reference_family_name, "#94A3B8")
        fig.add_trace(
            go.Scatter(
                x=reference_df[x_col],
                y=reference_df[y_col],
                mode="markers+text",
                name=f"{reference_country} reference",
                marker=dict(
                    size=18,
                    color=reference_family_color,
                    symbol="diamond",
                    opacity=0.95,
                    line=dict(width=2.2, color="#F8FAFC"),
                ),
                text=[f"{reference_country}"],
                textposition="bottom center",
                textfont=dict(color="#CBD5E1", size=13),
                hovertemplate=(
                    "<b>%{text}</b><br>Reference country<br>"
                    f"{x_label}: " + "%{x:.2f}<br>"
                    f"{y_label}: " + "%{y:.2f}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    selected_family_color = "#EAB308"
    if not selected_df.empty:
        selected_family_name = selected_df.iloc[0].get("structural_family", None)
        selected_family_color = FAMILY_COLORS.get(selected_family_name, "#EAB308")

    if not selected_df.empty:
        fig.add_trace(
            go.Scatter(
                x=selected_df[x_col],
                y=selected_df[y_col],
                mode="markers+text",
                name=f"{selected_country} selected",
                marker=dict(
                    size=26,
                    color=selected_family_color,
                    symbol="star",
                    line=dict(width=2.8, color="#F8FAFC"),
                ),
                text=[f"{selected_country}"],
                textposition="top center",
                textfont=dict(color="#F8FAFC", size=15),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    f"{x_label}: " + "%{x:.2f}<br>"
                    f"{y_label}: " + "%{y:.2f}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    for family_name, family_df in plot_df.groupby("structural_family"):
        center_x = family_df[x_col].mean()
        center_y = family_df[y_col].mean()

        label = (
            family_name
            .replace(" Systems", "")
            .replace(" / ", " /<br>")
        )

        fig.add_annotation(
            x=center_x,
            y=center_y,
            text=f"<b>{label}</b>",
            showarrow=False,
            opacity=0.75,
            font=dict(
                size=13,
                color=FAMILY_COLORS.get(family_name, "#94A3B8"),
            ),
            bgcolor="rgba(2,6,23,0.62)",
            bordercolor=FAMILY_COLORS.get(family_name, "#94A3B8"),
            borderwidth=1,
            borderpad=4,
        )

    # Keep the graph annotation minimal to avoid duplicating the right-side card.
    if correlation is not None and not pd.isna(correlation):
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.96,
            y=0.96,
            align="center",
            showarrow=False,
            text=f"<b>r = {correlation:.2f}</b>",
            font=dict(size=13, color="#F8FAFC"),
            bgcolor="rgba(2,6,23,0.70)",
            bordercolor="#38BDF8",
            borderwidth=1,
            borderpad=6,
        )

    fig.add_hline(
        y=0,
        line_width=1,
        line_dash="dash",
        line_color="rgba(148,163,184,0.55)",
    )
    fig.add_vline(
        x=0,
        line_width=1,
        line_dash="dash",
        line_color="rgba(148,163,184,0.55)",
    )

    fig.update_layout(
        height=450,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.32)",
        margin=dict(l=18, r=18, t=24, b=26),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="left",
            x=0,
            font=dict(size=11),
            bgcolor="rgba(2,6,23,0)",
        ),
        xaxis=dict(
            title=dict(text=x_label, font=dict(size=16)),
            zeroline=False,
            gridcolor="rgba(148,163,184,0.18)",
            tickfont=dict(size=13),
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(size=16)),
            zeroline=False,
            gridcolor="rgba(148,163,184,0.18)",
            tickfont=dict(size=13),
        ),
    )

    return fig





def render_equal_interpretation_card(title: str, value: str, body: str, status: str, accent: str = "#38BDF8"):
    """Equal-height interpretation card for Section 05 current version logic."""
    st.html(
        f"""
        <div style="
            min-height: 184px;
            height: 184px;
            border-radius: 16px;
            border: 1px solid rgba(56,189,248,0.34);
            background: linear-gradient(135deg, rgba(30,58,95,0.82), rgba(15,23,42,0.86));
            padding: 14px 15px 13px 15px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        ">
            <div>
                <div style="color:#F8FAFC; font-size:0.82rem; font-weight:900; margin-bottom:10px;">{title}</div>
                <div style="color:#F8FAFC; font-size:1.18rem; font-weight:900; font-family:'IBM Plex Mono','Roboto Mono',monospace; margin-bottom:10px; line-height:1.2;">{value}</div>
                <div style="color:{accent}; font-size:0.88rem; font-weight:800; line-height:1.38;">{body}</div>
            </div>
            <div style="color:#F8FAFC; font-size:0.82rem; font-weight:850; line-height:1.30; margin-top:10px;">{status}</div>
        </div>
        """
    )


def render_journey_log_html(log_df: pd.DataFrame):
    """Compact, newest-first journey log table for current version review.

    The full shared log remains stored in st.session_state. This display keeps
    only the columns users need during the demo and shows the latest action first.
    """
    if log_df is None or log_df.empty:
        st.info("No journey actions recorded yet.")
        return

    display_cols = [
        "step",
        "page",
        "country",
        "reference",
        "topic",
        "observation",
        "next_step",
    ]
    display_df = log_df.copy()
    for col in display_cols:
        if col not in display_df.columns:
            display_df[col] = ""

    display_df = (
        display_df[display_cols]
        .sort_values("step", ascending=False)
        .head(8)
    )

    rename_map = {
        "step": "Step",
        "page": "Page",
        "country": "Country",
        "reference": "Reference",
        "topic": "Topic",
        "observation": "Observation",
        "next_step": "Next",
    }
    display_df = display_df.rename(columns=rename_map)

    html_rows = []
    for _, row in display_df.iterrows():
        cells = "".join(f"<td>{row[col]}</td>" for col in display_df.columns)
        html_rows.append(f"<tr>{cells}</tr>")

    headers = "".join(f"<th>{col}</th>" for col in display_df.columns)
    rows = "".join(html_rows)

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

    st.html(
        f"""
        <div style="
            margin-top: 12px;
            border-radius: 16px;
            border: 1px solid rgba(56,189,248,0.34);
            background: rgba(15, 23, 42, 0.72);
            padding: 14px;
            overflow-x: auto;
        ">
            <div style="color:#F8FAFC; font-size:1rem; font-weight:900; margin-bottom:4px;">Journey Log</div>
            <div style="color:#CBD5E1; font-size:0.82rem; margin-bottom:12px;">Latest actions first. Full details remain stored for P5/export.</div>
            <table style="
                width:100%;
                border-collapse: collapse;
                table-layout: fixed;
                background: rgba(51, 65, 85, 0.92);
                color:#F8FAFC;
                font-size:0.82rem;
            ">
                <colgroup>{colgroup}</colgroup>
                <thead><tr>{headers}</tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        <style>
            table th {{
                background: rgba(56, 189, 248, 0.14);
                color: #E0F2FE;
                border: 1px solid rgba(148,163,184,0.40);
                padding: 9px 8px;
                text-align: left;
                font-size: 0.74rem;
                font-weight: 900;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }}
            table td {{
                border: 1px solid rgba(148,163,184,0.32);
                padding: 9px 8px;
                vertical-align: top;
                line-height: 1.34;
                background: rgba(51, 65, 85, 0.78);
                word-wrap: break-word;
            }}
            table tbody tr:nth-child(even) td {{
                background: rgba(71, 85, 105, 0.68);
            }}
        </style>
        """
    )


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.markdown("## P2 — Investigate Tradeoffs")

st.html("""
<style>
.p2-brand-compact {
    min-height: 66px !important;
    padding: 10px 14px !important;
}
.p2-brand-compact .p1-logo { font-size: 32px !important; }
.p2-brand-compact .p1-brand-title { font-size: 1.02rem !important; }
.p2-brand-compact .p1-brand-subtitle { font-size: 0.72rem !important; }
.p2-kpi-ribbon { margin-bottom: 12px !important; }
.p2-kpi-ribbon .p1-kpi-card {
    padding: 10px 14px !important;
    min-height: 72px !important;
}
.p2-kpi-ribbon .p1-kpi-main { font-size: 0.88rem !important; }
.p2-kpi-ribbon .p1-kpi-sub { font-size: 0.72rem !important; }
.p2-kpi-ribbon .p1-kpi-number { font-size: 1.45rem !important; }
</style>
""")


# =============================================================================
# TOP CONTEXT — SHARED FRAME
# =============================================================================

top_col1, top_col2, top_col3, top_col_ref_country, top_col4 = st.columns(
    [1.8, 1.05, 1.15, 1.15, 0.9],
    gap="medium",
)

with top_col1:
    st.html(
        """
        <div class="p1-brand p2-brand-compact">
            <div class="p1-logo">⚖</div>
            <div>
                <div class="p1-brand-title">TRADEOFF<br>EXPLORER</div>
                <div class="p1-brand-subtitle">Investigate structural tensions<br>across European systems.</div>
            </div>
        </div>
        """
    )

country_options = sorted(tradeoff_df["country_name"].dropna().unique().tolist())
reference_options = ["EU Average", "Family Average", "Another Country"]
view_options = ["Relative", "Absolute"]

initialize_p2_from_atlas_state(
    country_options=country_options,
    reference_options=reference_options,
    view_options=view_options,
)

with top_col2:
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        key="p2_selected_country",
    )

with top_col3:
    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        key="p2_selected_reference",
    )

with top_col_ref_country:
    if selected_reference == "Another Country":
        reference_country_options = [c for c in country_options if c != selected_country]
        if not reference_country_options:
            reference_country_options = country_options

        if st.session_state.get("p2_reference_country") not in reference_country_options:
            st.session_state["p2_reference_country"] = _valid_or_default(
                st.session_state.get("atlas_reference_country", DEFAULT_REFERENCE_COUNTRY),
                reference_country_options,
                DEFAULT_REFERENCE_COUNTRY,
            )

        reference_country = st.selectbox(
            "Reference Country",
            options=reference_country_options,
            key="p2_reference_country",
        )
    else:
        reference_country = None
        st.text_input(
            "Reference Country",
            value="-----------",
            disabled=True,
            key="p2_reference_country_disabled",
        )

with top_col4:
    view_mode = st.radio(
        "View Mode",
        options=view_options,
        horizontal=True,
        key="p2_view_mode",
    )

sync_p2_to_atlas_state()


# =============================================================================
# P2 CONTEXT RIBBON
# =============================================================================

st.html(
    f"""
    <div class="p1-kpi-ribbon p2-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">CURRENT PAGE</div>
            <div class="p1-kpi-main">P2 Tradeoff Explorer</div>
            <div class="p1-kpi-sub">Investigation stage</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#38BDF8;">COUNTRY</div>
            <div class="p1-kpi-main">{selected_country}</div>
            <div class="p1-kpi-sub">Selected system</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#4ADE80;">DEFAULT TRADEOFF</div>
            <div class="p1-kpi-main">Innovation ↔ Fiscal</div>
            <div class="p1-kpi-sub">Skeleton placeholder</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F59E0B;">EVIDENCE</div>
            <div class="p1-kpi-number" style="color:#F59E0B;">B</div>
            <div class="p1-kpi-sub">Placeholder badge</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F472B6;">MODE</div>
            <div class="p1-kpi-main">{view_mode}</div>
            <div class="p1-kpi-sub">Display mode</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label">REFERENCE</div>
            <div class="p1-kpi-main">{selected_reference}</div>
            <div class="p1-kpi-sub">Comparison context</div>
        </div>
    </div>
    """
)


render_journey_progress(2)

st.html(
    """
    <div style="color:#38BDF8; font-size:0.96rem; font-weight:850; line-height:1.45; margin:6px 0 14px 0;">
        Choose a tradeoff to investigate → read the scatter pattern → compare family context and exceptions.
    </div>
    """
)

render_page_intro()


# =============================================================================
# THREE-COLUMN PAGE FRAME
# =============================================================================

left_col, main_col, right_col = st.columns(
    [0.85, 5.4, 1.15],
    gap="medium",
)

sections = [
    ("01", "CHOOSE INVESTIGATION", "Select the tradeoff question."),
    ("02", "OBSERVE PATTERN", "Read the tradeoff space."),
    ("03", "EXPLORE FAMILIES", "Check family behavior."),
    ("04", "INVESTIGATE EXCEPTIONS", "Find countries that differ."),
    ("05", "INTERPRET FINDINGS", "Translate pattern into insight."),
    ("06", "CONTINUE", "Move to strategy."),
]

with left_col:
    render_left_rail_placeholder(
        page_number=2,
        page_title="Tradeoff Explorer",
        sections=sections,
    )

with main_col:

         # =========================================================================
    # SECTION 01
    # =========================================================================

    st.markdown('<a id="p2-tradeoff-select"></a>', unsafe_allow_html=True)

    render_section_title(
        number="01",
        title="Which structural question should we investigate?",
        subtitle="Start with a curated tradeoff story, or open the full dimension-pair list for advanced exploration.",
    )

    def reset_p2_advanced_tradeoff():
        st.session_state["p2_advanced_tradeoff"] = "None — stay with curated question"

    curated_col, advanced_col, current_col = st.columns([1.0, 1.0, 1.8], gap="medium")

    with curated_col:
        selected_tradeoff = st.selectbox(
            "Curated tradeoff",
            options=CURATED_TRADEOFF_NAMES,
            index=0,
            key="p2_selected_tradeoff",
            on_change=reset_p2_advanced_tradeoff,
        )

    with advanced_col:
        advanced_tradeoff = st.selectbox(
            "Advanced relationship",
            options=["None — stay with curated question"] + ADVANCED_TRADEOFF_NAMES,
            index=0,
            key="p2_advanced_tradeoff",
        )

    active_tradeoff = (
        selected_tradeoff
        if advanced_tradeoff == "None — stay with curated question"
        else advanced_tradeoff
    )

    active_tradeoff_config = TRADEOFF_REGISTRY[active_tradeoff]

    with current_col:
        st.html(
            f"""
            <div style="
                border:1px solid rgba(56,189,248,0.36);
                border-radius:14px;
                background:linear-gradient(135deg, rgba(30,58,95,0.72), rgba(15,23,42,0.78));
                padding:10px 14px;
                min-height:78px;
            ">
                <div style="color:#CBD5E1; font-size:0.70rem; font-weight:900; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:5px;">Current Investigation</div>
                <div style="color:#F8FAFC; font-size:1.02rem; font-weight:900; font-family:'IBM Plex Mono','Roboto Mono',monospace; line-height:1.10; margin-bottom:5px;">{active_tradeoff}</div>
                <div style="color:#E2E8F0; font-size:0.84rem; font-weight:700; line-height:1.25;">{active_tradeoff_config['question']}</div>
            </div>
            """
        )


        # =========================================================================
    # SECTION 02
    # =========================================================================

    active_tradeoff_config = TRADEOFF_REGISTRY[active_tradeoff]


    render_section_title(
        number="02",
        title="What pattern appears across Europe?",
        subtitle=active_tradeoff_config["question"],
    )

    x_col = active_tradeoff_config["x_col"]
    y_col = active_tradeoff_config["y_col"]

    corr_df = tradeoff_df.dropna(subset=[x_col, y_col]).copy()
    correlation = corr_df[x_col].corr(corr_df[y_col])
    sample_size = len(corr_df)

    pattern_strength = get_pattern_strength(correlation)
    direction = get_pattern_direction(correlation)

    selected_row = corr_df[corr_df["country_name"] == selected_country]

    if not selected_row.empty:
        selected_x = selected_row.iloc[0][x_col]
        selected_y = selected_row.iloc[0][y_col]
        selected_family = selected_row.iloc[0]["structural_family"]
    else:
        selected_x = np.nan
        selected_y = np.nan
        selected_family = "Unknown"

    # Family correlations are used for graph hierarchy and user interpretation.
    family_corr_map = {}
    for family_name, family_df in corr_df.groupby("structural_family"):
        if len(family_df) >= 3:
            family_corr_map[family_name] = family_df[x_col].corr(family_df[y_col])
        else:
            family_corr_map[family_name] = np.nan

    strong_family_trends = [
        family_name
        for family_name, family_r in family_corr_map.items()
        if pd.notna(family_r) and abs(family_r) >= 0.60
    ]

    if pd.notna(correlation) and abs(correlation) >= 0.60:
        pattern_comment = "Strong EU-wide trend visible. Family lines are hidden to keep the hierarchy clear."
    elif strong_family_trends:
        pattern_comment = "No strong EU-wide trend, but a family-specific trend appears."
    else:
        pattern_comment = "No strong EU-wide trend is visible in this view."

    if len(corr_df) >= 3 and pd.notna(selected_x) and pd.notna(selected_y):
        section2_slope, section2_intercept = np.polyfit(
            corr_df[x_col].astype(float),
            corr_df[y_col].astype(float),
            1,
        )
        selected_expected_y = section2_slope * selected_x + section2_intercept
        selected_deviation = selected_y - selected_expected_y
    else:
        selected_deviation = np.nan

    if pd.isna(selected_deviation):
        country_position_label = "Position unavailable"
        country_position_status = "Missing data for this tradeoff."
    elif abs(selected_deviation) < 0.35:
        country_position_label = "Near expected pattern"
        country_position_status = "Read as typical within the current fitted relationship."
    elif selected_deviation > 0:
        country_position_label = "Above expected pattern"
        country_position_status = "Read as unusually high on the vertical dimension for its horizontal position."
    else:
        country_position_label = "Below expected pattern"
        country_position_status = "Read as unusually low on the vertical dimension for its horizontal position."

    if pd.notna(correlation) and abs(correlation) < 0.15:
        country_position_status = "Because the EU-wide trend is very weak, treat this mainly as location, not a strong deviation."

    registry_evidence_level = active_tradeoff_config["evidence"]

    # IMPORTANT: do not rewrite the source/registry evidence from the live graph.
    # The evidence badge shows the configured registry evidence. A separate
    # live signal is displayed to expose validation mismatches transparently.
    if pd.notna(correlation) and abs(correlation) >= 0.65:
        live_evidence_level = "A"
    elif pd.notna(correlation) and abs(correlation) >= 0.35:
        live_evidence_level = "B"
    elif pd.notna(correlation) and abs(correlation) >= 0.15:
        live_evidence_level = "C"
    else:
        live_evidence_level = "D"

    evidence_level = registry_evidence_level

    evidence_colors = {
        "A": "#22C55E",
        "B": "#EAB308",
        "C": "#F97316",
        "D": "#EF4444",
    }

    evidence_labels = {
        "A": "Strong Evidence",
        "B": "Moderate Evidence",
        "C": "Exploratory Evidence",
        "D": "Weak / No General Evidence",
    }

    evidence_confidence_labels = {
        "A": "High",
        "B": "Medium",
        "C": "Exploratory",
        "D": "Low",
    }

    evidence_color = evidence_colors.get(evidence_level, "#94A3B8")
    evidence_label = evidence_labels.get(evidence_level, "Evidence Review")
    evidence_confidence = active_tradeoff_config["confidence"]

    visual_col, insight_col = st.columns([2.75, 1], gap="medium")

    with visual_col:
        st.html(
            """
            <div style="
                color:#CBD5E1;
                font-size:0.86rem;
                line-height:1.35;
                margin:0 0 8px 0;
            ">
                Trendline rule: show the EU-wide line only when |r| ≥ 0.60.
                If the EU-wide trend is weak, show only structural-family lines with |r| ≥ 0.60.
            </div>
            """
        )

        st.plotly_chart(
            make_tradeoff_scatter(
                df=tradeoff_df,
                selected_country=selected_country,
                tradeoff_config=active_tradeoff_config,
                correlation=correlation,
                reference_country=reference_country if selected_reference == "Another Country" else None,
            ),
            use_container_width=True,
        )

        st.caption(
            "Positions show EU-relative structural scores. "
            "Higher values indicate stronger relative structural capacity."
        )

        render_guided_questions(
            title="Observation Questions",
            questions=[
                "Are countries clustered, or spread evenly across the space?",
                "Is the relationship strong enough to interpret?",
                f"Does {selected_country} follow the pattern or sit away from it?",
            ],
            accent="#C084FC",
        )


    with insight_col:
        render_pattern_summary_card(
            pattern_strength=pattern_strength,
            direction=direction,
            correlation=correlation,
            sample_size=sample_size,
            pattern_comment=pattern_comment,
        )

        st.html(
            f"""
            <div style="
                border: 1px solid {evidence_color};
                border-left: 6px solid {evidence_color};
                background: rgba(15, 23, 42, 0.82);
                border-radius: 14px;
                padding: 14px;
                margin-bottom: 9px;
            ">
                <div style="
                    color: #CBD5E1;
                    font-size: 0.72rem;
                    font-weight: 800;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    margin-bottom: 8px;
                ">
                    Evidence Level
                </div>

                <div style="
                    color: {evidence_color};
                    font-size: 1.7rem;
                    font-weight: 900;
                    line-height: 1;
                    margin-bottom: 8px;
                ">
                    {evidence_level}
                </div>

                <div style="
                    color: #F8FAFC;
                    font-size: 1rem;
                    font-weight: 800;
                    margin-bottom: 8px;
                ">
                    {evidence_label}
                </div>

                <div style="color:#38BDF8; font-size:0.9rem; font-weight:700;">
                    r = {correlation:.2f} · n = {sample_size}
                </div>

                <div style="color:#CBD5E1; font-size:0.86rem; margin-top:8px;">
                    Registry confidence: {evidence_confidence}<br>
                    Live graph signal: {live_evidence_level} from r = {correlation:.2f}
                </div>
            </div>
            """
        )

        st.html(
            f"""
            <div style="
                border:1px solid rgba(56,189,248,0.38);
                border-radius:14px;
                padding:14px 15px;
                background:linear-gradient(135deg, rgba(30,58,95,0.82), rgba(15,23,42,0.86));
                margin-bottom:10px;
            ">
                <div style="color:#F8FAFC; font-size:0.82rem; font-weight:900; margin-bottom:7px;">{selected_country} Position</div>
                <div style="color:#F8FAFC; font-size:1.18rem; font-weight:900; font-family:'IBM Plex Mono','Roboto Mono',monospace; margin-bottom:8px; line-height:1.18;">{country_position_label}</div>
                <div style="color:#38BDF8; font-size:0.86rem; font-weight:850; line-height:1.32; margin-bottom:7px;">
                    {active_tradeoff_config['x_label']}: {selected_x:.2f} | {active_tradeoff_config['y_label']}: {selected_y:.2f} | Deviation: {selected_deviation:+.2f}
                </div>
                <div style="color:#E2E8F0; font-size:0.83rem; font-weight:650; line-height:1.32;">{selected_family}. {country_position_status}</div>
            </div>
            """
        )


    # =========================================================================
    # SECTION 03
    # =========================================================================

    render_section_title(
        number="03",
        title="Do structural families explain the pattern?",
        subtitle=(
            "Before looking for exceptions, check whether countries behave "
            "differently by structural family."
        ),
    )

    family_summary = (
        corr_df
        .groupby("structural_family")
        .agg(
            avg_x=(x_col, "mean"),
            avg_y=(y_col, "mean"),
            count=("country_name", "count"),
        )
        .reset_index()
    )

    fam_cols = st.columns(len(family_summary), gap="medium")

    for fam_col, (_, fam_row) in zip(fam_cols, family_summary.iterrows()):
        family_name = fam_row["structural_family"]
        family_color = FAMILY_COLORS.get(family_name, "#94A3B8")
        family_r = family_corr_map.get(family_name, np.nan)
        family_strength = get_pattern_strength(family_r)
        family_direction = get_pattern_direction(family_r)
        family_arrow = get_direction_arrow(family_r)

        with fam_col:
            st.html(
                f"""
                <div style="
                    min-height: 178px;
                    border-radius: 16px;
                    border: 1px solid {family_color};
                    border-left: 6px solid {family_color};
                    background: rgba(15,23,42,0.80);
                    padding: 18px;
                ">
                    <div style="
                        color:{family_color};
                        font-size:0.75rem;
                        font-weight:900;
                        letter-spacing:0.08em;
                        text-transform:uppercase;
                        margin-bottom:10px;
                    ">
                        Family Pattern
                    </div>

                    <div style="
                        color:#F8FAFC;
                        font-size:1.05rem;
                        font-weight:900;
                        margin-bottom:12px;
                    ">
                        {family_name}
                    </div>

                    <div style="color:#CBD5E1; font-size:0.9rem; line-height:1.5;">
                        <span style="color:{family_color}; font-weight:900; font-size:1.05rem;">
                            {family_arrow} r = {family_r:.2f}
                        </span><br>
                        {family_strength} {family_direction}<br>
                        Avg. {active_tradeoff_config["x_label"]}: 
                        <b>{fam_row["avg_x"]:.2f}</b><br>
                        Avg. {active_tradeoff_config["y_label"]}: 
                        <b>{fam_row["avg_y"]:.2f}</b><br>
                        Countries: <b>{int(fam_row["count"])}</b>
                    </div>
                </div>
                """
            )

    render_compact_lens_block(
        question_title="Family Questions",
        questions=[
            "Which family behaves differently from the others?",
            "Are families clearly separated, or mostly overlapping?",
            "Does family context explain more than the EU-wide average?",
        ],
        lens_title="Family Lens",
        lens_value="Pattern ≠ Explanation",
        lens_body="Family context tests whether the EU-wide pattern is shared or fragmented.",
        next_step="Next: identify exceptions →",
        accent="#38BDF8",
    )

    # =========================================================================
    # SECTION 04
    # =========================================================================

    render_section_title(
        number="04",
        title="Who behaves differently from the pattern?",
        subtitle="Exceptions are educationally valuable because they reveal structural context.",
    )

    if len(corr_df) >= 3:
        slope, intercept = np.polyfit(
            corr_df[x_col].astype(float),
            corr_df[y_col].astype(float),
            1,
        )
        corr_df["expected_y"] = slope * corr_df[x_col] + intercept
        corr_df["deviation"] = corr_df[y_col] - corr_df["expected_y"]
    else:
        corr_df["deviation"] = 0

    selected_exception = corr_df[corr_df["country_name"] == selected_country]

    positive_exceptions = (
        corr_df
        .sort_values("deviation", ascending=False)
        .head(2)
    )

    negative_exceptions = (
        corr_df
        .sort_values("deviation", ascending=True)
        .head(2)
    )

    exception_df = pd.concat(
        [
            selected_exception,
            positive_exceptions,
            negative_exceptions,
        ],
        ignore_index=True,
    ).drop_duplicates(subset=["country_name"]).head(4)

    ex_cols = st.columns(4, gap="medium")

    for ex_col, (_, row) in zip(ex_cols, exception_df.iterrows()):
        deviation = row["deviation"]
        direction_label = (
            "Above expected"
            if deviation >= 0
            else "Below expected"
        )

        with ex_col:
            render_delta_card(
                title=row["country_name"],
                value=direction_label,
                delta_value=float(deviation),
                status=f"Deviation from pattern: {deviation:+.2f}",
            )

    render_compact_lens_block(
        question_title="Exception Questions",
        questions=[
            "Which countries break the pattern most clearly?",
            "Why might they differ from the expected relationship?",
            "Are they bridges, outliers, or constrained systems?",
        ],
        lens_title="Exception Lens",
        lens_value="Outliers Teach",
        lens_body="Countries above or below the expected pattern can reveal bridge roles or constraints.",
        next_step="Next: interpret findings →",
        accent="#F59E0B",
    )

    # =========================================================================
    # P2 current version INTERPRETATION + MISSION ENTRY
    # =========================================================================

    top_positive_exception = (
        positive_exceptions.iloc[0]["country_name"]
        if len(positive_exceptions) > 0
        else "Not available"
    )

    top_negative_exception = (
        negative_exceptions.iloc[0]["country_name"]
        if len(negative_exceptions) > 0
        else "Not available"
    )

    strongest_family_name = "No strong family-specific trend"
    strongest_family_r = np.nan
    if family_corr_map:
        valid_family_corrs = {
            family_name: family_r
            for family_name, family_r in family_corr_map.items()
            if pd.notna(family_r)
        }
        if valid_family_corrs:
            strongest_family_name, strongest_family_r = max(
                valid_family_corrs.items(),
                key=lambda item: abs(item[1]),
            )

    if pd.notna(correlation) and abs(correlation) >= 0.60:
        key_observation_value = "Strong EU-wide pattern"
        key_observation_text = (
            f"Across Europe, {active_tradeoff_config['x_label']} and "
            f"{active_tradeoff_config['y_label']} show a strong "
            f"{direction.lower()} association in this view."
        )
    elif strong_family_trends:
        key_observation_value = "Family-specific pattern"
        key_observation_text = (
            "The EU-wide pattern is not strong enough to show a general trendline, "
            f"but {strongest_family_name} shows a stronger internal pattern."
        )
    else:
        key_observation_value = "No clear general trend"
        key_observation_text = (
            "The EU-wide pattern is weak. Use the scatter mainly to compare clusters, "
            "families, and country positions rather than to infer a general relationship."
        )

    if pd.notna(strongest_family_r):
        family_interpretation_text = (
            f"Strongest family signal: {strongest_family_name} "
            f"({get_direction_arrow(strongest_family_r)} r = {strongest_family_r:.2f}). "
            "This suggests family context may matter for interpretation."
        )
    else:
        family_interpretation_text = (
            "No family has enough valid observations to estimate a separate trend here."
        )

    germany_interpretation_text = (
        f"{selected_country} is {country_position_label.lower()} "
        f"(deviation {selected_deviation:+.2f}). {country_position_status}"
        if pd.notna(selected_deviation)
        else f"{selected_country} position is unavailable for this tradeoff."
    )

    if registry_evidence_level != live_evidence_level:
        verification_note = (
            f"Validation flag: registry evidence is {registry_evidence_level}, "
            f"but the live graph signal is {live_evidence_level} from r = {correlation:.2f}. "
            "Do not change the data here; review the registry before final freeze."
        )
    else:
        verification_note = "Live graph signal and registry evidence are aligned for this relationship."

    key_observation = (
        f"{active_tradeoff} shows a {pattern_strength.lower()} "
        f"{direction.lower()} relationship. {key_observation_text}"
    )

    family_context_label = (
        f"{selected_country} belongs to {selected_family}."
        if selected_family != "Unknown"
        else "Family context unavailable."
    )

    mission_entry = {
        "step": 2,
        "page": "P2 Tradeoff Explorer",
        "action_type": "investigation",
        "country": selected_country,
        "topic": active_tradeoff,
        "observation": key_observation,
        "evidence": f"Registry {evidence_level}; live {live_evidence_level}",
        "confidence": evidence_confidence,
        "family_context": family_context_label,
        "exception": f"Above: {top_positive_exception}; Below: {top_negative_exception}",
        "next_step": "Build a Strategy",
    }

    add_journey_event(
        page=mission_entry["page"],
        action_type=mission_entry["action_type"],
        country=mission_entry["country"],
        topic=mission_entry["topic"],
        observation=mission_entry["observation"],
        evidence=mission_entry["evidence"],
        confidence=mission_entry["confidence"],
        family_context=mission_entry["family_context"],
        exception=mission_entry["exception"],
        next_step=mission_entry["next_step"],
        dedupe_key=f"p2_observation::{selected_country}::{active_tradeoff}::{live_evidence_level}::{correlation:.3f}",
    )

    mission_log_df = get_journey_log_df()

    # =========================================================================
    # SECTION 05
    # =========================================================================

    render_section_title(
        number="05",
        title="What does this tradeoff tell us?",
        subtitle="Translate the visual pattern into a cautious, evidence-aware interpretation.",
    )

    int1, int2, int3 = st.columns(3, gap="medium")

    with int1:
        render_equal_interpretation_card(
            title="Key Observation",
            value=key_observation_value,
            body=key_observation_text,
            status="Interpret as association, not causality.",
            accent="#38BDF8",
        )

    with int2:
        render_equal_interpretation_card(
            title="Family Context",
            value=(
                "Family signal visible"
                if pd.notna(strongest_family_r) and abs(strongest_family_r) >= 0.60
                else "Family signal limited"
            ),
            body=family_interpretation_text,
            status=verification_note,
            accent="#38BDF8",
        )

    with int3:
        render_equal_interpretation_card(
            title=f"{selected_country} Reading",
            value=country_position_label,
            body=germany_interpretation_text,
            status="Prompt for Strategic Choices, not a recommendation.",
            accent="#38BDF8",
        )

    # =========================================================================
# SECTION 06
# =========================================================================

render_section_title(
    number="06",
    title="Where should we go next?",
    subtitle="Continue from investigation toward strategic choice.",
)

cta_try, cta_next, cta_country, cta_assume = st.columns(4, gap="medium")

# -------------------------------------------------------------------------
# TRY ANOTHER TRADEOFF
# -------------------------------------------------------------------------

with cta_try:
    with st.container(border=True):

        st.html(
            """
            <div class="atlas-cta-explore"
                 style="
                    min-height:132px;
                    padding:14px 16px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                 ">

                <div>

                    <div style="
                        color:#94A3B8;
                        font-size:0.72rem;
                        font-weight:900;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                    ">
                        Try Again
                    </div>

                    <div style="
                        color:#4ADE80;
                        font-size:1.12rem;
                        font-weight:900;
                        margin:8px 0;
                    ">
                        Try Another Tradeoff
                    </div>

                    <div style="
                        color:#CBD5E1;
                        font-size:0.84rem;
                        line-height:1.35;
                    ">
                        Return to the investigation hub and choose another relationship.
                    </div>

                </div>

            </div>
            """
        )

        st.markdown(
            """
            <a href="#p2-tradeoff-select" class="p2-inline-cta-button">Try Another Tradeoff</a>
            <style>
            .p2-inline-cta-button {
                display:block;
                width:100%;
                text-align:center;
                text-decoration:none !important;
                background:linear-gradient(180deg, #38BDF8, #2563EB) !important;
                color:#FFFFFF !important;
                border:1px solid rgba(125,211,252,0.80) !important;
                border-radius:12px !important;
                font-weight:850 !important;
                padding:0.75rem 1rem !important;
                box-shadow:0 0 14px rgba(56,189,248,0.28), 0 0 24px rgba(37,99,235,0.20) !important;
                line-height:1.15 !important;
            }
            .p2-inline-cta-button:hover {
                background:linear-gradient(180deg, #67E8F9, #3B82F6) !important;
                color:#FFFFFF !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

# -------------------------------------------------------------------------
# STRATEGIC CHOICES
# -------------------------------------------------------------------------

with cta_next:
    with st.container(border=True):

        st.html(
            """
            <div class="atlas-cta-navigation"
                 style="
                    min-height:132px;
                    padding:14px 16px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                 ">

                <div>

                    <div style="
                        color:#94A3B8;
                        font-size:0.72rem;
                        font-weight:900;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                    ">
                        Next Page
                    </div>

                    <div style="
                        color:#38BDF8;
                        font-size:1.12rem;
                        font-weight:900;
                        margin:8px 0;
                    ">
                        Strategic Choices
                    </div>

                    <div style="
                        color:#CBD5E1;
                        font-size:0.84rem;
                        line-height:1.35;
                    ">
                        Move from investigation toward a strategy-building exercise.
                    </div>

                </div>

            </div>
            """
        )

        if st.button(
            "Open Strategic Choices",
            key="p2_cta_strategic_choices",
            use_container_width=True,
        ):
            sync_p2_to_atlas_state()
            add_journey_event(
                page="P2 Tradeoff Explorer",
                action_type="open page",
                country=selected_country,
                topic="Continue to Strategic Choices",
                observation=f"Opened P3 after investigating {active_tradeoff} for {selected_country}.",
                next_step="Build a strategy",
                dedupe_key=f"p2_to_p3::{selected_country}::{active_tradeoff}",
            )
            safe_switch_page("pages/p3_strategic_choices.py")

# -------------------------------------------------------------------------
# COUNTRY EXPLORER
# -------------------------------------------------------------------------

with cta_country:
    with st.container(border=True):

        st.html(
            """
            <div class="atlas-cta-compare"
                 style="
                    min-height:132px;
                    padding:14px 16px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                 ">

                <div>

                    <div style="
                        color:#94A3B8;
                        font-size:0.72rem;
                        font-weight:900;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                    ">
                        Start New Country
                    </div>

                    <div style="
                        color:#22D3EE;
                        font-size:1.12rem;
                        font-weight:900;
                        margin:8px 0;
                    ">
                        Country Explorer
                    </div>

                    <div style="
                        color:#CBD5E1;
                        font-size:0.84rem;
                        line-height:1.35;
                    ">
                        Go back to the country story and begin from another structural profile.
                    </div>

                </div>

            </div>
            """
        )

        if st.button(
            "Open Country Explorer",
            key="p2_cta_country_explorer",
            use_container_width=True,
        ):
            sync_p2_to_atlas_state()
            add_journey_event(
                page="P2 Tradeoff Explorer",
                action_type="open page",
                country=selected_country,
                topic="Return to Country Explorer",
                observation=f"Returned to P1 from {active_tradeoff} investigation.",
                next_step="Review country/reference context",
                dedupe_key=f"p2_to_p1::{selected_country}::{active_tradeoff}",
            )
            safe_switch_page("pages/p1_country_explorer.py")

# -------------------------------------------------------------------------
# ASSUMPTIONS
# -------------------------------------------------------------------------

with cta_assume:
    with st.container(border=True):

        st.html(
            """
            <div class="atlas-cta-reflect"
                 style="
                    min-height:132px;
                    padding:14px 16px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                 ">

                <div>

                    <div style="
                        color:#94A3B8;
                        font-size:0.72rem;
                        font-weight:900;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                    ">
                        Learn
                    </div>

                    <div style="
                        color:#A855F7;
                        font-size:1.12rem;
                        font-weight:900;
                        margin:8px 0;
                    ">
                        Assumptions
                    </div>

                    <div style="
                        color:#CBD5E1;
                        font-size:0.84rem;
                        line-height:1.35;
                    ">
                        Review evidence limits, uncertainty, and why this is not a recommendation.
                    </div>

                </div>

            </div>
            """
        )

        if st.button(
            "Review Assumptions",
            key="p2_cta_assumptions",
            use_container_width=True,
        ):
            add_journey_event(
                page="P2 Tradeoff Explorer",
                action_type="review assumptions",
                country=selected_country,
                topic=active_tradeoff,
                observation="Opened the assumptions reminder for exploratory, non-causal interpretation.",
                next_step="Continue with caution",
                dedupe_key=f"p2_assumptions::{selected_country}::{active_tradeoff}",
            )
            st.info(
                "Assumptions page/link will be wired during global framework cleanup."
            )


# =============================================================================
# RIGHT MISSION BAR — PAGE CONTEXT
# =============================================================================

with right_col:
    reference_label = (
        f"Another Country: {reference_country}"
        if selected_reference == "Another Country" and reference_country
        else selected_reference
    )

    st.html(
        f"""
        <div style="
            border:1px solid rgba(56,189,248,0.38);
            border-radius:16px;
            padding:14px 15px;
            background:linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.78));
            position: sticky;
            top: 0.75rem;
        ">
            <div style="
                color:#38BDF8;
                font-size:0.76rem;
                font-weight:900;
                letter-spacing:0.10em;
                text-transform:uppercase;
                margin-bottom:12px;
            ">Mission Log</div>

            <div style="color:#F8FAFC; font-size:0.86rem; font-weight:900; margin-bottom:5px;">Current Mission</div>
            <div style="color:#CBD5E1; font-size:0.82rem; line-height:1.35; margin-bottom:14px;">
                Investigate how <b>{selected_country}</b> behaves in the selected tradeoff space.
            </div>

            <div style="color:#F8FAFC; font-size:0.86rem; font-weight:900; margin-bottom:5px;">Latest Learning</div>
            <div style="color:#CBD5E1; font-size:0.82rem; line-height:1.35; margin-bottom:14px;">
                {active_tradeoff}: {pattern_strength.lower()} {direction.lower()} pattern; evidence {evidence_level}.
            </div>

            <div style="color:#F8FAFC; font-size:0.86rem; font-weight:900; margin-bottom:5px;">Context</div>
            <div style="color:#CBD5E1; font-size:0.82rem; line-height:1.35; margin-bottom:14px;">
                Country: <b>{selected_country}</b><br>
                Reference: <b>{reference_label}</b><br>
                View: <b>{view_mode}</b>
            </div>

            <div style="color:#A3E635; font-size:0.86rem; font-weight:900; margin-bottom:5px;">Suggested Next Step</div>
            <div style="color:#CBD5E1; font-size:0.82rem; line-height:1.35;">
                Use the graph and questions to interpret the tradeoff, then move to Strategy Choices.
            </div>
        </div>
        """
    )

# =============================================================================
# FULL WIDTH JOURNEY LOG
# =============================================================================

st.markdown("---")

st.html(
    """
    <div style="
        border:1px solid rgba(56,189,248,0.30);
        border-radius:14px;
        background:rgba(30,58,95,0.55);
        padding:12px 16px;
        margin-bottom:10px;
    ">
        <div style="
            color:#38BDF8;
            font-size:0.76rem;
            font-weight:900;
            letter-spacing:0.10em;
            text-transform:uppercase;
            margin-bottom:4px;
        ">
            Journey Log
        </div>

        <div style="
            color:#E2E8F0;
            font-size:0.92rem;
            line-height:1.4;
        ">
            Record of observations collected during this investigation.
        </div>
    </div>
    """
)

with st.expander("View Full Journey Log", expanded=False):
    render_journey_log_html(mission_log_df)

render_footer()

