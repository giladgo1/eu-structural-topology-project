"""
p9_frame_test.py

Purpose
-------
Temporary development page for testing the shared Atlas frame.

This page is not part of the MVP journey.
It exists only to test shared layout, cards, side panels, footer, CTA buttons,
and future sticky context behavior before applying them to P2–P5 or refactoring P1.
"""

from pathlib import Path

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
# PAGE CONFIG
# =============================================================================

st.markdown("## FRAME TEST — Shared Atlas Structure")
st.caption(
    "Temporary page. Use this to test repeated layout blocks before building P2–P5."
)


# =============================================================================
# TOP CONTEXT TEST — P1 STYLE
# =============================================================================

top_col1, top_col2, top_col3, top_col_ref_country, top_col4 = st.columns(
    [1.8, 1.05, 1.15, 1.15, 0.9],
    gap="medium",
)

with top_col1:
    st.html(
        """
        <div class="p1-brand">
            <div class="p1-logo">✦</div>
            <div>
                <div class="p1-brand-title">EUROPEAN<br>STRATEGY ATLAS</div>
                <div class="p1-brand-subtitle">Shared frame test<br>P2–P5 foundation.</div>
            </div>
        </div>
        """
    )

with top_col2:
    selected_country = st.selectbox(
        "Country",
        options=["Germany", "Sweden", "Romania", "Italy", "Poland"],
        index=0,
    )

with top_col3:
    selected_reference = st.selectbox(
        "Reference",
        options=["EU Average", "Family Average", "Another Country"],
        index=0,
    )

with top_col_ref_country:
    if selected_reference == "Another Country":
        st.selectbox(
            "Reference Country",
            options=["Sweden", "Romania", "Italy", "Poland"],
            index=0,
        )
    else:
        st.text_input(
            "Reference Country",
            value="-----------",
            disabled=True,
        )

with top_col4:
    st.radio(
        "View Mode",
        options=["Relative", "Absolute"],
        horizontal=True,
        index=0,
    )


# =============================================================================
# KPI / CONTEXT RIBBON TEST
# =============================================================================

st.html(
    """
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">CURRENT PAGE</div>
            <div class="p1-kpi-main">Frame Test</div>
            <div class="p1-kpi-sub">Reusable layout check</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#4ADE80;">POSITIVE SIGNAL</div>
            <div class="p1-kpi-number" style="color:#4ADE80;">+0.62</div>
            <div class="p1-kpi-sub">Semantic green</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F472B6;">CONSTRAINT</div>
            <div class="p1-kpi-number" style="color:#F472B6;">-0.53</div>
            <div class="p1-kpi-sub">Semantic magenta</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#38BDF8;">NEUTRAL</div>
            <div class="p1-kpi-number" style="color:#38BDF8;">0.02</div>
            <div class="p1-kpi-sub">Semantic blue</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F59E0B;">WARNING</div>
            <div class="p1-kpi-number" style="color:#F59E0B;">!</div>
            <div class="p1-kpi-sub">Challenge signal</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label">FRAME STATUS</div>
            <div class="p1-kpi-main">Reusable</div>
            <div class="p1-kpi-sub">Test before extraction</div>
        </div>
    </div>
    """
)


# =============================================================================
# THREE-COLUMN FRAME TEST
# =============================================================================

left_col, main_col, right_col = st.columns(
    [0.85, 5.4, 1.15],
    gap="medium",
)

sections = [
    ("01", "FRAME", "Test page shell."),
    ("02", "CARDS", "Test card components."),
    ("03", "LAYOUT", "Test grid behavior."),
    ("04", "CTA", "Test next actions."),
]

with left_col:
    render_left_rail_placeholder(
        page_number=9,
        page_title="Frame Test",
        sections=sections,
    )

with main_col:
    render_section_title(
        number="01",
        title="Shared frame test",
        subtitle="This section tests whether the Atlas frame can support P2–P5 without touching P1.",
    )

    card_a, card_b, card_c = st.columns(3)

    with card_a:
        render_hero_card(
            title="Hero Card",
            value="Blue Frame",
            delta_text="Used for summaries",
            status="Reusable",
        )

    with card_b:
        render_delta_card(
            title="Positive Delta",
            value="Advantage",
            delta_value=0.62,
            status="Semantic green",
        )

    with card_c:
        render_delta_card(
            title="Constraint Delta",
            value="Tradeoff",
            delta_value=-0.53,
            status="Semantic magenta",
        )

    render_section_title(
        number="02",
        title="Card grid behavior",
        subtitle="Use this to check spacing, fills, borders, typography, and repeated card structure.",
    )

    grid_cols = st.columns(4)

    for idx, col in enumerate(grid_cols, start=1):
        with col:
            render_atlas_card(
                title=f"Test Card {idx}",
                value="Stable",
                delta_text="Shared style",
                status="No page-specific CSS",
            )

    render_section_title(
        number="03",
        title="Placeholder hero visual",
        subtitle="This mimics a future P2 scatter / P3 strategy / P4 challenge chart area.",
    )

    with st.container(border=True):
        st.markdown(
            """
### Hero Visual Placeholder

This area should later hold the main page visual.

Examples:

- P2 scatter plot
- P3 consequence cards
- P4 challenge impact
- P5 reflection journey

The frame should work before real charts are added.
"""
        )

    render_section_title(
        number="04",
        title="Next action area",
        subtitle="CTA cards and buttons should reuse the same visual style across pages.",
    )

    cta1, cta2, cta3 = st.columns(3)

    with cta1:
        with st.container(border=True):
            render_hero_card(
                title="Next",
                value="Build P2",
                delta_text="Use this frame",
                status="Proceed after test passes",
            )
            st.button(
                "→ Build P2 Skeleton",
                disabled=True,
                use_container_width=True,
            )

    with cta2:
        with st.container(border=True):
            render_hero_card(
                title="Later",
                value="Sticky Header",
                delta_text="Solve once",
                status="Apply to all pages",
            )
            st.button(
                "→ Test Sticky Frame",
                disabled=True,
                use_container_width=True,
            )

    with cta3:
        with st.container(border=True):
            render_hero_card(
                title="Later",
                value="Mission Log",
                delta_text="Shared component",
                status="Do not overbuild now",
            )
            st.button(
                "→ Test Mission Log",
                disabled=True,
                use_container_width=True,
            )

    render_footer()

with right_col:
    render_mission_log_placeholder(
        current_mission="Test the shared Atlas frame.",
        latest_learning="P1 patterns are being converted into reusable blocks.",
        suggested_next="If this page renders correctly, build the P2 skeleton using this frame.",
    )