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
                pygame.image.load(f"GUI\\Resources\\Boards\\{i}.png"),
                (720, 674)
            ).convert_alpha()

        for i in self.ParentObject.PieceOptions:

            self.Data["PieceOptions"][i] = {}

            for j in self.ParentObject.Pieces:

                self.Data["PieceOptions"][i][j] = pygame.transform.scale(
                    pygame.image.load(f"GUI\\Resources\\Pieces\\{i}\\{j}.png"),
                    (126, 161),
                ).convert_alpha()


    def drawBoard(self):

        self.Display.blit(self.Data["BoardOptions"]
                          [self.ParentObject.BoardPreference], (40, 63))

        for Square in range(64):

            for Piece in range(12):

                if self.ParentObject.BitBoards[Piece] & (1 << Square):

                    self.Display.blit(
                        self.Data["PieceOptions"][self.ParentObject.PiecePreference][self.ParentObject.Pieces[Piece]],
                        (self.OffSet[0] + (Square % 8) * 90, self.OffSet[1] + (Square // 8) * 83))
