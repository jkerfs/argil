import pandas as pd

from argil.simulation.base import BaseSimulation


class PandasSimulation(BaseSimulation):
    def __init__(self, env, observe):
        self.env = env
        self.observe = observe
        self.agent_data = []

    def run(self, num_steps=None, inc=1):
        self.env.reset()
        step_ind = 0
        self.agent_data = []

        while True:
            step_ind += inc
            done = False
            for j in range(inc):
                done = self.env.step()
                if (num_steps and step_ind > num_steps) or done:
                    done = True
                    break

            for i, agent in enumerate(self.env.agents):
                observations = self.observe(agent)
                observations.update({"_step": step_ind, "_agent": i})
                self.agent_data.append(observations)

            if done:
                break

        self.df = pd.DataFrame(self.agent_data)
        self.df.set_index(["_step", "_agent"], inplace=True)
        self.df.index.names = ["step", "agent"]
        return self.df
