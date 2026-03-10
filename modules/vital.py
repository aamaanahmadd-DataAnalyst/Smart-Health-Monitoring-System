import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ---- Shared alert CSS ----
ALERT_CSS = """
<style>
.vital-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 1.2rem;
}
.vital-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 10px;
    text-align: center;
    backdrop-filter: blur(10px);
}
.vital-name {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #95a5a6;
    margin-bottom: 8px;
    font-weight: 600;
}
.vital-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
}
.vital-unit {
    font-size: 0.75rem;
    font-weight: 400;
}
.vital-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-normal   { background: rgba(46,204,113,0.2);  color: #2ecc71; }
.badge-warning  { background: rgba(243,156,18,0.2);   color: #f39c12; }
.badge-danger   { background: rgba(231,76,60,0.2);    color: #e74c3c; }
.color-normal   { color: #2ecc71; }
.color-warning  { color: #f39c12; }
.color-danger   { color: #e74c3c; }

.shms-alert {
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    font-size: 0.95rem;
    font-weight: 500;
    line-height: 1.5;
    margin: 1rem 0;
}
.alert-ok   { background: rgba(46,204,113,0.1);  border: 1px solid rgba(46,204,113,0.35);  color: #2ecc71; }
.alert-warn { background: rgba(243,156,18,0.1);   border: 1px solid rgba(243,156,18,0.35);   color: #f39c12; }
.alert-crit { background: rgba(231,76,60,0.1);    border: 1px solid rgba(231,76,60,0.35);    color: #e74c3c; }
.alert-icon { font-size: 1.5rem; flex-shrink: 0; }

.rec-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #2980b9;
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #bdc3c7;
    line-height: 1.5;
}
</style>
"""


def vital_card(name, value, unit, status, label):
    color_cls = f"color-{status}"
    badge_cls = f"badge-{status}"
    return f"""
    <div class="vital-card">
        <div class="vital-name">{name}</div>
        <div class="vital-value {color_cls}">{value}<span class="vital-unit"> {unit}</span></div>
        <span class="vital-badge {badge_cls}">{label}</span>
    </div>"""


def shms_alert(level, message):
    icons = {"ok": "✅", "warn": "⚠️", "crit": "🚨"}
    return f"""
    <div class="shms-alert alert-{level}">
        <span class="alert-icon">{icons[level]}</span>
        <span>{message}</span>
    </div>"""


def rec_item(text):
    return f'<div class="rec-item">{text}</div>'


def show_vital():

    st.subheader("🩺 Vital Signs Check & Analysis")
    st.markdown(ALERT_CSS, unsafe_allow_html=True)

# ============================================================
# VITAL.PY — REFERENCE RANGES, STATUS LOGIC, ANALYSIS, CHARTS, RECOMMENDATIONS
# ============================================================

    st.markdown("""
<div style="background:rgba(41,128,185,0.08);border:1px solid rgba(41,128,185,0.2);
border-radius:12px;padding:14px 18px;margin-bottom:1rem;font-size:0.8rem;">
<div style="color:#3498db;font-weight:700;margin-bottom:10px;">📋 Reference Ranges</div>
<div style="display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:6px 10px;">
  <div style="color:#7f8c8d;font-size:0.68rem;font-weight:700;text-transform:uppercase;">Parameter</div>
  <div style="color:#2ecc71;font-size:0.68rem;font-weight:700;text-transform:uppercase;">✅ Normal</div>
  <div style="color:#e74c3c;font-size:0.68rem;font-weight:700;text-transform:uppercase;">🚨 Critical</div>
  <div style="color:#95a5a6;">Heart Rate</div><div style="color:#2ecc71;font-weight:600;">60 – 100 bpm</div><div style="color:#e74c3c;font-weight:600;">&gt;120 / &lt;40</div>
  <div style="color:#95a5a6;">Temperature</div><div style="color:#2ecc71;font-weight:600;">97 – 99 °F</div><div style="color:#e74c3c;font-weight:600;">&gt;103 °F</div>
  <div style="color:#95a5a6;">Systolic BP</div><div style="color:#2ecc71;font-weight:600;">90 – 120 mmHg</div><div style="color:#e74c3c;font-weight:600;">&gt;160 mmHg</div>
  <div style="color:#95a5a6;">Diastolic BP</div><div style="color:#2ecc71;font-weight:600;">60 – 80 mmHg</div><div style="color:#e74c3c;font-weight:600;">&gt;100 mmHg</div>
  <div style="color:#95a5a6;">SpO2</div><div style="color:#2ecc71;font-weight:600;">95 – 100 %</div><div style="color:#e74c3c;font-weight:600;">&lt;90 %</div>
  <div style="color:#95a5a6;">Resp. Rate</div><div style="color:#2ecc71;font-weight:600;">12 – 20 /min</div><div style="color:#e74c3c;font-weight:600;">&gt;25 /min</div>
</div></div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        heart_rate  = st.number_input("Heart Rate (bpm)", 20, 250, 75,
                                      help="Normal resting: 60–100 bpm")
        temperature = st.number_input("Body Temperature (°F)", 90.0, 110.0, 98.6,
                                      help="Normal: 97–99°F")
        systolic    = st.number_input("Systolic BP (mm Hg)", 70, 220, 120,
                                      help="Normal: 90–120 mm Hg")

    with col2:
        diastolic   = st.number_input("Diastolic BP (mm Hg)", 40, 140, 80,
                                      help="Normal: 60–80 mm Hg")
        oxygen      = st.number_input("Oxygen Saturation SpO2 (%)", 50, 100, 98,
                                      help="Normal: 95–100%")
        resp_rate   = st.number_input("Respiratory Rate (/min)", 5, 60, 16,
                                      help="Normal: 12–20 breaths/min")

    if st.button("🔍 Analyze Vitals", use_container_width=True):

        # ---- Status logic ----
        def hr_status(v):
            if v < 60:   return "warning", "Low (Bradycardia)"
            if v > 120:  return "danger",  "High (Tachycardia)"
            if v > 100:  return "warning", "Elevated"
            return "normal", "Normal"

        def temp_status(v):
            if v < 97:   return "warning", "Low"
            if v >= 103: return "danger",  "High Fever"
            if v >= 99.5: return "warning", "Mild Fever"
            return "normal", "Normal"

        def bps_status(v):
            if v < 90:   return "warning", "Low BP"
            if v >= 160: return "danger",  "High BP"
            if v >= 130: return "warning", "Elevated"
            return "normal", "Normal"

        def bpd_status(v):
            if v < 60:   return "warning", "Low"
            if v >= 100: return "danger",  "High"
            if v >= 85:  return "warning", "Elevated"
            return "normal", "Normal"

        def spo2_status(v):
            if v < 90:  return "danger",  "Critical"
            if v < 95:  return "warning", "Low"
            return "normal", "Normal"

        def rr_status(v):
            if v < 12:  return "warning", "Low (Bradypnea)"
            if v >= 25: return "danger",  "High (Tachypnea)"
            if v >= 20: return "warning", "Elevated"
            return "normal", "Normal"

        hr_st,   hr_lb   = hr_status(heart_rate)
        tmp_st,  tmp_lb  = temp_status(temperature)
        bps_st,  bps_lb  = bps_status(systolic)
        bpd_st,  bpd_lb  = bpd_status(diastolic)
        spo2_st, spo2_lb = spo2_status(oxygen)
        rr_st,   rr_lb   = rr_status(resp_rate)

        statuses = [hr_st, tmp_st, bps_st, bpd_st, spo2_st, rr_st]
        worst = "danger" if "danger" in statuses else "warning" if "warning" in statuses else "normal"

        # ---- Vital Cards Grid ----
        st.markdown(f"""
        <div class="vital-grid">
            {vital_card("HEART RATE",   heart_rate,   "bpm",  hr_st,   hr_lb)}
            {vital_card("TEMPERATURE",  temperature,  "°F",   tmp_st,  tmp_lb)}
            {vital_card("SYSTOLIC BP",  systolic,     "mmHg", bps_st,  bps_lb)}
            {vital_card("DIASTOLIC BP", diastolic,    "mmHg", bpd_st,  bpd_lb)}
            {vital_card("SPO2",         oxygen,       "%",    spo2_st, spo2_lb)}
            {vital_card("RESP. RATE",   resp_rate,    "/min", rr_st,   rr_lb)}
        </div>
        """, unsafe_allow_html=True)

        # ---- Main Alert ----
        if worst == "normal":
            alert_msg = "All vitals are within normal range. Keep maintaining a healthy lifestyle!"
            alert_lvl = "ok"
        elif worst == "warning":
            alert_msg = "One or more vitals need attention. Monitor closely and consult a doctor if symptoms persist."
            alert_lvl = "warn"
        else:
            alert_msg = "Critical readings detected! Seek immediate medical attention."
            alert_lvl = "crit"

        st.markdown(shms_alert(alert_lvl, alert_msg), unsafe_allow_html=True)

        # ---- Save to history ----
        score = 100
        if tmp_st  != "normal": score -= 20
        if bps_st  != "normal" or bpd_st != "normal": score -= 25
        if hr_st   != "normal": score -= 20
        if spo2_st != "normal": score -= 25
        score = max(score, 0)

        severity = "Low" if score > 75 else "Mild" if score > 50 else "Moderate"
        st.session_state.history.append({
            "Type": "Vital Signs",
            "Probability": float(100 - score),
            "Severity": severity
        })

        # ---- Charts ----
        st.markdown("---")
        st.subheader("📊 Visual Analysis")

        col_g, col_r = st.columns(2)

        with col_g:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Overall Health Score"},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2ecc71" if score > 75 else "#f1c40f" if score > 50 else "#e74c3c"},
                    'steps': [
                        {'range': [0, 50],   'color': "rgba(231,76,60,0.2)"},
                        {'range': [50, 75],  'color': "rgba(241,196,15,0.2)"},
                        {'range': [75, 100], 'color': "rgba(46,204,113,0.2)"}
                    ]
                }
            ))
            fig.update_layout(template="plotly_dark", height=280)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=[heart_rate, temperature, systolic, oxygen, resp_rate],
                theta=["Heart Rate", "Temperature", "Systolic BP", "SpO2", "Resp Rate"],
                fill='toself', name='Your Values', line_color='#3498db'
            ))
            fig2.add_trace(go.Scatterpolar(
                r=[75, 98.6, 120, 98, 16],
                theta=["Heart Rate", "Temperature", "Systolic BP", "SpO2", "Resp Rate"],
                fill='toself', name='Normal', line_color='#2ecc71', opacity=0.4
            ))
            fig2.update_layout(template="plotly_dark", showlegend=True, height=280)
            st.plotly_chart(fig2, use_container_width=True)

        # ---- Recommendations ----
        st.subheader("💡 Recommendations")

        recs = []
        if hr_st != "normal":
            recs.append("❤️ Heart rate abnormal — rest, avoid caffeine, and monitor closely.")
        if tmp_st == "danger":
            recs.append("🌡️ High fever detected — take antipyretics, stay hydrated, seek immediate medical attention.")
        elif tmp_st == "warning":
            recs.append("🌡️ Mild fever — rest, drink fluids, monitor temperature every 2 hours.")
        if bps_st == "danger" or bpd_st == "danger":
            recs.append("🩺 BP critically high — avoid salt and stress, consult a doctor immediately.")
        elif bps_st == "warning" or bpd_st == "warning":
            recs.append("🩺 BP slightly elevated — reduce sodium intake, exercise regularly.")
        if spo2_st == "danger":
            recs.append("💨 SpO2 critically low — seek emergency medical care immediately.")
        elif spo2_st == "warning":
            recs.append("💨 SpO2 low — practice deep breathing, consult a doctor.")
        if rr_st != "normal":
            recs.append("🫁 Respiratory rate abnormal — practice deep breathing, consult doctor if difficulty persists.")
        if not recs:
            recs.append("✅ All vitals normal — maintain balanced diet, exercise 30 min/day, sleep 7–8 hrs.")
            recs.append("💧 Stay hydrated — drink 8–10 glasses of water daily.")
            recs.append("🧘 Practice stress management — yoga or meditation helps maintain healthy vitals.")

        html_recs = "".join(rec_item(r) for r in recs)
        st.markdown(html_recs, unsafe_allow_html=True)