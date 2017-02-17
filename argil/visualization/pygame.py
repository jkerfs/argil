import pygame
from pygame.sprite import Sprite
from pygame import Surface
from .simulation import Simulation


class AgentSprite(Sprite):
    def __init__(self, agent, observe, glance, scale):
        super().__init__()
        self.agent = agent
        self.observe = observe
        self.glance = glance
        self.scale = scale

        glance_params = glance(self.agent)
        if "shape" not in glance_params:
            raise Exception("Must specify agent shape")

        self.shape = glance_params["shape"]
        if self.shape == "circle":
            self.radius = glance_params.get("radius", 1)
            self.color = glance_params.get("color", ((0, 0, 255)))
            self.x = glance_params.get("x", 0)
            self.y = glance_params.get("y", 0)

            self.image = Surface([self.radius * 2 * self.scale, self.radius * 2 * self.scale])
            self.image.fill((255, 0, 255))
            self.image.set_colorkey((255, 0, 255))
            pygame.draw.circle(self.image, self.color, (int(self.radius * self.scale), int(self.radius * self.scale)), int(self.radius * self.scale))

            self.rect = self.image.get_rect()
            self.rect.x = (self.x - self.radius) * self.scale
            self.rect.y = (self.y - self.radius) * self.scale

    def update(self):
        obs_params = self.observe(self.agent)
        self.x = obs_params.get("x", self.x)
        self.y = obs_params.get("y", self.y)
        self.radius = obs_params.get("radius", self.radius)

        self.rect.x = (self.x - self.radius) * self.scale
        self.rect.y = (self.y - self.radius) * self.scale


class PyGameSimulation(Simulation):
    def __init__(self, env, observe, glance, scale):
        self.env = env
        self.observe = observe
        self.glance = glance
        self.scale = scale
        self.width = env.width * self.scale
        self.height = env.height * self.scale

    def run(self):
        self.env.reset()
        pygame.init()
        screen = pygame.display.set_mode([self.width, self.height])

        all_sprites_list = pygame.sprite.Group()
        for agent in self.env.agents:
            all_sprites_list.add(AgentSprite(agent,self.observe, self.glance, self.scale))

        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            done = self.env.step()

            all_sprites_list.update()

            screen.fill((255, 255, 255))
            for obstacle in self.env.objects:
                screen.fill((0, 255, 0), (obstacle.x * self.scale, obstacle.y * self.scale, obstacle.width * self.scale, obstacle.height * self.scale))

            all_sprites_list.draw(screen)

            pygame.display.flip()

            clock.tick(20)

            if done:
                break
        pygame.quit()
