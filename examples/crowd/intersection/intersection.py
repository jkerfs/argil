import sys
sys.path.append('../')
from scenario import Scenario

from argil import Environment, Object
from argil.contrib.crowd import SocialForceAgent

import numpy as np

import matplotlib.pyplot as plt


class IntersectionScenario(Scenario):
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
            locs = [0., np.pi / 2, np.pi, 3 * np.pi / 2]
            start_side = np.random.choice(locs)
            end_side = start_side
            while np.isclose(start_side, end_side):
                end_side = np.random.choice(locs)

            startx = np.cos(start_side) * self.width / 2. + self.width / 2. + np.random.normal(0, .2)
            starty = np.sin(start_side) * self.height / 2. + self.height / 2. + np.random.normal(0, .2)
            start = (startx, starty)

            endx = np.cos(end_side) * self.width / 2. + self.width / 2. + np.random.normal(0, .2)
            endy = np.sin(end_side) * self.height / 2. + self.height / 2. + np.random.normal(0, .2)
            end = (endx, endy)

            midx = np.min([np.max([(startx + endx) / 2., 4.5]), 5.5])
            midy = np.min([np.max([(starty + endy) / 2., 4.5]), 5.5])
            mid = (midx, midy)
            vel = np.random.normal(1.0, .1)

            delay = int(np.random.uniform(1, 400))
            agent = SocialForceAgent(startx, starty, .2, vel_max=vel, color=next(colors), delay=delay, hide=True)

            agent.add_waypoint(start)
            agent.add_waypoint(mid)
            agent.add_waypoint(end)
            agent.index = i
            agents.append(agent)

        ob1 = Object(x=0, y=0, width=3, height=3)
        ob2 = Object(x=0, y=7, width=3, height=3)
        ob3 = Object(x=7, y=0, width=3, height=3)
        ob4 = Object(x=7, y=7, width=3, height=3)
        objects = [ob1, ob2, ob3, ob4]
        env = Environment(agents, objects, self.width, self.height)
        return env
