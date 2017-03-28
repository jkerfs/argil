import random
import string

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from matplotlib import animation

from argil.producers.base import BaseProducer

class Animation:
    def __init__(self, width, height, agent_data, object_data):
        self.width, self.height = width, height
        self.agent_data = agent_data
        self.object_data = object_data

    def display_step(self, figsize, step, agent_index=None):
        fig = plt.figure(figsize=figsize)
        plt.clf()
        axbg = fig.add_subplot(111)
        plt.xlim((0, self.width))
        plt.ylim((0, self.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])
        for o in self.object_data:
            axbg.add_patch(
                patches.Rectangle(
                    (o["x"], o["y"]),
                    o["width"],
                    o["height"],
                    color = o.get("color", o.get("fill", "black"))
                )
            )
        axfg = fig.add_axes(axbg.get_position(), frameon=False)

        axfg.cla()
        plt.xlim((0, self.width))
        plt.ylim((0, self.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])
        if agent_index is not None:
            cur = self.agent_data[step][agent_index]
            plt.scatter(cur["x"], cur["y"], color=cur["color"], s=cur.get("size", 10))
        else:
            for d in self.agent_data[step]:
                if d:
                    plt.scatter(d["x"], d["y"], color=d["color"], s=d.get("size", 10))
        return fig

    def _operate(self, figsize, agent_index=None):
        def init_func():
            pass

        def func(frame):
            axfg.cla()
            plt.xlim((0, self.width))
            plt.ylim((0, self.height))
            plt.gca().invert_yaxis()
            plt.xticks([])
            plt.yticks([])

            if agent_index is not None:
                cur = self.agent_data[frame][agent_index]
                plt.scatter(cur["x"], cur["y"], color=cur["color"], s=cur.get("size", 10))
            else:
                for d in self.agent_data[frame]:
                    if d:
                        plt.scatter(d["x"], d["y"], color=d["color"], s=d.get("size", 10))

        fig = plt.figure(figsize=figsize)
        plt.clf()

        axbg = fig.add_subplot(111)
        plt.xlim((0, self.width))
        plt.ylim((0, self.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])

        for o in self.object_data:
            axbg.add_patch(
                patches.Rectangle(
                    (o["x"], o["y"]),
                    o["width"],
                    o["height"],
                    color=o.get("color", o.get("fill", "black"))
                )
            )

        axfg = fig.add_axes(axbg.get_position(), frameon=False)

        self.fig = fig
        self.func = func
        self.init_func = init_func

    def save_gif(self, filename, figsize, num_steps, speed, agent_index=None):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize, agent_index)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                       frames=num_steps, interval=speed)

        anim.save(filename, writer='imagemagick')
        plt.clf()
        return None

    def display_gif(self, filename, figsize, num_steps, speed, agent_index=None):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize, agent_index)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                       frames=num_steps, interval=speed)
        unique_flag = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        anim.save(filename, writer='imagemagick')
        plt.clf()
        return display(HTML('<img src="{}"/>'.format(filename + "?" + unique_flag)))

    def display_video(self, figsize, num_steps, speed, agent_index=None):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize, agent_index)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                            frames=num_steps, interval=speed)
        plt.clf()
        return display(HTML(anim.to_html5_video()))


class MatplotlibProducer(BaseProducer):
    def __init__(self):
        pass

    def produce(self, record):
        env_data = record.env_data
        agent_data = record.observed_agent_data
        object_data = record.glance_object_data

        return Animation(env_data["width"], env_data["height"], agent_data, object_data)

