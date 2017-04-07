import pygame
from PIL import Image
import os, sys, math, random
from Producer import Producer
from Conveyor import Conveyor
from Game_Constants import *
import math
import random

clock = pygame.time.Clock()
im = Image.open('images/TeddyBear.jpg')
im.thumbnail((64, 64), Image.ANTIALIAS)
im.save('images/ThisGuy.jpg', "JPEG")
assemblerpng = Image.open('images/Assembler.png')

assemblerimg = pygame.image.load('images/Assembler.png')
bearimg = pygame.image.load('images/ThisGuy.jpg')

class GameMain():
    """Main Game Class"""
    def __init__(self,width=WINDOW_WIDTH,height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption('Manual Control')
        # initializes screen
        self.screen = pygame.display.set_mode([width, height])
        self.x_view = 200
        self.y_view = self.x_view * 3/4


    def MainLoop(self):
        self.button_dict = {}
        self.scale = 40000/self.x_view
        self.filledSpaces = [] # add coordinate tuples whenever a space if filled e.g. (x, y)
	self.setRhythms(1) # 4 rhythms, each expressed as a array of 8 ones or zeros (for each 8th note beat)
        # sprite groups so we can render everything all at once
        self.allConveyorSprites = pygame.sprite.Group()
        self.factories = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.allConveyorSprites,self.factories)
        self.factories.add(Producer('teddybear',self,assemblerimg,0,0))
        self.addFactory()
        #Background music from the following music
        #http://audionautix.com/?utm_campaign=elearningindustry.com&utm_source=%2Fultimate-list-free-music-elearning-online-education&utm_medium=link
        pygame.mixer.music.load('BigCarTheft.ogg')
        pygame.mixer.music.play(-1)
	t = 0
        running = True
        while(running):
            self.scale = 40000/self.x_view
            self.x_view += 0.125
            self.y_view += 3/32
            button = False
            clock.tick(160)
	    t += 1/160.0/60*135
	    t = t%4
            pygame.display.update()
            self.screen.fill((160, 82, 45))
            self.allConveyorSprites.draw(self.screen)
            self.factories.draw(self.screen)
            for event in pygame.event.get():
                if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
                    else:
                        pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.FULLSCREEN | pygame.HWSURFACE)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            for factory in self.factories.sprites():
                for conveyor in factory.conveyors:
                    self.conveyor_render(self.screen, conveyor)
            for factory in self.factories:
                self.factory_render(self.screen, assemblerimg, assemblerpng, bearimg, factory)
                factory.step(pygame.key.get_pressed()[factory.button], t)
                if factory.button not in list(self.button_dict.keys()):
                    self.button_dict[factory.button] = factory
                if factory in list(self.button_dict.values()):
                    place = list(self.button_dict.values()).index(factory)
                    self.prod_render(self.screen, factory, place)
    def prod_render(self, screen, factory, place):
        progress = 50*factory.progress
        pygame.draw.rect(screen, (255, 255, 255), (32*place + 16, 32+progress, 16, 16), 0)
        pygame.draw.rect(screen, (255, 255, 255), (32*place, 102, 48, 4), 0)


    def factory_render(self, screen, assemberimg, assemblerpng, bearimg, factory):
        # Render inputs to factory
        # Render factory
        img = pygame.transform.scale(assemblerimg, (int(self.scale), int(self.scale)))
        factory.image = img
        factory.rect.topleft  = (WINDOW_WIDTH/2 + self.scale*(factory.x-.5), WINDOW_HEIGHT/2 + self.scale*(factory.y-.5))
        #screen.blit(img, (WINDOW_WIDTH/2 + self.scale*(factory.x-.5), WINDOW_HEIGHT/2 + self.scale*(factory.y-.5)))
        # Render output of factory
        if factory.built:
            if factory.t < 20:
                factory.t += 0.5
                img = pygame.transform.scale(bearimg, (int(self.scale/4), int(self.scale/4)))
                screen.blit(img, (WINDOW_WIDTH/2 + self.scale*(factory.x - .125), WINDOW_HEIGHT/2 + self.scale*(factory.y - .125 - factory.t/100.0)))
            else:
                factory.t = 0
                factory.built = False


    def conveyor_render(self, screen, conveyor):
        conveyor.update(self.scale)
        #pygame.draw.rect(screen, (0,0,0), (WINDOW_WIDTH/2 + self.scale*conveyor.x - (self.scale/100)*16, WINDOW_HEIGHT/2 + self.scale*conveyor.y - (self.scale/100)*16, (self.scale/100)*32, (self.scale/100)*32), 0)


    def addFactory(self, last_x = 0, last_y = 0):
        randx = random.random()-.5
        signx = -1 if randx<0 else 1
        randy = random.random()-.5
        signy = -1 if randy<0 else 1
        if random.random()>.5:
            x = round(signx*(2+(abs(randx)**2)*(WINDOW_WIDTH/self.scale*4)) + last_x)
            y = round(signy*((abs(randy)**2)*(WINDOW_HEIGHT/self.scale*4)) + last_y)
        else:
            x = round(signx*((abs(randx)**2)*(WINDOW_WIDTH/self.scale*4)) + last_x)
            y = round(signy*(2+(abs(randy)**2)*(WINDOW_HEIGHT/self.scale*4)) + last_y)
        if (x, y) in self.filledSpaces:
            return self.addFactory(last_x, last_y)
        else:
            producer = Producer(self.getType(), self, assemblerimg,x, y, button = BUTTON_DICT_M[math.floor(random.random()*4)+1])
            self.factories.add(producer)
            return producer
        self.filledSpaces.append((x,y))


    def getType(self):
        if self.x_view == 200: # First factory
            return 'teddybear'
        i = int(random.random()*self.x_view/100)
        if i == 0:
            return 'teddybear' # placeholder
        elif i == 1:
            return 'teddybear' # placeholder
        else:
            return 'teddybear' # placeholder


    def onScreen(self, x, y):
        return abs(x)<=WINDOW_WIDTH/self.scale and abs(y)<=WINDOW_HEIGHT/self.scale


    def setRhythms(self, difficulty):
	self.rhythms = range(4)
	for i in range(0,4):
            duplicates = True
            while duplicates:
		self.rhythms[i] = [0]*8
		r1 = random.random()
		r2 = random.random()
		r3 = random.random()
		if difficulty-i <= 1:
		    self.rhythms[i][int(r1*4)*2] = 1
		elif difficulty-i <= 2:
		    self.rhythms[i][int(r1*8)] = 1
		elif difficulty-i <= 3:
		    r1 = int(r1*4)*2
		    r2 = int(r2*3)*2
		    if r2>=r1: r2 += 1
		    self.rhythms[i][r1] = 1
		    self.rhythms[i][r2] = 1
		elif difficulty-i <= 4:
		    r1 = int(r1*8)
		    r2 = int(r2*7)
		    if r2>=r1: r2 += 1
		    self.rhythms[i][r1] = 1
		    self.rhythms[i][r2] = 1
                elif difficulty-i <= 5:
		    r1 = int(r1*4)*2
		    r2 = int(r2*3)*2
		    r3 = int(r3*2)*2
		    if r2>=r1: r2 += 1
		    if r3>=r1: r3 += 1
		    if r3>=r2: r3 += 1
		    self.rhythms[i][r1] = 1
		    self.rhythms[i][r2] = 1
		    self.rhythms[i][r3] = 1
                else:
		    r1 = int(r1*8)
		    r2 = int(r2*7)
		    r3 = int(r3*6)
		    if r2>=r1: r2 += 1
		    if r3>=r1: r3 += 1
		    if r3>=r2: r3 += 1
		    self.rhythms[i][r1] = 1
		    self.rhythms[i][r2] = 1
		    self.rhythms[i][r3] = 1
                duplicates = False
                for j in range(i):
                    if self.rhythms[i] == self.rhythms[j]:
                        duplicates = True
        print("rhythms: "+str(self.rhythms))


if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    MainWindow = GameMain()
    MainWindow.MainLoop()
