import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.colors as mcolors
import plotly.io as pio

st.set_page_config(page_title="Professional Perspective Grid", layout="wide")
st.title("🎨 Professional Perspective Grid Generator")

# -----------------------------
# Canvas settings
# -----------------------------
canvas_width = st.sidebar.number_input("Canvas width (px)", 400, 3000, 1200, 100)
canvas_height = st.sidebar.number_input("Canvas height (px)", 200, 3000, 800, 50)
bg_color = st.sidebar.color_picker("Background color", "#ffffff")
grid_color = st.sidebar.color_picker("Grid color", "#888888")
grid_opacity = st.sidebar.slider("Grid opacity", 0.05, 0.5, 0.2, 0.01)

# -----------------------------
# Perspective settings
# -----------------------------
vp_count = st.sidebar.slider("Number of vanishing points", 1, 5, 2)
lines_per_vp = st.sidebar.slider("Number of lines per VP", 5, 80, 20)
directions = ["Up", "Down", "Left", "Right"]
line_styles = ["solid", "dot", "dash"]

# -----------------------------
# Initialize SessionState
# -----------------------------
if 'vp_positions' not in st.session_state:
    st.session_state.vp_positions = [[canvas_width*0.5, canvas_height*0.5, directions[i%4]] for i in range(vp_count)]
if 'vp_colors' not in st.session_state:
    st.session_state.vp_colors = ["#222222" for _ in range(vp_count)]
if 'vp_styles' not in st.session_state:
    st.session_state.vp_styles = ["solid" for _ in range(vp_count)]

# Adjust size if vp_count changes
if len(st.session_state.vp_positions) < vp_count:
    for i in range(len(st.session_state.vp_positions), vp_count):
        st.session_state.vp_positions.append([canvas_width*0.5, canvas_height*0.5, directions[i%4]])
if len(st.session_state.vp_colors) < vp_count:
    for i in range(len(st.session_state.vp_colors), vp_count):
        st.session_state.vp_colors.append("#222222")
if len(st.session_state.vp_styles) < vp_count:
    for i in range(len(st.session_state.vp_styles), vp_count):
        st.session_state.vp_styles.append("solid")

# -----------------------------
# Horizon
# -----------------------------
horizon_y = st.sidebar.slider("Horizon line Y (px)", 0, canvas_height, int(canvas_height*0.5))

# -----------------------------
# Ojo de pez / curvatura
# -----------------------------
enable_fisheye = st.sidebar.checkbox("Enable fish-eye distortion")
fisheye_strength = 0.6
if enable_fisheye:
    fisheye_strength = st.sidebar.slider("Fish-eye strength", 0.01, 2.0, 0.6, 0.01)

enable_curvature = st.sidebar.checkbox("Enable curved/cylindrical perspective")
curvature_strength = 0.3
if enable_curvature:
    curvature_strength = st.sidebar.slider("Curvature strength", 0.01, 1.0, 0.3, 0.01)

# -----------------------------
# Markers of plane
# -----------------------------
marker_planes = {}
for plane in ["Floor", "Wall", "Ceiling"]:
    x = st.sidebar.slider(f"{plane} marker X", 0, canvas_width, int(canvas_width*0.5))
    y = st.sidebar.slider(f"{plane} marker Y", 0, canvas_height, int(canvas_height*0.5))
    marker_planes[plane] = [x, y]

# -----------------------------
# VP controls in sidebar
# -----------------------------
st.sidebar.markdown("### Vanishing Points Controls")
for i in range(vp_count):
    st.sidebar.markdown(f"**VP {i+1}**")
    x = st.sidebar.slider(f"VP {i+1} X", 0, canvas_width, int(st.session_state.vp_positions[i][0]))
    y = st.sidebar.slider(f"VP {i+1} Y", 0, canvas_height, int(st.session_state.vp_positions[i][1]))
    dir = st.sidebar.selectbox(f"VP {i+1} direction", directions, index=directions.index(st.session_state.vp_positions[i][2]))
    color = st.sidebar.color_picker(f"VP {i+1} color", st.session_state.vp_colors[i])
    style = st.sidebar.selectbox(f"VP {i+1} line style", line_styles, index=line_styles.index(st.session_state.vp_styles[i]))
    st.session_state.vp_positions[i] = [x, y, dir]
    st.session_state.vp_colors[i] = color
    st.session_state.vp_styles[i] = style

# -----------------------------
# Layers / Capas
# -----------------------------
st.sidebar.markdown("### Layers / Capas")
show_grid = st.sidebar.checkbox("Show Grid", True)
show_horizon = st.sidebar.checkbox("Show Horizon", True)
show_vp = [st.sidebar.checkbox(f"Show VP {i+1}", True) for i in range(vp_count)]
show_planes = {}
for plane in ["Floor", "Wall", "Ceiling"]:
    show_planes[plane] = st.sidebar.checkbox(f"Show {plane} plane", True)
show_guides = st.sidebar.checkbox("Show Proportion Guides", True)
n_guides = st.sidebar.slider("Number of proportion guides", 2, 20, 5)

# -----------------------------
# Helper functions
# -----------------------------
def fisheye(x, y, cx, cy, strength):
    dx, dy = x-cx, y-cy
    dist = np.sqrt(dx**2 + dy**2)
    factor = 1 + strength*(dist/max(canvas_width, canvas_height))**2
    return cx + dx*factor, cy + dy*factor

def curvature(x, y, cx, cy, strength):
    dx, dy = x-cx, y-cy
    factor = 1 + strength*np.sin(np.pi*dx/canvas_width)
    return cx + dx*factor, cy + dy*factor

def hex_to_rgba(hex_color, alpha):
    rgb = mcolors.hex2color(hex_color)
    return f"rgba({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)},{alpha})"

grid_rgba = hex_to_rgba(grid_color, grid_opacity)

# -----------------------------
# Generate figure
# -----------------------------
fig = go.Figure()
fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color)

# Grid
if show_grid:
    grid_spacing = 50
    for gx in np.arange(0, canvas_width, grid_spacing):
        fig.add_shape(type="line", x0=gx, y0=0, x1=gx, y1=canvas_height, line=dict(color=grid_rgba, width=1, dash="dot"))
    for gy in np.arange(0, canvas_height, grid_spacing):
        fig.add_shape(type="line", x0=0, y0=gy, x1=canvas_width, y1=gy, line=dict(color=grid_rgba, width=1, dash="dot"))

# Horizon line
if show_horizon:
    fig.add_shape(type="line", x0=0, y0=horizon_y, x1=canvas_width, y1=horizon_y, line=dict(color="blue", width=2, dash="dash"))

# Lines towards VPs
for i, vp in enumerate(st.session_state.vp_positions):
    if show_vp[i]:
        x_vp, y_vp, dir = vp
        vp_color = st.session_state.vp_colors[i]
        vp_style = st.session_state.vp_styles[i]
        if dir in ["Up", "Down"]:
            starts = np.linspace(0, canvas_width, lines_per_vp)
            for sx in starts:
                sy = canvas_height if dir=="Up" else 0
                x1, y1, x2, y2 = sx, sy, x_vp, y_vp
                if enable_fisheye:
                    x1, y1 = fisheye(x1, y1, canvas_width/2, canvas_height/2, fisheye_strength)
                    x2, y2 = fisheye(x2, y2, canvas_width/2, canvas_height/2, fisheye_strength)
                if enable_curvature:
                    x1, y1 = curvature(x1, y1, canvas_width/2, canvas_height/2, curvature_strength)
                    x2, y2 = curvature(x2, y2, canvas_width/2, canvas_height/2, curvature_strength)
                fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2, line=dict(color=vp_color, width=2, dash=vp_style))
        else:
            starts = np.linspace(0, canvas_height, lines_per_vp)
            for sy in starts:
                sx = canvas_width if dir=="Left" else 0
                x1, y1, x2, y2 = sx, sy, x_vp, y_vp
                if enable_fisheye:
                    x1, y1 = fisheye(x1, y1, canvas_width/2, canvas_height/2, fisheye_strength)
                    x2, y2 = fisheye(x2, y2, canvas_width/2, canvas_height/2, fisheye_strength)
                if enable_curvature:
                    x1, y1 = curvature(x1, y1, canvas_width/2, canvas_height/2, curvature_strength)
                    x2, y2 = curvature(x2, y2, canvas_width/2, canvas_height/2, curvature_strength)
                fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2, line=dict(color=vp_color, width=2, dash=vp_style))

# VP markers
for i, vp in enumerate(st.session_state.vp_positions):
    if show_vp[i]:
        fig.add_trace(go.Scatter(x=[vp[0]], y=[vp[1]], mode="markers", marker=dict(size=12, color="red"), name=f"VP {i+1}"))

# Markers for planes
for plane, pos in marker_planes.items():
    if show_planes[plane]:
        fig.add_trace(go.Scatter(x=[pos[0]], y=[pos[1]], mode="markers+text", marker=dict(size=10, color="green"),
                                 text=[plane], textposition="top center"))

# Proportion guides
if show_guides:
    for i in range(1, n_guides):
        y = horizon_y + i*(canvas_height-horizon_y)/n_guides
        fig.add_shape(type="line", x0=0, y0=y, x1=canvas_width, y1=y,
                      line=dict(color="gray", width=1, dash="dot", opacity=0.3))

# Layout
fig.update_layout(width=canvas_width, height=canvas_height,
                  xaxis=dict(range=[0, canvas_width], showgrid=False, zeroline=False),
                  yaxis=dict(range=[0, canvas_height], showgrid=False, zeroline=False, scaleanchor="x"),
                  dragmode="pan")

# Display figure
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Download PNG
# -----------------------------
try:
    img_bytes = pio.to_image(fig, format='png')
    st.download_button("⬇️ Download PNG", data=img_bytes, file_name="perspective_grid.png", mime="image/png")
except:
    st.warning("PNG export requires 'kaleido'. Add 'kaleido' to requirements.txt")

