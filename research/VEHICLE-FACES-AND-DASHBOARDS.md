# Vehicle face and dashboard study (4.1 / 4.2)

## Evidence and decisions

### 2006 Subaru WRX STI

The Subaru owner-manual diagram identifies a three-gauge cluster, a center tachometer with STI marking, a speedometer, and a separate instrument group. The game uses this as a period cue for its amber-ringed, red-needle STI instrument art. It displays live km/h only; the game does not simulate tachometer, rev-limit, fuel, temperature, or DCCD telemetry, so those values are intentionally not faked.

Source: https://www.carmanual.org/OwnersManual/subaru/2006_subaru_impreza_wrx.pdf

### Audi RS 6

Audi's RS 6 documentation describes a 12.3-inch Virtual Cockpit, RS-specific displays, and configurable performance-oriented presentation. The game uses a cool cyan digital-style frame as a visual cue, while its one reliable measurement remains live vehicle speed.

Source: https://uploads.audi-mediacenter.com/system/production/uploaded_files/23920/file/2e3557af8e101b60efd0f280bd174d7c30236ceb/230607_BI_RS_6_Avant_DE.pdf

### Racing-game UI

Forza documents HUD contrast and text scaling as accessibility controls. CrazyAuto keeps the speed number high contrast, labels km/h, and retains a numeric value in the live DOM for assistive/automation integration. The code/layout review of the open-source Aarekaz/f1-game and swaekaa/klustor repositories supports isolating HUD assets from the Three.js scene and validating the playable page through a repeatable browser smoke workflow. These repositories were studied, not copied.

- https://support.forza.net/hc/en-us/articles/20964254277267-Forza-Motorsport-Accessibility-Support
- https://github.com/Aarekaz/f1-game
- https://github.com/swaekaa/klustor

## Art and model contract

- `src/assets/dashboards/*.svg` are separately authored vector drawings; don't recreate them as HTML, don't rasterize unless a target renderer requires it.
- `src/dashboards.ts` selects a dashboard by car ID and maps live km/h to the art's needle angle. Add a new car only with a matching SVG, tested max-speed range, accessible label, and accent.
- Keep the data field truthful: display speed only until drivetrain, RPM, gear, temperature, and assist values exist in the simulation.
- Use car-specific recognition landmarks on both ends: lamp silhouette and placement, grille/cooling layout, hood or auxiliary-lamp feature, tail lamp partition, plate position, and exhaust/diffuser treatment. Compare front, front-three-quarter, rear-three-quarter, and rear views at the actual garage camera size.
- For shape refinement, increase longitudinal cross-section and wheel-arch samples moderately, then compare a baseline screenshot. Avoid adding polygons blindly; keep faceted planes readable and inspect for z-fighting, shading seams, and hitbox changes.
- Verify every asset ID appears in the model catalog and that selection updates both model and instrument art. Run the existing build and browser smoke; review car-selection screenshots plus the drive HUD screenshot.

## License and attribution

All five SVGs and the car mesh edits in this update are original CrazyAuto project work, informed by public visual/documentation references. No commercial screenshots, logos, GitHub code, or third-party car models are distributed by this update. Source terms remain those of each linked reference or repository.
