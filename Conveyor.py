from Game_Constants import *
import pygame
import random
class Conveyor(pygame.sprite.Sprite):
    def __init__(self, begin_factory, end_factory, x, y, game, prev_dir='Up'):
        super(Conveyor, self).__init__()
        self.image = pygame.image.load('images/ConveyorBelt1.png')
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.game = game
        self.begin_factory = begin_factory
        self.end_factory = end_factory
        self.x = x
        self.y = y
        self.rect.topleft = (x,y)
        self.end_factory.conveyors.append(self)
        if random.random() > CONVEYOR_DIRECTION:
            if abs(self.y - end_factory.y) > 0.25:
                if self.y - end_factory.y < 0:
                    self.dir = 'Up'
                    newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y +0.5, self.game, self.dir)
                    self.game.allConveyorSprites.add(newConveyor)
                else:
                    self.dir = 'Down'
                    newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y -0.5, self.game,self.dir)
                    self.game.allConveyorSprites.add(newConveyor)

            elif abs(self.x - self.end_factory.x) > 0.25:
                if self.x - self.end_factory.x < 0:
                    self.dir = 'Right'
                    newConveyor = Conveyor(self.begin_factory, end_factory, self.x + 0.5, self.y,self.game,self.dir)
                    self.game.allConveyorSprites.add(newConveyor)
                else:
                    self.dir = 'Left'
                    newConveyor = Conveyor(self.begin_factory, end_factory, self.x - 0.5, self.y,self.game,self.dir)
                    self.game.allConveyorSprites.add(newConveyor)
        elif abs(self.x - self.end_factory.x) > 0.25 or abs(self.y - self.end_factory.y) > 0.25:
            r = random.random()
            if r <= 0.25:
                self.dir = 'Up'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y + 0.5,self.game, self.dir)
                self.game.allConveyorSprites.add(newConveyor)
            elif r <= 0.5:
                self.dir = 'Down'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x, self.y - 0.5,self.game,self.dir)
                self.game.allConveyorSprites.add(newConveyor)
            elif r <= 0.75:
                self.dir = 'Right'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x + 0.5, self.y,self.game,self.dir)
                self.game.allConveyorSprites.add(newConveyor)
            else:
                self.dir = 'Left'
                newConveyor = Conveyor(self.begin_factory, self.end_factory, self.x - 0.5, self.y,self.game,self.dir)
                self.game.allConveyorSprites.add(newConveyor)
    def update(self,scale):
        self.image = pygame.transform.scale(self.originalImage,(int(scale/2), int(scale/2)))
        self.rect.topleft = (WINDOW_WIDTH/2 + scale*(self.x-.25), WINDOW_HEIGHT/2 +scale*(self.y-.25))

