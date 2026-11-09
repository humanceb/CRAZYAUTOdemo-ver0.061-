# Model-specific face study

## Supplied photo targets for 4.25

- **STI Hawkeye:** The first supplied picture shows rounded twin eye lenses, a Subaru central grille with curved surround, a low broad bumper opening, a hood scoop set behind the nose and a sedan roof. The game keeps its blue rally palette while following those component shapes.
- **Sport Quattro S1 E2:** The second picture shows square main lamps in the fenders, four Audi rings inside the dark center grille, two high round lamps and four lower round lamps on a bracket, plus box arches and a broad white bumper. The model now uses six separate circular rally lamps and a crossbar with uprights.
- **RS 6 Avant:** The third picture shows a deep black Singleframe grille, narrow lamp blades, deep outer air openings and a long wagon roof. The model has separate dark grille, honeycomb cells, outer curtains and four rings.

These user-provided photos guide shape placement; release packages contain our original procedural geometry and renders, not copies of the photos. The three-dimensional car shells still need more proportion work to match the pictures closely.

Procedural front and rear details in `src/otherCars.ts` are deliberately authored per car. Keep this checklist beside the modeling code when refining the 4.0 garage.

| Model | Face cues to preserve | Geometry notes |
|---|---|---|
| Subaru Impreza WRX STI Hawkeye | Swept headlamp outline, wide Subaru wing grille, center trapezoid, separate side-wing grille openings, intercooler opening, rear-set hood scoop, gold wheels, tall rear wing | Let the eye lamps sweep into the fenders; keep the three-part wing grille and move the scoop back onto the hood. Do not reuse the Evo III's rectangular lamps or narrow badge grille. |
| Mitsubishi Lancer Evolution III | Compact rectangular twin-reflector lamps, narrow three-diamond grille, centered rectangular bumper intake, separate corner ducts, deep rally chin, high rear spoiler | Keep the upper grille slim and the central intake rectangular. Separate the corner ducts so the face cannot read as the Subaru wing grille. |
| Audi Sport Quattro S1 E2 | Short, blunt Group B nose, square lamps, four auxiliary rally lamps, broad cooling mouths, large rear aero | Rally pods should sit as a distinct light bar; keep their square reflectors visible. |
| Audi RS 6 Avant C8 | Wide, flat Singleframe grille with honeycomb, sharp Matrix-style lamps, vertical outer air curtains, broad road blade, wagon roof and hatch | Treat grille surround, mesh, badge and bumper as depth layers, with the mesh inset behind the surround. |

## Source references and real-car picture checks

Use the manufacturer's archive or museum collection as the primary shape source. For each model, use front, front-three-quarter, side, rear-three-quarter, and rear views together; do not infer three-dimensional placement from one perspective. Normalize against the published vehicle width, then compare the widths of lamps, grille, and intakes as fractions of that width. These linked photographs are research references only; this project does not redistribute their photos.

- **Evo X / Evo III:** Mitsubishi Motors' [official Car History](https://www.mitsubishi-motors.com/en/company/history/car/) is the primary source for generation identity; it explicitly describes the Evo III's redesigned bumper and larger cooling openings. Compare it with the publisher's [Evo X photo gallery](https://www.webcg.net/articles/gallery/9678) for front-three-quarter proportions.
- **2006 STI Hawkeye:** use the 2006 [Impreza brochure scan](https://www.centuryu.com/uploads/1/4/4/6/144698822/2006_impreza.pdf) for the actual model-year appearance, plus Subaru's period [press material](https://www.subaru.co.jp/en/news/archives/press/2005/05_06_16e.html). Subaru's 2005 [WRC 2006 prototype release](https://www.subaru.co.jp/en/news/archives/press/2005/05_08_05e.pdf) provides a direct front photo but is a rally prototype, so do not confuse its body kit with the production Hawkeye.
- **Audi Sport Quattro S1 E2:** Petersen Automotive Museum's [vehicle record and photo gallery](https://petersen.org/pages/petersen-vehicle/1985-audi-sport-quattro-s1-e2) includes multiple views of a catalogued 1985 S1 E2. It is a strong source for the squared nose, wide arches, and rally lamp arrangement; check the page's image-use terms before reusing any photo.
- **Audi RS 6 C8:** Audi MediaCenter's [RS 6 Avant press information](https://www.audi-mediacenter.com/system/production/uploaded_files/23921/file/fcdafb26ca0c8d5e8cab9bfc4c98d65a5df608c8/230607_BI_RS_6_Avant_EN.pdf?1686126117=&disposition=attachment) and [official dimension drawings](https://www.audi-mediacenter.com/en/publications/dimensions/dimensions-rs-6-avant-1431/download) give factory proportions and a front-three-quarter view.
- **Low-poly finish target:** the user-provided FR Legends screenshots are the style benchmark for rounded low-poly body volumes and clearly separated, well-fitted exterior parts. Consult the [official FR Legends site](https://www.twinturbogames.com/) and the developer's [App Store listing and screenshots](https://apps.apple.com/us/app/fr-legends/id1435740083) for additional game-view context. Use FR Legends as a finish/readability reference, not a source to copy its car assets.

- Audi MediaCenter, RS 6 Avant product information (Singleframe proportions, honeycomb grille, lamps, vertical intakes): <https://uploads.audi-mediacenter.com/system/production/uploaded_files/15878/file/b1d88632d3d98a1d5e5a281460e22fadd7233567/en_BasisInfo_RS_6_Avant.pdf?1572966423=&disposition=attachment>
- Mitsubishi Motors, company history (Evolution III redesigned bumper and aero): <https://www.mitsubishi-motors.com/en/company/history/car/?year=1960s>
- Subaru 2006 Impreza brochure (Hawkeye era reference): <https://www.centuryu.com/uploads/1/4/4/6/144698822/2006_impreza.pdf>
- Petersen Automotive Museum, 1985 Audi Sport Quattro S1 E2: <https://petersen.org/pages/petersen-vehicle/1985-audi-sport-quattro-s1-e2>
- Three.js `ShapeGeometry` and `BufferGeometry` (polygon and batched mesh construction): <https://threejs.org/docs/pages/ShapeGeometry.html>, <https://threejs.org/docs/pages/BufferGeometry.html>

The game models are original low-poly approximations, not copied manufacturer meshes. Use these references for silhouette and component placement; confirm all face geometry follows the car's actual front/rear surface helpers in `otherCars.ts` to prevent clipping or floating parts.

## 2026-11-07 geometry and light pass

The garage references showed the Evo X reading as a more authored object because its shell catches more facets and its lamps have stronger internal contrast. The other cars had nominally unique fascia layouts, but earlier captures still made the STI and Evo III look too similar. The 4.21 review fixed a front-surface alignment mismatch, separated face polygon triangulation from body-panel triangulation, moved the STI scoop onto the hood, and gave the Evo III a narrow badge grille, central rectangular intake, and separate corner ducts. The STI keeps the wider wing grille, swept lamps, and lower mesh. The production build and headless smoke check passed for all five selectable cars without browser errors.

The FR Legends style check favors a smooth readable roof/hood/fender shape with restrained facets, plus separate recognizable lamps, grille, and intake parts. A small authored crosshatch SVG is used only on the Evo III grille insert; the rest of the fascia remains low-poly geometry. The broader shell still falls short of the user-provided model-quality target and needs a later car-by-car silhouette pass.

For visual review, `qa/` keeps model-only screenshots: direct front, front three-quarter, and rear three-quarter for every car. The smoke script hides the garage UI while capturing these so the body silhouette and fascia can be compared cleanly. Treat the images as a quality gate, not an OEM-accuracy claim; the shared low-poly chassis still needs car-by-car silhouette work before calling it reference-accurate.

The garage display was shifted clear of the title and brought to a more face-visible three-quarter view. The production build and headless smoke check passed for all five selectable cars with no browser errors. The rendered result is a style/detail improvement, not an OEM-accuracy claim; inspect full front, side, and rear views before further curve tuning.
