class BaseSimulation:
    def __init__(self, observe, num_steps=None):
        self.observer = observe
        self.num_steps = num_steps

    def run(self, env):
        pass
