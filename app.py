import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import plotly.io as pio
from fpdf import FPDF
import io
from PIL import Image
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt


st.set_page_config(page_title="DSP Signal processing", layout="wide")
st.title("DSP signal")

col1, col2 = st.columns(2)
global data
global data1
global file
global file1
global x
global y
global x1
global y1


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
    fig = go.Figure(go.scatter(x=x, y=y, ))
    return fig.show()


def save_as_pdf(statistics, fig, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    # save the signal as pdf
    pio.write_image(fig, 'figure.png')
    # set name for the pdf
    pdf_file = f'{file_name}.pdf'
    # add image to pdf
    pdf.image('figure.png', x=10, y=10, w=100)
    # add statistics to pdf
    pdf.cell(0, 20, f'The Statistics:{statistics} ', ln=1)
    # save the pdf
    pdf.output(f'{pdf_file}', 'F')


def createfig(data, color_dropdown, xdata, ydata):
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


# def update_animations(fig1, fig2):
#     # get the active button state
#     button_state = fig1.layout.updatemenus[0].buttons[0].args[1]['frame']['redraw']
#
#     # update the animation frames for both figures
#     if button_state:
#         fig1.update(frames=frames)
#         fig2.update(frames=frames)


def Linking(data, data1, points, speed=1):
    frames = []
    for i in range(points, len(data)):
        x_new = data.iloc[i - points:i, 0]
        y_new = data.iloc[i - points:i, 1]
        x_new1 = data1.iloc[i-points:i, 0]
        y_new1 = data1.iloc[i-points:i, 1]
        # frames = go.Frame(
        # data=[
        #     go.Scatter(x=x_new, y=y_new, mode='lines', name='sin wave'),
        #     go.Scatter(x=x_new1, y=y_new1, mode='lines', name='y=x')])
        frames.append(
            go.Frame(data=[go.Scatter(x=x_new, y=y_new, mode='lines', name=' Signal'),
                           go.Scatter(x=x_new1, y=y_new1, mode='lines', name='y=x')]))
    figlink = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True)
    figlink.add_traces([
        go.Scatter(x=x, y=y, mode='lines', name='sin wave'),
        go.Scatter(x=x1, y=y1, mode='lines', name='y=x')
    ], rows=[1, 1], cols=[1, 2])
    figlink.frames = frames
    animation_settings = dict(frame=dict(
        duration=50 / speed, redraw=True), fromcurrent=True)
    figlink.update_layout(title='Dynamic Signal Plot', xaxis_title='Time (s)', yaxis_title='Amplitude')
    figlink.update_layout(
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
    return figlink



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


Link = st.checkbox("Link")

with col1:
    # Upload file
    file = st.file_uploader("Please upload a file", type=[
        "csv"], key="file_upload_1")
    color = st.selectbox("Change 1th signal Color", options=[
        "Blue", "Red", "Green", "Yellow"])

    # Read data and plot dynamic graph
    if file is not None:
        data = pd.read_csv(file)
        num_points = 30  # Number of data points to display at each frame
        x = data.iloc[:num_points, 0]
        y = data.iloc[:num_points, 1]
        datastats = data.iloc[:, 1]
        mean = np.mean(datastats)
        std = np.std(datastats)
        statistics = f"The mean is: {mean}The Standerd Devision  is : {std}"
        st.write("The mean is :", mean,
                 "The Standerd Devision  is :", std)
        frame_index = st.slider('Select data frame to display:', 0, len(data) - 1)

        # Add a trace for the selected data frame
        x_static = data.iloc[frame_index - num_points:frame_index, 0]
        y_static = data.iloc[frame_index - num_points:frame_index, 1]
        fig = createfig(data, color, x, y)
        animate(data, fig, num_points)
        fig.add_trace(go.Scatter(x=x_static, y=y_static, mode='lines', name='Static Signal', visible=True))

        # Define the layout for the static signal trace

        st.plotly_chart(fig, use_container_width=True)
        ima = createfig(data, 'blue', x_static, y_static)
        if st.button("save as PDF"):
            name = "signal1"
            save_as_pdf(statistics, ima, name)

with col2:
    # Upload file
    file1 = st.file_uploader("Please upload a file", type=[
        "csv"], key="file_upload_2")
    color1 = st.selectbox("Change 2th signal Color", options=[
        "Blue", "Red", "Green", "Yellow"])
    # Read data and plot dynamic graph
    if file1 is not None:
        data1 = pd.read_csv(file1)
        num_points = 30
        x1 = data1.iloc[:num_points, 0]
        y1 = data1.iloc[:num_points, 1]
        stats = data1.iloc[:, 1]
        mean1 = np.mean(stats)
        std1 = np.std(stats)
        statistics = f"The mean is: {mean1}The Standerd Devision  is : {std1}"
        st.write("The mean is :", mean1,
                 "The Standerd Devision  is :", std1)
        frame_index = st.slider('Select data frame to Display:', 0, len(data1) - 1)

        # Add a trace for the selected data frame
        x_static1 = data1.iloc[frame_index - num_points:frame_index, 0]
        y_static1 = data1.iloc[frame_index - num_points:frame_index, 1]
        fig1 = createfig(data1, color1, x1, y1)
        animate(data1, fig1, num_points)
        fig.add_trace(go.Scatter(x=x_static1, y=y_static1, mode='lines', name='Static Signal', visible=True))

        st.plotly_chart(fig1, use_container_width=True)
        ima1 = createfig(data1, 'blue', x_static1, y_static1)
        if st.button("Save as PDF"):
            name1 = "signal2"
            save_as_pdf(statistics, ima1, name1)

if Link:
    figlink = Linking(data, data1, 30)
    st.plotly_chart(figlink, use_container_width=True)