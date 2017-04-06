import sys
sys.path.append('../')
from scenario import Scenario


from argil import Environment, Object
from argil.contrib.crowd import SocialForceAgent

import numpy as np
import matplotlib.pyplot as plt


class HallwayScenario(Scenario):
    """
    Recommended Settings:
    num_steps = 100
    inc = 10
    """
    def __init__(self, num_agents=5):
        self.width = 10
        self.height = 10
        self.num_agents = num_agents
        self.size = 100

    def make_env(self):
        agents = []
        cm = plt.get_cmap('brg')
        l = [cm(1. * i / self.num_agents) for i in range(self.num_agents)]
        colors = iter(l)
        for i in range(self.num_agents):
            start_side = np.random.choice([0, 1])
            startx = start_side * self.width
            starty = (2 * start_side - 1) * self.height / 4. + self.height / 2. + np.random.normal(0, 2.0)
            starty = min(max(starty, 1.5), 8.5)

            endx = (1 - start_side) * self.width
            endy = (2 * start_side - 1) * self.height / 4. + self.height / 2. + np.random.normal(0, 2.0)
            endy = min(max(endy, 1.5), 8.5)
            end = (endx, endy)

            vel = np.random.normal(.8, .1)

            delay = i * 10 + int(np.random.uniform(1, 10))
            agent = SocialForceAgent(startx, starty, .2, vel_max=vel, color=next(colors), delay=delay)

            agent.add_waypoint(end)
            agent.index = i
            agents.append(agent)

        ob1 = Object(x=0, y=0, width=10, height=1)
        ob2 = Object(x=0, y=9, width=10, height=1)
        objects = [ob1, ob2]
        env = Environment(agents, objects, self.width, self.height)
        return env
