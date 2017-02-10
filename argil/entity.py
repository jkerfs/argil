class Entity:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

class Agent(Entity):
    def __init__(self, step, **kwargs):
        super().__init__(**kwargs)
        self.step = step




class Object(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
