import pygame
from PIL import Image
import os, sys
from Producer import Producer
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


    def MainLoop(self):
        self.LoadSprites()
	self.scale = pygame.display.get_surface().get_size()[0]/4 # screen is 4 x 3 units initially
	self.level = 1
        running = True
        while(running):
            button = False
            clock.tick(120)
            pygame.display.update()
            self.screen.fill((160, 82, 45))
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_0]:
                    button = True
            for factory in self.factories:
                self.render(self.screen, assemblerimg, assemblerpng, bearimg, factory)
                factory.step(button,self.screen)
            if self.factories[0].score >= 10:
                self.changeLevel()


    def render(self,screen,assemberimg,assemblerpng,bearimg, factory):
        # Render inputs to factory
        progress = 1.0*factory.progress/factory.production
        if factory.inputs[0]: # up
            pygame.draw.rect(screen, (255, 255, 255), (self.scale*(factory.x-.125), self.scale*(factory.y-(factory.inputs[0])*(1-progress)-.125), self.scale/4, self.scale/4), 0)
        if factory.inputs[1]: # right
            pygame.draw.rect(screen, (255, 255, 255), (self.scale*(factory.x+(factory.inputs[1])*(1-progress)-.125), self.scale*(factory.y-.125), self.scale/4, self.scale/4), 0)
        if factory.inputs[2]: # down
            pygame.draw.rect(screen, (255, 255, 255), (self.scale*(factory.x-.125), self.scale*(factory.y+(factory.inputs[2])*(1-progress)-.125), self.scale/4, self.scale/4), 0)
        if factory.inputs[3]: # left
            pygame.draw.rect(screen, (255, 255, 255), (self.scale*(factory.x-(factory.inputs[3])*(1-progress)-.125), self.scale*(factory.y-.125), self.scale/4, self.scale/4), 0)
        # Render factory
        img = pygame.transform.scale(assemblerimg, (int(self.scale), int(self.scale)))
	screen.blit(img, (self.scale*(factory.x-.5), self.scale*(factory.y-.5)))
        # Render output of factory
        if factory.built:
            if factory.t < 20:
                factory.t += 0.5
		img = pygame.transform.scale(bearimg, (int(self.scale/4), int(self.scale/4)))
                screen.blit(img, (self.scale*(factory.x - .125),self.scale*(factory.y - .125 - factory.t/100.0)))
            else:
                factory.t = 0
                factory.built = False


    def changeLevel(self):
        self.level += 1
        self.factories[0].score = 0
        if self.level == 2:
            self.scale *= 2.0/3
            del self.factories[:]
            self.factories.append(Producer('teddybear', 2, 2.25, [0,2,2,0]))#left
            self.factories.append(Producer('teddybear', 4, 2.25, [0,0,2,0]))#right
        elif self.level == 3:
            self.scale *= 3.0/4
            del self.factories[:]
            self.factories.append(Producer('teddybear', 3, 2, [0,2,2,2]))#left
            self.factories.append(Producer('teddybear', 3, 4, [0,2,0,2]))
            self.factories.append(Producer('teddybear', 5, 2, [0,0,2,0]))#right
            self.factories.append(Producer('teddybear', 5, 4, [0,0,0,0]))
        elif self.level == 4:
            del self.factories[:]
            self.factories.append(Producer('teddybear', 4, 2, [2,2,2,2]))#middle
            self.factories.append(Producer('teddybear', 4, 4, [0,2,0,2]))
            self.factories.append(Producer('teddybear', 2, 2, [2,0,2,0]))#left
            self.factories.append(Producer('teddybear', 2, 4, [0,0,0,0]))
            self.factories.append(Producer('teddybear', 6, 2, [2,0,2,0]))#right
            self.factories.append(Producer('teddybear', 6, 4, [0,0,0,0]))
        elif self.level == 5:
            del self.factories[:]
            self.factories.append(Producer('teddybear', 4, 3, [2,2,2,2]))#middle
            self.factories.append(Producer('teddybear', 2, 3, [2,0,2,0]))
            self.factories.append(Producer('teddybear', 6, 3, [2,0,2,0]))
            self.factories.append(Producer('teddybear', 4, 5, [0,2,0,2]))#bottom
            self.factories.append(Producer('teddybear', 2, 5, [0,0,0,0]))
            self.factories.append(Producer('teddybear', 6, 5, [0,0,0,0]))
            self.factories.append(Producer('teddybear', 4, 1, [0,2,0,2]))#top
            self.factories.append(Producer('teddybear', 2, 1, [0,0,0,0]))
            self.factories.append(Producer('teddybear', 6, 1, [0,0,0,0]))


    def LoadSprites(self):
        self.factories = []
        for i in range(0, 1):
            producer = Producer('teddybear', 2, 1.5, [0,2,0,0])
            self.factories.append(producer)



if __name__ == '__main__':
    MainWindow = GameMain()
    MainWindow.MainLoop()
