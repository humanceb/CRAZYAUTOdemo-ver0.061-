"""Browser smoke check for garage selection, driving input and pause flow."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
out=root/'qa';out.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
server=ThreadingHTTPServer(('127.0.0.1',0),lambda *a,**k:Handler(*a,directory=str(root/'dist'),**k))
threading.Thread(target=server.serve_forever,daemon=True).start()
result={'cars':{},'errors':[]}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader','--no-sandbox'])
        page=browser.new_page(viewport={'width':1280,'height':720})
        page.on('pageerror',lambda e:result['errors'].append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='domcontentloaded',timeout=60000)
        page.wait_for_function('window.__crazyauto !== undefined')
        # Garage UI is fixed above the WebGL canvas; hide it for true model-only
        # art reviews so labels never masquerade as part of the car silhouette.
        review_css=page.add_style_tag(content='#garage,#hud,#pause,#grain{visibility:hidden!important}')
        for car in ('evoX','sti','evo3','quattro','rs6'):
            page.evaluate(f'window.__crazyauto.select("{car}")')
            page.evaluate('window.__crazyauto.setGarageView(-0.48,3.8,1.15,.7)')
            page.wait_for_timeout(350)
            page.locator('canvas').screenshot(path=str(out/f'{car}-front.png'))
            page.evaluate('window.__crazyauto.setGarageView(0.0,4.4,1.15,.7)')
            page.wait_for_timeout(500)
            page.locator('canvas').screenshot(path=str(out/f'{car}-front-three-quarter.png'))
            page.evaluate('window.__crazyauto.setGarageView(3.42,4.0,2.0,.77)')
            page.wait_for_timeout(500)
            page.locator('canvas').screenshot(path=str(out/f'{car}-rear-three-quarter.png'))
            result['cars'][car]=page.evaluate('window.__crazyauto.getState().selected')==car
        result['tracks']={}
        for stage in ('pine','pikes','snow','quarry'):
            page.evaluate(f'window.__crazyauto.selectStage("{stage}");window.__crazyauto.drive()')
            page.wait_for_timeout(250)
            page.keyboard.down('w');page.wait_for_timeout(800)
            state=page.evaluate('window.__crazyauto.getState()')
            page.keyboard.up('w')
            page.locator('canvas').screenshot(path=str(out/f'world-{stage}.png'))
            result['tracks'][stage]={'selected':state['track'],'speed':state['speed'],'position':state['position']}
            page.evaluate('window.__crazyauto.returnGarage()')
        review_css.evaluate('(el)=>el.remove()')
        page.evaluate('window.__crazyauto.setGarageView(0.0,4.4)')
        page.locator('#play').click()
        page.keyboard.down('w');page.wait_for_timeout(1150)
        result['drive']=page.evaluate('window.__crazyauto.getState()')
        page.screenshot(path=str(out/'drive-world.png'))
        page.keyboard.up('w');page.keyboard.press('Escape')
        result['pause']=page.evaluate('window.__crazyauto.getState().mode')
        page.locator('#restart').click()
        page.keyboard.down('w');page.keyboard.down('d');page.wait_for_timeout(1650)
        result['steer_right']=page.evaluate('window.__crazyauto.getState()')
        page.keyboard.up('w');page.keyboard.up('d')
        page.locator('#restart').click() if page.locator('#restart').is_visible() else page.keyboard.press('Escape')
        if page.locator('#restart').is_visible():page.locator('#restart').click()
        page.keyboard.down('w');page.keyboard.down('a');page.wait_for_timeout(1650)
        result['steer_left']=page.evaluate('window.__crazyauto.getState()')
        page.keyboard.up('w');page.keyboard.up('a')
        browser.close()
finally:
    server.shutdown()
(out/'smoke.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
start_yaw=result.get('drive',{}).get('yaw',0)
if (result['errors'] or not all(result['cars'].values()) or result.get('drive',{}).get('speed',0)<=0
    or any(v.get('selected')!=k or v.get('speed',0)<=0 for k,v in result.get('tracks',{}).items())
    or result.get('pause')!='pause' or result.get('steer_right',{}).get('yaw',start_yaw)>=start_yaw-.03
    or result.get('steer_left',{}).get('yaw',start_yaw)<=start_yaw+.03):raise SystemExit(1)

