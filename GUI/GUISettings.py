import pygame
import pygame_widgets.button

class Settings:

    def __init__(self, ParentObject):

        self.FullRect = pygame.Rect(480, 270, 960, 540)

        self.ParentObject = ParentObject

        self.CrossButtonRect = pygame.Rect(480 + 960 - 40,270,40,40)

        self.CrossButtonPressed = False

        self.CrossButtonHover = False

    def DisplaySettings(self):

        pygame.draw.rect(self.ParentObject.Display,(255,255,255),self.FullRect,border_top_right_radius=10,border_top_left_radius=10,border_bottom_left_radius=10,border_bottom_right_radius=10)
        
        pygame.draw.rect(self.ParentObject.Display,(0,0,0),self.FullRect,5,border_top_right_radius=10,border_top_left_radius=10,border_bottom_left_radius=10,border_bottom_right_radius=10)

        if self.CrossButtonHover:

            pygame.draw.rect(
                self.ParentObject.Display,
                (255, 0, 0),
                self.CrossButtonRect,
                border_top_left_radius=10,
                border_bottom_left_radius=10,
                border_bottom_right_radius=10,
                border_top_right_radius=10
            )

        elif self.CrossButtonPressed:

            pygame.draw.rect(
                self.ParentObject.Display,
                (150, 0, 0),
                self.CrossButtonRect,
                border_top_left_radius=10,
                border_bottom_left_radius=10,
                border_bottom_right_radius=10,
            )

        pygame.draw.rect(
            self.ParentObject.Display,
            (170, 170, 170),
            self.CrossButtonRect,
            width=5,
            border_top_left_radius=10,
            border_bottom_left_radius=10,
            border_bottom_right_radius=10,
            border_top_right_radius=10
        )

        pygame.draw.line(self.ParentObject.Display, (255, 255, 255), (915, 295), (935, 315),3)

        pygame.draw.line(self.ParentObject.Display, (255, 255, 255), (915, 315), (935, 295),3)

        button = pygame_widgets.button.Button(
            self.ParentObject.Display,  # Surface to place button on
            640,  # X-coordinate of top left corner
            720,  # Y-coordinate of top left corner
            150,  # Width
            100,  # Height

            # Optional Parameters
            text='Hello',  # Text to display
            fontSize=20,  # Size of font
            margin=10,  # Minimum distance between text/image and edge of button
            inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
            hoverColour=(150, 0, 0),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=15,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: print('Click')  # Function to call when clicked on
        )

    def UpdateEvents(self,events):
        pygame_widgets.update(events)

    def SettingsEventCheck(self, Event):

        if self.CrossButtonRect.collidepoint(pygame.mouse.get_pos()):

            if Event.type == pygame.MOUSEBUTTONDOWN:

                self.CrossButtonPressed = True

                self.CrossButtonHover = False

            elif self.CrossButtonPressed and Event.type == pygame.MOUSEBUTTONUP:

                self.ParentObject.SettingsOpen = False

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