import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from fpdf import FPDF
from plotly.subplots import make_subplots


st.set_page_config(page_title="DSP Signal processing", layout="wide")
st.title("DSP Signal Viewer")

col1, col2 = st.columns(2)


def getstatictics(data):
    datastats = data.iloc[:, 1]
    mean = np.around(np.mean(datastats), decimals=2)
    std = np.around(np.std(datastats), decimals=2)
    statistics = f"Mean: {mean} \n\n\n\nStandard Deviation: {std}"
    return statistics


def Extractdata(file, num_points):
    data = pd.read_csv(file)
    x = data.iloc[:num_points, 0]
    y = data.iloc[:num_points, 1]
    return data, x, y


def ViewSignal(num_points, figure, frame_index):
    # Add a trace for the selected data frame
    x_static = data.iloc[frame_index - num_points:frame_index, 0]
    y_static = data.iloc[frame_index - num_points:frame_index, 1]
    figure.add_trace(go.Scatter(x=x_static, y=y_static, mode='lines', name='Static Signal', visible=False))


def save_as_pdf(statistics, fig, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', '', 15)
    # save the signal as pdf
    pio.write_image(fig, 'figure.png')
    # set name for the pdf
    pdf_file = f'{file_name}.pdf'
    # add image to pdf
    pdf.image('figure.png', x=50, y=50, w=100)
    # add statistics to pdf
    pdf.cell(0, 20, f'{statistics} ', align='C')
    # save the pdf
    pdf.output(f'{pdf_file}', 'F')


def createfig(data, color_dropdown, xdata, ydata):
    plot_spot = st.empty()
    ymax = max(data.iloc[:, 1]) + 1
    ymin = min(data.iloc[:, 1]) - 1

    change_color(color_dropdown)
    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=xdata, y=ydata, mode='lines',
                             name='Signal', line_color=color_dropdown))
    return fig


def createlinkedfig(data, data1, color_dropdown, xdata, ydata, xdata1, ydata1):
    plot_spot = st.empty()
    ymax = max(data.iloc[:, 1]) + 1
    ymin = min(data.iloc[:, 1]) - 1
    ymax1 = max(data1.iloc[:, 1]) + 1
    ymin1 = min(data1.iloc[:, 1]) - 1
    if ymax > ymax1:
        ymaxgraph = ymax
    else:
        ymaxgraph = ymax1

    if ymin < ymin1:
        ymingraph = ymin
    else:
        ymingraph = ymin1

    y_range = (ymingraph, ymaxgraph)
    figlink = make_subplots(rows=2, cols=1, specs=[[{}], [{}]], shared_xaxes=True)
    figlink.add_traces([
        go.Scatter(x=xdata, y=ydata, mode='lines', name='Signal1', line_color=color_dropdown),
        go.Scatter(x=xdata1, y=ydata1, mode='lines', name='Signall2', line_color=color_dropdown)
    ], rows=[1, 2], cols=[1, 1])

    if y_range is not None:
        figlink.update_yaxes(range=y_range, row=1, col=1)
        figlink.update_yaxes(range=y_range, row=2, col=1)

    return figlink


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

    initial_frame = go.Frame(
        data=[go.Scatter(x=data.iloc[:points, 0], y=data.iloc[:points, 1], mode='lines', name='Signal')])

    fig.update_layout(
        title='Dynamic Signal Plot',
        xaxis_title='Time (s)',
        yaxis_title='Amplitude',
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                direction='left',  # Set the direction to 'left' for horizontal arrangement
                buttons=[
                    dict(
                        label='&#9654; / &#9724;',  # Play/Pause icon (right-facing triangle and two vertical bars)
                        method='animate',
                        args2= [None, animation_settings],
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate",
                                           transition=dict(duration=0))]
                    ),
                    dict(
                        label='&#8630;',  # Restart icon (rotating arrow)
                        method='animate',
                        args=[[initial_frame], animation_settings]
                    ),
                    dict(
                        label='&#9658;&#9658;',  # Speed up icon (double right-facing triangle)
                        method='animate',
                        args=[None, dict(frame=dict(duration=15, redraw=True), fromcurrent=True)]
                    ),
                    dict(
                        label='&#9668;&#9668;',  # Slow down icon (double left-facing triangle)
                        method='animate',
                        args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
                    ),
                    dict(
                        label='Hide',  # Hide icon (eye with slash)
                        method='update',
                        args=[{'visible': False}, {'title': 'Signal Hidden'}],
                        args2=[{'visible': True}, {'title': 'Signal'}]
                    ),
                    dict(
                        label='Show Frame',  # Show Static Signal icon (eye and eye with slash)
                        method='update',
                        args=[{'visible': [False, True]}],
                        args2=[{'visible': [True, False]}]
                    )
                ],
                x=0.65,  # Adjust the x position of the buttons (0.1 represents 10% from the left)
                y=-0.18  # Adjust the y position of the buttons (negative value to position below the graph)
            )
        ]
    )



def LinkedSignalSlider(data1, data2, fig, num_points):
    if len(data1) > len(data2):
        slider = len(data1)
    else:
        slider = len(data2)
    frame_index3 = st.slider('Select data frame to display:', 0, slider)
    x_static = data.iloc[frame_index3 - num_points:frame_index3, 0]
    y_static = data.iloc[frame_index3 - num_points:frame_index3, 1]
    x_static1 = data1.iloc[frame_index3 - num_points:frame_index3, 0]
    y_static1 = data1.iloc[frame_index3 - num_points:frame_index3, 1]

    # Add static signal traces to subplots
    fig.add_trace(go.Scatter(x=x_static, y=y_static, mode='lines', name='Signal 1 (Static)', visible=False), row=1,
                  col=1)
    fig.add_trace(go.Scatter(x=x_static1, y=y_static1, mode='lines', name='Signal 2 (Static)', visible=False), row=2,
                  col=1)


def Linking(data, data1, figlink, points, speed=1):
    frames = []
    for i in range(points, len(data)):
        x_new = data.iloc[i - points:i, 0]
        y_new = data.iloc[i - points:i, 1]
        x_new1 = data1.iloc[i - points:i, 0]
        y_new1 = data1.iloc[i - points:i, 1]
        frames.append(
            go.Frame(data=[go.Scatter(x=x_new, y=y_new, mode='lines', name=' Signal1'),
                           go.Scatter(x=x_new1, y=y_new1, mode='lines', name='Signal2')]))
    figlink.frames = frames
    animation_settings = dict(frame=dict(
        duration=50 / speed, redraw=True), fromcurrent=True)

    initial_frames = [
        go.Frame(data=[go.Scatter(x=data.iloc[:points, 0], y=data.iloc[:points, 1], mode='lines', name='Signal')]),
        go.Frame(data=[go.Scatter(x=data1.iloc[:points, 0], y=data1.iloc[:points, 1], mode='lines', name='y=x')])
    ]
    figlink.update_layout(title='Linked Signals', xaxis_title='Time (s)', yaxis_title='Amplitude')
    figlink.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                direction='left',  # Set the direction to 'left' for horizontal arrangement
                buttons=[
                    dict(
                        label='&#9654; / &#9724;',  # Play/Pause icon (right-facing triangle and two vertical bars)
                        method='animate',
                        args2= [None, animation_settings],
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate",
                                           transition=dict(duration=0))]
                    ),
                    dict(
                        label='&#8630;',
                        method='animate',
                        args=[[initial_frames[0], initial_frames[1]], animation_settings]  # Use initial frames
                    ),

                    dict(
                        dict(label='&#9658;&#9658;', method='animate',
                             args=[None, dict(frame=dict(duration=10, redraw=True), fromcurrent=True)])
                    ),
                    dict(
                        dict(label='&#9668;&#9668;', method='animate',
                             args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)])
                    ),
                    dict(
                        label='Hide',
                        method='update',
                        args=[{'visible': False}, {'title': 'Signal Hidden'}],
                        args2=[{'visible': True}, {'title': 'Signal'}]
                    ),
                    dict(label='Show frame', method='update',
                         args=[{'visible': [False, False, True, True]}],
                         args2=[{'visible': [True, True, False, False]}]
                         )
                ],
                x=0.7,  # Adjust the x position of the buttons (0.1 represents 10% from the left)
                y=-0.18  # Adjust the y position of the buttons (negative value to position below the graph)
            )
        ]
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

#--------------------------------------------------------------------------------------------------
#main


Link = st.checkbox("Link")

with col1:
    # Upload file
    file = st.file_uploader("Please upload a file", type=[
        "csv"], key="file_upload_1")
    # Read data and plot dynamic graph
    if file is not None:
        color = st.selectbox("Change Color", options=[
            "Blue", "Red", "Green", "Yellow"])
        num_points = 30
        data, x, y = Extractdata(file, num_points)
        statistics = getstatictics(data)
        # # st.write(statistics)
        frame_index = st.slider('Select data frame to display:', 0, len(data), key=1)
        fig = createfig(data, color, x, y)
        animate(data, fig, num_points)
        ViewSignal(num_points, fig, frame_index)
        st.plotly_chart(fig, use_container_width=True)
        x_all = data.iloc[:, 0]
        y_all = data.iloc[:, 1]
        ima = createfig(data, 'blue', x_all, y_all)
        if st.button("Save as PDF"):
            name = "signal1"
            save_as_pdf(statistics, ima, name)

with col2:
    # Upload file
    file1 = st.file_uploader("Please upload a file", type=[
        "csv"], key="file_upload_2")
    # Read data and plot dynamic graph
    if file1 is not None:
        color1 = st.selectbox("Change  Color", options=[
            "Blue", "Red", "Green", "Yellow"])
        data1, x1, y1 = Extractdata(file1, num_points)
        statistics2 = getstatictics(data1)
        # st.write(statistics2)
        frame_index1 = st.slider('Select data frame to Display:', 0, len(data1), key=2)
        fig1 = createfig(data1, color1,x1 ,y1)
        animate(data1, fig1, num_points)
        ViewSignal(num_points, fig1, frame_index1)
        st.plotly_chart(fig1, use_container_width=True)
        x_all1 = data1.iloc[:, 0]
        y_all1 = data1.iloc[:, 1]
        ima1 = createfig(data1, 'blue', x_all1, y_all1)
        if st.button("Save as PDF "):
            name1 = "signal2"
            save_as_pdf(statistics, ima1, name1)

if Link:
    color3 = st.selectbox("Change Color", options=[
        "Blue", "Red", "Green", "Yellow"], key=3)
    figlinker = createlinkedfig(data, data1, color3, x, y, x1, y1)
    LinkedSignalSlider(data, data1, figlinker, 30)
    Linking(data, data1, figlinker, 30)
    st.plotly_chart(figlinker, use_container_width=True)
