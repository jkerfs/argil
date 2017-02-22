from itertools import product

class Experiment:
    def __init__(self, builder, sim, params=None):
        self.builder = builder
        self.sim = sim
        self.params = params

    def run(self, reps):
        if self.params:
            keys = list(self.params.keys())

        treatments = product(*list(self.params.values()))
        results = {}
        for t in treatments:
            kwargs = dict(zip(keys, t))
            results[str(t)] = []
            for r in range(reps):
                results[str(t)].append(self.sim.run(self.builder(**kwargs)))
        return results
