import evoX from './assets/dashboards/evox.svg?raw';
import sti from './assets/dashboards/sti.svg?raw';
import evo3 from './assets/dashboards/evo3.svg?raw';
import quattro from './assets/dashboards/quattro.svg?raw';
import rs6 from './assets/dashboards/rs6.svg?raw';
import trail from './assets/dashboards/trail.svg?raw';
import evoXPlate from './assets/dashboards/evox-pic.webp?inline';
import grYarisPlate from './assets/dashboards/gr-yaris.webp?inline';
import deltaPlate from './assets/dashboards/delta.webp?inline';
import p205Plate from './assets/dashboards/p205.webp?inline';
import celicaPlate from './assets/dashboards/celica.webp?inline';
import rs200Plate from './assets/dashboards/rs200.webp?inline';

type DashArt={svg?:string;pic?:string;label:string;state:string;accent:string;max:number};
export const dashboardArt:Record<string,DashArt>= {
  evoX:{pic:evoXPlate,label:'EVO X · RALLY',state:'S-AWC',accent:'#f0b74b',max:300},
  sti:{svg:sti,label:'STI · DCCD',state:'DCCD',accent:'#c4b077',max:240},
  evo3:{svg:evo3,label:'EVO III · GROUP A',state:'ACTIVE AWD',accent:'#e47737',max:200},
  quattro:{svg:quattro,label:'QUATTRO · GROUP B',state:'4WD',accent:'#d92e30',max:280},
  rs6:{svg:rs6,label:'RS 6 · PERFORMANCE',state:'QUATTRO',accent:'#65d5d8',max:320},
  grYaris:{pic:grYarisPlate,label:'GR YARIS · GR-FOUR',state:'AWD',accent:'#4fe3e9',max:260},
  delta:{pic:deltaPlate,label:'DELTA HF · INTEGRALE',state:'4WD',accent:'#e2b65f',max:240},
  p205:{pic:p205Plate,label:'205 T16 · GROUP B',state:'MID-ENGINE',accent:'#e9d8b2',max:260},
  celica:{pic:celicaPlate,label:'CELICA · GT-FOUR',state:'AWD',accent:'#9dd3e4',max:260},
  rs200:{pic:rs200Plate,label:'RS200 · GROUP B',state:'4WD',accent:'#e6c581',max:260},
  trail:{svg:trail,label:'CK TRAIL · 4×4',state:'RALLY SUV',accent:'#d38d4b',max:220},
};

export function mountDashboard(id:string){
  const item=dashboardArt[id]??dashboardArt.evoX;
  const host=document.getElementById('dash-art');
  if(host)host.innerHTML=item.pic
    ?'<img class="dash-plate" alt="" src="'+item.pic+'"><div class="dash-live"><b id="dash-speed">0</b><small>KM/H</small></div><div class="dash-pedal"><span id="dash-pedal-fill"></span></div>'
    :item.svg||'';
  const card=document.getElementById('dashboard');
  card?.style.setProperty('--dash-accent',item.accent);
  const label=document.getElementById('dash-model');
  if(label)label.textContent=item.label;
  const state=document.getElementById('dash-state');
  if(state)state.textContent=item.state;
}

export function updateDashboard(speed:number,id:string,throttle=0,brake=0){
  const item=dashboardArt[id]??dashboardArt.evoX;
  const host=document.getElementById('dash-art');
  const value=host?.querySelector<HTMLElement>('#dash-speed');
  const needle=host?.querySelector<SVGPathElement>('.needle');
  if(value)value.textContent=String(Math.round(speed));
  const pedal=host?.querySelector<HTMLElement>('#dash-pedal-fill');
  if(pedal){pedal.style.width=`${Math.round((brake>0?brake:throttle)*100)}%`;pedal.style.background=brake>0?'#e65c4d':item.accent}
  if(needle){const fraction=Math.max(0,Math.min(1,speed/item.max));needle.style.transform=`rotate(${-90+fraction*270}deg)`}
}
