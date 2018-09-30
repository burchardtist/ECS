import os
from decimal import Decimal

import pygame
from pygame.rect import Rect


class SimpleSprite(pygame.sprite.Sprite):
    _posx: Decimal = None
    _posy: Decimal = None
    width = None
    height = None
    image = None
    rect = None

    def __init__(self, posx, posy, path, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(
            os.path.join(
                os.getcwd(),
                'example/assets',
                path
            )
        )
        self._posx = Decimal(posx)
        self._posy = Decimal(posy)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.update()

    def set_position(self, posx, posy):
        self._posx += posx
        self._posy += posy
        self.update()

    def update(self):
        self.rect = Rect(
            self._posx * self.width,
            self._posy * self.height,
            self.width,
            self.height
        )
