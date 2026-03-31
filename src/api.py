"""
SenseFlow API - FastAPI Backend
For Browser Extension Integration
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model_utils import detect_indicators, load_model, predict_email

# ========================= CONFIG =========================
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# """ best model among the models deberta,roberta,distilberta is roberta so the roberta model is used"""
DEFAULT_MODEL = "roberta"
# 
tokenizer = None
model = None
device = None
# =========================================================

app = FastAPI(
    title="SenseFlow Phishing Detector",
    description="Transformer-based Phishing Detection API for Browser Extension",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    """Load the Transformer model when API starts"""
    global tokenizer, model, device

    print(f"[SYSTEM] Loading {DEFAULT_MODEL.upper()} model...")

    model_path = MODELS_DIR / DEFAULT_MODEL.lower()

    if not model_path.exists():
        raise RuntimeError(f"❌ Model folder not found: {model_path}")

    try:
        tokenizer, model, device = load_model(str(model_path))
        print(f"[✅ SUCCESS] {DEFAULT_MODEL.upper()} model loaded on {device}")
    except Exception as e:
        print(f"[❌ ERROR] Model loading failed: {e}")
        raise


class EmailData(BaseModel):
    text: str


@app.post("/analyze")
async def analyze_email(email: EmailData):
    """Main endpoint used by Browser Extension"""
    if not email.text or not email.text.strip():
        raise HTTPException(status_code=400, detail="Email text cannot be empty")

    try:
        # Transformer Prediction
        label, confidence = predict_email(email.text, tokenizer, model, device)

        # Rule-based indicators
        indicators = detect_indicators(email.text)

        return {
            "threat_level": label,
            "confidence_score": round(float(confidence), 2),
            "flags": indicators,
            "model_used": DEFAULT_MODEL.upper(),
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {str(e)}"
        ) from e


@app.get("/health")
async def health_check():
    """Used by extension to check if backend is running"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_name": DEFAULT_MODEL.upper()
    }