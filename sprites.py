import os
from constants import *

sprites = {}

for img_name in os.listdir('sprites'):
    sprites[img_name[1]] = pygame.transform.scale(pygame.image.load(f'sprites/{img_name}'),(BOARD_WIDTH // 8,BOARD_HEIGHT // 8))