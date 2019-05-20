from base_switch import BaseSwitch
from packet import Packet
import random
import numpy as np


class WPimSwitch(BaseSwitch):

    def __init__(self,
                 num_input,
                 num_output,
                 credit: np.ndarray,
                 frame_length,
                 num_iteration=4):
        super().__init__(num_input, num_output)
        self.num_iteration = num_iteration
        self.frame_length = frame_length

        self.credit = credit
        assert credit.shape == (num_input, num_output)

        self.current_time = 0
        self.sent_credits = np.zeros(credit.shape)

    def schedule(self):
        matched_inputs, matched_outputs = [], []
        final_decision = {}

        def remove_masked_elements(reqs, output):
            masked_reqs = []
            for input in reqs:
                if self.sent_credits[
                        input][output] + self.get_outstanding_packet(
                            input,
                            output).packet_size <= self.credit[input][output]:
                    masked_reqs.append(input)
            return masked_reqs

        def run_wpim_once():
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
                    # Mask
                    masked_reqs = remove_masked_elements(
                        received_requests[output], output)
                    if len(masked_reqs) > 0:
                        chosen_input = random.choice(masked_reqs)
                        reqs_to_inputs[chosen_input] = reqs_to_inputs.get(
                            chosen_input, []) + [output]

            current_decision = {}
            # Step 3: Input chooses one of the output queue
            for input in reqs_to_inputs:
                output = random.choice(reqs_to_inputs[input])
                matched_inputs.append(input)
                matched_outputs.append(output)

                final_decision[input] = output

                # Increate the sent credits.
                self.sent_credits[input][output] += self.get_outstanding_packet(
                    input, output).packet_size

        for _ in range(self.num_iteration):
            run_wpim_once()

        self.current_time += 1
        if self.current_time >= self.frame_length:
            self.current_time = 0
            self.sent_credits = np.zeros(self.credit.shape)

        return final_decision.items()


credit = np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]])
p = WPimSwitch(4, 4, credit, 6, 4)
for i in range(4):
    for j in range(4):
        for _ in range(10):
            p.receive(Packet(i, j))

print(p.schedule())
print(p.schedule())
print(p.schedule())
print(p.schedule())
print(p.schedule())
print(p.schedule())
