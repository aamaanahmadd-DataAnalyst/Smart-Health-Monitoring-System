import pickle
import streamlit as st
import os

@st.cache_resource
def load_models():
    """
    Load diabetes and heart disease models.
    Models are saved as dict: {"model": rf, "scaler": scaler}
    Returns (diabetes_bundle, heart_bundle)
    """

    diabetes_path = "models/diabetes_model.pkl"
    heart_path    = "models/heart_model.pkl"

    # ---- Diabetes ----
    if not os.path.exists(diabetes_path):
        st.error("❌ diabetes_model.pkl not found. Please run train_models.py first.")
        st.stop()

    # ---- Heart ----
    if not os.path.exists(heart_path):
        st.error("❌ heart_model.pkl not found. Please run train_models.py first.")
        st.stop()

    with open(diabetes_path, "rb") as f:
        diabetes_bundle = pickle.load(f)

    with open(heart_path, "rb") as f:
        heart_bundle = pickle.load(f)

    return diabetes_bundle, heart_bundle
