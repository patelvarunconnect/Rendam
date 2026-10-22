"""Train the sentiment model (TF-IDF + Logistic Regression) and save it with its test metrics."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "reviews.csv"
MODEL_PATH = ROOT / "model" / "sentiment_model.joblib"
METRICS_PATH = ROOT / "model" / "metrics.json"


def train(data_path=DATA_PATH):
    if not data_path.exists():  # first run: create the sample dataset
        import generate_data
        generate_data.main()
    df = pd.read_csv(data_path).dropna(subset=["review", "sentiment"])
    df["sentiment"] = df["sentiment"].str.lower().str.strip()
    x_train, x_test, y_train, y_test = train_test_split(
        df["review"], df["sentiment"], test_size=0.2, random_state=42, stratify=df["sentiment"]
    )

    # Stop words are kept on purpose: words like "not" change the meaning of a review
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, lowercase=True)),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    model.fit(x_train, y_train)

    predicted = model.predict(x_test)
    labels = sorted(df["sentiment"].unique())
    metrics = {
        "accuracy": accuracy_score(y_test, predicted),
        "labels": labels,
        "confusion_matrix": confusion_matrix(y_test, predicted, labels=labels).tolist(),
        "report": classification_report(y_test, predicted, output_dict=True),
        "train_size": len(x_train),
        "test_size": len(x_test),
    }

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    return model, metrics


if __name__ == "__main__":
    _, m = train()
    print(f"Model saved to {MODEL_PATH}")
    print(f"Test accuracy: {m['accuracy']:.2%} on {m['test_size']} reviews")
