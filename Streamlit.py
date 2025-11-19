# app.py
import streamlit as st
import pandas as pd
import joblib
import io
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fraud Detection - Demo", layout="wide")

st.title("Fraud Detection — Streamlit Frontend")
st.markdown("Upload a CSV of transactions. This app will preprocess, predict and let you download the results.")

# Load artifacts
@st.cache_resource
def load_artifacts():
    preprocessor = joblib.load("artifacts/preprocessor.pkl")
    model = joblib.load("artifacts/xgb_model.pkl")
    return preprocessor, model

try:
    preprocessor, model = load_artifacts()
    st.success("Loaded model and preprocessor.")
except Exception as e:
    st.error(f"Error loading artifacts: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload CSV (transactions)", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    st.subheader("Input sample")
    st.dataframe(df.head(5))

    # Identify whether there's a known target column
    possible_targets = ['Class', 'isFraud', 'fraud', 'label', 'target']
    target = next((t for t in possible_targets if t in df.columns), None)

    X = df.drop(columns=[target]) if target is not None else df.copy()

    # Preprocess and predict
    try:
        X_prep = preprocessor.transform(X)
    except Exception as e:
        st.error("Preprocessing failed. Make sure uploaded CSV has same schema as training data.\n\n" + str(e))
        st.stop()

    preds = model.predict(X_prep)
    pred_proba = model.predict_proba(X_prep)[:, 1]

    # Prepare output
    out = X.reset_index(drop=True).copy()
    out["pred_label"] = preds
    out["pred_proba"] = pred_proba

    if target is not None:
        out[target] = df[target].reset_index(drop=True)

    st.subheader("Prediction sample")
    st.dataframe(out.head(10))

    # If ground truth exists, show metrics
    if target is not None:
        y_true = out[target]
        y_pred = out["pred_label"]
        try:
            acc = accuracy_score(y_true, y_pred) * 100
            prec = precision_score(y_true, y_pred, zero_division=0) * 100
            rec = recall_score(y_true, y_pred, zero_division=0) * 100
            f1 = f1_score(y_true, y_pred, zero_division=0) * 100
            roc = roc_auc_score(y_true, out["pred_proba"]) * 100

            st.subheader("Evaluation Metrics (on uploaded data)")
            col1, col2, col3 = st.columns(3)
            col1.metric("Accuracy", f"{acc:.2f}%")
            col2.metric("F1 Score", f"{f1:.2f}%")
            col3.metric("ROC-AUC", f"{roc:.2f}%")

            with st.expander("Detailed classification report"):
                st.text(classification_report(y_true, y_pred, zero_division=0))
        except Exception as e:
            st.warning("Could not compute metrics: " + str(e))

    # Confusion matrix plot (if possible)
    if target is not None:
        try:
            cm = confusion_matrix(out[target], out["pred_label"])
            fig, ax = plt.subplots(figsize=(4,3))
            im = ax.imshow(cm, cmap="Blues")
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    ax.text(j, i, cm[i, j], ha="center", va="center")
            st.pyplot(fig)
        except Exception:
            pass

    # Let user download predictions
    csv_buffer = io.StringIO()
    out.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()
    st.download_button("Download predictions CSV", data=csv_bytes, file_name="predictions.csv", mime="text/csv")

    st.info("If your uploaded CSV doesn't match the training schema, do preprocessing to match columns (e.g., datetime columns, categorical names).")
else:
    st.info("Upload a CSV file to get started. If you'd like a sample file, generate `artifacts/test_predictions.csv` using the helper script.")
