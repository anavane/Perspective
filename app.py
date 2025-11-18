import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Advanced Multi-Vanishing Point Grid Generator",
    layout="wide"
)

st.title("🎨 Multi-Vanishing Point Perspective Grid Generator")
st.write(
    "Generate professional 1 to 5-point perspective grids for drawing, storyboarding, design, and proportion studies."
)

# -------------------------
# Sidebar settings
# -------------------------
st.sidebar.header("Canvas Settings")

canvas_width = st.sidebar.number_input(
    "Canvas width (px)", min_value=400, max_value=3000, value=1200, step=100
)

canvas_height = st.sidebar.number_input(
    "Canvas height (px)", min_value=100, max_value=3000, value=800, step=50
)

bg_color = st.sidebar.color_picker("Background color", value="#ffffff")

# -------------------------
# Grid Settings
# -------------------------
st.sidebar.header("Grid Settings")

perspective_type = st.sidebar.selectbox(
    "Perspective type",
    ["One-Point", "Two-Point", "Three-Point", "Four-Point", "Five-Point", "Fisheye"]
)

horizon_frac = st.sidebar.slider(
    "Horizon height (fraction of canvas)",
    min_value=0.05, max_value=0.95, value=0.45, step=0.01
)

# Up to 5 vanishing points
vp_points = []
vp_directions = []
for i in range(5):
    st.sidebar.markdown(f"**Vanishing Point {i+1}**")
    x_frac = st.sidebar.slider(f"VP {i+1} X (fraction)", 0.0, 1.0, 0.5, 0.01)
    y_frac = st.sidebar.slider(f"VP {i+1} Y (fraction)", 0.0, 1.0, horizon_frac, 0.01)
    direction = st.sidebar.selectbox(f"VP {i+1} Direction", ["Up", "Down", "Left", "Right"], key=f"dir{i}")
    vp_points.append((x_frac, y_frac))
    vp_directions.append(direction)

n_converging = st.sidebar.slider(
    "Number of converging lines",
    min_value=6, max_value=100, value=24, step=1
)

n_horizontal = st.sidebar.slider(
    "Number of horizontal guides",
    min_value=3, max_value=50, value=10, step=1
)

line_thickness = st.sidebar.slider(
    "Line thickness",
    min_value=0.5, max_value=4.0, value=1.2, step=0.1
)

line_opacity = st.sidebar.slider(
    "Line opacity", min_value=0.1, max_value=1.0, value=1.0, step=0.05
)

grid_color = st.sidebar.color_picker("Grid line color", value="#222222")

# -------------------------
# Advanced options
# -------------------------
st.sidebar.header("Advanced Options")

reference_image_file = st.sidebar.file_uploader(
    "Upload reference image (optional)", type=["png", "jpg", "jpeg"]
)

show_cubes = st.sidebar.checkbox("Overlay cubes", value=False)

# -------------------------
# Function to generate grid
# -------------------------
def generate_grid(width, height, bg_color, perspective_type,
                  vp_points, vp_directions, n_converging, n_horizontal,
                  line_thickness, line_opacity, grid_color,
                  reference_image=None, show_cubes=False):
    
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # Load reference image if provided
    if reference_image:
        ref_im = Image.open(reference_image)
        ax.imshow(ref_im, extent=[0, width, 0, height])
    
    # Horizontal guides
    for i in range(n_horizontal):
        y = i * height / (n_horizontal - 1)
        ax.plot([0, width], [y, y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
    
    # Function to draw converging lines to a vanishing point
    def draw_lines(vp_x, vp_y, direction):
        for i in range(n_converging):
            x = i * width / (n_converging - 1)
            y = i * height / (n_converging - 1)
            if direction == "Up":
                ax.plot([x, vp_x], [height, vp_y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
            elif direction == "Down":
                ax.plot([x, vp_x], [0, vp_y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
            elif direction == "Left":
                ax.plot([width, vp_x], [y, vp_y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
            elif direction == "Right":
                ax.plot([0, vp_x], [y, vp_y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
    
    # Draw vanishing points according to perspective type
    vp_count = {
        "One-Point": 1,
        "Two-Point": 2,
        "Three-Point": 3,
        "Four-Point": 4,
        "Five-Point": 5,
        "Fisheye": 1
    }[perspective_type]
    
    if perspective_type != "Fisheye":
        for i in range(vp_count):
            vp_x = vp_points[i][0]*width
            vp_y = vp_points[i][1]*height
            draw_lines(vp_x, vp_y, vp_directions[i])
    else:
        # Fisheye simulation
        for i in range(n_converging):
            theta = i / n_converging * 2 * np.pi
            x = width/2 + np.cos(theta)*(width/2)
            y = height/2 + np.sin(theta)*(height/2)
            ax.plot([width/2, x], [height/2, y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
    
    # Optional ove
