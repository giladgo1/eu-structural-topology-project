"""
p6_how_it_was_made_v08_reduced_redundancy.py

EUROPEAN STRATEGY ATLAS — P6 How It Was Made
Graduation current version methodology appendix.

Place in:
    streamlit_app/pages/p6_how_it_was_made.py

Place assets in:
    streamlit_app/assets/p6/

Required/expected assets:
    p6_sankey_translation_crop.png
    p6_structural_families_map_clean.png
    p6_heatmap_families_crop.png
    p6_context_tradeoffs_crop.png
    p6_app_journey_crop.png

Optional assets:
    p6_normalization_framework.png
    p6_strategy_engine.png
    p6_challenge_engine.png
"""

from __future__ import annotations

from pathlib import Path
import base64
import html as html_lib
import textwrap

import streamlit as st

try:
    from components.page_frame import render_footer
except Exception:
    def render_footer():
        st.markdown("---")
        st.caption("EUROPEAN STRATEGY ATLAS — current version")


# =============================================================================
# PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="How It Was Made | EUROPEAN STRATEGY ATLAS",
    layout="wide",
)


def load_css() -> None:
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


def safe_switch_page(page_path: str) -> None:
    """Navigate safely across Streamlit multipage apps."""
    candidates = [
        page_path,
        f"pages/{page_path}" if not page_path.startswith("pages/") else page_path.replace("pages/", "", 1),
        "pages/p0_landing.py",
        "p0_landing.py",
        "pages/p1_country_explorer.py",
        "p1_country_explorer.py",
    ]

    for candidate in dict.fromkeys(candidates):
        try:
            st.switch_page(candidate)
            return
        except Exception:
            pass

    st.info("Navigation target not found. Use the sidebar to return to the Atlas landing page.")


ASSET_CANDIDATES = [
    Path(__file__).parent.parent / "assets" / "p6",
    Path(__file__).parent.parent / "assets",
    Path.cwd() / "streamlit_app" / "assets" / "p6",
    Path.cwd() / "streamlit_app" / "assets",
    Path.cwd() / "assets" / "p6",
    Path.cwd() / "assets",
    Path("/mnt/data") / "p6_assets_cropped",
    Path("/mnt/data") / "p6_assets",
]


def find_asset(filename: str) -> Path | None:
    for folder in ASSET_CANDIDATES:
        path = folder / filename
        if path.exists():
            return path
    return None


def image_data_uri(filename: str) -> str | None:
    path = find_asset(filename)
    if path is None:
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def img_block(filename: str, caption: str, compact: bool = False) -> str:
    src = image_data_uri(filename)
    if not src:
        return (
            "<div class='p6-missing'>"
            f"Missing asset: <code>{html_lib.escape(filename)}</code><br>"
            "Expected under <code>streamlit_app/assets/p6/</code>."
            "</div>"
        )
    klass = "p6-figure compact" if compact else "p6-figure"
    return (
        f"<figure class='{klass}'>"
        f"<img src='{src}' alt='{html_lib.escape(caption)}' />"
        f"<figcaption>{html_lib.escape(caption)}</figcaption>"
        "</figure>"
    )


def html(block: str) -> None:
    """Render HTML reliably without Markdown code-block interpretation."""
    st.html(textwrap.dedent(block).strip())


# =============================================================================
# STATIC TABLE CONTENT
# =============================================================================

KPI_ROWS = [
    ("GDP growth", "Eurostat / OECD macro", "Economic context"),
    ("Inflation", "Eurostat / OECD macro", "Economic context"),
    ("Unemployment", "Eurostat labour market", "Social Stability"),
    ("Gini", "Eurostat income distribution", "Social Stability"),
    ("Education", "Eurostat education", "Human Capital Capacity"),
    ("R&D", "Eurostat R&D", "Innovation Capacity"),
    ("ICT specialists", "Eurostat digital economy", "Innovation Capacity"),
    ("Renewables", "Eurostat energy", "Sustainability Capacity"),
    ("Emissions", "Eurostat / EEA environment", "Sustainability Capacity"),
    ("Debt", "Eurostat government finance", "Fiscal Flexibility"),
    ("Defense spending", "Eurostat COFOG", "Security Reprioritization"),
    ("Economic affairs spending", "Eurostat COFOG", "Innovation / Economy"),
    ("Fuel & energy spending", "Eurostat COFOG", "Security / Energy"),
    ("Communication spending", "Eurostat COFOG", "Innovation / Economy"),
    ("Environment spending", "Eurostat COFOG", "Sustainability Capacity"),
    ("Health spending", "Eurostat COFOG", "Social Stability"),
    ("Education spending", "Eurostat COFOG", "Human Capital / Innovation"),
    ("Social protection spending", "Eurostat COFOG", "Social Stability"),
    ("Total government expenditure", "Eurostat COFOG", "Fiscal Flexibility"),
]

DIMENSION_ROWS = [
    (
        "Sustainability Capacity",
        "Can the country transition toward a more sustainable economy?",
        "0.40 × Renewables + 0.30 × Environment Spending − 0.30 × Emissions",
        "Sustainability Performance",
    ),
    (
        "Human Capital Capacity",
        "Can the country develop talent and skills?",
        "0.60 × Education + 0.40 × Education Spending",
        "Innovation Readiness / Social Cohesion",
    ),
    (
        "Innovation Capacity",
        "Can the country build future capability?",
        "0.45 × R&D + 0.35 × ICT Specialists + 0.20 × Economic Affairs Spending",
        "Innovation Readiness / Growth Potential",
    ),
    (
        "Social Stability",
        "Can the country maintain cohesion and wellbeing?",
        "0.30 × Social Protection + 0.25 × Health − 0.25 × Unemployment − 0.20 × Gini",
        "Social Cohesion / Resilience",
    ),
    (
        "Fiscal Flexibility",
        "How much room does the country have to act?",
        "−0.60 × Debt − 0.40 × Total Government Expenditure",
        "Fiscal Pressure / Flexibility",
    ),
    (
        "Security Reprioritization",
        "How strongly is the country shifting toward security and resilience?",
        "0.80 × Defense Spending + 0.20 × Fuel / Energy Spending",
        "Resilience / Security response",
    ),
    (
        "Adaptive Transformation",
        "How effectively is the country combining innovation and sustainability?",
        "0.50 × Innovation Capacity + 0.50 × Sustainability Capacity",
        "Resilience / Sustainability Performance",
    ),
]

DYNAMIC_ROWS = [
    ("Static position", "Latest EU-relative dimension score", "Where is the country now relative to Europe?"),
    ("Dynamic gain", "Dimension score in 2024 − dimension score in 2014", "How much did the country improve over time?"),
    ("Shock response", "COVID-period change relative to baseline", "How did the system move during stress?"),
    ("Transition shift", "Energy/geopolitical-period change relative to baseline", "How did the system reposition after shocks?"),
    ("Adaptation shift", "Transition shift − Shock response", "Did the country recover, accelerate, or stall?"),
]

FAMILY_ROWS = [
    ("Innovation-Core", "Sweden, Finland, Denmark, Netherlands, Belgium, Austria", "Innovation and sustainability leaders.", "Sweden / Finland / Netherlands"),
    ("Industrial / Transition", "Germany, France, Poland, Czechia, Slovakia, Hungary, Slovenia, Italy", "Strong capabilities under transformation.", "Germany / Poland"),
    ("Adaptive / Peripheral", "Spain, Portugal, Romania, Bulgaria, Greece, Croatia, Estonia, Latvia, Lithuania, Cyprus, Malta", "Alternative pathways and adaptation strategies.", "Spain / Romania / Estonia"),
    ("Other / Transitional", "Ireland, Luxembourg", "Structurally unusual cases reviewed separately.", "Outliers / special cases"),
]

EVIDENCE_ROWS = [
    ("A", "Strong", "Consistent, interpretable relationship used with higher confidence."),
    ("B", "Moderate", "Useful relationship with context or family limitations."),
    ("C", "Weak", "Conditional or family-specific signal; mainly used as a prompt."),
    ("D", "Exploratory", "Question-generating only; not treated as a conclusion."),
]

DRIVER_ROWS = [
    ("Human Capital", "Capability + investment", "Education level and education spending move together; useful for long-term capability building."),
    ("Innovation", "Capability + capability-building", "R&D, ICT specialists, and economic-affairs investment support innovation capacity."),
    ("Security", "Capability + reprioritization", "Defense and energy-related spending capture a strategic shift toward security and resilience."),
    ("Sustainability", "State + pathway + conversion effectiveness", "Renewables, environmental spending, and emissions determine the sustainability signal."),
]

STRATEGY_ROWS = [
    ("Education", "Human Capital", "A", "+", "Strong universal relationship."),
    ("Defense", "Security", "A", "+", "Strong universal relationship."),
    ("Social Protection", "Fiscal Flexibility", "A", "−", "Tradeoff relationship."),
    ("Social Protection", "Social Stability", "B", "+", "Moderate positive relationship."),
    ("Education", "Innovation", "B", "+", "Supports innovation capacity."),
    ("Environment", "Sustainability", "C", "+", "Family-dependent relationship."),
    ("Economic Affairs", "Innovation", "D", "+", "Exploratory relationship."),
]

CHALLENGE_ROWS = [
    ("Pandemic Pressure", "COVID transition, 2020–2021", "Social stability, fiscal flexibility, human capital, innovation, adaptive transformation."),
    ("Energy Crisis", "Energy/geopolitical transition, 2022–2025", "Security, sustainability, adaptive transformation, fiscal flexibility, social stability, innovation."),
]

NORMALIZATION_ROWS = [
    ("Absolute values", "What actually happened?", "Keeps original units and scale."),
    ("EU-relative normalization", "How does the country compare structurally to Europe?", "Used for cross-country position."),
    ("Country-relative normalization", "How does the country evolve relative to itself?", "Used for internal transformation."),
]

PERIOD_ROWS = [
    ("Pre-shock baseline", "2014–2019", "Baseline structural reference period."),
    ("COVID transition", "2020–2021", "Stress-response period."),
    ("Energy/geopolitical transition", "2022–2025", "Energy, security, and fiscal pressure period."),
]


# =============================================================================
# HTML HELPERS
# =============================================================================

def table_html(headers: list[str], rows: list[tuple[str, ...]], small: bool = False, compact_width: bool = False) -> str:
    head = "".join(f"<th>{html_lib.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html_lib.escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    klass = "p6-table"
    if small:
        klass += " p6-table-small"
    if compact_width:
        klass += " p6-table-compact"
    return f"<table class='{klass}'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def card(label: str, title: str, body: str, accent: str = "#38BDF8") -> str:
    return (
        f"<div class='p6-card' style='--accent:{accent};'>"
        f"<div class='p6-card-label'>{html_lib.escape(label)}</div>"
        f"<div class='p6-card-title'>{html_lib.escape(title)}</div>"
        f"<div class='p6-card-body'>{html_lib.escape(body)}</div>"
        "</div>"
    )


def section(number: str, title: str, subtitle: str) -> None:
    html(
        f"""
        <div class='p6-section-title'>
            <div class='p6-section-num'>{html_lib.escape(number)}</div>
            <div>
                <h2>{html_lib.escape(title)}</h2>
                <p>{html_lib.escape(subtitle)}</p>
            </div>
        </div>
        """
    )


def intro(text: str) -> None:
    html(f"<div class='p6-intro'>{html_lib.escape(text)}</div>")


def intro_html(text: str) -> None:
    html(f"<div class='p6-intro'>{text}</div>")


def render_p6_footer() -> None:
    html(
        """
        <div class='p6-simple-footer'>
            <div><b>EUROPEAN STRATEGY ATLAS — current version</b></div>
            <div>Gilad Gotesman · SPICED Academy Capstone Project</div>
        </div>
        """
    )


# =============================================================================
# CSS
# =============================================================================

html(
    """
<style>
.p6-page { max-width:1500px; margin:0 auto; }
.p6-brand { border:1px solid rgba(56,189,248,0.28); border-radius:18px; background:rgba(15,23,42,0.82); padding:18px 22px; display:flex; align-items:center; gap:16px; min-height:78px; }
.p6-logo { color:#38BDF8; font-size:2.15rem; line-height:1; }
.p6-brand-title { color:#F8FAFC; font-size:1.12rem; font-weight:950; letter-spacing:0.04em; line-height:1.1; }
.p6-brand-subtitle { color:#94A3B8; font-size:0.86rem; font-weight:700; margin-top:4px; }
.p6-hero { border-radius:30px; padding:42px 46px; margin-bottom:26px; background:radial-gradient(circle at 88% 12%, rgba(56,189,248,0.23), transparent 34%), linear-gradient(135deg, rgba(15,23,42,0.98), rgba(15,23,42,0.74)); border:1px solid rgba(56,189,248,0.32); box-shadow:0 28px 70px rgba(0,0,0,0.24); }
.p6-kicker { color:#38BDF8; font-size:0.78rem; font-weight:950; letter-spacing:0.16em; text-transform:uppercase; margin-bottom:15px; }
.p6-title { color:#F8FAFC; font-size:2.55rem; line-height:1.05; font-weight:950; letter-spacing:-0.035em; max-width:1040px; }
.p6-title span { color:#38BDF8; }
.p6-body { color:#E2E8F0; font-size:1.10rem; line-height:1.65; margin-top:18px; max-width:1180px; }
.p6-flow-strip { margin-top:24px; display:grid; grid-template-columns:repeat(7, minmax(0, 1fr)); gap:10px; }
.p6-flow-step { border:1px solid color-mix(in srgb, var(--step-color, #38BDF8) 45%, transparent); border-radius:16px; padding:13px 12px; background:linear-gradient(135deg, color-mix(in srgb, var(--step-color, #38BDF8) 16%, transparent), rgba(2,6,23,0.56)); min-height:78px; }
.p6-flow-step strong { color:#F8FAFC; font-size:0.96rem; display:block; margin-bottom:4px; }
.p6-flow-step span { color:#CBD5E1; font-size:0.82rem; line-height:1.25; }
.p6-flow-step strong { color:var(--step-color, #F8FAFC); }
.p6-section-title { display:flex; align-items:flex-start; gap:14px; margin:42px 0 12px 0; }
.p6-section-num { border:1px solid rgba(56,189,248,0.45); color:#38BDF8; border-radius:11px; padding:9px 12px; font-family:'IBM Plex Mono','Roboto Mono',monospace; font-weight:950; background:rgba(14,116,144,0.24); }
.p6-section-title h2 { color:#F8FAFC; font-size:1.72rem; line-height:1.12; margin:0 0 8px 0; font-weight:950; }
.p6-section-title p { color:#CBD5E1; margin:0; font-size:1.03rem; line-height:1.4; }
.p6-intro { color:#E2E8F0; font-size:1.04rem; line-height:1.65; font-weight:650; max-width:1180px; margin:0 0 16px 56px; }
.p6-intro b { color:#F8FAFC; }
.p6-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.p6-grid-3 { display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; }
.p6-grid-4 { display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; }
.p6-card { border:1px solid rgba(148,163,184,0.24); border-left:5px solid var(--accent); border-radius:18px; background:rgba(15,23,42,0.82); padding:18px 20px; min-height:132px; box-shadow:0 14px 34px rgba(0,0,0,0.15); }
.p6-card-label { color:var(--accent); font-size:0.74rem; font-weight:950; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:9px; }
.p6-card-title { color:#F8FAFC; font-size:1.20rem; font-weight:950; line-height:1.18; margin-bottom:9px; }
.p6-card-body { color:#CBD5E1; font-size:0.97rem; line-height:1.48; font-weight:650; }
.p6-panel { border:1px solid rgba(56,189,248,0.26); border-radius:22px; background:linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.78)); padding:24px; margin:14px 0 18px 0; }
.p6-panel h3 { color:#F8FAFC; margin-top:0; font-size:1.25rem; }
.p6-note { border:1px solid rgba(245,158,11,0.28); border-radius:18px; padding:17px 19px; background:rgba(245,158,11,0.07); color:#FDE68A; line-height:1.52; font-weight:750; margin:12px 0 16px 0; }
.p6-v2-note { border:1px solid rgba(168,85,247,0.36); border-radius:18px; padding:17px 19px; background:rgba(88,28,135,0.18); color:#E9D5FF; line-height:1.52; font-weight:750; margin:12px 0 16px 0; }
.p6-table { width:100%; border-collapse:collapse; border-radius:14px; overflow:hidden; border:1px solid rgba(56,189,248,0.36); margin:12px 0 18px 0; background:rgba(15,23,42,0.86); }
.p6-table th { background:rgba(14,116,144,0.54); color:#38BDF8; text-align:left; padding:11px 12px; font-size:0.76rem; letter-spacing:0.08em; text-transform:uppercase; border:1px solid rgba(125,211,252,0.20); }
.p6-table td { background:rgba(30,41,59,0.72); color:#E2E8F0; padding:11px 12px; border:1px solid rgba(148,163,184,0.22); font-size:0.92rem; line-height:1.36; vertical-align:top; }
.p6-table tr:nth-child(even) td { background:rgba(51,65,85,0.64); }
.p6-table td:first-child { color:#F8FAFC; font-weight:850; }
.p6-table-small td { font-size:0.84rem; padding:8px 9px; }
.p6-table-small th { font-size:0.70rem; padding:8px 9px; }
.p6-table-compact { max-width:980px; margin-left:auto; margin-right:auto; }
.p6-figure { margin:12px 0 18px 0; border:1px solid rgba(56,189,248,0.28); border-radius:20px; background:rgba(2,6,23,0.45); padding:14px; }
.p6-figure.compact { max-width:980px; margin-left:auto; margin-right:auto; }
.p6-figure.heatmap { max-width:760px; margin-left:auto; margin-right:auto; }
.p6-figure img { width:100%; border-radius:14px; display:block; background:white; }
.p6-figure figcaption { color:#94A3B8; font-size:0.88rem; font-weight:700; margin-top:10px; text-align:center; }
.p6-missing { border:1px dashed rgba(248,113,113,0.45); border-radius:16px; padding:18px; color:#FCA5A5; background:rgba(127,29,29,0.18); margin:12px 0; }
.p6-warning-list { margin:0; padding-left:1.15rem; color:#CBD5E1; line-height:1.65; font-size:0.98rem; }
.p6-evidence-a { border-left-color:#22C55E !important; }
.p6-evidence-b { border-left-color:#F59E0B !important; }
.p6-evidence-c { border-left-color:#EF4444 !important; }
.p6-evidence-d { border-left-color:#A855F7 !important; }
div[data-testid="stButton"] > button { background:linear-gradient(180deg, #38BDF8, #2563EB) !important; color:#F8FAFC !important; border:1px solid rgba(125,211,252,0.55) !important; border-radius:10px !important; box-shadow:0 0 18px rgba(56,189,248,0.28) !important; font-weight:850 !important; }
div[data-testid="stButton"] > button p { color:#F8FAFC !important; font-weight:850 !important; }
.p6-simple-footer { border-top:1px solid rgba(148,163,184,0.18); margin-top:36px; padding:22px 0 10px 0; color:#CBD5E1; line-height:1.55; }
.p6-simple-footer b { color:#F8FAFC; }
@media (max-width:1100px) { .p6-flow-strip, .p6-grid-4, .p6-grid-3, .p6-grid-2 { grid-template-columns:1fr 1fr; } }
@media (max-width:760px) { .p6-flow-strip, .p6-grid-4, .p6-grid-3, .p6-grid-2 { grid-template-columns:1fr; } .p6-title{font-size:2rem;} .p6-intro{margin-left:0;} }
</style>
"""
)


# =============================================================================
# PAGE CONTENT
# =============================================================================

html("<div class='p6-page'>")

left, right = st.columns([1, 0.26])
with left:
    html(
        """
        <div class='p6-brand'>
            <div class='p6-logo'>✦</div>
            <div>
                <div class='p6-brand-title'>EUROPEAN<br>STRATEGY ATLAS</div>
                <div class='p6-brand-subtitle'>Methods • Assumptions • Validation • App logic</div>
            </div>
        </div>
        """
    )
with right:
    if st.button("← Return to Atlas", use_container_width=True, key="p6_return_top"):
        safe_switch_page("pages/p0_landing.py")

html(
    """
    <div class='p6-hero'>
        <div class='p6-kicker'>How it was made</div>
        <div class='p6-title'>From public data to a <span>transparent methodology appendix.</span></div>
        <div class='p6-body'>
            This page explains the Atlas construction logic: how KPIs become dimensions, how countries become structural families,
            how tradeoffs receive evidence levels, and how the strategy and challenge engines translate analysis into an educational app.
        </div>
        <div class='p6-flow-strip'>
            <div class='p6-flow-step' style='--step-color:#38BDF8;'><strong>Data</strong><span>Public European indicators</span></div>
            <div class='p6-flow-step' style='--step-color:#22D3EE;'><strong>KPIs</strong><span>19 cleaned signals</span></div>
            <div class='p6-flow-step' style='--step-color:#4ADE80;'><strong>Dimensions</strong><span>7 structural lenses</span></div>
            <div class='p6-flow-step' style='--step-color:#A855F7;'><strong>Families</strong><span>Context and topology</span></div>
            <div class='p6-flow-step' style='--step-color:#F59E0B;'><strong>Tradeoffs</strong><span>Relationships and evidence</span></div>
            <div class='p6-flow-step' style='--step-color:#FACC15;'><strong>Engines</strong><span>Strategy and challenge logic</span></div>
            <div class='p6-flow-step' style='--step-color:#EF4444;'><strong>Limits</strong><span>What Atlas is not</span></div>
        </div>
    </div>
    """
)

section("01", "What is Atlas?", "An educational system for exploring structural pathways, not a ranking or forecasting model.")
intro("Atlas was designed to solve a communication problem: European public data is rich, but hard to interpret as a system. The app turns fragmented indicators into a guided learning path so users can compare pathways, investigate tradeoffs, test simplified strategies, and reflect on what changed.")
html(
    "<div class='p6-grid-3'>"
    + card("Goal", "Make complexity explorable", "Atlas translates fragmented public data into guided structural learning.", "#38BDF8")
    + card("Core idea", "Rankings explain where, not how", "The app focuses on pathways, tradeoffs, context, and questions.", "#A855F7")
    + card("Boundary", "Exploratory only", "No forecasts, no causal claims, no policy recommendations, and no official ranking.", "#F59E0B")
    + "</div>"
)

section("02", "Data foundation", "The app starts from public European indicators and turns them into an app-ready country-year panel.")
intro("The KPI layer was chosen to cover the core structural themes used throughout the project: innovation, sustainability, human capital, social stability, fiscal flexibility, security reprioritization, and adaptive transformation. The table is intentionally compact: it documents what each signal contributes without turning the page into a data dictionary.")
html(
    "<div class='p6-grid-4'>"
    + card("Coverage", "27 EU countries", "The Atlas compares European structural patterns across countries.", "#38BDF8")
    + card("Period", "2014–2025", "The period covers baseline, COVID transition, and energy/geopolitical transition.", "#22C55E")
    + card("Inputs", "19 KPIs", "Economic, social, innovation, sustainability, fiscal, and spending indicators.", "#F59E0B")
    + card("Outputs", "7 dimensions", "Composite structural lenses used throughout the app.", "#A855F7")
    + "</div>"
)
html(table_html(["KPI", "Source", "Used in"], KPI_ROWS, small=True, compact_width=True))

section("03", "From KPIs to dimensions", "The translation layer makes the model explainable instead of hiding raw indicators behind a single score.")
intro("Raw indicators are not directly comparable: debt, emissions, education, R&D, and public spending have different units and meanings. The Atlas therefore translates cleaned KPIs into seven interpretable structural dimensions. Each dimension keeps its equation visible, so the user can see the modeling assumption behind the app output.")
html(img_block("p6_sankey_translation_crop.png", "KPI → Dimension → Output translation layer."))
html(table_html(["Dimension", "Interpretation", "Equation", "Output supported"], DIMENSION_ROWS))

section("04", "Normalization framework", "Different analytical lenses answer different questions.")
intro("Normalization was one of the most important methodological decisions. Absolute values show what happened, EU-relative scores show where a country sits compared with Europe, and country-relative scores show how a country changed compared with its own history. Static and dynamic metrics are kept separate because current position and transition behavior are not the same thing.")
html(
    "<div class='p6-grid-2'>"
    + "<div class='p6-panel'><h3>Normalization perspectives</h3>" + table_html(["Perspective", "Question", "Use"], NORMALIZATION_ROWS, small=True) + "</div>"
    + "<div class='p6-panel'><h3>Transition periods</h3>" + table_html(["Period", "Years", "Interpretation"], PERIOD_ROWS, small=True) + "</div>"
    + "</div>"
)
html(table_html(["Dynamic metric", "Calculation", "Interpretation"], DYNAMIC_ROWS))
html(
    """
    <div class='p6-v2-note'>
        Static vs Dynamic was validated as an analytical lens, but the graduation current version exposes it only partially. In this version, it is documented as methodology and future direction rather than presented as a fully interactive feature.
    </div>
    """
)
html(img_block("p6_static_dynamic_crop.png", "Static position vs dynamic gain — shown as a validated analytical lens and V2 boundary.", compact=True))

section("05", "Structural families", "Families provide context: similar profiles often share structural tensions even when rankings differ.")
intro("Families were developed to avoid treating Europe as one universal model. Countries were first represented by their seven structural dimensions, then grouped by similarity, checked with clustering diagnostics, and finally reviewed through anchors, bridges, and outliers. Bridges are countries that share meaningful similarity with more than one family or behave differently across static and dynamic lenses.")
html(
    "<div class='p6-grid-3'>"
    + card("Step 1", "Build structural profiles", "Represent each country by its seven dimension scores.", "#38BDF8")
    + card("Step 2", "Cluster + validate", "Use similarity, elbow/silhouette checks, bridge review, and outlier review.", "#8B5CF6")
    + card("Step 3", "Interpret families", "Assign labels that explain pathway context, not winners and losers.", "#F59E0B")
    + "</div>"
)
html(img_block("p6_structural_families_map_clean.png", "Final structural families map used for methodology explanation."))
html(table_html(["Family", "Members", "Interpretation", "Anchors / bridges"], FAMILY_ROWS))

section("06", "Heatmap → families", "The heatmap was an intermediate validation artifact, not a final app ranking.")
intro("This uploaded heatmap compares representative countries across outcome and investment-pathway signals. It helped check whether the final family labels were plausible before simplifying them for the app. The important message is not the numeric score in each cell; it is the repeated pattern across rows that supported family interpretation.")
html(
    "<div class='p6-grid-2'>"
    + "<div class='p6-panel'><h3>How to read it</h3><ul class='p6-warning-list'><li>Rows are representative countries or archetypes.</li><li>Columns are integrated structural dimensions and investment-pathway signals.</li><li>Green cells mark stronger positive signals; red cells mark weaker or negative signals.</li><li>The heatmap helped move from many dimensions toward interpretable structural families.</li></ul></div>"
    + img_block("p6_heatmap_families_crop.png", "Integrated EU structural archetype heatmap used as family-validation evidence.", compact=True).replace("p6-figure compact", "p6-figure heatmap")
    + "</div>"
)
html(
    """
    <div class='p6-note'>
        This artifact supports methodology only. It is not an app ranking, not a country scorecard, and not a prediction.
    </div>
    """
)

section("07", "Tradeoff analysis", "Context changes the story: the same relationship can behave differently by family.")
intro("Tradeoff analysis screens whether two structural dimensions move together, oppose each other, or behave differently by family. The app uses these relationships to ask better questions: is the pattern visible across Europe, only inside one family, or too weak to treat as a conclusion? This is why P2 emphasizes context rather than a single universal rule.")
html(img_block("p6_context_tradeoffs_crop.png", "Tradeoff relationships can be universal, weak/conditional, or family-specific."))
html(
    """
    <div class='p6-note'>
        Correlations are used as evidence-guided prompts. They do not prove causality. A weak EU-wide relationship can still be useful when a family-specific pattern appears.
    </div>
    """
)

section("08", "Evidence framework ABCD", "Evidence levels control how strongly the app should interpret a relationship.")
intro("Evidence levels translate analysis quality into app language. Stronger relationships can be described more confidently; weaker relationships are used mainly as prompts. To reduce redundancy, the current version page shows this as four traffic-light cards instead of repeating the same information in a separate table.")
html(
    "<div class='p6-grid-4'>"
    + card("A", "Strong", "Consistent and interpretable; used as a relatively strong educational signal.", "#22C55E")
    + card("B", "Moderate", "Useful but interpreted with context or family limits.", "#F59E0B")
    + card("C", "Weak", "Conditional or family-specific; mostly used to raise questions.", "#EF4444")
    + card("D", "Exploratory", "Question-generating only; not treated as a conclusion.", "#A855F7")
    + "</div>"
)

section("09", "Strategy engine", "The strategy sandbox translates investment priorities into structural output changes using evidence-weighted relationships.")
intro("The strategy engine does not claim that public investment directly creates outcomes. It uses a simplified educational chain: investment priorities influence structural dimensions, dimensions influence outputs, and evidence weights control how strongly each relationship is applied. The goal is to make tradeoffs visible, not to optimize policy.")
html(table_html(["Investment lever", "Target dimension", "Evidence", "Direction", "Notes"], STRATEGY_ROWS, small=True))
html(
    """
    <div class='p6-note'>
        Investments first influence structural dimensions. Evidence weights determine relationship strength. Family-specific overrides capture different development pathways.
    </div>
    """
)

section("10", "Challenge engine", "Challenge Mode tests how a selected strategy behaves under simplified external disruptions.")
intro("The challenge engine represents external disruption in a transparent way. Energy Crisis and Pandemic Pressure are simplified scenario assumptions inspired by the observed transition periods. The user first sees damage, then allocates a recovery response, and finally compares whether resilience improved or pressure moved elsewhere.")
html(table_html(["Shock type", "Based on", "Affected dimensions"], CHALLENGE_ROWS))
html(
    """
    <div class='p6-note'>
        Low, Medium, and High strengths act as scenario multipliers. The challenge engine is a learning model, not a prediction model.
    </div>
    """
)

section("11", "Validation framework", "Validation focused on plausibility, transparency, and consistency rather than prediction.")
intro("Validation sits near the end because it checks the whole chain: dimensions, families, tradeoffs, drivers, and app behavior. The goal was not to prove a causal model, but to make sure the framework behaves plausibly and consistently enough for educational exploration.")
html(
    "<div class='p6-grid-4'>"
    + card("Dimensions", "KPI + weight validation", "Checked direction, interpretation, and whether each dimension behaves plausibly.", "#38BDF8")
    + card("Families", "Anchors, bridges, outliers", "Reviewed representative countries, borderline cases, and unusual profiles.", "#8B5CF6")
    + card("Tradeoffs", "Correlation + context", "Screened relationships globally and by family context.", "#F59E0B")
    + card("Drivers", "RCA-style review", "Reviewed mechanisms behind Human Capital, Innovation, Security, and Sustainability.", "#22C55E")
    + "</div>"
)
html(table_html(["Area", "Driver logic", "Validation interpretation"], DRIVER_ROWS))

section("12", "Learning journey", "The final product is a guided learning experience rather than a static dashboard.")
intro("Each app page answers a different question and passes context forward. The user observes a country, investigates relationships, chooses a strategy, challenges it under disruption, and reflects on the learning trail. This is why the Atlas is structured as a guided journey rather than a collection of disconnected charts.")
html(img_block("p6_app_journey_crop.png", "Observe → Investigate → Choose → Challenge → Reflect."))

section("13", "Assumptions and limits", "The Atlas is useful because its assumptions are visible.")
intro("The methodology is intentionally transparent about what it can and cannot support. Composite indicators make complexity easier to explore, but they also simplify reality. Evidence levels guide interpretation, not certainty. The app should help users ask better structural questions rather than produce definitive answers.")
html(
    "<div class='p6-grid-2'>"
    + "<div class='p6-panel'><h3>Key assumptions</h3><ul class='p6-warning-list'><li>Public data can reveal structural tendencies.</li><li>Composite dimensions simplify complex systems.</li><li>Family context helps interpret patterns.</li><li>Evidence levels guide interpretation, not certainty.</li></ul></div>"
    + "<div class='p6-panel'><h3>What Atlas is not</h3><ul class='p6-warning-list'><li>Not a forecast.</li><li>Not a policy recommendation system.</li><li>Not causal inference.</li><li>Not an official country ranking.</li></ul></div>"
    + "</div>"
)

section("14", "Return to Atlas", "Continue exploring countries, tradeoffs, strategies, and resilience pathways.")
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("← Return to Atlas", use_container_width=True, key="p6_return_bottom"):
        safe_switch_page("pages/p0_landing.py")

render_p6_footer()
html("</div>")
