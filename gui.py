from data import *
from sprites import *
from main import *

class Game:
    
    def __init__(self,display):
        self.curr = None
        self.display = display

    def display_board(self,display):
        for row in range(8):
            for col in range(8):
                if (row + col) & 1:
                    pygame.draw.rect(display,(255,255,255,255),((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1)),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))
                else:
                    pygame.draw.rect(display,(86,99,239,255),((WINDOW_WIDTH >> 1) - (BOARD_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1)),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))

    def display_black_pieces(self,display):
        temp = BLACK_BISHOPS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['b'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = BLACK_ROOKS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['r'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = BLACK_QUEEN
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['q'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = BLACK_KNIGHTS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['n'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = BLACK_PAWNS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['p'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = BLACK_KING
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['k'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        
    def display_white_pieces(self,display):
        temp = WHITE_BISHOPS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['B'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = WHITE_ROOKS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['R'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = WHITE_QUEEN
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['Q'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = WHITE_KNIGHTS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['N'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = WHITE_PAWNS
        while temp:
            index = least_significant_bit_count(temp)
            row,col = index >> 3,index % 8
            display.blit(sprites['P'],((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
            temp &= temp - uint(1)
        temp = WHITE_KING
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
            surface.fill((255,255,255) if (row + col) & 1 else (86,99,239))
            surface.set_alpha(100)
            if (uint(1) << uint(index)) & self.white_pieces or (uint(1) << uint(index)) & self.black_pieces:
                pygame.draw.circle(surface,(0,0,0,200),(BOARD_WIDTH >> 4,BOARD_HEIGHT >> 4),BOARD_WIDTH >> 4,12)
            else:
                pygame.draw.circle(surface,(0,0,0,200),(BOARD_WIDTH >> 4,BOARD_HEIGHT >> 4),BOARD_WIDTH >> 5)
            x,y = (WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))
            display.blit(surface,(x,y))
            moves &= moves - uint(1)

    def run(self):
        global BLACK_BISHOPS,BLACK_KING,BLACK_KNIGHTS,BLACK_QUEEN,BLACK_ROOKS,BLACK_PAWNS
        global WHITE_BISHOPS,WHITE_KING,WHITE_KNIGHTS,WHITE_QUEEN,WHITE_ROOKS,WHITE_PAWNS
        run = True
        while run:
            self.bitboard = (WHITE_PAWNS,WHITE_KNIGHTS,WHITE_BISHOPS,WHITE_ROOKS,WHITE_QUEEN,WHITE_KING,BLACK_PAWNS,BLACK_KNIGHTS,BLACK_BISHOPS,BLACK_ROOKS,BLACK_QUEEN,BLACK_KING)
            self.white_pieces = WHITE_PAWNS | WHITE_KNIGHTS | WHITE_BISHOPS | WHITE_ROOKS | WHITE_QUEEN | WHITE_KING
            self.black_pieces = BLACK_PAWNS | BLACK_KNIGHTS | BLACK_BISHOPS | BLACK_ROOKS | BLACK_QUEEN | BLACK_KING
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        for i in range(48,56):
                            if self.curr and i == (self.curr[0] * 8 + self.curr[1]):
                                self.curr = None
                            WHITE_PAWNS -= (uint(1) << uint(i))
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
                self.display.blit(POINTER,((WINDOW_WIDTH >> 1) - (BOARD_WIDTH >> 1) + self.curr[1] * (BOARD_WIDTH >> 3),self.curr[0] * (BOARD_HEIGHT >> 3) + ((WINDOW_HEIGHT >> 1) - (BOARD_HEIGHT >> 1))))
                self.display_moves(self.curr)
                
            # DISPLAYLING PIECES
            self.display_black_pieces(self.display)
            self.display_white_pieces(self.display)

            pygame.display.update()
            
        pygame.quit()

if __name__ == '__main__':
    game = Game(display)
    game.run()