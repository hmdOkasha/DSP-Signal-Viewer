import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import pdfkit

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


def save_as_pdf(statistics, fig, file_name):
    # Set the PDF file name
    pdf_file = f'{file_name}.pdf'

    # Create a HTML string with the signal statistics and plot
    fig_html1 = fig.to_html(full_html=False)
    html_string = f"<h2>Signal Statistics</h2>{statistics}<br><br>{fig_html1}"

    # Save the HTML string as a PDF file

    pdfkit.from_string(html_string, pdf_file)


def createfig(data, color_dropdown):
    plot_spot = st.empty()
    ymax = max(data.iloc[:, 1]) + 5
    ymin = min(data.iloc[:, 1]) - 5
    colors = change_color(color_dropdown)
    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=[], y=[], mode='lines',
                  name='Signal', line_color=color_dropdown))
    return fig


def animate(data, fig, speed=1):
    frames = []
    for i in range(500):
        x_new = data.iloc[:i + 1, 0]
        y_new = data.iloc[:i + 1, 1]
        frames.append(
            go.Frame(data=[go.Scatter(x=x_new, y=y_new, mode='lines', name='Sine Wave')]))

    fig.frames = frames
    animation_settings = dict(frame=dict(
        duration=50 / speed, redraw=True), fromcurrent=True)

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
                    dict(count=10, label="10s",
                         step="second", stepmode="backward"),
                    dict(count=1, label="1m", step="minute", stepmode="backward"),
                    dict(count=10, label="10m",
                         step="minute", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="linear"
        )
    )


def change_color(color_dropdown):
    if color_dropdown == "Red":
        line_color = 'red'
        return line_color
    elif color_dropdown == "Green":
        line_color = 'green'
        return line_color
    elif color_dropdown == "Yellow":
        line_color = 'yellow'
        return line_color
    else:
        line_color = 'blue'
        return line_color


with col1:
    # Upload file
    file = st.file_uploader("Please upload a file", type=[
                            "csv"], key="file_upload_1")
    color = st.selectbox("Change 1st signal Color", options=[
        "Blue", "Red", "Green", "Yellow"])

    # Read data and plot dynamic graph
    if file is not None:
        data = pd.read_csv(file)
        fig = createfig(data, color)
        y = data.iloc[:, 1]
        mean = np.mean(y)
        std = np.std(y)
        statistics = f"The mean is: {mean}The Standard Devation is : {std}"
        st.write("The mean is :", mean,
                 "The Standard Deviation is :", std)
        animate(data, fig)
        st.plotly_chart(fig, use_container_width=True)
        if st.button("save as PDF"):
            name = "signal1"
            save_as_pdf(statistics, fig, name)


with col2:
    # Upload file
    file1 = st.file_uploader("Please upload a file", type=[
                             "csv"], key="file_upload_2")
    color1 = st.selectbox("Change 2nd signal Color", options=[
        "Blue", "Red", "Green", "Yellow"])
    # Read data and plot dynamic graph
    if file1 is not None:
        data1 = pd.read_csv(file1)
        fig = createfig(data1, color1)
        y = data1.iloc[:, 1]
        mean1 = np.mean(y)
        std1 = np.std(y)
        statistics = f"The mean is: {mean1}The Standard Deviation is : {std1}"
        st.write("The mean is :", mean1,
                 "The Standard Deviation is :", std1)

        animate(data1, fig)
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Save as PDF"):
            name1 = "signal2"
            save_as_pdf(statistics, fig, name1)