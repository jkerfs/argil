class Entity(object):
    def __init__(self, **kwargs):
        self.params = kwargs
        self._setup()

    def _setup(self):
        for key in self.params:
            setattr(self, key, self.params[key])

class Agent(Entity):
    def __init__(self, step, **kwargs):
        self.params = kwargs
        self._setup()
        self.step = step

    def reset(self):
        self._setup()

    def _setup(self):
        for key in self.params:
            setattr(self, key, self.params[key])

class Object(Entity):
    def __init__(self, **kwargs):
        self.params = kwargs
        self._setup()

    def _setup(self):
        for key in self.params:
            setattr(self, key, self.params[key])