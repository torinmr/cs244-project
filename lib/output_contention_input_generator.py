import random

from lib.base_input_generator import BaseInputGenerator
from lib.packet import Packet

class OutputContentionInputGenerator(BaseInputGenerator):
    """An input generator which simulates multiple inputs trying to talk to one output."""
    
    def __init__(self, switch, load_per_input=-1, num_contending_inputs=-1,
                 output_port=None, input_ports=None):
        """load_per_input is the probability that a packet arrives at each input port at
        a given timestep. 
        
        num_contending_inputs is the number of inputs trying to talk to one output port.
        
        load_per_input must be between 0.0 and 1.0 inclusive, and num_contending_inputs
        must be less than or equal to the number of input ports on the switch. Which exact
        input and output ports are used will be randomly determined, though they can be
        explicitly provided to avoid this.
        
        If load * num_contending_inputs < 1, then there should be no contention.
        """
        super().__init__(switch)
        
        assert load_per_input >= 0.0
        assert load_per_input <= 1.0
        
        self.load_per_input = load_per_input
        if output_port is not None:
            self.output_port = output_port
        else:
            self.output_port = random.randrange(self.switch.num_output)
        if input_ports is not None:
            self.input_ports = input_ports
        else:
            assert num_contending_inputs > 0
            assert num_contending_inputs <= self.switch.num_input
            self.input_ports = random.sample(range(self.switch.num_input), num_contending_inputs)

    def generate_packets(self, unused_step):
        for i in self.input_ports:
            if random.random() < self.load_per_input:
                self.switch.receive(Packet(i, self.output_port))