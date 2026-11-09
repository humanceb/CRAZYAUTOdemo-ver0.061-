# 4.3 World Overhaul art notes

## Visual references

- [DiRT Rally 2.0: Baranowo, Poland environment art](https://zhiwei.artstation.com/projects/EVb9R8) — study the forest road corridor, nearby terrain breaks, and changing tree masses around bends.
- [Nintendo's art of rally product page](https://www.nintendo.com/en-ca/store/products/art-of-rally-switch/) — a stylized color and landmark reference for keeping road edges, foliage patches and roadside silhouettes distinct at driving distance.
- [FIA Rally Guidelines](https://www.fia.com/sites/default/files/19_02_21_fia_rally_guidelines_2018_full_02_2.pdf) — rally route markers, spectator setbacks, and safety furniture are cues for later stage-authored set dressing.

## 4.3 authored routes

- **Pine Ridge:** keeps its existing loop and handling, with the dirt grain tile repeated tightly over the road.
- **Pikes Peak:** retains the USGS heightfield route and tarmac/gravel shoulders.
- **Frostline:** new seeded loop, snowy road grain, cooler meadow and stone colors, and lower packed-snow grip.
- **Redstone Quarry:** new seeded loop with a broader rocky gravel road grain and dry ochre terrain palette.

Route generation uses independent deterministic seeds so the world builder can produce a repeatable but different tree/rock layout for each map. The two new loop centerlines are intentionally game-designed studies, not claims of matching surveyed public roads. Existing named mascot props remain asset-only and are not automatically placed in any route.
