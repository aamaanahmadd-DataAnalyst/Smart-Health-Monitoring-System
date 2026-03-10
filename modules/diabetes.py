import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from modules.vital import ALERT_CSS, shms_alert, rec_item

RESULT_CSS = """
<style>
/* ---- Risk Level Banner ---- */
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

.risk-icon   { font-size: 3rem; flex-shrink: 0; }
.risk-title  { font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 4px; }
.risk-desc   { font-size: 0.88rem; color: rgba(255,255,255,0.85); line-height: 1.5; }
.risk-pct    { margin-left: auto; font-size: 2.8rem; font-weight: 800; color: white; flex-shrink: 0; }

/* ---- Progress Bar ---- */
.prob-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    height: 14px;
    margin: 0.8rem 0 1.4rem;
    overflow: hidden;
    position: relative;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 1.2s ease;
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

/* ---- Risk Factor Cards ---- */
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
.rf-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; color: #95a5a6; margin-bottom: 6px; }
.rf-value { font-size: 1.1rem; font-weight: 700; margin-bottom: 4px; }
.rf-status { font-size: 0.62rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; display: inline-block; }

.c-ok   { color: #2ecc71; } .b-ok   { background: rgba(46,204,113,0.15);  color: #2ecc71; }
.c-warn { color: #f39c12; } .b-warn { background: rgba(243,156,18,0.15);   color: #f39c12; }
.c-bad  { color: #e74c3c; } .b-bad  { background: rgba(231,76,60,0.15);    color: #e74c3c; }

/* ---- Section Title ---- */
.sec-title {
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


def show_diabetes_prediction(diabetes_bundle):

    if isinstance(diabetes_bundle, dict):
        diabetes_model = diabetes_bundle["model"]
        scaler         = diabetes_bundle["scaler"]
    else:
        diabetes_model = diabetes_bundle
        scaler         = None

    st.subheader("🩸 Diabetes Risk Prediction")
    st.markdown(ALERT_CSS + RESULT_CSS, unsafe_allow_html=True)
    st.warning("⚠️ This diabetes model is trained using the PIMA Indian Women dataset.")
    st.caption("Predictions for male patients may be less accurate.")

    st.markdown(ALERT_CSS + RESULT_CSS, unsafe_allow_html=True)
    

# ============================================================
# DIABETES.PY REFERENCE RANGES, STATUS LOGIC, ANALYSIS, CHARTS, RECOMMENDATIONS
# ============================================================

    st.markdown("""
<div style="background:rgba(41,128,185,0.08);border:1px solid rgba(41,128,185,0.2);
border-radius:12px;padding:14px 18px;margin-bottom:1rem;font-size:0.8rem;">
<div style="color:#3498db;font-weight:700;margin-bottom:10px;">📋 Reference Ranges</div>
<div style="display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:6px 10px;">
  <div style="color:#7f8c8d;font-size:0.68rem;font-weight:700;text-transform:uppercase;">Parameter</div>
  <div style="color:#2ecc71;font-size:0.68rem;font-weight:700;text-transform:uppercase;">✅ Normal</div>
  <div style="color:#e74c3c;font-size:0.68rem;font-weight:700;text-transform:uppercase;">🚨 Critical</div>
  <div style="color:#95a5a6;">Glucose</div><div style="color:#2ecc71;font-weight:600;">70 – 140 mg/dL</div><div style="color:#e74c3c;font-weight:600;">&gt;200 mg/dL</div>
  <div style="color:#95a5a6;">Blood Pressure</div><div style="color:#2ecc71;font-weight:600;">60 – 80 mmHg</div><div style="color:#e74c3c;font-weight:600;">&gt;90 mmHg</div>
  <div style="color:#95a5a6;">BMI</div><div style="color:#2ecc71;font-weight:600;">18.5 – 24.9</div><div style="color:#e74c3c;font-weight:600;">&gt;35</div>
  <div style="color:#95a5a6;">Insulin</div><div style="color:#2ecc71;font-weight:600;">16 – 166 μU/mL</div><div style="color:#e74c3c;font-weight:600;">&gt;300 μU/mL</div>
  <div style="color:#95a5a6;">Skin Thickness</div><div style="color:#2ecc71;font-weight:600;">10 – 40 mm</div><div style="color:#e74c3c;font-weight:600;">&gt;60 mm</div>
  <div style="color:#95a5a6;">DPF Score</div><div style="color:#2ecc71;font-weight:600;">0.0 – 0.5</div><div style="color:#e74c3c;font-weight:600;">&gt;1.5</div>
</div></div>
""", unsafe_allow_html=True)
    
#REFERENCE------

    col1, col2 = st.columns(2)

    with col1:
        preg    = st.number_input("Pregnancies (0–17)", 0, 20)
        glucose = st.number_input("Glucose Level (mg/dL)", 0, 300,
                                  help="Normal: 70–140 mg/dL")
        bp      = st.number_input("Blood Pressure (mm Hg)", 0, 200,
                                  help="Normal: 60–80 mm Hg")
        bmi     = st.number_input("BMI (kg/m²)", 0.0, 70.0,
                                  help="Normal: 18.5–24.9")
    with col2:
        insulin = st.number_input("Insulin (μU/mL)", 0, 900,
                                  help="Normal: 16–166 μU/mL")
        age     = st.number_input("Age (years)", 1, 120)
        dpf     = st.number_input("Diabetes Pedigree Function", 0.0, 3.0,
                                  help="Genetic risk score. Range: 0.0–2.5")
        skin    = st.number_input("Skin Thickness (mm)", 0, 100,
                                  help="Normal: 10–40 mm")

    if st.button("🤖 Predict Diabetes Risk"):

        if glucose == 0:
            st.warning("Glucose value cannot be zero.")
            st.stop()
        if bmi == 0:
            st.warning("BMI cannot be zero.")
            st.stop()

        input_data = pd.DataFrame(
            [[preg, glucose, bp, skin, insulin, bmi, dpf, age]],
            columns=['Pregnancies','Glucose','BloodPressure','SkinThickness',
                     'Insulin','BMI','DiabetesPedigreeFunction','Age']
        )

        if scaler is not None:
            input_data = scaler.transform(input_data)

        probability = diabetes_model.predict_proba(input_data)[0][1] * 100

        # ---- Severity config ----
        if probability >= 80:
            severity   = "Severe"
            cls        = "severe"
            icon       = "🚨"
            bar_color  = "linear-gradient(90deg, #c0392b, #e74c3c)"
            title      = "Severe Diabetes Risk"
            desc       = "High diabetes probability detected. Immediate consultation with a diabetologist is strongly recommended. Do not delay."
        elif probability >= 60:
            severity   = "Moderate"
            cls        = "moderate"
            icon       = "⚠️"
            bar_color  = "linear-gradient(90deg, #d35400, #e67e22)"
            title      = "Moderate Diabetes Risk"
            desc       = "Moderate risk observed. Significant lifestyle correction and medical consultation are advised."
        elif probability >= 40:
            severity   = "Mild"
            cls        = "mild"
            icon       = "🟡"
            bar_color  = "linear-gradient(90deg, #b7950b, #f1c40f)"
            title      = "Mild Diabetes Risk"
            desc       = "Early risk stage detected. Preventive measures now can significantly reduce future risk."
        else:
            severity   = "Low"
            cls        = "low"
            icon       = "✅"
            bar_color  = "linear-gradient(90deg, #1e8449, #2ecc71)"
            title      = "Low Diabetes Risk"
            desc       = "Low risk profile. Maintain your healthy habits and get annual screening."

        st.session_state.history.append({
            "Type": "Diabetes",
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

        # ---- Gauge + Risk Factors ----
        col_g, col_f = st.columns([1, 1])

        with col_g:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=probability,
                number={'suffix': "%", 'font': {'size': 36}},
                delta={'reference': 40, 'increasing': {'color': "#e74c3c"}, 'decreasing': {'color': "#2ecc71"}},
                title={'text': "Risk Probability", 'font': {'size': 14}},
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

        with col_f:
            # Risk factor breakdown cards
            def gluc_st(v):
                if v > 200: return "c-bad","b-bad","Critical"
                if v > 140: return "c-warn","b-warn","Elevated"
                return "c-ok","b-ok","Normal"

            def bmi_st(v):
                if v >= 30: return "c-bad","b-bad","Obese"
                if v >= 25: return "c-warn","b-warn","Overweight"
                return "c-ok","b-ok","Normal"

            def bp_st(v):
                if v >= 90: return "c-bad","b-bad","High"
                if v >= 80: return "c-warn","b-warn","Elevated"
                return "c-ok","b-ok","Normal"

            def ins_st(v):
                if v > 166: return "c-bad","b-bad","High"
                if v < 16 and v > 0: return "c-warn","b-warn","Low"
                return "c-ok","b-ok","Normal"

            def dpf_st(v):
                if v > 1.5: return "c-bad","b-bad","High Risk"
                if v > 0.8: return "c-warn","b-warn","Moderate"
                return "c-ok","b-ok","Low"

            def age_st(v):
                if v > 55: return "c-bad","b-bad","High Risk Age"
                if v > 40: return "c-warn","b-warn","Moderate"
                return "c-ok","b-ok","Low Risk"

            gc, bc, ic = gluc_st(glucose)
            bmc, bmc2, bms = bmi_st(bmi)
            bpc, bpc2, bps2 = bp_st(bp)
            ic2, ic3, ins_s = ins_st(insulin)
            dc, dc2, ds = dpf_st(dpf)
            ac, ac2, as2 = age_st(age)

            st.markdown(f"""
            <div class="sec-title">🔬 Risk Factor Breakdown</div>
            <div class="rf-grid">
                {rf_card("Glucose", glucose, "mg/dL", gc, bc, gluc_st(glucose)[2])}
                {rf_card("BMI", bmi, "kg/m²", bmc, bmc2, bms)}
                {rf_card("Blood Pressure", bp, "mmHg", bpc, bpc2, bps2)}
                {rf_card("Insulin", insulin, "μU/mL", ic2, ic3, ins_s)}
                {rf_card("Pedigree", dpf, "", dc, dc2, ds)}
                {rf_card("Age", age, "yrs", ac, ac2, as2)}
            </div>
            """, unsafe_allow_html=True)

        # ---- Recommendations ----
        st.markdown('<div class="sec-title">💡 Recommendations & Prevention</div>', unsafe_allow_html=True)

        recs = []
        if probability >= 60:
            recs.append("🥗 Eat multigrain roti/brown rice (controlled portion), green leafy vegetables, sprouts, dal, and chana daily.")
        else:
            recs.append("🥗 Maintain balanced home-cooked meals with whole grains instead of refined flour.")
        if glucose > 140:
            recs.append("🌾 Increase fiber — oats, flax seeds, and salad before meals help control glucose spikes.")
        if probability >= 60 or glucose > 140:
            recs.append("❌ Avoid sugary drinks, sweets, white bread, and maida products completely.")
        if bmi > 25:
            recs.append("❌ Limit fried food and fast food — excess body fat increases insulin resistance.")
        if bmi > 30:
            recs.append("🏃 Walk briskly for 45 minutes daily — exercise is the most effective way to reduce diabetes risk.")
        elif bmi > 25:
            recs.append("🏃 30–40 minutes of walking or light exercise daily is recommended.")
        else:
            recs.append("🏃 20–30 min daily physical activity maintains healthy blood sugar levels.")
        recs.append("😴 Sleep before 11 PM and manage stress — both directly affect blood glucose levels.")
        if severity == "Severe":
            recs.append("📊 Monitor fasting glucose 2–3x/week. Get HbA1c every 3 months. Consult diabetologist immediately.")
        elif severity == "Moderate":
            recs.append("📊 Weekly glucose monitoring recommended. Consult a doctor soon.")
        elif severity == "Mild":
            recs.append("📊 Monthly glucose check advised.")
        else:
            recs.append("📊 Annual diabetes screening is sufficient at current risk level.")
        if glucose > 200:
            recs.append("🚨 Seek medical help if you experience: excessive thirst, blurry vision, or extreme fatigue.")


        st.markdown("".join(rec_item(r) for r in recs), unsafe_allow_html=True)
