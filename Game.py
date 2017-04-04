import pygame
from PIL import Image
import os, sys, math, random
from Producer import Producer
from Conveyor import Conveyor
from Game_Constants import *
import random

clock = pygame.time.Clock()
im = Image.open('TeddyBear.jpg')
im.thumbnail((64, 64), Image.ANTIALIAS)
im.save('ThisGuy.jpg', "JPEG")
assemblerpng = Image.open('Assembler.png')

assemblerimg = pygame.image.load('Assembler.png')
bearimg = pygame.image.load('ThisGuy.jpg')

class GameMain():
    """Main Game Class"""
    def __init__(self,width=800,height=600):
        pygame.init()
        pygame.display.set_caption('Manual Control')
        # initializes screen
        self.screen = pygame.display.set_mode([width, height])
        self.x_view = 200
        self.y_view = self.x_view * 3/4


    def MainLoop(self):
        self.scale = 40000/self.x_view
        self.filledSpaces = [] # add coordinate tuples whenever a space if filled e.g. (x, y)
        self.factories = []
        self.factories.append(Producer('teddybear', self, 0, 0))
        self.addFactory()
        #Background music from the following music
        #http://audionautix.com/?utm_campaign=elearningindustry.com&utm_source=%2Fultimate-list-free-music-elearning-online-education&utm_medium=link
        pygame.mixer.music.load('BigCarTheft.mp3')
        pygame.mixer.music.play(-1)

        running = True
        while(running):
            self.scale = 40000/self.x_view
            self.x_view += 0.5
            self.y_view += 3/8
            button = False
            clock.tick(160)
            pygame.display.update()
            self.screen.fill((160, 82, 45))
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False
            for factory in self.factories:
                self.factory_render(self.screen, assemblerimg, assemblerpng, bearimg, factory)
                factory.step(pygame.key.get_pressed()[factory.button],self.screen)
                for conveyor in factory.conveyors:
                    self.conveyor_render(self.screen, conveyor)


    def factory_render(self, screen, assemberimg, assemblerpng, bearimg, factory):
        # Render inputs to factory
        progress = 1.0*factory.progress/factory.production
        pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH/2 + self.scale*(factory.x-(1-progress)-.125), WINDOW_HEIGHT/2 + self.scale*(factory.y-.125), self.scale/4, self.scale/4), 0)
        # Render factory
        img = pygame.transform.scale(assemblerimg, (int(self.scale), int(self.scale)))
        screen.blit(img, (WINDOW_WIDTH/2 + self.scale*(factory.x-.5), WINDOW_HEIGHT/2 +self.scale*(factory.y-.5)))
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
        pygame.draw.rect(screen, (0,0,0), (WINDOW_WIDTH/2 + self.scale*conveyor.x - (self.scale/100)*16, WINDOW_HEIGHT/2 + self.scale*conveyor.y - (self.scale/100)*16, (self.scale/100)*32, (self.scale/100)*32), 0)


    def addFactory(self, last_x = 0, last_y = 0):
        x = round((random.random()-.5)*8 + last_x)
        y = round((random.random()-.5)*8 + last_y)
        if (x, y) in self.filledSpaces:
            return self.addFactory(last_x, last_y)
        else:
            producer = Producer(self.getType(), self, x, y)
            self.factories.append(producer)
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

if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    MainWindow = GameMain()
    MainWindow.MainLoop()
