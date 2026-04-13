# SenseFlow: Phishing & Social Engineering Detector

**Team:** Markandeyan Gokul, Kanamarlapudi Sai Charithanjali 

## 📌 Problem Statement
Traditional antivirus systems use signature-based detection, which fails against "Clean Attacks" (Business Email Compromise). SenseFlow uses **Semantic Analysis (BERT)** to detect psychological triggers like Urgency and Authority.

## 🚀 Tech Stack
* **AI Engine:** Google BERT (via Hugging Face Transformers)-Roberta Model
* **Explainability:** LIME (Local Interpretable Model-agnostic Explanations) through Llama X-AI
* **Frontend:** Streamlit
* **Backend:** PyTorch & Python 3.9+


## Setup  
### i) Clone the repository to local 
```
git clonehttps://github.com/gokul2736/SenseFlow-Final.git
```

### ii) Create a virtual Environment
### iii) Activate Venv
### iv) install requirements 
 ```
pip install requirements
```
### v) run the model in cpu
```
python src/main.py
```
### vi) run Streamlit for interface
```
streamlit run src/app.py
```

[Download Roberta - Model data through drive link ](https://drive.google.com/drive/folders/1cT2ODJgLEoATLFfN_wWPhffZid-mcVhH?usp=sharing)

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
|   ├── api.py
│   ├── model_utils.py
|   ├── main.py
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
