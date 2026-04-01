"""
SenseFlow Model Utilities
Handles loading the RoBERTa model and running phishing detection with basic explainability.
"""

import re
from typing import List, Tuple

import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import spacy

# Load spaCy for better entity detection...to preview the basic type of fraud/attempt of pishing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

def load_model(model_path: str) -> Tuple:
    """Load the fine-tuned RoBERTa model from local directory."""
    print(f"[SYSTEM] Loading RoBERTa model from {model_path}...")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    # using autotokenizer

    model.to(device)
    model.eval()

    print(f"[SUCCESS] RoBERTa model loaded on {device.type.upper()}")
    return tokenizer, model, device


def predict_email(text: str, tokenizer, model, device) -> Tuple[str, float]:
    """Perform inference and return threat label with confidence percentage."""
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probabilities = F.softmax(logits, dim=-1)
    confidence_score = torch.max(probabilities).item()
    predicted_class = torch.argmax(probabilities, dim=-1).item()

    label = "Phishing" if predicted_class == 1 else "Safe"
    confidence_pct = round(confidence_score * 100, 2)

    return label, confidence_pct


"""1-shows the signs of pishing or anamolity and 0- indicate the negative risk"""

def detect_indicators(text: str) -> List[str]:
    """
    Detect common phishing indicators using the  regex  pattern matching standard and spaCy-NLP.
    This helps provide better reasoning to the user.
    """
    text_lower = text.lower()
    detected = []

    # Common phishing patterns - these are the  common indicators hightly recognized in phishing attempts
    patterns = {
        "Urgency / Time Pressure": r"\b(urgent|immediately|asap|now|act fast|overdue|suspended)\b",
        "Financial Payload": r"\b(bank|account|payment|transfer|money|invoice|billing|paypal)\b",
        "Credential Harvesting": r"\b(verify|password|login|credentials|authenticate|reset password)\b",
        "Threat / Fear": r"\b(hacked|compromised|blocked|fraud|warning|alert)\b",
        "Authority Impersonation": r"\b(admin|support|official|security)\b",
    }

    for category, pattern in patterns.items():
        if re.search(pattern, text_lower):
            detected.append(category)

    # Additional detection using spaCy-NLP
    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                detected.append("Financial Amount Mentioned")
            elif ent.label_ == "URL":
                detected.append("Suspicious External Link")

    return list(dict.fromkeys(detected))