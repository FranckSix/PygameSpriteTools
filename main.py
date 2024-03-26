from pathlib import Path

import pygame
from pygame import Color, Surface

from parallax_bg import ParallaxBackground
from spritesheet import SpriteSheet

pygame.init()
win = pygame.display.set_mode((800, 447))
clock = pygame.time.Clock()
sprites = SpriteSheet(Path("chess_set.png"), 90, 90, 2, 5)
background = ParallaxBackground()
background.add_background(Path("bg0.png"))
background.add_background(Path("bg1.png"))
background.add_background(Path("bg2.png"))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        background.update(-1)
    elif keys[pygame.K_RIGHT]:
        background.update(1)
    else:
        background.update(0)

    clock.tick(60)
    win.fill((255,255,255))

    background.draw(win)

#    x = 0
#    sprite:Surface
#    for sprite in sprites.get_sprite_list():
#        win.blit(sprite, (x,0))
#        x += sprite.get_width()

    pygame.display.update()
