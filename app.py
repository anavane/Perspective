import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import streamlit as st

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Advanced Perspective Grid Generator",
    layout="wide"
)

st.title("🎨 Advanced Multi-Vanishing-Point Perspective Grid Generator")
st.write(
    "Generate advanced perspective grids with up to **five vanishing points**, "
    "custom directions, presets, fish-eye distortion, and PNG export."
)

# -------------------------
# Sidebar: Presets
# -------------------------
st.sidebar.header("Presets")

preset = st.sidebar.selectbox(
    "Choose a preset (optional):",
    [
        "None",
        "Architecture",
        "Interior Room",
        "Comic Dynamic",
        "Storyboard",
        "Cartoon Fish-Eye"
    ]
)

# -------------------------
# Sidebar: Canvas Settings
# -------------------------
st.sidebar.header("Canvas Settings")

canvas_width = st.sidebar.number_input("Canvas width (px)", 400, 3000, 1200, 50)
canvas_height = st.sidebar.number_input("Canvas height (px)", 400, 3000, 800, 50)

line_thickness = st.sidebar.slider("Line thickness", 0.5, 4.0, 1.2, 0.1)

grid_color = st.sidebar.color_picker("Grid line color", "#222222")
bg_color = st.sidebar.color_picker("Background color", "#ffffff")

# -------------------------
# Sidebar: Fish-Eye Mode
# -------------------------
st.sidebar.header("Fish-Eye Distortion (Curvilinear)")

enable_fisheye = st.sidebar.checkbox("Enable fish-eye distortion", False)

if enable_fisheye:
    fisheye_strength = st.sidebar.slider(
        "Distortion strength",
        0.01, 2.0, 0.6, 0.01
    )

# -------------------------
# Presets definition
# -------------------------
def apply_preset(name):
    if name == "Architecture":
        return [
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Up"},
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Down"},
            {"x": 0.5, "y": 0.5, "n":

