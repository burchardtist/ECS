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
    done = False

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(settings.RESOLUTION)
        self.clock = pygame.time.Clock()

    def display_fps(self):
        caption = f'{settings.CAPTION} - FPS: {self.clock.get_fps():.2f}'
        pygame.display.set_caption(caption)

    def game_loop(self, engine) -> None:
        logger.info('Game loop started')
        while not self.done:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
            engine.run_processes(events=events)
            self.clock.tick(settings.FPS)
            self.display_fps()
        logger.info('Game loop finished')
        pygame.quit()
        sys.exit()
