from .utils.geometry import *


class Environment:
    def __init__(self, agents, obstacles, width, height):
        self.width = width
        self.height = height
        self.agents = agents
        self.obstacles = obstacles

    def _get_nearby(self, state, radius, items):
        for item in items:
            if item is state:
                continue
            d, a = rect_distance(state, item)
            if d < radius:
                yield (d, a, item)

    def get_neighbors(self, state):
        return lambda r: self._get_nearby(state, r, self.agents)

    def get_obstacles(self, state):
        return lambda r: self._get_nearby(state, r, self.obstacles)

    def step(self, delta=1.0):
        for agent in self.agents:
            get_obstacles = self.get_obstacles(agent)
            get_neighbors = self.get_neighbors(agent)
            agent.vel = agent.step(get_obstacles, get_neighbors)
        for agent in self.agents:
            agent.x += agent.vel[0] * delta
            agent.y += agent.vel[1] * delta