# Experiment: Phishing Detection System using RoBERTa

## 1. Aim
To design and implement a machine learning-based phishing detection system (SenseFlow) utilizing a transformer-based language model (RoBERTa) to analyze email text and accurately identify potential phishing threats.

## 2. Theory
Phishing is a type of social engineering attack where malicious actors deceive users into revealing sensitive information. Traditional phishing detection relies heavily on fixed keyword matching, which struggles with complex or novel deceptive techniques. 

To overcome these limitations, this system uses **RoBERTa (Robustly Optimized BERT Pretraining Approach)**. RoBERTa is a state-of-the-art Natural Language Processing (NLP) model based on the Transformer architecture. Unlike older models (such as RNNs or LSTMs), transformers use a "self-attention" mechanism that allows them to weigh the importance of different words in a sentence, capturing deep contextual meaning and user intent.

The system employs a two-tier architecture:
*   **FastAPI Backend**: Hosts the computationally heavy RoBERTa model and serves predictions over a REST API. Running an AI model is computationally heavy; placing it here ensures the UI remains responsive.
*   **Streamlit Frontend**: Provides an interactive, user-friendly dashboard for users to paste suspected emails and view the results quickly.
*   **Explainable AI (XAI)**: The system extracts specific urgency metrics or suspicious patterns (e.g., "account suspended") using heuristics alongside the ML model. This allows the system to provide a human-readable explanation of *why* an email was flagged, building user trust.

## 3. Procedure
1.  **Model Loading**: Initialize the pre-trained RoBERTa model during the backend application startup to minimize prediction latency.
2.  **Preprocessing**: Implement text preprocessing logic to clean the input email payload, handle punctuation, and normalize text casing.
3.  **Inference Pipeline**: Create a REST API endpoint (`/analyze`) that receives email text, tokenizes it, and passes it through the RoBERTa model to get a confidence score and a threat label ("Phishing" or "Safe").
4.  **Heuristic Scanning**: Complement the ML model by extracting hardcoded phishing indicators (e.g., urgency phrases like "act now" or "account suspended") using Regular Expressions.
5.  **Explainability**: Generate a user-friendly explanation based on the detected heuristic indicators to clarify the model's algorithmic decision.
6.  **Frontend Interface**: Develop a Streamlit application that accepts user input, makes an HTTP POST request to the back end, and visualizes the results (highlighting suspicious words and displaying confidence scores).
7.  **Execution**: Run the back-end server and the front-end interface concurrently to serve user requests on local ports.

## 4. Program (Core Snippets)

**Backend API (`api.py` snippet):**
```python
@app.post("/analyze")
async def analyze_email(email: EmailData):
    # Predict using RoBERTa model
    label, confidence = predict_email(email.text, tokenizer, model, device)
    
    # Detect hardcoded patterns (heuristics)
    indicators = detect_indicators(email.text)
    explanation = get_explanation(indicators)

    return {
        "threat_level": label,
        "confidence_score": round(float(confidence), 2),
        "flags": indicators,
        "xai_explanation": explanation
    }
```

**Frontend Dashboard (`app.py` snippet):**
```python
import streamlit as st
import requests

st.title("🛡️ SenseFlow Phishing Detection")
email_text = st.text_area("Paste the suspected email here:")

if st.button("🚀 Analyze Email"):
    resp = requests.post("http://localhost:8000/analyze", json={"text": email_text})
    result = resp.json()
    
    if result["threat_level"] == "Phishing":
        st.error(f"🚨 HIGH RISK - PHISHING DETECTED ({result['confidence_score']}%)")
    else:
        st.success(f"✅ SAFE ({result['confidence_score']}%)")
        
    st.info(result["xai_explanation"])
```

## 5. Output
The system produces a visual dashboard where users can input text. The output consists of:
*   **Threat Status**: A clear banner indicating if the email is Safe (✅) or Phishing (🚨).
*   **Confidence Score**: A percentage representing the RoBERTa model's certainty (e.g., 98.4%).
*   **Detected Indicators**: A list of suspicious flags found in the text (e.g., "Generic Greeting", "Urgent request").
*   **AI Explanation**: A short text explaining the rationale behind the flags.
*   **Highlighted Payload**: The original email text with urgent or suspicious words highlighted in red.

## 6. Results
The SenseFlow Phishing Detection System was successfully implemented and evaluated. The integration of a RoBERTa transformer model with a FastAPI backend and a Streamlit frontend allows for accurate, real-time, and explainable detection of phishing emails. The deep learning model correctly classifies complex deceptive language, outperforming traditional keyword-based heuristic approaches.
