import pygame

from ecs.system import ISystem
from example.components import Renderable, Player, Fruit
from example.enums import DirectionEnum, ContextEnum


def make_position(renderable):
    pos_x = renderable.sprite.rect.x
    pos_y = renderable.sprite.rect.y
    return '{}_{}'.format(pos_x, pos_y)


class RenderableSystem(ISystem):
    def process(self, *args, **kwargs):
        self.engine.app.window.fill((0, 0, 0))
        for _, renderable in self.engine.get_components(Renderable):
            self.engine.app.window.blit(
                renderable.sprite.image,
                renderable.sprite.rect
            )
            self.update_position(renderable)
        pygame.display.update()
        pygame.display.flip()

    def update_position(self, renderable):
        try:
            self.engine.context[ContextEnum.RENDERABLE].add(renderable.sprite)
        except KeyError:
            self.engine.context[ContextEnum.RENDERABLE] = set()
            self.engine.context[ContextEnum.RENDERABLE].add(renderable.sprite)


class MovePlayerSystem(ISystem):
    def process(self, events):
        _, player, renderable = next(self.engine.get_components((Player, Renderable)))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP and
                        player.direction != DirectionEnum.DOWN):
                    player.direction = DirectionEnum.UP
                if (event.key == pygame.K_DOWN and
                        player.direction != DirectionEnum.UP):
                    player.direction = DirectionEnum.DOWN
                if (event.key == pygame.K_RIGHT and
                        player.direction != DirectionEnum.LEFT):
                    player.direction = DirectionEnum.RIGHT
                if (event.key == pygame.K_LEFT and
                        player.direction != DirectionEnum.RIGHT):
                    player.direction = DirectionEnum.LEFT

        direction_x, direction_y = player.direction.value
        renderable.sprite.set_position(
            direction_x*player.speed,
            direction_y*player.speed,
        )
        if self.collided_sprite(renderable):
            player.speed = 0

    def collided_sprite(self, renderable):
        sprites = self.engine.get_context_item(ContextEnum.RENDERABLE) or set()
        for sprite in sprites:
            if (renderable.sprite.is_collided_with(sprite) and
                    renderable.sprite is not sprite):
                return sprite


class FruitSystem(ISystem):
    def process(self, *args, **kwargs):
        _, fruit, renderable = next(self.engine.get_components((Fruit, Renderable)))
        if not fruit.spawned:
            self.respawn_fruit()

    def respawn_fruit(self):
        pass
