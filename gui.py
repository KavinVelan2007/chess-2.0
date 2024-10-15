import pygame
import pygame_widgets
from pygame_widgets.animations import Translate
from fen import *


def count_bits(bit_board):
	c = 0
	while bit_board:
		bit_board &= bit_board - 1
		c += 1
	return c


def least_significant_bit_count(bit_board):
	return count_bits((bit_board & -bit_board) - 1)


def global_init():
    import sys
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()

BITBOARDS = list(generate_bitboards_from_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')[0])
            

class GUI:


    def __init__(self):

        pygame.init()
        self.display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Chess")

        self.current_board_theme = 'Green-Glass'
        self.current_piece_theme = 'Glass'
        
        self.init_images()

        self.mainloop()


    def init_images(self):
        self.pieces = ['White-Pawn', 'White-Knight', 'White-Bishop', 'White-Rook', 'White-Queen', 'White-King', 'Black-Pawn', 'Black-Knight', 'Black-Bishop', 'Black-Rook', 'Black-Queen', 'Black-King']
        board_themes = ['Black-White-Aluminium', 'Brushed-Aluminium', 'China-Blue', 'China-Green', 'China-Grey', 'China-Scarlet', 'China-Yellow', 'Classic-Blue', 'Glass', 'Gold-Silver', 'Green-Glass', 'Jade', 'Light-Wood', 'Power-Coated', 'Purple-Black', 'Rosewood', 'Wax', 'Wood-Glass']
        piece_themes = ['Basic', 'Experimental', 'Glass', 'Lord', 'Metal', 'Modern', 'ModernJade', 'ModernWood', 'RedVBlue', 'Tournament', 'Trimmed', 'Wax', 'Wood']
        

        self.piece_images = {}
        self.board_images = {}

        for i in board_themes:
            self.board_images[i] = pygame.image.load(f'Resources\\Boards\\{i}.png').convert_alpha()

        for i in piece_themes:
            self.piece_images[i] = {}
            for j in self.pieces:
                self.piece_images[i][j] = pygame.image.load(f'Resources\\Pieces\\{i}\\{j}.png').convert_alpha()


    def mainloop(self):

        self.running = True

        board_image = pygame.transform.scale_by(self.board_images[self.current_board_theme], 4/7)
        piece_image = self.piece_images[self.current_piece_theme]
        for i in piece_image:
            piece_image[i] = pygame.transform.scale_by(piece_image[i], 0.35)

        self.clock = pygame.time.Clock()

        offset = (560 - 10, ((1080 - 1310 * (4/7)) / 2) - 55)

        bitboards = BITBOARDS.copy()
        
        squares = [None for i in range(64)]

        for i in range(12):
            while bitboards[i]:
                square = least_significant_bit_count(bitboards[i])
                bitboards[i] &= (bitboards[i] - 1)
                squares[square] = piece_image[self.pieces[i]]
        font = pygame.font.SysFont('Arial', 30)

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False
            


            self.display.fill((20, 20, 20))
            self.display.blit(board_image, (560, (1080 - 1310 * (4/7)) / 2))

            for i in range(64):
                if squares[i] != None:
                    self.display.blit(squares[i], ((i % 8) * 100 + offset[0], (i // 8) * 91 + offset[1]))

            self.clock.tick()
            
            self.display.blit(font.render(f'{self.clock.get_fps()}', False, (255, 255, 255)), (0, 0))
            pygame.display.update()

global_init()
GUI()