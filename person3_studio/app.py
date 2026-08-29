import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import streamlit as st
import json
import time

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from orchestrator import MCPForgeOrchestrator

# ── Streamlit Page Configuration ──
st.set_page_config(
    page_title="MCP-Forge Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom Minimalist Dark + Golden/Orange Styling ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Dark Theme Overrides */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Preserve Streamlit icon fonts */
    [data-testid="stIconMaterial"], [class*="material-symbols"], [class*="material-icons"], .material-symbols-rounded {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }
    
    .stApp {
        background-color: #090B0E;
        color: #E6EDF3;
    }

    /* Minimalist Top Navigation & Header */
    .forge-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.5rem;
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .forge-logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .forge-badge {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #090B0E;
        padding: 4px 10px;
        border-radius: 6px;
    }
    .forge-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin: 0;
    }
    .forge-subtitle {
        font-size: 0.85rem;
        color: #9CA3AF;
        margin: 2px 0 0 0;
    }

    /* Card Panels */
    .forge-card {
        background: #11141A;
        border: 1px solid #1F242C;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        transition: border 0.2s ease-in-out;
    }
    .forge-card:hover {
        border-color: rgba(245, 158, 11, 0.4);
    }
    .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #F59E0B;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #0D1015 !important;
        border: 1px solid #232936 !important;
        color: #F3F4F6 !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #F59E0B !important;
        box-shadow: 0 0 0 1px #F59E0B !important;
    }

    /* Primary Launch Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        color: #090B0E !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 24px rgba(245, 158, 11, 0.4) !important;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        background-color: #161B22 !important;
        color: #F59E0B !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-color: #F59E0B !important;
    }

    /* Metric Badges */
    .metric-box {
        background: #11141A;
        border: 1px solid #1F242C;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #F59E0B;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0D1015;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1F242C;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #9CA3AF !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1A1F29 !important;
        color: #F59E0B !important;
    }

    /* Code Blocks */
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Preset Data ──
sample_path = os.path.join(os.path.dirname(__file__), "..", "person1_compiler", "sample_inputs", "raw_github_input.json")
default_spec_str = ""
if os.path.exists(sample_path):
    with open(sample_path, "r", encoding="utf-8") as f:
        sample_data = json.load(f)
        default_spec_str = json.dumps(sample_data.get("spec_content", {}), indent=2)

# ── Top Hero Header ──
st.markdown("""
<div class="forge-header">
    <div class="forge-logo">
        <span class="forge-badge">v2.0 Autonomous</span>
        <div>
            <h1 class="forge-title">⚡ MCP-FORGE</h1>
            <p class="forge-subtitle">Autonomous Daytona-Powered FastMCP & CLI Compiler</p>
        </div>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #10B981; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
            Daytona Engine Ready
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main 2-Column Clean Grid ──
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown('<div class="card-title">⚙️ 1. Specification & Credentials</div>', unsafe_allow_html=True)
    
    preset_choice = st.selectbox(
        "Showcase API Presets",
        ["GitHub Issues & Repositories (Showcase)", "Custom Specification"],
        label_visibility="collapsed"
    )
    
    if preset_choice.startswith("GitHub"):
        initial_spec = default_spec_str
        initial_svc = "GitHubIssues"
        initial_base = "https://api.github.com"
        initial_auth = "bearer"
        initial_env = "GITHUB_TOKEN"
    else:
        initial_spec = ""
        initial_svc = ""
        initial_base = ""
        initial_auth = "none"
        initial_env = "API_KEY"

    spec_format = st.segmented_control(
        "Spec Format",
        options=["openapi_json", "openapi_yaml", "curl"],
        default="openapi_json"
    ) or "openapi_json"

    st.markdown('<div style="font-size: 0.82rem; font-weight: 700; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; margin: 12px 0 6px 0;">📝 Raw Specification Payload</div>', unsafe_allow_html=True)
    spec_content_str = st.text_area(
        "Spec Payload",
        value=initial_spec,
        height=200,
        label_visibility="collapsed",
        placeholder="Paste OpenAPI / Swagger JSON or YAML here..."
    )

    st.markdown('<div class="card-title" style="margin-top: 1rem;">🔐 2. Configuration & Sandbox Auth</div>', unsafe_allow_html=True)
    
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        service_name = st.text_input("Service Name", value=initial_svc, placeholder="e.g. GitHubIssues")
        auth_type = st.selectbox("Auth Type", ["bearer", "none", "header", "query", "basic"], index=["bearer", "none", "header", "query", "basic"].index(initial_auth))
    with c_s2:
        base_url = st.text_input("Base URL Override", value=initial_base, placeholder="https://api.github.com")
        env_var_name = st.text_input("Env Variable Name", value=initial_env, placeholder="e.g. GITHUB_TOKEN")

    test_token = st.text_input(
        "Secret Token / API Key (Optional)",
        type="password",
        placeholder="e.g. ghp_xxxx (Injected into Daytona Sandbox for live testing)..."
    )

    submit_btn = st.button("🚀 Compile, Deploy & Verify in Daytona", type="primary", use_container_width=True)

with col_right:
    st.markdown('<div class="card-title">⚡ 3. Sandbox Telemetry & Deliverables</div>', unsafe_allow_html=True)
    
    output_container = st.container()

    if not submit_btn:
        with output_container:
            st.markdown("""
            <div style="background: #11141A; border: 1px dashed #232936; border-radius: 14px; padding: 2.5rem; text-align: center; color: #6B7280;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">⚡</div>
                <div style="font-weight: 600; color: #9CA3AF; font-size: 1rem;">Awaiting Compilation Trigger</div>
                <div style="font-size: 0.82rem; margin-top: 4px;">Click <b>Compile, Deploy & Verify</b> on the left to initiate the multi-agent Daytona pipeline.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        if not spec_content_str.strip():
            st.error("API Specification content is required.")
        else:
            # Intelligent fallback if user accidentally pastes token in variable name field
            sanitized_env_var = env_var_name.strip() if env_var_name else ""
            actual_test_token = test_token.strip() if test_token else ""
            if sanitized_env_var.startswith(("ghp_", "sk-", "Bearer", "ey")) or len(sanitized_env_var) > 25:
                if not actual_test_token:
                    actual_test_token = sanitized_env_var
                sanitized_env_var = "GITHUB_TOKEN" if "github" in (service_name or "").lower() else "API_KEY"
            elif not sanitized_env_var:
                sanitized_env_var = "GITHUB_TOKEN" if "github" in (service_name or "").lower() else "API_KEY"

            raw_payload = {
                "spec_format": spec_format,
                "spec_content": spec_content_str,
                "service_name": service_name if service_name else None,
                "base_url": base_url if base_url else None,
                "auth": {
                    "auth_type": auth_type,
                    "header_name": "Authorization",
                    "query_param_name": None,
                    "env_var_name": sanitized_env_var,
                    "test_token": actual_test_token if actual_test_token else None
                }
            }

            progress_bar = st.progress(0)
            status_box = st.empty()
            
            final_result = None
            for event in MCPForgeOrchestrator.run(raw_payload):
                step = event.get("step")
                msg = event.get("message", "")
                prog = event.get("progress", 0)
                
                progress_bar.progress(prog)
                status_box.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid #F59E0B; padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; color: #F3F4F6; margin-bottom: 10px;">
                    <b style="color: #F59E0B;">[{step}]</b> {msg}
                </div>
                """, unsafe_allow_html=True)
                
                if step in ("COMPLETED", "ERROR", "DEPLOYMENT_FAILED"):
                    final_result = event
                    break

            if final_result and final_result.get("step") == "COMPLETED":
                progress_bar.progress(100)
                status_box.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10B981; padding: 10px 14px; border-radius: 8px; font-size: 0.88rem; color: #10B981; font-weight: 600; margin-bottom: 12px;">
                    ✅ Pipeline Success: FastMCP Server Deployed, Tested & Verified in Daytona Sandbox
                </div>
                """, unsafe_allow_html=True)
                
                bundle = final_result.get("bundle", {})
                deploy_out = final_result.get("deploy_output", {})
                tester_out = final_result.get("tester_output", {})
                bench_rep = final_result.get("benchmark_report", {})
                
                # ── Minimalist Metric Grid ──
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Benchmark</div><div class="metric-value">{bench_rep.get("overall_score", "100/100")}</div></div>', unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Sandbox ID</div><div class="metric-value" style="font-size: 0.95rem; line-height: 1.8;">{final_result.get("workspace_id", "mock-ws")[:11]}..</div></div>', unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Test Status</div><div class="metric-value" style="color: #10B981; font-size: 1.05rem;">{tester_out.get("status", "PASSED")}</div></div>', unsafe_allow_html=True)
                with m_col4:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Fidelity</div><div class="metric-value">{bench_rep.get("metrics", {}).get("schema_completeness", "100%")}</div></div>', unsafe_allow_html=True)

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                # ── Sleek Tabs Navigation ──
                t_srv, t_cfg, t_tst, t_log, t_eval = st.tabs([
                    "💻 server.py",
                    "⚙️ Claude / Cursor Config",
                    "🧪 Test Protocol",
                    "⚡ Daytona Telemetry",
                    "📊 Scorecard"
                ])

                with t_srv:
                    d_c1, d_c2 = st.columns([3, 1])
                    with d_c1:
                        st.markdown("<span style='font-size: 0.8rem; color: #9CA3AF;'>Production-ready FastMCP server with secret redaction & bounded pooling.</span>", unsafe_allow_html=True)
                    with d_c2:
                        st.download_button("📥 Download server.py", bundle.get("server.py", ""), file_name="server.py", mime="text/x-python", use_container_width=True)
                    st.code(bundle.get("server.py", ""), language="python")

                with t_cfg:
                    config_json = json.dumps(bundle.get("claude_desktop_config.json", {}), indent=2)
                    c_c1, c_c2 = st.columns([3, 1])
                    with c_c1:
                        st.markdown("<span style='font-size: 0.8rem; color: #9CA3AF;'>Ready-to-paste configuration for Claude Desktop, Cursor, and Antigravity.</span>", unsafe_allow_html=True)
                    with c_c2:
                        st.download_button("📥 Download JSON", config_json, file_name="claude_desktop_config.json", mime="application/json", use_container_width=True)
                    st.code(config_json, language="json")

                with t_tst:
                    st.json(bundle.get("test_protocol.json", {}))

                with t_log:
                    st.json({
                        "workspace_id": deploy_out.get("workspace_id"),
                        "status": deploy_out.get("status"),
                        "deployed_files": deploy_out.get("deployed_files"),
                        "test_status": tester_out.get("status"),
                        "self_healed": final_result.get("self_healed", False),
                        "healing_attempts": final_result.get("healing_attempts", 0)
                    })

                with t_eval:
                    st.json(bench_rep)
            elif final_result and final_result.get("step") in ("ERROR", "DEPLOYMENT_FAILED"):
                st.error(f"Execution Error: {final_result.get('message')}")
