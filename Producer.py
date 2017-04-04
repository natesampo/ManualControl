import pygame
class Producer(pygame.sprite.Sprite):
    def __init__(self, product, x=-1, y=-1, inputs=[]):
	# inputs = distance to nearest feeder factory in directions [up, right, down, left]
        self.product = product
        self.x = x
        self.y = y
        self.built = False
        self.t = 0
        self.score = 0
        self.inputs = inputs
        if self.product == "teddybear":
            self.progress = 0
            self.production = 100
            self.button = pygame.K_0


    def step(self, button, screen):
        self.progress += 3.0/2
        if self.progress >= self.production-30:
            if button:
                self.built = True
        if self.progress >= self.production+15:
            self.progress = 0
            if self.built:
                self.score += 1

