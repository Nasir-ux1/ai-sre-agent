import streamlit as st
import sys
from ai_sre.agent import SREAgent
from ai_sre.tools import SRETools
from ai_sre.config import Config

st.set_page_config(
    page_title="AI-SRE Autonomous Troubleshooting Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Premium Stylesheet injection
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 255, 128, 0.4);
    }
    .terminal-output {
        font-family: 'Courier New', Courier, monospace;
        background-color: #0b0c10;
        color: #66ff66;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00ff80;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI-SRE: Autonomous Linux Troubleshooting Agent")
st.markdown("---")