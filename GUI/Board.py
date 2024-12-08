import pygame


class Board:


    def __init__(self, ParentObject):

        self.ParentObject = ParentObject

        self.Display = self.ParentObject.Display

        self.Width = 800

        self.Height = 800

        self.OffSet = (24, 0)

        self.InitImages()


    def InitImages(self):

        self.Data = {"BoardOptions": {}, "PieceOptions": {}}

        for i in self.ParentObject.BoardOptions:

            self.Data["BoardOptions"][i] = pygame.transform.scale(
                pygame.image.load(f"chess-2.0\\GUI\\Resources\\Boards\\{i}.png"),
                (720, 674)
            ).convert_alpha()

        for i in self.ParentObject.PieceOptions:

            self.Data["PieceOptions"][i] = {}

            for j in self.ParentObject.Pieces:

                self.Data["PieceOptions"][i][j] = pygame.transform.scale(
                    pygame.image.load(f"chess-2.0\\GUI\\Resources\\Pieces\\{i}\\{j}.png"),
                    (126, 161),
                ).convert_alpha()


    def drawBoard(self):

        self.Display.blit(self.Data["BoardOptions"]
                          [self.ParentObject.BoardPreference], (40, 63))

    def drawPieces(self):
        for Square in range(64):

            for Piece in range(12):

                if self.ParentObject.ActivePoint:
                    x,y = self.ParentObject.ActivePoint
                    x -= self.ParentObject.x
                    y -= self.ParentObject.y
                    row = y // 83
                    col = x // 90

                if self.ParentObject.ChessBoardObj.bitboards[Piece] & (1 << Square):

                    if not self.ParentObject.ActivePoint or (self.ParentObject.ActivePoint and Square != row * 8 + col):

                        self.Display.blit(
                            self.Data["PieceOptions"][self.ParentObject.PiecePreference][self.ParentObject.Pieces[Piece]],
                            (self.OffSet[0] + (Square % 8) * 90, self.OffSet[1] + (Square // 8) * 83))