import pandas as pd

from argil.simulation.base import BaseSimulation


class PandasSimulation(BaseSimulation):
    def __init__(self, observe, num_steps=10, inc=1):
        super().__init__(observe, num_steps)
        self.observe = observe
        self.inc = inc

    def run(self, env):
        env.reset()
        step_ind = 0
        agent_data = []

        while True:
            step_ind += self.inc
            done = False
            for j in range(self.inc):
                done = env.step()
                if (self.num_steps and step_ind > self.num_steps) or done:
                    done = True
                    break

            for i, agent in enumerate(env.agents):
                observations = self.observe(agent)
                observations.update({"_step": step_ind, "_agent": i})
                agent_data.append(observations)

            if done:
                break

        df = pd.DataFrame(agent_data)
        df.set_index(["_step", "_agent"], inplace=True)
        df.index.names = ["step", "agent"]
        return df

