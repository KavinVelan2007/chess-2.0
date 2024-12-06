import pygame


class SideBar:


    def __init__(self, Display):

        self.Display = Display

        self.SideBarRect = pygame.Rect(0, 0, 100, 1080)

        self.EventSettingsOpened = pygame.event.custom_type()

        self.EventNewGameAI = pygame.event.custom_type()

        self.EventNewGameHuman = pygame.event.custom_type()

        self.CrossButtonRect = pygame.Rect(1850, 0, 70, 70)

        self.CrossButtonHover = False

        self.CrossButtonPressed = False

        self.SettingsIcon = pygame.transform.scale(
            pygame.image.load("GUI\\Resources\\Misc\\Settings.png"), (100, 100)
        ).convert_alpha()

        self.SettingsRect = self.SettingsIcon.get_rect()

        self.SettingsRect.topleft = (0, 960)

        self.SettingsPressed = False

        self.SettingsHover = False

        self.NewGameAI = False

        self.NewGameHuman = False

        self.NewGameAIHover = False

        self.NewGameHumanHover = False

        self.NewGameAISelected = False

        self.NewGameHumanSelected = False


    def DisplaySideBar(self):

        pygame.draw.rect(
            self.Display,
            (30, 30, 30),
            self.SideBarRect,
        )

        if self.CrossButtonHover:

            pygame.draw.rect(
                self.Display,
                (255, 0, 0),
                self.CrossButtonRect,
                border_top_left_radius=10,
                border_bottom_left_radius=10,
                border_bottom_right_radius=10,
            )

        elif self.CrossButtonPressed:

            pygame.draw.rect(
                self.Display,
                (150, 0, 0),
                self.CrossButtonRect,
                border_top_left_radius=10,
                border_bottom_left_radius=10,
                border_bottom_right_radius=10,
            )

        pygame.draw.rect(
            self.Display,
            (170, 170, 170),
            self.CrossButtonRect,
            width=3,
            border_top_left_radius=10,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
        )

        if self.SettingsHover:

            pygame.draw.rect(
                self.Display, (60, 60, 60), self.SettingsRect, border_radius=20
            )

        elif self.SettingsPressed:

            pygame.draw.rect(
                self.Display, (45, 45, 45), self.SettingsRect, border_radius=20
            )

        if self.SettingsPressed:

            self.Display.blit(
                pygame.transform.scale_by(self.SettingsIcon, 0.8),
                self.SettingsRect.scale_by(0.8),
            )

        else:

            self.Display.blit(self.SettingsIcon, self.SettingsRect)

        pygame.draw.line(self.Display, (255, 255, 255), (1875, 25), (1895, 45))

        pygame.draw.line(self.Display, (255, 255, 255), (1875, 45), (1895, 25))


    def SideBarEventCheck(self, Event):

        if self.SideBarRect.collidepoint(pygame.mouse.get_pos()):

            if self.SettingsRect.collidepoint(pygame.mouse.get_pos()):

                if (
                    pygame.mouse.get_pressed()[0]
                    and Event.type == pygame.MOUSEBUTTONDOWN
                ):

                    self.SettingsPressed = True

                if not self.SettingsPressed and not pygame.mouse.get_pressed()[0]:

                    self.SettingsHover = True

                elif self.SettingsPressed and Event.type == pygame.MOUSEBUTTONUP:

                    pygame.event.post(pygame.event.Event(
                        self.EventSettingsOpened))

                    self.SettingsPressed = False

                    self.SettingsHover = True

                else:

                    self.SettingsHover = False

            elif self.SettingsPressed and Event.type == pygame.MOUSEBUTTONUP:

                self.SettingsPressed = False

            else:

                self.SettingsHover = False

        elif self.SettingsPressed and Event.type == pygame.MOUSEBUTTONUP:

            self.SettingsPressed = False

        else:

            self.SettingsHover = False

        if self.CrossButtonRect.collidepoint(pygame.mouse.get_pos()):

            if Event.type == pygame.MOUSEBUTTONDOWN:

                self.CrossButtonPressed = True

                self.CrossButtonHover = False

            elif self.CrossButtonPressed and Event.type == pygame.MOUSEBUTTONUP:

                pygame.event.post(pygame.event.Event(pygame.QUIT))

                self.CrossButtonPressed = False

                self.CrossButtonHover = True

            elif not self.CrossButtonPressed and not pygame.mouse.get_pressed()[0]:

                self.CrossButtonHover = True

            else:

                self.CrossButtonHover = False

        elif self.CrossButtonPressed and Event.type == pygame.MOUSEBUTTONUP:

            self.CrossButtonPressed = False

        else:

            self.CrossButtonHover = False
