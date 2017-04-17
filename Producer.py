import pygame
from Conveyor import Conveyor
from Game_Constants import *
class Producer(pygame.sprite.Sprite):
    def __init__(self, product, game, img, x=-1, y=-1, num_inputs=1, button = pygame.K_1):
	# inputs = distance to nearest feeder factory in directions [up, right, down, left]
        super(Producer, self).__init__()
        #self.image = pygame.image.load(img)
        self.game = game
        self.product = product
        self.x = x
        self.y = y
        self.t = 0
        self.score = 0
        self.beatsHit = [0]*8
        self.num_inputs = num_inputs
        self.button = button
        self.conveyors = []
        self.image = img
        self.rect = self.image.get_rect()
        self.rhythm = game.rhythms[BUTTON_DICT_TWO[self.button]-1]
        self.built = [0]*sum(self.rhythm)
        self.progress = [0]*sum(self.rhythm)
        self.keyDown = [0]*sum(self.rhythm)
        self.onBeat = [0]*sum(self.rhythm)
        #if self.game.onScreen(self.x, self.y):
            #for i in range(0, self.num_inputs):
            #    producer = game.addFactory(self.x, self.y)
            #    conveyor = Conveyor(producer, self, producer.x, producer.y,self.game)
                #self.game.allConveyorSprites.add(conveyor)
         #   self.num_inputs = 0

    def update(self):
        self.rect.topleft = (x,y)

    def step(self, button, t):
        # t = number of beats since start of last measure (not necessarily a whole number)
	# add new factories once on screen
        #if self.num_inputs != 0:
            #if self.game.onScreen(self.x, self.y):
                #for i in range(0, self.num_inputs):
                    #producer = self.game.addFactory(self.x, self.y)
                    #conveyor = Conveyor(producer, self, producer.x, producer.y,self.game)
                    #self.game.allConveyorSprites.add(conveyor)
             #   self.num_inputs = 0

	# check if a beat was hit
        self.progress = [0]*sum(self.rhythm)
        j = 0
        for i, beat in enumerate(self.rhythm):
            if beat:
                progress = ((t*2-i)%8)/8.0
                self.progress[j] = progress
                if abs(t*2-i)/8 <= .1 or abs(t*2-i)/8 >= .9: # on the beat
                    self.onBeat[j] = 1
                    if button and not self.beatsHit[i] and not self.keyDown[j]: # beat was hit for first time
                        self.score += 1
                        self.beatsHit[i] = 1
                        self.built = [0]*sum(self.rhythm)
                        self.built[j] = 1
                        self.t = 0
                        self.game.score += 1
                        self.keyDown[j] = 1
                    if not button:
                        self.keyDown[j] = 0
                else:
                    if not self.beatsHit[i] and self.onBeat[j]: # didn't hit the beat
                        self.game.health -= 1
                    self.beatsHit[i] = 0
                    self.onBeat[j] = 0
                    if button and not self.keyDown[j] and not sum(self.onBeat): # pressed at wrong time
                        self.game.health -= 1
                        self.keyDown[j] = 1
                    if not button:
                        self.keyDown[j] = 0
                j = j+1
