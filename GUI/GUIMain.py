import pygame

import pygame_widgets

import threading

import time

from GUI.GUISideBar import *

from GUI.GUIBoard import *

from GUI.GUIMoveHistory import *

from GUI.GUISettings import *


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

        self.font = pygame.font.SysFont("Arial", 100)

        self.Display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

        pygame.display.set_caption("Chess")

        self.LoadingFlag = True

        def LoadingScreen():

            while self.LoadingFlag:

                ReferenceText = self.font.render("Loading...", False, (255, 255, 255))
                
                for i in range(5):

                    if not self.LoadingFlag:

                        break
                
                    self.Display.fill((70, 70, 70))

                    Text = self.font.render("Loading" + '.' * i, False, (0, 0, 255))

                    self.Display.blit(Text, (960 - ReferenceText.get_width() // 2, 540 - ReferenceText.get_height() // 2))

                    pygame.display.update()

                    time.sleep(0.2)

        threading.Thread(target = LoadingScreen).start()

        self.InitPreferences()

        self.SettingsOpen = False

        self.SideBar = SideBar(self.Display)

        self.Settings = Settings(self)

        self.Board = Board(self)

        self.Running = True


    def DisplayBase(self):
        
        if not self.SettingsOpen:

            self.Display.fill((70, 70, 70))

            self.Board.DisplayBoard()

            self.SideBar.DisplaySideBar()

        else:

            self.Settings.DisplaySettings()


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

        self.LoadingFlag = False

        while self.Running:

            Events = pygame.event.get()

            for Event in Events:

                if Event.type == pygame.QUIT:

                    self.Running = False

                elif Event.type == self.SideBar.EventSettingsOpened:

                    self.SettingsOpen = True

                if not self.SettingsOpen:

                    self.SideBar.SideBarEventCheck(Event)

                    self.Board.BoardEventCheck(Event)

                else:

                    self.Settings.SettingsEventCheck(Event)

            self.DisplayBase()

            Clock.tick()

            """ self.Display.blit(
                self.font.render(f"{Clock.get_fps()}", False,
                            (255, 255, 255)), (0, 0)
            ) """

            self.Settings.UpdateEvents(Events)

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
