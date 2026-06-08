"""
chart_utils.py

Purpose
-------
Reusable plotting functions for the European Strategy Atlas.

Used by:
- P1 Country Explorer
- P2 Tradeoff Explorer
- P3 Strategic Choices

Current Version
---------------
Contains timeline charts only.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import plotly.express as px
import plotly.graph_objects as go
from utils.app_config import (
    COUNTRY_COLORS,
    DEFAULT_COUNTRY_COLOR,
)

# =============================================================================
# COUNTRY EVOLUTION TIMELINE
# =============================================================================

def create_country_timeline_chart(timeline_df, country_name):
    """
    Create the P1 evolution chart.

    Shows how the selected country's structural dimensions evolve over time.

    Units
    -----
    EU-relative dimension scores.

    Baseline
    --------
    EU Average = 0.

    Interpretation
    --------------
    Positive values = above EU average.
    Negative values = below EU average.
    """

    plot_df = timeline_df.rename(
        columns={
            "dim_innovation_capacity": "Innovation",
            "dim_sustainability_capacity": "Sustainability",
            "dim_social_stability": "Social Stability",
            "dim_fiscal_flexibility": "Fiscal Flexibility",
            "dim_security_reprioritization": "Security",
        }
    )

    plot_df = plot_df[
        [
            "year",
            "Innovation",
            "Sustainability",
            "Social Stability",
            "Fiscal Flexibility",
            "Security",
        ]
    ]

    plot_df = plot_df.melt(
        id_vars="year",
        var_name="Dimension",
        value_name="Score",
    )

    fig = px.line(
        plot_df,
        x="year",
        y="Score",
        color="Dimension",
        markers=True,
        title=None,
    )

    # COVID transition background: 2020–2021.
    # x1=2022 makes the shaded region visually cover both 2020 and 2021.
    fig.add_vrect(
        x0=2020,
        x1=2022,
        fillcolor="rgba(239,68,68,0.08)",
        line_width=0,
        layer="below",
        annotation_text="COVID transition",
        annotation_position="top left",
        annotation_font_size=11,
        annotation_font_color="#FCA5A5",
    )

    # Energy / geopolitical transition background: 2022 onward.
    fig.add_vrect(
        x0=2022,
        x1=2025.5,
        fillcolor="rgba(56,189,248,0.06)",
        line_width=0,
        layer="below",
        annotation_text="Energy transition",
        annotation_position="top left",
        annotation_font_size=11,
        annotation_font_color="#93C5FD",
    )

    # EU baseline.
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="rgba(226,232,240,0.80)",
        annotation_text="EU average = 0",
        annotation_position="top left",
        annotation_font_size=14,
        annotation_font_color="#E2E8F0",
    )

    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",
        margin=dict(
            l=34,
            r=22,
            t=86,
            b=42,
        ),
        font=dict(
            color="#E5E7EB",
            size=12,
        ),
        title=dict(
            text=(
                f"{country_name} Structural Evolution<br>"
                "<span style='font-size:12px;color:#CBD5E1'>"
                "EU-relative dimension scores • EU Average = 0"
                "</span>"
            ),
            font=dict(
                size=22,
                color="#F8FAFC",
            ),
            x=0.01,
            xanchor="left",
            y=0.96,
        ),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=14,
                color="#E2E8F0",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="x unified",
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.10)",
        tickmode="linear",
        dtick=1,
        color="#CBD5E1",
        tickfont=dict(
            size=15,
            color="#E2E8F0",
        ),
        title=None,
    )

    fig.update_yaxes(
        title="EU-relative score",
        title_font=dict(
            size=15,
            color="#E2E8F0",
        ),
        gridcolor="rgba(148,163,184,0.22)",
        zeroline=False,
        color="#CBD5E1",
        tickfont=dict(
            size=15,
            color="#E2E8F0",
        ),
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
    )

    return fig

# =============================================================================
# STRUCTURAL SNAPSHOT RADAR
# =============================================================================

def create_dimension_radar_chart(country_profile):
    """
    Create radar chart for the country structural dimension profile.

    Purpose
    -------
    Used in P1 Section 01.

    Shows structural dimensions relative to the EU average.

    Interpretation
    --------------
    0 = EU average.
    Positive values = above EU average.
    Negative values = below EU average.
    """

    dimensions = country_profile["dimensions"]

    labels = list(dimensions.keys())
    values = list(dimensions.values())

    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    country_color = COUNTRY_COLORS.get(
        country_profile["country"],
        DEFAULT_COUNTRY_COLOR,
    )

    fig = go.Figure()

    # Main country radar shape
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name=country_profile["country"],
            line=dict(
                color="#38BDF8",
                width=1,
                dash="dot",
            ),
            fillcolor=country_color,
            opacity=0.38,
            hovertemplate=(
                "<b>%{theta}</b><br>"
                "EU-relative score: %{r:.2f}<extra></extra>"
            ),
        )
    )

       # EU baseline ring at r = 0
    fig.add_trace(
        go.Scatterpolar(
            r=[0] * len(labels_closed),
            theta=labels_closed,
            mode="lines",
            name="EU Average = 0",
            line=dict(
                color="#38BDF8",
                width=1,
                dash="dot",
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=dict(
            text=(
                "Structural Profile<br>"
                "<span style='font-size:14px;color:#CBD5E1'>"
                "EU-relative dimension scores · EU Average = 0"
                "</span>"
            ),
            font=dict(
                size=16,
                color="#F8FAFC",
            ),
            x=0.5,
            xanchor="center",
            y=0.94,
        ),
        height=500,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(
                tickfont=dict(
                    size=12,
                    color="#F8FAFC",
                ),
                linecolor="rgba(255,255,255,0.20)",
                gridcolor="rgba(255,255,255,0.12)",
            ),
            radialaxis=dict(
                visible=True,
                range=[-1.5, 1.5],
                tickvals=[-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5],
                tickfont=dict(
                    size=11,
                    color="#CBD5E1",
                ),
                gridcolor="rgba(255,255,255,0.18)",
                linecolor="rgba(255,255,255,0.22)",
            ),
        ),
        annotations=[
            dict(
                text="EU = 0 baseline",
                x=0.50,
                y=0.56,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    size=11,
                    color="#38BDF8",
                ),
            )
        ],
        margin=dict(
            l=70,
            r=90,
            t=120,
            b=45,
        ),
    )

    return fig