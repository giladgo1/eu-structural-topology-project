"""
p6_how_it_was_made.py

European Strategy Atlas — How it was made page.

Purpose:
- explain the data analytics process behind the Atlas
- import app data and reproduce key report-style visuals inside Streamlit
- document the route from raw KPIs to dimensions, families, tradeoffs, assumptions, and app logic

Place in:
    streamlit_app/pages/p6_how_it_was_made.py

Expected data folder:
    streamlit_app/data/app/
    or project_root/data/app/
"""

from pathlib import Path
from typing import Optional, Iterable

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from components.typography import render_section_title
from components.page_frame import render_footer


# =============================================================================
# PAGE CONFIG / CSS
# =============================================================================

def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
<style>
.report-hero {
    border-radius: 30px;
    padding: 42px 46px;
    margin-bottom: 34px;
    background:
        radial-gradient(circle at 84% 10%, rgba(56,189,248,0.20), transparent 34%),
        linear-gradient(135deg, rgba(15,23,42,0.98), rgba(15,23,42,0.76));
    border: 1px solid rgba(56,189,248,0.30);
    box-shadow: 0 28px 70px rgba(0,0,0,0.24);
}
.report-kicker {
    color: #38BDF8;
    font-size: 0.78rem;
    font-weight: 950;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.report-title {
    color: #F8FAFC;
    font-size: 2.85rem;
    line-height: 1.05;
    font-weight: 950;
    letter-spacing: -0.035em;
    max-width: 860px;
}
.report-title span { color: #38BDF8; }
.report-body {
    color: #E2E8F0;
    font-size: 1.08rem;
    line-height: 1.65;
    margin-top: 20px;
    max-width: 1050px;
}
.report-metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-top: 28px;
}
.report-metric {
    min-height: 86px;
    border-radius: 18px;
    padding: 16px;
    background: rgba(2,6,23,0.56);
    border: 1px solid rgba(148,163,184,0.22);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.report-metric-num {
    color: #38BDF8;
    font-size: 1.45rem;
    font-weight: 950;
    line-height: 1.05;
}
.report-metric-label {
    color: #E2E8F0;
    font-size: 0.92rem;
    font-weight: 750;
    margin-top: 6px;
}
.report-panel {
    border-radius: 24px;
    padding: 26px;
    background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.76));
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 42px rgba(0,0,0,0.20);
    height: 100%;
}
.report-panel-blue { border-left: 5px solid #38BDF8; }
.report-panel-purple { border-left: 5px solid #8B5CF6; }
.report-panel-amber { border-left: 5px solid #F59E0B; }
.report-panel-green { border-left: 5px solid #22C55E; }
.report-panel-red { border-left: 5px solid #EF4444; }
.report-label {
    color: #38BDF8;
    font-size: 0.76rem;
    font-weight: 950;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.report-card-title {
    color: #F8FAFC;
    font-size: 1.28rem;
    font-weight: 950;
    line-height: 1.22;
    margin-bottom: 10px;
}
.report-card-body {
    color: #CBD5E1;
    font-size: 1.02rem;
    line-height: 1.58;
}
.report-card-body b { color: #F8FAFC; }
.report-bullets {
    color: #CBD5E1;
    font-size: 1.0rem;
    line-height: 1.72;
    margin: 0;
    padding-left: 1.15rem;
}
.report-flow {
    display: flex;
    align-items: stretch;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 12px;
}
.report-flow-node {
    flex: 1 1 128px;
    min-height: 96px;
    border-radius: 18px;
    padding: 16px;
    background: rgba(2,6,23,0.52);
    border: 1px solid rgba(56,189,248,0.25);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.report-flow-node strong {
    color: #F8FAFC;
    font-size: 1.02rem;
    display: block;
}
.report-flow-node span {
    color: #94A3B8;
    font-size: 0.86rem;
    margin-top: 6px;
}
.report-arrow {
    color: #38BDF8;
    font-size: 1.65rem;
    font-weight: 950;
    display: flex;
    align-items: center;
    justify-content: center;
}
.report-mini-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin-top: 12px;
}
.report-mini {
    border-radius: 18px;
    padding: 18px;
    background: rgba(2,6,23,0.52);
    border: 1px solid rgba(148,163,184,0.22);
    min-height: 122px;
}
.report-mini strong {
    color: #F8FAFC;
    display: block;
    margin-bottom: 8px;
    font-size: 1.05rem;
}
.report-mini span {
    color: #CBD5E1;
    font-size: 0.95rem;
    line-height: 1.45;
}
.report-warning {
    margin-top: 14px;
    border-radius: 20px;
    padding: 22px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.30);
    color: #FDE68A;
    line-height: 1.55;
}
.report-note {
    margin-top: 12px;
    border-radius: 18px;
    padding: 16px 18px;
    color: #CBD5E1;
    background: rgba(2,6,23,0.44);
    border: 1px solid rgba(148,163,184,0.18);
    line-height: 1.5;
}
.report-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
    margin-top: 10px;
}
.report-table th {
    color: #93C5FD;
    text-align: left;
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 8px 10px;
}
.report-table td {
    color: #CBD5E1;
    background: rgba(2,6,23,0.48);
    border-top: 1px solid rgba(148,163,184,0.16);
    border-bottom: 1px solid rgba(148,163,184,0.16);
    padding: 12px 10px;
    font-size: 0.95rem;
}
.report-table td:first-child {
    border-left: 1px solid rgba(148,163,184,0.16);
    border-radius: 12px 0 0 12px;
    color: #F8FAFC;
    font-weight: 850;
}
.report-table td:last-child {
    border-right: 1px solid rgba(148,163,184,0.16);
    border-radius: 0 12px 12px 0;
}
.report-family-grid, .report-evidence-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 12px;
}
.report-family, .report-evidence {
    border-radius: 18px;
    padding: 18px;
    background: rgba(2,6,23,0.52);
    border: 1px solid rgba(148,163,184,0.22);
    min-height: 136px;
}
.report-family.core { border-top: 4px solid #38BDF8; }
.report-family.industrial { border-top: 4px solid #8B5CF6; }
.report-family.adaptive { border-top: 4px solid #F59E0B; }
.report-family.other { border-top: 4px solid #94A3B8; }
.report-family strong, .report-evidence strong {
    color: #F8FAFC;
    display: block;
    margin-bottom: 8px;
}
.report-family span, .report-evidence span {
    color: #CBD5E1;
    line-height: 1.42;
    font-size: 0.94rem;
}
.report-evidence strong { color: #38BDF8; font-size: 1.35rem; }
.report-cta {
    border-radius: 26px;
    padding: 34px;
    margin-top: 20px;
    text-align: center;
    background:
        radial-gradient(circle at top, rgba(56,189,248,0.18), transparent 42%),
        linear-gradient(135deg, rgba(37,99,235,0.28), rgba(15,23,42,0.90));
    border: 1px solid rgba(56,189,248,0.35);
}
.report-cta-title {
    color: #F8FAFC;
    font-size: 1.75rem;
    font-weight: 950;
    margin-bottom: 10px;
}
.report-cta-text {
    color: #CBD5E1;
    max-width: 900px;
    margin: 0 auto;
    line-height: 1.55;
}
@media (max-width: 1050px) {
    .report-metric-grid, .report-mini-grid, .report-family-grid, .report-evidence-grid { grid-template-columns: 1fr 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# DATA LOADING
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR_CANDIDATES = [
    # Most likely location for the Streamlit app data folder.
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "data" / "app",
    PROJECT_ROOT / "data" / "processed",

    # Fallbacks for running from repository root or from nested app folders.
    PROJECT_ROOT.parent / "data",
    PROJECT_ROOT.parent / "data" / "app",
    PROJECT_ROOT.parent / "data" / "processed",
    Path.cwd() / "data",
    Path.cwd() / "data" / "app",
    Path.cwd() / "data" / "processed",

    # Sandbox fallback for testing here only; harmless in local Streamlit.
    Path("/mnt/data"),
]

DIMENSION_COLS = [
    "dim_sustainability_capacity",
    "dim_human_capital_capacity",
    "dim_innovation_capacity",
    "dim_social_stability",
    "dim_fiscal_flexibility",
    "dim_security_reprioritization",
    "dim_adaptive_transformation",
]

DIMENSION_LABELS = {
    "dim_sustainability_capacity": "Sustainability",
    "dim_human_capital_capacity": "Human capital",
    "dim_innovation_capacity": "Innovation",
    "dim_social_stability": "Social stability",
    "dim_fiscal_flexibility": "Fiscal flexibility",
    "dim_security_reprioritization": "Security",
    "dim_adaptive_transformation": "Adaptive transformation",
}

KPI_TO_DIM = {
    "gdp_growth": "Economy",
    "inflation": "Economy",
    "unemployment": "Social stability",
    "gini": "Social stability",
    "education": "Human capital",
    "rnd": "Innovation",
    "ict_specialists": "Innovation",
    "renewables": "Sustainability",
    "emissions": "Sustainability",
    "debt": "Fiscal flexibility",
    "defense_spending": "Security reprioritization",
    "economic_affairs_spending": "Innovation / Economy",
    "fuel_energy_spending": "Security / Energy",
    "communication_spending": "Innovation / Economy",
    "environment_spending": "Sustainability",
    "health_spending": "Social stability",
    "education_spending": "Human capital / Innovation",
    "social_protection_spending": "Social stability",
    "total_gov_expenditure": "Fiscal flexibility",
}

DIM_TO_OUTPUT = {
    "Sustainability": "Sustainability performance",
    "Human capital": "Innovation readiness",
    "Innovation": "Innovation readiness",
    "Social stability": "Social cohesion",
    "Fiscal flexibility": "Fiscal pressure",
    "Security reprioritization": "Resilience",
    "Adaptive transformation": "Resilience",
}

@st.cache_data(show_spinner=False)
def load_csv_file(filename: str) -> Optional[pd.DataFrame]:
    """Load one CSV from the known app-data locations.

    Returns None when the file is unavailable. Do not use the returned
    DataFrame in boolean expressions; pandas DataFrames have ambiguous truth
    values.
    """
    for folder in DATA_DIR_CANDIDATES:
        path = folder / filename
        if path.exists():
            return pd.read_csv(path)
    return None


def first_available_csv(*filenames: str) -> pd.DataFrame:
    """Return the first available non-empty CSV, otherwise an empty DataFrame."""
    for filename in filenames:
        df = load_csv_file(filename)
        if df is not None and not df.empty:
            return df
    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_all_data():
    return {
        "country_year_full": first_available_csv(
            "dashboard1_country_year_full_norm.csv",
            "dashboard1_country_year.csv",
        ),
        "country_year": first_available_csv(
            "dashboard1_country_year.csv",
            "dashboard1_country_year_full_norm.csv",
        ),
        "profiles": first_available_csv(
            "country_dimension_profiles.csv",
        ),
        "summary": first_available_csv(
            "country_structural_summary_v2_dimensions.csv",
            "country_structural_summary.csv",
        ),
        "families": first_available_csv(
            "structural_family_metadata.csv",
            "family_metadata.csv",
        ),
        "tradeoffs": first_available_csv(
            "tradeoff_space_coordinates.csv",
        ),
        "relationships": first_available_csv(
            "sandbox_response_matrix_v1.csv",
            "relationship_registry.csv",
        ),
        "ecosystem": first_available_csv(
            "dimension_ecosystem_registry_v1.csv",
        ),
        "feature_priority": first_available_csv(
            "feature_priority_matrix.csv",
        ),
        "kpi_meta": first_available_csv(
            "kpi_metadata.csv",
            "kpi_dimension_metadata.csv",
        ),
    }

DATA = load_all_data()


def has_data(name: str) -> bool:
    df = DATA.get(name)
    return isinstance(df, pd.DataFrame) and not df.empty


def first_nonempty_df(*dfs: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Return the first non-empty DataFrame, otherwise an empty DataFrame.

    This avoids pandas truth-value errors such as `df1 or df2`.
    """
    for df in dfs:
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
    return pd.DataFrame()


def available_data_message(required: Iterable[str]) -> Optional[str]:
    missing = [name for name in required if not has_data(name)]
    if missing:
        return "Missing app data tables: " + ", ".join(missing)
    return None


def html(block: str):
    st.markdown(block, unsafe_allow_html=True)


def panel(label: str, title: str, body: str, klass: str = "report-panel-blue"):
    html(
        f"""
<div class="report-panel {klass}">
    <div class="report-label">{label}</div>
    <div class="report-card-title">{title}</div>
    <div class="report-card-body">{body}</div>
</div>
"""
    )


def plotly_theme(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=30, r=30, t=70, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,6,23,0.55)",
        font=dict(color="#E2E8F0", family="Inter, Segoe UI, Arial"),
        title_font=dict(size=18, color="#F8FAFC"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.16)", zerolinecolor="rgba(148,163,184,0.35)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.16)", zerolinecolor="rgba(148,163,184,0.35)")
    return fig


P6_PLOT_COUNTER = 0


def safe_plot(fig: Optional[go.Figure], fallback: str, key: Optional[str] = None):
    """Render a Plotly figure with a guaranteed unique Streamlit key.

    Streamlit 1.57 can raise DuplicateElementId when two generated
    figures have identical specs. This helper assigns stable unique keys
    in page order unless an explicit key is supplied.
    """
    global P6_PLOT_COUNTER

    if fig is None:
        if fallback:
            st.info(fallback)
        return

    if key is None:
        P6_PLOT_COUNTER += 1
        key = f"p6_plot_{P6_PLOT_COUNTER:02d}"

    st.plotly_chart(fig, use_container_width=True, key=key)


def first_existing(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def dim_cols_in(df: pd.DataFrame) -> list[str]:
    return [c for c in DIMENSION_COLS if c in df.columns]


# =============================================================================
# FIGURE BUILDERS
# =============================================================================

def make_sankey() -> go.Figure:
    kpis = list(KPI_TO_DIM.keys())
    dims = sorted(set(KPI_TO_DIM.values()))
    outputs = sorted(set(DIM_TO_OUTPUT.values()))
    labels = kpis + dims + outputs
    index = {label: i for i, label in enumerate(labels)}

    sources, targets, values = [], [], []
    for kpi, dim in KPI_TO_DIM.items():
        sources.append(index[kpi])
        targets.append(index[dim])
        values.append(1)
    for dim, out in DIM_TO_OUTPUT.items():
        if dim in index:
            sources.append(index[dim])
            targets.append(index[out])
            values.append(2)

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=15,
                    thickness=14,
                    line=dict(color="rgba(226,232,240,0.35)", width=0.5),
                    label=[x.replace("_", " ").title() for x in labels],
                    color=["#38BDF8"] * len(kpis) + ["#8B5CF6"] * len(dims) + ["#22C55E"] * len(outputs),
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color="rgba(148,163,184,0.25)",
                ),
            )
        ]
    )
    fig.update_layout(title="KPI → Dimension → Output translation layer")
    return plotly_theme(fig, height=540)


def make_eu_trend_fig(kpis: list[str]) -> Optional[go.Figure]:
    df = first_nonempty_df(DATA.get("country_year_full"), DATA.get("country_year"))
    if df.empty or "year" not in df.columns:
        return None
    value_cols = [k for k in kpis if k in df.columns]
    # Prefer raw columns. If raw not present, try eu_long_zscore versions.
    if not value_cols:
        value_cols = [f"{k}_eu_long_zscore" for k in kpis if f"{k}_eu_long_zscore" in df.columns]
    if not value_cols:
        return None
    long = df[["year"] + value_cols].copy().melt("year", var_name="indicator", value_name="value")
    long = long.dropna()
    long["indicator"] = long["indicator"].str.replace("_eu_long_zscore", "", regex=False).str.replace("_", " ").str.title()
    agg = long.groupby(["year", "indicator"], as_index=False).agg(mean=("value", "mean"), std=("value", "std"))

    fig = px.line(
        agg,
        x="year",
        y="mean",
        color="indicator",
        markers=True,
        title="EU-average structural trend signals",
        labels={"mean": "EU mean", "year": "Year", "indicator": "Indicator"},
    )
    for period_start, period_end, color in [(2020, 2021, "rgba(239,68,68,0.14)"), (2022, 2025, "rgba(56,189,248,0.10)")]:
        fig.add_vrect(x0=period_start, x1=period_end, fillcolor=color, opacity=1, layer="below", line_width=0)
    return plotly_theme(fig, height=420)


def make_investment_trend_fig() -> Optional[go.Figure]:
    investment = [
        "defense_spending", "economic_affairs_spending", "environment_spending",
        "health_spending", "education_spending", "social_protection_spending", "fuel_energy_spending"
    ]
    return make_eu_trend_fig(investment)


def make_country_profile_heatmap() -> Optional[go.Figure]:
    df = first_nonempty_df(DATA.get("profiles"), DATA.get("tradeoffs"), DATA.get("summary"))
    if df.empty:
        return None
    dims = dim_cols_in(df)
    if not dims:
        return None
    name_col = "country_name" if "country_name" in df.columns else "country"
    work = df[[name_col] + dims].dropna(subset=dims, how="all").copy()
    if len(work) == 0:
        return None
    work["sort_score"] = work[dims].fillna(0).sum(axis=1)
    work = work.sort_values("sort_score", ascending=False).drop(columns="sort_score")
    z = work[dims].to_numpy()
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=[DIMENSION_LABELS.get(c, c) for c in dims],
            y=work[name_col],
            colorscale="RdYlGn",
            zmid=0,
            colorbar=dict(title="EU-relative<br>score"),
        )
    )
    fig.update_layout(title="Structural heatmap across countries")
    return plotly_theme(fig, height=max(520, 26 * len(work) + 120))


def make_family_map_scatter() -> Optional[go.Figure]:
    df = first_nonempty_df(DATA.get("tradeoffs"), DATA.get("profiles"), DATA.get("summary"))
    fam = DATA.get("families")
    if df.empty:
        return None
    dims = dim_cols_in(df)
    xcol = "dim_innovation_capacity" if "dim_innovation_capacity" in dims else (dims[0] if dims else None)
    ycol = "dim_sustainability_capacity" if "dim_sustainability_capacity" in dims else (dims[1] if len(dims) > 1 else None)
    if xcol is None or ycol is None:
        return None
    work = df.copy()
    if fam is not None and "structural_family" not in work.columns:
        join_col = "country_name" if "country_name" in work.columns and "country_name" in fam.columns else "country"
        if join_col in work.columns and join_col in fam.columns:
            work = work.merge(fam[[join_col, "structural_family"]].drop_duplicates(), on=join_col, how="left")
    if "structural_family" not in work.columns:
        work["structural_family"] = "Country"
    name_col = "country_name" if "country_name" in work.columns else "country"
    fig = px.scatter(
        work,
        x=xcol,
        y=ycol,
        color="structural_family",
        hover_name=name_col,
        text=name_col,
        title="Family-colored structural map: innovation vs sustainability",
        labels={xcol: DIMENSION_LABELS.get(xcol, xcol), ycol: DIMENSION_LABELS.get(ycol, ycol), "structural_family": "Family"},
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(226,232,240,0.55)")
    fig.add_vline(x=0, line_dash="dot", line_color="rgba(226,232,240,0.55)")
    return plotly_theme(fig, height=520)


def make_clustering_figs() -> tuple[Optional[go.Figure], Optional[go.Figure]]:
    df = first_nonempty_df(DATA.get("profiles"), DATA.get("tradeoffs"), DATA.get("summary"))
    if df.empty:
        return None, None
    dims = dim_cols_in(df)
    if len(dims) < 3:
        return None, None
    work = df.dropna(subset=dims).copy()
    if len(work) < 6:
        return None, None
    X = work[dims].to_numpy()
    name_col = "country_name" if "country_name" in work.columns else "country"

    # Fallback: heatmap sorted by first principal direction-like score
    scores = pd.Series(X.mean(axis=1), index=work.index)
    ordered = work.assign(_score=scores).sort_values("_score", ascending=False)
    heat = go.Figure(data=go.Heatmap(
        z=ordered[dims].to_numpy(),
        x=[DIMENSION_LABELS.get(c, c) for c in dims],
        y=ordered[name_col],
        colorscale="RdYlGn",
        zmid=0,
        colorbar=dict(title="score"),
    ))
    heat.update_layout(title="Cluster input matrix: countries × structural dimensions")
    heat = plotly_theme(heat, height=max(500, 24 * len(ordered) + 120))

    eval_fig = None
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        inertias, silhouettes, ks = [], [], list(range(2, min(8, len(work) - 1)))
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=20).fit(X)
            inertias.append(float(km.inertia_))
            silhouettes.append(float(silhouette_score(X, km.labels_)))
        eval_df = pd.DataFrame({"k": ks, "inertia": inertias, "silhouette": silhouettes})
        eval_fig = go.Figure()
        eval_fig.add_trace(go.Scatter(x=eval_df["k"], y=eval_df["inertia"], mode="lines+markers", name="Inertia / elbow", yaxis="y1"))
        eval_fig.add_trace(go.Scatter(x=eval_df["k"], y=eval_df["silhouette"], mode="lines+markers", name="Silhouette", yaxis="y2"))
        eval_fig.update_layout(
            title="Cluster-number checks: elbow and silhouette",
            xaxis_title="Number of clusters",
            yaxis=dict(title="Inertia"),
            yaxis2=dict(title="Silhouette", overlaying="y", side="right"),
        )
        eval_fig = plotly_theme(eval_fig, height=420)
    except Exception:
        pass
    return heat, eval_fig


def make_tradeoff_matrix_or_scatter() -> Optional[go.Figure]:
    df = first_nonempty_df(DATA.get("tradeoffs"), DATA.get("profiles"), DATA.get("summary"))
    if df.empty:
        return None
    dims = dim_cols_in(df)
    if len(dims) < 2:
        return None
    # Prefer a useful P2-style tradeoff.
    xcol = "dim_fiscal_flexibility" if "dim_fiscal_flexibility" in dims else dims[0]
    ycol = "dim_innovation_capacity" if "dim_innovation_capacity" in dims else dims[1]
    work = df.copy()
    name_col = "country_name" if "country_name" in work.columns else "country"
    color_col = "structural_family" if "structural_family" in work.columns else ("archetype_type" if "archetype_type" in work.columns else None)
    fig = px.scatter(
        work,
        x=xcol,
        y=ycol,
        color=color_col,
        hover_name=name_col,
        text=name_col,
        title="Example tradeoff space: innovation capacity vs fiscal flexibility",
        labels={xcol: DIMENSION_LABELS.get(xcol, xcol), ycol: DIMENSION_LABELS.get(ycol, ycol)},
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(226,232,240,0.55)")
    fig.add_vline(x=0, line_dash="dot", line_color="rgba(226,232,240,0.55)")
    return plotly_theme(fig, height=520)


def make_dimension_correlation_heatmap() -> Optional[go.Figure]:
    df = first_nonempty_df(DATA.get("profiles"), DATA.get("tradeoffs"), DATA.get("summary"))
    if df.empty:
        return None
    dims = dim_cols_in(df)
    if len(dims) < 3:
        return None
    corr = df[dims].corr(method="spearman")
    fig = go.Figure(data=go.Heatmap(
        z=corr.to_numpy(),
        x=[DIMENSION_LABELS.get(c, c) for c in corr.columns],
        y=[DIMENSION_LABELS.get(c, c) for c in corr.index],
        colorscale="RdBu",
        zmin=-1,
        zmax=1,
        zmid=0,
        text=np.round(corr.to_numpy(), 2),
        texttemplate="%{text}",
        colorbar=dict(title="ρ"),
    ))
    fig.update_layout(title="Dimension relationship screen: Spearman correlation")
    return plotly_theme(fig, height=520)


def make_relationship_evidence_fig() -> Optional[go.Figure]:
    rel = first_nonempty_df(DATA.get("relationships"), DATA.get("ecosystem"))
    if rel.empty:
        return None
    level_col = first_existing(rel, ["evidence_level", "evidence_class", "relationship_strength", "evidence"])
    if level_col is None:
        return None
    counts = rel[level_col].fillna("Unclassified").astype(str).value_counts().reset_index()
    counts.columns = ["Evidence level", "Count"]
    fig = px.bar(counts, x="Evidence level", y="Count", title="Evidence-level distribution in relationship registry", text="Count")
    return plotly_theme(fig, height=380)


def make_relationship_example_scatter() -> Optional[go.Figure]:
    """Create a dependency-free example scatter for relationship screening.

    Uses numpy for a simple trend line. No statsmodels dependency.
    """
    df = first_nonempty_df(DATA.get("country_year_full"), DATA.get("country_year"))
    if df.empty:
        return None

    x_col = first_existing(
        df,
        [
            "education_spending_eu_long_zscore",
            "education_spending",
            "education_eu_long_zscore",
            "education",
        ],
    )
    y_col = first_existing(
        df,
        [
            "rnd_eu_long_zscore",
            "dim_innovation_capacity",
            "rnd",
            "ict_specialists_eu_long_zscore",
            "ict_specialists",
        ],
    )

    if x_col is None or y_col is None:
        return None

    name_col = "country_name" if "country_name" in df.columns else ("country" if "country" in df.columns else None)
    keep_cols = [c for c in [x_col, y_col, name_col, "year"] if c is not None and c in df.columns]
    work = df[keep_cols].dropna(subset=[x_col, y_col]).copy()

    if len(work) < 5:
        return None

    if len(work) > 800:
        work = work.sample(800, random_state=42)

    fig = px.scatter(
        work,
        x=x_col,
        y=y_col,
        color="year" if "year" in work.columns else None,
        hover_name=name_col if name_col in work.columns else None,
        title="Example relationship screen: education signal and innovation signal",
        labels={
            x_col: x_col.replace("_eu_long_zscore", "").replace("_", " ").title(),
            y_col: y_col.replace("_eu_long_zscore", "").replace("_", " ").title(),
        },
    )

    # Manual linear trend line, avoiding external statsmodels dependency.
    x = work[x_col].to_numpy(dtype=float)
    y = work[y_col].to_numpy(dtype=float)
    if len(np.unique(x)) > 1:
        coef = np.polyfit(x, y, 1)
        x_line = np.linspace(float(np.nanmin(x)), float(np.nanmax(x)), 100)
        y_line = coef[0] * x_line + coef[1]
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Simple linear trend",
                line=dict(color="#F8FAFC", width=2, dash="dash"),
            )
        )

    return plotly_theme(fig, height=480)

# =============================================================================
# HEADER
# =============================================================================

st.html(
    """
    <div class="p1-brand">
        <div class="p1-logo">✦</div>
        <div>
            <div class="p1-brand-title">EUROPEAN<br>STRATEGY ATLAS</div>
            <div class="p1-brand-subtitle">
                Behind the data • Methods • Validation • App translation
            </div>
        </div>
    </div>
    """
)


# =============================================================================
# SECTION 00 — HERO
# =============================================================================

profiles = DATA.get("profiles")
cy = first_nonempty_df(DATA.get("country_year_full"), DATA.get("country_year"))
num_countries = int(profiles["country_name" if "country_name" in profiles.columns else "country"].nunique()) if isinstance(profiles, pd.DataFrame) and not profiles.empty and ("country_name" in profiles.columns or "country" in profiles.columns) else 27
num_years = int(cy["year"].nunique()) if isinstance(cy, pd.DataFrame) and not cy.empty and "year" in cy.columns else 12

html(
    f"""
<div class="report-hero">
    <div class="report-kicker">HOW IT WAS MADE</div>
    <div class="report-title">From public data to a<br><span>scientific exploration Atlas.</span></div>
    <div class="report-body">
        This page opens the analytical black box behind the app. It shows how public European data was cleaned,
        normalized, translated into dimensions, tested through tradeoff analysis, validated through families and evidence levels,
        and finally turned into a Streamlit learning experience.
    </div>
    <div class="report-metric-grid">
        <div class="report-metric"><div class="report-metric-num">{num_countries}</div><div class="report-metric-label">EU countries</div></div>
        <div class="report-metric"><div class="report-metric-num">{num_years}</div><div class="report-metric-label">years of data</div></div>
        <div class="report-metric"><div class="report-metric-num">19</div><div class="report-metric-label">core KPIs</div></div>
        <div class="report-metric"><div class="report-metric-num">7</div><div class="report-metric-label">structural dimensions</div></div>
    </div>
</div>
"""
)


# =============================================================================
# SECTION 01 — WHY THIS PROJECT
# =============================================================================

render_section_title(
    number="01",
    title="Why this project?",
    subtitle="The project starts from a communication problem: public European data exists, but it is hard to interpret structurally.",
)

c1, c2 = st.columns(2, gap="medium")
with c1:
    panel(
        "Problem",
        "Public data is fragmented and indicator-heavy.",
        "Eurostat-style data is rich, but difficult for non-experts to interpret beyond single indicators, charts, or rankings. Raw KPIs alone do not explain structural pathways.",
        "report-panel-red",
    )
with c2:
    panel(
        "Goal",
        "Turn data into guided structural exploration.",
        "The Atlas translates public data into country profiles, tradeoff spaces, structural families, and educational prompts. The goal is understanding — not prediction, ranking, or prescription.",
        "report-panel-green",
    )


# =============================================================================
# SECTION 02 — DATA PIPELINE
# =============================================================================

render_section_title(
    number="02",
    title="Data pipeline",
    subtitle="From public data tables to app-ready analytical layers.",
)

html(
    """
<div class="report-panel">
    <div class="report-label">Pipeline summary</div>
    <div class="report-card-title">A country-year panel becomes the analytical backbone.</div>
    <div class="report-flow">
        <div class="report-flow-node"><strong>Download</strong><span>Eurostat / public EU indicators</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Clean</strong><span>countries, years, units, missing values</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Normalize</strong><span>raw, EU-relative, country-relative</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Model</strong><span>dimensions, families, tradeoffs</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Export</strong><span>Streamlit tables and registries</span></div>
    </div>
</div>
"""
)

if cy is not None and "year" in cy.columns:
    year_counts = cy.groupby("year").size().reset_index(name="records")
    fig = px.bar(year_counts, x="year", y="records", title="Country-year records available by year")
    safe_plot(plotly_theme(fig, height=320), "")


# =============================================================================
# SECTION 03 — KPI TO DIMENSION TO OUTPUT
# =============================================================================

render_section_title(
    number="03",
    title="Analytical translation layer",
    subtitle="The app does not show all raw KPIs directly. It translates them into interpretable structural dimensions and outputs.",
)

safe_plot(make_sankey(), "Sankey diagram could not be rendered.")
html(
    """
<div class="report-note">
    The Sankey summarizes the conceptual modeling layer: raw indicators are grouped into structural dimensions,
    and dimensions are then used to support app outputs and tradeoff interpretation.
</div>
"""
)


# =============================================================================
# SECTION 04 — NORMALIZATION
# =============================================================================

render_section_title(
    number="04",
    title="Normalization method",
    subtitle="Different questions require different baselines. The Atlas keeps three lenses visible.",
)

html(
    """
<div class="report-mini-grid">
    <div class="report-mini"><strong>Raw values</strong><span>What actually happened? Preserves units such as %, debt, emissions, or spending share.</span></div>
    <div class="report-mini"><strong>EU-relative score</strong><span>Where does a country stand compared with the European structural baseline?</span></div>
    <div class="report-mini"><strong>Country-relative score</strong><span>How is a country changing compared with its own historical baseline?</span></div>
</div>
<div class="report-warning">
    Normalization is not decoration. It changes the question. Raw values explain scale, EU-relative values explain structural position, and country-relative values explain internal transformation.
</div>
"""
)

safe_plot(make_eu_trend_fig(["renewables", "emissions", "rnd", "ict_specialists"]), "Trend chart requires dashboard1_country_year_full_norm.csv or dashboard1_country_year.csv.")


# =============================================================================
# SECTION 05 — TRENDS AND PERIODS
# =============================================================================

render_section_title(
    number="05",
    title="Trends, periods, and structural signals",
    subtitle="The time axis was split into meaningful periods so the app can separate baseline structure, shock response, and transition behavior.",
)

html(
    """
<div class="report-mini-grid">
    <div class="report-mini"><strong>2014–2019<br>Baseline</strong><span>Pre-shock structural position and long-term country profile.</span></div>
    <div class="report-mini"><strong>2020–2021<br>COVID transition</strong><span>Short-term disruption period used to observe shock response.</span></div>
    <div class="report-mini"><strong>2022–2025<br>Energy / geopolitical transition</strong><span>Post-shock repositioning and adaptation period.</span></div>
</div>
"""
)

safe_plot(make_investment_trend_fig(), "Investment trend chart requires public-spending KPI columns.")

html(
    """
<table class="report-table">
    <tr><th>Layer</th><th>Question</th><th>Use in app</th></tr>
    <tr><td>EU trends</td><td>What changed across Europe?</td><td>Context for common structural pressures.</td></tr>
    <tr><td>Country trends</td><td>How did one country evolve?</td><td>Country Explorer evolution story.</td></tr>
    <tr><td>Period shifts</td><td>How did shocks alter the path?</td><td>Challenge and resilience interpretation.</td></tr>
</table>
"""
)


# =============================================================================
# SECTION 06 — COUNTRY PROFILE
# =============================================================================

render_section_title(
    number="06",
    title="Country profile construction",
    subtitle="Each country becomes a structural profile, not a single score.",
)

c1, c2 = st.columns([1.05, 1], gap="medium")
with c1:
    panel(
        "Country profile",
        "A profile combines position, change, and context.",
        "For each country, the app stores latest dimension values, historical movement, reference gaps, strongest advantages, constraints, family membership, archetype label, and dynamic pathway information.",
    )
with c2:
    html(
        """
<div class="report-panel report-panel-purple">
    <div class="report-label">Profile ingredients</div>
    <ul class="report-bullets">
        <li>Current structural dimensions</li>
        <li>Country vs EU / family / another country</li>
        <li>Strengths and constraints</li>
        <li>Archetype and family context</li>
        <li>Shock and adaptation signals</li>
    </ul>
</div>
"""
    )

safe_plot(make_country_profile_heatmap(), "Country profile heatmap requires country_dimension_profiles.csv or tradeoff_space_coordinates.csv.")


# =============================================================================
# SECTION 07 — HEATMAP, CLUSTERING, FAMILIES
# =============================================================================

render_section_title(
    number="07",
    title="From heatmap to structural families",
    subtitle="Families were developed by combining structural position, clustering evidence, interpretability, and narrative usefulness.",
)

cluster_heat, cluster_eval = make_clustering_figs()
safe_plot(cluster_heat, "Clustering input heatmap requires country × dimension table.")
safe_plot(cluster_eval, "Cluster-number checks require scikit-learn and enough country profiles.")
safe_plot(make_family_map_scatter(), "Family map requires structural_family_metadata.csv and dimension profiles.")

html(
    """
<div class="report-family-grid">
    <div class="report-family core"><strong>Innovation-Core Systems</strong><span>High innovation, human capital, and adaptive capacity. Representative examples include Germany, Sweden, Netherlands, and Finland.</span></div>
    <div class="report-family industrial"><strong>Industrial / Transition Systems</strong><span>Industrial strength, transition pressure, and mixed adaptation patterns. Representative examples include Poland, Spain, and Italy.</span></div>
    <div class="report-family adaptive"><strong>Adaptive / Peripheral Systems</strong><span>Convergence pathways, selective strengths, and distinct fiscal or transition profiles. Romania is a key learning example.</span></div>
    <div class="report-family other"><strong>Bridge / Transitional cases</strong><span>Countries that sit between families or behave differently across static and dynamic lenses.</span></div>
</div>
"""
)


# =============================================================================
# SECTION 08 — TRADEOFF AND RELATIONSHIP ANALYSIS
# =============================================================================

render_section_title(
    number="08",
    title="Tradeoff and relationship analysis",
    subtitle="Tradeoffs were screened globally and by family, using correlation strength, direction, and interpretability.",
)

safe_plot(make_tradeoff_matrix_or_scatter(), "Tradeoff scatter requires tradeoff_space_coordinates.csv or dimension profiles.")
safe_plot(make_dimension_correlation_heatmap(), "Dimension correlation heatmap requires country dimension profiles.")

html(
    """
<div class="report-panel">
    <div class="report-label">Relationship screening logic</div>
    <div class="report-flow">
        <div class="report-flow-node"><strong>Select pair</strong><span>dimension ↔ dimension or investment ↔ dimension</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Global test</strong><span>Pearson + Spearman across countries</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Family test</strong><span>Does the pattern hold inside families?</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>Evidence class</strong><span>A / B / C / D interpretation level</span></div>
    </div>
</div>
"""
)

safe_plot(make_relationship_evidence_fig(), "Evidence summary requires sandbox_response_matrix_v1.csv or dimension_ecosystem_registry_v1.csv.")

html(
    """
<div class="report-evidence-grid">
    <div class="report-evidence"><strong>A</strong><span>Strong, consistent, interpretable relationship.</span></div>
    <div class="report-evidence"><strong>B</strong><span>Moderate or useful relationship with some context limits.</span></div>
    <div class="report-evidence"><strong>C</strong><span>Weak, conditional, or family-specific signal.</span></div>
    <div class="report-evidence"><strong>D</strong><span>Exploratory only. Useful for questions, not conclusions.</span></div>
</div>
"""
)


# =============================================================================
# SECTION 09 — RELATIONSHIPS, EVIDENCE & WEIGHTS
# =============================================================================

render_section_title(
    number="09",
    title="Relationships, evidence, and weight design",
    subtitle="How exploratory relationships became transparent educational building blocks.",
)

c1, c2 = st.columns([1.15, 1], gap="medium")

with c1:
    html(
        """
<div class="report-panel report-panel-blue">
    <div class="report-label">Relationship discovery process</div>
    <div class="report-card-title">The project screened relationships before promoting them into the app.</div>
    <ul class="report-bullets">
        <li>Pearson correlations checked linear association.</li>
        <li>Spearman correlations checked rank-order association.</li>
        <li>Family-level checks tested whether patterns changed by structural context.</li>
        <li>Tradeoff spaces tested whether relationships were visually interpretable.</li>
        <li>Conceptual review checked whether the relationship made sense as an educational explanation.</li>
    </ul>
</div>
"""
    )

with c2:
    html(
        """
<div class="report-panel report-panel-purple">
    <div class="report-label">Evidence logic</div>
    <div class="report-card-title">Not every relationship received the same confidence.</div>
    <div class="report-card-body">
        Relationships were classified by consistency, direction, interpretability,
        family robustness, and educational value. The evidence level guides how strongly
        the app explains a pattern.
        <br><br>
        <b>Important:</b> evidence levels guide interpretation, not certainty.
    </div>
</div>
"""
    )

safe_plot(
    make_relationship_example_scatter(),
    "Example relationship scatter requires relevant columns such as education_spending and R&D / innovation.",
)

safe_plot(
    make_relationship_evidence_fig(),
    "Evidence summary requires sandbox_response_matrix_v1.csv or dimension_ecosystem_registry_v1.csv.",
)

html(
    """
<div class="report-evidence-grid">
    <div class="report-evidence"><strong>A</strong><span>Strong, consistent, interpretable relationship.</span></div>
    <div class="report-evidence"><strong>B</strong><span>Moderate or useful relationship with context limits.</span></div>
    <div class="report-evidence"><strong>C</strong><span>Weak, conditional, or family-specific signal.</span></div>
    <div class="report-evidence"><strong>D</strong><span>Exploratory only. Useful for questions, not conclusions.</span></div>
</div>
"""
)

st.markdown("---")

c3, c4 = st.columns(2, gap="medium")

with c3:
    html(
        """
<div class="report-panel report-panel-amber">
    <div class="report-label">Weight definition process</div>
    <ul class="report-bullets">
        <li>Start from KPI meaning and direction.</li>
        <li>Normalize indicators to comparable scales.</li>
        <li>Combine KPIs into structural dimensions using transparent weights.</li>
        <li>Use correlation and regression-style screening as support, not proof.</li>
        <li>Prefer interpretability over statistical sophistication.</li>
    </ul>
</div>
"""
    )

with c4:
    html(
        """
<div class="report-panel report-panel-green">
    <div class="report-label">Example dimension logic</div>
    <div class="report-card-title">Adaptive Transformation</div>
    <div class="report-card-body">
        A simplified dimension combining innovation and sustainability capacity.
        This kind of formula makes the app explainable while keeping assumptions visible.
        <br><br>
        <b>Important:</b> coefficients are educational design choices supported by EDA,
        not causal policy effects.
    </div>
</div>
"""
    )

html(
    """
<div class="report-warning">
    Observed relationships are historical associations. They do not imply causation,
    prediction, policy recommendation, or optimization.
</div>
"""
)

# =============================================================================
# SECTION 10 — ASSUMPTIONS AND DISCLAIMERS
# =============================================================================

render_section_title(
    number="10",
    title="Assumptions and limitations",
    subtitle="The Atlas is useful because its assumptions are visible, not because it claims certainty.",
)

html(
    """
<div class="report-mini-grid">
    <div class="report-mini"><strong>Structural proxy awareness</strong><span>GDP growth is not prosperity. Renewables are not full sustainability. Debt is not weakness. ICT specialists are not innovation itself.</span></div>
    <div class="report-mini"><strong>Correlation is not causation</strong><span>The project identifies historical associations and comparative patterns, not causal mechanisms or policy effects.</span></div>
    <div class="report-mini"><strong>Educational purpose</strong><span>The Atlas is designed to help users reason about tradeoffs, compare pathways, and ask better questions.</span></div>
</div>
<div class="report-mini-grid">
    <div class="report-mini"><strong>Not predictive</strong><span>The app does not forecast future country performance.</span></div>
    <div class="report-mini"><strong>Not prescriptive</strong><span>The app does not recommend policies or optimize decisions.</span></div>
    <div class="report-mini"><strong>Not a ranking system</strong><span>Countries are shown as different structural pathways, not winners and losers.</span></div>
</div>
<div class="report-warning">
    The strongest interpretation of this project is methodological:
    it transforms fragmented public data into a transparent learning system for structural reasoning.
</div>
"""
)

# =============================================================================
# SECTION 11 — DATA TO APP
# =============================================================================

render_section_title(
    number="11",
    title="From data analysis to Streamlit app",
    subtitle="The final step was translating analytical outputs into a guided learning experience.",
)

html(
    """
<div class="report-panel">
    <div class="report-label">App translation</div>
    <div class="report-card-title">The analysis became an exploration loop.</div>
    <div class="report-flow">
        <div class="report-flow-node"><strong>P0<br>Orient</strong><span>What is this Atlas?</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>P1<br>Observe</strong><span>Who is this country?</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>P2<br>Investigate</strong><span>What tradeoffs shape it?</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>P3<br>Choose</strong><span>What priority would you test?</span></div>
        <div class="report-arrow">→</div>
        <div class="report-flow-node"><strong>P4–P5<br>Challenge & Reflect</strong><span>What did you learn?</span></div>
    </div>
</div>
<div class="report-cta">
    <div class="report-cta-title">The final product is not a dashboard.</div>
    <div class="report-cta-text">
        It is a guided data analytics story: public data → normalized indicators → dimensions → profiles → families → tradeoffs → strategic learning.
    </div>
</div>
"""
)

render_footer()
