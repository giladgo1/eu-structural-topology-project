"""
p1_country_explorer.py

Purpose
-------
Page 1 of the European Strategy Atlas.

This page will eventually answer:

"What makes this country unique?"

Current development stage
-------------------------
Minimal Germany-first prototype.

Goal:
- verify that the app can import utility functions
- load real country profile data
- display identity, family, archetype, strongest dimension, weakest dimension

This is NOT the final layout.
This is the first production test of the data layer.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import pandas as pd
import textwrap
from pathlib import Path
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

header_col1, header_col2, header_col3, header_col_ref_country, header_col4, header_col5 = st.columns(
    [1.25, 1.05, 1.15, 1.15, 0.9, 0.85],
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

with header_col5:
    st.html(
        """
        <div class="p1-context-card p1-mission-button">
            ▣ Mission Log
        </div>
        """
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
# LOAD COUNTRY PROFILE EARLY FOR KPI RIBBON
# =============================================================================

country_profile = load_country_profile(selected_country)



# -----------------------------
# Full Width KPI Ribbon
# -----------------------------

innovation_score = country_profile["dimensions"].get(
    "Innovation Capacity", 0
)

sustainability_score = country_profile["dimensions"].get(
    "Sustainability Capacity", 0
)

fiscal_score = country_profile["dimensions"].get(
    "Fiscal Flexibility", 0
)

security_score = country_profile["dimensions"].get(
    "Security Reprioritization", 0
)

st.html(
    f"""
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">ARCHETYPE</div>
            <div class="p1-kpi-main">{country_profile['archetype']}</div>
            <div class="p1-kpi-sub">Why this archetype?</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label">INNOVATION CAPACITY</div>
            <div class="p1-kpi-number">{innovation_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label sustainability">SUSTAINABILITY</div>
            <div class="p1-kpi-number">{sustainability_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label fiscal">FISCAL FLEXIBILITY</div>
            <div class="p1-kpi-number">{fiscal_score:+.2f}</div>
            <div class="p1-kpi-sub">EU-relative score</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label security">SECURITY</div>
            <div class="p1-kpi-number">{security_score:+.2f}</div>
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
# START BELOW FULL-WIDTH RIBBON
# =============================================================================

left_nav_col, main_col, right_log_col = st.columns([0.95, 5.3, 1.35], gap="medium")

 
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
    # SECTION 01 — COUNTRY SNAPSHOT
    # =============================================================================

    st.header(
        f"01 — Who is {selected_country} today?"
    )

    st.info(
        f"""
### {selected_country}

**Archetype:** {country_profile['archetype']}  
**Family:** {country_profile['family']}  

**Strongest capability:** {country_profile['strongest_dimension']} ({country_profile['strongest_value']:.2f})  
**Main constraint:** {country_profile['weakest_dimension']} ({country_profile['weakest_value']:.2f})
"""
    )

    st.subheader("Structural Snapshot")

    section_left, section_center, section_right = st.columns(
        [1.15, 2.0, 1.15]
    )

    with section_left:
        st.markdown("**Key strengths**")

        for _, row in strengths_df.iterrows():
            st.success(
                f"{row['dimension']}  \n"
                f"{row['gap_label']} ({row['gap']:+.2f})"
            )

        st.info(
            f"""
**About this archetype**

{country_profile['archetype']}

Countries in this pathway typically combine:

• strong industrial capability  
• innovation investment  
• export competitiveness

Typical challenge:

Balancing innovation strength with long-term fiscal flexibility.
"""
        )

    with section_center:
        radar_chart = create_dimension_radar_chart(
            country_profile
        )

        st.plotly_chart(
            radar_chart,
            use_container_width=True
        )

    with section_right:
        st.markdown("**Key constraints**")

        for _, row in constraints_df.iterrows():
            st.warning(
                f"{row['dimension']}  \n"
                f"{row['gap_label']} ({row['gap']:+.2f})"
            )

        st.info(
            f"""
**Family context**

{country_profile['family']}

Countries in the same family tend to share:

• structural investment patterns  
• similar development priorities  
• related strategic tradeoffs

Future version:

Explore family members and compare pathways.
"""
        )

    st.info(
        f"""
**What's next?**

Why is {selected_country} part of this structural family?

Look at the evolution section to see whether the profile is stable or changing.
"""
    )



    # =============================================================================
    # SECTION 02 — COUNTRY EVOLUTION
    # =============================================================================

    st.header(
        f"02 — How did {selected_country} become this way?"
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

    st.header(
        f"03 — How does {selected_country} compare?"
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.info(
            f"""
**Compared With**

{comparison_reference_name}
"""
        )

    with summary_col2:
        st.success(
            f"""
**Largest Advantage**

{largest_gain_dimension}

{largest_gain_value:+.2f}
"""
        )

    with summary_col3:
        st.warning(
            f"""
**Largest Constraint**

{largest_constraint_dimension}

{largest_constraint_value:+.2f}
"""
        )

    comparison_left, comparison_right = st.columns([3, 1])

    with comparison_left:
        st.caption(
            f"Compared with: {comparison_profile['reference_name']}"
        )

        comparison_rows = list(gap_df.iterrows())

        for i in range(0, len(comparison_rows), 4):
            row_items = comparison_rows[i:i + 4]
            cols = st.columns(len(row_items))

            for col, (_, row) in zip(cols, row_items):
                with col:
                    st.metric(
                        label=row["dimension"],
                        value=f"{row['country_value']:.2f}",
                        delta=f"{row['gap']:+.2f}",
                    )

                    st.markdown(
                        f"**{row['gap_label']}**"
                    )

    with comparison_right:
        st.info(
            f"""
**Bottom Line**

{comparison_bottom_line}
"""
        )

        st.info(
            f"""
**Investigation Question**

Which dimensions differ most from the reference?

Use the comparison grid to identify where {selected_country} is strongest and where the largest structural gaps remain.
"""
        )
      # =============================================================================
    # SECTION 04 — WHAT STANDS OUT?
    # =============================================================================

    st.header("04 — What stands out?")

    section04_left, section04_right = st.columns([1.15, 1])

    with section04_left:
        st.subheader("Key strengths")

        for _, row in strengths_df.iterrows():
            st.success(
                f"{row['dimension']} — "
                f"{row['gap_label']} "
                f"({row['gap']:+.2f})"
            )

        st.subheader("Key constraints")

        for _, row in constraints_df.iterrows():
            st.warning(
                f"{row['dimension']} — "
                f"{row['gap_label']} "
                f"({row['gap']:+.2f})"
            )

    with section04_right:
        st.subheader("Strategic Summary")

        strongest_dimension = strengths_df.iloc[0]["dimension"]
        strongest_gap = strengths_df.iloc[0]["gap"]

        weakest_dimension = constraints_df.iloc[0]["dimension"]
        weakest_gap = constraints_df.iloc[0]["gap"]

        st.info(
            f"""
**Key Observation**

Strongest advantage:  
{strongest_dimension} ({strongest_gap:+.2f})

Main constraint:  
{weakest_dimension} ({weakest_gap:+.2f})

---

**Structural Interpretation**

{selected_country} shows an uneven structural profile.

The strategic question is how to build on its strongest dimension without worsening its main constraint.

---

**AI-generated dynamic insights**

Coming soon.
"""
        )
    # =============================================================================
    # SECTION 05 — WHERE NEXT?
    # =============================================================================

    st.header("05 — Where would you like to go next?")

    st.caption(
        "Choose the next step in your exploration journey."
    )

    next_col1, next_col2, next_col3 = st.columns(3)

    with next_col1:
        st.subheader("Explore tradeoffs")
        st.write(
            "Investigate relationships between structural dimensions "
            "and strategic priorities."
        )
        st.button("Go to Tradeoff Explorer")

    with next_col2:
        st.subheader("Build a strategy")
        st.write(
            "Experiment with investment priorities and observe possible "
            "structural tradeoffs."
        )
        st.button("Go to Strategic Choices")

    with next_col3:
        st.subheader("Compare countries")
        st.write(
            "Explore how another country follows a different structural pathway."
        )
        st.button("Compare Another Country")

# =============================================================================
# PAGE FOOTER
# =============================================================================

st.divider()

footer_left, footer_right = st.columns([1, 1])

with footer_left:

    st.info(
        """
**European Strategy Atlas — MVP v0.1**

Created by Gilad Gotesman

Educational exploration of European structural pathways,
strategic tradeoffs, and transformation patterns using public European data.
"""
    )

with footer_right:

    st.info(
        """
**Key Assumptions & Constraints**

• Results are exploratory, not predictive.

• Relationships do not imply causality.

• Structural dimensions are composite indicators based on selected public datasets and design assumptions.

• Country profiles are strategic lenses, not rankings.

• Results should not be interpreted as policy recommendations.
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



# =============================================================================
# DEBUG / DEVELOPMENT VIEW
# =============================================================================

with st.expander("Developer view: full country profile object"):
    st.write(country_profile)

with st.expander("Developer view: country story object"):
    st.write(country_story)





