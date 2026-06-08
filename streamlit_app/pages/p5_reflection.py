"""
p5_reflection_v05_pdf_next_mission.py

Purpose
-------
Page 5 of the European Strategy Atlas.

This page closes the learning journey by turning the Atlas exploration into a
compact mission debrief: what was observed, what repeated, what mattered, and
what the user should explore next.
"""

from pathlib import Path

import streamlit as st

from components.typography import render_section_title
from components.cards import (
    render_atlas_card,
    render_hero_card,
    render_delta_card,
    render_ai_insight_panel,
)
from components.page_frame import (
    render_left_rail_placeholder,
    render_footer,
)


# =============================================================================
# LOAD GLOBAL CSS
# =============================================================================

def load_css():
    css_file = (
        Path(__file__).parent.parent / "styles" / "atlas_theme.css"
    )

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


load_css()


# =============================================================================
# P5 PAGE-SPECIFIC CSS
# =============================================================================

st.html(
    """
    <style>
    .p5-green-panel {
        border:1px solid rgba(74,222,128,0.34);
        border-radius:18px;
        background:linear-gradient(135deg, rgba(20,83,45,0.32), rgba(15,23,42,0.82));
        padding:18px 20px;
        margin:8px 0 16px 0;
        box-shadow:0 0 24px rgba(74,222,128,0.08);
    }
    .p5-journey-card-v2 {
        border:1px solid rgba(74,222,128,0.36);
        border-radius:18px;
        background:linear-gradient(135deg, rgba(20,83,45,0.28), rgba(15,23,42,0.84));
        padding:22px 24px;
        margin:8px 0 18px 0;
    }
    .p5-journey-track-v2 {
        display:grid;
        grid-template-columns: repeat(5, 1fr);
        gap:14px;
        align-items:stretch;
    }
    .p5-journey-step-v2 {
        border:1px solid rgba(148,163,184,0.24);
        border-radius:16px;
        background:rgba(15,23,42,0.78);
        padding:15px 14px;
        min-height:132px;
    }
    .p5-journey-step-v2.current {
        border-color:rgba(74,222,128,0.70);
        box-shadow:0 0 22px rgba(74,222,128,0.20);
    }
    .p5-step-num {
        color:#4ADE80;
        font-family:'IBM Plex Mono','Roboto Mono',monospace;
        font-size:1.18rem;
        font-weight:950;
        margin-bottom:8px;
    }
    .p5-step-title {
        color:#F8FAFC;
        font-size:1.08rem;
        font-weight:950;
        line-height:1.15;
        margin-bottom:8px;
    }
    .p5-step-text {
        color:#CBD5E1;
        font-size:0.91rem;
        font-weight:700;
        line-height:1.35;
    }
    .p5-journey-caption-v2 {
        color:#E2E8F0;
        font-size:1.05rem;
        line-height:1.45;
        font-weight:750;
        margin-top:16px;
        padding-top:14px;
        border-top:1px solid rgba(148,163,184,0.18);
    }
    .p5-pattern-grid {
        display:grid;
        grid-template-columns: repeat(4, 1fr);
        gap:14px;
        margin:10px 0 14px 0;
    }
    .p5-pattern-card {
        border:1px solid rgba(148,163,184,0.24);
        border-left:5px solid var(--accent);
        border-radius:16px;
        background:rgba(15,23,42,0.80);
        padding:16px 17px;
        min-height:152px;
        box-shadow:0 0 20px rgba(0,0,0,0.18);
    }
    .p5-pattern-label {
        color:var(--accent);
        font-size:0.72rem;
        font-weight:950;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:9px;
    }
    .p5-pattern-value {
        color:#F8FAFC;
        font-size:1.12rem;
        font-weight:950;
        line-height:1.18;
        margin-bottom:9px;
    }
    .p5-pattern-text {
        color:#CBD5E1;
        font-size:0.88rem;
        line-height:1.35;
        font-weight:700;
    }
    .p5-log-summary-grid {
        display:grid;
        grid-template-columns: repeat(5, 1fr);
        gap:12px;
        margin:10px 0 16px 0;
    }
    .p5-log-summary-card {
        border:1px solid rgba(74,222,128,0.28);
        border-radius:15px;
        background:rgba(15,23,42,0.78);
        padding:14px 15px;
        min-height:122px;
    }
    .p5-log-label {
        color:#86EFAC;
        font-size:0.70rem;
        font-weight:950;
        letter-spacing:0.09em;
        text-transform:uppercase;
        margin-bottom:8px;
    }
    .p5-log-value {
        color:#F8FAFC;
        font-size:1.04rem;
        font-weight:950;
        line-height:1.18;
        margin-bottom:8px;
    }
    .p5-log-text {
        color:#CBD5E1;
        font-size:0.84rem;
        line-height:1.32;
        font-weight:700;
    }
    .p5-cta-grid {
        display:grid;
        grid-template-columns: repeat(4, 1fr);
        gap:14px;
        margin:12px 0 16px 0;
    }
    .p5-cta-card {
        border:1px solid rgba(148,163,184,0.24);
        border-left:5px solid var(--accent);
        border-radius:16px;
        background:rgba(15,23,42,0.80);
        padding:16px 17px;
        min-height:142px;
    }
    .p5-cta-label {
        color:#94A3B8;
        font-size:0.70rem;
        font-weight:950;
        letter-spacing:0.10em;
        text-transform:uppercase;
        margin-bottom:8px;
    }
    .p5-cta-title {
        color:var(--accent);
        font-size:1.12rem;
        font-weight:950;
        line-height:1.18;
        margin-bottom:8px;
    }
    .p5-cta-text {
        color:#CBD5E1;
        font-size:0.86rem;
        line-height:1.35;
        font-weight:700;
    }
    div[data-testid="stDownloadButton"] > button {
        background:linear-gradient(180deg, #38BDF8, #2563EB) !important;
        color:#F8FAFC !important;
        border:1px solid rgba(125,211,252,0.55) !important;
        border-radius:10px !important;
        box-shadow:0 0 18px rgba(56,189,248,0.28) !important;
        font-weight:800 !important;
    }
    div[data-testid="stDownloadButton"] > button p {
        color:#F8FAFC !important;
        font-weight:800 !important;
    }
    @media (max-width: 1100px) {
        .p5-journey-track-v2, .p5-pattern-grid, .p5-log-summary-grid, .p5-cta-grid {
            grid-template-columns:1fr 1fr;
        }
    }
    </style>
    """
)


# =============================================================================
# NAVIGATION HELPER
# =============================================================================

def safe_switch_page(page_path: str):
    try:
        st.switch_page(page_path)
    except Exception:
        st.info(f"Navigation target not found: {page_path}")


def _pdf_escape(text):
    """Escape text for a minimal built-in PDF writer."""
    text = str(text)
    replacements = {
        "→": "->",
        "↔": "<->",
        "—": "-",
        "–": "-",
        "✓": "OK",
        "Δ": "Delta",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_pdf_line(text, width=92):
    """Simple word wrap for PDF text lines."""
    words = str(text).split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def get_country_report_profile(selected_country):
    """MVP report profile used by the P5 PDF export."""
    profiles = {
        "Germany": {
            "family": "Industrial / Transition Systems",
            "family_description": (
                "A structurally mature industrial pathway with strong innovation capacity, "
                "visible transformation strengths, and recurring fiscal/sustainability tradeoffs."
            ),
            "kpis": [
                ("Innovation Capacity", 62),
                ("Social Stability", 59),
                ("Adaptive Transformation", 55),
                ("Security Reprioritization", 50),
                ("Fiscal Flexibility", 49),
                ("Human Capital Capacity", 47),
                ("Sustainability Capacity", 42),
            ],
        },
        "Sweden": {
            "family": "Innovation Core / Nordic Frontier",
            "family_description": "A high-capacity transition pathway with strong sustainability and innovation signals.",
            "kpis": [],
        },
        "Romania": {
            "family": "Adaptive / Peripheral Systems",
            "family_description": "A convergence-oriented pathway where structural change and capacity-building are central.",
            "kpis": [],
        },
    }
    return profiles.get(
        selected_country,
        {
            "family": "Selected structural family",
            "family_description": "Family description will be generated from the Atlas metadata in a future version.",
            "kpis": [],
        },
    )


def _ascii_bar(value, width=24):
    """Return a simple fixed-width bar for PDF text output."""
    value = max(0, min(100, int(round(value))))
    filled = int(round(width * value / 100))
    return "█" * filled + "░" * (width - filled)


def build_reflection_pdf_bytes(selected_country, selected_reference):
    """Create a lightweight PDF containing summary, KPI bars, family context, disclaimers, and log table."""
    profile = get_country_report_profile(selected_country)
    log_rows = [
        ("P1 Observe", "Country profile review", "Innovation capacity appeared as a structural strength."),
        ("P2 Investigate", "Relationship exploration", "Innovation and fiscal flexibility appeared as a recurring tension."),
        ("P3 Choose", "Strategy test", "Sustainability improved, while tradeoffs remained visible."),
        ("P4 Challenge", "Energy shock review", "Fiscal flexibility became a key vulnerability under disruption."),
        ("P5 Reflect", "Learning debrief", "The journey highlighted tradeoffs rather than one optimal answer."),
    ]

    content_lines = [
        "European Strategy Atlas - Reflection Summary",
        "",
        f"Country: {selected_country}",
        f"Reference: {selected_reference}",
        f"Structural family: {profile['family']}",
        "",
        "Family context:",
        profile["family_description"],
        "",
        "Journey: Observe -> Investigate -> Choose -> Challenge -> Reflect",
        "",
        "Core pattern:",
        f"{selected_country} showed recurring Innovation Capacity strength while Fiscal Flexibility remained the main pressure point.",
        "",
        "Country KPI bars (0-100 structural index):",
    ]

    if profile["kpis"]:
        for name, value in profile["kpis"]:
            content_lines.append(f"{name:<30} {_ascii_bar(value)} {value:>3}/100")
    else:
        content_lines.append("KPI bar profile will be generated from the Atlas data in a future version.")

    content_lines.extend([
        "",
        "Bottom line:",
        "The exploration highlights tradeoffs rather than one optimal pathway. Strategy can improve one side of the system while exposing another constraint.",
        "",
        "Disclaimers:",
        "- Educational exploration only; not a forecast, prediction, or policy recommendation.",
        "- Composite scores are simplified structural indicators, not official rankings.",
        "- Observed relationships are associative patterns, not causal claims.",
        "- Strategy and challenge results are illustrative scenario assumptions for learning.",
        "",
        "Next question:",
        "Would another country or structural family show the same pattern?",
        "",
        "Mission Log Table:",
        "Stage | Action | Main finding",
        "-" * 78,
    ])

    for stage, action, finding in log_rows:
        content_lines.append(f"{stage} | {action} | {finding}")

    pdf_text_lines = []
    for line in content_lines:
        pdf_text_lines.extend(_wrap_pdf_line(line, width=88))

    text_stream = ["BT", "/F1 10 Tf", "42 800 Td", "12 TL"]
    first = True
    for line in pdf_text_lines[:62]:
        safe_line = _pdf_escape(line)
        if first:
            text_stream.append(f"({safe_line}) Tj")
            first = False
        else:
            text_stream.append(f"T* ({safe_line}) Tj")
    text_stream.append("ET")
    stream = "\n".join(text_stream).encode("latin-1", "replace")

    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode())
    return bytes(pdf)


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.markdown("## P5 — Reflection & Learning")
st.caption("Mission Debrief: summarize the exploration, capture learning, and choose the next Atlas path.")

st.html(
    """
    <div class="p5-green-panel">
        <div style="color:#86EFAC; font-size:0.78rem; font-weight:950; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:8px;">What this page does</div>
        <div style="color:#E2E8F0; font-size:1.10rem; line-height:1.50; font-weight:760;">
            We reached the end of this exploration mission. This page collects the learning trail from <b>Observe → Investigate → Choose → Challenge</b> and turns it into a short debrief: what repeated, what mattered, what remained uncertain, and where to continue.
        </div>
    </div>
    """
)


# =============================================================================
# TOP CONTEXT — SHARED FRAME
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
                <div class="p1-brand-title">REFLECT<br>& LEARN</div>
                <div class="p1-brand-subtitle">Summarize exploration.<br>Export learning.</div>
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
        index=1,
    )

with top_col_ref_country:
    if selected_reference == "Another Country":
        reference_country = st.selectbox(
            "Reference Country",
            options=["Sweden", "Romania", "Italy", "Poland"],
            index=0,
        )
    else:
        reference_country = None
        st.text_input(
            "Reference Country",
            value="-----------",
            disabled=True,
        )

with top_col4:
    view_mode = st.radio(
        "View Mode",
        options=["Relative", "Absolute"],
        horizontal=True,
        index=0,
    )


# =============================================================================
# P5 CONTEXT RIBBON
# =============================================================================

st.html(
    f"""
    <div class="p1-kpi-ribbon">
        <div class="p1-kpi-card">
            <div class="p1-kpi-label">CURRENT PAGE</div>
            <div class="p1-kpi-main">P5 Reflection</div>
            <div class="p1-kpi-sub">Learning summary stage</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#38BDF8;">COUNTRY</div>
            <div class="p1-kpi-main">{selected_country}</div>
            <div class="p1-kpi-sub">Explored system</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#4ADE80;">QUESTIONS</div>
            <div class="p1-kpi-number" style="color:#4ADE80;">4</div>
            <div class="p1-kpi-sub">Learning count</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F59E0B;">CHALLENGES</div>
            <div class="p1-kpi-number" style="color:#F59E0B;">1</div>
            <div class="p1-kpi-sub">Learning count</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#A855F7;">EXPORT</div>
            <div class="p1-kpi-main">Ready</div>
            <div class="p1-kpi-sub">Learning summary</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label">REFERENCE</div>
            <div class="p1-kpi-main">{selected_reference}</div>
            <div class="p1-kpi-sub">Comparison context</div>
        </div>
    </div>
    """
)


# =============================================================================
# THREE-COLUMN PAGE FRAME
# =============================================================================

left_col, main_col, right_col = st.columns(
    [0.85, 5.4, 1.15],
    gap="medium",
)

sections = [
    ("01", "JOURNEY", "Review what happened."),
    ("02", "PATTERNS", "Identify recurring signals."),
    ("03", "MISSION LOG", "Review activity."),
    ("04", "BOTTOM LINE", "Final reflection."),
    ("05", "NEXT", "Save or continue."),
]

with left_col:
    render_left_rail_placeholder(
        page_number=5,
        page_title="Reflection",
        sections=sections,
    )


with main_col:

       # =========================================================================
    # SECTION 01
    # =========================================================================

    render_section_title(
        number="01",
        title="What did this journey cover?",
        subtitle="Review the Atlas path from observing a country to reflecting on what the exploration taught you.",
    )

    st.html(
        f"""
        <div class="p5-journey-card-v2">
            <div class="p5-journey-track-v2">
                <div class="p5-journey-step-v2">
                    <div class="p5-step-num">01</div>
                    <div class="p5-step-title">Observe</div>
                    <div class="p5-step-text">Locate {selected_country} structurally and identify its strongest capabilities and constraints.</div>
                </div>
                <div class="p5-journey-step-v2">
                    <div class="p5-step-num">02</div>
                    <div class="p5-step-title">Investigate</div>
                    <div class="p5-step-text">Explore relationships, tradeoffs, families, and exceptions behind the country profile.</div>
                </div>
                <div class="p5-journey-step-v2">
                    <div class="p5-step-num">03</div>
                    <div class="p5-step-title">Choose</div>
                    <div class="p5-step-text">Build a strategy package and test how priorities may shift structural outputs.</div>
                </div>
                <div class="p5-journey-step-v2">
                    <div class="p5-step-num">04</div>
                    <div class="p5-step-title">Challenge</div>
                    <div class="p5-step-text">Apply disruption, observe damage, and test whether adaptation can recover resilience.</div>
                </div>
                <div class="p5-journey-step-v2 current">
                    <div class="p5-step-num">05</div>
                    <div class="p5-step-title">Reflect</div>
                    <div class="p5-step-text">Turn the journey into learning: what mattered, what repeated, and what to explore next.</div>
                </div>
            </div>
            <div class="p5-journey-caption-v2">
                This page is the Mission Debrief. It does not introduce a new model; it summarizes the learning trail created across P1–P4.
            </div>
        </div>
        """
    )

    # =========================================================================
    # SECTION 02
    # =========================================================================

    render_section_title(
        number="02",
        title=f"Which patterns appeared for {selected_country}?",
        subtitle="Read the recurring signals from the completed Atlas journey.",
    )

    st.html(
        f"""
        <div class="p5-pattern-grid">
            <div class="p5-pattern-card" style="--accent:#4ADE80;">
                <div class="p5-pattern-label">Repeated Strength</div>
                <div class="p5-pattern-value">Innovation Capacity</div>
                <div class="p5-pattern-text">{selected_country} repeatedly appears strongest where capability-building and innovation signals are visible.</div>
            </div>
            <div class="p5-pattern-card" style="--accent:#F59E0B;">
                <div class="p5-pattern-label">Repeated Constraint</div>
                <div class="p5-pattern-value">Fiscal Flexibility</div>
                <div class="p5-pattern-text">The main pressure point returns when strategy and disruption are interpreted together.</div>
            </div>
            <div class="p5-pattern-card" style="--accent:#A855F7;">
                <div class="p5-pattern-label">Recurring Tradeoff</div>
                <div class="p5-pattern-value">Innovation ↔ Fiscal</div>
                <div class="p5-pattern-text">The useful question is not whether one side wins, but how much pressure appears elsewhere.</div>
            </div>
            <div class="p5-pattern-card" style="--accent:#38BDF8;">
                <div class="p5-pattern-label">What This Means</div>
                <div class="p5-pattern-value">No free pathway</div>
                <div class="p5-pattern-text">Every pathway creates a mix of strengths, constraints, and next questions.</div>
            </div>
        </div>
        <div class="p5-green-panel">
            <div style="color:#86EFAC; font-size:0.76rem; font-weight:950; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:8px;">Pattern Summary</div>
            <div style="color:#E2E8F0; font-size:1.06rem; line-height:1.50; font-weight:760;">
                For {selected_country}, the core pattern is a structural tension: capability-building can improve one side of the system while exposing another pressure point. The Atlas does not select a winner; it makes the tradeoff visible.
            </div>
        </div>
        """
    )

    # =========================================================================
    # SECTION 03
    # =========================================================================

    render_section_title(
        number="03",
        title="What did the Mission Log record?",
        subtitle="A compact record of the exploration path and the main finding from each stage.",
    )

    st.html(
        f"""
        <div class="atlas-mission-table-card">
            <div class="atlas-mission-table-title">Mission Log Summary</div>
            <div class="atlas-mission-table-subtitle">
                The table keeps only the essence: stage, action, learning, and how that learning feeds the final reflection.
            </div>

            <div class="atlas-mission-table-wrap p5-log-scroll">
                <table class="atlas-mission-table">
                    <thead>
                        <tr>
                            <th>Stage</th>
                            <th>Action</th>
                            <th>Core learning</th>
                            <th>Feeds into</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>P1 Observe</td>
                            <td>Country profile review</td>
                            <td>{selected_country} has a distinct profile with visible strengths and constraints.</td>
                            <td>Comparison and tradeoff exploration.</td>
                        </tr>
                        <tr>
                            <td>P2 Investigate</td>
                            <td>Relationship exploration</td>
                            <td>Innovation and fiscal flexibility appear as a recurring tension.</td>
                            <td>Strategy choice.</td>
                        </tr>
                        <tr>
                            <td>P3 Choose</td>
                            <td>Strategy test</td>
                            <td>Sustainability can improve, but tradeoffs remain visible.</td>
                            <td>Challenge testing.</td>
                        </tr>
                        <tr>
                            <td>P4 Challenge</td>
                            <td>Energy shock review</td>
                            <td>Fiscal flexibility becomes a key vulnerability under disruption.</td>
                            <td>Final reflection.</td>
                        </tr>
                        <tr>
                            <td>P5 Reflect</td>
                            <td>Learning debrief</td>
                            <td>The journey highlights tradeoffs rather than one optimal answer.</td>
                            <td>Next exploration.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
    )

    # =========================================================================
    # SECTION 04
    # =========================================================================

    render_section_title(
        number="04",
        title="Final reflections",
        subtitle="AI-supported reflection will be generated from the Mission Log in a later version. For now, this is the MVP debrief summary.",
    )

    render_ai_insight_panel(
        title="Final Reflection — AI support coming soon",
        observation=f"Across this journey, {selected_country} repeatedly appeared strong in Innovation Capacity while Fiscal Flexibility remained the main pressure point.",
        interpretation="The strongest learning is not that one strategy is best. It is that capability-building can create clear upside while exposing a different constraint under stress. In this journey, the Green Transition pathway improved sustainability logic, but the challenge step kept fiscal space visible as the limiting factor.",
        limitation="This is an educational synthesis of the demo journey. It is not a forecast, ranking, causal claim, or policy recommendation.",
        next_question="Would the same pattern appear for Sweden, Romania, or another structural family under the same strategy and challenge?",
    )

    # =========================================================================
    # SECTION 05
    # =========================================================================

    render_section_title(
        number="05",
        title=f"Thank you for exploring {selected_country}",
        subtitle="Save your learning summary or continue to the next exploration mission.",
    )

    reflection_pdf = build_reflection_pdf_bytes(
        selected_country=selected_country,
        selected_reference=selected_reference,
    )

    st.html(
        f"""
        <div class="p5-green-panel">
            <div style="color:#86EFAC; font-size:0.78rem; font-weight:950; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:8px;">Mission Complete</div>
            <div style="color:#E2E8F0; font-size:1.08rem; line-height:1.50; font-weight:760;">
                Thank you for exploring <b>{selected_country}</b>. You can save a compact PDF with the learning summary, country KPI bars, family context, disclaimers, and full mission-log table, continue exploring, or start the next mission.
            </div>
        </div>
        """
    )

    save_col, continue_col, next_col = st.columns(3, gap="medium")

    with save_col:
        st.download_button(
            "Save Summary PDF",
            data=reflection_pdf,
            file_name=f"european_strategy_atlas_{selected_country.lower()}_reflection_summary.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="p5_download_summary_pdf",
        )

    with continue_col:
        if st.button(
            "Continue Exploration",
            use_container_width=True,
            key="p5_continue_exploration",
        ):
            safe_switch_page("pages/p1_country_explorer.py")

    with next_col:
        if st.button(
            "Next Mission",
            use_container_width=True,
            key="p5_next_mission",
        ):
            safe_switch_page("pages/p0_landing.py")

    render_footer()