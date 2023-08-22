import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np

st.set_page_config(page_title="DSP Signal processing", layout="wide")
st.title("DSP signal")

col1, col2 = st.columns(2)

st.markdown("""
<style>
.css-1rs6os.edgvbvh3
{
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.css-10pw50.egzxvld1
{
visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


def createfig(data):
    plot_spot = st.empty()
    ymax = max(data["Amplitude"]) + 5
    ymin = min(data["Amplitude"]) - 5

    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Signal'))
    return fig


def animate(data, fig, speed=1):
    frames = []
    for i in range(500):
        x_new = data.iloc[:i + 1, 0]
        y_new = data.iloc[:i + 1, 1]
        frames.append(go.Frame(data=[go.Scatter(x=x_new, y=y_new, mode='lines', name='Sine Wave')]))

    fig.frames = frames
    animation_settings = dict(frame=dict(duration=50 / speed, redraw=True), fromcurrent=True)

    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, animation_settings]
                    ),
                    dict(
                        label='Stop',
                        method='animate',
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate",
                                           transition=dict(duration=0))]
                    ),
                    dict(
                        label='Rewind',
                        method='animate',
                        args=[[0], dict(frame=dict(duration=0, redraw=True), mode="immediate",
                                        transition=dict(duration=0))]
                    ),
                    dict(
                        label='Speed Up',
                        method='relayout',
                        args=['frame.duration', 10]
                    ),
                    dict(
                        label='Slow Down',
                        method='relayout',
                        args=['frame.duration', 100]
                    )
                ]
            )
        ]
    )
    fig.update_layout(
        xaxis=dict(
            fixedrange=False,
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1s", step="second", stepmode="backward"),
                    dict(count=10, label="10s", step="second", stepmode="backward"),
                    dict(count=1, label="1m", step="minute", stepmode="backward"),
                    dict(count=10, label="10m", step="minute", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="linear"
        )
    )


with col1:
    # Upload file
    file = st.file_uploader("Please upload a file", type=["csv"], key="file_upload_1")

    # Read data and plot dynamic graph
    if file is not None:
        data = pd.read_csv(file)
        fig = createfig(data)
        animate(data, fig)
        st.plotly_chart(fig, use_container_width=True)
with col2:
    # Upload file
    file1 = st.file_uploader("Please upload a file", type=["csv"], key="file_upload_2")

    # Read data and plot dynamic graph
    if file1 is not None:
        data1 = pd.read_csv(file1)
        fig= createfig(data1)
        animate(data1, fig)
        st.plotly_chart(fig, use_container_width=True)