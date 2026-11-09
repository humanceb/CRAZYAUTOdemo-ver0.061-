# CrazyKids rally world prop prefabs

These original Three.js props are intentionally unplaced. Import only the prefab you want from `rally-reward-assets.ts` and add it to a stage yourself.

```ts
import { createJimmothyMascot, createSnackMarshalSign, createAutumnLeafScatter } from './assets/props/rally-reward-assets';

// Explicit stage-author placement, not run by this asset module:
// world.add(createJimmothyMascot());
// world.add(createSnackMarshalSign());
// world.add(createAutumnLeafScatter(101, 24));
```

`createJimmothyMascot()` makes an original short, round raccoon crew mascot. It takes the round silhouette as a broad visual cue from the viral Jimothy story, without copying its photos or fan art. `createSnackMarshalSign()` is an original joke sign. `createAutumnLeafScatter()` makes a seeded, low-poly leaf patch for later surface dressing.

Visual study links:

- [DiRT Rally 2.0 environment art: Baranowo, Poland](https://zhiwei.artstation.com/projects/EVb9R8) — use the forest layering and terrain color breakup as scene-density cues.
- [Official art of rally screenshots](https://www.nintendo.com/us/store/products/art-of-rally-switch/) — use the bold roadside silhouettes, color blocks and readable ground details as stylization cues.
- [Jimothy the raccoon background](https://www.smithsonianmag.com/smart-news/an-unusual-looking-raccoon-nicknamed-jimothy-is-winning-hearts-across-the-internet-for-his-short-round-body-180989157/) — context for the mascot concept; do not use the news photos as game textures.

All prefabs are separate from `world.ts`; importing this file alone does not add them to a map.

