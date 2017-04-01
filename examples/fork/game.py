import pandas as pd
import numpy as np
import random
import string
import json
import sys
sys.path.append("../../")

from argil.producers import D3Producer, MatplotlibProducer, PandasProducer
from argil import Object, Agent, Environment, Experiment
from argil.simulations import RecordSimulation, PyGameSimulation
import argil

width = 5
height = 3

def step(self, get_obstacles, get_neighbors):
    if self.y < 19:
        self.y += .05
    elif self.y == 19:
        self.direction = random.choice([-1,1])
        self.y += .05
    else:
        self.x += self.direction * .05
        if self.x < 0 or self.x > width:
            return True
    return False

agent1 = argil.Agent(step, x=2.5, y=0)
agent2 = argil.Agent(step, x=2.5, y=.6)
agents = [agent1, agent2]

left_wall = argil.Object(x=0, y=0, width=2, height=1.5, fill="purple")
right_wall = argil.Object(x=3, y=0, width=2, height=1.5, fill="purple")
bottom_wall = argil.Object(x=0, y=2.5, width=5, height=.5, fill="blue")
objects = [left_wall, right_wall, bottom_wall]
roboWorld = argil.Environment(agents, objects, width, height)

def glance(entity):
    if isinstance(entity, argil.Object):
        return {"x": entity.x, "y": entity.y, "color": (255, 0, 255)}
    else:
        return {"_shape": "circle", "r": .02, "fill": "red"}

def observe(agent):
    return {"x": agent.x, "y": agent.y, "radius": .02, "color": (255,0,0)}

def survey(env):
    return {"width": env.width, "height": env.height}

simulation = PyGameSimulation(glance, observe, survey)
simulation.run(roboWorld)