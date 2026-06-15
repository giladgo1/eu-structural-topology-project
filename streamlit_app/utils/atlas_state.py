"""Shared Atlas state + journey log helpers.

MVP purpose:
- One global country/reference/view context across pages.
- One shared journey log available from P1 onward.
- Log only meaningful actions, not every Streamlit rerun.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


DEFAULT_ATLAS_STATE = {
    "atlas_country": "Germany",
    "atlas_reference_type": "EU Average",
    "atlas_reference_country": "Sweden",
    "atlas_view_mode": "Relative",
}

JOURNEY_COLUMNS = [
    "step",
    "page",
    "action_type",
    "country",
    "reference",
    "topic",
    "observation",
    "evidence",
    "confidence",
    "family_context",
    "exception",
    "next_step",
]


def init_atlas_state(default_country: str = "Germany", default_reference: str = "EU Average", default_reference_country: str = "Sweden", default_view_mode: str = "Relative") -> None:
    """Initialize global Atlas state once per session."""
    defaults = {
        "atlas_country": default_country,
        "atlas_reference_type": default_reference,
        "atlas_reference_country": default_reference_country,
        "atlas_view_mode": default_view_mode,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Backward-compatible aliases used by older pages.
    st.session_state.setdefault("selected_country", st.session_state["atlas_country"])
    st.session_state.setdefault("selected_reference", st.session_state["atlas_reference_type"])
    st.session_state.setdefault("reference_country", st.session_state["atlas_reference_country"])
    st.session_state.setdefault("view_mode", st.session_state["atlas_view_mode"])

    if "atlas_journey_log" not in st.session_state:
        st.session_state["atlas_journey_log"] = []


def get_atlas_context() -> dict[str, Any]:
    """Return current global Atlas context."""
    return {
        "country": st.session_state.get("atlas_country", DEFAULT_ATLAS_STATE["atlas_country"]),
        "reference_type": st.session_state.get("atlas_reference_type", DEFAULT_ATLAS_STATE["atlas_reference_type"]),
        "reference_country": st.session_state.get("atlas_reference_country", DEFAULT_ATLAS_STATE["atlas_reference_country"]),
        "view_mode": st.session_state.get("atlas_view_mode", DEFAULT_ATLAS_STATE["atlas_view_mode"]),
    }


def _current_reference_label(reference_type: str | None = None, reference_country: str | None = None) -> str:
    ref_type = reference_type or st.session_state.get("atlas_reference_type", DEFAULT_ATLAS_STATE["atlas_reference_type"])
    ref_country = reference_country or st.session_state.get("atlas_reference_country", DEFAULT_ATLAS_STATE["atlas_reference_country"])
    if ref_type == "Another Country":
        return f"Another Country: {ref_country}"
    return ref_type


def update_atlas_context(
    *,
    country: str | None = None,
    reference_type: str | None = None,
    reference_country: str | None = None,
    view_mode: str | None = None,
    source_page: str = "Atlas",
    log_context_change: bool = False,
) -> None:
    """Update global Atlas context and optionally log meaningful changes."""
    old = get_atlas_context()

    new_country = country if country is not None else old["country"]
    new_reference_type = reference_type if reference_type is not None else old["reference_type"]
    new_reference_country = reference_country if reference_country is not None else old["reference_country"]
    new_view_mode = view_mode if view_mode is not None else old["view_mode"]

    st.session_state["atlas_country"] = new_country
    st.session_state["atlas_reference_type"] = new_reference_type
    st.session_state["atlas_reference_country"] = new_reference_country
    st.session_state["atlas_view_mode"] = new_view_mode

    # Backward-compatible aliases.
    st.session_state["selected_country"] = new_country
    st.session_state["selected_reference"] = new_reference_type
    st.session_state["reference_country"] = new_reference_country
    st.session_state["view_mode"] = new_view_mode

    changed = (
        old["country"] != new_country
        or old["reference_type"] != new_reference_type
        or old["reference_country"] != new_reference_country
        or old["view_mode"] != new_view_mode
    )

    if log_context_change and changed:
        add_journey_event(
            page=source_page,
            action_type="context change",
            country=new_country,
            reference=_current_reference_label(new_reference_type, new_reference_country),
            topic="Country / reference selection",
            observation=(
                f"Selected {new_country}; reference set to "
                f"{_current_reference_label(new_reference_type, new_reference_country)}; "
                f"view mode {new_view_mode}."
            ),
            next_step="Continue exploration",
            dedupe_key=f"context::{source_page}::{new_country}::{new_reference_type}::{new_reference_country}::{new_view_mode}",
        )


def add_journey_event(
    *,
    page: str,
    action_type: str,
    country: str | None = None,
    reference: str | None = None,
    topic: str = "",
    observation: str = "",
    evidence: str = "",
    confidence: str = "",
    family_context: str = "",
    exception: str = "",
    next_step: str = "",
    dedupe_key: str | None = None,
) -> None:
    """Append a meaningful journey event with last-event de-duplication."""
    if "atlas_journey_log" not in st.session_state:
        st.session_state["atlas_journey_log"] = []

    log = st.session_state["atlas_journey_log"]
    key = dedupe_key or f"{page}::{action_type}::{country or get_atlas_context()['country']}::{topic}::{observation}"

    if log and log[-1].get("_dedupe_key") == key:
        return

    entry = {
        "step": len(log) + 1,
        "page": page,
        "action_type": action_type,
        "country": country or get_atlas_context()["country"],
        "reference": reference or _current_reference_label(),
        "topic": topic,
        "observation": observation,
        "evidence": evidence,
        "confidence": confidence,
        "family_context": family_context,
        "exception": exception,
        "next_step": next_step,
        "_dedupe_key": key,
    }
    log.append(entry)
    st.session_state["atlas_journey_log"] = log


def get_journey_log_df() -> pd.DataFrame:
    """Return shared journey log as a display DataFrame."""
    log = st.session_state.get("atlas_journey_log", [])
    if not log:
        return pd.DataFrame(columns=JOURNEY_COLUMNS)
    df = pd.DataFrame(log)
    for col in JOURNEY_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[JOURNEY_COLUMNS]
