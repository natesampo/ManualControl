import pygame
from PIL import Image
import os, sys

class Producer():
    def __init__(self, product, x=-1, y=-1, progress=0, production=100, built=False):
        self.product = product
        self.x = x
        self.y = y
        self.progress = progress
        self.production = production
        self.built = built
        self.t = 0
        self.p = 0

    def render(self, screen, assemblerimg, assemblerpng, bearimg):
        screen.blit(assemblerimg, (self.x, self.y))
        if self.built:
            if self.t < 30:
                self.t += 1
                screen.blit(bearimg, (self.x + (assemblerpng.size[0]/2), ((self.y/2)-2*self.t) + (assemblerpng.size[1]/2)))
            else:
                self.t = 0
                self.built = False

    def step(self, button):
        self.progress += 3
        pygame.draw.rect(screen, (255, 255, 255), (self.progress*4, 500, 32, 100), 0)
        pygame.draw.rect(screen, (255, 255, 255), (800-self.progress*4, 500, 32, 100), 0)
        if self.progress >= self.production-15:
            if button:
                self.built = True
        if self.progress >= self.production:
            if button == False:
                self.progress = 0



if __name__ == '__main__':
    factories = []
    for i in range(0, 1):
        producer = Producer('teddybear', 100, 100)
        factories.append(producer)

    pygame.init()
    pygame.display.set_caption('Manual Control')
    screen = pygame.display.set_mode([800, 600])
    clock = pygame.time.Clock()

    im = Image.open('TeddyBear.jpg')
    im.thumbnail((64, 64), Image.ANTIALIAS)
    im.save('ThisGuy.jpg', "JPEG")
    assemblerpng = Image.open('Assembler.png')

    assemblerimg = pygame.image.load('Assembler.png')
    bearimg = pygame.image.load('ThisGuy.jpg')

    running = True
    while(running):
        button = False
        clock.tick(60)
        pygame.display.update()
        screen.fill((160, 82, 45))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_0]:
                button = True
        for f in factories:
            f.render(screen, assemblerimg, assemblerpng, bearimg)
            f.step(button)
