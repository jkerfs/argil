from itertools import product
from multiprocessing import Process, JoinableQueue


class Experiment:
    def __init__(self, builder, sim, params=None):
        self.builder = builder
        self.sim = sim
        self.params = params if params else {}

    def _single(self, reps, keys, treatments):

        results = {}
        for t in treatments:
            kwargs = dict(zip(keys, t)) if keys else {}
            results[str(t)] = []
            for r in range(reps):
                results[str(t)].append(self.sim.run(self.builder(**kwargs)))
        return results

    def _parallel(self, reps, keys, treatments, num_threads):
        jobs = JoinableQueue()
        results = JoinableQueue()

        for t in treatments:
            kwargs = dict(zip(keys, t)) if keys else {}
            for r in range(reps):
                jobs.put((str(t), kwargs))

        def op(jobs, results):
            while True:
                name, kwargs = jobs.get()
                res = self.sim.run(self.builder(**kwargs))
                results.put((name, res))
                jobs.task_done()

        for th in range(num_threads):
            process = Process(
                target=op,
                name=str(th),
                args=[jobs, results]
            )
            process.start()

        jobs.join()

        formatted_results = {}
        while not results.empty():
            n, r = results.get()
            if n in formatted_results:
                formatted_results[n].append(r)
            else:
                formatted_results[n] = [r]
        if len(formatted_results) == 1:
            return formatted_results[formatted_results.keys()[0]]
        return formatted_results


    def run(self, reps, num_threads=1):
        keys = list(self.params.keys()) if self.params else None

        treatments = product(*list(self.params.values()))

        if num_threads > 1:
            return self._parallel(reps, keys, treatments, num_threads)
        else:
            return self._single(reps, keys, treatments)

