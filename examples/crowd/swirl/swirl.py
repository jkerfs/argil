import sys
sys.path.append('../')
from scenario import Scenario


from argil import Environment, Object
from argil.contrib.crowd import SocialForceAgent

import numpy as np
import matplotlib.pyplot as plt


class SwirlScenario(Scenario):
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
        cm = plt.get_cmap('brg')
        l = [cm(1. * i / self.num_agents) for i in range(self.num_agents)]
        colors = iter(l)
        agents = []
        for i in np.linspace(0, 2 * np.pi, self.num_agents):
            scale = min(self.width, self.height) / 8
            start = (scale * np.cos(i) + scale, scale * np.sin(i) + scale)
            offset = .5  # np.random.normal(.3, .2)
            end = (scale * np.cos(np.pi + i + offset) + scale, scale * np.sin(np.pi + i + offset) + scale)
            ped = SocialForceAgent(start[0], start[1], .2)
            ped.color = next(colors)
            ped.add_waypoint(end)
            agents.append(ped)

        objects = []
        env = Environment(agents, objects, self.width, self.height)
        return env
