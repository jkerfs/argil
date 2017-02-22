import random
import string

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from matplotlib import animation

from argil.simulation.base import BaseSimulation


class MatplotlibSimulation(BaseSimulation):
    def __init__(self, observe, glance, num_steps=None, speed=10, inc=1, step=None, figsize=(6,6), filename="temp.gif"):
        self.observe = observe
        self.glance = glance
        self.num_steps = num_steps
        self.speed = speed
        self.inc = inc
        self.step = step
        self.figsize = figsize
        self.filename = filename

        self.agent_data = []

    def snapshot(self, env, agent_data):
        plt.figure(figsize=self.figsize)
        plt.xlim((0, env.width))
        plt.ylim((0, env.height))
        plt.xticks([])
        plt.gca().invert_yaxis()
        for d in agent_data[self.step]:
            plt.scatter(d["x"], d["y"], color=d["color"])
        plt.title("Matplotlib Simulation")
        plt.show()

    def render(self, env, agent_data, object_data):
        def init_func():
            pass

        def func(frame):
            axfg.cla()
            plt.xlim((0, env.width))
            plt.ylim((0, env.height))
            plt.gca().invert_yaxis()
            plt.xticks([])
            plt.yticks([])
            for d in agent_data[frame]:
                plt.scatter(d["x"], d["y"], color=d["color"])

        fig = plt.figure(figsize=self.figsize)
        plt.clf()

        axbg = fig.add_subplot(111)
        plt.xlim((0, env.width))
        plt.ylim((0, env.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])

        for o in object_data:
            axbg.add_patch(
                patches.Rectangle(
                    (o["x"], o["y"]) ,
                    o["width"],
                    o["height"],
                )
            )

        axfg = fig.add_axes(axbg.get_position(), frameon=False)
        num_steps = min(len(agent_data), self.num_steps)

        anim = animation.FuncAnimation(fig, func, init_func=init_func,
                                       frames=num_steps, interval=self.speed)
        anim.save(self.filename, writer='imagemagick')
        plt.clf()

        unique_flag = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        display(HTML("<img src={} />".format(self.filename + "?" + unique_flag)))

    def run(self, env):
        env.reset()
        if self.speed < 1 or self.speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
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
        if self.step:
            self.snapshot(env, agent_data)
        else:
            self.render(env, agent_data, object_data)

