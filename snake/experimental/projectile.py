"""Define Projectiles and its manager."""
from enum import Enum
from typing import Set, Tuple

import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.terrain import Blueprint


class ProjectileState(Enum):
    """"""

    MOVING = 1
    DELETED = 2


class Projectile:
    """Projectile."""

    def __init__(self, blueprint: Blueprint, dir: Vector2, pos: Vector2):
        """Simulates a Projectile from the Turret.

        :param blueprint: Terrain Blueprint.
        :param pos: Initial Position, in screen coordinates.
        :param speed: Initial Speed Vector, in screen coordinates.
        """
        self._blueprint: Blueprint = blueprint
        self._dir: Vector2 = dir
        self._curr_pos: Vector2 = pos

        self.state = ProjectileState.MOVING

    def _oos_collision(self) -> bool:
        """Out of Screen Collision Detection.

        :return `True` when the current position is not inside the screen.
        """
        return not self._blueprint.rect.collidepoint(
            self._curr_pos.x,
            self._curr_pos.y,
        )

    @property
    def color(self) -> Tuple[int, int, int]:
        """Projectile Color."""
        return 0xFF, 0xFF, 0x00  # Yellow

    @property
    def radius(self) -> int:
        """Projectile Radius."""
        return 5

    @property
    def speed(self) -> float:
        """Scalar Speed."""
        return 0.05

    @property
    def velocity(self) -> Vector2:
        """Velocity Vector."""
        return self.speed * self._dir

    def process_logic(self) -> None:
        """Process the Projectile logic and update its status."""
        self._curr_pos += self.velocity

        if self._oos_collision():
            self.state = ProjectileState.DELETED
            return

        # TODO: Detect collisions with terrain

    def get_render_position(self, interp: float) -> Vector2:
        """Calculate the Rendering Position, in screen coordinates.

        A linear interpolation is made between the current position and a
        prediction of the next position.
        """
        next_pos: Vector2 = self._curr_pos + self.velocity
        return self._curr_pos.lerp(next_pos, interp)


class ProjectileManager:
    """Projectile Manager."""

    def __init__(self, blueprint: Blueprint):
        """Manage and Render all projectiles.

        :param blueprint: Terrain Blueprint.
        """
        self._blueprint = blueprint
        self._projectiles: Set[Projectile] = set()

    def create_projectile(self, dir: Vector2, pos: Vector2) -> None:
        """Create a Projectile and add it to the list.

        :param dir: Initial Direction, in screen coordinates.
        :param pos: Initial Position, in screen coordinates.
        """
        self._projectiles.add(
            Projectile(blueprint=self._blueprint, dir=dir, pos=pos)
        )

    def process_logic(self) -> None:
        """Process logic and update status."""
        to_be_removed = set()
        for proj in self._projectiles:
            proj.process_logic()
            if proj.state == ProjectileState.DELETED:
                to_be_removed.add(proj)

        self._projectiles -= to_be_removed

    def build_surface(self, interp: float) -> Surface:
        """Fully rendered Surface."""
        sface = Surface(size=self._blueprint.rect.size, flags=pygame.SRCALPHA)
        for proj in self._projectiles:
            draw.circle(
                surface=sface,
                color=proj.color,
                center=proj.get_render_position(interp=interp),
                radius=proj.radius,
            )

        return sface
