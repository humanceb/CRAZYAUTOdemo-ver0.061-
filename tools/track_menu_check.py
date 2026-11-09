"""Headless menu, local profile, class choice, and ten-stage drive check."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import threading

root = Path(__file__).resolve().parents[1]
out = root / "qa" / "0.0602"
out.mkdir(parents=True, exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *a, **k: Handler(*a, directory=str(root/"dist"), **k))
threading.Thread(target=server.serve_forever, daemon=True).start()
report = {"errors": [], "tracks": {}}
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True, args=["--enable-unsafe-swiftshader", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_function("window.__crazyauto !== undefined", timeout=60000)
        page.wait_for_timeout(750)
        report["stage_cards"] = page.locator(".stage-button").count()
        report["car_cards"] = page.locator(".car-button").count()
        report["art_loaded"] = page.evaluate("Array.from(document.querySelectorAll('.stage-art,.car-art,.front-panel img')).every(img => img.complete && img.naturalWidth > 0)")
        report["route_summary"] = page.locator("#route-summary").inner_text()
        report["home_visible"] = page.locator("#front-menu").is_visible()
        page.screenshot(path=str(out/"home.png"))
        page.locator('[data-screen="race"]').click()
        report["race_visible"] = page.locator("#garage").is_visible()
        report["sport_count"] = page.locator(".car-button:visible").count()
        page.locator("#route-next").click()
        report["route_next"] = page.evaluate("window.__crazyauto.getState().track") == "pikes"
        page.locator("#route-prev").click()
        page.screenshot(path=str(out/"race.png"))
        page.locator('#class-tabs [data-class="suv"]').click()
        report["suv_selected"] = page.evaluate("window.__crazyauto.getState().selected")
        report["suv_count"] = page.locator(".car-button:visible").count()
        page.screenshot(path=str(out/"suv.png"))
        page.locator("#garage-back").click()
        page.locator('[data-screen="profile"]').click()
        page.locator("#profile-name").fill("Bob Driver")
        page.locator(".menu-primary").click()
        report["profile_saved"] = "Bob Driver" in page.locator("#front-driver").inner_text()
        page.reload(wait_until="domcontentloaded")
        page.wait_for_function("window.__crazyauto !== undefined", timeout=60000)
        report["profile_cookie"] = page.evaluate("document.cookie.includes('crazyauto_driver=Bob%20Driver')")
        report["profile_persisted"] = "Bob Driver" in page.locator("#front-driver").inner_text()
        page.locator('[data-screen="log"]').click()
        report["log_visible"] = page.locator("#menu-panel h2").inner_text() == "DAILY LOG"
        page.locator(".menu-sheet-back").click()
        page.locator('[data-screen="race"]').click()
        for track in ("pine", "pikes", "snow", "quarry", "cedar", "copper", "highland", "motu", "dakar", "rx"):
            page.evaluate("(id) => { window.__crazyauto.selectStage(id); window.__crazyauto.drive() }", track)
            page.keyboard.down("w")
            page.wait_for_function("window.__crazyauto.getState().speed > 0.2", timeout=10000)
            page.wait_for_timeout(250)
            page.keyboard.up("w")
            state = page.evaluate("window.__crazyauto.getState()")
            report["tracks"][track] = {"selected": state["track"], "speed": state["speed"], "ground": state["ground"], "position": state["position"]}
            if track in ("cedar", "copper", "highland", "motu", "dakar", "rx"):
                page.screenshot(path=str(out/f"{track}.png"))
            page.evaluate("window.__crazyauto.returnGarage()")
        page.evaluate("window.__crazyauto.selectStage('dakar');window.__crazyauto.drive()")
        page.keyboard.down("w")
        page.wait_for_function("window.__crazyauto.getState().effectVisible", timeout=25000)
        report["speed_effect"] = page.evaluate("({speedKmh:window.__crazyauto.getState().speed*3.6,visual:window.__crazyauto.getState().speedVisual,fov:window.__crazyauto.getState().cameraFov,visible:window.__crazyauto.getState().effectVisible})")
        page.screenshot(path=str(out/"speed-effect.png"))
        page.keyboard.up("w")
        page.evaluate("window.__crazyauto.returnGarage()")
        browser.close()
finally:
    server.shutdown()
(out/"report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
if report["errors"] or report["stage_cards"] != 10 or report["car_cards"] != 11 or not report["art_loaded"] or not all(report[k] for k in ("home_visible","race_visible","route_next","profile_saved","profile_cookie","profile_persisted","log_visible")) or report["sport_count"] != 10 or report["suv_count"] != 1 or report["suv_selected"] != "trail" or any(v["selected"] != k or v["speed"] <= 0 for k, v in report["tracks"].items()) or not report.get("speed_effect",{}).get("visible") or report["speed_effect"]["fov"] <= 61:
    raise SystemExit(1)
