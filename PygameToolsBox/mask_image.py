import pygame
from pygame import Surface, Rect, Mask
from pygame.sprite import Sprite


class MaskImage(Sprite):
    def __init__(self, image: Surface):
        super().__init__()
        self.image: Surface = image
        self.mask: Mask = pygame.mask.from_surface(image)
        self.rect = self.image.get_rect()
