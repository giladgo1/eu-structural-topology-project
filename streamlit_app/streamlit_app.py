from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="European Strategy Atlas",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
css_path = APP_DIR / "styles" / "atlas_theme.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.markdown("""
<div style="min-height:72vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;">
  <div style="font-size:48px;font-weight:800;color:#F8FAFC;margin-bottom:18px;">European Strategy Atlas</div>
  <div style="font-size:21px;color:#CBD5E1;line-height:1.6;margin-bottom:34px;">
    Welcome to the European Strategy Atlas.<br>
    To start your exploration journey around Europe, please click <b>Enter Atlas</b>.
  </div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([2,1,2])
with center:
    if st.button("Enter Atlas →", use_container_width=True, type="primary"):
        st.switch_page("pages/p0_landing.py")
