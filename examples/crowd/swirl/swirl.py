import sys
sys.path.append('../')
from scenario import Scenario


from argil import Environment
from argil.contrib.crowd import SocialForceAgent

import numpy as np
import matplotlib.pyplot as plt


class SwirlScenario(Scenario):
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
        center = min(self.width, self.height) / 2
        scale = min(self.width, self.height) / 2.1
        for i in np.linspace(0, 2 * np.pi, self.num_agents)[:-1]:
            start = (scale * np.cos(i) + center, scale * np.sin(i) + center)
            offset = np.pi / 3  # np.random.normal(.3, .2)
            end = (scale * np.cos(np.pi + i + offset) + center, scale * np.sin(np.pi + i + offset) + center)
            ped = SocialForceAgent(start[0], start[1], .5, vel_max=.5)
            ped.color = next(colors)
            ped.add_waypoint(end)
            agents.append(ped)

        objects = []
        env = Environment(agents, objects, self.width, self.height)
        return env
