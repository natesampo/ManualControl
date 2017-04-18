import pygame
try:
    import android
except ImportError:
    android = None
from PIL import Image
import os, sys, math, random
from Producer import Producer
from Conveyor import Conveyor
from Game_Constants import *
import math
import random

clock = pygame.time.Clock()
myMusic = pygame.mixer.music

imagespath = os.path.join(os.path.dirname(__file__), 'images')
assemblerimg = [0,0,0,0]
assemblerimg[0] = pygame.image.load(os.path.join(imagespath, "factory_cyan.png"))
assemblerimg[1] = pygame.image.load(os.path.join(imagespath, "factory_blue.png"))
assemblerimg[2] = pygame.image.load(os.path.join(imagespath, "factory_green.png"))
assemblerimg[3] = pygame.image.load(os.path.join(imagespath, "factory_gray.png"))
bearimg = [0,0,0,0]
bearimg[0] = pygame.image.load(os.path.join(imagespath, "Production1.png"))
bearimg[1] = pygame.image.load(os.path.join(imagespath, "Production2.png"))
bearimg[2] = pygame.image.load(os.path.join(imagespath, "Production3.png"))
bearimg[3] = pygame.image.load(os.path.join(imagespath, "Production4.png"))

class GameMain():
    """Main Game Class"""
    def __init__(self,width=WINDOW_WIDTH,height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption('Manual Control')
        # initializes screen
        self.screen = pygame.display.set_mode([width, height])
        self.x_view = 200
        self.y_view = self.x_view * 3/4
        self.level = 1
        self.score = 0
        self.health = 100
        self.quota = 0
        self.sleeping = False  # checks if the app is sleeping
        self.straightImages = []
        self.turnImages = []
        for i in range(1,15):
            self.straightImages.append(pygame.image.load(os.path.join(imagespath, 'ConveyorBelt%s.png' % i)))
        for i in range(1,5):
            self.turnImages.append(pygame.image.load(os.path.join(imagespath, 'Turn%s.png' % i)).convert_alpha())
        self.conveyorImg = pygame.image.load(os.path.join(imagespath, 'ConveyorBelt1.png'))
    def MainLoop(self):
        self.button_dict = {}
        self.scale = 40000/self.x_view
        self.filledSpaces = [] # add coordinate tuples whenever a space if filled e.g. (x, y)
        self.setRhythms(self.level) # 4 rhythms, each expressed as a array of 8 ones or zeros (for each 8th note beat)
        self.quota = self.score+100*sum(map(lambda r: sum(r), self.rhythms))-200

        # sprite groups so we can render everything all at once
        self.allConveyorSprites = pygame.sprite.Group()
        self.factories = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.allConveyorSprites,self.factories)

        #Background music from the following music
        #http://audionautix.com/?utm_campaign=elearningindustry.com&utm_source=%2Fultimate-list-free-music-elearning-online-education&utm_medium=link
        myMusic.load(os.path.join(os.path.dirname(__file__), 'BigCarTheft.ogg'))
        myMusic.play(-1)
        self.songTime = 0  # how far along in the song the system thinks we are in ms
        self.lastReportedPlayheadPosition = 0  # the last reported song position from the mixer
        self.beatStep = 0
        self.beatProgress = 0  # number of beats that have passed
        self.beatPos = 0  # position inside our current beat
        self.renderTeddy = False
        self.counter= 0
        self.frameCounter = 0
        self.fps = 0
        self.timePassed = 0
        self.displayDebug = False
        self.beatAlternate = True
        self.gamestart = False

        while not self.gamestart:
            self.screen.fill((20, 20, 20))  # setting background color
            font ="norasi"
            font_size1 = 100
            font_size2 = 30
            k = 250
            if self.health <= 0:
                msg1 = "Game Over"
                msg2 = "PRESS ENTER TO TRY AGAIN"
                msg3 = "Final Score: " + str(self.score)
                msg4 = "Final Level: " + str(self.level)
                msg_location1 = (120+k,100)
                msg_location2 = (165+k,300)
                msg_location3 = (270+k,370)
                msg_location4 = (270+k,420)
                self.MsgRender(self.screen, font, font_size2, msg3, msg_location3,(255,255,255))
                self.MsgRender(self.screen, font, font_size2, msg4, msg_location4,(255,255,255))
            elif self.level == 1:
                msg1 = "Manual Control"
                msg2 = "PRESS ENTER TO ENJOY!"
                msg_location1 = (40+k,100)
                msg_location2 = (210+k,300)
            else:
                msg1 = "Level " + str(self.level)
                msg2 = "PRESS ENTER TO CONTINUE!"
                msg_location1 = (230+k,100)
                msg_location2 = (170+k,300)

            self.MsgRender(self.screen, font, font_size1, msg1, msg_location1,(255,255,255))
            self.MsgRender(self.screen, font, font_size2, msg2, msg_location2,(255,255,255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.gamestart = True
                        self.lastFactory = Producer('teddybear',self,assemblerimg[0],0,0)
                        self.factories.add(self.lastFactory)
                        self.lastBeatProgress = self.beatProgress+16
                        if self.health <= 0:
                            self.score = 0
                            self.quota = 200
                            self.level = 1
                        self.health = 100

                if event.type == pygame.QUIT:
                    pygame.display.quit()

            pygame.display.flip()

        while self.gamestart:
            self.scale = 40000.0/self.x_view
            self.x_view += 0.125
            self.y_view += 3/32
            button = False
            if self.health <= 0: # game over
                print("died")
                self.health = -1000
                self.x_view = 200
                self.y_view = self.x_view * 3/4
                self.MainLoop()
                return
            if self.score >= self.quota and self.health > 0:
                self.level += 1
                self.score += self.health
                self.x_view = 200
                self.y_view = self.x_view * 3/4
                self.MainLoop() #TODO: This is actually terrible
                return

            # frameTimeDifference attribute keeps track of the time passed between this frame and the last
            self.frameTimeDifference = clock.tick(120)  #clock.tick also is limiting the frame rate to 60fps

            self.checkEvents()
            self.checkFPS()
            self.trackSongPos()  # smooths out accuracy of song position

            pygame.display.update()  # updates the display to show everything that has been drawn/blit

            # add a factory
            if self.beatProgress-self.lastBeatProgress > 16:
                producer = self.addFactory(self.lastFactory.x, self.lastFactory.y)
                conveyor = Conveyor(producer, self.lastFactory, producer.x, producer.y,self)
                self.lastFactory = producer
                self.lastBeatProgress = self.beatProgress

            # draws sprites onto the screen
            self.screen.fill((20, 20, 20))  # setting background color
            self.allConveyorSprites.draw(self.screen)

            for factory in self.factories.sprites():
                for conveyor in factory.conveyors:
                    self.conveyor_render(self.screen, conveyor)
            self.factories.draw(self.screen)
            for factory in self.factories:
                self.factory_render(self.screen, factory)
                if self.onScreen(factory.x, factory.y):
                    factory.step(pygame.key.get_pressed()[factory.button], self.beatProgress%4-2)
                    if factory.button not in list(self.button_dict.keys()):
                        self.button_dict[factory.button] = factory
                if factory in list(self.button_dict.values()):
                    place = list(self.button_dict.values()).index(factory)
                    self.prod_render(self.screen, factory, place)

            # Display score
            if pygame.font:
                font = pygame.font.Font(None, 40)
                text1 = font.render("Score: %s" % self.score,1,(255,255,0))
                text2 = font.render("Level: %s" % self.level,1,(255,255,0))
                text3 = font.render("Health: %s" % self.health,1,(255,255,0))
                textpos1 = text1.get_rect(top=10, right = self.screen.get_width()-20)
                textpos2 = text2.get_rect(top=50, right = self.screen.get_width()-20)
                textpos3 = text3.get_rect(top=90, right = self.screen.get_width()-20)
                self.screen.blit(text1, textpos1)
                self.screen.blit(text2, textpos2)
                self.screen.blit(text3, textpos3)

            #  displays Debug
            if self.displayDebug:
                #self.renderDebug()
                pass


    def MsgRender(self,screen,font,font_size,msg,msg_location,color):
        myfont = pygame.font.SysFont(font, font_size, True)
        label = myfont.render(msg, True, color)
        screen.blit(label, msg_location)

    def checkEvents(self):
        for event in pygame.event.get():
            if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if self.screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
                else:
                    pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.FULLSCREEN | pygame.HWSURFACE)
            if event.type is pygame.KEYDOWN and event.key == pygame.K_F3:
                self.displayDebug = not self.displayDebug

            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                screen = pygame.display.set_mode(( 1280, 720))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.gamestart == False:
                self.gamestart = True
                if self.health <= 0:
                    self.health = 200
                    self.score = 0
                    self.quota = 200
                    self.level = 1

    def checkFPS(self):
        self.frameCounter+=1
        self.timePassed += self.frameTimeDifference
        if self.timePassed >= 1000:
            self.fps = int(self.frameCounter/(self.timePassed/1000))
            self.frameCounter = 0
            self.timePassed = 0

    def renderDebug(self):
        if pygame.font:
            font = pygame.font.Font(None, 24)
            text = font.render("fps: %s" % self.fps,1,(255,255,0))
            textpos = text.get_rect(top=10, right = self.screen.get_width()-10)
            self.screen.blit(text, textpos)
            self.checkBeat()

    def checkBeat(self):
        if self.beatPos < .05:  # we are in the beginning of the beat
            self.renderTeddy = True
        if self.renderTeddy:
            if self.counter < 10:
                self.counter +=1
                pygame.draw.rect(self.screen,(255,61,61),(self.screen.get_width()-50,50,30,30),0)
            else:
                self.counter = 0
                self.renderTeddy = False


    def trackSongPos(self):
        self.beatStep = self.frameTimeDifference*BPms
        self.beatProgress += self.beatStep
        self.beatPos = self.beatProgress - int(self.beatProgress)

        self.songTime += self.frameTimeDifference
        if(not myMusic.get_pos()==self.lastReportedPlayheadPosition):
            # sets songTime to an average of itself and the position the mixer says the music is
            self.songTime = (self.songTime + myMusic.get_pos())/2
            self.lastReportedPlayheadPosition = myMusic.get_pos()


    def prod_render(self, screen, factory, place):
        for i, prog in enumerate(factory.progress):
            progress = 150*prog
            pygame.draw.rect(screen, (255, 255, 255), (32*place + 16, 32+progress, 16, 16), 0)
            pygame.draw.rect(screen, (255, 255, 255), (32*place, 150+32+16, 48, 4), 0)
            if factory.built[i] and factory.t < 10:
                s = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
                s.set_alpha(128)
                s.set_colorkey((0,0,0))
                pygame.draw.circle(s, (255,255,255,128), (32*place + 24, int(40+progress)), int((5+factory.t)*3), 10)
                screen.blit(s, (0,0))


    def factory_render(self, screen, factory):
        # Render inputs to factory
        # Render factory
        img = pygame.transform.scale(assemblerimg[BUTTON_DICT_TWO[factory.button]-1], (int(self.scale), int(self.scale)))
        factory.image = img
        factory.rect.topleft  = (WINDOW_WIDTH/2 + self.scale*(factory.x-.5), WINDOW_HEIGHT/2 + self.scale*(factory.y-.5))
        #screen.blit(img, (WINDOW_WIDTH/2 + self.scale*(factory.x-.5), WINDOW_HEIGHT/2 + self.scale*(factory.y-.5)))
        # Render output of factory
        if sum(factory.built):
            if factory.t < 20:
                factory.t += 0.5
                img = pygame.transform.scale(bearimg[BUTTON_DICT_TWO[factory.button]-1], (int(self.scale/2), int(self.scale/2)))
                screen.blit(img, (WINDOW_WIDTH/2 + self.scale*(factory.x - .25), WINDOW_HEIGHT/2 + self.scale*(factory.y - .45 - factory.t/100.0)))
            else:
                factory.t = 0
                factory.built = [0]*sum(factory.rhythm)

    def conveyor_render(self, screen, conveyor):
        conveyor.update(self.scale, screen)


    def addFactory(self, last_x = 0, last_y = 0):
        randx = random.random()-.5
        signx = -1 if randx<0 else 1
        randy = random.random()-.5
        signy = -1 if randy<0 else 1
        if 1:#random.random()>.5:
            x = round(randx*WINDOW_WIDTH/self.scale)
            y = round(randy*WINDOW_HEIGHT/self.scale)
        else:
            x = round(signx*((abs(randx)**2)*(WINDOW_WIDTH/self.scale*4)) + last_x)
            y = round(signy*(2+(abs(randy)**2)*(WINDOW_HEIGHT/self.scale*4)) + last_y)
        if (x, y) in self.filledSpaces:
            return self.addFactory(last_x, last_y)
        else:
            bmax = len(self.button_dict)+1
            b = math.floor(random.random()*4)+1
            if b > bmax: b = bmax
            producer = Producer(self.getType(), self, assemblerimg[int(b)-1], x, y, button=BUTTON_DICT_M[b])
            self.factories.add(producer)
            self.filledSpaces.append((x,y))
            return producer


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
        self.rhythms = [0]*4
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
                    self.rhythms[i][int(r1*4)*2+1] = 1
                elif difficulty-i <= 5:
                    r1 = int(r1*4)*2
                    r2 = int(r2*3)*2
                    if r2>=r1: r2 += 1
                    self.rhythms[i][r1] = 1
                    self.rhythms[i][r2] = 1
                elif difficulty-i <= 6:
                    r1 = int(r1*8)
                    r2 = int(r2*7)
                    if r2>=r1: r2 += 1
                    self.rhythms[i][r1] = 1
                    self.rhythms[i][r2] = 1
                elif difficulty-i <= 9:
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

def main():
    sys.setrecursionlimit(5000)
    MainWindow = GameMain()
    MainWindow.MainLoop()
if __name__ == '__main__':
    main()
