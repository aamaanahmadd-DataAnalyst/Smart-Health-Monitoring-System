import streamlit as st
import plotly.graph_objects as go


def show_bmi_calculator():

    st.subheader("⚖️ Body Mass Index Calculator")

    col1, col2 = st.columns(2)

    with col1:
        height_cm = st.number_input("Height (cm)", 100.0, 250.0, 170.0)

    with col2:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

    if st.button("Calculate BMI"):

        bmi = round(weight / ((height_cm/100)**2), 2)

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            number={'suffix': " BMI"},
            gauge={
                'axis': {'range': [0, 40]},
                'steps': [
                    {'range': [0, 18.5], 'color': "#3498db"},
                    {'range': [18.5, 25], 'color': "#2ecc71"},
                    {'range': [25, 30], 'color': "#f1c40f"},
                    {'range': [30, 40], 'color': "#e74c3c"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- CATEGORY ----------------
        if bmi < 18.5:
            category = "Underweight"
            st.info("🔵 Underweight")

        elif bmi < 25:
            category = "Normal"
            st.success("🟢 Normal Weight")

        elif bmi < 30:
            category = "Overweight"
            st.warning("🟡 Overweight")

        else:
            category = "Obese"
            st.error("🔴 Obese")

        # ---------------- HUMAN INTERPRETATION ----------------
        st.markdown("## ⚖️ Body Composition Interpretation")

        if category == "Underweight":
            st.write(
                f"Your BMI is {bmi}, which falls below the healthy range. "
                "Being underweight may indicate nutritional deficiency or muscle loss. "
                "A structured weight gain plan is recommended."
            )

            st.markdown("### 🥗 What You Should Eat")
            st.write("• High-protein foods (eggs, paneer, dal)")
            st.write("• Healthy fats (peanut butter, nuts)")
            st.write("• Milk & dairy products")
            st.write("• 4–5 small meals per day")

            st.markdown("### ❌ Avoid")
            st.write("• Skipping meals")
            st.write("• Excess junk food for weight gain")

            st.markdown("### 🏋️ Exercise Plan")
            st.write("• Light strength training 3–4 times/week")
            st.write("• Avoid excessive cardio")

            st.markdown("### 📊 Monitoring")
            st.write("• Track weight weekly")
            st.write("• Consider dietitian consultation")

        elif category == "Normal":
            st.write(
                f"Your BMI is {bmi}, which is within the healthy range. "
                "Maintaining consistency in diet and activity is important to sustain metabolic balance."
            )

            st.markdown("### 🥗 Maintain Balanced Diet")
            st.write("• Whole grains")
            st.write("• Seasonal fruits & vegetables")
            st.write("• Adequate protein intake")

            st.markdown("### 🏃 Stay Active")
            st.write("• 30 minutes daily activity")
            st.write("• Light cardio or sports")
            st.write("• Strength training 2x/week")

        elif category == "Overweight":
            st.write(
                f"Your BMI is {bmi}, indicating excess body weight. "
                "Reducing body fat can significantly lower your future diabetes and heart risk."
            )

            st.markdown("### 🥗 Recommended Diet")
            st.write("• Calorie-controlled meals")
            st.write("• High-fiber foods (oats, vegetables)")
            st.write("• Lean protein sources")

            st.markdown("### ❌ Limit")
            st.write("• Fried food")
            st.write("• Sugary beverages")
            st.write("• Late-night eating")

            st.markdown("### 🏃 Exercise Plan")
            st.write("• 40 minutes brisk walking daily")
            st.write("• Strength training 3x/week")

            st.markdown("### 📊 Monitoring")
            st.write("• Track weight every 2 weeks")
            st.write("• Aim 0.5–1 kg weight loss per month")

        else:  # Obese
                st.write(
                    f"Your BMI is {bmi}, which falls in the obesity range. "
                    "This significantly increases the risk of diabetes, hypertension, and heart disease. "
                    "Structured intervention is strongly recommended."
                )
    
                st.markdown("### 🥗 Strict Dietary Plan")
                st.write("• Low-calorie structured diet")
                st.write("• Avoid refined carbs completely")
                st.write("• Increase protein & fiber intake")
    
                st.markdown("### ❌ Strictly Avoid")
                st.write("• Fast food")
                st.write("• Sugary snacks")
                st.write("• Sedentary lifestyle")
    
                st.markdown("### 🏃 Physical Activity")
                st.write("• Start with 30 min walking daily")
                st.write("• Gradually increase intensity")
                st.write("• Seek fitness trainer guidance")
    
                st.markdown("### 📊 Monitoring")
                st.write("• Weekly weight tracking")
                st.write("• Consult physician for structured plan")
    
                st.markdown("### 🚨 Immediate Attention If")
                st.write("• Breathlessness")
                st.write("• Joint pain")
                st.write("• Fatigue during mild activity")
