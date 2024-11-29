import customtkinter as ctk
import pygame
from GUI.SideBar import SideBar
from GUI.Board import Board
import os
import platform


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

        self.update()

        self.mainloop()


    def update(self):

        self.Display.fill(self.BaseColour)

        self.Board.drawBoard()

        pygame.display.update()

        self.after(1, self.update)
