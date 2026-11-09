"""Serve a built CrazyAuto web game on a free local port and open it."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

root = Path(__file__).resolve().parents[1]
folder = root / 'dist'
if not (folder / 'index.html').exists():
    raise SystemExit('Build first: npm run build')
handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(folder), **kwargs)
server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
url = f'http://127.0.0.1:{server.server_port}/'
print('CrazyAuto is running at', url, flush=True)
webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
