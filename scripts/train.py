from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from obstacle_crossing.config import load_config
from obstacle_crossing.training import SimulatorAdapter, Trainer


class PlaceholderSimulator(SimulatorAdapter):
    def reset(self, terrain, priors) -> None:
        self.steps = 0

    def step(self):
        self.steps += 1
        return {
            "success": self.steps >= 50,
            "collision": False,
            "foot_errors": [0.05],
            "com_error": 0.02,
            "head_error": 0.01,
            "energy": 0.1,
            "stability": 0.02,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.json")
    args = parser.parse_args()

    cfg = load_config(args.config)
    trainer = Trainer(cfg, simulator=PlaceholderSimulator())
    trainer.train()


if __name__ == "__main__":
    main()
