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
vp_x_fracs = []
vp_y_fracs = []
for i in range(5):
    vp_x_fracs.append(st.sidebar.slider(f"Vanishing Point {i+1} X (fraction)", 0.0, 1.0, 0.5, 0.01))
    vp_y_fracs.append(st.sidebar.slider(f"Vanishing Point {i+1} Y (fraction)", 0.0, 1.0, horizon_frac, 0.01))

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

direction = st.sidebar.selectbox(
    "Converging lines direction",
    ["Up", "Down", "Left", "Right"]
)

reference_image_file = st.sidebar.file_uploader(
    "Upload reference image (optional)", type=["png", "jpg", "jpeg"]
)

show_cubes = st.sidebar.checkbox("Overlay cubes", value=False)

# -------------------------
# Function to generate grid
# -------------------------
def generate_grid(width, height, bg_color, perspective_type,
                  vp_points, n_converging, n_horizontal,
                  line_thickness, line_opacity, grid_color,
                  direction, reference_image=None, show_cubes=False):
    
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
    
    # Draw converging lines to a vanishing point
    def draw_lines(vp_x, vp_y):
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
    
    # Determine number of vanishing points based on perspective type
    if perspective_type == "One-Point":
        draw_lines(*vp_points[0])
    elif perspective_type == "Two-Point":
        draw_lines(*vp_points[0])
        draw_lines(*vp_points[1])
    elif perspective_type == "Three-Point":
        draw_lines(*vp_points[0])
        draw_lines(*vp_points[1])
        draw_lines(*vp_points[2])
    elif perspective_type == "Four-Point":
        for i in range(4):
            draw_lines(*vp_points[i])
    elif perspective_type == "Five-Point":
        for i in range(5):
            draw_lines(*vp_points[i])
    elif perspective_type == "Fisheye":
        for i in range(n_converging):
            theta = i / n_converging * 2 * np.pi
            x = width/2 + np.cos(theta)*(width/2)
            y = height/2 + np.sin(theta)*(height/2)
            ax.plot([width/2, x], [height/2, y], color=grid_color, linewidth=line_thickness, alpha=line_opacity)
    
    # Optional overlay cubes
    if show_cubes:
        cube_size = min(width, height)/10
        cube_positions = [(width/4, height/4), (width/2, height/2)]
        for cx, cy in cube_positions:
            ax.plot([cx, cx+cube_size], [cy, cy], color="red", linewidth=1.5)
            ax.plot([cx+cube_size, cx+cube_size], [cy, cy+cube_size], color="red", linewidth=1.5)
            ax.plot([cx+cube_size, cx], [cy+cube_size, cy+cube_size], color="red", linewidth=1.5)
            ax.plot([cx, cx], [cy+cube_size, cy], color="red", linewidth=1.5)
    
    ax.axis('off')
    fig.tight_layout(pad=0)
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    im = Image.open(buf)
    plt.close(fig)
    return im

# -------------------------
# Prepare vanishing points
# -------------------------
vp_points = [(vp_x_fracs[i]*canvas_width, vp_y_fracs[i]*canvas_height) for i in range(5)]

# -------------------------
# Generate and show grid
# -------------------------
grid_image = generate_grid(
    canvas_width, canvas_height, bg_color, perspective_type,
    vp_points, n_converging, n_horizontal,
    line_thickness, line_opacity, grid_color,
    direction, reference_image_file, show_cubes
)

st.image(grid_image, use_column_width=True)
