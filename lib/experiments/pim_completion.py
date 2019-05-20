import random

from lib.pim import PimSwitch
from lib.packet import Packet

def test_pim_completion(arrival_probability, num_trials):
    """Test converge of PIM.
    
    Examines how many matches PIM finds in a given number of iterations,
    relative to if it is allowed to run to completion. Meant to reproduce
    Table I from Anderson et al.
    """
    def run_trial():
        p = PimSwitch(16, 16, num_iteration=0)

        for i in range(16):
            for j in range(16):
                if random.random() < arrival_probability:
                    p.receive(Packet(i, j))
        p.schedule()
        return [c / p.match_counts[-1] for c in p.match_counts]

    results = []
    for _ in range(num_trials):
        results.append(run_trial())

    sum_results = {}
    count_results = {}
    for result in results:
        for idx, val in enumerate(result):
            sum_results[idx] = sum_results.get(idx, 0) + val
            count_results[idx] = count_results.get(idx, 0) + 1

    print("Results of experiment with arrival probability "
          "{} ({} trials):".format(arrival_probability, num_trials))
    for idx in sum_results:
        print("Iteration {}: {}".format(idx+1, sum_results[idx] / count_results[idx]))
    print()
   

# Each experiment file should have a main() function like this, which runs the experiment
# exactly as we want it to be reproduced. It should have no arguments, so that all of the
# "configuration" is included in this file.
#
# Note that we can't make a "real" main function (i.e. __main__) in this file, because
# absolute imports would break. So, this needs to be called from the root directory,
# i.e. in run.py.
def main():
    print("Testing convergence of PIM.")
    print()
    num_iterations = 1000 * 100
    test_pim_completion(0.10, num_iterations)
    test_pim_completion(0.25, num_iterations)
    test_pim_completion(0.50, num_iterations)
    test_pim_completion(0.75, num_iterations)
    test_pim_completion(1.00, num_iterations)
    