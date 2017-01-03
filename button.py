# imports
import pygame


class Button(object):
    """a button object, containing the following:
        the rectangle it is contained in
        the text present in it
        the color of the text
        the font of the text"""

    # gotta initialize it
    def __init__(self, in_rect, text, text_color, outline_color, font):
        self.button_rect = in_rect
        self.button_font = font.render(text, 1, text_color)
        self.outline_color = outline_color
        self.info = text
        self.center_text = self.button_font.get_rect()
        self.center_text.centerx = self.button_rect.centerx
        self.center_text.centery = self.button_rect.centery
        self.click = False

    def draw_button(self, display):
        """draws the button's rectangle on the display
            :param display: the display to draw on passed in as an arg"""

        pygame.draw.rect(display, self.outline_color, self.button_rect, 2)
        display.blit(self.button_font, self.center_text)

    def check_click(self, pos_x, pos_y):
        """checks whether the passed in click event is within the bounds of the button
            :param pos_x: x position of the mouse on click
            :param pos_y: y position of the mouse on click"""

        if self.click:
            if self.button_rect.left < pos_x < self.button_rect.right \
                    and self.button_rect.top < pos_y < self.button_rect.bottom:
                return True
        return False

    def reset_click(self):
        """resets the click boolean to False"""

        self.click = False

    def set_click(self):
        """sets the click boolean to True"""

        self.click = True
