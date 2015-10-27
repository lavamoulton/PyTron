import pygame
from pygame.locals import *

#Button object
class Button(object):
        #gotta initialize it
        def __init__(self, inRect, text, color, font):
                self.buttonRect = inRect
                self.buttonFont = font.render(text, 1, (230, 230, 230))
                self.color = color
                self.info = text
                self.centerText = self.buttonFont.get_rect()
                self.centerText.centerx = self.buttonRect.centerx
                self.centerText.centery = self.buttonRect.centery
                self.click = False

        def drawButton(self, GRID_DISPLAY):
                pygame.draw.rect(GRID_DISPLAY, self.color, self.buttonRect, 2)
                GRID_DISPLAY.blit(self.buttonFont, self.centerText)

        def checkClick(self, posX, posY):
                if self.click:
                        if posX > self.buttonRect.left and posX < self.buttonRect.right:
                                if posY > self.buttonRect.top and posY < self.buttonRect.bottom:
                                        return True
                return False

        def resetClick(self):
                self.click = False

        def setClick(self):
                self.click = True
