from base_switch import BaseSwitch
from packet import Packet
import random


class PimSwitch(BaseSwitch):

    def __init__(self, num_input, num_output, num_iteration=4):
        super().__init__(num_input, num_output)
        self.num_iteration = num_iteration

    def schedule(self):
        matched_inputs, matched_outputs = [], []
        final_decision = {}

        def run_pim_once():
            # Step 1: Send requests to output queues.
            received_requests = [[] for _ in range(self.num_output)]
            for input in range(self.num_input):
                if input in matched_inputs:
                    continue
                for output in range(self.num_output):
                    if len(self.input_to_output_queue[(input, output)]) != 0:
                        received_requests[output].append(input)

            # Step 2: Choose one of the request.
            reqs_to_inputs = {}
            for output in range(self.num_output):
                if output in matched_outputs:
                    continue
                if len(received_requests[output]) > 0:
                    chosen_input = random.choice(received_requests[output])
                    reqs_to_inputs[chosen_input] = reqs_to_inputs.get(
                        chosen_input, []) + [output]
            current_decision = {}
            # Step 3: Input chooses one of the output queue
            for input in reqs_to_inputs:
                output = random.choice(reqs_to_inputs[input])
                matched_inputs.append(input)
                matched_outputs.append(output)

                final_decision[input] = output

        for _ in range(self.num_iteration):
            run_pim_once()

        return final_decision.items()


p = PimSwitch(16, 16)
for i in range(16):
    for j in range(16):
        p.receive(Packet(i, j))

print(p.schedule())
