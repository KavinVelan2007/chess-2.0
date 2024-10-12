import os
from constants import *

sprites = {}

for img_name in os.listdir('sprites'):
    sprites[img_name[1]] = pygame.transform.scale(pygame.image.load(f'sprites/{img_name}').convert_alpha(),(BOARD_WIDTH // 8,BOARD_HEIGHT // 8))
    sprites[img_name[1]].set_alpha(225)
POINTER = pygame.transform.scale(pygame.image.load('sprites/blackpointer.png').convert_alpha(),(BOARD_WIDTH // 8,BOARD_HEIGHT // 8))