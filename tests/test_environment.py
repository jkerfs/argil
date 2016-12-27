import unittest
from argil.environment import Environment
from argil.entity import Agent


class TestEnvironment(unittest.TestCase):

    def test_get_neighbors(self):
        agents = [Agent(10, 10, 5, 5), Agent(20, 20, 10, 10)]
        env = Environment(agents, [], 100, 100)
        assert len(list(env.get_neighbors(agents[0])(200))) == 1
        assert len(list(env.get_neighbors(agents[0])(5))) == 0

