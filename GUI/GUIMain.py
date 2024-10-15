import pygame

from GUI.GUISideBar import *

from GUI.GUIBoard import *

from GUI.GUIMoveHistory import *


class Game:


    def __init__(self, **kwargs):

        if kwargs["BitBoards"] and kwargs["BoardData"]:

            self.BitBoards = kwargs["BitBoards"]

            self.BoardData = kwargs["BoardData"]

            del kwargs["BitBoards"], kwargs["BoardData"]

        elif kwargs:

            raise ValueError("Unknown Keyword Arguments")

        del kwargs

        import sys

        if sys.platform == "win32":

            import ctypes

            ctypes.windll.user32.SetProcessDPIAware()

        pygame.init()

        self.InitPreferences()

        self.Display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

        pygame.display.set_caption("Chess")

        self.SideBar = SideBar(self.Display)

        self.Board = Board(self)

        self.Running = True


    def DisplayBase(self):

        self.Display.fill((70, 70, 70))

        self.SideBar.DisplaySideBar()

        self.Board.DisplayBoard()


    def InitPreferences(self):

        import pickle

        with open("GUI\\PreferenceData.dat", "rb") as File:

            Data = pickle.load(File)

            self.BoardOptions = Data["BoardOptions"]

            self.PieceOptions = Data["PieceOptions"]

            self.Pieces = Data["Pieces"]

            self.BoardPreference = Data["BoardPreference"]

            self.PiecePreference = Data["PiecePreference"]


    def MainLoop(self):

        Clock = pygame.time.Clock()

        font = pygame.font.SysFont("Arial", 30)

        while self.Running:

            for Event in pygame.event.get():

                if Event.type == pygame.QUIT:

                    self.Running = False

                elif Event.type == self.SideBar.EventSettingsOpened:

                    pass

                self.SideBar.SideBarEventCheck(Event)

                self.Board.BoardEventCheck(Event)

            self.DisplayBase()

            Clock.tick()

            """ self.Display.blit(
                font.render(f"{Clock.get_fps()}", False,
                            (255, 255, 255)), (0, 0)
            ) """

            pygame.display.update()

        import pickle

        with open("GUI\\PreferenceData.dat", "wb") as File:

            Data = {}

            Data["BoardOptions"] = self.BoardOptions

            Data["PieceOptions"] = self.PieceOptions

            Data["Pieces"] = self.Pieces

            Data["BoardPreference"] = self.BoardPreference

            Data["PiecePreference"] = self.PiecePreference

            pickle.dump(Data, File)

        pygame.quit()
