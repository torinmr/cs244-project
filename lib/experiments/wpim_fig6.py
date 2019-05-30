from lib.output_contention_input_generator import OutputContentionInputGenerator
from lib.pim import PimSwitch
from lib.statistical import StatisticalSwitch
from lib.wpim import WPimSwitch
from lib.plot import draw_plot
import numpy as np

loads = np.linspace(0.05, 1, 19)
credit = np.array([[100, 0, 0, 0], [200, 0, 0, 0], [300, 0, 0, 0], [400, 0, 0, 0]])
credit_stat = np.array([[1], [2], [3], [4]])

data = [np.zeros((4, len(loads))) for _ in range(3)]
total_run = 10000

for l, load in enumerate(loads):
    switches = [PimSwitch(4, 4), StatisticalSwitch(4, 1, credit_stat, 10), WPimSwitch(4, 4, credit, frame_length=1000)]
    for i, switch in enumerate(switches):
        gen = OutputContentionInputGenerator(switch, load, 4, 0, [0, 1, 2, 3])
        gen.run(total_run)

        bandwidth_usage = switch.input_output_cnt[:, 0]
        normalized_bandwidth = bandwidth_usage / total_run

        for j in range(4):
            data[i][j][l] = normalized_bandwidth[j]

for i, d in enumerate(data):
    draw_plot(loads, d, [str(i) for i in range(4)], ylim=[0, 1], figure_index=i, spacing=0.1)
