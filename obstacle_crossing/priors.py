from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class FootstepTarget:
    position: Tuple[float, float, float]
    timestamp: int


@dataclass(frozen=True)
class BodyTarget:
    com: Tuple[float, float, float]
    head: Tuple[float, float, float]


@dataclass(frozen=True)
class PriorBundle:
    footsteps: List[FootstepTarget]
    body_targets: List[BodyTarget]


def validate_priors(bundle: PriorBundle, horizon: int) -> None:
    if len(bundle.footsteps) < horizon:
        raise ValueError("Footstep horizon shorter than required.")
    if not bundle.body_targets:
        raise ValueError("Body targets must be provided for CoM/head conditioning.")


def default_body_targets(com_height: float, head_height: float, steps: int) -> List[BodyTarget]:
    return [
        BodyTarget(com=(0.0, 0.0, com_height), head=(0.0, 0.0, head_height))
        for _ in range(steps)
    ]
