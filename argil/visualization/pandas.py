import pandas as pd
from .simulation import Simulation


class PandasSimulation(Simulation):
    def __init__(self, env, observe):
        self.env = env
        self.observe = observe
        self.agent_data = []

    def run(self, num_steps=None):
        step_ind = 0
        self.agent_data = []

        while True:
            step_ind += 1

            done = self.env.step()

            for i, agent in enumerate(self.env.agents):
                observations = self.observe(agent)
                observations.update({"_step": step_ind, "_agent": i})
                self.agent_data.append(observations)

            if (num_steps and step_ind > num_steps) or done:
                break
        self.df = pd.DataFrame(self.agent_data)
        self.df.set_index(["_step", "_agent"], inplace=True)
        self.df.index.names = ["step", "agent"]
        return self.df

