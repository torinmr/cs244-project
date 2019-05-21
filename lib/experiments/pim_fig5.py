from lib.uniform_input_generator import UniformInputGenerator
from lib.pim import PimSwitch
from lib.plot import draw_plot
import numpy as np

loads = np.linspace(0.1, 1, 19)
delay_per_load = [[] for _ in range(5)]

for num_iter in range(0, 5):
    for load in loads:
        switch = PimSwitch(16, 16, num_iter)
        gen = UniformInputGenerator(switch, load)

        gen.run(1000)

        # Compute the average queueing delay of packets.
        delays = []
        for packet in switch.processed_packets:
            delays.append(packet.time_in_queue)

        average_delay = np.average(delays)
        delay_per_load[num_iter].append(average_delay)

legends = ["Infinite Iterations"] + ["Iterations : " + str(i) for i in range(1, 5)]
draw_plot(loads, np.array(delay_per_load), legends, [0, 25], 0)