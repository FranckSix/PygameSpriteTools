import pygame
from pygame import Surface, Rect


class MaskImage():
    def __init__(self, image: Surface):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self._image_rect = self.image.get_rect()
        self._mask_rect = self.mask.get_rect()

    @property
    def rect(self):
        return self._image_rect

    @rect.setter
    def rect(self, value: Rect):
        self._image_rect.topleft = value.topleft
        self._mask_rect.topleft = value.topleft
