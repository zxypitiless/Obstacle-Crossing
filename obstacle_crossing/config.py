from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class EnvironmentConfig:
    seed: int
    obstacle_count: int
    obstacle_height_range: Tuple[float, float]
    obstacle_width_range: Tuple[float, float]
    obstacle_length_range: Tuple[float, float]
    spawn_area: Tuple[float, float]


@dataclass(frozen=True)
class PriorsConfig:
    footstep_horizon: int
    com_height: float
    head_height: float
    landing_tolerance: float


@dataclass(frozen=True)
class RewardConfig:
    success_bonus: float
    collision_penalty: float
    tracking_weight: float
    com_weight: float
    head_weight: float
    energy_weight: float
    stability_weight: float


@dataclass(frozen=True)
class CurriculumStage:
    max_height: float
    max_count: int


@dataclass(frozen=True)
class CurriculumConfig:
    stages: List[CurriculumStage]
    success_threshold: float


@dataclass(frozen=True)
class TrainingConfig:
    episodes: int
    episode_length: int
    log_every: int


@dataclass(frozen=True)
class TaskConfig:
    environment: EnvironmentConfig
    priors: PriorsConfig
    reward: RewardConfig
    curriculum: CurriculumConfig
    training: TrainingConfig


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(path: str | Path) -> TaskConfig:
    data = _load_json(Path(path))

    env = data["environment"]
    priors = data["priors"]
    reward = data["reward"]
    curriculum = data["curriculum"]
    training = data["training"]

    return TaskConfig(
        environment=EnvironmentConfig(
            seed=env["seed"],
            obstacle_count=env["obstacle_count"],
            obstacle_height_range=tuple(env["obstacle_height_range"]),
            obstacle_width_range=tuple(env["obstacle_width_range"]),
            obstacle_length_range=tuple(env["obstacle_length_range"]),
            spawn_area=tuple(env["spawn_area"]),
        ),
        priors=PriorsConfig(
            footstep_horizon=priors["footstep_horizon"],
            com_height=priors["com_height"],
            head_height=priors["head_height"],
            landing_tolerance=priors["landing_tolerance"],
        ),
        reward=RewardConfig(
            success_bonus=reward["success_bonus"],
            collision_penalty=reward["collision_penalty"],
            tracking_weight=reward["tracking_weight"],
            com_weight=reward["com_weight"],
            head_weight=reward["head_weight"],
            energy_weight=reward["energy_weight"],
            stability_weight=reward["stability_weight"],
        ),
        curriculum=CurriculumConfig(
            stages=[CurriculumStage(**stage) for stage in curriculum["stages"]],
            success_threshold=curriculum["success_threshold"],
        ),
        training=TrainingConfig(
            episodes=training["episodes"],
            episode_length=training["episode_length"],
            log_every=training["log_every"],
        ),
    )
