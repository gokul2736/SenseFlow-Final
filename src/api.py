"""
SenseFlow FastAPI Backend
Handles the RoBERTa model inference for phishing detection.
"""

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model_utils import detect_indicators, load_model, predict_email

# ========================= CONFIG =========================
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

DEFAULT_MODEL = "roberta"

""" The roberta is selected after abilation study as it gave the best accuracy at training stage """

app = FastAPI(
    title="SenseFlow API",
    description="RoBERTa-based Phishing Detection Service",
    version="1.0"
)

tokenizer = None
model = None
device = None


@app.on_event("startup")
async def startup_event():
    """Load the RoBERTa model when API starts."""
    global tokenizer, model, device
    print(f"[SYSTEM] Loading {DEFAULT_MODEL.upper()} model...")

    model_path = MODELS_DIR / DEFAULT_MODEL.lower()
    if not model_path.exists():
        raise RuntimeError(f"Model folder not found: {model_path}")

    tokenizer, model, device = load_model(str(model_path))
    print(f"[SUCCESS] RoBERTa model loaded successfully.")

"""Ensures the model is loaded before the api starts """

class EmailData(BaseModel):
    text: str


def get_explanation(flags: List[str]) -> str:
    """Generates a simple local explanation based on detected flags i.e patterns"""
    if not flags:
        return "The email doesn't show strong / any phishing characteristics according to the trained model."
    
    return (f"The RoBERTa model flagged this email due to patterns like: "
            f"{', '.join(flags[:4])}. These are common indicators of phishing attempts.")


@app.post("/analyze")
async def analyze_email(email: EmailData):
    """Main endpoint for the phishing analysis."""
    if not email.text or not email.text.strip():
        raise HTTPException(status_code=400, detail="Email text cannot be empty.")

    try:
        label, confidence = predict_email(email.text, tokenizer, model, device)
        indicators = detect_indicators(email.text)
        explanation = get_explanation(indicators)

        return {
            "threat_level": label,
            "confidence_score": round(float(confidence), 2),
            "flags": indicators,
            "model_used": DEFAULT_MODEL.upper(),
            "xai_explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}") from e


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": DEFAULT_MODEL.upper()}


if __name__ == "__main__":
    import uvicorn
    print("[+] Starting SenseFlow Backend...")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)