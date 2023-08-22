import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

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


st.title("Signal Viewer")
st.markdown("---")
# Read the csv file and store the data in a list
file = st.file_uploader("Please upload a file", type=["csv"])
if file is not None:
    data = pd.read_csv(file)
    data = data.iloc[:, :]
    # st.write(file)
    X_values = list(data.iloc[:, 0])
    Y_values = list(data.iloc[:, 1])
    # limit_values = list(data.iloc[:, 0])
    # limit1_values = list(data.iloc[:, 1])
    x = np.asarray(X_values)
    y = np.asarray(Y_values)
    # y_sin = np.asarray(limit1_values)
    # y_cos = np.sin(x)
    fig = plt.figure()
    ax1 = plt.subplot()
    # ax2 = plt.subplot(2, 1, 2)
    SkipIT = 70

    def init_func():
        ax1.set_xlabel("Amplitude")
        ax1.set_ylabel("Time in uS")
        ax1.set_xlim((x[0], x[-1]))
        ax1.set_ylim((-1, 1))

    def update_plot(i):
        ax1.clear()
        ax1.plot(x[i : i + SkipIT], y[i : i + SkipIT], color="b")

    # ax1.scatter(x[i], y_sin[i], marker='o', color='r')
    # ax2.plot(x[i:i+data_skip], y_cos[i:i+data_skip], color='k')
    # ax2.scatter(x[i], y_cos[i], marker='o', color='r')

    anim = FuncAnimation(
        fig, update_plot, frames=130, init_func=init_func, interval=100
    )
    components.html(anim.to_jshtml(), height=1000)


# data = pd.read_csv("test data.csv", skiprows=1)
# data = data.iloc[:, :]
# print(data)
# data=list(data)
# print(data)
# Extract the x and y values from the data list


# x = np.asarray(limit_values)
# y = np.asarray(limit1_values)
# y_sin = np.asarray(limit1_values)
# y_cos = np.sin(x)

# fig = plt.figure()
# ax1 = plt.subplot(2, 1, 1)
# ax2 = plt.subplot(2, 1, 2)

# data_skip = 70


# def init_func():
#     ax1.clear()
#     ax2.clear()
#     ax1.set_xlabel('pi')
#     ax1.set_ylabel('sin(pi)')
#     ax2.set_xlabel('pi')
#     ax2.set_ylabel('cos(pi)')
#     ax1.set_xlim((x[0], x[-1]))
#     ax1.set_ylim((-1, 1))
#     ax2.set_xlim((x[0], x[-1]))
#     ax2.set_ylim((-1, 1))


# def update_plot(i):
#     ax1.clear()
#     ax1.plot(x[i:i+data_skip], y_sin[i:i+data_skip], color='k')
#     # ax1.scatter(x[i], y_sin[i], marker='o', color='r')
#     ax2.plot(x[i:i+data_skip], y_cos[i:i+data_skip], color='k')
#     # ax2.scatter(x[i], y_cos[i], marker='o', color='r')


# anim = FuncAnimation(fig,
#                      update_plot,
#                      frames=130,
#                      init_func=init_func,
#                      interval=100)
# components.html(anim.to_jshtml(), height=1000)
