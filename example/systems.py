import pygame

from ecs.system import ISystem
from example.components import Renderable, Player, Fruit, Floor
from example.enums import DirectionEnum, ContextEnum
from example.utils import spawn_fruit


def make_position(renderable):
    pos_x = renderable.sprite.rect.x
    pos_y = renderable.sprite.rect.y
    return '{}_{}'.format(pos_x, pos_y)


class RenderableSystem(ISystem):
    def process(self, *args, **kwargs):
        self.engine.app.window.fill((0, 0, 0))
        self.engine.context[ContextEnum.RENDERABLE] = list()
        for entity, renderable in self.engine.get_components(Renderable):
            self.engine.app.window.blit(
                renderable.sprite.image,
                renderable.sprite.rect
            )
            self.update_position(entity, renderable)
        pygame.display.update()
        pygame.display.flip()

    def update_position(self, entity, renderable):
        self.engine.context[ContextEnum.RENDERABLE].append(
            (entity, renderable.sprite)
        )


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
        self.resolve_collision(player, renderable)

    def collided_entity(self, renderable):
        context_renderables = self.engine.get_context_item(
            ContextEnum.RENDERABLE) or list()
        for entity, sprite in context_renderables:
            if (renderable.sprite.is_collided_with(sprite) and
                    renderable.sprite is not sprite):
                return entity

    def resolve_collision(self, player, renderable):
        entity = self.collided_entity(renderable)
        if not entity:
            return

        entity_components = self.engine.get_entity_components(entity)
        if not entity_components:  # already dead entity
            return

        if entity_components.get(Fruit):
            self.engine.remove_entity(entity)
        elif entity_components.get(Floor):
            player.speed = 0


class FruitSystem(ISystem):
    def process(self, *args, **kwargs):
        fruit_ec = next(self.engine.get_components((Fruit, Renderable)), None)
        if not fruit_ec:
            self.respawn_fruit()

    def respawn_fruit(self):
        spawn_fruit(self.engine)
