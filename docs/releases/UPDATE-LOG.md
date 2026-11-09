# CrazyAuto release updates

## 6.0 — All Cylinders

- Promoted the cumulative ten-car, four-stage game from 5.5 into the new official major release without replacing earlier subreleases.
- Added the selected car's instrument preview and clearly labeled estimated game-tune facts to the 3D garage.
- Packaged the same current client as a local web build, a self-contained Google Apps Script page, and a portable Electron desktop window. The desktop package passed a hidden smoke check for ten cars, four stages, game API, and dashboard preview.
- Preserved the older Pygame build as a historical checkpoint because it does not contain the current ten-car/dashboard content.
- Bundled a snapshot of the CrazyKids car-engine and drift skills, added a desktop launcher and installer script, and retained third-party runtime notices.
- Google Apps Script has been prepared locally but has not been deployed to the user's Google account.

## 5.5 — Ten Car Garage

- Added GR Yaris, Delta HF Integrale, Peugeot 205 Turbo 16, Celica GT-Four ST205, and Ford RS200 stylized study models and estimated four-wheel setups.
- Added six generated transparent instrument plates, including Evo X, with live HTML speed and pedal overlays. Prior STI, Evo III, Quattro S1, and RS 6 SVG dashboards remain car-specific.
- Ramped digital throttle/brake, tapered drive torque with speed, released brake pressure during impending wheel lock, and delayed reverse until S is held at rest.
- Measured 6.23 s from 0–100 km/h and 56.1 m / 4.0 s from 100–0 on the flat tarmac check world. These are gameplay estimates.
- Bundled a local web build and a self-contained Google Apps Script page. Google deployment is a separate sign-in step.

## 5.3 — Countersteer Clinic

- Fixed the drift-catch direction check: the browser previously classified steering with lateral motion as countersteer. It now recognizes steering against the latched slide direction.
- Kept the slide direction briefly through zero body slip. Countersteering now fades smoothly near alignment instead of returning to full steering lock on the first frame the car straightens.
- During an actual catch, the rear tires progressively regain handbrake-reduced grip and handbrake torque tapers. Ported the same behavior to Pygame.
- Removed the browser's extra steering-derived yaw command. Normal turning yaw now comes from the front tire forces; a bounded high-slip recovery assist remains.
- Added a browser physics HUD cue for `COUNTERSTEER`, `UNWIND COUNTERSTEER`, `SLIDE`, and `GRIP`.
- Research note: `PHYSICS-5.3-COUNTERSTEER-RECOVERY.md` records official Forza telemetry fields, BeamNG's tire-data calibration note, SAE combined-slip/transient tire modeling, and a GitHub rally tire model studied without copying.
- Verification: TypeScript/Vite build and Python syntax compilation. A human still needs to confirm the catch timing and turn-in feel in the actual game.

## 5.2 — Grip Before Glory

- Fixed fast ordinary steering that could saturate the tires and kick the car into an unwanted drift. Both builds now cap the requested steering angle against available surface grip as well as the car's steering setup and speed limit.
- The Pygame build now matches the browser's grip-based steering ceiling. The browser gradually reserves up to 18% lateral grip above 12 m/s, reaching the full reserve at 30 m/s; low-speed lock remains unchanged.
- Kept handbrake entry, rear grip release, clutch-kick torque, combined tire slip, countersteer recovery, steering animation, suspension roll, and smoke intact. The intent is “planted by default, slide when asked.”
- Research note: `PHYSICS-5.2-GRIP-LED-DRIFT-ENTRY.md` explains what public Forza and driving-instruction sources support, what is inference, and the checks still needed. Commercial game source and exact tuning values are not public.
- Verification: Vite production build and Python syntax compilation. Human drive feel on the shipped Google Apps Script page still needs a player pass.

## 5.1 — Spring & Smoke

- Added a bounded, reusable low-poly smoke pool. Puffs emit from individual rear tires under sustained tire slip and from any tire pushed into braking lock, rise, expand, fade, and recycle. The visual effect applies no force and cannot change grip.
- Increased S/Down braking torque by 18%. Braking and cornering still share each tire's combined-slip force budget, so hard braking while turning reduces lateral grip and can start a controllable slide.
- Replaced the underdamped, nearly fixed suspension setting with per-wheel damping derived from the car's sprung corner mass and spring rate (`c = max(c_setup, 0.68 × 2√(k m_corner))`). It targets a calmer response while remaining below critical damping; each car keeps its own spring, mass, and setup values.
- Applied the four simulated wheel travel values to the visible wheel pivots, so body roll/bumps move the wheels relative to the chassis while retaining all four wheel meshes.
- Ported the same 18% brake increase and mass-derived damper target into the native Pygame build. Added a bounded low-poly smoke pool to the Pygame scene as well; the compatibility renderer uses quantized opacity values to keep its display-list cache bounded.
- Added the best preserved 2.x, 3.x, and 4.x playable builds to the official release history: CrazyAuto 2.0, CrazyAuto 3.0, and 4.5 Weight Shift. Each stays intact as its own three-folder package; the curated 4.5 snapshot omits nested duplicate 200 MB archives.
- Research: SAE combined braking-and-steering tire work supports sharing longitudinal and lateral force limits; vehicle roll research supports tuning spring/damper/roll behavior as connected suspension properties. This is a game approximation, not measured car calibration.
- Verification: TypeScript/Vite production build and Python syntax compilation passed. In-game human feel and Apps Script-hosted play still need a user drive session; no live Google deployment was made.

## 4.5 — Weight Shift

- Reduced the speed-based steering cut by 18% and raised the default lateral-acceleration ceiling from 0.84 g to 1.00 g (1.08 g during handbrake entry) to reduce persistent understeer.
- Positioned front and rear axle force application points around each car's estimated CG using its front axle-load fraction. Acceleration and braking pitch moments now use the correct unequal axle distances instead of a centered wheelbase.
- Preserved explicit front-wheel steer-pivot animation and wheel spin; verified the draw loop applies simulated steering angle to the front pivots.
- Added exponential Lerp steering input for digital keyboard keys and a separate rendered wheel-angle interpolation so steering-in and unwind are visible and smooth.
- Replaced independent tire-force saturation plus post-clamp with one combined-slip ellipse; throttle/brake now consume lateral cornering capacity at the same wheel.
- Research: Criterion's GDC vehicle-feel talk supports tuning player assists as a separate layer over physical response; tire slip-based friction guidance motivates retaining the combined grip limit. Vehicle axle-load estimates remain approximate and trim-dependent.

## 4.42 — Lost Parts Found

- Fixed the car optimizer: indexed box meshes and non-indexed fascia polygons now use separate batches. A failed merge keeps its original meshes instead of deleting them.
- Restored STI, Quattro S1 and RS 6 front lamp, grille, intake and trim layers while retaining normal depth testing; curved front polygons now follow the bumper profile across their width.
- Checked headless direct-front garage images for STI, Quattro S1 and RS 6 and a direct-rear RS 6 image. Front elements are visible again and do not show through the rear.

## 4.41 — Front Faces Stay Put

- Removed the disabled depth testing and forced render order from the STI, Quattro S1, and RS 6 front fascia layers, auxiliary lamps, and badges. Those settings made some front parts visible through the car from rear or side views.
- Seated their curved front skins slightly ahead of the body and added side return panels, matching the Evo III's physical fascia approach.
- Kept the 4.4 rear improvements and previous vehicle/world features. Rebuilt browser and Apps Script packages; a live garage angle review is still needed.

## 4.4 — Rear View Revival

- Resculpted the shared rear clip into five connected width segments with rounded-back corners.
- Separated STI and Evo III rear lamps and bumper layouts; gave the STI a lower dual-plane wing and the Evo III a taller wing with brake strip.
- Kept the Quattro's square Group B rear cluster; changed the RS 6 C8 to separate segmented light units and oval exhaust outlets rather than a full-width hatch bar.
- Reshaped the Evo X rear lamp pockets, clear sections, number recess, and diffuser fins.
- Rebuilt the browser and Apps Script editions. These are stylized procedural models; visual inspection in the target game window remains required.

## 4.34 — Seated Diamond

- Replaced the Evo III's front-only drawing override with a physical curved fascia that uses normal depth testing and side return panels.
- Moved raised lens cells, reflectors, and grille slats from roughly 34–40 cm ahead of the nose to shallow, layered offsets around 10–15 cm. The parts now follow the bumper's x-dependent crown.
- Kept the existing car silhouette, other cars, UI, and four tracks. Rebuilt the browser and Apps Script outputs; in-game visual inspection is still needed.

## 4.33 — Uncovered Diamond

- Added a continuous curved Evo III front skin ahead of the old bumper and hood edge, then layered its grille, lamps, reflectors, indicators, and badge above that skin.
- Removed the Evo III rule that hid detail meshes, so the existing parts are visible in the garage view. The four 4.3 tracks and other car models remain.
- Built the browser edition and regenerated the Apps Script source. Visual inspection in the target Apps Script deployment remains pending.

## 4.32 — Diamond Nose Classic

- Restored the Evo III front behavior exactly as shipped in 4.23 Diamond Nose, including its selective fascia visibility rule. The 4.31 change to that rule altered the intended look.
- Kept the later STI, Quattro and RS 6 changes, dashboard UI, and four 4.3 tracks.
- Archived 4.31 alongside all earlier checkpoints.

## 4.31 — Diamond Lights Return

- Restored the Evo III front-detail meshes that the 4.3 visibility filter accidentally hid: segmented rectangular lamps, reflectors, grille slats, and lower corner lamps.
- Kept the curved bumper skin and the 4.3 four-track world. The model source had remained identical to 4.26; the regression was a draw-visibility rule, not missing geometry.
- Built the browser edition and exported a fresh Apps Script edition. The original 4.3 package remains archived.

## 4.3 — World Overhaul

- Added two loop roads with distinct route profiles: Frostline (snow) and Redstone Quarry (gravel), alongside Pine Ridge and the existing Pikes Peak stage.
- Each loop gets an independent seeded terrain and vegetation layout, its own road mesh, and a tightly repeated surface grain texture; Frostline also uses the snow texture palette and reduced grip.
- Expanded the garage stage picker to four tracks and made the HUD report the selected route and current surface.
- Preserved Pine Ridge's original handling, and kept the USGS Pikes Peak stage available.

## 4.26 — Pit Stop Oddballs

- Researched DiRT Rally 2.0 forest environment art, official art of rally imagery, and the Jimothy raccoon story for visual cues.
- Added three original, low-poly, standalone world prefabs: a round raccoon pit-crew mascot, a joke marshal sign, and a seeded autumn leaf scatter.
- Kept the asset module unreferenced by stage builders, so none of the objects appear on a track until a map author deliberately imports and places them.
- Added an asset README with usage examples and research links. The raccoon is an original stylized tribute, not a copied photograph or fan illustration.

## 4.21 — Grille Golems

- Started separate procedural face layouts for the STI Hawkeye, Evo III, Quattro S1 and RS 6.
- Added the first manufacturer and museum reference sheet and a repeatable model-only garage review workflow.
- Preserved this source checkpoint in the 4.21 release archive; its remaining fit/readability issues drove the 4.22 nose-surface corrections.

## 4.25 — Joined at the Nose

- Used the three supplied photographs as specific shape references for the STI Hawkeye, Sport Quattro S1 E2 and RS 6 Avant.
- Added a segmented body-color front skin for each model so the lamp, grille and bumper pieces sit over one continuous nose surface in the garage view.
- Replaced the Quattro's floating square rally pods with the photographed two upper and four lower round lamps, with a crossbar and two upright supports.
- Kept the STI's broad grille and swept eyes separate from the RS 6 Singleframe and honeycomb. All front skins use the same faceted nose profile as their car body.
- Browser model and drive check passed; these remain stylized procedural studies rather than exact vehicle replicas.

## 4.24 — Three Faces, One Garage

- Made the STI Hawkeye lamps, broad grille, rear-set hood scoop and compact intercooler opening readable at the garage camera.
- Brought out the Sport Quattro S1's squared lamps, central grille, four rally pods and a narrower lower intake; added a visible support for the auxiliary lamp bar.
- Made the RS 6 C8's sharp lamp outlines, dark Singleframe grille, lighter honeycomb cells and four-ring badge visible.
- Checked front and three-quarter renders of all three cars. These are still stylized study models, with further body silhouette work needed to match the reference photographs closely.

## 4.23 — Diamond Nose

- Rebuilt the Evo III's bumper cross section around a more pronounced center crown, with the main grille mesh following that physical curve in 24 sections.
- Brought the long rectangular headlights, amber outside indicators, narrow Mitsubishi grille and three diamond badge forward so the body skin no longer hides them in the garage camera.
- Reduced the central cooling mouth and added a separate intercooler strip and corner ducts using the supplied 1995 Evo III photo as the visual target.
- Inspected fresh front and three-quarter renders and confirmed the car selector and driving input still run without browser errors.

## 4.22 — Wing vs. Diamond

- Reworked the car-face review using linked manufacturer, brochure, and museum photo references for all five vehicles. Exact reference links and source-use notes are in `MODEL-FACE-STUDY.md`.
- Corrected the shared front-surface helper to follow the body nose's center, shoulder, and outer-corner facets, so fascia details follow the shell profile.
- Separated front/rear fascia triangulation from longitudinal body panels. Concave face outlines are triangulated in their own plane to avoid outlines crossing their notches.
- Increased the STI/Evo III contrast: the Hawkeye keeps the wide three-part wing grille and swept lamp form, with the scoop seated farther back on the hood; the Evo III uses rectangular twin reflectors, a narrow badge grille, a centered rectangular intake, and separate corner ducts.
- Added an original tiny crosshatch SVG for the Evo III intake mesh. It is a restrained low-poly pattern asset mapped onto its separate grille insert, not a photo texture.
- Added model-only direct-front, front-three-quarter, and rear-three-quarter screenshots for each of the five cars. The capture script hides the fixed menu overlay before it takes the images.
- Scope: the body shells remain stylized procedural shapes. This update improves facial recognition and component seating; it does not claim OEM-accurate full-body modeling.

## 4.2 — Driver instruments

- Added five original, separately drawn SVG speed dials for Evo X, STI, Evo III, Quattro S1, and RS 6. Each uses its own period/vehicle-inspired visual language and accent palette; the displayed speed and needle update from the running vehicle speed.
- Followed an image-first UI workflow: SVG files provide the visible dial artwork, while JavaScript selects the asset and animates its needle and number; HTML remains the shell and accessible host.
- Each dashboard header switches with the selected car and names its AWD system as a static vehicle cue; only speed is presented as live telemetry.
- Embedded the SVG artwork in the TypeScript build, so the same visuals travel with the single-file Apps Script export.
- Kept a hidden numeric speed field for existing telemetry integrations and small-screen fallback compatibility.
- Improved HUD contrast and small-screen sizing, guided by Forza's published HUD contrast/text-scaling accessibility settings.

## 4.1 — Recognizable car faces and smoother sculpting

- Increased procedural body profile samples from 56 to 72 and wheel-arch facets from 18 to 24. This softens hood, shoulder, and fender transitions while keeping deliberate low-poly panel faces.
- Increased the front nose wrap across its center-to-fender sections so each car's distinct light housings, grille, and cooling openings sit on a more sculpted fascia.
- Tightened the desktop auto-show camera framing so distinctive front and rear features read larger in the model picker.
- Preserved car-specific front/rear signatures: Hawkeye lamps and divided grille on STI; twin rectangular lamps and separate cooling openings on Evo III; square Group B lamp pods and block rear lights on Quattro S1; wide honeycomb grille/matrix lamps and hatch-spanning LEDs on RS 6.
- The geometry is an original stylized study, not a dimensionally exact scan. View-by-view reference review remains necessary before claiming high visual accuracy.

## References used

- Subaru, 2006 Impreza WRX/STI owner manual, instrument-cluster diagram: https://www.carmanual.org/OwnersManual/subaru/2006_subaru_impreza_wrx.pdf
- Audi MediaCenter, RS 6 Avant information (virtual cockpit and RS-specific display options): https://uploads.audi-mediacenter.com/system/production/uploaded_files/23920/file/2e3557af8e101b60efd0f280bd174d7c30236ceb/230607_BI_RS_6_Avant_DE.pdf
- Forza Motorsport HUD contrast/text scaling guidance: https://support.forza.net/hc/en-us/articles/20964254277267-Forza-Motorsport-Accessibility-Support
- GitHub HUD/module study: https://github.com/Aarekaz/f1-game
- GitHub Three.js racing HUD and page separation study: https://github.com/swaekaa/klustor

The GitHub projects informed module boundaries and smoke-check workflow only. No code or artwork was copied. CrazyAuto's dial drawings and model meshes remain original project assets.

## 6.01 — Five-View Bodywork (9 November 2026)

- Preserved the original 6.0 as `SUB RELEASES/6.0-All-Cylinders-Original` before editing.
- Rebuilt the five added cars with connected curved front/rear caps and side wraps. Removed the detached rear facade panel.
- Adjusted the roof, windows, A/B/C pillars, rear quarters, fender widths, wheel faces, wing mounts, headlamp seating, grilles, vents, and tail-lamp graphics per vehicle.
- Generated five-view low-poly concept sheets, kept as visual guides with real-car reference links in `UPDATE NOTES/6.01-Five-View-Bodywork.md`.
- Added an unobtrusive `?reviewCar=...&view=...` renderer QA route. Built the TypeScript/Vite bundle and inspected five cars in a hidden browser without console errors.
- Re-exported the HTML, Apps Script, and portable app files from the same source; updated the CrazyKids skill's five-view modeling procedure.
- These are stylized study models; silhouette and panel accuracy still require further per-car sculpting before claiming Evo-level quality.

## 6.02 — Coupe and Doors (9 November 2026)

- Used direct side renders to shorten the Celica roof and lengthen its rear-glass slope, and raised the RS200 engine deck to distinguish the mid-engine silhouette.
- Added door cuts to the five model studies and preserved the 6.01 geometry checkpoint.
- Rebuilt all three delivery formats and passed a hidden portable Windows smoke check selecting all ten cars and loading all four stages.

## 6.03 — Mesh Magic (9 November 2026)

- Changed all five added cars to use X/Y-varying front and rear face profiles, with connected hood/deck end strips and narrower car-specific nose widths.
- Seated lamps, intakes and tail lights against the local curved surface to reduce floating components in front/rear three-quarter views.
- Drew cached low-poly grille and lens patterns as code-native `CanvasTexture` materials; kept geometry as the depth/occlusion source.
- Rebuilt and reviewed hidden game-renderer views; no browser console errors. Preserved 6.0, 6.01 and 6.02 separately.

## 6.04 — Side Stories (9 November 2026)

- Added car-specific side panel art drawn in code, including door and trim cues.
- Moved 205 T16 and RS200 mid-engine side intakes clear of the rear wheel openings; inspected direct side views.
- Retained the previous 6.03 checkpoint and all cumulative features.

## 6.05 — Faceted Forms (9 November 2026)

- Rebuilt the five added cars' hood sections as car-specific center, crease, and outer facets, with matching cap connectors.
- Bridged the body sides to window bases with sampled belt strips and shared A/B/C pillar coordinates.
- Tessellated curved grille/lamp patches so their center stays ahead of the fascia; added a recessed square RS200 headlight pod.
- Varied wheel spoke count by car, reduced glass glare and garage overexposure, and visually checked five-angle model views.
- Rebuilt the web, local Apps Script, and portable desktop packages; 6.04 and older checkpoints remain preserved.
# CrazyAuto 4.3 — distinct front faces

- Reworked face proportions around body width: STI Hawkeye now has a wide wing grille with swept lamps; Evo III now has compact rectangular twin lamps, a narrow center grille, and a separate lower cooling mouth.
- Scaled lens, grille, and reflector pieces to their actual visual role, reducing details that became noisy at garage distance.
- Kept rear lamp signatures and the Quattro/RS 6 front layouts model-specific.
- Checked in the selected-car garage views and the browser smoke workflow.

Research references: `MODEL-FACE-STUDY.md`, Subaru 2006 brochure/manual references, and the Three.js geometry construction links recorded there. These are original procedural interpretations, not copied models.


## 0.0601 — All Cylinders: Reindexed (9 November 2026)

- Adopted the user's exact version label 0.0601 for the current cumulative game.
- Updated game title, garage, desktop launcher, splash, package metadata, and Google export.
- Gameplay, ten cars, four stages, and the 6.05 model improvements are carried forward unchanged.
- Kept the 6.05 checkpoint and older releases intact. npm metadata uses valid semver 0.6.1 while the product displays 0.0601.

## 0.0602 — The Long Way Round (9 November 2026)

- Added six original routes for ten total: three longer loops, a Motu-inspired point-to-point sprint, desert raid practice, and a mixed-surface rallycross practice circuit.
- Added route-map SVG assets, car glyphs, a graphic main menu, Garage/Enter Race/Daily Log/Driver ID flow, local profile persistence, and Sport/SUV class filtering.
- Added the independent CK Trail 4×4 SUV model, setup and instrument panel; retained all ten earlier cars.
- Corrected dirt-road material response and the HUD surface label; preserved earlier handling and terrain contracts.
- Built local web, portable desktop, and Google Apps Script packages. The Google deployment remains local and unpublished.


## 0.061 — Gripline (9 November 2026)
- Added analog gamepad steering, throttle, brake, and handbrake axes with progressive smoothing.
- Drift assist now enters on deliberate handbrake plus steering; wheel level grip/load-transfer physics remain active underneath.
- Inspired by the user-provided Race Driver: GRID / Racing Master control notes. Their exact title attribution and game internals are unverified; this release uses the notes as design reference, not a claim of simulation parity.
- Existing routes, cars, UI, speed effect, and Jimmothy roadside props are retained.

