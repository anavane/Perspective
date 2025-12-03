import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------
# Streamlit Page Config
# ---------------------------------
st.set_page_config(page_title="Perspective Grid Generator", layout="wide")

st.title("🎨 Perspective Grid Generator (1–5 Vanishing Points)")
st.write(
    "Create customizable perspective grids with up to 5 independent vanishing points."
)

# ---------------------------------
# Sidebar Settings
# ---------------------------------
st.sidebar.header("Canvas Settings")

canvas_width = st.sidebar.number_input("Canvas width (px)", 400, 3000, 1200, 100)
canvas_height = st.sidebar.number_input("Canvas height (px)", 200, 3000, 800, 100)

bg_color = st.sidebar.color_picker("Background color", "#ffffff")
line_color = st.sidebar.color_picker("Line color", "#222222")
line_thickness = st.sidebar.slider("Line thickness", 0.5, 5.0, 1.5, 0.1)

st.sidebar.header("Perspective Settings")

vp_count = st.sidebar.slider(
    "Number of vanishing points", 
    min_value=1, 
    max_value=5, 
    value=2, 
    step=1
)

# ---------------------------------
# Default VP presets (for convenience)
# ---------------------------------
default_vp = [
    {"x": 0.5, "y": 0.5, "n": 25},
    {"x": 0.25, "y": 0.5, "n": 25},
    {"x": 0.75, "y": 0.5, "n": 25},
    {"x": 0.5, "y": 0.25, "n": 25},
    {"x": 0.5, "y": 0.75, "n": 25},
]

# ---------------------------------
# Collect Vanishing Points
# ---------------------------------
vp_list = []

st.sidebar.subheader("Vanishing Points Controls")

for i in range(vp_count):

    st.sidebar.markdown(f"### VP {i+1}")

    x = st.sidebar.slider(
        f"VP {i+1} X (fraction)", 
        0.0, 1.0, default_vp[i]["x"], 0.01
    )
    y = st.sidebar.slider(
        f"VP {i+1} Y (fraction)", 
        0.0, 1.0, default_vp[i]["y"], 0.01
    )
    n = st.sidebar.slider(
        f"VP {i+1}: Number of lines", 
        5, 80, default_vp[i]["n"], 1
    )

    vp_list.append({
        "x": x * canvas_width,
        "y": y * canvas_height,
        "n": n
    })

# ----
