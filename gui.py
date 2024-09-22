from sprites import *
from main import *
from utils import *

class Game:
    
    def __init__(self,display):
        self.curr = None
        self.display = display
        self.halfMoves = halfMoves
        self.data = data
        self.black_bishops = BLACK_BISHOPS
        self.white_bishops = WHITE_BISHOPS
        self.black_pawns = BLACK_PAWNS
        self.white_pawns = WHITE_PAWNS
        self.black_queen = BLACK_QUEEN
        self.white_queen = WHITE_QUEEN
        self.black_knights = BLACK_KNIGHTS
        self.white_knights = WHITE_KNIGHTS
        self.black_king = BLACK_KING
        self.white_king = WHITE_KING
        self.black_rooks = BLACK_ROOKS
        self.white_rooks = WHITE_ROOKS

    def display_board(self,display):
        for row in range(8):
            for col in range(8):
                if (row + col) & 1 == 0:
                    pygame.draw.rect(display,(255,255,255,255),((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1)),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))
                else:
                    pygame.draw.rect(display,(86,99,239,255),((WINDOW_WIDTH >> 1) - (BOARD_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1)),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))

    def display_black_pieces(self,display):
        temp = self.black_bishops
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['b'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.black_rooks
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['r'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.black_queen
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['q'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.black_knights
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['n'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.black_pawns
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['p'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.black_king
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['k'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        
    def display_white_pieces(self,display):
        temp = self.white_bishops
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['B'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.white_rooks
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['R'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.white_queen
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['Q'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.white_knights
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['N'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.white_pawns
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['P'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = self.white_king
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['K'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)

    def display_moves(self,curr):
        moves = return_moves(curr[0] * 8 + curr[1],self.bitboard)
        while moves:
            index = least_significant_bit_count(moves)
            row,col = index // 8,index % 8
            surface = pygame.Surface((BOARD_WIDTH // 8,BOARD_HEIGHT // 8),pygame.SRCALPHA)
            surface.fill((255,255,255) if (row + col) & 1 == 0 else (86,99,239))
            surface.set_alpha(100)
            if (uint(1) << uint(index)) & self.white_pieces or (uint(1) << uint(index)) & self.black_pieces:
                pygame.draw.circle(surface,(0,0,0,200),(BOARD_WIDTH >> 4,BOARD_HEIGHT >> 4),BOARD_WIDTH >> 4,12)
            else:
                pygame.draw.circle(surface,(0,0,0,200),(BOARD_WIDTH >> 4,BOARD_HEIGHT >> 4),BOARD_WIDTH >> 5)
            x,y = (WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))
            display.blit(surface,(x,y))
            moves &= moves - uint(1)

    def run(self):
        run = True
        while run:
            self.bitboard = (self.white_pawns,self.white_knights,self.white_bishops,self.white_rooks,self.white_queen,self.white_king,self.black_pawns,self.black_knights,self.black_bishops,self.black_rooks,self.black_queen,self.black_king)
            self.white_pieces = self.white_pawns | self.white_knights | self.white_bishops | self.white_rooks | self.white_queen | self.white_king
            self.black_pieces = self.black_pawns | self.black_knights | self.black_bishops | self.black_rooks | self.black_queen | self.black_king
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(WINDOW_WIDTH - 50,0,50,50).collidepoint(pygame.mouse.get_pos()):
                        run = False
                    x,y = pygame.mouse.get_pos()
                    x -= (WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1)
                    y -= (WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1)
                    row,col = y // (BOARD_HEIGHT >> 3),x // (BOARD_WIDTH >> 3)
                    if self.white_pieces & (uint(1) << uint((row << 3) + col)):
                        self.curr = (row,col)
            display.fill((30,30,30,255))
            
            # DISPLAYING BOARD
            self.display_board(self.display)

            # DISPLAYING WINDOW CLOSE BUTTON
            pygame.draw.rect(self.display,(255,0,0),(WINDOW_WIDTH - 50,0,50,50),0,0,0,0,5)
            pygame.draw.line(self.display,(255,255,255),(WINDOW_WIDTH,0),(WINDOW_WIDTH - 47,47),3)
            pygame.draw.line(self.display,(255,255,255),(WINDOW_WIDTH - 50,0),(WINDOW_WIDTH,47),3)
            
            if self.curr:
                # DISPLAY POINTER
                row,col = self.curr
                self.display.blit(POINTER,((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
                self.display_moves(self.curr)
                
            # DISPLAYLING PIECES
            self.display_black_pieces(self.display)
            self.display_white_pieces(self.display)

            pygame.display.update()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game(display)
    game.run()