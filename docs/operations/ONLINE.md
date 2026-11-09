# Online deployment path

The current playable site is a static Three.js build. Client-side graphics, physics and keyboard input run in the visitor's browser. A future standalone desktop release can reuse the model data but needs its own renderer and input layer.

## Google Apps Script option

Apps Script [web apps](https://developers.google.com/apps-script/guides/web) serve an `HtmlOutput` from `doGet()`. HTML Service runs in an [iframe sandbox](https://developers.google.com/apps-script/guides/html/restrictions) and requires HTTPS for active external content. The generated single-file `Index.html` keeps the game code inside the HTML response. The wrapper is in `apps-script/Code.gs` and the exporter is `tools/export_apps_script.py`.

The prepared Apps Script edition adds up to four-player ephemeral ghost rooms using `CacheService` and asynchronous [`google.script.run`](https://developers.google.com/apps-script/guides/html/communication) calls every 1.2 seconds. The rendering and four-wheel driving model stay client-side. Apps Script has [execution quotas](https://developers.google.com/apps-script/guides/services/quotas), so this is a small shared stage rather than low-latency, server-authoritative racing. Browser localStorage remains the offline progression store. No public multiplayer deployment is live until Google sign-in and deployment complete; see `apps-script/README.md`.

## Current private web edition

The production static site is hosted separately so the game assets load as ordinary HTTPS files. It is owner-private while we develop. Sharing/public access should only be changed when intended.
