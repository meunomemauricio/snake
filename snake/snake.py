"""Represent the main protagonist."""
from typing import Tuple

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.rect import Rect


class Snake:
    """Snake."""

    HEAD_COLOR = (0x00, 0xFF, 0x00)

    def __init__(self, grid_size: int):
        self._x: int = 0
        self._y: int = 0
        self._grid_size = grid_size

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y

    def move_x(self, step: int) -> None:
        self._x += step

    def move_y(self, step: int) -> None:
        self._y += step

    def draw(self, surface: Surface):
        """Draw the snake on the surface."""
        pygame.draw.rect(
            surface=surface,
            color=self.HEAD_COLOR,
            rect=Rect(
                self._x * self._grid_size,
                self._y * self._grid_size,
                self._grid_size,
                self._grid_size,
            ),
        )

    def handle_input(self, event: Event) -> None:
        """Handle events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_y(step=-1)
            if event.key == pygame.K_DOWN:
                self.move_y(step=1)
            if event.key == pygame.K_RIGHT:
                self.move_x(step=1)
            if event.key == pygame.K_LEFT:
                self.move_x(step=-1)
