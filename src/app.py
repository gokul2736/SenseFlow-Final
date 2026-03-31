"""
SenseFlow - High-Tech Dashboard
Premium redesign with speedometer gauge + text highlighting
"""

import requests
import streamlit as st

# ========================= CUSTOM HIGH-TECH CSS =========================
st.set_page_config(page_title="SenseFlow | Phishing Detection", page_icon="🛡️", layout="centered")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Montserrat', sans-serif; }

body {
    background: linear-gradient(to right, #e2e2e2, #c9d6ff);
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    background-color: #fff;
    border-radius: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    width: 900px;
    max-width: 95%;
    min-height: 580px;
    padding: 40px 50px;
    position: relative;
    overflow: hidden;
}

.gauge-container {
    width: 220px;
    height: 220px;
    margin: 20px auto;
    position: relative;
}

.gauge {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: conic-gradient(#512da8 0% var(--score), #e0e0e0 var(--score) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.gauge::before {
    content: '';
    width: 160px;
    height: 160px;
    background: white;
    border-radius: 50%;
    position: absolute;
}

.score-text {
    position: absolute;
    font-size: 42px;
    font-weight: 700;
    color: #512da8;
    z-index: 2;
}

h1 { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 10px; }
.subtitle { text-align: center; color: #666; margin-bottom: 30px; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

API_URL = "http://localhost:8000/analyze"

def analyze_email(email_text: str):
    try:
        response = requests.post(API_URL, json={"text": email_text}, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception:
        st.error("❌ Backend not running. Start with: python src/main.py")
        return None

def main():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    st.markdown("<h1>🛡️ SenseFlow: Phishing Detection</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Transformer-powered Email Threat Intelligence</p>', unsafe_allow_html=True)

    email_input = st.text_area(
        "Paste the full email content here:",
        height=220,
        placeholder="Dear customer, your account has been suspended...",
    )

    if st.button("🔍 Analyze Email", type="primary", use_container_width=True):
        if not email_input.strip():
            st.warning("Please paste an email.")
            return

        with st.spinner("Running RoBERTa inference..."):
            result = analyze_email(email_input)

        if result:
            # --- Gauge + Score ---
            score = result["confidence_score"]
            st.markdown(f"""
            <div class="gauge-container">
                <div class="gauge" style="--score: {score}%;"></div>
                <div class="score-text">{score}%</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                if result["threat_level"] == "Phishing":
                    st.error("🚨 HIGH RISK - PHISHING DETECTED")
                else:
                    st.success("✅ SAFE")

            # Highlighted email text
            st.subheader("Email with Anomalous Parts Highlighted")
            highlighted_text = email_input
            for flag in result.get("flags", []):
                highlighted_text = highlighted_text.replace(flag.lower(), f'<span style="background-color:#ffeb3b;color:#000;padding:2px 6px;border-radius:4px;">{flag}</span>')
            st.markdown(highlighted_text, unsafe_allow_html=True)

            # Indicators
            if result.get("flags"):
                st.subheader("🔴 Detected Threat Indicators")
                for flag in result["flags"]:
                    st.warning(f"🚩 {flag}")

            st.success("✅ Analysis Complete!")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()