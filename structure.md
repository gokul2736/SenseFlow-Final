## Project Structure

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
