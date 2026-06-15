"""Shared ATLAS journey progress component for P1-P5.

Place in:
    streamlit_app/utils/journey_progress.py
"""

from __future__ import annotations

import streamlit as st

JOURNEY_STEPS = [
    (1, "Observe"),
    (2, "Investigate"),
    (3, "Invest & Strategy"),
    (4, "Challenge"),
    (5, "Reflect"),
]


def render_journey_progress(current_step: int) -> None:
    """Render compact ATLAS journey bar.

    Use only on P1-P5. Do not use on P0 landing or P6 methodology.
    """
    items = []
    for step, label in JOURNEY_STEPS:
        if step < current_step:
            state = "done"
        elif step == current_step:
            state = "active"
        else:
            state = "future"
        items.append(
            f"""
            <div class=\"atlas-journey-step {state}\">
                <div class=\"atlas-journey-num\">{step:02d}/05</div>
                <div class=\"atlas-journey-label\">{label}</div>
            </div>
            """
        )

    st.html(
        f"""
        <style>
        .atlas-journey-bar {{
            display:grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            align-items: stretch;
            margin: 10px 0 18px 0;
            max-width: 1500px;
        }}
        .atlas-journey-step {{
            border:1px solid rgba(148,163,184,0.24);
            border-radius:14px;
            background: rgba(15,23,42,0.72);
            padding: 10px 12px;
            min-height: 64px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        }}
        .atlas-journey-num {{
            font-family:'IBM Plex Mono','Roboto Mono',monospace;
            font-size:0.72rem;
            font-weight:950;
            letter-spacing:0.08em;
            margin-bottom:5px;
        }}
        .atlas-journey-label {{
            font-size:0.95rem;
            line-height:1.15;
            font-weight:900;
        }}
        .atlas-journey-step.done {{
            border-color: rgba(56,189,248,0.52);
            background: linear-gradient(135deg, rgba(14,116,144,0.46), rgba(15,23,42,0.82));
            box-shadow: inset 0 0 0 1px rgba(56,189,248,0.10);
        }}
        .atlas-journey-step.done .atlas-journey-num {{ color:#67E8F9; }}
        .atlas-journey-step.done .atlas-journey-label {{ color:#38BDF8; }}
        .atlas-journey-step.active {{
            border-color: rgba(56,189,248,0.94);
            background: linear-gradient(135deg, rgba(37,99,235,0.70), rgba(14,116,144,0.54));
            box-shadow: 0 0 26px rgba(56,189,248,0.28), inset 0 0 0 1px rgba(255,255,255,0.08);
        }}
        .atlas-journey-step.active .atlas-journey-num {{ color:#BAE6FD; }}
        .atlas-journey-step.active .atlas-journey-label {{ color:#F8FAFC; font-size:1.03rem; }}
        .atlas-journey-step.future {{ opacity:0.48; }}
        .atlas-journey-step.future .atlas-journey-num,
        .atlas-journey-step.future .atlas-journey-label {{ color:#94A3B8; }}
        @media (max-width: 950px) {{
            .atlas-journey-bar {{ grid-template-columns:1fr; }}
        }}
        </style>
        <div class=\"atlas-journey-bar\">
            {''.join(items)}
        </div>
        """
    )
