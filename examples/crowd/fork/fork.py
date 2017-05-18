import sys
sys.path.append('../')
from scenario import Scenario

from argil import Environment, Object
from argil.contrib.crowd import SocialForceAgent

import numpy as np

import matplotlib.pyplot as plt


class ForkScenario(Scenario):
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

    def _get_coords(self, loc):
        if loc == "top":
            x = np.random.uniform(4, 6)
            y = 0
        elif loc == "left":
            x = 0
            y = np.random.uniform(4, 6)
        elif loc == "right":
            x = 10
            y = np.random.uniform(4, 6)
        return x, y

    def make_env(self):
        agents = []
        cm = plt.get_cmap('brg')
        l = [cm(1. * i / self.num_agents) for i in range(self.num_agents)]
        colors = iter(l)
        for i in range(self.num_agents):
            start_side = np.random.choice(["top", "left", "right"])
            startx, starty = self._get_coords(start_side)

            end_side = start_side
            while start_side == end_side:
                end_side = np.random.choice(["top", "left", "right"])
            endx, endy = self._get_coords(end_side)

            if start_side == "top":
                midx = startx
                midy = endy
            else:
                midx = 5 + np.random.uniform(-1, 1)
                midy = 5.5 + np.random.uniform(-.8, .8)

            vel = max(np.random.normal(.3, .1), .3)

            delay = i * 50 + int(np.random.uniform(1, 10))
            agent = SocialForceAgent(startx, starty, .2, vel_max=vel, color=next(colors), delay=delay, hide=True)
            agent.add_waypoint((midx, midy))
            agent.add_waypoint((endx, endy))
            agent.index = i
            agents.append(agent)

        ob1 = Object(x=0, y=0, width=3.5, height=4.)
        ob2 = Object(x=6.5, y=0, width=3.5, height=4.)
        ob3 = Object(x=0, y=6.5, width=10, height=3.5)
        objects = [ob1, ob2, ob3]
        env = Environment(agents, objects, self.width, self.height)
        return env