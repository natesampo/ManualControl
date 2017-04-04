import pygame
class Producer(pygame.sprite.Sprite):
    def __init__(self, product, x=-1, y=-1, progress=0, production=100, built=False):
        self.product = product
        self.x = x
        self.y = y
        self.progress = progress
        self.production = production
        self.built = built
        self.t = 0


    def step(self, button, screen):
        self.progress += 3
        pygame.draw.rect(screen, (255, 255, 255), (self.progress*4, 500, 32, 100), 0)
        pygame.draw.rect(screen, (255, 255, 255), (800-self.progress*4, 500, 32, 100), 0)
        if self.progress >= self.production-15:
            if button:
                self.built = True
        if self.progress >= self.production:
            if button == False:
                self.progress = 0