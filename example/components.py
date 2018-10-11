from decimal import Decimal

import attr

from example.enums import DirectionEnum
from example.sprite import SimpleSprite


@attr.s(slots=True)
class Wall:
    walkable: bool = attr.ib(bool)


@attr.s(slots=True)
class Renderable:
    sprite = attr.ib(type=SimpleSprite)
    priority = attr.ib(type=int, default=100)  # todo: render by priority


@attr.s(slots=True)
class Player:
    direction = attr.ib(type=DirectionEnum, default=DirectionEnum.UP)
    speed = attr.ib(type=Decimal, default=Decimal('0.3'))
    tail = attr.ib(type=list, default=list())

    @property
    def head(self):
        try:
            return self.tail[0]
        except IndexError:
            pass


@attr.s(slots=True)
class Tail:
    old_position = attr.ib(type=tuple, default=(0, 0))


@attr.s(slots=True)
class Fruit:
    spawned = True
