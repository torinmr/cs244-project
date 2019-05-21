import matplotlib.pyplot as plt
import numpy as np
from typing import List, AnyStr


# y is a 2d array of shape (num_line, len(x))
def draw_plot(x, y: np.ndarray, legends: List[AnyStr], figure_index=0):
    assert y.shape[1] == len(x)
    assert len(legends) == y.shape[0]

    plt.figure(figure_index)
    for i in range(y.shape[0]):
        plt.plot(x, y[i])

    plt.legend(legends, loc='upper left')
    plt.show()
