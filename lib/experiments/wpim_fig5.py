from lib.client_server_input_generator import ClientServerInputGenerator
from lib.pim import PimSwitch
from lib.statistical import StatisticalSwitch
from lib.wpim import WPimSwitch
from lib.plot import draw_plot
import numpy as np
from tqdm import tqdm

loads = np.linspace(0.05, 0.95, 18)
credit = np.zeros((16, 16))

# 95% of server traffic distributed to 12 clients, 5% to other servers
# 40% of client traffic goes to 4 servers. 60% goes to clients

# Server credits
for i in range(4):
    for j in range(16):
        if j < 4 and j != i:
            credit[i][j] = 1000 * 0.05 / 3
        elif j >= 4:
            credit[i][j] = 1000 * 0.95 / 12

# Client credits
for i in range(4, 16):
    for j in range(16):
        if j < 4:
            credit[i][j] = 1000 * 0.1
        elif j >= 4 and j != i:
            credit[i][j] = 1000 * 0.6 / 11

total_run = 20000

delay_per_load = np.zeros((4, len(loads)))

for num_iter in range(1, 5):
    for l, load in enumerate(tqdm(loads)):
        switch = WPimSwitch(16, 16, credit, frame_length=1000, num_iteration=num_iter)
        gen = ClientServerInputGenerator(switch, L=load)
        gen.run(total_run)

        # Compute the average queueing delay of packets.
        delays = []
        for packet in switch.processed_packets:
            delays.append(packet.time_in_queue)

        average_delay = np.average(delays)
        delay_per_load[num_iter - 1][l] = average_delay

print(delay_per_load)
draw_plot(loads, delay_per_load, [str(i) + " iterations" for i in range(1, 5)], scale="log")