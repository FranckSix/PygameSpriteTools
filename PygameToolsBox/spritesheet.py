from pathlib import Path

import pygame
from pygame import Surface


class SpriteSheet:
    def __init__(self,
                 sprite_sheet_path: Path,
                 sprite_size_x: int,
                 sprite_size_y: int,
                 nb_rows: int,
                 nb_cols: int,
                 alpha: bool = True):
        """
        :param sprite_sheet_path:
            Path and file of the spead sheet
            All sprites of the sprite sheet must be relative to same purpose.
            N.B. Each instance of the image must have sames sizes. Each instance
            may have different height and width. Each sub-sprites is delimited by this width and height.
            It's possible in case you have multiples sprites to make many rows, in this case each rows must have the
            same size as a single sub sprite.
        :param sprite_size_x:
            Single sprite width. Used for cut sub sprite from sprite sheet
        :param sprite_size_y:
            Single sprite height. Used for cut sub sprite from sprite sheet
        :param nb_rows:
            How many rows of the sub sprite, sprite sheet contains
        :param nb_cols:
            How many cols of the sub sprite, sprite sheet contains
        :param alpha:
            Is the sprite sheet contains a canal alpha for transparency. Otherwise,
            you may use the property "set_colorkey" from the sub image
        """
        if alpha:
            self._sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        else:
            self._sprite_sheet = pygame.image.load(sprite_sheet_path).convert()
        self._sprite_size_x = sprite_size_x
        self._sprite_size_y = sprite_size_y
        self._rows = nb_rows
        self._cols = nb_cols
        self._alpha = alpha

    def get_sprite(self, row: int, col: int) -> Surface | None:
        """
        :param row:
            Row of the sprite sheet to get (0 based index)
        :param col:
            Column of the sprite sheet to get (0 based index)
        :return:
            Single instance of sub-sprite or None if out of bound limits
        """
        if 0 > row > self._rows - 1 or 0 > col > self._cols - 1:
            return None

        offset_x = col * self._sprite_size_x
        offset_y = row * self._sprite_size_y

        rect = (offset_x, offset_y, self._sprite_size_x, self._sprite_size_y)
        key_alpha = pygame.SRCALPHA if self._alpha else pygame.SRCCOLORKEY
        image = Surface((self._sprite_size_x, self._sprite_size_y), key_alpha)
        image.blit(self._sprite_sheet, (0, 0), rect)

        return image

    def get_sprite_list(self) -> [Surface]:
        """
        Obtain all occurrences of sub sprites in sprite sheet
        :return (pygame.Surface):
            list of sub sprite
        """
        for r in range(self._rows):
            for c in range(self._cols):
                yield self.get_sprite(r, c)

    def get_sprite_range(self, start: [int, int], stop: [int, int]) -> [Surface]:
        """
        Return list of sub sprites for row, col start to row col end
        the start and end is included into set
        the index ins 0 based range
        :param start: (row, col) to start
        :param end: (row, col) to end
        :return:
        """
        index_start = start[0] * 100 + start[1]
        index_stop = stop[0] * 100 + stop[1]
        for row in range(start[0], stop[0] + 1):
            for col in range(self._cols):
                if index_start <= row * 100 + col <= index_stop:
                    yield self.get_sprite(row, col)
