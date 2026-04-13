import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReadmitIQ · Diabetic Readmission Risk",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Instrument+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
    background: #f7f4ef;
    color: #1a1a1a;
}

.stApp { background: #f7f4ef; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero header ── */
.hero {
    background: #1a1a1a;
    border-radius: 20px;
    padding: 48px 52px 44px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, #e8533422 0%, transparent 70%);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, #f0a50015 0%, transparent 70%);
}
.hero-tag {
    display: inline-block;
    background: #e85334;
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 99px;
    margin-bottom: 20px;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #f7f4ef !important;
    line-height: 1.1 !important;
    margin: 0 0 12px !important;
}
.hero p {
    color: #888 !important;
    font-size: 0.95rem;
    max-width: 560px;
    line-height: 1.6;
    margin: 0;
}
.hero-meta {
    margin-top: 28px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.hero-pill {
    background: #2a2a2a;
    border: 1px solid #333;
    color: #aaa;
    font-size: 0.75rem;
    padding: 6px 14px;
    border-radius: 8px;
    font-family: 'Instrument Sans', sans-serif;
}
.hero-pill span { color: #f7f4ef; font-weight: 500; }

/* ── Section cards ── */
.section-card {
    background: white;
    border-radius: 16px;
    padding: 28px 28px 24px;
    border: 1px solid #e8e4de;
    margin-bottom: 20px;
}
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #e85334;
    margin-bottom: 18px;
}

/* ── Form elements ── */
[data-testid="stSelectbox"] > div > div {
    background: #f7f4ef !important;
    border: 1.5px solid #e0dbd3 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
}
[data-testid="stNumberInput"] input {
    background: #f7f4ef !important;
    border: 1.5px solid #e0dbd3 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
}

label {
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #555 !important;
}

/* ── Slider accent ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #e85334 !important;
    border-color: #e85334 !important;
}

/* ── Predict button ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #f7f4ef !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 36px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #e85334 !important;
    box-shadow: 0 8px 24px #e8533430 !important;
}

/* ── Result cards ── */
.result-high {
    background: linear-gradient(135deg, #fff5f3 0%, #fff0ed 100%);
    border: 2px solid #e85334;
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
}
.result-low {
    background: linear-gradient(135deg, #f3faf5 0%, #edf7f0 100%);
    border: 2px solid #2d9e5c;
    border-radius: 20px;
    padding: 32px 28px;
    text-align: center;
}
.result-icon { font-size: 2.4rem; margin-bottom: 10px; }
.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 6px;
}
.result-verdict.high { color: #c0392b; }
.result-verdict.low  { color: #1e7e46; }
.result-sub {
    color: #777;
    font-size: 0.83rem;
    line-height: 1.5;
    max-width: 300px;
    margin: 0 auto;
}
.risk-number {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    margin: 16px 0 2px;
    line-height: 1;
}
.risk-number.high { color: #e85334; }
.risk-number.low  { color: #2d9e5c; }
.risk-label {
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #aaa;
}

/* ── Metric strip ── */
.metric-strip {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 20px;
}
.metric-chip {
    flex: 1;
    min-width: 80px;
    background: white;
    border: 1px solid #e8e4de;
    border-radius: 12px;
    padding: 12px 14px;
    text-align: center;
}
.metric-chip .val {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a1a1a;
}
.metric-chip .lbl {
    font-size: 0.65rem;
    color: #999;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Disclaimer ── */
.disclaimer {
    background: #fffbf0;
    border-left: 3px solid #f0a500;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 0.77rem;
    color: #7a6200;
    line-height: 1.6;
    margin-top: 16px;
}

/* ── Awaiting state ── */
.awaiting {
    text-align: center;
    padding: 60px 20px;
    color: #ccc;
}
.awaiting-icon { font-size: 3rem; margin-bottom: 16px; }
.awaiting-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #bbb;
    margin-bottom: 8px;
}
.awaiting-sub {
    font-size: 0.83rem;
    line-height: 1.6;
    max-width: 240px;
    margin: 0 auto;
    color: #ccc;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #bbb;
    font-size: 0.75rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #e8e4de;
}
.footer strong { color: #888; }
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = Path("model/model_01.pkl")
    if path.exists():
        return joblib.load(path), True
    return None, False

model, model_loaded = load_model()


# ── Gauge chart ───────────────────────────────────────────────────────────────
def risk_gauge(prob, high):
    color = "#e85334" if high else "#2d9e5c"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number=dict(suffix="%", font=dict(color=color, family="Syne", size=30)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#ccc",
                      tickfont=dict(color="#aaa", size=10),
                      tickvals=[0, 25, 50, 75, 100]),
            bar=dict(color=color, thickness=0.22),
            bgcolor="#f7f4ef",
            borderwidth=0,
            steps=[
                dict(range=[0,   25],  color="#e8f5ec"),
                dict(range=[25,  50],  color="#fff8e8"),
                dict(range=[50,  75],  color="#fff0ec"),
                dict(range=[75, 100],  color="#fde8e4"),
            ],
            threshold=dict(line=dict(color=color, width=3),
                           thickness=0.8, value=prob * 100),
        ),
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=10),
        height=175,
        font=dict(color='#888'),
    )
    return fig


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🫀 Clinical Decision Support</div>
    <h1>ReadmitIQ</h1>
    <p>Predict 30-day hospital readmission risk for diabetic patients using validated
    machine learning — supporting faster, evidence-informed clinical decisions.</p>
    <div class="hero-meta">
        <div class="hero-pill">Accuracy <span>~94%</span></div>
        <div class="hero-pill">Dataset <span>99,900 records · 10 years</span></div>
        <div class="hero-pill">Threshold <span>≥ 25% = High Risk</span></div>
        <div class="hero-pill">Algorithm <span>Gradient Boosting</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.warning("⚠️ Model not found at `model/model_01.pkl` — running in demo mode.")

# ── LAYOUT ────────────────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.15, 0.85], gap="large")

with col_form:

    # 01 Demographics
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">01 · Patient Demographics</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        race = st.selectbox("Race", [0,1,2,3,4],
            format_func=lambda x: ["Caucasian","African American","Hispanic","Asian","Other"][x])
    with d2:
        gender = st.selectbox("Gender", [0,1],
            format_func=lambda x: ["Female","Male"][x])
    with d3:
        age = st.selectbox("Age Group", list(range(10)),
            format_func=lambda x: f"[{x*10}–{x*10+10})")
    st.markdown('</div>', unsafe_allow_html=True)

    # 02 Hospital Stay
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">02 · Hospital Stay & Utilisation</div>', unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    with h1:
        time_in_hospital = st.slider("Days in Hospital", 1, 14, 3)
    with h2:
        number_emergency = st.number_input("Emergency Visits", 0, 50, 0)
    with h3:
        total_procedures = st.number_input("Total Procedures", 0, 100, 1)
    outpatient_to_inpatient_ratio = st.slider(
        "Outpatient / Inpatient Visit Ratio", 0.0, 20.0, 1.0, 0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # 03 Lab Results
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 · Lab Results</div>', unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    with l1:
        max_glu_serum = st.selectbox("Max Glucose Serum", [0,1,2,3],
            format_func=lambda x: ["None",">200",">300","Normal"][x])
    with l2:
        A1Cresult = st.selectbox("HbA1c Result", [0,1,2,3],
            format_func=lambda x: ["None",">7",">8","Normal"][x])
    st.markdown('</div>', unsafe_allow_html=True)

    # 04 Medications
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">04 · Medications</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        insulin = st.selectbox("Insulin", [0,1,2,3],
            format_func=lambda x: ["No","Down","Steady","Up"][x])
    with m2:
        change = st.selectbox("Med Change", [0,1],
            format_func=lambda x: ["No","Yes"][x])
    with m3:
        diabetesMed = st.selectbox("Diabetes Med", [0,1],
            format_func=lambda x: ["No","Yes"][x])
    with m4:
        medication = st.number_input("# Medications", 0, 50, 5)
    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("🔍  Assess Readmission Risk")


# ── RESULT PANEL ──────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Risk Assessment</div>', unsafe_allow_html=True)

    if predict_clicked:
        features = np.array([
            race, gender, age, time_in_hospital, max_glu_serum,
            A1Cresult, insulin, change, diabetesMed, number_emergency,
            outpatient_to_inpatient_ratio, total_procedures, medication
        ]).reshape(1, -1)

        if model_loaded:
            proba = float(model.predict_proba(features)[0][1])
        else:
            proba = min(0.95, max(0.05,
                0.1 + time_in_hospital * 0.03
                + number_emergency * 0.04
                + (1 - diabetesMed) * 0.1
                + change * 0.08
                + (age / 10) * 0.02
            ))

        high = proba >= 0.45
        pct  = round(proba * 100, 1)
        cls  = "high" if high else "low"
        icon = "⚠️" if high else "✅"
        verdict = "High Risk" if high else "Low Risk"
        advice = (
            "Elevated readmission risk detected. Consider a structured discharge plan and follow-up within 7 days."
            if high else
            "Lower readmission likelihood. Routine follow-up and medication adherence counselling recommended."
        )
        card_cls = "result-high" if high else "result-low"

        st.markdown(f"""
        <div class="{card_cls}">
            <div class="result-icon">{icon}</div>
            <div class="result-verdict {cls}">{verdict}</div>
            <div class="risk-number {cls}">{pct}%</div>
            <div class="risk-label">30-Day Readmission Probability</div>
            <p class="result-sub" style="margin-top:12px;">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(risk_gauge(proba, high),
                        use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown(f"""
        <div class="metric-strip">
            <div class="metric-chip">
                <div class="val">{time_in_hospital}d</div>
                <div class="lbl">Stay</div>
            </div>
            <div class="metric-chip">
                <div class="val">{number_emergency}</div>
                <div class="lbl">Emergency</div>
            </div>
            <div class="metric-chip">
                <div class="val">{medication}</div>
                <div class="lbl">Meds</div>
            </div>
            <div class="metric-chip">
                <div class="val">{'Yes' if change else 'No'}</div>
                <div class="lbl">Med Change</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            <strong>⚕️ Disclaimer:</strong> This tool supports clinical decision-making only.
            It does not replace professional medical judgement or diagnosis.
            Always review results within the full context of patient history.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="awaiting">
            <div class="awaiting-icon">🫀</div>
            <div class="awaiting-title">Awaiting Patient Data</div>
            <div class="awaiting-sub">
                Complete the form on the left and click
                <strong style="color:#888;">Assess Readmission Risk</strong>
                to generate a prediction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <strong>ReadmitIQ</strong> · 30-Day Diabetic Readmission Risk Predictor ·
    MIT World Peace University, Pune · {datetime.now().year}<br>
    Saaransh Johri · Tanmay Dhumal · Milind Muravane · Dr. Devendra Joshi
</div>
""", unsafe_allow_html=True)
