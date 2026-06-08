"""
p1_country_explorer.py

Purpose
-------
Page 1 of the European Strategy Atlas.

This page answers:

"What makes this country unique?"

Current development stage
-------------------------
Full P1 layout stabilization.

Goal:
- preserve the approved Country Explorer structure
- support country + reference comparison
- show identity, evolution, comparison, strengths, constraints, and next steps
- prepare reusable visual patterns for P2–P5

Deferred:
- sticky header final solution
- Mission Log component extraction
"""
# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import pandas as pd
import textwrap
from pathlib import Path
from components.typography import (
    render_section_title,
    render_card_title,
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


from components.typography import render_section_title
from components.cards import (
    render_atlas_card,
    render_hero_card,
    render_delta_card,
)

# =============================================================================
# LOAD GLOBAL CSS
# =============================================================================

def load_css():
    """
    Load Atlas CSS theme.
    """

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


# =============================================================================
# LOAD THEME
# =============================================================================

load_css()


# =============================================================================
# LOAD BASE DATA
# =============================================================================

profiles_df = load_profiles()
families_df = load_families()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def order_countries(country_list, priority_countries):
    """
    Return countries in UX-friendly order.

    Priority countries appear first.
    All other countries appear alphabetically.

    Duplicates are removed automatically.
    """

    priority = []

    for country in priority_countries:
        if country in country_list and country not in priority:
            priority.append(country)

    remaining = sorted(
        [
            country
            for country in country_list
            if country not in priority
        ]
    )

    return priority + remaining



# =============================================================================
# =============================================================================

# =============================================================================
# PAGE 1 — STICKY CONTEXT RIBBON + FULL WIDTH KPI RIBBON
# =============================================================================

all_countries = sorted(profiles_df["country_name"].unique())

country_options = order_countries(
    all_countries,
    PRIORITY_COUNTRIES,
)

# -----------------------------
# Functional selection state
# -----------------------------

all_countries = sorted(
    profiles_df["country_name"].unique()
)

country_options = order_countries(
    all_countries,
    PRIORITY_COUNTRIES,
)

reference_options = [
    "EU Average",
    "Family Average",
    "Another Country",
]

reference_country_options = order_countries(
    all_countries,
    PRIORITY_COUNTRIES,
)
# =============================================================================
# STICKY HEADER CONTAINER
# =============================================================================

st.html(
    """
    <div class="p1-sticky-header-marker"></div>
    """
)
# -----------------------------
# Header / Context Ribbon
# -----------------------------

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
        index=country_options.index(DEFAULT_COUNTRY),
    )

with header_col3:
    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        index=reference_options.index(DEFAULT_REFERENCE_TYPE),
    )

with header_col_ref_country:
    if selected_reference == "Another Country":
        filtered_reference_options = [
            country
            for country in reference_country_options
            if country != selected_country
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
        st.text_input(
            "Reference Country",
            value="-----------",
            disabled=True,
        )

with header_col4:
    view_mode = st.radio(
        "View Mode",
        options=["Relative", "Absolute"],
        horizontal=True,
        index=0,
    )




# =============================================================================
# TOP DISCLAIMER
# =============================================================================

st.info(
    """
**Important**

The Atlas is designed to explore structural pathways, tradeoffs, and strategic patterns across European countries.

It is an educational and exploratory tool, not a forecasting model.

Observed relationships should be interpreted as patterns rather than evidence of causality.
"""
)



# =============================================================================
# SNAPSHOT RIBBON — COUNTRY FACTS PLACEHOLDER
# =============================================================================
st.html(
    """
    <div class="p1-snapshot-ribbon">
        <div class="p1-snapshot-title">COUNTRY SNAPSHOT</div>
        <div class="p1-snapshot-card">
            <span>Population</span>
            <strong>—</strong>
        </div>
        <div class="p1-snapshot-card">
            <span>GDP / capita</span>
            <strong>—</strong>
        </div>
        <div class="p1-snapshot-card">
            <span>Debt</span>
            <strong>—</strong>
        </div>
        <div class="p1-snapshot-card">
            <span>Median Age</span>
            <strong>—</strong>
        </div>
        <div class="p1-snapshot-card">
            <span>EU Since</span>
            <strong>—</strong>
        </div>
    </div>
    """
)


# =============================================================================
# SHARED SEMANTIC COLOR HELPER
# =============================================================================

def get_delta_color(value):
    if value >= 0.20:
        return "#4ADE80"
    if value <= -0.20:
        return "#F472B6"
    return "#38BDF8"


# =============================================================================
# LOAD COUNTRY PROFILE EARLY FOR KPI RIBBON
# =============================================================================

country_profile = load_country_profile(selected_country)



# -----------------------------
# Full Width KPI Ribbon
# -----------------------------

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
            <div class="p1-kpi-sub">Why this archetype?</div>
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
            <div class="p1-kpi-sub">View family members →</div>
        </div>
    </div>
    """
)

 
# =============================================================================
# LOAD COUNTRY PROFILE
# =============================================================================

# For the first P1 implementation we hardcode Germany.
# Later this will become a country selector.

country_profile = load_country_profile(
    selected_country
)
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

elif selected_reference == "Another Country":

    comparison_profile = build_country_reference_profile(
        country_profile=country_profile,
        reference_country_name=reference_country,
        profiles_df=profiles_df,
    ) 
gap_df = build_dimension_gap_table(
    comparison_profile
)

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
    f"{selected_country} performs relatively better in "
    f"{largest_gain_dimension}, "
    f"but trails its reference in "
    f"{largest_constraint_dimension}."
)

country_year_df = load_country_year()

country_timeline = build_country_timeline(
    country_name=selected_country,
    country_year_df=country_year_df
)
country_name = country_profile["country"]

# =============================================================================
# PAGE 1 — THREE-COLUMN EXPLORATION SHELL TEST
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
                    <div class="p1-nav-title">WHO IS {selected_country.upper()}?</div>
                    <div class="p1-nav-sub">Snapshot of {selected_country} today.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">02</div>
                <div>
                    <div class="p1-nav-title">EVOLUTION OVER TIME</div>
                    <div class="p1-nav-sub">How {selected_country}'s priorities evolved.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">03</div>
                <div>
                    <div class="p1-nav-title">HOW DOES {selected_country.upper()} COMPARE?</div>
                    <div class="p1-nav-sub">Compare to selected reference.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">04</div>
                <div>
                    <div class="p1-nav-title">WHAT STANDS OUT?</div>
                    <div class="p1-nav-sub">Strengths and constraints.</div>
                </div>
            </div>

            <div class="p1-nav-item">
                <div class="p1-nav-number">05</div>
                <div>
                    <div class="p1-nav-title">WHERE NEXT?</div>
                    <div class="p1-nav-sub">Choose next step.</div>
                </div>
            </div>
        </div>
        """
    )

with main_col:
    st.html('<div class="p1-content-shell"></div>')




    # =============================================================================
    # SHARED CARD HELPERS — P1
    # =============================================================================

   

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

    

      # =============================================================================
    # SECTION 01 — COUNTRY SNAPSHOT
    # =============================================================================

    render_section_title(
        number="01",
        title=f"Who is {selected_country} today?",
        subtitle="Start with identity, strengths, constraints, and structural family context.",
    )

    with st.container(border=True, key="identity_card"):
        identity_left, identity_right = st.columns([1, 1])

        with identity_left:
            st.markdown(
                f"""
### {selected_country}

**Archetype:** {country_profile['archetype']}  
**Family:** {country_profile['family']}
"""
            )

        with identity_right:
            st.markdown(
                f"""
### Structural Signal

**Strongest capability:** {country_profile['strongest_dimension']} :green[**({country_profile['strongest_value']:+.2f})**]  
**Main constraint:** {country_profile['weakest_dimension']} :violet[**({country_profile['weakest_value']:+.2f})**]
"""
            )

    render_subsection_title("Structural Snapshot")

    section_left, section_center, section_right = st.columns([1.15, 2.0, 1.15])

    second_strength = strengths_df.iloc[1]
    second_constraint = constraints_df.iloc[1]

    with section_left:
        st.markdown("**Key strengths**")

        for _, row in strengths_df.head(2).iterrows():
            render_gap_html_card(
                title=row["dimension"],
                value=f"▲ Δ {row['gap']:+.2f}",
                delta_text=row["gap_label"],
                status="",
                delta_color=get_delta_color(row["gap"]),
                card_class="atlas-gap-card atlas-s04-strength atlas-s01-compact",
            )

        render_gap_html_card(
            title="About this archetype",
            value=country_profile["archetype"],
            delta_text="Industrial capability · innovation investment · export competitiveness",
            status="Typical challenge: long-term fiscal flexibility.",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top atlas-s01-info-compact",
        )

    with section_center:
        radar_chart = create_dimension_radar_chart(country_profile)
        st.plotly_chart(radar_chart, use_container_width=True)

    with section_right:
        st.markdown("**Key constraints**")

        for _, row in constraints_df.head(2).iterrows():
            render_gap_html_card(
                title=row["dimension"],
                value=f"▼ Δ {row['gap']:+.2f}",
                delta_text=row["gap_label"],
                status="",
                delta_color=get_delta_color(row["gap"]),
                card_class="atlas-gap-card atlas-s04-constraint atlas-s01-compact",
            )

        render_gap_html_card(
            title="Family context",
            value=country_profile["family"],
            delta_text="Shared investment patterns · development priorities · strategic tradeoffs",
            status="Future: compare family members.",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top atlas-s01-info-compact",
        )

    render_gap_html_card(
        title="What's next?",
        value=f"Why is {selected_country} part of this structural family?",
        delta_text="Look at the evolution section to see whether the profile is stable or changing.",
        status="Next step: structural evolution",
        delta_color="#38BDF8",
        card_class="atlas-gap-card atlas-gap-card-top atlas-s01-next",
    )

    # =============================================================================
    # SECTION 02 — COUNTRY EVOLUTION
    # =============================================================================

    render_section_title(
        number="02",
        title=f"How did {selected_country} become this way?",
        subtitle="Trace structural evolution relative to the EU average over time.",
    )

    evolution_chart_col, evolution_text_col = st.columns([2.2, 1])

    with evolution_chart_col:
        timeline_chart = create_country_timeline_chart(
            country_timeline,
            selected_country
        )

        st.plotly_chart(
            timeline_chart,
            use_container_width=True
        )

    with evolution_text_col:
        st.info(
            """
**How to read this**

Scores are EU-relative structural indices.

0 = EU average.

Positive values indicate above-average structural performance.
"""
        )

        st.info(
            f"""
**Investigation question**

What changed after 2020?

Use the timeline to see whether {selected_country}'s profile is stable, shifting, or volatile.
"""
        )

    # =============================================================================
    # SECTION 03 — DIMENSION GAP ANALYSIS
    # =============================================================================

    render_section_title(
        number="03",
        title=f"How does {selected_country} compare?",
        subtitle="Compare the selected country against the chosen reference.",
    )

    

    def render_gap_html_card(title, value, delta_text, status, delta_color, card_class="atlas-gap-card"):
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

    summary_col1, summary_col2, summary_col3 = st.columns([0.85, 1.15, 1.15])

    with summary_col1:
        render_gap_html_card(
            title="Compared With",
            value=comparison_reference_name,
            delta_text="Reference baseline",
            status="Neutral reference",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    with summary_col2:
        render_gap_html_card(
            title="Largest Advantage",
            value=largest_gain_dimension,
            delta_text=f"▲ Δ {largest_gain_value:+.2f}",
            status="Strength",
            delta_color=get_delta_color(largest_gain_value),
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    with summary_col3:
        render_gap_html_card(
            title="Largest Constraint",
            value=largest_constraint_dimension,
            delta_text=f"▼ Δ {largest_constraint_value:+.2f}",
            status="Constraint",
            delta_color=get_delta_color(largest_constraint_value),
            card_class="atlas-gap-card atlas-gap-card-top",
        )

    comparison_left, comparison_right = st.columns([3, 1])

    with comparison_left:
        with st.container(border=True):
            st.markdown(
                f"### Score = {selected_country} EU-relative score · "
                f"Δ = difference vs {comparison_profile['reference_name']}"
            )

            comparison_rows = list(gap_df.iterrows())

            def render_native_gap_card(row, card_key):
                gap_value = row["gap"]
                country_value = row["country_value"]
                dimension = row["dimension"]

                if gap_value >= 0.50:
                    arrow = "▲"
                    status = "Strong Advantage"
                    semantic_type = "strength"
                elif gap_value >= 0.20:
                    arrow = "▲"
                    status = "Advantage"
                    semantic_type = "strength"
                elif gap_value <= -0.50:
                    arrow = "▼"
                    status = "Major Constraint"
                    semantic_type = "constraint"
                elif gap_value <= -0.20:
                    arrow = "▼"
                    status = "Constraint"
                    semantic_type = "constraint"
                else:
                    arrow = "→"
                    status = "Similar to Reference"
                    semantic_type = "info"

                with st.container(key=f"s03_{card_key}_{semantic_type}"):
                    render_gap_html_card(
                        title=dimension,
                        value=f"{country_value:.2f}",
                        delta_text=f"{arrow} Δ {gap_value:+.2f}",
                        status=status,
                        delta_color=get_delta_color(gap_value),
                    )

            top_items = comparison_rows[:4]
            top_cols = st.columns(4)

            for idx, (col, (_, row)) in enumerate(zip(top_cols, top_items)):
                with col:
                    render_native_gap_card(row, f"top_{idx}")

            spacer_left, bottom_1, bottom_2, bottom_3, spacer_right = st.columns(
                [0.25, 1, 1, 1, 0.25]
            )

            bottom_items = comparison_rows[4:]
            bottom_cols = [bottom_1, bottom_2, bottom_3]

            for idx, (col, (_, row)) in enumerate(zip(bottom_cols, bottom_items)):
                with col:
                    render_native_gap_card(row, f"bottom_{idx}")

    with comparison_right:
        with st.container(key="s03_bottom_line"):
            st.info(
                f"""
**Bottom Line**

**Strength:** {largest_gain_dimension}

**Constraint:** {largest_constraint_dimension}

{comparison_bottom_line}
"""
            )

        with st.container(key="s03_question_1"):
            st.info(
                f"""
**Question 1**

Which dimensions differ most from the reference?

- Where is {selected_country} strongest?
- Where is the largest structural constraint?
- Which dimensions are similar to the reference?
"""
            )


        # =============================================================================
    # SECTION 04 — WHAT STANDS OUT?
    # =============================================================================

    render_section_title(
        number="04",
        title="What stands out?",
        subtitle="Summarize the clearest advantages, constraints, and strategic interpretation.",
    )

    section04_left, section04_right = st.columns([1.05, 1])

    with section04_left:
        st.subheader("Key strengths & constraints")

        second_strength = gap_df.sort_values("gap", ascending=False).iloc[1]
        second_constraint = gap_df.sort_values("gap", ascending=True).iloc[1]

        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            render_gap_html_card(
                title=largest_gain_dimension,
                value=f"▲ Δ {largest_gain_value:+.2f}",
                delta_text=f"Advantage vs {comparison_reference_name}",
                status="",
                delta_color=get_delta_color(largest_gain_value),
                card_class="atlas-gap-card atlas-s04-strength atlas-s04-compact",
            )

        with row1_col2:
            render_gap_html_card(
                title=largest_constraint_dimension,
                value=f"▼ Δ {largest_constraint_value:+.2f}",
                delta_text=f"Constraint vs {comparison_reference_name}",
                status="",
                delta_color=get_delta_color(largest_constraint_value),
                card_class="atlas-gap-card atlas-s04-constraint atlas-s04-compact",
            )

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            render_gap_html_card(
                title=second_strength["dimension"],
                value=f"▲ Δ {second_strength['gap']:+.2f}",
                delta_text=f"Advantage vs {comparison_reference_name}",
                status="",
                delta_color=get_delta_color(second_strength["gap"]),
                card_class="atlas-gap-card atlas-s04-strength atlas-s04-compact",
            )

        with row2_col2:
            render_gap_html_card(
                title=second_constraint["dimension"],
                value=f"▼ Δ {second_constraint['gap']:+.2f}",
                delta_text=f"Constraint vs {comparison_reference_name}",
                status="",
                delta_color=get_delta_color(second_constraint["gap"]),
                card_class="atlas-gap-card atlas-s04-constraint atlas-s04-compact",
            )


    with section04_right:
        st.subheader("Strategic Summary")

        render_gap_html_card(
            title="Key Observation",
            value="Structural signal",
            delta_text=f"Strongest advantage: {largest_gain_dimension}",
            status=f"Main constraint: {largest_constraint_dimension}",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top",
        )

        render_gap_html_card(
            title="Structural Interpretation",
            value="Uneven profile",
            delta_text=f"{selected_country} shows an uneven structural profile.",
            status="The strategic question is how to build on its strongest dimension without worsening its main constraint.",
            delta_color="#38BDF8",
            card_class="atlas-gap-card atlas-gap-card-top",
        )
    st.markdown("### AI Insight")

    render_gap_html_card(
    title="AI Insight",
    value="Coming soon...",
    delta_text="",
    status="",
    delta_color="#38BDF8",
    card_class="atlas-gap-card atlas-gap-card-top",
)
       
    # =============================================================================
    # SECTION 05 — WHERE NEXT?
    # =============================================================================

    render_section_title(
        number="05",
        title="Where would you like to go next?",
        subtitle="Continue the exploration through tradeoffs, strategy, or comparison.",
    )

    next_col1, next_col2, next_col3 = st.columns(3)

    with next_col1:
        with st.container(border=True):
            st.info(
                """
**Explore tradeoffs**

Investigate relationships between structural dimensions and strategic priorities.
"""
            )
            st.button("→ Open Tradeoff Explorer", disabled=True, use_container_width=True)

    with next_col2:
        with st.container(border=True):
            st.info(
                """
**Build a strategy**

Experiment with investment priorities and observe possible structural tradeoffs.
"""
            )
            st.button("→ Build a Strategy", disabled=True, use_container_width=True)

    with next_col3:
        with st.container(border=True):
            st.info(
                """
**Compare countries**

Explore how another country follows a different structural pathway.
"""
            )
            st.button("→ Compare Countries", disabled=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # =============================================================================
    # FOOTER — MVP CONTEXT
    # =============================================================================

    footer_left, footer_right = st.columns([1.1, 0.9])

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
        
# =============================================================================
with right_log_col:

    st.markdown("### Mission Log")

    st.info(
        f"""
**Current Mission**

Explore {selected_country}'s structural profile.
"""
    )

    st.success(
    f"""
**Latest Learning**

{selected_country}'s strongest relative advantage is

{largest_gain_dimension}

when compared with the selected reference.
"""
)

    st.success(
    f"""
**Largest Gain**

{largest_gain_dimension}  
{largest_gain_value:+.2f} vs reference
"""
)

    st.warning(
    f"""
**Largest Constraint**

{largest_constraint_dimension}  
{largest_constraint_value:+.2f} vs reference
"""
)

    st.info(
        f"""
**Key Insight**

{selected_country}'s profile is not weak overall.  
It is structurally strong, but uneven.
"""
    )

    st.markdown("### Journey Summary")

    st.markdown(
        """
✓ Snapshot  
✓ Evolution  
✓ Comparison  
✓ Takeaways  
○ Next Step
"""
    )

    
# =============================================================================
# STRENGTH / CONSTRAINT EXTRACTION
# =============================================================================

strengths_df = get_key_strengths(gap_df)

constraints_df = get_key_constraints(gap_df)









