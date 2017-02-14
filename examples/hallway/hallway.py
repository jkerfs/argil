import numpy as np
import sys
sys.path.append('../..')

from argil.environment import Environment
from argil.entity import Object
from argil.socialforce import SocialForceAgent
from argil.visualization.pygame import PyGameSimulation


width, height = 10, 5

agents = []
for i in range(20):
    vel = np.random.normal(1.0, .1)
    start = ((i % 5) + .5, int(i / 5) + 1)
    agents.append(SocialForceAgent(start[0], start[1], .2, vel_max=vel))
    agents[-1].add_waypoint((10 - (start[0]), start[1] + .1))
obstacles = [Object(x=0, y=0, width=10., height=.2), Object(x=0., y=4.8, width=10., height=.2)]
env = Environment(agents, obstacles, width, height)
game = PyGameSimulation(env)
game.run()