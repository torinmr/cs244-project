from base_switch import BaseSwitch
from packet import Packet
import random
import numpy as np


class StatisticalSwitch(BaseSwitch):

    def __init__(self,
                 num_input,
                 num_output,
                 credit: np.ndarray,
                 num_iteration=4):
        super().__init__(num_input, num_output)
        self.num_iteration = num_iteration

        self.credit = credit
        assert credit.shape == (num_input, num_output)

        self.prob_matrix = np.zeros(credit.shape)
        output_sum = np.sum(credit, axis=0)
        for input in range(num_input):
            for output in range(num_output):
                self.prob_matrix[input][output] = self.credit[input][output] / output_sum[output]

    def schedule(self):
        matched_inputs, matched_outputs = [], []
        final_decision = {}

        def normalize_prob_matrix(reqs, output):
            probs = []
            for input in reqs:
                probs.append(self.prob_matrix[input][output])
            probs = probs / np.sum(probs)
            return probs

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
                    # We have to normalize probabilities based on available input ports.
                    weighted_probs = normalize_prob_matrix(received_requests[output], output)
                    # Choose the input port using the weighted probability.
                    chosen_input = np.random.choice(received_requests[output], p=weighted_probs)

                    reqs_to_inputs[chosen_input] = reqs_to_inputs.get(chosen_input, []) + [output]

            # Step 3: Input chooses one of the output queue
            for input in reqs_to_inputs:
                output = random.choice(reqs_to_inputs[input])
                matched_inputs.append(input)
                matched_outputs.append(output)

                final_decision[input] = output

        for _ in range(self.num_iteration):
            run_wpim_once()

        return final_decision.items()


credit = np.array([[10, 0, 0, 0], [20, 0, 0, 0], [30, 0, 0, 0], [40, 0, 0, 0]])
p = StatisticalSwitch(4, 4, credit)
for i in range(4):
    for _ in range(100):
        p.receive(Packet(i, 0))

for _ in range(100):
    print(p.schedule())
