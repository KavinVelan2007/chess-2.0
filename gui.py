from data import *
from sprites import *
from main import *

def display_board(display):
    for row in range(8):
        for col in range(8):
            if (row + col) & 1:
                pygame.draw.rect(display,(255,255,255),((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))
            else:
                pygame.draw.rect(display,(114,149,83),((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3))

def display_black_pieces(display):
    temp = BLACK_BISHOPS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['b'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = BLACK_ROOKS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['r'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = BLACK_QUEEN
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['q'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = BLACK_KNIGHTS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['n'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = BLACK_PAWNS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['p'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = BLACK_KING
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['k'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    
def display_white_pieces(display):
    temp = WHITE_BISHOPS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['B'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = WHITE_ROOKS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['R'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = WHITE_QUEEN
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['Q'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = WHITE_KNIGHTS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['N'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = WHITE_PAWNS
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['P'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)
    temp = WHITE_KING
    while temp:
        index = least_significant_bit_count(temp)
        row,col = index >> 3,index % 8
        display.blit(sprites['K'],((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + col * (BOARD_WIDTH >> 3),row * (BOARD_HEIGHT >> 3)))
        temp &= temp - uint(1)

def run():
    global BLACK_BISHOPS,BLACK_KING,BLACK_KNIGHTS,BLACK_QUEEN,BLACK_ROOKS,BLACK_PAWNS
    global WHITE_BISHOPS,WHITE_KING,WHITE_KNIGHTS,WHITE_QUEEN,WHITE_ROOKS,WHITE_PAWNS
    run = True
    curr = None
    while run:
        bitboard = WHITE_BISHOPS | WHITE_KING | WHITE_KNIGHTS | WHITE_QUEEN | WHITE_ROOKS | WHITE_PAWNS
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                x -= (WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1)
                row,col = y // (BOARD_HEIGHT >> 3),x // (BOARD_WIDTH >> 3)
                if bitboard & (uint(1) << uint((row << 3) + col)):
                    curr = (row,col)
        display.fill((30,30,30))
        display_board(display)
        display_black_pieces(display)
        display_white_pieces(display)
        
        if curr:
            pygame.draw.rect(display,(255,0,0),((WINDOW_WIDTH >> 1) - (WINDOW_HEIGHT >> 1) + curr[1] * (BOARD_WIDTH >> 3),curr[0] * (BOARD_HEIGHT >> 3),BOARD_WIDTH >> 3,BOARD_HEIGHT >> 3),3)
        
        pygame.display.update()
        
    pygame.quit()

if __name__ == '__main__':
    run()