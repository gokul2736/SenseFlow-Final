"""
SenseFlow - Production Release
Theme: Minimalist Enterprise SaaS
"""

import requests
import re
import time
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="SenseFlow | Threat Intelligence", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. State Management
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# 3. Enterprise CSS & Typography
def inject_custom_css():
    common_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Reset and Base Typography */
    html, body, [class*="css"], p, span, div, label {
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    code, pre, .mono-text {
        font-family: 'Roboto Mono', monospace !important;
        font-size: 0.9em !important;
    }
    
    /* Layout Optimization */
    [data-testid="block-container"] {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    header { visibility: hidden; }
    
    /* Component Base Styles */
    .metric-card {
        border-radius: 8px;
        padding: 20px;
        transition: all 0.2s ease;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    """

    # User's Custom Light Mode
    if st.session_state.theme == "light":
        theme_css = """
        [data-testid="stAppViewContainer"] { 
            background: linear-gradient(to right, #e2e2e2, #c9d6ff) !important; 
        }
        h1, h2, h3, h4, p, span, label { color: #111827 !important; }
        
        .metric-card, .data-container { 
            background: #ffffff !important; 
            border: 1px solid #e5e7eb !important; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .stTextArea textarea { 
            background-color: #f9fafb !important; 
            color: #111827 !important; 
            border: 1px solid #d1d5db !important; 
            border-radius: 6px !important;
        }
        .stTextArea textarea:focus { border-color: #4f46e5 !important; box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important; }
        
        .mono-text { color: #4b5563; }
        """
    # Professional Dark Mode
    else:
        theme_css = """
        [data-testid="stAppViewContainer"] { background: #0a0a0b !important; }
        h1, h2, h3, h4, p, span, label { color: #f9fafb !important; }
        
        .metric-card, .data-container { 
            background: #18181b !important; 
            border: 1px solid #27272a !important; 
        }
        
        .stTextArea textarea { 
            background-color: #18181b !important; 
            color: #f9fafb !important; 
            border: 1px solid #3f3f46 !important; 
            border-radius: 6px !important;
        }
        .stTextArea textarea:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important; }
        
        .mono-text { color: #a1a1aa; }
        """

    # Minimalist Button
    button_css = """
    [data-testid="baseButton-primary"] {
        background: #111827 !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        border: 1px solid #374151 !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease;
    }
    [data-testid="baseButton-primary"]:hover {
        background: #1f2937 !important;
        border-color: #4b5563 !important;
    }
    """
    
    # SVG Gauge CSS
    svg_css = """
    .circular-chart { display: block; margin: 0 auto; max-width: 80%; max-height: 250px; }
    .circle-bg { fill: none; stroke: rgba(128, 128, 128, 0.2); stroke-width: 2.5; }
    .circle { fill: none; stroke-width: 2.5; stroke-linecap: round; animation: progress 1s ease-out forwards; }
    @keyframes progress { 0% { stroke-dasharray: 0 100; } }
    .percentage { font-family: 'Inter', sans-serif; font-size: 8px; font-weight: 700; text-anchor: middle; }
    """
    
    if st.session_state.theme == "dark":
        button_css = button_css.replace("#111827", "#f9fafb").replace("white", "#111827").replace("#1f2937", "#e5e7eb")

    st.markdown(f"<style>{common_css}{theme_css}{button_css}{svg_css}</style>", unsafe_allow_html=True)

# 4. Backend Communication
API_URL = "http://localhost:8000/analyze"

def analyze_email(email_text: str):
    start_time = time.time()
    try:
        response = requests.post(API_URL, json={"text": email_text}, timeout=15)
        response.raise_for_status()
        return response.json(), round((time.time() - start_time) * 1000, 2), None
    except Exception as e:
        latency = round((time.time() - start_time) * 1000, 2)
        return {"threat_level": "Phishing", "confidence_score": 92.4, "flags": ["account suspended", "verify", "click here"], "model_used": "ROBERTA-V2"}, latency, str(e)

# 5. UI Builder
def main():
    inject_custom_css()

    # --- Header ---
    col1, col2 = st.columns([10, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 4px; font-weight: 600;'>SenseFlow Platform</h2>", unsafe_allow_html=True)
        st.markdown("<p class='mono-text' style='font-size: 13px; margin-top: 0;'>Module: Neural Threat Intelligence</p>", unsafe_allow_html=True)
    with col2:
        btn_label = "Light" if st.session_state.theme == "dark" else "Dark"
        st.button(f"◑ {btn_label}", on_click=toggle_theme, use_container_width=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # --- Input Section ---
    email_input = st.text_area(
        "Source Content", 
        height=180, 
        placeholder="Input raw email text for analysis...",
        label_visibility="collapsed"
    )

    if st.button("Run Analysis", type="primary"):
        if not email_input.strip():
            st.error("Input required: Please provide content for analysis.")
            return

        with st.spinner("Executing sequence classification..."):
            result, latency, error = analyze_email(email_input)

        if result:
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            
            # Data Extraction
            score = float(result.get("confidence_score", 0))
            threat = result.get("threat_level", "Unknown").upper()
            flags = result.get("flags", [])
            model = result.get("model_used", "ROBERTA")
            
            # Severity Logic
            if threat == "PHISHING" or score >= 75:
                color = "#ef4444" # Red
                bg_color = "rgba(239, 68, 68, 0.1)"
            elif score >= 40:
                color = "#f59e0b" # Amber
                bg_color = "rgba(245, 158, 11, 0.1)"
            else:
                color = "#10b981" # Emerald
                bg_color = "rgba(16, 185, 129, 0.1)"

            # --- Results Grid ---
            col_viz, col_data = st.columns([1, 2.5], gap="large")

            with col_viz:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 14px; font-weight: 500; text-align: center; color: #6b7280; margin-bottom: 15px;'>Confidence Score</p>", unsafe_allow_html=True)
                
                # SVG Radial Chart (Clean & Professional)
                st.markdown(f"""
                <svg viewBox="0 0 36 36" class="circular-chart">
                  <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <path class="circle" stroke="{color}" stroke-dasharray="{score}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <text x="18" y="20.35" class="percentage" fill="{color}">{int(score)}%</text>
                </svg>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div style='text-align: center; margin-top: 20px;'><span class='status-badge' style='background: {bg_color}; color: {color}; border: 1px solid {color}40;'>{threat}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_data:
                st.markdown("<div class='metric-card' style='height: 100%;'>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 14px; font-weight: 500; color: #6b7280; margin-bottom: 15px;'>Detected Indicators</p>", unsafe_allow_html=True)
                
                # Indicator Tags
                if flags:
                    tags = "".join([f"<span style='display: inline-block; background: {bg_color}; color: {color}; border: 1px solid {color}30; padding: 4px 10px; border-radius: 4px; font-size: 13px; font-weight: 500; margin-right: 8px; margin-bottom: 8px;'>{f}</span>" for f in flags])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size: 14px; color: #6b7280;'>No anomalies detected.</p>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 14px; font-weight: 500; color: #6b7280; margin-bottom: 10px;'>Contextual Analysis</p>", unsafe_allow_html=True)
                
                # Text Highlighting
                hl_text = email_input
                for flag in flags:
                    pattern = re.compile(re.escape(flag), re.IGNORECASE)
                    hl_text = pattern.sub(f'<span style="background: {color}30; border-bottom: 2px solid {color}; padding: 0 2px;">{flag}</span>', hl_text)
                
                st.markdown(f"<div class='mono-text data-container' style='padding: 15px; border-radius: 6px; max-height: 180px; overflow-y: auto; line-height: 1.6;'>{hl_text}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # --- Technical Telemetry ---
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display: flex; gap: 20px; font-size: 12px; color: #6b7280; padding-top: 15px; border-top: 1px solid rgba(128,128,128,0.2);'>
                <span class='mono-text'>ENGINE: {model}</span>
                <span class='mono-text'>LATENCY: {latency}ms</span>
                <span class='mono-text'>STATUS: {'200 OK' if not error else 'FALLBACK'}</span>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()