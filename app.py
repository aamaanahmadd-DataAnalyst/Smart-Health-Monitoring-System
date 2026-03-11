import streamlit as st
import json
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Health Monitoring System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="auto"
)

# ---------------- LOAD CSS ----------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()


# ---------------- LOAD LOTTIE JSON ----------------
def load_lottiefile(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None


health_animation = load_lottiefile("assets/health.json")


# ---------------- LOAD MODELS ----------------
from utils.load_models import load_models

@st.cache_resource
def load_models_cached():
    return load_models()

diabetes_model, heart_model = load_models_cached()


if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- LOAD MODULES ----------------
from modules.vital import show_vital
from modules.bmi import show_bmi_calculator
from modules.diabetes import show_diabetes_prediction
from modules.heart import show_heart_prediction
from modules.analytics import show_health_analytics
from modules.about import show_about


# ---------------- HEADER ----------------
col1, col2 = st.columns([1,2])

with col1:

    if health_animation:
        components.html(f"""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

        <lottie-player
            autoplay
            loop
            mode="normal"
            src='{json.dumps(health_animation)}'
            style="width:280px;height:200px;background:transparent;">
        </lottie-player>
        """, height=200)

with col2:
    st.markdown("""
    <h1 style='margin-top:40px;'>🩺 Smart Health Monitoring System</h1>
    <p style='color:lightgray;'>AI-Powered Multi Disease Risk Prediction System</p>
    """, unsafe_allow_html=True)

st.markdown("---")


# ---------------- SIDEBAR ----------------
st.sidebar.title("🩺 Monitoring Options")

menu = st.sidebar.radio(
    "Select a Module",
    [
        "Vital Health Check",
        "BMI Calculator",
        "Diabetes Prediction",
        "Heart Disease Prediction",
        "Health Analytics & Report",
        "About"
    ]
)


# ---------------- ROUTING ----------------
if menu == "Vital Health Check":
    show_vital()

elif menu == "BMI Calculator":
    show_bmi_calculator()

elif menu == "Diabetes Prediction":
    show_diabetes_prediction(diabetes_model)

elif menu == "Heart Disease Prediction":
    show_heart_prediction(heart_model)

elif menu == "Health Analytics & Report":
    show_health_analytics(st.session_state.history)

elif menu == "About":
    show_about()

# Mobile sidebar auto-close
st.markdown("""
<script>
const items = window.parent.document.querySelectorAll('[data-testid="stSidebarNavItems"] label');
items.forEach(item => {
    item.addEventListener('click', () => {
        const btn = window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"]');
        if (btn && window.parent.innerWidth < 768) btn.click();
    });
});
</script>
""", unsafe_allow_html=True)
# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center>
<p style='color:gray;'>© 2026 Smart Health Monitoring System | AI + ML Powered</p>
</center>
""", unsafe_allow_html=True)


