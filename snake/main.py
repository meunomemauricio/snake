"""Main Application."""
from typing import Iterable

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.time import Clock

from snake.grid import Grid
from snake.utils import Layer, multi_text, time_ms


class QuitApplication(Exception):
    """Quit the application if raised inside the Main Loop."""


def handle_quit(event: Event) -> None:
    """Handle the Quit events.

    :param event: PyGame Event object.
    """
    if event.type == pygame.QUIT:
        raise QuitApplication
    elif event.type == pygame.KEYUP and event.key == pygame.K_q:
        raise QuitApplication


class MainApp:
    """Main application."""

    #: Screen/Window parameters.
    CAPTION = "Snake v0.1"
    BG_COLOR = (0x00, 0x00, 0x00)

    #: FPS meter parameters.
    DEBUG_SIZE = 25
    DEBUG_COLOR = (0xFF, 0x00, 0x00)

    #: Grid parameters.
    GRID_ALPHA = 50
    GRID_COLOR = (0xFF, 0xFF, 0xFF)
    GRID_LINE = 1
    GRID_SIZE = (20, 20)
    GRID_STEP = 30

    #: Difference in time between ticks (Basically, the snake speed...)
    TICK_STEP = 250.0  # ms

    def __init__(self, debug: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the screen.
        :param debug: If `True`, render the debug info on screen.
        """
        self._debug = debug

        # Init PyGame
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        # Application Variables
        self._next_tick = time_ms()
        self._render_clock = Clock()
        self._running = True

        # Game Elements
        self._fps_font = SysFont(get_default_font(), size=self.DEBUG_SIZE)
        self._grid = Grid(
            size=self.GRID_SIZE,
            step=self.GRID_STEP,
            alpha=self.GRID_ALPHA,
            color=self.GRID_COLOR,
            line=self.GRID_LINE,
        )
        self._apple = self._grid.apple
        self._snake = self._grid.snake
        self._screen = pygame.display.set_mode(size=self._grid.resolution)

    @property
    def _debug_surface(self) -> Iterable[Layer]:
        """Debug text layers."""
        return multi_text(
            font=self._fps_font,
            color=self.DEBUG_COLOR,
            msgs=(
                f"FPS: {self._render_clock.get_fps()}",
                str(self._grid.snake),
                str(self._grid.apple),
            ),
        )

    def _handle_events(self):
        """Handle Game Events."""
        for event in pygame.event.get():
            handle_quit(event=event)
            self._snake.handle_event(event=event)

    def _render_graphics(self) -> None:
        """Render the frame and display it in the screen."""
        self._screen.fill(color=self.BG_COLOR)
        layers = self._grid.layers
        if self._debug:
            layers.extend(self._debug_surface)

        self._screen.blits(layers)
        pygame.display.flip()
        self._render_clock.tick()

    def _main_loop(self) -> None:
        """Main Application Loop."""
        if time_ms() > self._next_tick:
            self._snake.update_state()
            self._next_tick += self.TICK_STEP

        self._handle_events()
        self._render_graphics()

    def run(self) -> None:
        """Run the application."""
        while True:
            try:
                self._main_loop()
            except QuitApplication:
                break
