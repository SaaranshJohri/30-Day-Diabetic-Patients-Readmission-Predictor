# 🏥 30-Day Diabetic Patients Readmission Predictor

This project builds a machine learning model to predict whether a diabetic patient will be readmitted to the hospital within 30 days of discharge. It includes model training, evaluation, and deployment using a Flask-based web application with a modern, user-friendly frontend.

---

## 📊 Model Overview

- **Algorithm Used**: Random Forest Classifier  
- **Training Accuracy**: **0.9977**  
- **Testing Accuracy**: **0.9703**  
- **Cross-Validation Score**: **0.9570**

---

## 🧠 Confusion Matrix (Test Set)
|              | Predicted Not Readmitted | Predicted Readmitted |
|--------------|--------------------------|-----------------------|
| **Actual Not Readmitted** | 25,606 (TN)              | 1,517 (FP)            |
| **Actual Readmitted**     | 89 (FN)                  | 27,034 (TP)           |

- Very low false negatives (FN), which is crucial in healthcare.
- Model tends to predict more false positives than false negatives—safer in medical use cases.

---

## 📈 Classification Report (Test Set)

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Not Readmitted (0) | 0.94 | 0.94 | 0.97 | 27,123 |
| Readmitted (1)     | 0.95 | 1.00 | 0.97 | 27,123 |
| **Accuracy**       |      |      | **0.97** | 54,246 |

> 🔍 **Interpretation**:  
> The model demonstrates **exceptional recall (1.00)** for readmitted patients, making it highly effective at identifying high-risk cases.

---

## ⚙️ Technologies Used

- Python
- Scikit-learn
- Flask
- PowerTransformer
- Joblib
- Bootstrap (Frontend)
- HTML5, FontAwesome (UI)

---

## 🌐 Web Interface Features

The trained model is deployed using Flask and includes a responsive HTML5-based UI.

**Frontend Features:**
- Clean, healthcare-themed design using Bootstrap and CSS
- Inputs for age, race, gender, glucose levels, insulin use, etc.
- Prediction output with:
  - **Risk Status**: Likely / Not Likely
  - **Confidence Score**
- Icons for input clarity using FontAwesome

---

## 🧪 Sample Use Cases

### ✅ Readmitted Patient
- Age: 85  
- Gender: Female  
- Glucose: >300  
- A1Cresult: >8  
- Insulin: Up  
- Outpatient visits: 0  
- Inpatient visits: 3  

→ **Prediction: Likely to be readmitted**

---

### ❌ Not Readmitted Patient
- Age: 35  
- Gender: Male  
- Glucose: Normal  
- A1Cresult: None  
- Insulin: No  
- Outpatient visits: 2  
- Inpatient visits: 0  

→ **Prediction: Not likely to be readmitted**

---

## 📁 Files

| File | Description |
|------|-------------|
| `app.py` | Flask app for backend processing |
| `templates/form.html` | HTML frontend |
| `README.md` | You’re here. |

---

## 📬 Contact

**Author:** Saaransh Johri  
**Affiliation:** MIT World Peace University  
📧 saaransh.johri@mitwpu.edu.in

---

> 🚨 **Disclaimer:** This is a research prototype. It should not be used for real medical decision-making without clinical validation.

