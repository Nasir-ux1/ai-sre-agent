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

# Sidebar settings panel
with st.sidebar:
    st.image("https://img.icons8.com/color/144/shield.png", width=80)
    st.header("Agent Control Center")
    api_provider, _ = Config.get_api_key()
    st.info(f"Active Provider: **{api_provider.upper()} Mode**")
    
    st.subheader("System Health Metrics")
    st.sidebar.progress(85, text="Server Uptime: 99.8%")
    st.sidebar.progress(40, text="RAM Usage: 40%")

# Layout Splitting
col_query, col_metric = st.columns([2, 1])


with col_query:
    st.subheader("🤖 SRE Incident Reporter")
    query = st.text_input("Enter your server issue, warning log, or diagnostic query:", placeholder="e.g. My database port 5432 is blocked and I have disk space failures")
    
    if st.button("Launch Autonomous SRE Audit", type="primary"):
        if not query:
            st.warning("Please describe your system issue before auditing.")
        else:
            agent = SREAgent(mode="mock")
            
            trace_placeholder = st.empty()
            trace_logs = []
            
            def render_trace(msg):
                trace_logs.append(f"[AGENT] {msg}")
                trace_placeholder.markdown(
                    f'<div class="terminal-output">{"<br>".join(trace_logs)}</div>',
                    unsafe_allow_html=True
                )
                
            res = agent.run(query, trace_callback=render_trace)
            
            st.session_state["sre_results"] = res


with col_metric:
    st.subheader("📊 System Vital Gauges")
    st.markdown(
        '''
        <div class="metric-card">
            <h4>Storage Cluster</h4>
            <h2 style="color:#ff4d4d;">94% In Use</h2>
            <p>Partition <b>/dev/sda1</b> is near capacity limits.</p>
        </div>
        <br>
        <div class="metric-card">
            <h4>Port Daemon</h4>
            <h2 style="color:#ffcc00;">Warning Binding</h2>
            <p>Port <b>5432</b> is not accepting connections.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )


if "sre_results" in st.session_state:
    res = st.session_state["sre_results"]
    st.markdown("---")
    
    col_analysis, col_code = st.columns([1, 1])
    
    with col_analysis:
        st.error("🚨 Root Cause Analysis Findings")
        st.write(res["analysis"])
        
        st.warning("🛡️ Execution Safety Assurance")
        st.write(res["explanation"])
        
    with col_code:
        st.success("🛠️ Recommended Bash Safe-Fix Script")
        st.code(res["bash_fix"], language="bash")
        st.info("💡 Copy and review the script contents before executing on production servers.")
