import sys
sys.path.append('../..')

from argil.environment import Environment
from argil.entity import Obstacle
from argil.socialforce import SocialForceAgent
from argil.visualization.game import Game


width, height = 10, 5

agents = [SocialForceAgent(.2, 2.40, .2, .2), SocialForceAgent(9.0, 1.0, .2, .2), SocialForceAgent(9.0, 2.4, .2, .2)]
obstacles = [Obstacle(0, 0, 10., .2), Obstacle(0., 4.8, 10., .2), Obstacle(3.0, 1.8, 1., 2.)]
env = Environment(agents, obstacles, width, height)
agents[0].add_waypoint((8.00, 1.00))
agents[1].add_waypoint((.2, 1.00))
agents[2].add_waypoint((.2, 4.1, .5, .5))
game = Game(env)
game.run()