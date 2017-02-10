class AgentSprite:
    def __init__(self, agent):
        super().__init__()
        self.radius = agent.radius
        self.image = Surface([self.radius * 2 * SCALE, self.radius * 2 * SCALE])
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        pygame.draw.circle(self.image, BLUE, (int(agent.radius * SCALE), int(agent.radius * SCALE)), int(agent.radius * SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = (agent.x - self.radius) * SCALE
        self.rect.y = (agent.y - self.radius) * SCALE
        self.agent = agent

    def update(self):
        self.rect.x = (self.agent.x - self.agent.radius) * SCALE
        self.rect.y = (self.agent.y - self.agent.radius) * SCALE