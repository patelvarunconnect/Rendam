"""Shared look and feel: page style, header banner and API key input."""
import os

import streamlit as st

CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
[data-testid="stDeployButton"] {display: none;}
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {
  padding: 1.6rem 2rem; border-radius: 16px; margin-bottom: 1.5rem; color: #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}
.hero h1 {color: #fff; font-size: 2rem; margin: 0 0 .35rem 0; padding: 0;}
.hero p {color: rgba(255, 255, 255, .9); margin: 0; font-size: 1.02rem;}
.card {
  background: #fff; border: 1px solid #E5E7EB; border-radius: 14px;
  padding: 1.1rem 1.3rem; box-shadow: 0 1px 3px rgba(0, 0, 0, .04); margin-bottom: 1rem;
}
.card h4 {margin: 0 0 .5rem 0;}
.chip {
  display: inline-block; padding: .25rem .75rem; margin: .2rem .3rem .2rem 0;
  border-radius: 999px; font-size: .85rem; font-weight: 500;
}
.chip-green {background: #DCFCE7; color: #166534;}
.chip-red {background: #FEE2E2; color: #991B1B;}
.chip-blue {background: #DBEAFE; color: #1E40AF;}
.muted {color: #6B7280; font-size: .9rem;}
.footer {text-align: center; color: #9CA3AF; font-size: .8rem; margin-top: 3rem;}
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title, subtitle, start="#2563EB", end="#7C3AED"):
    st.markdown(
        f'<div class="hero" style="background: linear-gradient(135deg, {start} 0%, {end} 100%);">'
        f"<h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def footer(text="Built by Varun Patel with Python and Streamlit"):
    st.markdown(f'<div class="footer">{text}</div>', unsafe_allow_html=True)


def groq_api_key():
    """Return the Groq API key from .env, Streamlit secrets or the sidebar input."""
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            key = ""
    if key:
        st.sidebar.success("Groq API key loaded", icon="✅")
        return key
    key = st.sidebar.text_input(
        "Groq API key",
        type="password",
        help="Get a free key at https://console.groq.com/keys",
    )
    if not key:
        st.sidebar.info("Add your free Groq API key to start.", icon="🔑")
    return key
