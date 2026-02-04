from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from obstacle_crossing.config import TaskConfig
from obstacle_crossing.curriculum import CurriculumScheduler, CurriculumStage
from obstacle_crossing.priors import (
    FootstepTarget,
    PriorBundle,
    default_body_targets,
    validate_priors,
)
from obstacle_crossing.reward import RewardTerms, compute_reward
from obstacle_crossing.terrain import generate_obstacles, Terrain


@dataclass
class EpisodeResult:
    success: bool
    reward: float


class SimulatorAdapter:
    """Adapter to connect ASAP or another simulator.

    Replace these stubs with calls to your simulator/environment to
    reset, step, and query contacts/metrics.
    """

    def reset(self, terrain: Terrain, priors: PriorBundle) -> None:
        raise NotImplementedError("Connect to your simulator reset call.")

    def step(self) -> Dict[str, float]:
        raise NotImplementedError("Connect to your simulator step call.")


class Trainer:
    def __init__(self, cfg: TaskConfig, simulator: SimulatorAdapter) -> None:
        self.cfg = cfg
        self.simulator = simulator
        self.curriculum = CurriculumScheduler(
            stages=[
                CurriculumStage(stage.max_height, stage.max_count)
                for stage in cfg.curriculum.stages
            ],
            success_threshold=cfg.curriculum.success_threshold,
        )
        self.reward_terms = RewardTerms(**cfg.reward.__dict__)

    def _build_priors(self) -> PriorBundle:
        footsteps = [
            FootstepTarget(position=(0.2 * idx, 0.0, 0.0), timestamp=idx * 20)
            for idx in range(self.cfg.priors.footstep_horizon)
        ]
        bundle = PriorBundle(
            footsteps=footsteps,
            body_targets=default_body_targets(
                self.cfg.priors.com_height,
                self.cfg.priors.head_height,
                self.cfg.priors.footstep_horizon,
            ),
        )
        validate_priors(bundle, self.cfg.priors.footstep_horizon)
        return bundle

    def _sample_terrain(self, stage: CurriculumStage) -> Terrain:
        return generate_obstacles(
            seed=self.cfg.environment.seed,
            count=min(self.cfg.environment.obstacle_count, stage.max_count),
            height_range=(0.01, stage.max_height),
            width_range=self.cfg.environment.obstacle_width_range,
            length_range=self.cfg.environment.obstacle_length_range,
            spawn_area=self.cfg.environment.spawn_area,
        )

    def run_episode(self, stage: CurriculumStage) -> EpisodeResult:
        terrain = self._sample_terrain(stage)
        priors = self._build_priors()
        self.simulator.reset(terrain, priors)

        reward_total = 0.0
        success = False
        for _ in range(self.cfg.training.episode_length):
            metrics = self.simulator.step()
            reward_total += compute_reward(
                success=metrics.get("success", False),
                collision=metrics.get("collision", False),
                foot_errors=metrics.get("foot_errors", []),
                com_error=metrics.get("com_error", 0.0),
                head_error=metrics.get("head_error", 0.0),
                energy=metrics.get("energy", 0.0),
                stability=metrics.get("stability", 0.0),
                terms=self.reward_terms,
            )
            success = success or metrics.get("success", False)
        return EpisodeResult(success=success, reward=reward_total)

    def train(self) -> List[EpisodeResult]:
        results: List[EpisodeResult] = []
        success_history: List[bool] = []
        for episode in range(1, self.cfg.training.episodes + 1):
            stage = self.curriculum.current_stage()
            result = self.run_episode(stage)
            results.append(result)
            success_history.append(result.success)

            if episode % self.cfg.training.log_every == 0:
                recent = success_history[-self.cfg.training.log_every :]
                success_rate = sum(recent) / len(recent)
                self.curriculum.update(success_rate)
        return results
