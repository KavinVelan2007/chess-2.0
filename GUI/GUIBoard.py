import pygame

from main import ReturnMoves


class Board:


    def __init__(self, ParentObject):

        self.Display = ParentObject.Display

        self.ParentObject = ParentObject

        self.FullRect = pygame.Rect(100, 0, 1136, 1080)

        self.BoardCoordinates = (228, 128)

        self.PieceOffset = (-20, -72)

        self.SquareSize = (110, 100)

        self.BoardRect = pygame.Rect(228, 132, 880, 800)

        self.Dragging = False

        self.CurrDragLocation = None

        self.PiecesPresent = [None for i in range(64)]

        self.SideToMove = False

        self.CurrDragPieceLocation = None

        self.InitImages()


    def count_bits(self, bit_board):

        c = 0

        while bit_board:

            bit_board &= bit_board - 1

            c += 1

        return c


    def least_significant_bit_count(self, bit_board):

        return self.count_bits((bit_board & -bit_board) - 1)


    def DisplayPieces(self):

        self.PiecesPresent = [None for i in range(64)]

        for i in range(12):

            CurrentBitboard = self.ParentObject.BitBoards[i]

            while CurrentBitboard:

                CurrentSquare = self.least_significant_bit_count(CurrentBitboard)

                if 0 <= i <= 5:

                    self.PiecesPresent[CurrentSquare] = False # type: ignore

                else:

                    self.PiecesPresent[CurrentSquare] = True # type: ignore

                CurrentBitboard &= CurrentBitboard - 1

                CurrentBlitPosition = (
                    (CurrentSquare % 8) * self.SquareSize[0]
                    + self.BoardCoordinates[0]
                    + self.PieceOffset[0],
                    (CurrentSquare // 8) * self.SquareSize[1]
                    + self.BoardCoordinates[1]
                    + self.PieceOffset[1],
                )

                self.ParentObject.Display.blit(
                    self.Data["PieceOptions"][self.ParentObject.PiecePreference][
                        self.ParentObject.Pieces[i]
                    ],
                    CurrentBlitPosition,
                )


    def DisplayBoard(self):

        pygame.draw.rect(self.ParentObject.Display, (218, 109, 66), self.FullRect)

        self.ParentObject.Display.blit(self.WoodTexture, self.FullRect)

        pygame.draw.line(self.Display, (170, 170, 170), (102, 0), (102, 1080), width=5)

        pygame.draw.line(
            self.ParentObject.Display, (170, 170, 170), (1231, 0), (1231, 1080), width=5
        )

        self.ParentObject.Display.blit(self.Data["BoardOptions"][self.ParentObject.BoardPreference], self.BoardCoordinates)

        self.DisplayPieces()


    def InitImages(self):

        self.WoodTexture = pygame.transform.scale(
            pygame.image.load("GUI\\Resources\\Misc\\WoodTexture.png"), (1136, 1080)
        ).convert_alpha()

        self.Data = {"BoardOptions": {}, "PieceOptions": {}}

        for i in self.ParentObject.BoardOptions:

            self.Data["BoardOptions"][i] = pygame.transform.scale(
                pygame.image.load(f"GUI\\Resources\\Boards\\{i}.png"), (880, 824)
            ).convert_alpha()

        for i in self.ParentObject.PieceOptions:

            self.Data["PieceOptions"][i] = {}

            for j in self.ParentObject.Pieces:

                self.Data["PieceOptions"][i][j] = pygame.transform.scale(
                    pygame.image.load(f"GUI\\Resources\\Pieces\\{i}\\{j}.png"),
                    (154, 197),
                ).convert_alpha()


    def RefreshMoves(self):

        Moves = ReturnMoves(self.ParentObject.BitBoards, self.ParentObject.BoardData)

        BoardPossibleMoves = [() for i in range(64)]

        for Move in Moves['move_list']:

            SourceSquare = Move & 63

            TargetSquare = (Move >> 6) & 63

            BoardPossibleMoves[SourceSquare] += (TargetSquare, )

        return BoardPossibleMoves


    def BoardEventCheck(self, Event):

        if self.BoardRect.collidepoint(pygame.mouse.get_pos()) and Event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

            CurrentPos = pygame.mouse.get_pos()

            CurrentSquare = (
                (CurrentPos[0] - self.BoardRect.x) // self.SquareSize[0]
                + (CurrentPos[1] - self.BoardRect.y) // self.SquareSize[1] * 8
            )

            BoardSquareMoves = self.RefreshMoves()
            
            if BoardSquareMoves[CurrentSquare]:

                self.Dragging = True

                self.CurrDragLocation = CurrentSquare

                self.CurrDragPieceLocation = CurrentSquare

        elif Event.type == pygame.MOUSEBUTTONUP and self.BoardRect.collidepoint(pygame.mouse.get_pos()) and self.Dragging:

            self.Dragging = False

            self.CurrDragLocation = None

            self.CurrDragPieceLocation = None

            self.CurrDragPieceLocation = None

        elif self.Dragging and Event.type == pygame.MOUSEMOTION:

            self.CurrDragLocation = pygame.mouse.get_pos()
        
        else:

            if self.Dragging:
            
                self.Dragging = False

                self.CurrDragLocation = None

                self.CurrDragPieceLocation = None