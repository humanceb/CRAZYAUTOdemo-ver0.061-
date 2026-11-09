# CrazyAuto 5.1: braking, drift smoke, and suspension

## What the references support

- SAE's paper on [combined braking and steering tire forces](https://saemobilus.sae.org/papers/modeling-combined-braking-steering-tire-forces-2000-01-0357) explains that braking and cornering forces act together at the tire contact patch and must be combined under a friction limit. CrazyAuto keeps its simplified combined-slip ellipse and increases brake torque at the wheel; once the tire saturates, steering force falls. This is a game approximation, not the paper's tire model.
- SAE's [evaluation of vehicle roll behavior](https://saemobilus.sae.org/papers/evaluation-improvement-vehicle-roll-behavior-970093) describes tuning roll sensation through suspension properties including roll centers, nonlinear load changes, and damping. CrazyAuto's current planar chassis does not model those kinematics; the reference motivates treating suspension feel and roll as a coupled system rather than adding a tilt animation.
- A quarter-car damper reference is the standard critical-damping relation `c_crit = 2√(k m_sprung_corner)`. CrazyAuto estimates sprung mass by removing four unsprung wheel masses and splitting the remainder by each car's front/rear weight fraction. It targets `ζ = 0.68` (below critical), while honoring the car's existing minimum damper value. This reduces excess oscillation without claiming a validated rally damper curve.
- Three.js documents transparent materials and particle rendering in its [transparency guide](https://threejs.org/manual/pages/transparency.html). The game uses a fixed 28-puff pool of small low-poly spheres, not an unbounded particle allocation.

## Implemented behavior

- `src/physics.ts`: each wheel calculates its damper from its sprung corner mass and spring stiffness. Wheel slip ratio is stored alongside slip angle. S applies 1.18× setup brake torque; tire force still saturates through the combined-slip calculation.
- `src/driftSmoke.ts`: smoke is purely visual. Rear tires emit when tire slip angle passes 0.13 rad; all tires can emit under hard braking when longitudinal slip magnitude exceeds 0.28. Puffs drift backward/up, expand, fade, and recycle.
- `src/main.ts`: the fixed 120 Hz step advances the smoke pool and uses simulated suspension travel to move the visible wheel pivots. Chassis roll remains force-driven.
- Native Pygame (`AI-Game-Demo/Desktop/CrazyAuto-Demo/game/vehicle.py`, `game/suspension.py`, `game/drift_smoke.py`, `main.py`) uses the same brake multiplier and damping target. Its smoke puffs are fixed-capacity world-space octahedra with quantized alpha, preventing unbounded display-list cache growth.

## Limits and checks

Both game builds are not full 6-DOF vehicle dynamics. They still lack measured damper curves, suspension link kinematics, ABS, tire relaxation, and reference-car braking/ride traces. Build/syntax checks verify compilation only; human play is still required to judge braking distance, smoke visibility, suspension harshness, and wheel/body fit on the actual stage.
