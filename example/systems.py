import pygame

from ecs.system import ISystem
from example.components import Renderable, Player
from example.enums import DirectionEnum


class RenderableSystem(ISystem):
    def process(self, *args, **kwargs):
        self.engine.app.window.fill((0, 0, 0))
        self.engine.app.rect_list = list()  # todo queue?
        for _, renderable in self.engine.get_components(Renderable):
            self.engine.app.rect_list += [self.engine.app.window.blit(renderable.sprite.image, renderable.sprite.rect)]
        pygame.display.update(self.engine.app.rect_list)
        pygame.display.flip()


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
