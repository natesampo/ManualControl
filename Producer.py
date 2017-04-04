import pygame
from Conveyor import Conveyor
class Producer(pygame.sprite.Sprite):
    def __init__(self, product, game, x=-1, y=-1, num_inputs=1, button = pygame.K_0, progress=0, production=100, built=False):
	# inputs = distance to nearest feeder factory in directions [up, right, down, left]
        self.game = game
        self.product = product
        self.x = x
        self.y = y
        self.built = False
        self.t = 0
        self.score = 0
        self.num_inputs = num_inputs
        self.button = button
        self.conveyors = []
        if self.game.onScreen(self.x, self.y):
            for i in range(0, self.num_inputs):
                producer = game.addFactory(self.x, self.y)
                conveyor = Conveyor(producer, self, producer.x, producer.y)
            self.num_inputs = 0
        if self.product == "teddybear":
            self.progress = 0
            self.production = 100
            self.button = pygame.K_0


    def step(self, button, screen):
        if self.num_inputs != 0:
            if self.game.onScreen(self.x, self.y):
                for i in range(0, self.num_inputs):
                    producer = self.game.addFactory(self.x, self.y)
                    conveyor = Conveyor(producer, self, producer.x, producer.y)
                self.num_inputs = 0
        self.progress += 3.0/2
        if self.progress >= self.production-30:
            if button:
                self.built = True
        if self.progress >= self.production+15:
            self.progress = 0
            if self.built:
                self.score += 1
