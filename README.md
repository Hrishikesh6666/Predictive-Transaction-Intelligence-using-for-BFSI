# Predictive Transaction Intelligence for BFSI

> Fraud detection demo using XGBoost & Random Forest with a Streamlit front-end.

This repository contains notebooks, datasets and a simple Streamlit app that demonstrate transaction-level fraud detection for Banking, Financial Services & Insurance (BFSI) use-cases. The core models used are **XGBoost** and **RandomForest** trained on the included `card_fraud.csv` dataset.

---

## Repository contents (key files)

* `card_fraud.csv` — raw transactions dataset used for modeling.
* `card_fraud.csv_processed (2).csv`, `card_fraud.csv_processed.csv.csv` — processed versions used by notebooks.
* `XG_BOOST_fraud_dataset.ipynb` — notebook demonstrating preprocessing, feature engineering and XGBoost model training/evaluation.
* `fraudditection.ipynb` — alternate notebook (RandomForest, experiments, EDA).
* `Streamlit.py` — Streamlit front-end to demo model predictions interactively.
* `Hrishikesh_final.1.xlsm` — additional data/analysis workbook (macro-enabled).
* `requirements.txt` — Python package requirements.
* `LICENSE` — MIT license.

## Quick start

1. Clone the repo:

```bash
git clone https://github.com/Hrishikesh6666/Predictive-Transaction-Intelligence-using-for-BFSI.git
cd Predictive-Transaction-Intelligence-using-for-BFSI
```

2. Create a virtual environment and install:

```bash
python -m venv .venv
# linux / mac
source .venv/bin/activate
# windows
.venv\Scripts\activate

pip install -r requirements.txt
```

3. Run the Streamlit demo:

```bash
streamlit run Streamlit.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`) to interact with the demo.

4. Reproduce experiments:

* Open `XG_BOOST_fraud_dataset.ipynb` or `fraudditection.ipynb` in Jupyter / VS Code to run model training, EDA and evaluation steps.

---

## What the code does

* Loads and preprocesses transaction data.
* Trains models (XGBoost and RandomForest) for binary fraud classification.
* Evaluates using standard classification metrics (precision, recall, F1, AUC).
* Provides a small Streamlit UI to input transaction features and get a predicted fraud probability / label.

---

## Expected requirements

Typical packages (as in `requirements.txt`):

* `numpy`, `pandas`, `scikit-learn`
* `xgboost`
* `streamlit`
* `matplotlib`, `seaborn` (for plotting in notebooks)
* `joblib` or `pickle` (for model persistence)

If anything fails, run:

```bash
pip install -r requirements.txt --upgrade
```

---

## Notes, limitations & practical realities (be warned)

* **Data bias & imbalance**: Fraud datasets are heavily imbalanced. You’ll need to handle class imbalance (resampling, class weights, threshold tuning) before trusting model predictions.
* **Feature limitations**: The included dataset is likely a toy/academic dataset. Real-world BFSI fraud requires richer features (device metadata, geolocation, customer history, temporal patterns).
* **Evaluation**: Don’t rely solely on accuracy. Use precision, recall, F1 for the minority class and ROC-AUC / PR-AUC; operationally, tune for acceptable false positive rate vs detection rate.
* **No production plumbing**: This repo is for experimentation/proof-of-concept. No monitoring, no CI/CD, no secure model serving, no privacy-preserving or compliance controls. Do not deploy to production without proper engineering, logging, alerting and governance.
* **Explainability**: For BFSI, explainability is essential. Consider adding SHAP or LIME explanations before using in any human-facing workflows.

---

## Suggested next steps / improvements

1. Add stratified cross-validation and robust hyperparameter search (e.g., `RandomizedSearchCV` or `Optuna`).
2. Implement class-imbalance strategies: SMOTE variants, class weighting, focal loss for XGBoost.
3. Add model explainability (SHAP) and show explanations in the Streamlit app.
4. Build a small REST API (FastAPI / Flask) and containerize with Docker for realistic serving.
5. Add unit tests and CI checks for data schema, training reproducibility and model performance guards.
6. Add synthetic data generation and privacy checks if you plan to test on production-like data.

---

## How to contribute

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Commit changes and open a pull request describing your work and tests.

---

## License

MIT — see `LICENSE` file.

---

## Contact / Attribution

Repository owner: `Hrishikesh6666` (GitHub). Use Issues / Pull Requests on the repository to report bugs or propose changes.




