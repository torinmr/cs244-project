import collections
import numpy as np


class BaseSwitch:

    def __init__(self, num_input, num_output):
        self.num_input = num_input
        self.num_output = num_output
        self.current_time = 0

        # key : (input, output)
        # value : queue
        self.input_to_output_queue = {}

        for i in range(self.num_input):
            for j in range(self.num_output):
                self.input_to_output_queue[(i, j)] = collections.deque()

        # keep track of the number of packets that is forwarded in input->output port
        self.input_output_cnt = np.zeros((self.num_input, self.num_output))

    def receive(self, packet):
        assert 0 <= packet.input_port < self.num_input
        assert 0 <= packet.output_port < self.num_output
        self.input_to_output_queue[(packet.input_port,
                                    packet.output_port)].append(packet)
        packet.received_packet(self.current_time)

    # returns list of (input, output) pairs you want to pop
    def schedule(self):
        raise NotImplementedError()

    # Schedule packets per step.
    def step(self):
        queues_to_pop = self.schedule()
        inputs = set(input for input, _ in queues_to_pop)
        outputs = set(output for _, output in queues_to_pop)

        assert len(inputs) == len(outputs) == len(queues_to_pop)

        for input, output in queues_to_pop:
            processed_packet = self.input_to_output_queue[(input,
                                                           output)].popleft()
            processed_packet.time_in_queue = self.current_time - processed_packet.time_arrive
            self.input_output_cnt[input][output] += 1

        self.current_time += 1

    def get_outstanding_packet(self, input, output):
        if len(self.input_to_output_queue[(input, output)]) == 0:
            raise Exception("Requesting Packet From Empty Queue")

        return self.input_to_output_queue[(input, output)][0]
