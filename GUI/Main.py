import customtkinter as ctk
import pygame
from GUI.SideBar import SideBar
from GUI.Board import Board
import os
from numpy import uint64 as uint
from numpy import uint32
import platform
import brains


ctk.set_default_color_theme("GUI\\Themes.json")


class Game(ctk.CTk):


    def __init__(self, **kwargs):

        super().__init__()

        self.minsize(1280, 720)

        self.title('Chess')

        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(0, weight=1)

        self.SideBarFrame = SideBar(self)

        self.BitBoards, self.BoardData = kwargs["BitBoards"], kwargs["BoardData"]

        self.BoardCanvas = ctk.CTkCanvas(self, width=800, height=800)

        self.BoardCanvas.place(x=600, y=90)

        os.environ['SDL_WINDOWID'] = str(self.BoardCanvas.winfo_id())

        system = platform.system()

        if system == "Windows":

            os.environ['SDL_VIDEODRIVER'] = 'windib'

        elif system == "Linux":

            os.environ['SDL_VIDEODRIVER'] = 'x11'

        self.Display = pygame.display.set_mode(
            (800, 800), pygame.NOFRAME)

        self.BoardPreference = 'Light-Wood'

        self.PiecePreference = 'Glass'

        self.BoardOptions = ['Black-White-Aluminium', 'Brushed-Aluminium', 'China-Blue', 'China-Green', 'China-Grey', 'China-Scarlet', 'China-Yellow',
                             'Classic-Blue', 'Glass', 'Gold-Silver', 'Green-Glass', 'Jade', 'Light-Wood', 'Power-Coated', 'Purple-Black', 'Rosewood', 'Wax', 'Wood-Glass']

        self.PieceOptions = ['Basic', 'Experimental', 'Glass', 'Lord', 'Metal', 'Modern',
                             'ModernJade', 'ModernWood', 'RedVBlue', 'Tournament', 'Trimmed', 'Wax', 'Wood']

        self.Pieces = ['White-Pawn', 'White-Knight', 'White-Bishop', 'White-Rook', 'White-Queen', 'White-King',
                       'Black-Pawn', 'Black-Knight', 'Black-Bishop', 'Black-Rook', 'Black-Queen', 'Black-King']
                       

        self.Board = Board(self)

        self.BaseColour = (26, 26, 26) if ctk.get_appearance_mode() == "Dark" else (242, 242, 242)

        self.SquareSurface = pygame.Surface((90,83),pygame.SRCALPHA)
        self.SquareSurface.fill((0,0,0))
        self.SquareSurface.set_alpha(200)

        self.x = 40
        self.y = 63

        self.CurrentSquare = None

        self.ActivePoint = None

        self.ChessBoardObj = brains.Board(self.BitBoards,self.BoardData)

        self.ValidMoves = self.ChessBoardObj.return_moves()

        self.update()

        self.mainloop()


    def update(self):

        self.WHITE = self.BLACK = uint(0)
        for i in range(6):
            self.WHITE |= self.BitBoards[i]
        for i in range(6, 12):
            self.BLACK |= self.BitBoards[i]

        self.EventCheck()

        self.Display.fill(self.BaseColour)

        self.Board.drawBoard()

        x,y = pygame.mouse.get_pos()
        x -= self.x
        y -= self.y
        row,col = y // 83,x // 90
        if 0 <= row < 8 and 0 <= col < 8:
            self.Display.blit(self.SquareSurface,(self.x + col * 90,self.y + row * 83))

        if self.CurrentSquare:

            row,col = self.CurrentSquare

            self.Display.blit(self.SquareSurface,(self.x + col * 90,self.y + row * 83))

            self.showValidMoves()

        self.Board.drawPieces()

        self.showDraggingPiece()

        pygame.display.update()

        self.after(1, self.update)

    def showValidMoves(self):

        if self.CurrentSquare:

            row,col = self.CurrentSquare
            for move in self.ValidMoves.return_move_list():
                from_index = move & uint32((1 << 6) - 1)
                to_index = (move >> uint32(6)) & uint32((1 << 6) - 1)
                if from_index == row * 8 + col:
                    to_row,to_col = to_index // 8, to_index % 8
                    self.Display.blit(self.SquareSurface,(self.x + to_col * 90,self.y + to_row * 83))

    def showDraggingPiece(self):
        if self.ActivePoint:

            x,y = self.ActivePoint
            x -= self.x
            y -= self.y
            row = y // 83
            col = x // 90

            Square = row * 8 + col

            for Piece in range(12):
                x,y = pygame.mouse.get_pos()
                if self.BitBoards[Piece] & (uint(1) << uint(Square)):
                    Sprite = self.Board.Data["PieceOptions"][self.PiecePreference][self.Pieces[Piece]]
                    self.Display.blit(
                        Sprite,
                        (x - Sprite.get_width() // 2, y - Sprite.get_height() // 2))

    def EventCheck(self):

        for Event in pygame.event.get():

            if Event.type == pygame.MOUSEBUTTONDOWN:

                x,y = pygame.mouse.get_pos()
                self.ActivePoint = (x,y)
                x -= self.x
                y -= self.y
                row,col = y // 83,x // 90
                if 0 <= row < 8 and 0 <= col < 8:
                    pos = row * 8 + col
                    if self.WHITE & (uint(1) << pos):
                        self.CurrentSquare = (row,col)
                    
            elif Event.type == pygame.MOUSEBUTTONUP:

                self.ActivePoint = None