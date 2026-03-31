# src/benchmark.py
import os

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def run_baseline_failure_benchmark():
    print("--- SenseFlow: Baseline Failure Benchmark ---")
    file_path = "data/processed/processed_data.csv"

    if not os.path.exists(file_path):
        print("ERROR: processed_data.csv not found. Run preprocessing.py first!")
        return

    df = pd.read_csv(file_path).dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42
    )

    # Standard Keyword Matching
    vectorizer = CountVectorizer(max_features=2000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train Naive Bayes
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # Evaluate
    predictions = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\n🎯 Target Metric - Baseline Accuracy: {accuracy * 100:.2f}%")
    print("ANALYSIS: Naive Bayes evaluates words in isolation (Bag of Words).")
    print(
        "CONCLUSION: It fundamentally fails to capture psycholinguistic intent (Urgency/Authority) in BEC attacks."
    )
    print("PIVOT: Shifting to RoBERTa-based architecture for semantic understanding.")


if __name__ == "__main__":
    run_baseline_failure_benchmark()
