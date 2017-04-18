from Game_Constants import *
import pygame
import random
class Conveyor(pygame.sprite.Sprite):
    def __init__(self, begin_factory, end_factory, x, y, game, prev_dir=None):
        super(Conveyor, self).__init__()
        self.image = game.conveyorImg
        self.originalImage = self.image
        self.straightImages = game.straightImages
        self.turnImages = game.turnImages
        self.rect = self.image.get_rect()
        self.game = game
        self.begin_factory = begin_factory
        self.end_factory = end_factory
        self.x = x
        self.y = y
        self.rect.topleft = (x,y)
        self.end_factory.conveyors.append(self)
        self.dir = None
        self.prev_dir = prev_dir
        if abs(self.y - end_factory.y) > 0.25:
            if self.y - end_factory.y < 0:
                self.dir = 'Up'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y + (0.125 * 4/3), self.game, self.dir)
                #self.game.allConveyorSprites.add(newConveyor)
            else:
                self.dir = 'Down'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y - (0.125 * 4/3), self.game,self.dir)
                #self.game.allConveyorSprites.add(newConveyor)
        elif abs(self.x - self.end_factory.x) > 0.25:
            if self.x - self.end_factory.x < 0:
                self.dir = 'Right'
                newConveyor = Conveyor(self.begin_factory, end_factory, self.x + 0.125, self.y,self.game,self.dir)
                #self.game.allConveyorSprites.add(newConveyor)
            else:
                self.dir = 'Left'
                newConveyor = Conveyor(self.begin_factory, end_factory, self.x - 0.125, self.y,self.game,self.dir)
                #self.game.allConveyorSprites.add(newConveyor)

    def update(self, scale, screen):
        width = max(scale/200, .5)
        if self.dir == 'Right' or self.dir == 'Left':
            pygame.draw.rect(screen, (76, 174, 255), (WINDOW_WIDTH/2 + self.x * scale, WINDOW_HEIGHT/2 + self.y * scale, 35 * width, 6 * width), 0)
            pygame.draw.rect(screen, (76, 174, 255), (WINDOW_WIDTH/2 + self.x * scale, 35 * scale/200 + WINDOW_HEIGHT/2 + self.y * scale, 35 * width, 6 * width), 0)
        else:
            pygame.draw.rect(screen, (76, 174, 255), (WINDOW_WIDTH/2 + self.x * scale, WINDOW_HEIGHT/2 + self.y * scale, 6 * width, 35 * width), 0)
            pygame.draw.rect(screen, (76, 174, 255), (35 * scale/200 + WINDOW_WIDTH/2 + self.x * scale, WINDOW_HEIGHT/2 + self.y * scale, 6 * width, 35 * width), 0)
