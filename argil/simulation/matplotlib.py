import random
import string

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from matplotlib import animation

from argil.simulation.base import BaseSimulation

class Animation:
    def __init__(self, width, height, agent_data, object_data):
        self.width, self.height = width, height
        self.agent_data = agent_data
        self.object_data = object_data

    def display_step(self, figsize, step):
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
                )
            )
        axfg = fig.add_axes(axbg.get_position(), frameon=False)

        axfg.cla()
        plt.xlim((0, self.width))
        plt.ylim((0, self.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])
        for d in self.agent_data[step]:
            plt.scatter(d["x"], d["y"], color=d["color"])
        return fig

    def _operate(self, figsize):
        def init_func():
            pass

        def func(frame):
            axfg.cla()
            plt.xlim((0, self.width))
            plt.ylim((0, self.height))
            plt.gca().invert_yaxis()
            plt.xticks([])
            plt.yticks([])
            for d in self.agent_data[frame]:
                plt.scatter(d["x"], d["y"], color=d["color"])

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
                )
            )

        axfg = fig.add_axes(axbg.get_position(), frameon=False)

        self.fig = fig
        self.func = func
        self.init_func = init_func

    def save_gif(self, filename, figsize, num_steps, speed):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                       frames=num_steps, interval=speed)

        anim.save(filename, writer='imagemagick')
        plt.clf()
        return None

    def display_gif(self, filename, figsize, num_steps, speed):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                       frames=num_steps, interval=speed)
        unique_flag = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        anim.save(filename, writer='imagemagick')
        plt.clf()
        return display(HTML('<img src="{}"/>'.format(filename + "?" + unique_flag)))

    def display_video(self, figsize, num_steps, speed):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        self._operate(figsize)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(self.fig, self.func, init_func=self.init_func,
                                            frames=num_steps, interval=speed)
        plt.clf()
        return display(HTML(anim.to_html5_video()))


class MatplotlibSimulation(BaseSimulation):
    def __init__(self, observe, glance, num_steps=None, inc=1, step=None):
        self.observe = observe
        self.glance = glance
        self.num_steps = num_steps
        self.inc = inc
        self.step = step

        self.agent_data = []

    def render(self, env, agent_data, object_data):
        return Animation(env.width, env.height, agent_data, object_data)

    def run(self, env):
        env.reset()

        step_ind = 0
        agent_data = []
        object_data = [self.glance(object) for object in env.objects]

        while True:
            step_ind += self.inc
            done = False
            for i in range(self.inc):
                done = env.step()
                if (self.num_steps and step_ind > self.num_steps) or done:
                    done = True
                    break
            agent_data.append([self.observe(agent) for agent in env.agents])
            if done:
                break
        return self.render(env, agent_data, object_data)

