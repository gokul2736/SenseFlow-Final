"""
SenseFlow Model Utilities
Core functions for loading Transformer models and running phishing detection inference.
"""

import re
from typing import List, Tuple

import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def load_model(model_path: str) -> Tuple:
    """
    Loads a fine-tuned HuggingFace transformer model + tokenizer from local folder.
    Automatically uses GPU if available.
    """
    print(f"[SYSTEM] Loading model from {model_path}...")

    # Auto-detect hardware
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
    # Tokenize with safe length limit
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="pt",
    ).to(device)

    # Forward pass (no gradients needed)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Convert to probabilities
    probabilities = F.softmax(logits, dim=-1)
    confidence_score = torch.max(probabilities).item()
    predicted_class_id = torch.argmax(probabilities, dim=-1).item()

    label = "Phishing" if predicted_class_id == 1 else "Safe"
    confidence_pct = round(confidence_score * 100, 2)

    return label, confidence_pct


def detect_indicators(text: str) -> List[str]:
    """
    Rule-based scanner for common social engineering & phishing patterns.
    Returns list of detected threat indicators.
    """
    text_lower = text.lower()
    detected = []

    patterns = {
        "Urgency / Time Pressure": r"\b(urgent|immediately|asap|now|act fast|overdue|suspended|limited time)\b",
        "Financial Payload": r"\b(bank|account|payment|transfer|money|invoice|billing|paypal|credit card)\b",
        "Credential Harvesting": r"\b(verify|password|login|credentials|authenticate|click here|reset password)\b",
        "Threat / Fear": r"\b(hacked|compromised|suspended|blocked|fraud|warning|alert)\b",
        "Authority Impersonation": r"\b(admin|support|team|official|security|it department)\b",
    }

    for category, pattern in patterns.items():
        if re.search(pattern, text_lower):
            detected.append(category)

    return detected
    