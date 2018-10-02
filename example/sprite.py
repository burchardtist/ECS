import os
from decimal import Decimal
from typing import Union

import pygame
from pygame.rect import Rect


class SimpleSprite(pygame.sprite.Sprite):
    _posx: Decimal = None
    _posy: Decimal = None
    width: int = None
    height: int = None
    image: pygame.Surface = None
    rect: Rect = None

    def __init__(
            self,
            posx: Union[Decimal, float, int],
            posy: Union[Decimal, float, int],
            path: str,
            *groups
    ) -> None:
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

    def set_position(self, posx: Decimal, posy: Decimal) -> None:
        self._posx += posx
        self._posy += posy
        self.update()

    def update(self) -> None:
        self.rect = Rect(
            self._posx * self.width,
            self._posy * self.height,
            self.width,
            self.height
        )

    def is_collided_with(self, sprite: 'SimpleSprite') -> bool:
        return self.rect.colliderect(sprite.rect)