"""Product Review Sentiment Analysis: classify reviews as positive or negative with machine learning."""
import json

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from train import DATA_PATH, METRICS_PATH, MODEL_PATH, train
from ui import apply_style, footer, hero

COLORS = {"positive": "#16A34A", "negative": "#DC2626"}

st.set_page_config(page_title="Review Sentiment Analysis", page_icon="📊", layout="wide")
apply_style()


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        train()
    return joblib.load(MODEL_PATH), json.loads(METRICS_PATH.read_text())


def predict(model, texts):
    labels = model.predict(texts)
    confidence = model.predict_proba(texts).max(axis=1)
    return labels, confidence


model, metrics = load_model()

with st.sidebar:
    st.header("🧠 Model")
    st.metric("Test accuracy", f"{metrics['accuracy']:.1%}")
    st.caption(f"Trained on {metrics['train_size']} reviews, tested on {metrics['test_size']}.")
    st.markdown("**Algorithm:** TF-IDF (1-2 word phrases) + Logistic Regression")
    if st.button("🔄 Retrain model", use_container_width=True):
        with st.spinner("Training…"):
            train()
        load_model.clear()
        st.rerun()

hero(
    "📊 Product Review Sentiment Analysis",
    "A machine learning model that reads customer reviews and tells you whether they are positive or "
    "negative — one at a time or thousands at once from a CSV file.",
    start="#EA580C",
    end="#DC2626",
)

single_tab, bulk_tab, perf_tab = st.tabs(["✍️ Single Review", "📁 Bulk Analysis (CSV)", "📈 Model Performance"])

# ---------- Single review ----------
with single_tab:
    text = st.text_area(
        "Write or paste a review",
        height=120,
        placeholder="e.g. The headphones have amazing sound quality and the battery lasts all day.",
    )
    if st.button("Analyze sentiment", type="primary", disabled=not text.strip()):
        (label,), (conf,) = predict(model, [text])
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            emoji = "😊" if label == "positive" else "😞"
            st.markdown(
                f'<div class="card" style="text-align:center; border-left: 6px solid {COLORS[label]};">'
                f'<div style="font-size:3rem">{emoji}</div>'
                f'<h3 style="color:{COLORS[label]}; margin:0">{label.title()}</h3>'
                f'<p class="muted">Confidence {conf:.0%}</p></div>',
                unsafe_allow_html=True,
            )
        with c2:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(conf * 100),
                number={"suffix": "%"},
                title={"text": "Confidence"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": COLORS[label]}},
            ))
            gauge.update_layout(height=230, margin=dict(t=40, b=10, l=30, r=30))
            st.plotly_chart(gauge, use_container_width=True)

# ---------- Bulk CSV ----------
with bulk_tab:
    st.markdown('<p class="muted">Upload a CSV file with a column of review text.</p>', unsafe_allow_html=True)
    upload = st.file_uploader("Upload CSV", type="csv")
    use_sample = st.button("Use sample file (40 reviews)")
    if use_sample:
        st.session_state.bulk_df = pd.read_csv(DATA_PATH.parent / "new_reviews_to_test.csv")
    if upload is not None:
        st.session_state.bulk_df = pd.read_csv(upload)

    df = st.session_state.get("bulk_df")
    if df is not None:
        text_columns = [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == object]
        if not text_columns:
            st.error("No text column found in this file.")
        else:
            default = text_columns.index("review") if "review" in text_columns else 0
            column = st.selectbox("Which column has the review text?", text_columns, index=default)
            result = df.copy()
            texts = result[column].fillna("").astype(str)
            result["sentiment"], result["confidence"] = predict(model, texts)
            result["confidence"] = result["confidence"].round(3)

            counts = result["sentiment"].value_counts()
            k1, k2, k3 = st.columns(3)
            k1.metric("Total reviews", len(result))
            k2.metric("Positive", int(counts.get("positive", 0)), f"{counts.get('positive', 0) / len(result):.0%}")
            k3.metric("Negative", int(counts.get("negative", 0)), f"-{counts.get('negative', 0) / len(result):.0%}")

            ch1, ch2 = st.columns(2, gap="large")
            pie = px.pie(
                names=counts.index, values=counts.values, hole=0.55,
                color=counts.index, color_discrete_map=COLORS, title="Sentiment share",
            )
            ch1.plotly_chart(pie, use_container_width=True)
            hist = px.histogram(
                result, x="confidence", color="sentiment", nbins=20, barmode="overlay",
                color_discrete_map=COLORS, title="How confident is the model?",
            )
            ch2.plotly_chart(hist, use_container_width=True)

            st.dataframe(
                result[[column, "sentiment", "confidence"]],
                use_container_width=True,
                hide_index=True,
                column_config={"confidence": st.column_config.ProgressColumn("confidence", min_value=0, max_value=1)},
            )
            st.download_button(
                "⬇️ Download results (CSV)",
                result.to_csv(index=False).encode("utf-8"),
                file_name="sentiment_results.csv",
                mime="text/csv",
            )

# ---------- Model performance ----------
with perf_tab:
    report = metrics["report"]
    p1, p2, p3 = st.columns(3)
    p1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    p2.metric("Precision (avg)", f"{report['macro avg']['precision']:.1%}")
    p3.metric("Recall (avg)", f"{report['macro avg']['recall']:.1%}")

    g1, g2 = st.columns(2, gap="large")
    labels = metrics["labels"]
    cm = px.imshow(
        metrics["confusion_matrix"], x=labels, y=labels, text_auto=True, color_continuous_scale="Blues",
        labels=dict(x="Predicted", y="Actual", color="Reviews"), title="Confusion matrix",
    )
    g1.plotly_chart(cm, use_container_width=True)
    table = pd.DataFrame({k: report[k] for k in labels}).T[["precision", "recall", "f1-score", "support"]]
    g2.markdown("**Per-class scores**")
    g2.dataframe(table.style.format({"precision": "{:.2f}", "recall": "{:.2f}", "f1-score": "{:.2f}", "support": "{:.0f}"}),
                 use_container_width=True)
    g2.caption(
        "The bundled dataset is a small sample so the app runs out of the box. Replace data/reviews.csv "
        "with a real dataset (columns: review, sentiment) and click Retrain for real-world results."
    )

footer()
