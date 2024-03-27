from pathlib import Path

import pygame
from pygame import Rect, Color, Surface

from PygameToolsBox.animated_object import AnimatedObject
from PygameToolsBox.mask_image import MaskImage
from PygameToolsBox.spritesheet import SpriteSheet

pygame.init()
win = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

sprites = SpriteSheet(Path("sprites.png").resolve(), 60, 60, 3, 7)
player = AnimatedObject(sprites.get_sprite_range((1,1), (2,1)))
bullet = MaskImage(Surface((10, 10)))

run = True
while run:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if player.is_collide_with(bullet):
        bullet.image.fill(Color(255, 0, 0))
    else:
        bullet.image.fill(Color(0, 0, 255))

    win.fill(Color(0, 0, 0))
    player.image_index += 1
    player.update(Rect(100, 100, 60, 60))
    player.draw(win)

    bullet.rect.center = pygame.mouse.get_pos()
    win.blit(bullet.image, bullet.rect)

    pygame.display.update()

