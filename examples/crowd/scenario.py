import numpy as np
import pandas as pd

from argil.simulations import RecordSimulation
from argil.producers import MatplotlibProducer
from argil import Object


class Scenario(object):
    def __init__(self):
        self.width = 10
        self.height = 10
        self.size = 100

    def make_env(self):
        pass

    def get_rec(self, num_steps=200, inc=1):
        def glance(entity):
            if isinstance(entity, Object):
                return {"x": entity.x, "y": entity.y, "width": entity.width, "height": entity.height}

        def observe(agent):
            return {"x": agent.x, "y": agent.y, "done": agent.done, "color": agent.color, "size": self.size}

        def survey(env):
            return {"width": env.width, "height": env.height}

        sim = RecordSimulation(glance, observe, survey, num_steps=num_steps, inc=inc)
        env = self.make_env()
        return sim.run(env)

    def get_gif(self, num_steps=200, inc=1, figsize=(6,6), name="temp.gif"):
        rec = self.get_rec(num_steps, inc)

        mprod = MatplotlibProducer()
        anim = mprod.produce(rec)
        anim.display_gif(name, figsize, num_steps, inc)