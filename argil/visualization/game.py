import pygame
from pygame.sprite import Sprite
from pygame import Surface

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class AgentSprite(Sprite):
    def __init__(self, agent):
        super().__init__()
        self.image = Surface([agent.width * 100, agent.width * 100])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = agent.x * 100
        self.rect.y = agent.y * 100
        self.agent = agent

    def update(self):
        self.rect.x = (self.agent.x - self.agent.width / 2) * 100
        self.rect.y = (self.agent.y - self.agent.height / 2) * 100


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
