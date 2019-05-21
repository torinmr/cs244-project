import random

from lib.base_input_generator import BaseInputGenerator
from lib.packet import Packet

class ClientServerInputGenerator(BaseInputGenerator):
    """An input generator emulating a client-server workload.
    
    Based on the description in the third paragraph of section III of Stiliadis and Varma:
    
    * S of the switch ports are connected to servers and C are connected to clients.
    * Each client sends X percent of its traffic to each of the servers (total of S * X).
    * Each client divides the remaining 1 - S*X traffic between the other clients.
    * Each server sends Y percent of its traffic evenly divided between the clients (Y / C per client).
    * Each server divides the remaining 1 - Y traffic between the other servers.
    * Each incoming port (whether client or server) sends a packet each time step with probability L.
    
    In their experiment, they had S = 4, C = 12, X = 10%, and Y = 95%.
    """
    
    def __init__(self, switch, L=-1, S=4, C=12, X=0.1, Y=0.95):
        """See comment above for meanings of parameters."""
        super().__init__(switch)
        
        assert 0.0 <= L <= 1.0
        assert switch.num_input == switch.num_output
        assert S + C <= switch.num_input  # Can't have more clients and servers than ports.
        assert 0.0 <= X * S <= 1.0  # Can't allocate more than 100% of client traffic to servers.
        assert 0.0 <= Y <= 1.0  # Can't allocate more than 100% of server traffic to clients.
        self.L = L
        self.S = S
        self.C = C
        self.X = X
        self.Y = Y
        self.servers = list(range(S))
        self.clients = list(range(S, S+C))
        
    def generate_packets(self, unused_step):
        for i in self.servers:
            if random.random() < self.L:
                if random.random() < self.Y:
                    j = random.choice(self.clients)
                else:
                    j = random.choice(self.servers)
                self.switch.receive(Packet(i, j))
                
        for i in self.clients:
            if random.random() < self.L:
                if random.random() < self.X * self.S:
                    j = random.choice(self.servers)
                else:
                    j = random.choice(self.clients)
                self.switch.receive(Packet(i, j))