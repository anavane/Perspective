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
# Sidebar: Vanishing Points
# -------------------------
st.sidebar.header("Vanishing Points")

num_vp = st.sidebar.slider("Number of vanishing points", 1, 5, 3)

directions = ["Up", "Down", "Left", "Right"]

vp_data = []

# -------------------------
# Apply presets (optional)
# -------------------------
def apply_preset(name):
    if name == "Architecture":
        return [
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Up"},
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Down"},
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Left"},
            {"x": 0.5, "y": 0.5, "n": 40, "direction": "Right"},
        ]
    if name == "Interior Room":
        return [
            {"x": 0.8, "y": 0.5, "n": 35, "direction": "Left"},
            {"x": 0.2, "y": 0.5, "n": 35, "direction": "Right"},
        ]
    if name == "Comic Dynamic":
        return [
            {"x": 0.5, "y": 0.3, "n": 60, "direction": "Down"},
            {"x": 0.2, "y": 0.8, "n": 40, "direction": "Right"},
            {"x": 0.8, "y": 0.8, "n": 40, "direction": "Left"},
        ]
    if name == "Storyboard":
        return [
            {"x": 0.5, "y": 0.4, "n": 30, "direction": "Down"},
        ]
    if name == "Cartoon Fish-Eye":
        return [
            {"x": 0.5, "y": 0.5, "n": 100, "direction": "Up"},
            {"x": 0.5, "y": 0.5, "n": 100, "direction": "Down"},
            {"x": 0.5, "y": 0.5, "n": 100, "direction": "Left"},
            {"x": 0.5, "y": 0.5, "n": 100, "direction": "Right"},
        ]

    return None


preset_data = apply_preset(preset)

# -------------------------
# Manual vanishing points
# -------------------------
if preset == "None":
    for i in range(num_vp):
        st.sidebar.subheader(f"Vanishing Point {i+1}")

        x = st.sidebar.slider(f"VP {i+1} - X position", 0.0, 1.0, 0.5, 0.01)
        y = st.sidebar.slider(f"VP {i+1} - Y position", 0.0, 1.0, 0.5, 0.01)
        n = st.sidebar.slider(f"VP {i+1} - Number of Lines", 5, 100, 20)
        direction = st.sidebar.selectbox(
            f"VP {i+1} Direction",
            directions,
            key=f"dir_{i}"
        )

        vp_data.append({"x": x, "y": y, "n": n, "direction": direction})
else:
    vp_data = preset_data

# -------------------------
# Perspective helpers
# -------------------------
def generate_lines(vp, width, height):
    vp_x = vp["x"] * width
    vp_y = vp["y"] * height
    n = vp["n"]
    direction = vp["direction"]

    if direction == "Up":
        targets = [(i, 0) for i in np.linspace(0, width, n)]
    elif direction == "Down":
        targets = [(i, height) for i in np.linspace(0, width, n)]
    elif direction == "Left":
        targets = [(0, i) for i in np.linspace(0, height, n)]
    else:  # Right
        targets = [(width, i) for i in np.linspace(0, height, n)]

    return [((vp_x, vp_y), t) for t in targets]


def apply_fisheye(x, y, cx, cy, strength):
    dx = x - cx
    dy = y - cy
    dist = np.sqrt(dx * dx + dy * dy)

    factor = 1 + strength * (dist / max(canvas_width, canvas_height)) ** 2

    return cx + dx * factor, cy + dy * factor

# -------------------------
# Generate the grid
# -------------------------
fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)
ax.set_xlim(0, canvas_width)
ax.set_ylim(canvas_height, 0)
ax.set_facecolor(bg_color)

for vp in vp_data:
    lines = generate_lines(vp, canvas_width, canvas_height)

    for (x1, y1), (x2, y2) in lines:
        if enable_fisheye:
            cx, cy = canvas_width / 2, canvas_height / 2
            x1, y1 = apply_fisheye(x1, y1, cx, cy, fisheye_strength)
            x2, y2 = apply_fisheye(x2, y2, cx, cy, fisheye_strength)

        ax.plot([x1, x2], [y1, y2], color=grid_color, linewidth=line_thickness)

ax.axis("off")

# -------------------------
# Convert figure to image
# -------------------------
buf = io.BytesIO()
plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
buf.seek(0)

# -------------------------
# Display
# -------------------------
st.image(buf, use_column_width=True)

# -------------------------
# Download button
# -------------------------
st.download_button(
    label="⬇️ Download PNG",
    data=buf,
    file_name="perspective_grid.png",
    mime="image/png"
)

