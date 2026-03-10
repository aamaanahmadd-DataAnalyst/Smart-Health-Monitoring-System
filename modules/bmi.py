import streamlit as st
import plotly.graph_objects as go
from modules.vital import ALERT_CSS, shms_alert, rec_item


def show_bmi_calculator():

    st.subheader("⚖️ Body Mass Index Calculator")
    st.markdown(ALERT_CSS, unsafe_allow_html=True)
    
 #REFERENCE: BMI Categories Alert Box CSS   
    st.markdown("""
<div style="background:rgba(41,128,185,0.08);border:1px solid rgba(41,128,185,0.2);
border-radius:12px;padding:14px 18px;margin-bottom:1rem;font-size:0.8rem;">
<div style="color:#3498db;font-weight:700;margin-bottom:10px;">📋 BMI Categories</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
  <div style="color:#95a5a6;">Underweight</div>  <div style="color:#3498db;font-weight:600;">&lt; 18.5</div>
  <div style="color:#95a5a6;">Normal</div>        <div style="color:#2ecc71;font-weight:600;">18.5 – 24.9</div>
  <div style="color:#95a5a6;">Overweight</div>    <div style="color:#f39c12;font-weight:600;">25.0 – 29.9</div>
  <div style="color:#95a5a6;">Obese</div>         <div style="color:#e74c3c;font-weight:600;">&gt; 30.0</div>
</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        height_cm = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
    with col2:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

    if st.button("📊 Calculate BMI", width="stretch"):

        bmi = round(weight / ((height_cm / 100) ** 2), 2)

        if bmi < 18.5:
            category  = "Underweight"
            alert_lvl = "warn"
            alert_msg = f"BMI {bmi} — Underweight. Nutritional support and structured weight gain plan recommended."
            bar_color = "#3498db"
        elif bmi < 25:
            category  = "Normal Weight"
            alert_lvl = "ok"
            alert_msg = f"BMI {bmi} — Normal Weight! Great job. Keep maintaining your healthy lifestyle."
            bar_color = "#2ecc71"
        elif bmi < 30:
            category  = "Overweight"
            alert_lvl = "warn"
            alert_msg = f"BMI {bmi} — Overweight. Reducing body fat lowers your future diabetes and heart risk significantly."
            bar_color = "#f39c12"
        else:
            category  = "Obese"
            alert_lvl = "crit"
            alert_msg = f"BMI {bmi} — Obese. This significantly increases risk of diabetes, hypertension, and heart disease. Structured intervention strongly recommended."
            bar_color = "#e74c3c"

        # ---- Alert Box ----
        st.markdown(shms_alert(alert_lvl, alert_msg), unsafe_allow_html=True)

        # ---- Gauge ----
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            number={'suffix': " BMI"},
            title={'text': f"BMI Category: {category}"},
            gauge={
                'axis': {'range': [0, 40]},
                'bar': {'color': bar_color},
                'steps': [
                    {'range': [0, 18.5], 'color': "rgba(52,152,219,0.2)"},
                    {'range': [18.5, 25],'color': "rgba(46,204,113,0.2)"},
                    {'range': [25, 30],  'color': "rgba(241,196,15,0.2)"},
                    {'range': [30, 40],  'color': "rgba(231,76,60,0.2)"}
                ]
            }
        ))
        fig.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig, width="stretch")

        # ---- Recommendations ----
        st.subheader("💡 Recommendations")

        recs = []

        if category == "Underweight":
            recs.append("🥗 Eat high-protein foods (eggs, paneer, dal) and healthy fats (peanut butter, nuts). Have 4–5 small meals per day.")
            recs.append("🥛 Include milk and dairy products daily for calcium and protein.")
            recs.append("❌ Avoid skipping meals — consistency is key for healthy weight gain.")
            recs.append("🏋️ Light strength training 3–4 times/week. Avoid excessive cardio.")
            recs.append("📊 Track weight weekly. Consider consulting a dietitian for a structured plan.")

        elif category == "Normal Weight":
            recs.append("🥗 Maintain a balanced diet — whole grains, seasonal fruits & vegetables, and adequate protein.")
            recs.append("🏃 30 minutes of daily activity — light cardio or sports plus strength training 2x/week.")
            recs.append("💧 Stay hydrated — 8–10 glasses of water daily.")
            recs.append("😴 Maintain 7–8 hours of quality sleep for metabolic balance.")

        elif category == "Overweight":
            recs.append("🥗 Switch to calorie-controlled meals with high-fiber foods — oats, vegetables, lean protein.")
            recs.append("❌ Limit fried food, sugary beverages, and late-night eating.")
            recs.append("🏃 40 minutes of brisk walking daily plus strength training 3x/week.")
            recs.append("📊 Track weight every 2 weeks. Target 0.5–1 kg weight loss per month safely.")

        else:  # Obese
            recs.append("🥗 Follow a strict low-calorie structured diet. Avoid refined carbs completely. Increase protein and fiber.")
            recs.append("❌ Strictly avoid fast food, sugary snacks, and sedentary lifestyle.")
            recs.append("🏃 Start with 30 min walking daily, gradually increase intensity under fitness guidance.")
            recs.append("📊 Weekly weight tracking. Consult a physician for a structured weight management plan.")
            recs.append("🚨 Seek immediate attention if you experience breathlessness, joint pain, or fatigue during mild activity.")

        st.markdown("".join(rec_item(r) for r in recs), unsafe_allow_html=True)