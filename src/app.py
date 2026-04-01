"""
SenseFlow Dashboard - Final Version
"""

import re
import requests
import streamlit as st

from model_utils import detect_indicators

st.set_page_config(
    page_title="SenseFlow | Phishing Detection",
    page_icon="🛡️",
    layout="wide"
)

def highlight_payload(text: str) -> str:
    """Highlight suspicious keywords for better visibility."""
    styled_text = text
    urgency_words = ["immediate action", "account suspended", "final notice", "within 24 hours", 
                     "legal action", "arrest warrant", "password expires", "act now", "click here"]
    
    for word in urgency_words:
        styled_text = re.sub(
            f"(?i)({word})", 
            r"<span style='background-color: #ffe6e6; color: #d63031; font-weight: bold; padding: 3px 7px; border-radius: 4px;'>\1</span>", 
            styled_text
        )
    return styled_text

def main():
    st.title("🛡️ SenseFlow")
    st.markdown("**Advanced Transformer-powered Phishing Detection System**")
    st.divider()

    col_input, col_result = st.columns([2, 3])

    with col_input:
        st.subheader("📬 Email Input")
        email_text = st.text_area(
            "Paste the full email content:",
            height=420,
            placeholder="Paste the suspected email here..."
        )
        analyze_button = st.button("🚀 Analyze Email", type="primary", use_container_width=True)

    with col_result:
        if analyze_button:
            if not email_text.strip():
                st.warning("Please paste an email to analyze.")
            else:
                with st.spinner("Analyzing with RoBERTa..."):
                    try:
                        resp = requests.post(
                            "http://localhost:8000/analyze", 
                            json={"text": email_text}, 
                            timeout=25
                        )
                        resp.raise_for_status()
                        result = resp.json()

                        score = result["confidence_score"]
                        flags = result.get("flags", [])
                        threat_level = result["threat_level"]
                        xai_text = result.get("xai_explanation", "Analysis completed.")

                        if threat_level == "Phishing":
                            st.error(f"🚨 HIGH RISK - PHISHING DETECTED ({score}%)")
                        else:
                            st.success(f"✅ SAFE ({score}%)")

                        st.metric("RoBERTa Confidence", f"{score}%")

                        st.subheader("🔴 Detected Indicators")
                        if flags:
                            for f in flags:
                                st.warning(f"🚩 {f}")
                        else:
                            st.success("No suspicious indicators detected.")

                        st.subheader("🧠 AI Model Explanation")
                        st.info(xai_text)

                        st.subheader("🔍 Highlighted Email")
                        highlighted = highlight_payload(email_text)
                        st.markdown(
                            f"""
                            <div style="padding: 22px; background-color: #1e1e2f; border-radius: 12px; 
                            border-left: 6px solid #512da8; line-height: 1.85; color: #ffffff;">
                                {highlighted}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not running. Please run `python src/main.py`")
                    except Exception as e:
                        st.error("Analysis failed.")
                        st.code(str(e))
        else:
            st.info("Enter an email above and click **Analyze Email** to start.")

if __name__ == "__main__":
    main()