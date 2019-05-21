class BaseInputGenerator:
    def __init__(self, switch):
        """Build a new input generator for the given switch."""
        self.switch = switch
        
    def run(self, num_steps):
        """Run the input generator for num_steps steps."""
        step = 0
        while step < num_steps:
            self.generate_packets(step)
            self.switch.step()
            step += 1
        
    def generate_packets(self, step):
        """Generate the packets for the provided timestep.
        
        In general, should call self.switch.receive() muliple times."""
        raise NotImplementedError()