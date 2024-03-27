import pygame.sprite
from pygame import Surface, Rect

from PygameToolsBox.mask_image import MaskImage


class AnimatedObject:
    def __init__(self, images: [Surface]):
        self.images = list[MaskImage]()
        self._add_sprites(images)
        self._current_image = self.images[0]
        self._image_index = 0

    def _add_sprites(self, images: [Surface]):
        for i, image in enumerate(images):
            self.images.append(MaskImage(image))
            i += 1

    @property
    def image_index(self) -> int:
        return self._image_index

    @image_index.setter
    def image_index(self, value: int):
        self._image_index = value
        if self._image_index >= len(self.images):
            self._image_index = 0

    def update(self, rect: Rect):
        self._current_image.rect.center = rect.center
        self._current_image = self.images[self._image_index]

    def is_collide_with(self, other: MaskImage):
        if pygame.sprite.collide_rect(self._current_image, other):
            if pygame.sprite.collide_mask(self._current_image, other):
                return True
        return False

    def draw(self, win: Surface):
        win.blit(self._current_image.image, self._current_image.rect)
