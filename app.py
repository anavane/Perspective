import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Perspective Grid Generator", layout="wide")
st.title("🎨 Advanced Perspective Grid Generator")
st.write("Create perspective grids with up to 5 vanishing points, fish-eye distortion, and presets.")

# -----------------------------
# Sidebar: Canvas Settings
# -----------------------------
st.sidebar.header("Canvas Settings")
canvas_width = st.sidebar.number_input("Canvas width (px)", 400, 3000, 1200, 100)
canvas_height = st.sidebar.number_input("Canvas height (px)", 200, 3000, 800, 50)
bg_color = st.sidebar.color_picker("Background color", "#ffffff")
line_color = st.sidebar.color_picker("Line color", "#222222")
line_thickness = st.sidebar.slider("Line thickness", 0.5, 5.0, 1.5, 0.1)

# -----------------------------
# Sidebar: Presets
# -----------------------------
st.sidebar.header("Presets")
preset = st.sidebar.selectbox(
    "Choose a preset (optional):",
    ["None", "Architecture", "Interior Room", "Comic Dynamic", "Storyboard", "Cartoon Fish-Eye"]
)

# -----------------------------
# Sidebar: Fish-Eye
# -----------------------------
st.sidebar.header("Fish-Eye (Curvilinear)")
enable_fisheye = st.sidebar.checkbox("Enable fish-eye distortion", False)
if enable_fisheye:
    fisheye_strength = st.sidebar.slider("Distortion strength", 0.01, 2.0, 0.6, 0.01)

# -----------------------------
# Sidebar: Vanishing Points
# -----------------------------
st.sidebar.header("Vanishing Points")
vp_count = st.sidebar.slider("Number of vanishing points", 1, 5, 2)
directions = ["Up", "Down", "Left", "Right"]

# -----------------------------
# Presets Data (Corrected)
# -----------------------------
def apply_preset(name, w, h):
    if name == "Architecture":
        return [
            {"x": 0.2*w, "y": 0.2*h, "n": 30, "dir":"Down"},
            {"x": 0.8*w, "y": 0.2*h, "n": 30, "dir":"Down"},
            {"x": 0.2*w, "y": 0.8*h, "n": 30, "dir":"Up"},
            {"x": 0.8*w, "y": 0.8*h, "n": 30, "dir":"Up"},
        ]
    if name == "Interior Room":
        return [
            {"x": 0.25*w, "y": 0.25*h, "n": 30, "dir":"Down"},
            {"x": 0.75*w, "y": 0.25*h, "n": 30, "dir":"Down"},
            {"x": 0.25*w, "y": 0.75*h, "n": 30, "dir":"Up"},
            {"x": 0.75*w, "y": 0.75*h, "n": 30, "dir":"Up"},
        ]
    if name == "Comic Dynamic":
        return [
            {"x": 0.5*w, "y": 0.2*h, "n": 40, "dir":"Down"},
            {"x": 0.2*w, "y": 0.8*h, "n": 40, "dir":"Right"},
            {"x": 0.8*w, "y": 0.8*h, "n": 40, "dir":"Left"},
        ]
    if name == "Storyboard":
        return [
            {"x": 0.5*w, "y": 0.4*h, "n": 30, "dir":"Down"},
        ]
    if name == "Cartoon Fish-Eye":
        return [
            {"x": 0.2*w, "y": 0.2*h, "n": 50, "dir":"Down"},
            {"x": 0.8*w, "y": 0.2*h, "n": 50, "dir":"Down"},
            {"x": 0.2*w, "y": 0.8*h, "n": 50, "dir":"Up"},
            {"x": 0.8*w, "y": 0.8*h, "n": 50, "dir":"Up"},
        ]
    return None

preset_data = apply_preset(preset, canvas_width, canvas_height)

# -----------------------------
# Collect Vanishing Points
# -----------------------------
vp_list = []

if preset == "None" or preset_data is None:
    for i in range(vp_count):
        st.sidebar.markdown(f"### VP {i+1}")
        x = st.sidebar.slider(f"VP {i+1} X (fraction)", 0.0, 1.0, 0.5, 0.01, key=f"x{i}")*canvas_width
        y = st.sidebar.slider(f"VP {i+1} Y (fraction)", 0.0, 1.0, 0.5, 0.01, key=f"y{i}")*canvas_height
        n = st.sidebar.slider(f"VP {i+1} Number of lines", 2, 80, 20, key=f"n{i}")
        dir = st.sidebar.selectbox(f"VP {i+1} Direction", directions, index=0, key=f"dir{i}")
        vp_list.append({"x": x, "y": y, "n": n, "dir": dir})
else:
    vp_list = preset_data
    vp_count = len(vp_list)

# -----------------------------
# Helper functions
# -----------------------------
def generate_lines(vp, w, h):
    lines = []
    x, y, n, dir = vp["x"], vp["y"], vp["n"], vp["dir"]
    if dir in ["Up", "Down"]:
        xs = np.linspace(0, w, n)
        for i in range(n):
            start_y = h if dir=="Up" else 0
            lines.append(((xs[i], start_y), (x, y)))
    else:
        ys = np.linspace(0, h, n)
        for i in range(n):
            start_x = w if dir=="Left" else 0
            lines.append(((start_x, ys[i]), (x, y)))
    return lines

def apply_fisheye(x, y, cx, cy, strength):
    dx, dy = x-cx, y-cy
    dist = np.sqrt(dx*dx + dy*dy)
    factor = 1 + strength*(dist/max(canvas_width, canvas_height))**2
    return cx+dx*factor, cy+dy*factor

# -----------------------------
# Draw Canvas
# -----------------------------
fig, ax = plt.subplots(figsize=(canvas_width/100, canvas_height/100), dpi=100)
ax.set_xlim(0, canvas_width)
ax.set_ylim(canvas_height, 0)
ax.set_facecolor(bg_color)

for vp in vp_list:
    lines = generate_lines(vp, canvas_width, canvas_height)
    for (x1,y1),(x2,y2) in lines:
        if enable_fisheye:
            cx, cy = canvas_width/2, canvas_height/2
            x1,y1 = apply_fisheye(x1,y1,cx,cy,fisheye_strength)
            x2,y2 = apply_fisheye(x2,y2,cx,cy,fisheye_strength)
        ax.plot([x1,x2],[y1,y2], color=line_color, linewidth=line_thickness)

ax.axis("off")

# -----------------------------
# Display & Download
# -----------------------------
buf = io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
buf.seek(0)

st.image(buf, use_column_width=True)

st.download_button(
    label="⬇️ Download PNG",
    data=buf,
    file_name="perspective_grid.png",
    mime="image/png"
)
