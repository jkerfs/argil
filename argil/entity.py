class Entity:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color


class Agent(Entity):
    def __init__(self, x, y, radius, vel=(0, 0), shape="circle", color="blue"):
        super().__init__(x, y, shape, color)
        self.vel = vel
        self.radius = radius

    def step(self, get_obstacles, get_neighbors):
        return self.vel


class Obstacle(Entity):
    def __init__(self, x, y, width, height, shape="rect", color="red"):
        super().__init__(x, y, shape, color)
        self.width = width
        self.height = height
