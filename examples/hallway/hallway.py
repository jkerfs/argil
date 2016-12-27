import numpy as np
import sys
sys.path.append('../..')

from argil.environment import Environment
from argil.entity import Obstacle
from argil.socialforce import SocialForceAgent
from argil.visualization.game import Game


width, height = 10, 5

agents = []
for i in range(20):
    vel = np.random.normal(1.0, .1)
    start = ((i % 5) + .5, int(i / 5) + 1)
    agents.append(SocialForceAgent(start[0], start[1], .2, vel_max=vel))
    agents[-1].add_waypoint((10 - (start[0]), start[1] + .1))
obstacles = [Obstacle(0, 0, 10., .2), Obstacle(0., 4.8, 10., .2)]
env = Environment(agents, obstacles, width, height)
game = Game(env)
game.run()