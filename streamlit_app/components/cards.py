import streamlit as st


def get_delta_color(value: float) -> str:
    if value >= 0.20:
        return "#4ADE80"
    if value <= -0.20:
        return "#F472B6"
    return "#38BDF8"


def render_atlas_card(
    title: str,
    value: str,
    delta_text: str = "",
    status: str = "",
    delta_color: str = "#38BDF8",
    card_class: str = "atlas-gap-card",
) -> None:

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="atlas-gap-title">{title}</div>
            <div class="atlas-gap-score">{value}</div>
            <div class="atlas-gap-delta" style="color:{delta_color};">
                {delta_text}
            </div>
            <div class="atlas-gap-status">
                {status}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_card(
    title: str,
    value: str,
    delta_text: str = "",
    status: str = "",
    card_class: str = "atlas-gap-card atlas-gap-card-top",
) -> None:

    render_atlas_card(
        title=title,
        value=value,
        delta_text=delta_text,
        status=status,
        delta_color="#38BDF8",
        card_class=card_class,
    )


def render_delta_card(
    title: str,
    value: str,
    delta_value: float,
    status: str = "",
) -> None:

    render_atlas_card(
        title=title,
        value=value,
        delta_text=f"Δ {delta_value:+.2f}",
        status=status,
        delta_color=get_delta_color(delta_value),
        card_class="atlas-gap-card",
    )


def render_ai_insight_panel(
    title: str,
    observation: str,
    interpretation: str,
    limitation: str,
    next_question: str,
) -> None:
    """Reusable AI insight / reflection panel."""

    st.markdown(
        f"""<div class="atlas-ai-panel">
<div class="atlas-ai-title">🤖 {title}</div>
<div class="atlas-ai-label">Observation</div>
<div class="atlas-ai-text">{observation}</div>
<div class="atlas-ai-label">Interpretation</div>
<div class="atlas-ai-text">{interpretation}</div>
<div class="atlas-ai-label">Limitation</div>
<div class="atlas-ai-text">{limitation}</div>
<div class="atlas-ai-label">Next Question</div>
<div class="atlas-ai-text">{next_question}</div>
</div>""",
        unsafe_allow_html=True,
    )


    

