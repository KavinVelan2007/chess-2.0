import customtkinter as ctk
import pygame
from GUI.SideBar import SideBar
from GUI.Board import Board
import os
import platform

ctk.set_default_color_theme("GUI\\Themes.json")


class Game(ctk.CTk):


    def __init__(self, BitBoards, BoardData):

        super().__init__()

        self.minsize(1280, 720)

        self.title('Chess')

        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(0, weight=1)

        self.SideBarFrame = SideBar(self)

        self.BoardCanvas = ctk.CTkCanvas(self,width=800,height=800)

        self.BoardCanvas.place(x=600,y=90)

        os.environ['SDL_WINDOWID'] = str(self.BoardCanvas.winfo_id())
        
        system = platform.system()
        
        if system == "Windows":
        
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        elif system == "Linux":
        
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        self.Display = pygame.display.set_mode((800, 800),pygame.NOFRAME | pygame.SRCALPHA)

        self.BoardPreference = 'Light-Wood'
        
        self.PiecePreference = 'Glass'

        self.BoardOptions = os.listdir('GUI\\Resources\\Boards')
        
        self.PieceOptions = os.listdir('GUI\\Resources\\Pieces')

        self.Pieces = ['Black-Bishop.png', 'Black-King.png', 'Black-Knight.png', 'Black-Pawn.png', 'Black-Queen.png', 'Black-Rook.png', 'White-Bishop.png', 'White-King.png', 'White-Knight.png', 'White-Pawn.png', 'White-Queen.png', 'White-Rook.png']

        self.Board = Board(self)
        
        self.update()
        
        self.mainloop()


    def update(self):
        
        self.Display.fill((255,0,0))

        self.Board.drawBoard()

        pygame.display.update()

        self.after(1,self.update)