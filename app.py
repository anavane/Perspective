# app.py
import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="One-Point Perspective Grid Generator",
    layout="wide"
)

st.title("🎨 One-Point Perspective Grid Generator")
st.write(
    "Generate customizable one-point perspective grids for drawing, "
    "storyboarding, design, and proportion studies."
)

# -------------------------
# Sidebar settings
# -------------------------
st.sidebar.header("Grid Controls")

canvas_width = st.sidebar.number_input(
    "Canvas width (px)", min_value=400, max_value=3000, value=1200, step=100
)

canvas_height = st.sidebar.number_input(
    "Canvas height (px)", min_value=100, max_value=3000, value=800, step=50
)

horizon_frac = st.sidebar.slider(
    "Horizon height (fraction of canvas)",
    min_value=0.05, max_value=0.95, value=0.45, step=0.01
)

vp_x_frac = st.sidebar.slider(
    "Vanishing point X position (fraction of width)",
    min_value=0.0, max_value=1.0, value=0.5, step=0.01
)

n_converging = st.sidebar.slider(
    "Number of converging (depth) lines",
    min_value=6, max_value=80, value=24, step=1
)

n_horizontal = st.sidebar.slider(
    "Number of horizontal guides",
    min_value=3, max_value=50, value=10, step=1
)

line_thickness = st.sidebar.slider(
    "Line thickness",
    min_value=0.5, max_value=4.0, value=1.2, step=0.1
)

grid_color = st.sidebar.color_picker("Grid line color", value="#222222")
bg_color = st.sidebar.color_picker("Background color", value="#ffffff")

# -------------------------
# Function to generate the grid
# -------------------------
def generate_perspective_grid(width, height, horizon_frac, vp_x_frac,
                              n_converging, n_horizontal, line_thickness, grid_color, bg_color):
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # Vanishing point
    vp_x = vp_x_frac * width
    vp_y = horizon_frac * height
    
    # Horizontal guides
    for i in range(n_horizontal):
        y = i * height / (n_horizontal - 1)
        ax.plot([0, width], [y, y], color=grid_color, linewidth=line_thickness)
    
    # Converging lines
    for i in range(n_converging):
        x = i * width / (n_converging - 1)
        ax.plot([x, vp_x], [height, vp_y], color=grid_color, linewidth=line_thickness)
    
    ax.axis('off')
    fig.tight_layout(pad=0)
    
    # Convert to PIL image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    im = Image.open(buf)
    plt.close(fig)
    return im

# -------------------------
# Show the generated grid
# -------------------------
grid_image = generate_perspective_grid(
    canvas_width, canvas_height, horizon_frac, vp_x_frac,
    n_converging, n_horizontal, line_thickness, grid_color, bg_color
)

st.image(grid_image, use_column_width=True)

