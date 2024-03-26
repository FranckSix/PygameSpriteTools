import math
from pathlib import Path

import pygame.image
from pygame import Surface, Rect


class Background:
    def __init__(self, image: Surface):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.scroll = 0
        self.speed = 1

    def update(self, scroll: int):
        self.scroll += scroll
        if abs(self.scroll * self.speed) > self.width:
            self.scroll = 0

    def cover_left(self, win: Surface):
        rect = Rect(self.scroll * self.speed, 0, self.width, self.height)
        while rect.x > 0:
            rect.x -= self.width
            win.blit(self.image, rect)

    def cover_right(self, win: Surface):
        rect = Rect(self.scroll * self.speed, 0, self.width, self.height)
        while rect.x + rect.width < win.get_width():
            rect.x += self.width
            win.blit(self.image, rect)


class ParallaxBackground:
    """
    This class allows you to manage background images and apply a parallax effect.
    We must add the background images starting with the one that will be most in the background.
    Then we stack the images to finish with the one on top.
    By default, the speed is adjusted to 5, but it can be changed
    """

    def __init__(self):
        self._backgrounds = list[Background]()
        self.speed: int = 5

    def add_background(self, image: Path):
        """
        :param image: Image source path with filename
        """

        image = Background(pygame.image.load(image).convert_alpha())
        image.speed += len(self._backgrounds) * 0.2
        self._backgrounds.append(image)

    def update(self, scroll_direction: int):
        """
        Params:
            scroll_direction (int):width = {int} 1782
                -1 for _scroll left.
                1 to _scroll right.
                This value will be multiplied by the speed property.
        """
        for image in self._backgrounds:
            image.update(scroll_direction * -1 * self.speed)

    def draw(self, win: Surface):
        """
        Params win (pygame.Surface):
            The object takes care of stacking the background images in the order of insertion.
            Each image scrolls faster and faster as it nears the top of the stack
        """
        for i, image in enumerate(self._backgrounds):
            rect = Rect(image.scroll * image.speed, 0, image.scroll + image.width, image.height)
            win.blit(image.image, rect)  # Dessiner l'image avec le scrolling
            image.cover_left(win)
            image.cover_right(win)
