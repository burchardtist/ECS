import os
from decimal import Decimal
from typing import Union, Tuple

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

    def get_position(
            self,
            as_int=False
    ) -> Union[Tuple[Decimal, Decimal], Tuple[int, int]]:
        return ((int(self._posx), int(self._posy))
                if as_int
                else (self._posx, self._posy))

    def move_position(self, posx: Decimal, posy: Decimal) -> None:
        self._posx += posx
        self._posy += posy
        self.update()

    def set_position(self, posx: Decimal, posy: Decimal) -> None:
        self._posx = posx
        self._posy = posy
        self.update()

    def update(self) -> None:
        self.rect = Rect(
            int(self._posx) * self.width,
            int(self._posy) * self.height,
            self.width,
            self.height
        )

    def is_collided_with(self, sprite: 'SimpleSprite') -> bool:
        return self.rect.colliderect(sprite.rect)
