import pygame
from pygame.sprite import Sprite
from pygame import Surface

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCALE = 100

class AgentSprite(Sprite):
    def __init__(self, agent):
        super().__init__()
        self.radius = agent.radius
        self.image = Surface([self.radius * 2 * SCALE, self.radius * 2 * SCALE])
        self.image.fill((255,0,255))
        self.image.set_colorkey((255,0,255))
        pygame.draw.circle(self.image, BLUE, (int(agent.radius * SCALE), int(agent.radius * SCALE)), int(agent.radius * SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = (agent.x - self.radius) * SCALE
        self.rect.y = (agent.y - self.radius) * SCALE
        self.agent = agent

    def update(self):
        self.rect.x = (self.agent.x - self.agent.radius) * SCALE
        self.rect.y = (self.agent.y - self.agent.radius) * SCALE


class Game:
    def __init__(self, env):
        self.env = env
        self.width = env.width * 100
        self.height = env.height * 100

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([self.width, self.height])

        all_sprites_list = pygame.sprite.Group()
        for agent in self.env.agents:
            all_sprites_list.add(AgentSprite(agent))

        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            self.env.step()

            all_sprites_list.update()

            screen.fill(WHITE)
            for obstacle in self.env.obstacles:
                screen.fill((0, 255, 0), (obstacle.x * 100, obstacle.y * 100, obstacle.width * 100, obstacle.height * 100))

            all_sprites_list.draw(screen)

            pygame.display.flip()

            clock.tick(20)
        pygame.quit()
