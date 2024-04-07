from pathlib import Path

import pygame
from pygame import Rect, Color, Surface
from pygame.sprite import Sprite

from PygameToolsBox.animated_object import AnimatedObject, ANIMATION_END
from PygameToolsBox.spritesheet import SpriteSheet

pygame.init()
win = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)


class Bullet(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((10, 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def update(self, pos: Rect):
        self.rect.topleft = pos.topleft


sprites = SpriteSheet(Path("sprites.png").resolve(), 60, 60, 3, 7)
player = AnimatedObject(sprites.get_sprite_list(), 1)
player.add_action("run", -1, 8, 15)
player.add_action("jump", 0, 1, 7)
player.add_action("begin_slide", 0, 16, 17)
player.add_action("end_slide", 0, 17, 20)
player.add_action("dead", -1, 0, 0)
player.set_action("run")
player.rect = Rect(100, 100, 60, 60)
bullet = Bullet()

run = True
while run:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == ANIMATION_END:
            player.set_action("run")

    keys = pygame.key.get_pressed()
    action = player.get_action()
    if keys[pygame.K_DOWN] and action != "begin_slide":
        player.set_action("begin_slide")
    elif not keys[pygame.K_DOWN] and action == "begin_slide":
        player.set_action("end_slide")
    elif keys[pygame.K_UP] and action != "jump":
        player.set_action("jump")

    if pygame.sprite.collide_rect(player, bullet) and pygame.sprite.collide_mask(player, bullet):
        if pygame.mouse.get_pressed(3)[0]:
            player.set_action("dead")
        bullet.image.fill(Color(255, 0, 0))
    else:
        bullet.image.fill(Color(0, 0, 255))

    win.fill(Color(0, 0, 0))

    rect = player.rect
    player.update()
    player.draw(win)

    bullet.rect.center = pygame.mouse.get_pos()
    win.blit(bullet.image, bullet.rect)

    pygame.display.update()
