import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import plotly.io as pio
from fpdf import FPDF

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


def image(data):
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]
    fig = go.Figure(go.scatter(x=x, y=y,))
    return fig.show()


def save_as_pdf(statistics, fig, file_name):
    pdf = FPDF()
    pdf.add_page()
    # save the signal as pdf
    pio.write_image(fig, 'figure.png')
    # set name for the pdf
    pdf_file = f'{file_name}.pdf'
    # add image to pdf
    pdf.image('figure.png', x=10, y=10, w=100)
    # add statistics to pdf
    pdf.cell(0, 20, f'The Statistics://n{statistics} ', ln=1)
    # save the pdf
    pdf.output(f'{pdf_file}', 'F')


def createfig(data, color_dropdown, xdata , ydata):
    plot_spot = st.empty()
    ymax = max(data.iloc[:, 1]) + 1
    ymin = min(data.iloc[:, 1]) - 1
    colors = change_color(color_dropdown)
    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=xdata, y=ydata, mode='lines',
                  name='Signal', line_color=color_dropdown))
    return fig


def animate(data, fig, points, speed=1):
    frames = []
    for i in range(points, len(data)):
        x_new = data.iloc[i - points:i, 0]
        y_new = data.iloc[i - points:i, 1]
        frames.append(
            go.Frame(data=[go.Scatter(x=x_new, y=y_new, mode='lines', name=' Signal')]))

    fig.frames = frames
    animation_settings = dict(frame=dict(
        duration=50 / speed, redraw=True), fromcurrent=True)

    fig.update_layout(title='Dynamic Signal Plot', xaxis_title='Time (s)', yaxis_title='Amplitude')
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

                        args=[None, animation_settings]
                    ),

                    dict(
                        label='Fast Up',
                        method='relayout',
                        args=[{'xaxis.range': None, 'yaxis.range': None,
                               'frame.duration': animation_settings['frame']['duration'] / 2}]
                    ),
                    dict(
                        label='Slow Down',
                        method='relayout',
                        args=[{'xaxis.range': None, 'yaxis.range': None,
                               'frame.duration': animation_settings['frame']['duration'] * 2}]
                    ),
                    dict(
                        label='Hide',
                        method='update',
                        args=[{'visible': False}, {'title': 'Signal Hidden'}]

                    ),
                    dict(
                        label='Show',
                        method='update',
                        args=[{'visible': True}, {'title': 'Signal'}]
                    ),
                    dict(label='Hide Static Signal', method='update',
                                       args=[{'visible': [True, False]}]),
                    dict(label='Show Static Signal', method='update',
                                       args=[{'visible': [False, True]}])
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
        num_points = 30  # Number of data points to display at each frame
        x = data.iloc[:num_points, 0]
        y = data.iloc[:num_points, 1]
        fig = createfig(data, color, x, y)
        datastats = data.iloc[:, 1]
        mean = np.mean(datastats)
        std = np.std(datastats)
        statistics = f"The mean is: {mean}The Standard Deviation is : {std}"
        st.write("The mean is :", mean,
                 "The Standard Deviation is :", std)
        animate(data, fig, num_points)
        frame_index = st.slider('Select data frame to display:', 0, len(data) - 1)

        # Add a trace for the selected data frame
        x_static = data.iloc[frame_index - num_points:frame_index, 0]
        y_static = data.iloc[frame_index - num_points:frame_index, 1]
        fig.add_trace(go.Scatter(x=x_static, y=y_static, mode='lines', name='Static Signal', visible=True))

        # Define the layout for the static signal trace

        st.plotly_chart(fig, use_container_width=True)
        if st.button("save as PDF"):
            name = "signal1"
            # save_as_pdf(statistics, fig, name)


with col2:
    # Upload file
    file1 = st.file_uploader("Please upload a file", type=[
        "csv"], key="file_upload_2")
    color1 = st.selectbox("Change 2nd signal Color", options=[
        "Blue", "Red", "Green", "Yellow"])
    # Read data and plot dynamic graph
    if file1 is not None:
        data1 = pd.read_csv(file1)
        x1 = data1.iloc[:num_points, 0]
        y1 = data1.iloc[:num_points, 1]
        fig = createfig(data1, color1, x1, y1)
        stats = data1.iloc[:, 1]
        mean1 = np.mean(stats)
        std1 = np.std(stats)
        statistics = f"The mean is: {mean1}The Standard Deviation is : {std1}"
        st.write("The mean is :", mean1,
                 "The Standard Deviation is :", std1)
        animate(data1, fig, num_points)

        frame_index = st.slider('Select data frame to Display:', 0, len(data) - 1)

        # Add a trace for the selected data frame
        x_static1 = data1.iloc[frame_index - num_points:frame_index, 0]
        y_static1 = data1.iloc[frame_index - num_points:frame_index, 1]
        fig.add_trace(go.Scatter(x=x_static, y=y_static, mode='lines', name='Static Signal', visible=True))

        st.plotly_chart(fig, use_container_width=True)
        if st.button("Save as PDF"):
            name1 = "signal2"
            save_as_pdf(statistics, ima, name1)