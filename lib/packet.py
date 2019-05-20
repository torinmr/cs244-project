class Packet:
    # input_port, output_port : Integer
    def __init__(self, input_port, output_port, packet_size=1):
        self.input_port = input_port
        self.output_port = output_port
        self.time_arrive = -1
        self.time_in_queue = 0
        self.packet_size = packet_size

    def received_packet(self, time_arrive):
        self.time_arrive = time_arrive
