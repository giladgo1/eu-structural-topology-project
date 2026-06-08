"""
p0_landing.py

European Strategy Atlas landing page.

Purpose:
- orient the user
- explain what the Atlas is and is not
- introduce structural families, tradeoffs, strategy, challenge, and reflection
- frame the app before P1-P5
"""

from pathlib import Path
import base64

import streamlit as st
import streamlit.components.v1 as components

from components.typography import render_section_title
from components.page_frame import render_footer


# =============================================================================
# LOAD GLOBAL CSS
# =============================================================================

def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "atlas_theme.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


load_css()


# =============================================================================
# HERO BACKGROUND IMAGE
# =============================================================================

def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


hero_bg_path = (
    Path(__file__).parent.parent
    / "assets"
    / "p0_landing_background.png"
)

hero_bg = image_to_base64(hero_bg_path)


# =============================================================================
# PAGE HEADER
# =============================================================================

st.html(
    """
    <div class="p1-brand">
        <div class="p1-logo">✦</div>
        <div>
            <div class="p1-brand-title">EUROPEAN<br>STRATEGY ATLAS</div>
            <div class="p1-brand-subtitle">
                Explore pathways • Understand tradeoffs • Learn through experimentation
            </div>
        </div>
    </div>
    """
)


# =============================================================================
# SECTION 01 — CINEMATIC HERO
# =============================================================================

hero_html = f"""
<div class="p0-hero">
    <div class="p0-hero-bg"></div>
    <div class="p0-hero-glow"></div>

    <div class="p0-hero-content">
        <div class="p0-hero-kicker">EUROPEAN STRATEGY ATLAS</div>

        <div class="p0-hero-title">
            Explore how countries<br>
            <span>balance tradeoffs.</span>
        </div>

        <div class="p0-hero-line"></div>

        <div class="p0-hero-subtitle">
            An educational exploration tool for understanding how European countries differ,
            evolve, face tradeoffs, and respond to strategic choices.
        </div>

        <div class="p0-hero-pills">
            <div>◎ Observe</div>
            <div>⚖ Investigate</div>
            <div>◉ Choose</div>
            <div>⚡ Challenge</div>
            <div>▥ Reflect</div>
        </div>
    </div>

    <div class="p0-hero-legend">
        <div class="p0-legend-title">Structural Families</div>

        <div class="p0-family-row"><span class="dot core"></span><div><b>Innovation Core Systems</b><br>High innovation and human capital</div></div>
        <div class="p0-family-row"><span class="dot industrial"></span><div><b>Industrial / Transition Systems</b><br>Strong industry, evolving structure</div></div>
        <div class="p0-family-row"><span class="dot adaptive"></span><div><b>Adaptive / Peripheral Systems</b><br>Convergence and changing pathways</div></div>
        <div class="p0-family-row"><span class="dot bridge"></span><div><b>Bridge Systems</b><br>Between structural families</div></div>
        <div class="p0-family-row"><span class="dot transitional"></span><div><b>Transitional Systems</b><br>Mixed or still-forming profiles</div></div>
    </div>

    <div class="p0-entry-row">
        <div class="p0-entry-card blue">
            <div class="p0-entry-icon">◎</div>
            <div>
                <div class="p0-entry-title">Observe Countries</div>
                <div class="p0-entry-text">Start with a country and understand its structural profile.</div>
            </div>
        </div>

        <div class="p0-entry-card purple">
            <div class="p0-entry-icon">⌘</div>
            <div>
                <div class="p0-entry-title">Discover Families</div>
                <div class="p0-entry-text">See how countries group into different European pathways.</div>
            </div>
        </div>

        <div class="p0-entry-card cyan">
            <div class="p0-entry-icon">⚖</div>
            <div>
                <div class="p0-entry-title">Investigate Tradeoffs</div>
                <div class="p0-entry-text">Explore tensions that shape country outcomes and choices.</div>
            </div>
        </div>

        <div class="p0-entry-card amber">
            <div class="p0-entry-icon">♞</div>
            <div>
                <div class="p0-entry-title">Challenge Assumptions</div>
                <div class="p0-entry-text">Test choices under disruption and reflect on what you learned.</div>
            </div>
        </div>
    </div>
</div>

<style>
* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
}}

.p0-hero {{
    position: relative;
    min-height: 760px;
    border-radius: 34px;
    overflow: hidden;
    margin: 0;
    background: #020617;
    box-shadow: 0 28px 90px rgba(0,0,0,0.55);
    font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
}}

.p0-hero-bg {{
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(
            90deg,
            rgba(2,6,23,0.97) 0%,
            rgba(2,6,23,0.88) 30%,
            rgba(2,6,23,0.48) 58%,
            rgba(2,6,23,0.72) 100%
        ),
        url("data:image/png;base64,{hero_bg}");
    background-size: auto 91%;
    background-repeat: no-repeat;
    background-position: 70% 42%;
    filter: saturate(1.08) contrast(1.06);
}}

.p0-hero-glow {{
    position: absolute;
    width: 520px;
    height: 520px;
    right: 15%;
    top: 10%;
    background: radial-gradient(circle, rgba(56,189,248,0.24), rgba(56,189,248,0.04), transparent 70%);
    filter: blur(10px);
}}

.p0-hero-content {{
    position: absolute;
    left: 56px;
    top: 78px;
    width: 780px;
    z-index: 2;
}}

.p0-hero-kicker {{
    color: #38BDF8;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-weight: 850;
    font-size: 0.88rem;
    margin-bottom: 18px;
}}

.p0-hero-title {{
    color: #F8FAFC;
    font-size: 4.0rem;
    line-height: 0.98;
    font-weight: 900;
    letter-spacing: -0.055em;
}}

.p0-hero-title span {{
    color: #38BDF8;
    text-shadow:
        0 0 18px rgba(56,189,248,0.40),
        0 0 38px rgba(37,99,235,0.28);
}}

.p0-hero-line {{
    width: 64px;
    height: 3px;
    margin: 26px 0 24px 0;
    background: #38BDF8;
    border-radius: 999px;
    box-shadow: 0 0 18px rgba(56,189,248,0.9);
}}

.p0-hero-subtitle {{
    color: #E5E7EB;
    font-size: 1.16rem;
    line-height: 1.58;
    max-width: 610px;
}}

.p0-hero-pills {{
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    margin-top: 34px;
}}

.p0-hero-pills div {{
    border: 1px solid rgba(56,189,248,0.44);
    background: rgba(15,23,42,0.64);
    color: #E0F2FE;
    border-radius: 999px;
    padding: 13px 22px;
    font-weight: 800;
    font-size: 1.04rem;
    box-shadow: 0 0 18px rgba(56,189,248,0.10);
}}

.p0-hero-legend {{
    position: absolute;
    right: 42px;
    top: 62px;
    width: 350px;
    z-index: 3;
    background: rgba(15,23,42,0.80);
    border: 1px solid rgba(148,163,184,0.30);
    border-radius: 24px;
    padding: 24px;
    backdrop-filter: blur(12px);
}}

.p0-legend-title {{
    color: #F8FAFC;
    font-weight: 850;
    font-size: 1.12rem;
    margin-bottom: 18px;
}}

.p0-family-row {{
    display: flex;
    gap: 12px;
    align-items: flex-start;
    color: #CBD5E1;
    font-size: 0.88rem;
    line-height: 1.38;
    margin-bottom: 15px;
}}

.p0-family-row b {{
    color: #F8FAFC;
    font-weight: 850;
}}

.dot {{
    width: 12px;
    height: 12px;
    border-radius: 999px;
    margin-top: 4px;
    flex: 0 0 12px;
}}

.dot.core {{ background: #38BDF8; }}
.dot.industrial {{ background: #8B5CF6; }}
.dot.adaptive {{ background: #F59E0B; }}
.dot.bridge {{ background: #22D3EE; }}
.dot.transitional {{ background: #64748B; }}

.p0-entry-row {{
    position: absolute;
    left: 42px;
    right: 42px;
    bottom: 20px;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    z-index: 4;
}}

.p0-entry-card {{
    min-height: 158px;
    border-radius: 22px;
    padding: 24px;
    display: grid;
    grid-template-columns: 54px 1fr;
    gap: 18px;
    align-items: center;
    background: rgba(15,23,42,0.83);
    border: 1px solid rgba(148,163,184,0.24);
    backdrop-filter: blur(12px);
}}

.p0-entry-card.blue {{
    box-shadow: inset 0 0 0 1px rgba(56,189,248,0.24), 0 0 24px rgba(37,99,235,0.12);
}}

.p0-entry-card.purple {{
    box-shadow: inset 0 0 0 1px rgba(139,92,246,0.28), 0 0 24px rgba(139,92,246,0.12);
}}

.p0-entry-card.cyan {{
    box-shadow: inset 0 0 0 1px rgba(34,211,238,0.26), 0 0 24px rgba(34,211,238,0.10);
}}

.p0-entry-card.amber {{
    box-shadow: inset 0 0 0 1px rgba(245,158,11,0.26), 0 0 24px rgba(245,158,11,0.10);
}}

.p0-entry-icon {{
    width: 52px;
    height: 52px;
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,0.45);
    background: rgba(56,189,248,0.10);
    color: #38BDF8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.85rem;
}}

.p0-entry-title {{
    color: #F8FAFC;
    font-weight: 850;
    font-size: 1.22rem;
    line-height: 1.2;
    margin-bottom: 10px;
}}

.p0-entry-text {{
    color: #CBD5E1;
    font-size: 1.02rem;
    line-height: 1.46;
}}

@media (max-width: 950px) {{
    .p0-entry-row {{
        grid-template-columns: 1fr 1fr;
    }}

    .p0-hero-title {{
        font-size: 3.1rem;
    }}

    .p0-hero-legend {{
        display: none;
    }}
}}
</style>
"""

components.html(hero_html, height=780, scrolling=False)


# =============================================================================
# P0 LOWER PAGE — SAFE STREAMLIT SECTIONS
# =============================================================================

st.markdown(
    """
<style>
.p0-card-title {
    color: #F8FAFC;
    font-size: 1.12rem;
    font-weight: 900;
    line-height: 1.25;
    margin-bottom: 8px;
}

.p0-card-body {
    color: #CBD5E1;
    font-size: 0.96rem;
    line-height: 1.45;
}

.p0-mission-card,
.p0-loop-text-card,
.p0-loop-image-shell,
.p0-assumption-card,
.p0-ai-card,
.p0-cta-box {
    border-radius: 22px;
    background: linear-gradient(145deg, rgba(15,23,42,0.94), rgba(15,23,42,0.74));
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 42px rgba(0,0,0,0.22);
}

.p0-mission-card {
    padding: 28px 32px;
    border-left: 5px solid #38BDF8;
    background:
        radial-gradient(circle at left top, rgba(56,189,248,0.16), transparent 36%),
        linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.76));
}

.p0-mission-title {
    color: #F8FAFC;
    font-size: 1.48rem;
    font-weight: 950;
    line-height: 1.22;
    margin-bottom: 10px;
}

.p0-mission-body {
    color: #CBD5E1;
    font-size: 1.06rem;
    line-height: 1.55;
    max-width: 1080px;
}

.p0-loop-layout {
    display: grid;
    grid-template-columns: 0.82fr 1.18fr;
    gap: 28px;
    align-items: stretch;
    margin-top: 8px;
}

.p0-loop-text-card {
    padding: 30px 32px;
    border-left: 5px solid #38BDF8;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 500px;
}

.p0-loop-eyebrow {
    color: #38BDF8;
    font-size: 0.76rem;
    font-weight: 950;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.p0-loop-text-title {
    color: #F8FAFC;
    font-size: 1.72rem;
    font-weight: 950;
    line-height: 1.18;
    margin-bottom: 18px;
}

.p0-loop-text-body {
    color: #CBD5E1;
    font-size: 1.06rem;
    line-height: 1.58;
    margin-bottom: 22px;
}

.p0-loop-mini-steps {
    display: grid;
    gap: 10px;
}

.p0-loop-mini-step {
    display: grid;
    grid-template-columns: 38px 1fr;
    gap: 12px;
    align-items: start;
    padding: 12px 14px;
    border-radius: 16px;
    background: rgba(2,6,23,0.36);
    border: 1px solid rgba(148,163,184,0.16);
}

.p0-loop-mini-num {
    width: 30px;
    height: 30px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38BDF8;
    background: rgba(56,189,248,0.11);
    border: 1px solid rgba(56,189,248,0.34);
    font-weight: 950;
    font-size: 0.82rem;
}

.p0-loop-mini-title {
    color: #F8FAFC;
    font-size: 1.0rem;
    font-weight: 900;
    line-height: 1.25;
}

.p0-loop-mini-body {
    color: #CBD5E1;
    font-size: 0.92rem;
    line-height: 1.38;
    margin-top: 2px;
}

.p0-loop-image-shell {
    min-height: 500px;
    padding: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle at center, rgba(56,189,248,0.14), transparent 45%),
        linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.76));
    border: 1px solid rgba(56,189,248,0.28);
    overflow: hidden;
}

.p0-loop-image {
    width: min(560px, 100%);
    height: auto;
    display: block;
    filter: drop-shadow(0 0 28px rgba(56,189,248,0.22));
}

.p0-loop-bottom {
    margin-top: 20px;
    padding: 22px 26px;
    border-radius: 20px;
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.22);
}

.p0-loop-bottom-title {
    color: #F8FAFC;
    font-size: 1.16rem;
    font-weight: 950;
    line-height: 1.3;
    margin-bottom: 8px;
}

.p0-loop-bottom-text {
    color: #CBD5E1;
    font-size: 1.0rem;
    line-height: 1.5;
}

.p0-assumption-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 14px;
}

.p0-assumption-card {
    min-height: 164px;
    padding: 20px 18px;
    border-top: 4px solid var(--accent);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

.p0-assumption-card.evidence { --accent: #38BDF8; }
.p0-assumption-card.purpose { --accent: #8B5CF6; }
.p0-assumption-card.boundary { --accent: #EF4444; }
.p0-assumption-card.lens { --accent: #22C55E; }
.p0-assumption-card.uncertainty { --accent: #F59E0B; }

.p0-tag {
    color: var(--accent);
    font-size: 0.68rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 12px;
    white-space: nowrap;
}

.p0-ai-card {
    padding: 30px;
    border: 1px solid rgba(139,92,246,0.34);
    background:
        radial-gradient(circle at top left, rgba(139,92,246,0.18), transparent 34%),
        linear-gradient(145deg, rgba(15,23,42,0.94), rgba(15,23,42,0.74));
}

.p0-ai-kicker {
    color: #A78BFA;
    font-size: 0.76rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 12px;
}

.p0-ai-title {
    color: #F8FAFC;
    font-size: 1.55rem;
    font-weight: 950;
    margin-bottom: 10px;
    line-height: 1.25;
}

.p0-ai-body {
    color: #CBD5E1;
    font-size: 1.04rem;
    line-height: 1.55;
}

.p0-cta-box {
    padding: 40px;
    text-align: center;
    background:
        radial-gradient(circle at center top, rgba(56,189,248,0.20), transparent 38%),
        linear-gradient(135deg, rgba(37,99,235,0.34), rgba(15,23,42,0.90));
    border: 1px solid rgba(56,189,248,0.34);
    box-shadow: 0 28px 70px rgba(37,99,235,0.18);
}

.p0-cta-title {
    color: #F8FAFC;
    font-size: 2.05rem;
    font-weight: 950;
    margin-bottom: 12px;
}

.p0-cta-text {
    color: #CBD5E1;
    font-size: 1.08rem;
    line-height: 1.55;
    max-width: 760px;
    margin: 0 auto;
}

div[data-testid="stPageLink"] a,
.stButton > button {
    width: 100% !important;
    min-height: 46px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(56,189,248,0.55) !important;
    background: linear-gradient(90deg, #38BDF8 0%, #2563EB 100%) !important;
    color: #F8FAFC !important;
    font-weight: 900 !important;
    box-shadow: 0 0 24px rgba(56,189,248,0.30) !important;
    text-align: center !important;
    justify-content: center !important;
}

@media (max-width: 1100px) {
    .p0-loop-layout {
        grid-template-columns: 1fr;
    }

    .p0-loop-text-card,
    .p0-loop-image-shell {
        min-height: auto;
    }

    .p0-assumption-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 700px) {
    .p0-assumption-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# SECTION 02 — MISSION BRIEFING
# =============================================================================

render_section_title(
    number="02",
    title="Your mission",
    subtitle="Use the Atlas to build understanding, not to search for a single best answer.",
)

st.html(
    """
<div class="p0-mission-card">
    <div class="p0-mission-title">Choose a country. Observe its profile. Investigate the tradeoffs.</div>
    <div class="p0-mission-body">
        Then choose strategic priorities, challenge them under disruption, and reflect on what you learned.
        The goal is to understand structural pathways across Europe — not to rank countries or prescribe policy.
    </div>
</div>
"""
)


# =============================================================================
# SECTION 03 — ATLAS LEARNING LOOP
# =============================================================================

render_section_title(
    number="03",
    title="How does the Atlas work?",
    subtitle="One learning loop connects the app steps: observe, investigate, choose, challenge, and reflect.",
)

loop_img_path = (
    Path(__file__).parent.parent
    / "assets"
    / "p0_learning_loop_circle.png"
)

# Fallback only helps when reviewing the generated file outside the Streamlit repo.
if not loop_img_path.exists():
    loop_img_path = Path("/mnt/data/p0_learning_loop_circle.png")

loop_img = image_to_base64(loop_img_path)

st.html(
    f"""
<div class="p0-loop-layout">
    <div class="p0-loop-text-card">
        <div class="p0-loop-eyebrow">Learning loop</div>
        <div class="p0-loop-text-title">The Atlas is not a straight path.</div>
        <div class="p0-loop-text-body">
            Each page builds one part of the learning journey. You first observe a country,
            then investigate tradeoffs, choose a strategic direction, challenge it under disruption,
            and reflect on what changed.
        </div>
        <div class="p0-loop-mini-steps">
            <div class="p0-loop-mini-step">
                <div class="p0-loop-mini-num">01</div>
                <div><div class="p0-loop-mini-title">Observe</div><div class="p0-loop-mini-body">Start with one country and understand its structural profile.</div></div>
            </div>
            <div class="p0-loop-mini-step">
                <div class="p0-loop-mini-num">02</div>
                <div><div class="p0-loop-mini-title">Investigate</div><div class="p0-loop-mini-body">Explore the tradeoffs and tensions behind the pattern.</div></div>
            </div>
            <div class="p0-loop-mini-step">
                <div class="p0-loop-mini-num">03</div>
                <div><div class="p0-loop-mini-title">Choose</div><div class="p0-loop-mini-body">Test a strategic priority and observe what changes.</div></div>
            </div>
            <div class="p0-loop-mini-step">
                <div class="p0-loop-mini-num">04</div>
                <div><div class="p0-loop-mini-title">Challenge</div><div class="p0-loop-mini-body">Apply disruption and reveal strengths and vulnerabilities.</div></div>
            </div>
            <div class="p0-loop-mini-step">
                <div class="p0-loop-mini-num">05</div>
                <div><div class="p0-loop-mini-title">Reflect</div><div class="p0-loop-mini-body">Summarize what you learned and decide what to explore next.</div></div>
            </div>
        </div>
    </div>

    <div class="p0-loop-image-shell">
        <img
            src="data:image/png;base64,{loop_img}"
            class="p0-loop-image"
            alt="European Strategy Atlas learning loop: Observe, Investigate, Choose, Challenge, Reflect"
        />
    </div>
</div>

<div class="p0-loop-bottom">
    <div class="p0-loop-bottom-title">Each exploration creates new questions.</div>
    <div class="p0-loop-bottom-text">
        There is no single optimal pathway. Different countries navigate innovation, sustainability,
        social cohesion, security, and fiscal flexibility in different ways.
    </div>
</div>
"""
)


# =============================================================================
# SECTION 04 — HOW TO INTERPRET RESULTS
# =============================================================================

render_section_title(
    number="04",
    title="How to interpret results",
    subtitle="Use the Atlas as an educational exploration tool, not as a forecast, ranking, or policy recommendation system.",
)

st.html(
    """
<div class="p0-assumption-grid">
    <div class="p0-assumption-card evidence">
        <div class="p0-tag">Evidence</div>
        <div class="p0-card-title">Public data</div>
        <div class="p0-card-body">Built from Eurostat and European public data sources.</div>
    </div>
    <div class="p0-assumption-card purpose">
        <div class="p0-tag">Purpose</div>
        <div class="p0-card-title">Educational</div>
        <div class="p0-card-body">Designed for exploration, learning, and reflection.</div>
    </div>
    <div class="p0-assumption-card boundary">
        <div class="p0-tag">Boundary</div>
        <div class="p0-card-title">Not predictive</div>
        <div class="p0-card-body">No forecasts, causal claims, or policy prescriptions.</div>
    </div>
    <div class="p0-assumption-card lens">
        <div class="p0-tag">Lens</div>
        <div class="p0-card-title">Structural</div>
        <div class="p0-card-body">Focus on long-term patterns, systems, and tradeoffs.</div>
    </div>
    <div class="p0-assumption-card uncertainty">
        <div class="p0-tag">Uncertainty</div>
        <div class="p0-card-title">Context matters</div>
        <div class="p0-card-body">Different countries may follow different valid pathways.</div>
    </div>
</div>
"""
)


# =============================================================================
# SECTION 05 — FUTURE ATLAS GUIDE
# =============================================================================

render_section_title(
    number="05",
    title="Future Atlas Guide",
    subtitle="Future AI support may guide learning, but it will not recommend policy or optimize decisions.",
)

st.html(
    """
<div class="p0-ai-card">
    <div class="p0-ai-kicker">Future V2 feature</div>
    <div class="p0-ai-title">A guide that explains, compares, and asks better questions.</div>
    <div class="p0-ai-body">
        The future Strategy Guide may help explain a country profile, compare two pathways,
        clarify a tradeoff, or suggest what to explore next. It will not forecast outcomes,
        optimize policy, rank countries, or tell users what Europe should do.
    </div>
</div>
"""
)


# =============================================================================
# SECTION 06 — READY TO BEGIN
# =============================================================================

render_section_title(
    number="06",
    title="Ready to begin?",
    subtitle="Start by choosing a country and observing its structural profile.",
)

st.html(
    """
<div class="p0-cta-box">
    <div class="p0-cta-title">Begin the exploration journey</div>
    <div class="p0-cta-text">
        Start with a country. Investigate tradeoffs, build a strategy,
        challenge it under disruption, and reflect on what you learned.
    </div>
</div>
"""
)

p1_page_path = Path(__file__).parent / "p1_country_explorer.py"

if p1_page_path.exists():
    st.page_link(
        "pages/p1_country_explorer.py",
        label="Enter Atlas →",
        use_container_width=True,
    )
else:
    st.button(
        "Enter Atlas →",
        disabled=False,
        use_container_width=True,
        key="p0_enter_atlas",
    )


# =============================================================================
# FOOTER
# =============================================================================

render_footer()
