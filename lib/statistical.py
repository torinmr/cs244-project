from lib.base_switch import BaseSwitch
from lib.packet import Packet
import random
import numpy as np
from scipy.stats import binom


class StatisticalSwitch(BaseSwitch):

    def __init__(self,
                 num_input,
                 num_output,
                 credit: np.ndarray,
                 frame_length=1000,
                 num_iteration=2,
                 run_pim_after=False):

        super().__init__(num_input, num_output)
        self.num_iteration = num_iteration

        self.credit = credit
        assert credit.shape == (num_input, num_output)

        self.prob_matrix = self.credit / np.sum(self.credit, axis=0, keepdims=True)
        
        self.X = frame_length
        self.vg_prob_matrix = np.zeros((num_input, num_output, np.max(self.credit)+1))
        for i in range(num_input):
            for j in range(num_output):
                credits = self.credit[i][j]
                if credits < 1:
                    continue
                probs = binom.pmf(range(credits+1), credits, 1 / self.X) * self.X / credits
                probs[0] = 0
                probs[0] = 1 - sum(probs)
                self.vg_prob_matrix[i][j][:len(probs)] = probs

        self.run_pim_after = run_pim_after

    def schedule(self):
        matched_inputs, matched_outputs = [], []
        final_decision = {}

        def run_sm_once():
            # Step 1: Output queues send request to input queues
            input_reqs = [list() for _ in range(self.num_input)]
            for output in range(self.num_output):
                choice = np.random.choice(list(range(self.num_input)),
                                          p=self.prob_matrix[:, output])
                input_reqs[choice].append(output)

            # Step 2. Interpret each grant as random number
            for input in range(self.num_input):
                if len(input_reqs[input]) == 0:
                    continue
                if input in matched_inputs:
                    continue
                virtual_grants = []  # virtual grant
                for output in input_reqs[input]:
                    credit = self.credit[input][output]
                    vg = np.random.choice(range(credit+1), p=self.vg_prob_matrix[input][output][:credit+1])
                    virtual_grants.append(vg)

                if np.sum(virtual_grants) == 0:
                    continue

                virtual_grants = virtual_grants / np.sum(virtual_grants)

                # Now chooses what to grant
                chosen_output = np.random.choice(input_reqs[input], p=virtual_grants)
                if (len(self.input_to_output_queue[(input, chosen_output)]) >= 1
                    and chosen_output not in matched_outputs):
                    matched_inputs.append(input)
                    matched_outputs.append(chosen_output)
                    final_decision[input] = chosen_output

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

            # Step 3: Input chooses one of the output queue
            for input in reqs_to_inputs:
                output = random.choice(reqs_to_inputs[input])
                matched_inputs.append(input)
                matched_outputs.append(output)
                final_decision[input] = output

        for _ in range(self.num_iteration):
            run_sm_once()

        if self.run_pim_after:
            for _ in range(self.num_iteration):
                run_pim_once()

        return final_decision.items()


if __name__ == "__main__":
    credit = np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]])
    p = StatisticalSwitch(4, 4, credit, 6, 1)
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