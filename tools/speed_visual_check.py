"""Headless speed-visual probe; keeps the game window invisible."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
import threading
import json

root=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
server=ThreadingHTTPServer(("127.0.0.1",0),lambda *a,**k:Handler(*a,directory=str(root/"dist"),**k))
threading.Thread(target=server.serve_forever,daemon=True).start()
samples=[]
try:
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",headless=True,args=["--enable-unsafe-swiftshader","--no-sandbox"])
        page=browser.new_page(viewport={"width":1440,"height":900})
        page.goto(f"http://127.0.0.1:{server.server_port}/",wait_until="domcontentloaded")
        page.wait_for_function("window.__crazyauto !== undefined")
        page.evaluate("window.__crazyauto.selectStage('dakar');window.__crazyauto.drive()")
        page.keyboard.down("w")
        for second in range(1,17):
            page.wait_for_timeout(1000)
            state=page.evaluate("window.__crazyauto.getState()")
            samples.append({"second":second,"kmh":round(state["speed"]*3.6,1),"visual":round(state["speedVisual"],3),"fov":round(state["cameraFov"],2),"effect":state["effectVisible"],"surface":page.locator("#surface").inner_text()})
            if second in (6,12,16):page.screenshot(path=str(root/"qa"/"0.0602"/f"speed-{second}s.png"))
        page.keyboard.up("w")
        browser.close()
finally:
    server.shutdown()
print(json.dumps(samples,indent=2))
