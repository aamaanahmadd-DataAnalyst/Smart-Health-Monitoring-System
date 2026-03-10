import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from modules.vital import ALERT_CSS, shms_alert, rec_item

RESULT_CSS = """
<style>
.risk-banner {
    border-radius: 16px;
    padding: 24px 28px;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
}
.risk-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -20px;
    width: 200px; height: 200px;
    border-radius: 50%;
    opacity: 0.08;
    background: white;
}
.risk-banner.low      { background: linear-gradient(135deg, #1a5e35, #27ae60); border: 1px solid #2ecc71; }
.risk-banner.mild     { background: linear-gradient(135deg, #7d6608, #d4ac0d); border: 1px solid #f1c40f; }
.risk-banner.moderate { background: linear-gradient(135deg, #784212, #d35400); border: 1px solid #e67e22; }
.risk-banner.severe   { background: linear-gradient(135deg, #7b241c, #c0392b); border: 1px solid #e74c3c; }

.risk-icon  { font-size: 3rem; flex-shrink: 0; }
.risk-title { font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 4px; }
.risk-desc  { font-size: 0.88rem; color: rgba(255,255,255,0.85); line-height: 1.5; }
.risk-pct   { margin-left: auto; font-size: 2.8rem; font-weight: 800; color: white; flex-shrink: 0; }

.prob-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    height: 14px;
    margin: 0.8rem 0 1.4rem;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 50px;
    position: relative;
}
.prob-bar-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}
@keyframes shimmer {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.rf-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 1rem 0;
}
.rf-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 10px;
    text-align: center;
}
.rf-label  { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; color: #95a5a6; margin-bottom: 6px; }
.rf-value  { font-size: 1.1rem; font-weight: 700; margin-bottom: 4px; }
.rf-status { font-size: 0.62rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; display: inline-block; }

.c-ok   { color: #2ecc71; } .b-ok   { background: rgba(46,204,113,0.15);  color: #2ecc71; }
.c-warn { color: #f39c12; } .b-warn { background: rgba(243,156,18,0.15);   color: #f39c12; }
.c-bad  { color: #e74c3c; } .b-bad  { background: rgba(231,76,60,0.15);    color: #e74c3c; }

.sec-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e74c3c;
    margin: 1.2rem 0 0.6rem;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.sec-title-blue {
    font-size: 1rem;
    font-weight: 700;
    color: #2980b9;
    margin: 1.2rem 0 0.6rem;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
</style>
"""


def rf_card(label, value, unit, color_cls, badge_cls, status_text):
    return f"""<div class="rf-card">
        <div class="rf-label">{label}</div>
        <div class="rf-value {color_cls}">{value}<small style="font-size:0.65rem"> {unit}</small></div>
        <span class="rf-status {badge_cls}">{status_text}</span>
    </div>"""


def show_heart_prediction(heart_bundle):

    if isinstance(heart_bundle, dict):
        heart_model = heart_bundle["model"]
        scaler      = heart_bundle["scaler"]
    else:
        heart_model = heart_bundle
        scaler      = None

    st.subheader("❤️ Heart Disease Prediction")
    st.markdown(ALERT_CSS + RESULT_CSS, unsafe_allow_html=True)
    
# ============================================================
# HEART.PY — REFERENCE RANGES, STATUS LOGIC, ANALYSIS, CHARTS, RECOMMENDATIONS
# ============================================================    
    st.markdown("""
<div style="background:rgba(41,128,185,0.08);border:1px solid rgba(41,128,185,0.2);
border-radius:12px;padding:14px 18px;margin-bottom:1rem;font-size:0.8rem;">
<div style="color:#3498db;font-weight:700;margin-bottom:10px;">📋 Reference Ranges</div>
<div style="display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:6px 10px;">
  <div style="color:#7f8c8d;font-size:0.68rem;font-weight:700;text-transform:uppercase;">Parameter</div>
  <div style="color:#2ecc71;font-size:0.68rem;font-weight:700;text-transform:uppercase;">✅ Normal</div>
  <div style="color:#e74c3c;font-size:0.68rem;font-weight:700;text-transform:uppercase;">🚨 Critical</div>
  <div style="color:#95a5a6;">Resting BP</div><div style="color:#2ecc71;font-weight:600;">90 – 120 mmHg</div><div style="color:#e74c3c;font-weight:600;">&gt;160 mmHg</div>
  <div style="color:#95a5a6;">Cholesterol</div><div style="color:#2ecc71;font-weight:600;">&lt;200 mg/dL</div><div style="color:#e74c3c;font-weight:600;">&gt;240 mg/dL</div>
  <div style="color:#95a5a6;">Max Heart Rate</div><div style="color:#2ecc71;font-weight:600;">220 – Age</div><div style="color:#e74c3c;font-weight:600;">Far below limit</div>
  <div style="color:#95a5a6;">Oldpeak</div><div style="color:#2ecc71;font-weight:600;">0.0 – 1.0</div><div style="color:#e74c3c;font-weight:600;">&gt;3.0</div>
  <div style="color:#95a5a6;">Fasting BS</div><div style="color:#2ecc71;font-weight:600;">&lt;120 = No</div><div style="color:#e74c3c;font-weight:600;">Yes = Risk</div>
  <div style="color:#95a5a6;">CA (Vessels)</div><div style="color:#2ecc71;font-weight:600;">0 = Normal</div><div style="color:#e74c3c;font-weight:600;">3 = Severe</div>
</div></div>
""", unsafe_allow_html=True)
# ============================================================
# HEART.PY REFERENCE RANGES, STATUS LOGIC, ANALYSIS, CHARTS, RECOMMENDATIONS
# ============================================================  
    
    col1, col2 = st.columns(2)

    with col1:
        age      = st.number_input("Age (years)", 1, 120)
        sex      = st.selectbox("Sex", ["Female", "Male"])
        cp       = st.selectbox("Chest Pain Type", [0,1,2,3],
                                format_func=lambda x: {
                                    0:"0 – Typical Angina",
                                    1:"1 – Atypical Angina",
                                    2:"2 – Non-Anginal Pain",
                                    3:"3 – Asymptomatic (Higher Risk)"
                                }[x])
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200,
                                   help="Normal: 90–120 mm Hg")
        chol     = st.number_input("Cholesterol (mg/dL)", 100, 600,
                                   help="Normal: <200 mg/dL")
        fbs      = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No","Yes"])
        restecg  = st.selectbox("Resting ECG Result", [0,1,2],
                                format_func=lambda x: {
                                    0:"0 – Normal",
                                    1:"1 – ST-T Wave Abnormality",
                                    2:"2 – Left Ventricular Hypertrophy"
                                }[x])

    with col2:
        thalach  = st.number_input("Max Heart Rate Achieved", 60, 220,
                                   help="Normal max ≈ 220 – Age")
        exang    = st.selectbox("Exercise Induced Angina", ["No","Yes"])
        oldpeak  = st.number_input("Oldpeak (ST Depression)", 0.0, 6.0,
                                   help="ST depression induced by exercise")
        slope    = st.selectbox("Slope of Peak Exercise ST Segment", [0,1,2],
                                format_func=lambda x: {
                                    0:"0 – Upsloping",
                                    1:"1 – Flat",
                                    2:"2 – Downsloping"
                                }[x])
        ca       = st.selectbox("Number of Major Vessels (0–3)", [0,1,2,3])
        thal     = st.selectbox("Thalassemia", [0,1,2,3],
                                format_func=lambda x: {
                                    0:"0 – Normal",
                                    1:"1 – Fixed Defect",
                                    2:"2 – Reversible Defect",
                                    3:"3 – Unknown"
                                }[x])

    if st.button("🤖 Predict Heart Disease Risk", use_container_width="True"):

        sex_val   = 1 if sex == "Male" else 0
        fbs_val   = 1 if fbs == "Yes" else 0
        exang_val = 1 if exang == "Yes" else 0

        input_data = pd.DataFrame(
            [[age, sex_val, cp, trestbps, chol, fbs_val, restecg,
              thalach, exang_val, oldpeak, slope, ca, thal]],
            columns=['age','sex','cp','trestbps','chol','fbs','restecg',
                     'thalach','exang','oldpeak','slope','ca','thal']
        )

        if scaler is not None:
            input_data = scaler.transform(input_data)

        probability = heart_model.predict_proba(input_data)[0][1] * 100

        # ---- Severity config ----
        if probability >= 80:
            severity  = "Severe"
            cls       = "severe"
            icon      = "🚨"
            bar_color = "linear-gradient(90deg, #c0392b, #e74c3c)"
            title     = "Severe Heart Disease Risk"
            desc      = "High cardiac risk detected. Immediate cardiology evaluation is strongly recommended. Do not ignore any chest symptoms."
        elif probability >= 60:
            severity  = "Moderate"
            cls       = "moderate"
            icon      = "⚠️"
            bar_color = "linear-gradient(90deg, #d35400, #e67e22)"
            title     = "Moderate Heart Disease Risk"
            desc      = "Moderate cardiac risk observed. Lifestyle correction and medical consultation are urgently advised."
        elif probability >= 40:
            severity  = "Mild"
            cls       = "mild"
            icon      = "🟡"
            bar_color = "linear-gradient(90deg, #b7950b, #f1c40f)"
            title     = "Mild Heart Disease Risk"
            desc      = "Early cardiac risk indicators detected. Preventive steps now can prevent future disease."
        else:
            severity  = "Low"
            cls       = "low"
            icon      = "✅"
            bar_color = "linear-gradient(90deg, #1e8449, #2ecc71)"
            title     = "Low Heart Disease Risk"
            desc      = "Low cardiac risk profile. Maintain heart-healthy habits and get annual check-ups."

        st.session_state.history.append({
            "Type": "Heart Disease",
            "Probability": probability,
            "Severity": severity
        })

        # ---- Risk Banner ----
        st.markdown(f"""
        <div class="risk-banner {cls}">
            <span class="risk-icon">{icon}</span>
            <div>
                <div class="risk-title">{title}</div>
                <div class="risk-desc">{desc}</div>
            </div>
            <div class="risk-pct">{probability:.1f}%</div>
        </div>
        <div class="prob-bar-wrap">
            <div class="prob-bar-fill" style="width:{probability}%; background:{bar_color}"></div>
        </div>
        """, unsafe_allow_html=True)

        # ---- Gauge + Risk Factor Cards ----
        col_g, col_f = st.columns([1, 1])

        with col_g:
            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=probability,
                number={'suffix': "%", 'font': {'size': 36}},
                delta={'reference': 40, 'increasing': {'color': "#e74c3c"}, 'decreasing': {'color': "#2ecc71"}},
                title={'text': "Cardiac Risk Level", 'font': {'size': 14}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#e74c3c" if probability >= 60 else "#f39c12" if probability >= 40 else "#2ecc71"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 40],   'color': "rgba(46,204,113,0.15)"},
                        {'range': [40, 60],  'color': "rgba(241,196,15,0.15)"},
                        {'range': [60, 80],  'color': "rgba(230,126,34,0.15)"},
                        {'range': [80, 100], 'color': "rgba(231,76,60,0.15)"},
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 3},
                        'thickness': 0.75,
                        'value': probability
                    }
                }
            ))
            fig.update_layout(
                template="plotly_dark",
                height=280,
                margin=dict(t=40, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, width="stretch")

            # Heart Rate vs Max HR comparison bar chart
            fig2 = go.Figure()
            max_hr_normal = 220 - age
            fig2.add_trace(go.Bar(
                x=["Resting BP", "Cholesterol", "Max HR Achieved"],
                y=[trestbps, chol / 3, thalach],
                name="Your Values",
                marker_color=["#e74c3c" if trestbps > 140 else "#2ecc71",
                               "#e74c3c" if chol > 200 else "#2ecc71",
                               "#f39c12" if thalach > max_hr_normal * 0.9 else "#2ecc71"]
            ))
            fig2.add_trace(go.Bar(
                x=["Resting BP", "Cholesterol", "Max HR Achieved"],
                y=[120, 200 / 3, max_hr_normal],
                name="Normal Range",
                marker_color="rgba(255,255,255,0.15)"
            ))
            fig2.update_layout(
                template="plotly_dark",
                barmode="group",
                height=200,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(font=dict(size=10)),
                showlegend=True
            )
            st.plotly_chart(fig2, width="stretch")

        with col_f:
            # Risk Factor Cards
            def bp_st(v):
                if v >= 160: return "c-bad","b-bad","High"
                if v >= 130: return "c-warn","b-warn","Elevated"
                return "c-ok","b-ok","Normal"

            def chol_st(v):
                if v >= 240: return "c-bad","b-bad","High"
                if v >= 200: return "c-warn","b-warn","Borderline"
                return "c-ok","b-ok","Normal"

            def hr_st(v, a):
                max_hr = 220 - a
                if v > max_hr: return "c-bad","b-bad","Too High"
                if v > max_hr * 0.85: return "c-warn","b-warn","Elevated"
                return "c-ok","b-ok","Normal"

            def cp_st(v):
                if v == 3: return "c-bad","b-bad","Asymptomatic"
                if v in [1,2]: return "c-warn","b-warn","Atypical"
                return "c-ok","b-ok","Typical"

            def age_st(v):
                if v > 65: return "c-bad","b-bad","High Risk"
                if v > 45: return "c-warn","b-warn","Moderate"
                return "c-ok","b-ok","Low Risk"

            def exang_st(v):
                if v == "Yes": return "c-bad","b-bad","Positive"
                return "c-ok","b-ok","Negative"

            bpc, bpc2, bps = bp_st(trestbps)
            cc, cc2, cs    = chol_st(chol)
            hc, hc2, hs    = hr_st(thalach, age)
            cpc, cpc2, cps = cp_st(cp)
            ac, ac2, as_   = age_st(age)
            ec, ec2, es    = exang_st(exang)

            st.markdown(f"""
            <div class="sec-title">🔬 Risk Factor Breakdown</div>
            <div class="rf-grid">
                {rf_card("Blood Pressure", trestbps, "mmHg", bpc, bpc2, bps)}
                {rf_card("Cholesterol", chol, "mg/dL", cc, cc2, cs)}
                {rf_card("Max Heart Rate", thalach, "bpm", hc, hc2, hs)}
                {rf_card("Chest Pain", cp, "type", cpc, cpc2, cps)}
                {rf_card("Age", age, "yrs", ac, ac2, as_)}
                {rf_card("Exercise Angina", "", "", ec, ec2, es)}
            </div>
            """, unsafe_allow_html=True)

            # Clinical notes based on inputs
            st.markdown('<div class="sec-title">🩺 Clinical Notes</div>', unsafe_allow_html=True)
            notes = []
            if chol > 200:   notes.append(shms_alert("warn", f"Cholesterol {chol} mg/dL is elevated — increases arterial plaque risk."))
            if trestbps > 140: notes.append(shms_alert("warn", f"BP {trestbps} mmHg is high — strains the heart muscle."))
            if cp == 3:      notes.append(shms_alert("crit", "Asymptomatic chest pain type — highest cardiac risk indicator."))
            if exang == "Yes": notes.append(shms_alert("warn", "Exercise-induced angina detected — significant cardiac signal."))
            if age > 55:     notes.append(shms_alert("warn", f"Age {age} increases cardiovascular vulnerability significantly."))
            if not notes:    notes.append(shms_alert("ok", "No critical individual risk factors detected. Overall profile looks healthy."))
            st.markdown("".join(notes), unsafe_allow_html=True)

        # ---- Recommendations ----
        st.markdown('<div class="sec-title-blue">💡 Recommendations & Prevention</div>', unsafe_allow_html=True)

        recs = []
        if probability >= 60:
            recs.append("🥗 Eat oats/multigrain breakfast, boiled vegetables, green salads, and omega-3 sources (fish/walnuts) daily.")
        else:
            recs.append("🥗 Maintain balanced home-cooked meals with seasonal fruits and vegetables.")
        if chol > 200:
            recs.append("🌾 Increase fiber — oats and beans lower cholesterol. Add flax seeds daily.")
            recs.append("❌ Avoid fried food and red meat — these raise LDL cholesterol significantly.")
        if trestbps > 140:
            recs.append("❌ Limit salt and processed food — sodium directly raises blood pressure.")
        if severity == "Severe":
            recs.append("🏃 Light walking ONLY under strict doctor supervision. Avoid all strenuous activity.")
        elif severity == "Moderate":
            recs.append("🏃 30 minutes brisk walking daily. Gradually increase under medical guidance.")
        else:
            recs.append("🏃 20–30 min daily activity. Yoga and meditation help maintain cardiac health.")
        recs.append("🧘 Manage stress actively — chronic stress is a major silent cardiac risk factor.")
        if severity == "Severe":
            recs.append("📊 Monitor BP daily. Lipid profile every 3 months. Consult cardiologist immediately.")
        elif severity == "Moderate":
            recs.append("📊 Monitor BP twice weekly. Lipid profile every 6 months.")
        else:
            recs.append("📊 Annual cardiac screening is recommended at your current risk level.")
        if cp == 3 or severity == "Severe":
            recs.append("🚨 Seek IMMEDIATE help if: chest pain/tightness, sudden breathlessness, dizziness, or fainting.")


        st.markdown("".join(rec_item(r) for r in recs), unsafe_allow_html=True)
