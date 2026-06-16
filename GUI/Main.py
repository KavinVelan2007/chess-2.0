import customtkinter as ctk
import pygame
from GUI.SideBar import SideBar
from GUI.Board import Board
import os
from numpy import uint64 as uint
from numpy import uint32
import platform
import brains
import sqlite3
from GUI.Defaults import DEFAULT_BOARD_THEME, DEFAULT_PIECE_THEME
from GUI.MoveHistory import ScrollableCheckBoxFrame
from GUI.Paths import DATABASE_PATH, FEN_STRING_PATH, THEME_PATH
from GUI.WindowUtils import maximize_window

ctk.set_default_color_theme(THEME_PATH)


class Game(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__()
        self.minsize(1280, 720)
        self.title("Chess")
        maximize_window(self)
        self.grid_rowconfigure(0, weight=1)
        self.UserName = kwargs.get("username")
        self.StorePreferences = kwargs.get("store_preferences", True)
        self.SideBarFrame = SideBar(self)
        self.BitBoards, self.BoardData = kwargs["BitBoards"], kwargs["BoardData"]
        self.BoardCanvas = ctk.CTkCanvas(self, width=800, height=800)

        self.MoveHistory = ScrollableCheckBoxFrame(self)

        self.MoveHistory.place(relx=0.8,rely=0.1)

        self.BoardCanvas.place(x=600, y=90)
        self.PieceIndex = {
            6: '♙',
            7: '♘',
            8: '♗',
            9: '♖',
            10: '♕',
            11: '♔',
            0: '♟',
            1: '♞',
            2: '♝',
            3: '♜',
            4: '♛',
            5: '♚',
        }
        self.Display = self.createPygameDisplay()
        self.BoardOptions = [
            "Black-White-Aluminium",
            "Brushed-Aluminium",
            "China-Blue",
            "China-Green",
            "China-Grey",
            "China-Scarlet",
            "China-Yellow",
            "Classic-Blue",
            "Glass",
            "Gold-Silver",
            "Green-Glass",
            "Jade",
            "Light-Wood",
            "Power-Coated",
            "Purple-Black",
            "Rosewood",
            "Wax",
            "Wood-Glass",
        ]
        self.PieceOptions = [
            "Basic",
            "Experimental",
            "Glass",
            "Lord",
            "Metal",
            "Modern",
            "ModernJade",
            "ModernWood",
            "RedVBlue",
            "Tournament",
            "Trimmed",
            "Wax",
            "Wood",
        ]
        self.Pieces = [
            "White-Pawn",
            "White-Knight",
            "White-Bishop",
            "White-Rook",
            "White-Queen",
            "White-King",
            "Black-Pawn",
            "Black-Knight",
            "Black-Bishop",
            "Black-Rook",
            "Black-Queen",
            "Black-King",
        ]
        self.PiecePreference = kwargs.get("piece_preference")
        self.BoardPreference = kwargs.get("board_preference")
        if self.PiecePreference is None or self.BoardPreference is None:
            sqliteobj = sqlite3.connect(DATABASE_PATH)
            pyobj = sqliteobj.cursor()
            pyobj.execute(
                "select piece,board from chess where username = ?",
                (self.UserName,),
            )
            d = pyobj.fetchone()
            sqliteobj.close()
            if d:
                self.PiecePreference, self.BoardPreference = d
            else:
                self.PiecePreference = DEFAULT_PIECE_THEME
                self.BoardPreference = DEFAULT_BOARD_THEME
        self.Board = Board(self)
        self.BaseColour = (
            (26, 26, 26)
            if ctk.get_appearance_mode() == "Dark"
            else (242, 242, 242)
        )
        self.SquareSurface = pygame.Surface((90, 83), pygame.SRCALPHA)
        self.SquareSurface.fill((0, 0, 0))
        self.SquareSurface.set_alpha(200)
        self.x = 40
        self.y = 63
        self.CurrentSquare = None
        self.ActivePoint = None
        self.AgainstAI = True
        self.Turn = "W"
        self.ChessBoardObj = brains.Board(self.BitBoards, self.BoardData)
        self.ValidMoves = self.ChessBoardObj.ReturnMoves()
        with open(FEN_STRING_PATH) as file:
            self.History = [file.read()]
        self.update()
        self.mainloop()

    def createPygameDisplay(self):
        system = platform.system()
        if system == "Windows":
            os.environ["SDL_VIDEODRIVER"] = "windib"
        elif system == "Linux":
            os.environ["SDL_VIDEODRIVER"] = "x11"

        self.update_idletasks()
        self.BoardCanvas.update_idletasks()
        self.BoardCanvas.wait_visibility()
        os.environ["SDL_WINDOWID"] = str(self.BoardCanvas.winfo_id())
        pygame.display.init()
        return pygame.display.set_mode((800, 800), pygame.NOFRAME)

    def update(self):
        if self.AgainstAI and self.Turn == "B":
            self.PlayBestMove()
        
        self.BitBoards = self.ChessBoardObj.bitboards
        self.BoardData = self.ChessBoardObj.board_data
        self.WHITE = self.BLACK = uint(0)
        for i in range(6):
            self.WHITE |= self.BitBoards[i]
        for i in range(6, 12):
            self.BLACK |= self.BitBoards[i]
        self.EventCheck()
        self.Display.fill(self.BaseColour)
        self.Board.drawBoard()
        x, y = pygame.mouse.get_pos()
        x -= self.x
        y -= self.y
        row, col = y // 83, x // 90
        if 0 <= row < 8 and 0 <= col < 8:
            self.Display.blit(
                self.SquareSurface, (self.x + col * 90, self.y + row * 83)
            )
        if self.CurrentSquare:
            row, col = self.CurrentSquare
            self.Display.blit(
                self.SquareSurface, (self.x + col * 90, self.y + row * 83)
            )
            self.showValidMoves()
        self.Board.drawPieces()
        self.showDraggingPiece()
        self.Board.DrawSquarePositions()

        pygame.display.update()

        if not self.ValidMoves and self.ChessBoardObj.check_for_check(1 if self.Turn == 'B' else 0):

            from tkinter import messagebox

            msg = "White" if self.Turn == 'B' else "Black"

            messagebox.showinfo("Game Over",f'{msg} Won!')

            self.SideBarFrame.StartNewGame()

            for i in range(len(self.MoveHistory.label_list)):

                self.MoveHistory.label_list.pop().destroy()

        self.after(1, self.update)

    def PlayBestMove(self):
        import time
        a = time.time()
        move = brains.BestMove(self.ChessBoardObj, 4)
        print(time.time() - a)
        from_index = move & uint32((1 << 6) - 1)
        to_index = (move >> uint32(6)) & uint32((1 << 6) - 1)
        p1 = p2 = False
        for i in range(12):
            if self.ChessBoardObj.bitboards[i] & (uint(1) << from_index):
                p1 = True
            elif self.ChessBoardObj.bitboards[i] & (uint(1) << to_index):
                p2 = True
        self.ChessBoardObj.MakeMove(move)
        self.ValidMoves = self.ChessBoardObj.ReturnMoves()
        self.AddMove(move, p1 and p2)
        self.Turn = 'W' if self.Turn == 'B' else 'B'
        

    def showValidMoves(self):
        if self.CurrentSquare:
            row, col = self.CurrentSquare
            for move in self.ValidMoves:
                from_index = move & uint32((1 << 6) - 1)
                to_index = (move >> uint32(6)) & uint32((1 << 6) - 1)
                if from_index == row * 8 + col:
                    to_row, to_col = to_index // 8, to_index % 8
                    self.Display.blit(
                        self.SquareSurface,
                        (self.x + to_col * 90, self.y + to_row * 83),
                    )

    def AddMove(self, move, isCapture):
        from_index = move & uint32((1 << 6) - 1)
        to_index = (move >> uint32(6)) & uint32((1 << 6) - 1)
        square = f"{chr(97 + to_index % 8)}{8 - to_index // 8}"
        for i in range(12):
            if self.ChessBoardObj.bitboards[i] & (uint(1) << to_index):
                if i in [0, 6]:
                    if isCapture:
                        self.MoveHistory.add_item(chr(97 + from_index % 8) + 'x' + square)
                    else:
                        self.MoveHistory.add_item(square)
                elif i in [5,11]:
                    if int(from_index) - int(to_index) in [2,-2]:
                        self.MoveHistory.add_item('O-O')
                    else:
                        self.MoveHistory.add_item(self.PieceIndex[i] + ('x' if isCapture else '') + square)
                else:
                    self.MoveHistory.add_item(self.PieceIndex[i] + ('x' if isCapture else '') + square)

    def showDraggingPiece(self):
        if self.ActivePoint and self.CurrentSquare:
            x, y = self.ActivePoint
            x -= self.x
            y -= self.y
            row = y // 83
            col = x // 90
            Square = row * 8 + col
            for Piece in range(12):
                x, y = pygame.mouse.get_pos()
                if self.BitBoards[Piece] & (uint(1) << uint(Square)):
                    Sprite = self.Board.Data["PieceOptions"][
                        self.PiecePreference
                    ][self.Pieces[Piece]]
                    self.Display.blit(
                        Sprite,
                        (
                            x - Sprite.get_width() // 2,
                            y - Sprite.get_height() // 2,
                        ),
                    )

    def EventCheck(self):
        for Event in pygame.event.get():
            if Event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x -= self.x
                y -= self.y
                row, col = y // 83, x // 90
                if 0 <= row < 8 and 0 <= col < 8:
                    pos = row * 8 + col
                    if self.Turn == "W":
                        if self.WHITE & (uint(1) << pos):
                            self.CurrentSquare = (row, col)
                            x, y = pygame.mouse.get_pos()
                            self.ActivePoint = (x, y)
                    else:
                        if self.BLACK & (uint(1) << pos) and not self.AgainstAI:
                            self.CurrentSquare = (row, col)
                            x, y = pygame.mouse.get_pos()
                            self.ActivePoint = (x, y)
            elif Event.type == pygame.MOUSEBUTTONUP and self.CurrentSquare:
                row, col = self.CurrentSquare
                x, y = pygame.mouse.get_pos()
                x -= self.x
                y -= self.y
                to_row, to_col = y // 83, x // 90
                for move in self.ValidMoves:
                    from_index = move & uint32((1 << 6) - 1)
                    to_index = (move >> uint32(6)) & uint32((1 << 6) - 1)
                    if (
                        from_index == row * 8 + col
                        and to_index == to_row * 8 + to_col
                    ):
                        p1 = p2 = False
                        for i in range(12):
                            if self.ChessBoardObj.bitboards[i] & (
                                uint(1) << from_index
                            ):
                                p1 = True
                            elif self.ChessBoardObj.bitboards[i] & (
                                uint(1) << to_index
                            ):
                                p2 = True
                        if (move >> uint(16)) & uint(1):
                            self.PromotionPopup(move)
                            self.ValidMoves = self.ChessBoardObj.ReturnMoves()
                            self.AddMove(move, p1 and p2)
                            self.Turn = 'W' if self.Turn == 'B' else 'B'
                            self.CurrentSquare = None
                            break
                        else:
                            self.ChessBoardObj.MakeMove(move)
                            self.ValidMoves = self.ChessBoardObj.ReturnMoves()
                            self.AddMove(move, p1 and p2)
                            self.Turn = 'W' if self.Turn == 'B' else 'B'
                            self.CurrentSquare = None
                self.ActivePoint = None

    def PromotionPopup(self, move):
        popup = ctk.CTkToplevel()
        popup.title('Promotion')
        pieces = ['Queen', 'Rook', 'Knight', 'Bishop']
        for piece in pieces:
            button = ctk.CTkButton(popup, text=piece, command=lambda piece=piece, move=move: self.Promote(piece, move, popup), width=400)
            button.pack()
        popup.mainloop()

    def Promote(self, piece, move, popup):
        popup.destroy()
        popup.quit()
        move &= ~(uint(1 << 17) & uint(1 << 18))
        if piece == 'Queen':
            move |= (uint(1 << 17) | uint(1 << 18))
        elif piece == 'Rook':
            move |= uint(1 << 18)
        elif piece == 'Bishop':
            move |= (uint(1 << 17))
        self.ChessBoardObj.MakeMove(move)
