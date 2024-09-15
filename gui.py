import pygame
from data import *

display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

WINDOW_WIDTH,WINDOW_HEIGHT = pygame.display.Info().current_w,pygame.display.Info().current_h
BOARD_WIDTH,BOARD_HEIGHT = WINDOW_HEIGHT,WINDOW_HEIGHT

def display_board(display):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2:
                pygame.draw.rect(display,(255,255,255),(WINDOW_WIDTH // 2 - WINDOW_HEIGHT // 2 + col * (BOARD_WIDTH // 8),row * (BOARD_HEIGHT // 8),BOARD_WIDTH // 8,BOARD_HEIGHT // 8))
            else:
                pygame.draw.rect(display,(114,149,83),(WINDOW_WIDTH // 2 - WINDOW_HEIGHT // 2 + col * (BOARD_WIDTH // 8),row * (BOARD_HEIGHT // 8),BOARD_WIDTH // 8,BOARD_HEIGHT // 8))
            
def run():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    
        display.fill((30,30,30))
        display_board(display)
        pygame.display.update()
        
    pygame.quit()

if __name__ == '__main__':
    run()