import time

import pygame
from pathlib import Path

pygame.init()

win = pygame.display.set_mode((800,800))

from PygameToolsBox.spritesheet import SpriteSheet

sprite_file = Path( "sprites.png").resolve()
sprites = SpriteSheet(sprite_file, 60, 60, 4, 4)

range = sprites.get_sprite_range((2, 0), (3, 3))


for i, image in enumerate(range):
    win.blit(image, (i * 60, 0))

pygame.display.update()

pygame.time.delay(10000)