"""
p5_reflection_v05_pdf_next_mission.py

Purpose
-------
Page 5 of the EUROPEAN STRATEGY ATLAS.

This page closes the learning journey by turning the Atlas exploration into a
compact mission debrief: what was observed, what repeated, what mattered, and
what the user should explore next.
"""

from pathlib import Path

import pandas as pd
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
from utils.atlas_state import (
    init_atlas_state,
    get_journey_log_df,
)
from utils.journey_progress import render_journey_progress



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
        "█": "#",
        "░": ".",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_text(text, width=92):
    """Simple word wrap for PDF and table cells."""
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


def _read_app_csv_optional(filename: str) -> pd.DataFrame | None:
    """Read an app CSV when available; return None instead of failing."""
    candidates = [
        Path(__file__).parent.parent.parent / "data" / "app" / filename,
        Path("/mnt/data") / filename,
    ]
    for path in candidates:
        try:
            if path.exists():
                return pd.read_csv(path)
        except Exception:
            pass
    return None


def _z_to_index(value) -> int | None:
    try:
        if pd.isna(value):
            return None
        return int(round(max(0, min(100, 50 + 15 * float(value)))))
    except Exception:
        return None


def get_country_report_profile(selected_country):
    """current version report profile used by the P5 PDF export.

    Prefer real app tables, then fall back to safe known profiles.
    """
    fallback_profiles = {
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
            "family": "Innovation-Core Systems",
            "family_description": "A high-capacity transition pathway with strong sustainability and innovation signals.",
            "kpis": [],
        },
        "Romania": {
            "family": "Adaptive / Peripheral Systems",
            "family_description": "A convergence-oriented pathway where structural change and capacity-building are central.",
            "kpis": [],
        },
    }

    family = "Selected structural family"
    family_description = "Family metadata was not available in the exported app session."

    family_df = _read_app_csv_optional("structural_family_metadata.csv")
    if family_df is not None and "country_name" in family_df.columns:
        rows = family_df[family_df["country_name"] == selected_country]
        if not rows.empty:
            row = rows.iloc[0]
            family = str(row.get("structural_family", family) or family)
            subfamily = str(row.get("structural_subfamily", "") or "")
            archetype = str(row.get("family_anchor_archetype", "") or "")
            parts = []
            if subfamily and subfamily.lower() != "nan":
                parts.append(f"Subfamily: {subfamily}")
            if archetype and archetype.lower() != "nan":
                parts.append(f"Anchor/archetype: {archetype}")
            if parts:
                family_description = "; ".join(parts) + "."
            else:
                family_description = f"{selected_country} belongs to {family}."

    kpis = []
    profile_df = _read_app_csv_optional("country_dimension_profiles.csv")
    if profile_df is not None and "country_name" in profile_df.columns:
        rows = profile_df[profile_df["country_name"] == selected_country]
        if not rows.empty:
            row = rows.iloc[0]
            dimension_map = [
                ("Innovation Capacity", "dim_innovation_capacity"),
                ("Sustainability Capacity", "dim_sustainability_capacity"),
                ("Human Capital Capacity", "dim_human_capital_capacity"),
                ("Social Stability", "dim_social_stability"),
                ("Fiscal Flexibility", "dim_fiscal_flexibility"),
                ("Security Reprioritization", "dim_security_reprioritization"),
                ("Adaptive Transformation", "dim_adaptive_transformation"),
            ]
            for label, col in dimension_map:
                if col in row.index:
                    score = _z_to_index(row.get(col))
                    if score is not None:
                        kpis.append((label, score))

    if family == "Selected structural family" and selected_country in fallback_profiles:
        family = fallback_profiles[selected_country]["family"]
        family_description = fallback_profiles[selected_country]["family_description"]
    if not kpis and selected_country in fallback_profiles:
        kpis = fallback_profiles[selected_country].get("kpis", [])

    return {"family": family, "family_description": family_description, "kpis": kpis}


def _ascii_bar(value, width=20):
    """Return a simple fixed-width bar for PDF text output."""
    value = max(0, min(100, int(round(value))))
    filled = int(round(width * value / 100))
    return "█" * filled + "░" * (width - filled)


def _reference_label_for_pdf(selected_reference: str, selected_reference_country: str | None = None) -> str:
    """Return a meaningful PDF reference label."""
    if selected_reference == "Another Country":
        if selected_reference_country:
            return f"Another Country ({selected_reference_country})"
        return "Another Country"
    return selected_reference


def _journey_log_rows_for_pdf(max_observation_chars: int = 150) -> list[dict[str, str]]:
    """Return the real shared Atlas journey log as table rows."""
    log = st.session_state.get("atlas_journey_log", [])
    if not log:
        return []

    log_df = pd.DataFrame(log)
    if "step" in log_df.columns:
        log_df = log_df.sort_values("step", ascending=True)

    rows = []
    for _, row in log_df.iterrows():
        observation = str(row.get("observation", "")).replace("\n", " ").strip()
        if len(observation) > max_observation_chars:
            observation = observation[: max_observation_chars - 3].rstrip() + "..."
        rows.append(
            {
                "Step": str(row.get("step", "")),
                "Page": str(row.get("page", "")),
                "Topic": str(row.get("topic", "")) or str(row.get("action_type", "")),
                "Observation": observation,
            }
        )
    return rows


class _SimplePDF:
    """Small dependency-free PDF writer with text and a real table."""

    def __init__(self):
        self.page_width = 595
        self.page_height = 842
        self.margin_x = 42
        self.y = 800
        self.pages: list[list[str]] = []
        self.current: list[str] = []

    def _new_page(self):
        if self.current:
            self.pages.append(self.current)
        self.current = []
        self.y = 800

    def _ensure_space(self, height):
        if self.y - height < 46:
            self._new_page()

    def text(self, line="", size=10, bold=False, gap=14):
        self._ensure_space(gap)
        safe = _pdf_escape(line)
        font = "/F1" if not bold else "/F2"
        self.current.append(f"BT {font} {size} Tf {self.margin_x} {self.y} Td ({safe}) Tj ET")
        self.y -= gap

    def wrapped_text(self, text, width=92, size=10, bold=False, gap=13):
        for line in _wrap_text(text, width):
            self.text(line, size=size, bold=bold, gap=gap)

    def section(self, title):
        self.y -= 4
        self.text(title, size=12, bold=True, gap=17)

    def table(self, rows: list[dict[str, str]]):
        self.section("Journey Log Table")
        if not rows:
            self.text("No journey log entries recorded.")
            return

        x = self.margin_x
        col_widths = [34, 112, 122, 245]
        headers = ["Step", "Page", "Topic", "Observation"]
        line_h = 10
        pad = 5
        header_h = 20

        def draw_cell_text(text, cx, cy, width, size=8, bold=False, max_chars=28):
            font = "/F1" if not bold else "/F2"
            lines = _wrap_text(text, max_chars)
            yy = cy
            for cell_line in lines:
                safe = _pdf_escape(cell_line)
                self.current.append(f"BT {font} {size} Tf {cx} {yy} Td ({safe}) Tj ET")
                yy -= line_h
            return len(lines)

        # Header per page before first row or after page break.
        def draw_header():
            nonlocal x
            self._ensure_space(header_h + 18)
            self.current.append("0.07 0.22 0.32 rg")
            self.current.append(f"{x} {self.y - header_h + 4} {sum(col_widths)} {header_h} re f")
            self.current.append("0.22 0.74 0.97 RG")
            self.current.append(f"{x} {self.y - header_h + 4} {sum(col_widths)} {header_h} re S")
            cx = x
            for header, w in zip(headers, col_widths):
                draw_cell_text(header, cx + pad, self.y - 9, w - 2 * pad, size=8, bold=True, max_chars=max(6, int(w / 5)))
                cx += w
            self.y -= header_h

        draw_header()

        for row in rows:
            cell_lines = []
            for header, w in zip(headers, col_widths):
                max_chars = max(8, int(w / 5.2))
                cell_lines.append(len(_wrap_text(row.get(header, ""), max_chars)))
            row_h = max(24, max(cell_lines) * line_h + 2 * pad)

            if self.y - row_h < 46:
                draw_header()

            self.current.append("0.20 0.27 0.36 rg")
            self.current.append(f"{x} {self.y - row_h + 4} {sum(col_widths)} {row_h} re f")
            self.current.append("0.46 0.56 0.68 RG")
            self.current.append(f"{x} {self.y - row_h + 4} {sum(col_widths)} {row_h} re S")
            cx = x
            for header, w in zip(headers, col_widths):
                self.current.append(f"{cx} {self.y - row_h + 4} {w} {row_h} re S")
                max_chars = max(8, int(w / 5.2))
                draw_cell_text(row.get(header, ""), cx + pad, self.y - 8, w - 2 * pad, size=8, bold=False, max_chars=max_chars)
                cx += w
            self.y -= row_h

    def build(self) -> bytes:
        if self.current:
            self.pages.append(self.current)
        if not self.pages:
            self.pages = [[]]

        objects = []
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objects.append(b"")  # pages placeholder
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

        first_page_obj_id = 5
        page_ids = []
        for i, commands in enumerate(self.pages):
            page_obj_id = first_page_obj_id + i * 2
            content_obj_id = page_obj_id + 1
            page_ids.append(page_obj_id)
            stream = "\n".join(commands).encode("latin-1", "replace")
            objects.append(
                f"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /MediaBox [0 0 {self.page_width} {self.page_height}] /Contents {content_obj_id} 0 R >>".encode()
            )
            objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")

        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()

        pdf = bytearray(b"%PDF-1.4\n")
        offsets = []
        for idx, obj in enumerate(objects, start=1):
            offsets.append(len(pdf))
            pdf.extend(f"{idx} 0 obj\n".encode())
            pdf.extend(obj)
            pdf.extend(b"\nendobj\n")
        xref_start = len(pdf)
        pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
        pdf.extend(b"0000000000 65535 f \n")
        for offset in offsets:
            pdf.extend(f"{offset:010d} 00000 n \n".encode())
        pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode())
        return bytes(pdf)




# =============================================================================
# SHARED JOURNEY LOG HELPERS
# =============================================================================

def get_journey_counts(log_df: pd.DataFrame) -> tuple[int, int, int]:
    """Return current version counts for the P5 ribbon from the shared journey log."""
    if log_df is None or log_df.empty:
        return 0, 0, 0

    df = log_df.copy()
    page_series = df.get("page", pd.Series(dtype=str)).astype(str)

    journey_actions_count = len(df)
    strategy_count = int(page_series.str.contains("P3", case=False, na=False).sum())
    challenge_count = int(page_series.str.contains("P4", case=False, na=False).sum())

    return journey_actions_count, strategy_count, challenge_count


def _html_escape(value) -> str:
    """Minimal HTML escape for generated table text."""
    text = str(value if value is not None else "")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _stage_from_page(page: str) -> str:
    page = str(page)
    if "P1" in page:
        return "Observe"
    if "P2" in page:
        return "Investigate"
    if "P3" in page:
        return "Invest & Strategy"
    if "P4" in page:
        return "Challenge"
    if "P5" in page:
        return "Reflect"
    return "Journey"


def build_mission_track_table_rows(log_df: pd.DataFrame, selected_country: str) -> str:
    """Build the P5 Mission Log table rows from the real shared Atlas journey log."""
    if log_df is None or log_df.empty:
        return (
            "<tr>"
            "<td>Observe</td>"
            "<td>Start mission</td>"
            f"<td>No shared journey events are recorded yet for {_html_escape(selected_country)}.</td>"
            "<td>Continue exploration</td>"
            "</tr>"
        )

    df = log_df.copy()
    if "step" in df.columns:
        df = df.sort_values("step", ascending=True)

    rows_html = []
    for _, row in df.iterrows():
        page = str(row.get("page", ""))
        stage = _stage_from_page(page)
        topic = str(row.get("topic", "") or row.get("action_type", "") or "Journey action")
        observation = str(row.get("observation", "") or "Recorded journey event.").replace("\n", " ").strip()
        next_step = str(row.get("next_step", "") or "Continue journey")

        if len(observation) > 220:
            observation = observation[:217].rstrip() + "..."

        rows_html.append(
            "<tr>"
            f"<td>{_html_escape(stage)}</td>"
            f"<td>{_html_escape(topic)}</td>"
            f"<td>{_html_escape(observation)}</td>"
            f"<td>{_html_escape(next_step)}</td>"
            "</tr>"
        )

    return "".join(rows_html)

def build_reflection_pdf_bytes(
    selected_country,
    selected_reference,
    selected_reference_country=None,
):
    """Create a simple, truthful current version Mission Summary PDF.

    No generated conclusions. No visual table. Only factual journey record.
    """

    profile = get_country_report_profile(selected_country)
    reference_label = _reference_label_for_pdf(
        selected_reference,
        selected_reference_country,
    )

    log_df = pd.DataFrame(st.session_state.get("atlas_journey_log", []))

    if not log_df.empty and "step" in log_df.columns:
        log_df = log_df.sort_values("step", ascending=True)

    tradeoffs = []
    strategies = []
    challenges = []
    journey_rows = []

    if not log_df.empty:
        for _, row in log_df.iterrows():
            page = str(row.get("page", "")).strip()
            topic = str(row.get("topic", "")).strip()
            action_type = str(row.get("action_type", "")).strip()
            observation = str(row.get("observation", "")).replace("\n", " ").strip()

            if not topic:
                topic = action_type or "Journey action"

            # Skip low-value context rows in the summary lists, but keep them in the log.
            is_context_row = topic == "Country / reference selection"

            if "P2" in page and not is_context_row and topic not in tradeoffs:
                tradeoffs.append(topic)
            elif "P3" in page and not is_context_row and topic not in strategies:
                strategies.append(topic)
            elif "P4" in page and not is_context_row and topic not in challenges:
                challenges.append(topic)

            short_page = page
            if "P1" in page:
                short_page = "P1 Country Explorer"
            elif "P2" in page:
                short_page = "P2 Tradeoff Explorer"
            elif "P3" in page:
                short_page = "P3 Strategic Choices"
            elif "P4" in page:
                short_page = "P4 Challenge Mode"

            if observation:
                log_text = f"{short_page} | {topic} | {observation}"
            else:
                log_text = f"{short_page} | {topic}"

            journey_rows.append(log_text)

    pdf = _SimplePDF()

    pdf.text("EUROPEAN STRATEGY ATLAS", size=14, bold=True, gap=20)
    pdf.text("Mission Summary", size=12, bold=True, gap=18)
    pdf.text(f"Country: {selected_country}")
    pdf.text(f"Reference: {reference_label}")
    pdf.text(f"Family: {profile['family']}")
    pdf.text("")

    pdf.section("Journey")
    pdf.text("Observe -> Investigate -> Invest & Strategy -> Challenge -> Reflect")
    pdf.text("")

    pdf.section("Tradeoffs Explored")
    if tradeoffs:
        for item in tradeoffs:
            pdf.wrapped_text(f"- {item}", width=86, gap=12)
    else:
        pdf.text("No tradeoffs recorded in this session.")
    pdf.text("")

    pdf.section("Strategies Tested")
    if strategies:
        for item in strategies:
            pdf.wrapped_text(f"- {item}", width=86, gap=12)
    else:
        pdf.text("No strategies recorded in this session.")
    pdf.text("")

    pdf.section("Challenges Tested")
    if challenges:
        for item in challenges:
            pdf.wrapped_text(f"- {item}", width=86, gap=12)
    else:
        pdf.text("No challenges recorded in this session.")
    pdf.text("")

    pdf.section("Journey Log")
    if journey_rows:
        for idx, item in enumerate(journey_rows, start=1):
            pdf.wrapped_text(f"{idx}. {item}", width=88, gap=12)
    else:
        pdf.text("No journey log entries recorded.")
    pdf.text("")

    pdf.section("Assumptions & Limitations")
    assumptions = [
        "Educational exploration only.",
        "Not a forecast.",
        "Not a policy recommendation.",
        "Not causal inference.",
        "Composite indicators simplify complex systems.",
    ]
    for item in assumptions:
        pdf.wrapped_text(f"- {item}", width=86, gap=12)

    pdf.text("")
    pdf.section("Future Improvements")
    future_items = [
        "Richer country and family profiles",
        "Enhanced strategy and resilience analysis",
        "Visual journey reports",
        "Additional challenge scenarios",
        "AI-assisted learning summaries",
    ]
    for item in future_items:
        pdf.wrapped_text(f"- {item}", width=86, gap=12)

    pdf.text("")
    pdf.text("Improved version coming soon.", bold=True)
    pdf.text("")
    pdf.text("Created with EUROPEAN STRATEGY ATLAS current version")
    pdf.text("Gilad Gotesman")
    pdf.text("SPICED Academy Capstone Project")

    return pdf.build()



# =============================================================================
# PAGE CONFIG
# =============================================================================

st.markdown("## P5 — Reflect")

init_atlas_state()
mission_log_df = get_journey_log_df()
journey_actions_count, strategy_count, challenge_count = get_journey_counts(mission_log_df)

st.html(
    """
    <div class="p5-green-panel">
        <div style="color:#86EFAC; font-size:0.78rem; font-weight:950; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:8px;">What this page does</div>
        <div style="color:#E2E8F0; font-size:1.10rem; line-height:1.50; font-weight:760;">
            We reached the end of this exploration mission. This page collects the learning trail from <b>Observe → Investigate → Invest & Strategy → Challenge</b> and turns it into a short debrief: what repeated, what mattered, what remained uncertain, and where to continue.
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
    country_options = ["Germany", "Sweden", "Romania", "Italy", "Poland", "Netherlands", "Spain", "Estonia", "Greece"]
    atlas_country = st.session_state.get("atlas_country", "Germany")
    selected_country = st.selectbox(
        "Country",
        options=country_options,
        index=country_options.index(atlas_country) if atlas_country in country_options else 0,
        key="p5_selected_country_v06",
    )

with top_col3:
    reference_options = ["EU Average", "Family Average", "Another Country"]
    atlas_reference = st.session_state.get("atlas_reference_type", "Family Average")
    selected_reference = st.selectbox(
        "Reference",
        options=reference_options,
        index=reference_options.index(atlas_reference) if atlas_reference in reference_options else 1,
        key="p5_selected_reference_v06",
    )

with top_col_ref_country:
    if selected_reference == "Another Country":
        reference_country = st.selectbox(
            "Reference Country",
            options=country_options,
            index=country_options.index(st.session_state.get("atlas_reference_country", "Sweden")) if st.session_state.get("atlas_reference_country", "Sweden") in country_options else 0,
            key="p5_reference_country_v06",
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
        key="p5_view_mode_v06",
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
            <div class="p1-kpi-label" style="color:#4ADE80;">LOG ACTIONS</div>
            <div class="p1-kpi-number" style="color:#4ADE80;">{journey_actions_count}</div>
            <div class="p1-kpi-sub">Shared journey events</div>
        </div>

        <div class="p1-kpi-card">
            <div class="p1-kpi-label" style="color:#F59E0B;">CHALLENGES</div>
            <div class="p1-kpi-number" style="color:#F59E0B;">{challenge_count}</div>
            <div class="p1-kpi-sub">P4 log events</div>
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


render_journey_progress(5)

st.html(
    """
    <div style="color:#38BDF8; font-size:0.96rem; font-weight:850; line-height:1.45; margin:6px 0 14px 0;">
        Review the journey log → summarize what changed → export the learning record if needed.
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
                    <div class="p5-step-title">Invest & Strategy</div>
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
        subtitle="This current version table is built from the shared journey log, so the reflection follows what actually happened in P1–P4.",
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
                        {build_mission_track_table_rows(mission_log_df, selected_country)}
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
        subtitle="AI-supported reflection will be generated from the Mission Log in a later version. For now, this is the current version debrief summary.",
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
        selected_reference_country=reference_country,
    )

    st.html(
        f"""
        <div class="p5-green-panel">
            <div style="color:#86EFAC; font-size:0.78rem; font-weight:950; letter-spacing:0.10em; text-transform:uppercase; margin-bottom:8px;">Mission Complete</div>
            <div style="color:#E2E8F0; font-size:1.08rem; line-height:1.50; font-weight:760;">
                Thank you for exploring <b>{selected_country}</b>. You can save a compact current version PDF with the factual mission record, journey log, assumptions, and future improvements, continue exploring, or start the next mission.
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