from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass(frozen=True)
class Obstacle:
    center: Tuple[float, float]
    size: Tuple[float, float, float]

    @property
    def height(self) -> float:
        return self.size[2]


@dataclass
class Terrain:
    obstacles: List[Obstacle]

    def heights(self) -> List[float]:
        return [obstacle.height for obstacle in self.obstacles]


def generate_obstacles(
    seed: int,
    count: int,
    height_range: Tuple[float, float],
    width_range: Tuple[float, float],
    length_range: Tuple[float, float],
    spawn_area: Tuple[float, float],
) -> Terrain:
    rng = random.Random(seed)
    obstacles: List[Obstacle] = []
    for _ in range(count):
        center = (
            rng.uniform(-spawn_area[0], spawn_area[0]),
            rng.uniform(0.3, spawn_area[1]),
        )
        size = (
            rng.uniform(*width_range),
            rng.uniform(*length_range),
            rng.uniform(*height_range),
        )
        obstacles.append(Obstacle(center=center, size=size))
    return Terrain(obstacles=obstacles)
