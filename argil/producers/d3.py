import os
import random
import string

from IPython.display import display, HTML

from argil.producers.base import BaseProducer


class D3Producer(BaseProducer):
    def __init__(self, speed=1):
        self.speed = speed
        if self.speed < 1 or self.speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")

    def produce(self, record):
        env_data = record.env_data
        agent_data = record.observed_agent_data
        start_data = record.glance_agent_data
        object_data = record.glance_object_data

        uid = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(directory, "resources/index.html"), 'r') as f:
            html = f.read()
            html = html.replace("__speed__", str(self.speed))
            html = html.replace("__width__", str(env_data["width"]))
            html = html.replace("__height__", str(env_data["height"]))
            html = html.replace("__uid__", uid)
            html = html.replace("__sequence__", str(agent_data))
            html = html.replace("__start__", str(start_data))
            html = html.replace("__object__", str(object_data))
            display(HTML(html))
