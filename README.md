# CrazyAuto 0.061 — Gripline

GitHub-ready source bundle for CrazyAuto (by CrazyKids). This folder contains the playable game's rebuildable TypeScript/Three.js source and the maintained CrazyKids car-engine skill.

## Contents

- `crazyauto-game/` — game source, original assets, Apps Script export source, desktop packaging files, release notes, and build scripts.
- `crazykids-car-engine-skill/` — the reusable Codex skill and its research, asset guidance, and workflow references.

## Build the web game

```powershell
cd crazyauto-game
npm install
npm run build
python tools/export_apps_script.py
```

The web build is written to `crazyauto-game/dist/`. Apps Script single-file HTML is written to `crazyauto-game/apps-script/Index.html`.

## License

CrazyKids game code, original art, and skill text are all rights reserved. Third-party dependencies and referenced assets remain under their own licenses; see the included credits and notices before redistribution.

This is a local GitHub preparation folder. It has not been pushed to a remote repository.
