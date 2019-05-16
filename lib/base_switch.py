import queue

class BaseSwitch:
    def __init__ (self, num_input, num_output):
        self.num_input = num_input
        self.num_output = num_output
        self.current_time = 0

        # key : (input, output)
        # value : queue
        self.input_to_output_queue = {}

        for i in range(self.num_input):
            for j in range(self.num_output):
                self.input_to_output_queue[(i, j)] = queue.Queue()

    def receive(self, packet):
        assert 0 <= packet.input_port < self.num_input
        assert 0 <= packet.output_port < self.num_output

        self.input_to_output_queue[(packet.input_port, packet.output_port)].put(packet)
        packet.received_packet(self.current_time)

    # returns list of (input, output) pairs you want to pop
    def schedule(self):
        raise NotImplementedError

    # Schedule packets per step.
    def step(self):
        queues_to_pop = self.schedule()
        inputs = set(input for input, _ in queues_to_pop)
        outputs = set(output for _, output in queues_to_pop)

        assert len(inputs) == len(outputs) == len(queues_to_pop)

        for input, output in queues_to_pop:
            processed_packet = self.input_to_output_queue[(input, output)].get()
            processed_packet.time_in_queue = self.current_time - self.time_arrive

        self.current_time += 1

