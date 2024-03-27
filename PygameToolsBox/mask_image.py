import pygame
from pygame import Surface


class MaskImage():
    def __init__(self, image: Surface):
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)