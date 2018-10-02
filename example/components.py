from decimal import Decimal

import attr

from example.enums import DirectionEnum
from example.sprite import SimpleSprite


@attr.s(slots=True)
class Floor:
    walkable: bool = attr.ib(bool)


@attr.s(slots=True)
class Renderable:
    sprite = attr.ib(type=SimpleSprite)


@attr.s(slots=True)
class Player:
    direction = attr.ib(type=DirectionEnum, default=DirectionEnum.UP)
    speed = attr.ib(type=Decimal, default=Decimal('0.2'))


@attr.s(slots=True)
class Fruit:
    spawned = True
