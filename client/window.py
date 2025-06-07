import pygame

import pygame.key

from common.input import KeyDownEvent, KeyUpEvent


class Window:
    WIDTH = 720
    HEIGHT = 480

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
        pygame.display.flip()
        self.__screen.fill((30, 30, 30))

    def is_running(self):
        return self.__running

    def close(self):
        pygame.quit()
        self.__running = False
        self.__screen = None

    def convert_to_screen_space(self, normalized_x, normalized_y):
        """
        Converts coordinates from -1 to 1 space to 0 to width/height space.

        :param normalized_x: X coordinate in the range [-1, 1]
        :param normalized_y: Y coordinate in the range [-1, 1]
        :return: Tuple (screen_x, screen_y) in screen space
        """
        # Get the screen dimensions dynamically
        screen = pygame.display.get_surface()
        if screen is None:
            raise ValueError("Pygame display surface is not initialized.")
        width, height = screen.get_size()

        screen_x = (normalized_x + 1) * (width / 2)
        screen_y = (1 - normalized_y) * (height / 2)  # Invert y-axis
        return int(screen_x), int(screen_y)

    def draw_rect(self, x, y, width, height, color):
        """
        Draws a rectangle on the screen with its center at (x, y) in normalized space.

        :param x: X coordinate of the rectangle's center in the range [-1, 1]
        :param y: Y coordinate of the rectangle's center in the range [-1, 1]
        :param width: Width of the rectangle relative to the screen size (0 to 1)
        :param height: Height of the rectangle relative to the screen size (0 to 1)
        :param color: Color of the rectangle (RGB tuple)
        """
        # Get the screen dimensions dynamically
        screen = pygame.display.get_surface()
        if screen is None:
            raise ValueError("Pygame display surface is not initialized.")
        screen_width, screen_height = screen.get_size()

        # Convert normalized center coordinates to screen space
        center_x, center_y = self.convert_to_screen_space(x, y)

        # Calculate rectangle dimensions in pixels
        rect_width = int(width * screen_width)
        rect_height = int(height * screen_height)

        # Calculate top-left corner of the rectangle
        top_left_x = center_x - rect_width // 2
        top_left_y = center_y - rect_height // 2

        # Draw the rectangle
        pygame.draw.rect(self.__screen, color, (top_left_x, top_left_y, rect_width, rect_height))