# 5.2 — Grip-led steering and intentional drift entry

## Goal

Ordinary fast cornering should remain a planted turn. A visible rally slide should come from a deliberate entry (weight-transfer flick, handbrake, or a torque/clutch input), not from simply holding a steering key at road speed. Preserve opposite-lock recovery and the physical roll state.

## Research and interpretation

- Turn 10's [Forza Motorsport accessibility guide](https://support.forza.net/hc/en-us/articles/20964254277267-Forza-Motorsport-Accessibility-Support) describes Normal steering as damping some physical effects and Simulation steering as removing steering-speed assistance. Its Stability Control description is a separate intervention. This supports separating steering accessibility from an explicit slide/stability system; it does not reveal Forza's private tire equations.
- Turn 10's [tire and Drivatar overview](https://forza.net/news/forza-motorsport-drivatars-tire-physics) describes multi-point tire contact and the AI's separate throttle, brake, and steering controller. The useful architecture lesson is that driver input is a request to the vehicle, while tire contact decides what force is available.
- Criterion's [GDC Vehicle Feel Masterclass](https://media.gdcvault.com/gdc2018/presentations/Harris_Matthew_VehicleFeelMasterclass.pdf) treats assists as a tunable part of vehicle feel and recommends progressive behavior and telemetry. This is a game-feel design source, not a rally setup specification.
- For driver technique, the [DirtFish pendulum-turn report](https://dsportmag.com/the-scene/getting-behind-wheel-learn-rally-race-dirtfish-rally-school/) and [Car and Driver Scandinavian-flick guide](https://www.caranddriver.com/features/a16581160/how-to-scandinavian-flick-feature/) describe a deliberate steering/load-transfer sequence, followed by opposite lock and a controlled unwind. They do not say that ordinary high-speed steering should automatically create a drift.
- SAE's [combined braking and steering tire-force paper](https://saemobilus.sae.org/papers/modeling-combined-braking-steering-tire-forces-2000-01-0357) supports keeping braking and cornering inside one tire-force budget. That budget remains separate from the player-facing entry assists.

These are public design and driving references. No Forza, Gran Turismo, or Dirt Rally source code or secret parameter values are used. CrazyAuto's approximation is an inference for this keyboard-driven prototype, not a measured-car calibration.

## Implementation

The Pygame build now caps requested wheel angle by all three bounds: car steering lock, speed-scaled steering, and an available-grip cornering bound. The browser build already had the grip bound; it now reserves up to 18% of lateral grip at road speed, with the reserve fading in above 12 m/s and reaching its maximum at 30 m/s. Low-speed steering is unchanged. Loose surfaces lower the cap through their own grip values. The handbrake retains its wider entry allowance and rear-axle grip cut.

The bound is a driver-friendly demand limit, not an added tire force. Once the player deliberately initiates a flick, handbrake turn, or clutch/power entry, the existing combined-slip tires can saturate, yaw, and body roll. Opposite-lock logic remains available to catch the slide.

## Tuning and observable checks

- Straight-line full lock must not cause a yaw impulse.
- A broad, steady high-speed turn should remain below tire saturation on dry tarmac; rough gravel/snow should reach the cap sooner because the sampled grip is lower.
- A short handbrake entry, a steering flick with lift/brake, and a clutch/power entry remain distinct inputs and should still exceed the normal body-slip band.
- Countersteer must reduce body slip and yaw without creating a second slide at alignment.
- Check both left and right turns, all five cars, and tarmac/gravel/snow. Capture speed, steering angle, per-wheel slip, body sideslip, yaw rate, wheel load, and roll.

## Limitations

We do not yet have measured tire curves, steering-ratio maps, differential torque maps, or a validated human-driven lap dataset. The new cap should improve high-speed keyboard feel, but a player still needs to confirm the final timing in the browser and Pygame builds. Do not describe this as simulation-grade tire calibration.
