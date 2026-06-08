import streamlit as st


def render_left_rail_placeholder(page_number: int, page_title: str, sections: list[tuple[str, str, str]]):
    st.html(
        f"""
        <div class="p1-left-nav-test">
            <div class="p1-nav-label">YOUR JOURNEY<br>ON PAGE {page_number}</div>
        """
    )

    for idx, (number, title, subtitle) in enumerate(sections):
        active_class = "active" if idx == 0 else ""
        st.html(
            f"""
            <div class="p1-nav-item {active_class}">
                <div class="p1-nav-number">{number}</div>
                <div>
                    <div class="p1-nav-title">{title}</div>
                    <div class="p1-nav-sub">{subtitle}</div>
                </div>
            </div>
            """
        )

    st.html("</div>")


def render_mission_log_placeholder(
    current_mission: str,
    latest_learning: str = "This page will capture the latest learning.",
    suggested_next: str = "Continue exploration.",
):
    st.markdown("### Mission Log")

    st.info(
        f"""
**Current Mission**

{current_mission}
"""
    )

    st.success(
        f"""
**Latest Learning**

{latest_learning}
"""
    )

    st.info(
        f"""
**Suggested Next Step**

{suggested_next}
"""
    )

    st.markdown("### Journey Summary")

    st.markdown(
        """
✓ Current page started  
○ Evidence reviewed  
○ Interpretation captured  
○ Next step selected
"""
    )


def render_footer():
    st.markdown("<br>", unsafe_allow_html=True)

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