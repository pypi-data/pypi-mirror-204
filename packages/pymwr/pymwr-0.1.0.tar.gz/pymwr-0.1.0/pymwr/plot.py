import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, HourLocator
from .utils import get_gaps


def plot(temp_data, parameter_name, yaxis_height_limit=10):
    """
    Creates a contour plot of the given parameter for the Microwave Radiometer data

    Args:
    temp_data (DataFrame): the Microwave Radiometer data to be plotted
    parameter_name (str): the name of the parameter to be plotted
    yaxis_height_limit (int): the maximum value of the y-axis

    Returns:
    fig (Figure): the figure object containing the plot
    """

    # Define color range for plotting based on scan angle
    if temp_data['400'].unique()[0] == '401':
        clevs = np.linspace(270, 300, 16, endpoint=True)
    elif temp_data['400'].unique()[0] == '404':
        clevs = np.linspace(40, 100, 7, endpoint=True)
    elif temp_data['400'].unique()[0] == '403':
        clevs = np.linspace(0, .01, endpoint=True)
    elif temp_data['400'].unique()[0] == '402':
        clevs = np.linspace(0, 15, endpoint=True)

    # Remove gaps in data
    temp_data = get_gaps(temp_data)

    # Create figure and plot
    fig = plt.figure(figsize=[25, 5], dpi=200)
    cs_t = plt.contourf(temp_data.index, temp_data.columns, temp_data.astype(float).T, clevs, cmap='turbo', extend='both')
    cs1 = plt.colorbar(cs_t, pad=0.008)
    cs1.ax.tick_params(labelsize=16, length=2)
    plt.xlabel("Datetime (UTC)", fontsize=20)
    plt.ylabel("Height (Km)", fontsize=20)
    plt.title("Microwave Radiometer" + '  ' * 6 + parameter_name + ' ' * 2, fontsize=22)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 3)))  # enter hours difference
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H\n%d%b'))
    plt.gca().xaxis.set_minor_formatter(DateFormatter('%H'))
    plt.tick_params(axis='both', which='major', labelsize=15, direction='out', length=8, width=2)
    plt.tick_params(axis='both', which='minor', labelsize=15, direction='out', length=8, width=2)
    plt.ylim(0, yaxis_height_limit)

    return fig
