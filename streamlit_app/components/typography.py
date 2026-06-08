"""
Reusable typography helpers for the European Strategy Atlas Streamlit app.

Rule:
- Use this file to render semantic text elements.
- Use atlas_theme.css to style the CSS classes.
- Do not hardcode font sizes inside page files.
"""

from __future__ import annotations

import html
from typing import Iterable

import streamlit as st


def _safe(text: str) -> str:
    """Escape text before inserting into HTML."""
    return html.escape(str(text))


def render_page_title(title: str, subtitle: str | None = None) -> None:
    """Render the main page title / question."""
    subtitle_html = (
        f"<div class='atlas-page-subtitle'>{_safe(subtitle)}</div>"
        if subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="atlas-page-title-block">
            <h1 class="atlas-page-title">{_safe(title)}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(
    number: str | int | None,
    title: str,
    subtitle: str | None = None,
) -> None:
    """Render a major section heading."""
    number_html = (
        f"<div class='atlas-section-number'>{_safe(number)}</div>"
        if number is not None
        else ""
    )

    subtitle_html = (
        f"<div class='atlas-section-subtitle'>{_safe(subtitle)}</div>"
        if subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="atlas-section-title-block">
            {number_html}
            <div>
                <h2 class="atlas-section-title">{_safe(title)}</h2>
                {subtitle_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card_title(title: str, subtitle: str | None = None) -> None:
    """Render a card title."""
    subtitle_html = (
        f"<div class='atlas-card-subtitle'>{_safe(subtitle)}</div>"
        if subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="atlas-card-title-block">
            <h3 class="atlas-card-title">{_safe(title)}</h3>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_body(text: str) -> None:
    """Render readable body text."""
    st.markdown(
        f"<p class='atlas-body-text'>{_safe(text)}</p>",
        unsafe_allow_html=True,
    )


def render_label(text: str) -> None:
    """Render small uppercase label text."""
    st.markdown(
        f"<div class='atlas-label'>{_safe(text)}</div>",
        unsafe_allow_html=True,
    )


def render_metric(value: str | int | float, label: str | None = None) -> None:
    """Render a metric value with optional label."""
    label_html = (
        f"<div class='atlas-metric-label'>{_safe(label)}</div>"
        if label
        else ""
    )

    st.markdown(
        f"""
        <div class="atlas-metric-block">
            <div class="atlas-metric-value">{_safe(value)}</div>
            {label_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_question(
    number: str | int,
    question: str,
    context: str | None = None,
) -> None:
    """Render numbered investigation question."""
    context_html = (
        f"<div class='atlas-question-context'>{_safe(context)}</div>"
        if context
        else ""
    )

    st.markdown(
        f"""
        <div class="atlas-question-block">
            <div class="atlas-question-number">Question { _safe(number) }</div>
            <div class="atlas-question-text">{_safe(question)}</div>
            {context_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_list(
    title: str,
    items: Iterable[str],
    variant: str = "neutral",
) -> None:
    """
    Render scannable bullet insights.

    variant options expected in CSS:
    - neutral
    - advantage
    - constraint
    - risk
    """
    items_html = "".join(
        f"<li>{_safe(item)}</li>"
        for item in items
        if str(item).strip()
    )

    st.markdown(
        f"""
        <div class="atlas-insight-list atlas-insight-{_safe(variant)}">
            <div class="atlas-insight-title">{_safe(title)}</div>
            <ul>
                {items_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_caption(text: str) -> None:
    """Render chart caption / note."""
    st.markdown(
        f"<div class='atlas-caption'>{_safe(text)}</div>",
        unsafe_allow_html=True,
    )


def render_subsection_title(title: str) -> None:
    """Render a subsection heading."""
    st.markdown(
        f"""
        <div class="atlas-subsection-title">
            {_safe(title)}
        </div>
        """,
        unsafe_allow_html=True,
    )


    