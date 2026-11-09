"""Headless UI adapter check with a simulated google.script.run transport."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
server=ThreadingHTTPServer(('127.0.0.1',0),lambda *a,**k:Handler(*a,directory=str(root/'dist'),**k))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader','--no-sandbox'])
        page=browser.new_page(viewport={'width':1280,'height':720})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.add_init_script("""
          const me={id:'me',name:'Driver',car:'evoX',x:93.5,y:.07,z:0,yaw:0,speed:0,last:Date.now()};
          const other={id:'friend',name:'Friend',car:'sti',x:96,y:.07,z:2,yaw:0,speed:2,last:Date.now()};
          const room={code:'ABC123',id:'me',players:[me,other]};
          const run={withSuccessHandler(fn){this.ok=fn;return this},withFailureHandler(fn){this.fail=fn;return this},
            roomCreate(){queueMicrotask(()=>this.ok({token:'secret',room}))},
            roomSync(_code,_token,state){Object.assign(me,state);queueMicrotask(()=>this.ok(room))},
            roomLeave(){queueMicrotask(()=>this.ok(true))}};
          window.google={script:{run}};
        """)
        page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='domcontentloaded',timeout=60000)
        page.wait_for_function('window.__crazyauto !== undefined')
        page.locator('#driver-name').fill('Driver')
        page.locator('#room-create').click()
        page.wait_for_function("document.querySelector('#room-status').textContent.includes('ABC123')")
        page.locator('#play').click()
        page.wait_for_timeout(400)
        assert page.locator('#room-hud').is_visible()
        assert 'Friend' in page.locator('#room-hud').inner_text()
        assert not errors,errors
        print({'room_status':page.locator('#room-status').inner_text(),'hud':page.locator('#room-hud').inner_text(),'errors':errors})
        browser.close()
finally:server.shutdown()
