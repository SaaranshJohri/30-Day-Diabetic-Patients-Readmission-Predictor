from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("model_01.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            int(request.form['race']),
            int(request.form['gender']),
            int(request.form['age']),
            int(request.form['time_in_hospital']),
            int(request.form['max_glu_serum']),
            int(request.form['A1Cresult']),
            int(request.form['insulin']),
            int(request.form['change']),
            int(request.form['diabetesMed']),
            int(request.form['number_emergency']),
            float(request.form['outpatient_to_inpatient_ratio']),
            int(request.form['total_procedures']),
            int(request.form['medication'])
        ]
    except:
        return "Error: Invalid input types. Please check your values."

    # Predict
    proba = model.predict_proba(np.array(features).reshape(1, -1))[0][1]  # Probability of class 1
    prediction = 1 if proba >= 0.25 else 0  # You can even lower threshold

    result = f"The patient is {'likely' if prediction == 1 else 'not likely'} to be readmitted."

    return render_template('index.html', prediction_text=f"{result}")

if __name__ == "__main__":
    app.run(debug=True)
