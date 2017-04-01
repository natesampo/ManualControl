import pygame
from PIL import Image
import os, sys
clock = pygame.time.Clock()
im = Image.open('TeddyBear.jpg')
im.thumbnail((64, 64), Image.ANTIALIAS)
im.save('ThisGuy.jpg', "JPEG")
assemblerpng = Image.open('Assembler.png')

assemblerimg = pygame.image.load('Assembler.png')
bearimg = pygame.image.load('ThisGuy.jpg')

class Producer(pygame.sprite.Sprite):
    def __init__(self, product, x=-1, y=-1, progress=0, production=100, built=False):
        self.product = product
        self.x = x
        self.y = y
        self.progress = progress
        self.production = production
        self.built = built
        self.t = 0


    def step(self, button, screen):
        self.progress += 3
        pygame.draw.rect(screen, (255, 255, 255), (self.progress*4, 500, 32, 100), 0)
        pygame.draw.rect(screen, (255, 255, 255), (800-self.progress*4, 500, 32, 100), 0)
        if self.progress >= self.production-15:
            if button:
                self.built = True
        if self.progress >= self.production:
            if button == False:
                self.progress = 0

class GameMain():
    """Main Game Class"""
    def __init__(self,width=800,height=600):
        pygame.init()
        pygame.display.set_caption('Manual Control')
        # initializes screen
        self.screen = pygame.display.set_mode([width, height])


    def MainLoop(self):
        self.LoadSprites()

        running = True
        while(running):
            button = False
            clock.tick(60)
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
                self.render(self.screen, assemblerimg, assemblerpng, bearimg)
                factory.step(button,self.screen)

    def render(self,screen,assemberimg,assemblerpng,bearimg):
        screen.blit(assemblerimg, (self.factories[0].x, self.factories[0].y))
        if self.factories[0].built:
            if self.factories[0].t < 30:
                self.factories[0].t += 1
                screen.blit(bearimg, (self.factories[0].x + (assemblerpng.size[0]/2),
                                      ((self.factories[0].y/2)-2*self.factories[0].t) + (assemblerpng.size[1]/2)))
            else:
                self.factories[0].t = 0
                self.factories[0].built = False


    def LoadSprites(self):
        self.factories = []
        for i in range(0, 1):
            producer = Producer('teddybear', 100, 100)
            self.factories.append(producer)




if __name__ == '__main__':
    MainWindow = GameMain()
    MainWindow.MainLoop()
