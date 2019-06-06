import matplotlib.pyplot as plt
import numpy as np
from typing import List, AnyStr
from matplotlib.ticker import MultipleLocator


# y is a 2d array of shape (num_line, len(x))
def draw_plot(x, y: np.ndarray, legends: List[AnyStr], ylim=None, figure_index=0, scale=None, spacing=None, title=None,
              xlabel=None, ylabel=None):
    assert y.shape[1] == len(x)
    assert len(legends) == y.shape[0]

    plt.figure(figure_index)
    for i in range(y.shape[0]):
        plt.plot(x, y[i], 'o-')

    if spacing:
        minorLocator = MultipleLocator(spacing)
        plt.axes().yaxis.set_minor_locator(minorLocator)
        plt.axes().xaxis.set_minor_locator(minorLocator)
        plt.axes().grid(which='both', axis='both')

    if ylim is not None:
        axes = plt.axes()
        axes.set_ylim(ylim)
    if scale is not None:
        plt.axes().set_yscale(scale)
        plt.grid(True, which="both", ls="-")

    if title is not None:
        plt.title(title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    plt.legend(legends, loc='upper left')
    return plt