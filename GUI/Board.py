import pygame
import os


class Board:


    def __init__(self,ParentObject):

        self.ParentObject = ParentObject

        self.Display = self.ParentObject.Display

        self.Width = 800

        self.Height = 800

        self.InitImages()
    

    def InitImages(self):

        self.Data = {"BoardOptions": {}, "PieceOptions": {}}

        for i in self.ParentObject.BoardOptions:

            self.Data["BoardOptions"][i] = pygame.transform.scale(
                pygame.image.load(f"GUI\\Resources\\Boards\\{i}"),
                (720, int(824 * 0.8181))
            ).convert_alpha()

        for i in self.ParentObject.PieceOptions:

            self.Data["PieceOptions"][i] = {}

            for j in self.ParentObject.Pieces:

                self.Data["PieceOptions"][i][j] = pygame.transform.scale(
                    pygame.image.load(f"GUI\\Resources\\Pieces\\{i}\\{j}"),
                    (int(154 * 0.8181), int(197 * 0.8181)),
                ).convert_alpha()


    def drawBoard(self):

        for row in range(8):

            for col in range(8):

                x,y = col * (self.Width // 8),row * (self.Height // 8)

                if (row + col) % 2 == 0:

                    pygame.draw.rect(self.Display,(0,0,0),(x,y,self.Width / 8,self.Height / 8))

                else:

                    pygame.draw.rect(self.Display,(255,255,255),(x,y,self.Width / 8,self.Height / 8))