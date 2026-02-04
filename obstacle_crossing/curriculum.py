from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CurriculumStage:
    max_height: float
    max_count: int


@dataclass
class CurriculumScheduler:
    stages: List[CurriculumStage]
    success_threshold: float
    stage_index: int = 0

    def current_stage(self) -> CurriculumStage:
        return self.stages[self.stage_index]

    def update(self, success_rate: float) -> CurriculumStage:
        if success_rate >= self.success_threshold and self.stage_index < len(self.stages) - 1:
            self.stage_index += 1
        return self.current_stage()
