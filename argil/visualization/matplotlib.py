import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from IPython.display import display, HTML
import random
import string

from .simulation import Simulation


class MatplotlibSimulation(Simulation):
    def __init__(self, env, observe, glance):
        self.env = env
        self.observe = observe
        self.glance = glance
        self.agent_data = []

    def snapshot(self, step, figsize):
        plt.figure(figsize=figsize)
        plt.xlim((0, self.env.width))
        plt.ylim((0, self.env.height))
        plt.xticks([])
        plt.gca().invert_yaxis()
        for d in self.agent_data[step]:
            plt.scatter(d["x"], d["y"], color=d["color"])
        plt.title("Matplotlib Simulation")
        plt.show()

    def render(self, filename, num_steps, speed, figsize):
        def init_func():
            pass

        def func(frame):
            axfg.cla()
            plt.xlim((0, self.env.width))
            plt.ylim((0, self.env.height))
            plt.gca().invert_yaxis()
            plt.xticks([])
            plt.yticks([])
            for d in self.agent_data[frame]:
                plt.scatter(d["x"], d["y"], color=d["color"])

        fig = plt.figure(figsize=figsize)
        plt.clf()

        axbg = fig.add_subplot(111)
        plt.xlim((0, self.env.width))
        plt.ylim((0, self.env.height))
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])

        for o in self.object_data:
            axbg.add_patch(
                patches.Rectangle(
                    (o["x"], o["y"]),  # (x,y)
                    o["width"],  # width
                    o["height"],  # height
                )
            )
        axbg.scatter(10,10, color="blue")

        axfg = fig.add_axes(axbg.get_position(), frameon=False)
        num_steps = min(len(self.agent_data), num_steps)

        anim = animation.FuncAnimation(fig, func, init_func=init_func,
                                       frames=num_steps, interval=speed)
        anim.save(filename, writer='imagemagick')
        plt.clf()

        display(HTML("<img src={} />".format(filename)))

    def run(self, num_steps=None, speed=1, step=None, figsize=(6,6), filename="temp.gif"):
        if speed < 1 or speed > 100:
            raise Exception("speed must be greater than or equal to 1 and less than or equal to 100")
        step_ind = 0
        self.agent_data = []
        self.object_data = [self.glance(object) for object in self.env.objects]

        while True:
            step_ind += 1

            done = self.env.step()
            self.agent_data.append([self.observe(agent) for agent in self.env.agents])

            if (num_steps and step_ind > num_steps) or done:
                break
        if step:
            self.snapshot(step, figsize)
        else:
            self.render(filename, num_steps, speed, figsize)

