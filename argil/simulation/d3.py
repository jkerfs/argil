import os
import random
import string

from IPython.display import display, HTML

from argil.simulation.base import BaseSimulation


class D3Simulation(BaseSimulation):
    def __init__(self, observe, glance, num_steps=None, speed=1):
        self.observe = observe
        self.glance = glance
        self.num_steps = num_steps
        self.speed = speed

        if self.speed < 1 or self.speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")

    def render(self, env, agent_data, object_data, start_data):
        uid = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(directory, "resources/index.html"), 'r') as f:
            html = f.read()
            html = html.replace("__speed__", str(self.speed))
            html = html.replace("__width__", str(env.width))
            html = html.replace("__height__", str(env.height))
            html = html.replace("__uid__", uid)
            html = html.replace("__sequence__", str(agent_data))
            html = html.replace("__start__", str(start_data))
            html = html.replace("__object__", str(object_data))
            display(HTML(html))

    def run(self, env):
        env.reset()

        step_ind = 0
        agent_data = []
        object_data = [self.glance(object) for object in env.objects]
        start_data = [self.glance(agent) for agent in env.agents]

        while True:
            step_ind += 1

            done = env.step()
            agent_data.append([self.observe(agent) for agent in env.agents])

            if (self.num_steps and step_ind > self.num_steps) or done:
                break
        self.render(env, agent_data, object_data, start_data)


