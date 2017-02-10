import random
import string
import os
from IPython.display import display, HTML

from .simulation import Simulation


class D3Simulation(Simulation):
    def __init__(self, env, observe, glance):
        self.env = env
        self.observe = observe
        self.glance = glance
        self.agent_data = []

    def render(self, speed):
        uid = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(directory, "resources/index.html"), 'r') as f:
            html = f.read()
            html = html.replace("__speed__", str(speed))
            html = html.replace("__width__", str(self.env.width))
            html = html.replace("__height__", str(self.env.height))
            html = html.replace("__uid__", uid)
            html = html.replace("__sequence__", str(self.agent_data))
            html = html.replace("__start__", str(self.start_data))
            html = html.replace("__object__", str(self.object_data))
            display(HTML(html))

    def run(self, num_steps=None, speed=1):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        step_ind = 0
        self.agent_data = []
        self.object_data = [self.glance(object) for object in self.env.objects]
        self.start_data = [self.glance(agent) for agent in self.env.agents]

        while True:
            step_ind += 1

            done = self.env.step()
            self.agent_data.append([self.observe(agent) for agent in self.env.agents])

            if (num_steps and step_ind > num_steps) or done:
                break
        self.render(speed)

