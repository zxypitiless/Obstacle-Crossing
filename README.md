# Obstacle Crossing (ASAP-aligned)

This repository contains a minimal, end-to-end scaffold for training a full-body controller
that can stably step over obstacles on flat ground. It follows the workflow described in ASAP
(https://github.com/LeCAR-Lab/ASAP) and adds explicit conditioning on footstep, CoM, and head
position priors at the start of a demonstration.

## What's included

- **Environment & obstacle generation**: parameterized terrain/obstacle sampling.
- **Priors**: structured representation for footstep, CoM, and head targets.
- **Rewards**: stable crossing objective with collision, tracking, and energy terms.
- **Curriculum**: difficulty scheduling from easy to complex obstacle layouts.
- **Training entrypoint**: a script that wires all components and exposes TODOs for
  integration with ASAP or your preferred simulator.

## Quickstart

```bash
python scripts/train.py --config configs/default.json
```

> Note: This is a scaffold. Integrate with your simulator (Isaac Gym, MuJoCo, etc.) and
> ASAP training loop where indicated in the code.

## File map

- `obstacle_crossing/config.py`: configuration dataclasses + JSON loader.
- `obstacle_crossing/terrain.py`: obstacle layout generation.
- `obstacle_crossing/priors.py`: footstep/CoM/head priors and validation.
- `obstacle_crossing/reward.py`: reward computation helpers.
- `obstacle_crossing/curriculum.py`: curriculum scheduler.
- `obstacle_crossing/training.py`: training loop scaffold.
- `scripts/train.py`: command-line entrypoint.
- `configs/default.json`: baseline configuration.

## Next steps

1. Replace the `SimulatorAdapter` stub with ASAP environment hooks.
2. Feed perception inputs (heightmap, obstacle features) into the policy.
3. Plug in your policy/wbc implementation and connect rewards to RL.

