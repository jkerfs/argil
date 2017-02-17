class Entity:
    def __init__(self, **kwargs):
        self.params = kwargs
        self._setup()

    def _setup(self):
        for key in self.params:
            setattr(self, key, self.params[key])

class Agent(Entity):
    def __init__(self, step, **kwargs):
        super().__init__(**kwargs)
        self.step = step

    def reset(self):
        super()._setup()


class Object(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
