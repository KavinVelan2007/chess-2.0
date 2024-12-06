import tkinter as tk
import pygame

import pygame_widgets.button

import pygame_widgets.dropdown

import pygame_widgets.textbox


class Settings:


    def __init__(self, ParentObject):

        self.FullRect = pygame.Rect(0, 0, 960, 540)

        self.ParentObject = ParentObject

        self.FullSurface = pygame.Surface(
            (960, 540), pygame.SRCALPHA)

        self.FullSurface.fill((0, 0, 0, 0))

        self.CrossButtonRect = pygame.Rect(920, 0, 40, 40)

        self.CrossButtonPressed = False

        self.CrossButtonHover = False

        self.BoardPreference = self.ParentObject.BoardPreference

        self.PiecePreference = self.ParentObject.PiecePreference

        self.CancelButton = pygame_widgets.button.Button(self.ParentObject.Display, 700, 700, 150, 40, text="Cancel", fontSize=20, inactiveColour=(
            150, 150, 150), hoverColour=(70, 70, 70), pressedColour=(170, 0, 0), radius=5, onRelease=self.OnCancel, textVAlign='center', textHAlign='center')

        self.ApplyButton = pygame_widgets.button.Button(self.ParentObject.Display, 700, 800, 150, 40, text="Apply", fontSize=20, inactiveColour=(
            150, 150, 150), hoverColour=(70, 70, 70), pressedColour=(0, 170, 0), radius=5, onRelease=self.OnApply, textVAlign='center', textHAlign='center')
        
        self.BoardPreferenceDropdown = pygame_widgets.dropdown.Dropdown(
        self, 440, 580, 200, 50, name='Select Board',
        choices=sorted(self.ParentObject.BoardOptions, key = lambda x: x.replace('-', ' ')),
        borderRadius=5,inactiveColor = (150,150,150),hoverColour=(70, 70, 70), pressedColour=(100,100,100), direction='down', textHAlign='center'
        )

        

    def DisplaySettings(self):

        pygame.draw.rect(self.FullSurface, (170, 170, 170),
                         self.FullRect, border_radius=10)

        pygame.draw.rect(self.FullSurface, (0, 0, 0),
                         self.FullRect, width=2, border_radius=10)

        if self.CrossButtonHover:

            pygame.draw.rect(
                self.FullSurface,
                (255, 0, 0),
                self.CrossButtonRect,
                border_radius=10
            )

        elif self.CrossButtonPressed:

            pygame.draw.rect(
                self.FullSurface,
                (150, 0, 0),
                self.CrossButtonRect,
                border_radius=10
            )

        pygame.draw.rect(
            self.FullSurface,
            (0, 0, 0),
            self.CrossButtonRect,
            width=2,
            border_radius=10
        )

        pygame.draw.line(self.FullSurface,
                         (255, 255, 255), (930, 10), (950, 30), 3)

        pygame.draw.line(self.FullSurface,
                         (255, 255, 255), (930, 30), (950, 10), 3)

        Text = self.ParentObject.SmallFont.render('Settings',False,(0,0,0))
        self.FullSurface.blit(Text,(960 // 2 - Text.get_width() // 2,Text.get_height() + 10))

        '''Text = self.ParentObject.SmallFont.render('Board Preferences',False,(30,30,30))
        self.FullSurface.blit(Text,(960 // 2 - Text.get_width() // 2,Text.get_height() + 80))'''

        self.ParentObject.Display.blit(self.FullSurface, (480, 270))

        '''button = pygame_widgets.button.Button(
            self.ParentObject.Display,  # Surface to place button on
            640,  # X-coordinate of top left corner
            720,  # Y-coordinate of top left corner
            150,  # Width
            100,  # Height

            # Optional Parameters
            text='Hello',  # Text to display
            fontSize=20,  # Size of font
            margin=10,  # Minimum distance between text/image and edge of button
            # Colour of button when not being interacted with
            inactiveColour=(200, 50, 0),
            # Colour of button when being hovered over
            hoverColour=(150, 0, 0),
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=15,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: print('Click')  # Function to call when clicked on
        )'''

    def SettingsEventCheck(self, Event):

        if self.CrossButtonRect.collidepoint((pygame.mouse.get_pos()[0] - 480, pygame.mouse.get_pos()[1] - 270)):

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


    def WidgetsUpdate(self, Events):

        pygame_widgets.update(Events)


    def OnCancel(self):

        self.PiecePreference = self.ParentObject.PiecePreference

        self.BoardPreference = self.ParentObject.BoardPreference

        self.ParentObject.SettingsOpen = False


    def OnApply(self):

        self.ParentObject.BoardPreference = self.BoardPreference
        
        self.ParentObject.PiecePreference = self.PiecePreference

        self.ParentObject.SettingsOpen = False