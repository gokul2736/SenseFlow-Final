"""
SenseFlow Model Utilities
Core functions for loading Transformer models and running phishing detection inference.
Enhanced with spaCy for better entity detection and explainability.
"""

import re
from typing import List, Tuple

import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import spacy

# Load spaCy model once at module level (efficient)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("[WARNING] spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None


def load_model(model_path: str) -> Tuple:
    """
    Loads a fine-tuned HuggingFace transformer model + tokenizer from local folder.
    Automatically uses GPU if available.
    """
    print(f"[SYSTEM] Loading model from {model_path}...")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    model.to(device)
    model.eval()

    print(f"[SUCCESS] Model loaded on {device.type.upper()}")
    return tokenizer, model, device


def predict_email(
    text: str, tokenizer, model, device
) -> Tuple[str, float]:
    """
    Runs inference on raw email text and returns (label, confidence).
    Label: "Phishing" or "Safe"
    """
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probabilities = F.softmax(logits, dim=-1)
    confidence_score = torch.max(probabilities).item()
    predicted_class_id = torch.argmax(probabilities, dim=-1).item()

    label = "Phishing" if predicted_class_id == 1 else "Safe"
    confidence_pct = round(confidence_score * 100, 2)

    return label, confidence_pct


def detect_indicators(text: str) -> List[str]:
    """
    Enhanced indicator detection using regex + spaCy NER.
    Returns list of detected threat indicators.
    """
    text_lower = text.lower()
    detected = []

    # 1. Regex-based patterns (fast and reliable)
    patterns = {
        "Urgency / Time Pressure": r"\b(urgent|immediately|asap|now|act fast|overdue|suspended|limited time)\b",
        "Financial Payload": r"\b(bank|account|payment|transfer|money|invoice|billing|paypal|credit card|payment required)\b",
        "Credential Harvesting": r"\b(verify|password|login|credentials|authenticate|click here|reset password|account suspended)\b",
        "Threat / Fear": r"\b(hacked|compromised|suspended|blocked|fraud|warning|alert|security breach)\b",
        "Authority Impersonation": r"\b(admin|support|team|official|security|it department|manager)\b",
    }

    for category, pattern in patterns.items():
        if re.search(pattern, text_lower):
            detected.append(category)

    # 2. spaCy NER for advanced entity detection (if model is loaded)
    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                detected.append("Financial Amount Mentioned")
            elif ent.label_ == "URL":
                detected.append("Suspicious External Link")
            elif ent.label_ == "EMAIL":
                detected.append("Email Address Harvesting")
            elif ent.label_ == "ORG" and any(word in ent.text.lower() for word in ["bank", "paypal", "google", "microsoft"]):
                detected.append("Impersonated Organization")

    # Remove duplicates while preserving order
    return list(dict.fromkeys(detected))