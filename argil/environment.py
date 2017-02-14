from .utils.geometry import *


class Environment:
    def __init__(self, agents, objects, width, height):
        self.width = width
        self.height = height
        self.agents = agents
        self.objects = objects

    def _get_nearby(self, state, radius, items, dist_func):
        for item in items:
            if item is state:
                continue
            d, a = dist_func(state, item)
            if d < radius:
                yield (d, a, item)

    def get_neighbors(self, state):
        return lambda r: self._get_nearby(state, r, self.agents, circle_distance)

    def get_objects(self, state):
        return lambda r: self._get_nearby(state, r, self.objects, rect_distance)

    def step(self, delta=1.0):
        done = True
        for agent in self.agents:
            get_obstacles = self.get_objects(agent)
            get_neighbors = self.get_neighbors(agent)
            done &= agent.step(agent, get_obstacles, get_neighbors)
        return done
