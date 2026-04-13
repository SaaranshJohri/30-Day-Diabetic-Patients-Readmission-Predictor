# 🏥 30-Day Diabetic Patients Readmission Predictor

A machine learning web application that predicts whether a diabetic patient
will be readmitted to the hospital within 30 days of discharge — built with
an ensemble of gradient boosting models and deployed via Streamlit.

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Training Accuracy | 0.9977 |
| Testing Accuracy | 0.9703 |
| Cross-Validation Score | 0.9570 |

> Model file (~331 MB) is not included in this repository due to GitHub's
> file size limit. Download instructions below.

---

## 🧠 Confusion Matrix (Test Set)

|  | Predicted Not Readmitted | Predicted Readmitted |
|--|--------------------------|----------------------|
| **Actual Not Readmitted** | 25,606 (TN) | 1,517 (FP) |
| **Actual Readmitted** | 89 (FN) | 27,034 (TP) |

- Very low false negatives — critical for healthcare applications.
- Model favours false positives over false negatives, the safer tradeoff
  in a clinical context.

---

## 📈 Classification Report (Test Set)

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Not Readmitted (0) | 0.94 | 0.94 | 0.97 |
| Readmitted (1) | 0.95 | 1.00 | 0.97 |
| **Overall Accuracy** | | | **0.97** |

The model achieves **perfect recall (1.00)** for readmitted patients,
meaning it misses almost no high-risk cases — the most important
property for a clinical screening tool.

---

## 🖥️ Dashboard Features

Built with **Streamlit** — replaces the original Flask frontend with a
faster, more maintainable single-file deployment.

- Inputs organised into four clinical sections:
  Patient Demographics · Hospital Stay · Lab Results · Medications
- Risk output with probability score and colour-coded verdict
  (High Risk / Low Risk)
- Animated gauge chart showing readmission probability
- Quick-view summary chips for key patient indicators
- Prediction threshold set at **≥ 25%** for high-risk classification
- Clinical disclaimer on every result

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| Model | Scikit-learn · Gradient Boosting · PowerTransformer |
| Backend | Python · Joblib |
| Frontend | Streamlit · Plotly |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Run Locally

```bash
git clone https://github.com/SaaranshJohri/30-Day-Diabetic-Patients-Readmission-Predictor
cd 30-Day-Diabetic-Patients-Readmission-Predictor

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Download the model file and place it at `model/model_01.pkl`,
then run:

```bash
streamlit run app.py
```

## 🧪 Sample Predictions

**High Risk Patient**
Age: 85 · Female · Glucose >300 · A1C >8 · Insulin: Up · 3 prior inpatient visits
→ `Likely to be readmitted`

**Low Risk Patient**
Age: 35 · Male · Glucose Normal · A1C None · Insulin: No · 2 outpatient visits
→ `Not likely to be readmitted`

---

## 📬 Contact

**Saaransh Johri** — MIT World Peace University, Pune
saaransh.johri@mitwpu.edu.in

---

> ⚕️ **Disclaimer:** This is a research prototype and decision-support tool
> only. It does not replace professional medical judgement or clinical
> validation.
