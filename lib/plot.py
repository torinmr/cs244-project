import matplotlib.pyplot as plt
import numpy as np
from typing import List, AnyStr


# y is a 2d array of shape (num_line, len(x))
def draw_plot(x, y: np.ndarray, legends: List[AnyStr], ylim=None, figure_index=0, scale=None):
    assert y.shape[1] == len(x)
    assert len(legends) == y.shape[0]

    plt.figure(figure_index)
    for i in range(y.shape[0]):
        plt.plot(x, y[i])

    if ylim is not None:
        axes = plt.axes()
        axes.set_ylim(ylim)
    if scale is not None:
        plt.axes().set_yscale(scale)

    plt.legend(legends, loc='upper left')
    plt.show()
