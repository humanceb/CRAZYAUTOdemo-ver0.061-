"""Draw lightweight, original route maps and car glyphs for the garage UI.

The maps are sampled from the same radial routes used by the game. Re-run after
editing route formulas in src/main.ts; keep the two definitions in sync.
"""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "assets" / "menu"
OUT.mkdir(parents=True, exist_ok=True)

ROUTES = {
    "pine": (lambda t: 91 + 9*math.sin(3*t+.4) + 5*math.sin(7*t-.2), "#182f2a", "#4b7459", "#f1c56a"),
    "snow": (lambda t: 78 + 12*math.sin(2*t+.65) + 5*math.sin(7*t-.4), "#253b45", "#9ab8bf", "#f4f4dd"),
    "quarry": (lambda t: 90 + 15*math.sin(3*t+.8) + 7*math.sin(6*t-.5), "#3b3029", "#b16a48", "#f7ca8a"),
    "cedar": (lambda t: 166 + 19*math.sin(3*t+.4) + 12*math.sin(8*t-.5), "#152e32", "#4f8578", "#cce7ad"),
    "copper": (lambda t: 180 + 21*math.sin(2*t+.2) + 14*math.sin(9*t+.7), "#3b2925", "#bd7950", "#f5c876"),
    "highland": (lambda t: 173 + 24*math.sin(4*t-.3) + 8*math.sin(11*t+.6), "#262e39", "#74869b", "#dbe4ca"),
    "motu": (lambda t: 178 + 27*math.sin(3*t+.5) + 12*math.sin(10*t-.3), "#102e26", "#488367", "#d4e5b1"),
    "dakar": (lambda t: 205 + 23*math.sin(2*t+.6) + 10*math.sin(9*t-.5), "#4b2f23", "#d5a26a", "#ffdf9d"),
    "rx": (lambda t: 133 + 14*math.sin(3*t+.4) + 7*math.sin(7*t-.8), "#252c31", "#757f78", "#f6b05f"),
}

def route_points(radius, end=2*math.pi):
    return [(radius(t)*math.cos(t), radius(t)*math.sin(t)) for t in [end*i/180 for i in range(181)]]

def route_svg(name, points, bg, hill, route):
    xs, ys = zip(*points)
    span = max(max(xs)-min(xs), max(ys)-min(ys), 1)
    scale = 108/span
    ox = 248 - (max(xs)+min(xs))*scale/2
    oy = 74 - (max(ys)+min(ys))*scale/2
    path = " ".join(("M" if i == 0 else "L") + f"{ox+x*scale:.1f},{oy+y*scale:.1f}" for i,(x,y) in enumerate(points))
    x0,y0=points[0]
    start_x,start_y=ox+x0*scale,oy+y0*scale
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 150">
<defs><linearGradient id="g" x2=".8" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{hill}"/></linearGradient>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".6" fill="#ffffff" opacity=".18"/></pattern></defs>
<rect width="320" height="150" fill="url(#g)"/><path d="M0 117 34 89 62 108 105 62 139 95 177 51 214 94 253 58 320 92V150H0Z" fill="{hill}" opacity=".45"/>
<path d="M0 138 42 120 83 134 132 103 166 124 211 103 257 119 320 94V150H0Z" fill="#071712" opacity=".3"/>
<rect width="320" height="150" fill="url(#dots)"/>
<g fill="none" stroke="#d3dfcb" stroke-opacity=".13"><path d="M-20 33q75-27 120 11t120-9 120 3"/><path d="M-20 49q75-27 120 11t120-9 120 3"/><path d="M-20 65q75-27 120 11t120-9 120 3"/><path d="M-20 81q75-27 120 11t120-9 120 3"/></g>
<path d="{path}" fill="none" stroke="#071714" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity=".65"/>
<path d="{path}" fill="none" stroke="{route}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="{start_x:.1f}" cy="{start_y:.1f}" r="7" fill="{route}" stroke="#10201d" stroke-width="2"/>
<path d="M14 16h39M14 20h25M14 24h32" stroke="{route}" stroke-opacity=".9" stroke-width="2"/>
</svg>"""
    (OUT/f"{name}.svg").write_text(svg,encoding="utf-8")

for name, (radius,bg,hill,route) in ROUTES.items():
    route_svg(name, route_points(radius,5.55 if name=="motu" else 2*math.pi),bg,hill,route)

pikes=json.loads((ROOT/"src"/"pikes_peak.json").read_text(encoding="utf-8"))
pikes_points=[(point[0],point[1]) for point in pikes["route"]]
route_svg("pikes",pikes_points,"#223547","#7995a4","#f6d69d")

# Original small profile art. The icon accent is tied to each car's garage tile.
CARS = {
    "evoX":("#e04c37",42,85,65,0), "sti":("#3581a3",39,80,64,0),
    "evo3":("#c7d6dc",46,81,68,1), "quattro":("#e9d9a7",47,77,70,2),
    "rs6":("#a5b8bd",36,89,59,0), "grYaris":("#e6e7dd",46,74,71,0),
    "delta":("#d25443",45,76,69,1), "p205":("#ddd2bb",49,73,72,2),
    "celica":("#698caa",41,80,57,1), "rs200":("#eee9d5",47,73,65,2),
    "trail":("#d38d4b",34,83,66,0),
}
for name,(color,roof_y,roof_end,hood_y,wing) in CARS.items():
    spoiler = f'<path d="M10 49h18v4H9z" fill="{color}"/>' if wing else ''
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 64">
<path d="M3 56 8 47 24 44 38 {roof_y} 64 {roof_y-2} {roof_end} 47 102 {hood_y} 115 49 119 56V59H3Z" fill="{color}" stroke="#f1f2dc" stroke-width="1.5"/>
<path d="M37 45 44 {roof_y+3} 62 {roof_y+1} 68 46Z" fill="#183037" opacity=".82"/>
<path d="M70 46 80 47 90 51 70 50Z" fill="#183037" opacity=".65"/>
{spoiler}<path d="M12 54h12M106 54h9" stroke="#f6dfaa" stroke-width="2"/>
<circle cx="29" cy="56" r="7" fill="#13201f" stroke="#e7dcc4" stroke-width="2"/><circle cx="94" cy="56" r="7" fill="#13201f" stroke="#e7dcc4" stroke-width="2"/>
</svg>"""
    (OUT/f"car-{name}.svg").write_text(svg,encoding="utf-8")

hero="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560">
<defs><linearGradient id="sky" x2=".2" y2="1"><stop stop-color="#24454e"/><stop offset="1" stop-color="#9bb0a0"/></linearGradient>
<linearGradient id="road" x2="0" y2="1"><stop stop-color="#464d47"/><stop offset="1" stop-color="#121d1b"/></linearGradient></defs>
<rect width="1000" height="560" fill="url(#sky)"/>
<circle cx="762" cy="111" r="62" fill="#f2c878" opacity=".85"/>
<path d="M0 286 94 176 185 255 314 120 409 238 530 162 682 296 796 154 1000 274V560H0Z" fill="#607d78"/>
<path d="M0 331 134 218 255 320 343 220 510 352 649 260 764 352 901 225 1000 295V560H0Z" fill="#355d58"/>
<path d="M0 427 139 325 203 382 322 298 443 399 552 310 675 397 833 285 1000 377V560H0Z" fill="#1c3f38"/>
<path d="M410 560 460 418 506 377 485 349 551 313 523 294 593 277 1000 560Z" fill="url(#road)"/>
<path d="M507 560 514 435 526 377 512 349 558 315 531 296 600 277" fill="none" stroke="#e9c47f" stroke-width="7" stroke-dasharray="25 24" opacity=".8"/>
<path d="M0 490 146 388 227 430 312 358 386 418 449 368" fill="none" stroke="#c9e2cb" stroke-opacity=".3" stroke-width="5"/>
<g fill="#12362c"><path d="M82 421 103 301 124 421Z"/><path d="M128 407 153 266 178 407Z"/><path d="M217 391 244 244 271 391Z"/><path d="M305 420 333 275 361 420Z"/><path d="M764 442 792 274 820 442Z"/><path d="M865 426 894 262 923 426Z"/></g>
<path d="M22 24h204M22 29h134M22 34h178" stroke="#efc67c" stroke-width="3"/>
</svg>"""
(OUT/"hero.svg").write_text(hero,encoding="utf-8")
ICONS={
    "garage":'<path d="M7 35 14 19h36l8 16v15H7Z M15 35h35 M20 45h5 M42 45h5" fill="none" stroke="#f1d18d" stroke-width="4" stroke-linejoin="round"/><circle cx="20" cy="49" r="5" fill="#f1d18d"/><circle cx="47" cy="49" r="5" fill="#f1d18d"/>',
    "race":'<path d="M15 54V12l14 7 16-7v27l-16 8-14-7" fill="none" stroke="#f1d18d" stroke-width="4"/><circle cx="45" cy="14" r="5" fill="#f1d18d"/>',
    "log":'<path d="M14 10h34v45H14Z M23 22h17 M23 31h17 M23 40h11" fill="none" stroke="#f1d18d" stroke-width="4" stroke-linejoin="round"/>',
    "driver":'<circle cx="32" cy="21" r="10" fill="none" stroke="#f1d18d" stroke-width="4"/><path d="M12 53q2-18 20-18t20 18Z" fill="none" stroke="#f1d18d" stroke-width="4"/>',
}
for name, shape in ICONS.items():
    (OUT/f"icon-{name}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{shape}</svg>',encoding="utf-8")
print(f"Created {len(ROUTES)+1} route maps, {len(CARS)} car glyphs, and menu plates in {OUT}")
