# 🩺 Smart Health Monitoring System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

> **AI-Powered Preventive Healthcare & Multi-Disease Risk Prediction Platform**  
> Integral University, Lucknow | B.Tech CSE 2025–26 | Project ID: PCS25/95

---

## 📌 Overview

The **Smart Health Monitoring System (SHMS)** is a web-based AI-powered application that helps users monitor their health vitals and predict the risk of chronic diseases like **Diabetes** and **Heart Disease** using trained Machine Learning models.

The system analyzes user-provided health parameters, classifies risk severity, and generates personalized clinical recommendations — all without storing any personal data, ensuring complete privacy.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🩺 **Vital Signs Check** | Analyze Heart Rate, BP, Temperature, SpO2, Respiratory Rate with color-coded alerts |
| ⚖️ **BMI Calculator** | Calculate Body Mass Index with health category and recommendations |
| 🩸 **Diabetes Prediction** | ML-based diabetes risk prediction with probability score and risk factor breakdown |
| ❤️ **Heart Disease Prediction** | ML-based cardiac risk prediction with clinical notes and visual analysis |
| 📊 **Health Analytics** | Dashboard with charts, prediction history, trend analysis and PDF report generation |
| ℹ️ **About** | Project info, tech stack, team members |

---

## 🤖 Machine Learning Models

| Model | Algorithm | Dataset | Accuracy |
|-------|-----------|---------|----------|
| Diabetes Prediction | Random Forest | Pima Indians Diabetes Dataset | 80%+ |
| Heart Disease Prediction | Logistic Regression | UCI Heart Disease Dataset | 80%+ |

**Severity Classification:**
- 🟢 **Low Risk** — 0% to 39%
- 🟡 **Mild Risk** — 40% to 59%
- 🟠 **Moderate Risk** — 60% to 79%
- 🔴 **Severe Risk** — 80% to 100%

---

## 🛠️ Tech Stack

```
Frontend        →  Streamlit, HTML, CSS, JavaScript
Visualization   →  Plotly (Gauge, Bar, Pie, Radar, Line Charts)
Machine Learning→  Scikit-learn (Random Forest, Logistic Regression)
PDF Generation  →  ReportLab
Animations      →  Lottie Files
Language        →  Python 3.x
```

---

## 📁 Project Structure

```
Smart_Health_Monitoring_System/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
│
├── modules/
│   ├── vital.py            # Vital Signs module
│   ├── bmi.py              # BMI Calculator module
│   ├── diabetes.py         # Diabetes Prediction module
│   ├── heart.py            # Heart Disease Prediction module
│   ├── analytics.py        # Analytics & PDF Report module
│   └── about.py            # About page module
│
├── models/
│   ├── diabetes_model.pkl  # Trained Diabetes ML model
│   └── heart_model.pkl     # Trained Heart Disease ML model
│
├── assets/
│   ├── style.css           # Custom CSS styling
│   └── health.json         # Lottie animation file
│
├── utils/
│   └── load_models.py      # Model loading utility
│
└── Team/
    ├── Amaan_A.jpg
    ├── Sharukh_S.jpeg
    └── Fuzail_K.jpeg
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/Smart-Health-Monitoring-System.git
cd Smart-Health-Monitoring-System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
plotly
reportlab
streamlit-lottie
matplotlib
seaborn
requests
```

---

## 👨‍💻 Team Members

| Name | Role |
|------|------|
| **Amaan Ahmad** | Machine Learning & Frontend Development |
| **Md. Sharukh** | Model Training & Backend Integration |
| **Mohd. Fuzail Khan** | Documentation & Research |

---

## 🏫 Project Details

- **University:** Integral University, Lucknow
- **Degree:** B.Tech Computer Science & Engineering
- **Year:** 2025–26
- **Project ID:** PCS25/95
- **Supervisor:** Department of Computer Science

---

## ⚠️ Medical Disclaimer

> This application is developed for **educational and preventive awareness purposes only**.  
> It does **not** constitute a medical diagnosis or replace professional medical advice.  
> Always consult a licensed healthcare provider for clinical decisions.

---

<p align="center">
  Made with ❤️ by Team SHMS | Integral University, Lucknow
</p>
