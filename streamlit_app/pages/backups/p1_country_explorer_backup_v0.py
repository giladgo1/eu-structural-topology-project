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
# LEFT COLUMN — JOURNEY NAVIGATOR PLACEHOLDER
# =============================================================================

# =============================================================================
# CENTER COLUMN — MAIN EXPLORER
# =============================================================================


st.title("European Strategy Atlas")

st.caption(
    "Explore structural strengths, tradeoffs and strategic pathways across European countries."
)

st.divider()

# =============================================================================
# EXPLORATION CONTROLS
# =============================================================================

all_countries = sorted(
    profiles_df["country_name"].unique()
)

country_options = order_countries(
    all_countries,
    PRIORITY_COUNTRIES,
)

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        index=country_options.index(DEFAULT_COUNTRY),
    )

with control_col2:

    reference_options = [
        "EU Average",
        "Family Average",
        "Another Country",
    ]

    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        index=reference_options.index(DEFAULT_REFERENCE_TYPE),
    )

reference_country_options = order_countries(
    all_countries,
    PRIORITY_COUNTRIES,
)

with control_col3:

    if selected_reference == "Another Country":

        reference_country = st.selectbox(
            "Reference Country",
            options=reference_country_options,
            index=reference_country_options.index(DEFAULT_REFERENCE_COUNTRY),
        )

    else:

        reference_country = None

        st.text_input(
            "Reference Country",
            value="-----------",
            disabled=True,
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

country_year_df = load_country_year()

country_timeline = build_country_timeline(
    country_name=selected_country,
    country_year_df=country_year_df
)
country_name = country_profile["country"]

# =============================================================================
# STRENGTH / CONSTRAINT EXTRACTION
# =============================================================================

strengths_df = get_key_strengths(gap_df)

constraints_df = get_key_constraints(gap_df)

# =============================================================================
# COUNTRY STORY
# =============================================================================

st.header(
    f"01 — Who is {country_name} today?"
)

st.info(
    f"""
### {country_name}

**Archetype:** {country_profile['archetype']}

**Family:** {country_profile['family']}

---

**Strongest capability**

{country_profile['strongest_dimension']}
({country_profile['strongest_value']:.2f})

**Main constraint**

{country_profile['weakest_dimension']}
({country_profile['weakest_value']:.2f})
"""
)



# =============================================================================
# STRUCTURAL SNAPSHOT — V2
# =============================================================================

st.subheader("Structural Snapshot")

snapshot_left, snapshot_center, snapshot_right = st.columns(
    [1.2, 2.2, 1.2]
)

with snapshot_left:
    st.markdown("**Key strengths**")

    for _, row in strengths_df.iterrows():
        st.success(
            f"{row['dimension']}  \n"
            f"{row['gap_label']} ({row['gap']:+.2f})"
        )

with snapshot_center:
    radar_chart = create_dimension_radar_chart(
        country_profile
    )

    st.plotly_chart(
        radar_chart,
        use_container_width=True
    )

with snapshot_right:
    st.markdown("**Key constraints**")

    for _, row in constraints_df.iterrows():
        st.warning(
            f"{row['dimension']}  \n"
            f"{row['gap_label']} ({row['gap']:+.2f})"
        )

st.info(
    f"{country_name} is shown as an EU-relative structural profile. "
    f"The radar highlights the country’s strategic shape across seven dimensions."
)

# =============================================================================
# DIMENSION VALUES — CARD GRID
# =============================================================================

st.subheader("Seven Structural Dimensions")

dimension_items = list(
    country_profile["dimensions"].items()
)

for i in range(0, len(dimension_items), 3):
    dim_cols = st.columns(3)

    for col, (dimension_name, dimension_value) in zip(
        dim_cols,
        dimension_items[i:i + 3]
    ):
        with col:
            st.markdown(
                f"""
                <div class="atlas-card">
                    <div class="atlas-card-title">{dimension_name}</div>
                    <div class="atlas-card-value">{dimension_value:.2f}</div>
                    <div class="atlas-muted">EU-relative score</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# =============================================================================
# DEBUG / DEVELOPMENT VIEW
# =============================================================================

with st.expander("Developer view: full country profile object"):
    st.write(country_profile)

with st.expander("Developer view: country story object"):
    st.write(country_story)

# =============================================================================
# SECTION 02 — COUNTRY EVOLUTION
# =============================================================================

st.header(
    f"How did {country_name} become this way?"
)

timeline_chart = create_country_timeline_chart(
    country_timeline,
    selected_country
)

st.plotly_chart(
    timeline_chart,
    use_container_width=True
)



st.info(
    "Scores are EU-relative structural indices. "
    "0 = EU average. Positive values indicate above-average structural performance."
)
# =============================================================================
# SECTION 03 — DIMENSION GAP ANALYSIS
# =============================================================================

st.header(
    f"How does {country_name} compare?"
)

st.caption(
    f"Compared with: {comparison_profile['reference_name']}"
)

# Show comparison cards in rows of 3.
# This avoids 7 tiny columns and keeps each interpretation label
# directly under the correct dimension.

comparison_rows = list(gap_df.iterrows())

for i in range(0, len(comparison_rows), 3):
    cols = st.columns(3)

    for col, (_, row) in zip(cols, comparison_rows[i:i + 3]):
        with col:
            st.metric(
                label=row["dimension"],
                value=f"{row['country_value']:.2f}",
                delta=f"{row['gap']:+.2f}"
            )

            st.markdown(
                f"**{row['gap_label']}**"
            )


            # =============================================================================
# =============================================================================
# SECTION 04 — WHAT STANDS OUT?
# =============================================================================

st.header("What stands out?")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Key strengths")

    for _, row in strengths_df.iterrows():
        st.success(
            f"{row['dimension']} — "
            f"{row['gap_label']} "
            f"({row['gap']:+.2f})"
        )

with right_col:
    st.subheader("Key constraints")

    for _, row in constraints_df.iterrows():
        st.warning(
            f"{row['dimension']} — "
            f"{row['gap_label']} "
            f"({row['gap']:+.2f})"
        )



      


st.subheader("AI Summary")

st.info(
    """
🧠 **Coming Soon**

Future versions of the Atlas will generate:

• strategic pathway observations

• tradeoff explanations

• country-specific structural insights

• family and archetype interpretation

based on the selected country and reference.
"""
)



# =============================================================================
# SECTION 05 — WHERE NEXT?
# =============================================================================

st.header("Where would you like to go next?")

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