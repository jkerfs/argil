class Entity:
    def __init__(self):
        pass

    def init_view(self):
        pass

class Agent(Entity):
    def __init__(self, step, **kwargs):
        super().__init__()
        self.step = step
        for key in kwargs:
            setattr(self, key, kwargs[key])



class Obstacle(Entity):
    def __init__(self):
        super().__init__()