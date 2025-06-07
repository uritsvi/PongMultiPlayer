import pygame

import pygame.key

from common.input import KeyDownEvent, KeyUpEvent


class Window:
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.__screen = None
        self.__running = False

    def create(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((
            self.WIDTH,
            self.HEIGHT
        ))
        self.__running = True

    def poll_events(self):
        out = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                    continue
                else:
                    out.append(KeyDownEvent(pygame.key.name(event.key)))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                    continue
                else:
                    out.append(KeyUpEvent(pygame.key.name(event.key)))
        return out

    def render(self):
        self.__screen.fill((30, 30, 30))
        pygame.display.flip()

    def is_running(self):
        return self.__running

    def close(self):
        pygame.quit()
        self.__running = False
        self.__screen = None