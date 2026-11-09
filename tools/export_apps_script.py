"""Inline a Vite production bundle into one Apps Script HTML Service page."""
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
dist=root/'dist'
html=(dist/'index.html').read_text(encoding='utf-8')
match=re.search(r'<script[^>]+src="(/assets/[^"]+\.js)"[^>]*></script>',html)
if not match:
    raise SystemExit('No Vite JavaScript bundle found; run npm run build first.')
bundle=(dist/match.group(1).lstrip('/')).read_text(encoding='utf-8')
html=html.replace(match.group(0),'<script type="module">\n'+bundle.replace('</script','<\\/script')+'\n</script>')
for css in re.findall(r'<link[^>]+href="(/assets/[^"]+\.css)"[^>]*>',html):
    css_text=(dist/css.lstrip('/')).read_text(encoding='utf-8')
    html=re.sub(r'<link[^>]+href="'+re.escape(css)+'"[^>]*>', '<style>'+css_text+'</style>',html)
out=root/'apps-script'/'Index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html,encoding='utf-8')
print(f'{out} ({out.stat().st_size} bytes)')
