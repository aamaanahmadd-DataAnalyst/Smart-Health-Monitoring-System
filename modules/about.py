import streamlit as st
from streamlit_lottie import st_lottie
import base64
import os
import json


# ----------- LOAD LOCAL LOTTIE -----------
def load_lottiefile(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None


# ----------- LOAD TEAM IMAGE -----------
def get_base64_image(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def show_about():

    # Load animation
    about_animation = load_lottiefile("assets/healthcare_heart.json")

    st.markdown("""
    <style>

    .about-hero{
        padding:40px 0px;
    }

    .fade-in{
        animation:fadeIn 1.5s ease-in;
    }

    @keyframes fadeIn{
        from{opacity:0;transform:translateY(30px);}
        to{opacity:1;transform:translateY(0);}
    }

    .metric-card{
        background:rgba(255,255,255,0.08);
        padding:25px;
        border-radius:18px;
        text-align:center;
        backdrop-filter:blur(12px);
        box-shadow:0 4px 30px rgba(0,0,0,0.3);
    }

    .team-card{
        background:rgba(255,255,255,0.08);
        padding:20px;
        border-radius:18px;
        text-align:center;
        backdrop-filter:blur(12px);
        box-shadow:0 4px 30px rgba(0,0,0,0.3);
    }

    .team-card img{
        border-radius:50%;
        width:100px;
        height:100px;
        margin-bottom:10px;
        object-fit:cover;
    }

    </style>
    """, unsafe_allow_html=True)


    # ----------- KPI SECTION -----------

    st.markdown("## 📊 Platform Highlights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h2>2+</h2>
            <p>Disease Models</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h2>80%+</h2>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h2>100%</h2>
            <p>Data Privacy</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    # ----------- HERO SECTION -----------

    col1, col2 = st.columns([1,2])

    with col1:
        if about_animation:
            st_lottie(about_animation, height=260)
        else:
            st.image("https://img.icons8.com/color/200/health-checkup.png", width=200)

    with col2:
        st.markdown("""
        <div class="about-hero fade-in">
        <h1 style='font-size:40px;font-weight:700;'>
        Welcome to the Smart Health Monitoring System
        </h1>

        <p style='font-size:18px;color:lightgray;'>
        AI-Powered Preventive Healthcare & Clinical Risk Assessment Platform
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)


    # ----------- PROJECT OVERVIEW -----------

    st.markdown("## 🧠 Project Overview")

    st.write("""
    The Smart Health Monitoring System integrates Machine Learning with a rule-based 
    clinical advisory engine to deliver early detection insights for chronic diseases 
    like Diabetes and Heart Disease.

    The system predicts risk probability and generates lifestyle recommendations 
    based on medical thresholds.
    """)


    # ----------- TECH STACK -----------

    st.markdown("## 🛠 Technology Stack")

    st.write("""
    • Python 3.x  
    • Streamlit  
    • Scikit-learn (Random Forest & Logistic Regression)  
    • Plotly Visualization  
    • ReportLab PDF Generation  
    • Lottie Animations  
    """)

    st.markdown("<hr>", unsafe_allow_html=True)


    # ----------- TEAM SECTION -----------

    st.markdown("## 👨‍💻 Team Members")

    t1, t2, t3 = st.columns(3)

    img1 = get_base64_image("Team/Amaan_A.jpg")
    img2 = get_base64_image("Team/Sharukh_S.jpeg")
    img3 = get_base64_image("Team/Fuzail_K.jpeg")

    fallback = "https://img.icons8.com/color/100/user-male-circle--v1.png"

    def img_tag(b64):
        if b64:
            return f'<img src="data:image/jpeg;base64,{b64}" width="100">'
        return f'<img src="{fallback}" width="100">'


    with t1:
        st.markdown(f"""
        <div class="team-card fade-in">
            {img_tag(img1)}
            <h4>Amaan Ahmad</h4>
            <p>Machine Learning & Frontend Development</p>
            <a href="https://www.linkedin.com/in/amaan-ahmadli" target="_blank">LinkedIn</a> |
            <a href="https://github.com/amaanahmaddd" target="_blank">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="team-card fade-in">
            {img_tag(img2)}
            <h4>Md. Sharukh</h4>
            <p>Model Training & Backend Integration</p>
            <a href="https://www.linkedin.com/in/shahrukh-ahmad-397145266?utm_source=share_via&utm_content=profile&utm_medium=member_android" target="_blank">LinkedIn</a>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown(f"""
        <div class="team-card fade-in">
            {img_tag(img3)}
            <h4>Mohd. Fuzail Khan</h4>
            <p>Documentation & Research</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)


    # ----------- DISCLAIMER -----------

    st.markdown("## ⚠️ Medical Disclaimer")

    st.write("""
    This platform provides predictive health insights for preventive awareness only.
    It does not replace professional medical diagnosis or treatment.
    Always consult a licensed healthcare provider for medical decisions.
    """)

    st.markdown("---")

    st.markdown(
        "<center><h4>🚀 AI-Integrated Preventive Healthcare Platform</h4>"
        "<p style='color:gray;'>Integral University, Lucknow | B.Tech CSE 2025-26</p></center>",
        unsafe_allow_html=True
    )