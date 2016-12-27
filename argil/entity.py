class Entity:
    def __init__(self, x, y, width, height, shape, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = shape
        self.color = color


class Agent(Entity):
    def __init__(self, x, y, width, height, vel=(0, 0), shape="circle", color="blue"):
        super().__init__(x, y, width, height, shape, color)
        self.vel = vel

    def step(self, get_obstacles, get_neighbors):
        return self.vel


class Obstacle(Entity):
    def __init__(self, x, y, width, height, shape="rect", color="red"):
        super().__init__(x, y, width, height, shape, color)
