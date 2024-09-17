import pygame

display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

WINDOW_WIDTH,WINDOW_HEIGHT = pygame.display.Info().current_w,pygame.display.Info().current_h
BOARD_WIDTH,BOARD_HEIGHT = WINDOW_HEIGHT - 150,WINDOW_HEIGHT - 150