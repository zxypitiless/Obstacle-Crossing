from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple
import math


@dataclass(frozen=True)
class RewardTerms:
    success_bonus: float
    collision_penalty: float
    tracking_weight: float
    com_weight: float
    head_weight: float
    energy_weight: float
    stability_weight: float


def _l2(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def compute_reward(
    success: bool,
    collision: bool,
    foot_errors: Iterable[float],
    com_error: float,
    head_error: float,
    energy: float,
    stability: float,
    terms: RewardTerms,
) -> float:
    reward = 0.0
    if success:
        reward += terms.success_bonus
    if collision:
        reward -= terms.collision_penalty
    reward -= terms.tracking_weight * sum(foot_errors)
    reward -= terms.com_weight * com_error
    reward -= terms.head_weight * head_error
    reward -= terms.energy_weight * energy
    reward -= terms.stability_weight * stability
    return reward
