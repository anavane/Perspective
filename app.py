import streamlit as st
import plotly.graph_objects as go
import numpy as np
import io
from PIL import Image

st.set_page_config(page_title="Interactive Perspective Grid", layout="wide")
st.title("🎨 Interactive Perspective Grid Generator")

# -----------------------------
# Canvas settings
# -----------------------------
canvas_width = st.sidebar.number_input("Canvas width (px)", 400, 3000, 1200, 100)
canvas_height = st.sidebar.number_input("Canvas height (px)", 200, 3000, 800, 50)
line_color = st.sidebar.color_picker("Line color", "#222222")
line_thickness = st.sidebar.slider("Line thickness", 0.5, 5.0, 1.5, 0.1)
grid_color = st.sidebar.color_picker("Grid color", "#888888")
grid_opacity = st.sidebar.slider("Grid opacity", 0.05, 0.5, 0.2, 0.01)

# Fish-eye settings
enable_fisheye = st.sidebar.checkbox("Enable fish-eye distortion", False)
fisheye_strength = 0.6
if enable_fisheye:
    fisheye_strength = st.sidebar.slider("Fish-eye strength", 0.01, 2.0, 0.6, 0.01)

# -----------------------------
# Vanishing points
# -----------------------------
vp_count = st.sidebar.slider("Number of vanishing points", 1, 5, 2)
directions = ["Up", "Down", "Left", "Right"]

# Initialize VP positions
if 'vp_positions' not in st.session_state or len(st.session_state.vp_positions) != vp_count:
    st.session_state.vp_positions = []
    for i in range(vp_count):
        st.session_state.vp_positions.append([canvas_width*0.5, canvas_height*0.5, directions[i%4]])

# VP controls in sidebar
for i in range(vp_count):
    st.sidebar.markdown(f"### VP {i+1}")
    x = st.sidebar.slider(f"VP {i+1} X (fraction)", 0.0, 1.0, st.session_state.vp_positions[i][0]/canvas_width, 0.01)
    y = st.sidebar.slider(f"VP {i+1} Y (fraction)", 0.0, 1.0, st.session_state.vp_positions[i][1]/canvas_height, 0.01)
    dir = st.sidebar.selectbox(f"VP {i+1} direction", directions, index=directions.index(st.session_state.vp_positions[i][2]))
    st.session_state.vp_positions[i] = [x*canvas_width, y*canvas_height, dir]

# Number of lines per VP
lines_per_vp = st.sidebar.slider("Number of lines per VP", 2, 80, 20)

# -----------------------------
# Fish-eye helper
# -----------------------------
def fisheye(x, y, cx, cy, strength):
    dx, dy = x-cx, y-cy
    dist = np.sqrt(dx**2 + dy**2)
    factor = 1 + strength*(dist/max(canvas_width, canvas_height))**2
    return cx + dx*factor, cy + dy*factor

# -----------------------------
# Generate lines
# -----------------------------
fig = go.Figure()

# Draw background grid
grid_spacing = 50
for gx in np.arange(0, canvas_width, grid_spacing):
    fig.add_shape(type="line", x0=gx, y0=0, x1=gx, y1=canvas_height,
                  line=dict(color=grid_color, width=1, dash="dot", opacity=grid_opacity))
for gy in np.arange(0, canvas_height, grid_spacing):
    fig.add_shape(type="line", x0=0, y0=gy, x1=canvas_width, y1=gy,
                  line=dict(color=grid_color, width=1, dash="dot", opacity=grid_opacity))

# Draw lines towards VPs
for vp in st.session_state.vp_positions:
    x_vp, y_vp, dir = vp
    if dir in ["Up", "Down"]:
        starts = np.linspace(0, canvas_width, lines_per_vp)
        for sx in starts:
            sy = canvas_height if_
