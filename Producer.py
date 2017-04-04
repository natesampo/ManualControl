import pygame
class Producer(pygame.sprite.Sprite):
    def __init__(self, product, x=-1, y=-1, inputs=[1,1,1,1], progress=0, production=100, built=False):
	# inputs = distance to nearest feeder factory in directions [up, right, down, left]
        self.product = product
        self.x = x
        self.y = y
        self.progress = progress
        self.production = production
        self.built = built
        self.t = 0
        self.score = 0
        self.inputs = inputs


    def step(self, button, screen):
        self.progress += self.production*.03/2
        if self.progress >= self.production*.7:
            if button:
                self.built = True
        if self.progress >= self.production*1.15:
            self.progress = 0
            if self.built:
                self.score += 1

