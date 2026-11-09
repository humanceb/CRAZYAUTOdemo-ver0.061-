# 5.3 — Countersteer clinic

## Player report

At higher steering input, the car breaks into a slide too readily, and opposite lock does not reliably catch it. The 5.2 high-speed steering reserve was not enough by itself: the browser's countersteer detector used the same sign as body sideslip, while steering forces produce lateral velocity with a known sign in this coordinate frame. That meant the handbrake grip return and catch logic could miss the player's actual recovery input.

## Research

- Forza's [public telemetry documentation](https://support.forza.net/hc/en-us/articles/21742934024211-Forza-Motorsport-Data-Out-Documentation) exposes per-wheel slip angle, slip ratio, combined slip, velocity, yaw rate, and steering. This supports using tire and chassis state separately to judge when grip is being used and whether a slide is being caught. Its normalized values describe Forza's telemetry conventions, not CrazyAuto thresholds.
- BeamNG's [tire development report](https://www.beamng.com/game/news/blog/tire-physics-development-sneak-peek/) says reliable tire behavior requires reference data and calibration, and describes their work with Calspan to measure tire performance in varied conditions. This is why CrazyAuto should not invent a “realistic” peak angle and call it calibrated.
- SAE's [combined-slip and transient tire model paper](https://saemobilus.sae.org/articles/a-new-semi-empirical-method-estimating-tire-combined-slip-forces-moments-handling-maneuvers-2015-01-9112) describes measured pure-slip curves, combined-slip weighting, and relaxation-length transient response. It supports separating (1) tire response, (2) driver steering, and (3) a bounded recovery aid.
- The [LibreRally open-source tire model](https://github.com/LibreRally/LibreRally/blob/main/LibreRally/Vehicle/Physics/TyreModel.cs) is useful code to study for a rally high-slip force-retention curve. Its source comments cite research but its chosen settings are not a measured CrazyAuto calibration, so this update does not copy its code or constants.

## Changes

- Browser countersteer detection now uses the sign of the latched slide direction and steering command. The previous condition was reversed. The slide side stays latched briefly through near-zero body slip, so holding countersteer across alignment fades the steering request rather than instantly switching back to full lock and creating a second slide.
- While countersteering, the rear tire recovers handbrake-reduced grip and handbrake torque fades smoothly, improving the driver's ability to catch the car while releasing SPACE.
- Removed the browser assist's second steering-derived yaw command. Front tire forces now create ordinary cornering yaw; the bounded high-sideslip assist remains for an actual recovery situation. This removes a duplicate yaw source that could make steering feel like it directly animated the chassis.
- Ported slide-side latching, opposite-lock detection, handbrake grip recovery, and near-alignment steering fade to the Pygame build.
- Added a small browser HUD cue: **COUNTERSTEER**, **UNWIND COUNTERSTEER**, **SLIDE**, or **GRIP**, derived from simulated body sideslip and steering input.

## Intended driving response

Normal steering should build yaw through front-tire force. If the player exceeds grip, the slide develops from the tire model rather than from a steering-to-yaw shortcut. During a slide, steering against the latched body-slip direction should restore rear grip and help the front wheels pull the car back into line. As body slip falls toward zero, the recovery cue changes to “UNWIND COUNTERSTEER”; release the opposite key or steer back toward the intended line.

This is a keyboard-friendly assist layered over the tire simulation, not a literal electronic stability-control system. It cannot reproduce the per-wheel brake interventions in a real ESC because CrazyAuto has no independent wheel brake controller.

## Verification targets

Build the browser and compile the Python source. In a human drive pass, check both turn directions and all cars: (1) a normal steady turn does not get extra yaw from an assist, (2) handbrake entry still initiates a slide, (3) opposite lock reduces slip and restores rear grip, (4) steering fades near alignment so a held key does not start a second slide, and (5) the HUD cue follows the actual input and body-slip state. Check tarmac, gravel, and snow separately. Do not treat a code build or the earlier regression profiles as a completed player-feel check.
