import random

from lib.base_input_generator import BaseInputGenerator
from lib.packet import Packet

class UniformInputGenerator(BaseInputGenerator):
    """An input generator which assumes each input wants to talk to each output
       with equal probability."""
    
    def __init__(self, switch, load=-1):
        """Load is the probability that a packet arrives at each input port at a given timestep. 
        
        It is allowed to range between 0 and 1, inclusive.
        """
        assert load >= 0.0
        assert load <= 1.0
        super().__init__(switch)
        self.load = load
        
    def generate_packets(self, unused_step):
        for i in range(self.switch.num_input):
            if random.random() < self.load:
                j = random.randrange(self.switch.num_output)
                self.switch.receive(Packet(i, j))