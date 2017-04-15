import pygame
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CONVEYOR_DIRECTION = 0.3
BUTTON_DICT_M = {1:pygame.K_1, 2:pygame.K_2, 3:pygame.K_3, 4:pygame.K_4, 5:pygame.K_5, 6:pygame.K_6, 7:pygame.K_7, 8:pygame.K_8, 9:pygame.K_9, 0:pygame.K_0}
BUTTON_DICT_TWO = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4, pygame.K_5:5, pygame.K_6:6, pygame.K_7:7, pygame.K_8:8, pygame.K_9:9, pygame.K_0:0}
BPM = 135.0  # Beats Per Minute for the music
BPs = BPM/60  # Beats per second
BPms = BPs/1000  # Beats per ms
msPB = 60000/BPM  # ms per beat
