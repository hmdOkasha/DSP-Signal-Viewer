import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="DSP Signal processing", layout="wide")
st.title("DSP signal")
layout = "wide"
st.markdown(
    """
<style>
.css-1rs6os.edgvbvh3
{
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
.css-10pw50.egzxvld1
{
visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)

file = st.file_uploader("Please upload a file", type=["csv"])
if file is not None:
    data = pd.read_csv(file)
    # else:
    #     st.warning("you need to upload a csv file")

    # data= pd.read_csv("E:\\ECG dataset\\test data.csv")
    plot_spot = st.empty()
    # yf=data["Ampitude"][:50]
    # xf=data["Time in uS"][:50]

    # function to make chart
    ymax = max(data["Amplitude"]) + 5
    ymin = min(data["Amplitude"]) - 5

    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines", name="Signal"))

    # fig.update_layout(width=900, height=570, xaxis_title='time',
    #                   yaxis_title="Ampitude")
    fig.update_layout(
        xaxis=dict(
            fixedrange=False,
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1s", step="second", stepmode="backward"),
                        dict(count=10, label="10s", step="second", stepmode="backward"),
                        dict(count=1, label="1m", step="minute", stepmode="backward"),
                        dict(count=10, label="10m", step="minute", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            type="linear",
        )
    )

    def animate(data):
        frames = []
        for i in range(500):
            x_new = data.iloc[: i + 1, 0]
            y_new = data.iloc[: i + 1, 1]
            frames.append(
                go.Frame(
                    data=[go.Scatter(x=x_new, y=y_new, mode="lines", name="Sine Wave")]
                )
            )

        fig.frames = frames
        animation_settings = dict(
            frame=dict(duration=50, redraw=True), fromcurrent=True
        )

        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, animation_settings],
                        )
                    ],
                )
            ]
        )

    animate(data)
    st.plotly_chart(fig, use_container_width=True)

    # Read data and plot dynamic graph
    if file1 is not None:
        data1 = pd.read_csv(file1)
        fig = createfig(data1)
        animate(data1, fig)
        st.plotly_chart(fig, use_container_width=True)
