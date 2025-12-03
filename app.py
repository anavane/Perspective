import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib.colors as mcolors
import plotly.io as pio

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

# Lines per VP
lines_per_vp = st.sidebar.slider("Number of lines per VP", 2, 80, 20)

# -----------------------------
# Helpers
# -----------------------------
def fisheye(x, y, cx, cy, strength):
    dx, dy = x-cx, y-cy
    dist = np.sqrt(dx**2 + dy**2)
    factor = 1 + strength*(dist/max(canvas_width, canvas_height))**2
    return cx + dx*factor, cy + dy*factor

def hex_to_rgba(hex_color, alpha):
    rgb = mcolors.hex2color(hex_color)
    rgba = f"rgba({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)},{alpha})"
    return rgba

grid_rgba = hex_to_rgba(grid_color, grid_opacity)

# -----------------------------
# Build figure
# -----------------------------
def create_figure():
    fig = go.Figure()

    # Background grid
    grid_spacing = 50
    for gx in np.arange(0, canvas_width, grid_spacing):
        fig.add_shape(type="line", x0=gx, y0=0, x1=gx, y1=canvas_height,
                      line=dict(color=grid_rgba, width=1, dash="dot"))
    for gy in np.arange(0, canvas_height, grid_spacing):
        fig.add_shape(type="line", x0=0, y0=gy, x1=canvas_width, y1=gy,
                      line=dict(color=grid_rgba, width=1, dash="dot"))

    # Lines towards VPs
    for vp in st.session_state.vp_positions:
        x_vp, y_vp, dir = vp
        if dir in ["Up", "Down"]:
            starts = np.linspace(0, canvas_width, lines_per_vp)
            for sx in starts:
                sy = canvas_height if dir=="Up" else 0
                x1, y1, x2, y2 = sx, sy, x_vp, y_vp
                if enable_fisheye:
                    cx, cy = canvas_width/2, canvas_height/2
                    x1, y1 = fisheye(x1, y1, cx, cy, fisheye_strength)
                    x2, y2 = fisheye(x2, y2, cx, cy, fisheye_strength)
                fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                              line=dict(color=line_color, width=line_thickness))
        else:
            starts = np.linspace(0, canvas_height, lines_per_vp)
            for sy in starts:
                sx = canvas_width if dir=="Left" else 0
                x1, y1, x2, y2 = sx, sy, x_vp, y_vp
                if enable_fisheye:
                    cx, cy = canvas_width/2, canvas_height/2
                    x1, y1 = fisheye(x1, y1, cx, cy, fisheye_strength)
                    x2, y2 = fisheye(x2, y2, cx, cy, fisheye_strength)
                fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                              line=dict(color=line_color, width=line_thickness))

    # VP points (draggable)
    for i, vp in enumerate(st.session_state.vp_positions):
        fig.add_trace(go.Scatter(
            x=[vp[0]], y=[vp[1]],
            mode="markers",
            marker=dict(size=12, color="red"),
            name=f"VP {i+1}",
            marker_symbol="circle",
            customdata=[i],
            hoverinfo="text"
        ))

    fig.update_layout(
        width=canvas_width, height=canvas_height,
        xaxis=dict(range=[0, canvas_width], showgrid=False, zeroline=False),
        yaxis=dict(range=[0, canvas_height], showgrid=False, zeroline=False, scaleanchor="x"),
        dragmode="pan"
    )
    return fig

fig = create_figure()
plotly_chart = st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Download PNG
# -----------------------------
try:
    img_bytes = pio.to_image(fig, format='png')
    st.download_button("⬇️ Download PNG", data=img_bytes, file_name="perspective_grid.png", mime="image/png")
except Exception as e:
    st.warning("PNG export requires 'kaleido'. Add 'kaleido' to requirements.txt")
