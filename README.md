# SenseFlow: Phishing & Social Engineering Detector

**TLead:** Markandeyan Gokul  
**TMemb:** Kanamarlapudi Sai Charithanjali 

## 📌 Problem Statement
Traditional antivirus systems use signature-based detection, which fails against "Clean Attacks" (Business Email Compromise). SenseFlow uses **Semantic Analysis (BERT)** to detect psychological triggers like Urgency and Authority.

## 🚀 Tech Stack
* **AI Engine:** Google BERT (via Hugging Face Transformers)
* **Explainability:** LIME (Local Interpretable Model-agnostic Explanations)
* **Frontend:** Streamlit
* **Backend:** PyTorch & Python 3.9+

##  Project Structure
```
SenseFlow/
│
├── data/
│   ├── raw/                  # Original datasets
│   └── processed/            # Cleaned datasets
│
├── models/                   # Trained transformer models
│   ├── distilbert/
│   ├── roberta/
│   └── deberta/
│
├── notebooks/                # Training notebooks
│   ├── DISTILBERT.ipynb
│   ├── ROBERTA.ipynb
│   ├── DEBERTA.ipynb
│
├── src/                      # Application source code
│   ├── app.py
│   ├── model_utils.py
│   ├── preprocessing.py
│   └── benchmark.py
│
├── docs/                     # Project documentation
│
├── README.md
└── requirements.txt
```

## Pipeline
              +----------------------+
              |   Email Input        |
              | (User Email Text)    |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Text Preprocessing |
              | remove html, urls,   |
              | lowercase, cleaning  |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |     Tokenization     |
              |  RoBERTa Tokenizer   |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Transformer Model  |
              | DistilBERT / RoBERTa |
              |     / DeBERTa        |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Phishing Detector  |
              |  Safe vs Phishing    |
              | Probability Score    |
              +----------+-----------+
                         |
                (If phishing detected)
                         |
                         v
              +----------------------+
              |   LLM Reasoning      |
              |      Llama 3.1       |
              | Detect manipulation  |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |   Explainable Output |
              | Urgency / Authority  |
              | Financial request    |
              +----------+-----------+
                         |
                         v
              +----------------------+
              |  User Interface      |
              | Web App / Extension  |
              | Warning Message      |
              +----------------------+
