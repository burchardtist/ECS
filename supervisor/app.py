import logging
import sys

import pygame
from simple_settings import settings

logger = logging.getLogger(__name__)


class App:
    window = None
    clock = None
    renderer = None
    background_color = None

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(settings.RESOLUTION)
        self.clock = pygame.time.Clock()

    def display_fps(self):
        caption = f'{settings.CAPTION} - FPS: {self.clock.get_fps():.2f}'
        pygame.display.set_caption(caption)

    def game_loop(self, engine) -> None:
        done = False
        # self.load_map(engine, settings.MAP_PATH)
        logger.info('Game loop started')
        while not done:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
            engine.process(events=events)
            self.clock.tick(settings.FPS)
            self.display_fps()
        logger.info('Game loop finished')
        pygame.quit()
        sys.exit()
