from Game_Constants import *
import pygame
import random
class Conveyor(pygame.sprite.Sprite):
    def __init__(self, begin_factory, end_factory, x, y, prev_dir='Up'):
        self.begin_factory = begin_factory
        self.end_factory = end_factory
        self.x = x
        self.y = y
        self.end_factory.conveyors.append(self)
        if random.random() > CONVEYOR_DIRECTION:
            if abs(self.y - end_factory.y) > 0.25:
                if self.y - end_factory.y < 0:
                    self.dir = 'Up'
                    Conveyor(self.begin_factory, self.end_factory, self.x, self.y + 0.5, self.dir)
                else:
                    self.dir = 'Down'
                    Conveyor(self.begin_factory, self.end_factory, self.x, self.y - 0.5, self.dir)
            elif abs(self.x - self.end_factory.x) > 0.25:
                if self.x - self.end_factory.x < 0:
                    self.dir = 'Right'
                    Conveyor(self.begin_factory, end_factory, self.x + 0.5, self.y, self.dir)
                else:
                    self.dir = 'Left'
                    Conveyor(self.begin_factory, end_factory, self.x - 0.5, self.y, self.dir)
        elif abs(self.x - self.end_factory.x) > 0.25 or abs(self.y - self.end_factory.y) > 0.25:
            r = random.random()
            if r <= 0.25:
                self.dir = 'Up'
                Conveyor(self.begin_factory, self.end_factory, self.x, self.y + 0.5, self.dir)
            elif r <= 0.5:
                self.dir = 'Down'
                Conveyor(self.begin_factory, self.end_factory, self.x, self.y - 0.5, self.dir)
            elif r <= 0.75:
                self.dir = 'Right'
                Conveyor(self.begin_factory, self.end_factory, self.x + 0.5, self.y, self.dir)
            else:
                self.dir = 'Left'
                Conveyor(self.begin_factory, self.end_factory, self.x - 0.5, self.y, self.dir)
