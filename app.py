import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🎨 Interactive Perspective Grid")

canvas_width = 1200
canvas_height = 800
n_lines = 20

# Inicializar puntos de fuga
if 'vp_positions' not in st.session_state:
    st.session_state.vp_positions = [
        [canvas_width*0.5, canvas_height*0.5],
        [canvas_width*0.2, canvas_height*0.8]
    ]

# Crear figura
fig = go.Figure()

# Dibujar cuadrícula de fondo
grid_spacing = 50
for x in np.arange(0, canvas_width, grid_spacing):
    fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=canvas_height, line=dict(color="gray", width=1, dash="dot", opacity=0.2))
for y in np.arange(0, canvas_height, grid_spacing):
    fig.add_shape(type="line", x0=0, y0=y, x1=canvas_width, y1=y, line=dict(color="gray", width=1, dash="dot", opacity=0.2))

# Dibujar líneas hacia cada VP
for vp in st.session_state.vp_positions:
    xs = np.linspace(0, canvas_width, n_lines)
    for x_start in xs:
        fig.add_shape(type="line", x0=x_start, y0=canvas_height, x1=vp[0], y1=vp[1], line=dict(color="black"))

# Dibujar VP como puntos arrastrables
for i, vp in enumerate(st.session_state.vp_positions):
    fig.add_trace(go.Scatter(x=[vp[0]], y=[vp[1]],
                             mode="markers",
                             marker=dict(size=12, color="red"),
                             name=f"VP {i+1}",
                             draggable=True))

fig.update_layout(width=canvas_width, height=canvas_height,
                  xaxis=dict(range=[0, canvas_width], showgrid=False, zeroline=False),
                  yaxis=dict(range=[0, canvas_height], showgrid=False, zeroline=False, scaleanchor="x"),
                  dragmode="drawopenpath")

st.plotly_chart(fig)

