import assert from 'node:assert/strict';
import {newVehicleState,stepVehicle} from '../src/physics.ts';
import evoX from '../src/carSpecs/evo_x.json' with {type:'json'};

const dt=1/120;
const world={surfaceHeightAt:()=>0,roadDistance:()=>0,surfaceAt:()=>({name:'tarmac',grip:.96,rolling:1,roughness:.01}),resolveVehicle:(x,z)=>({x,z,hit:false,normalX:0,normalZ:0})};
const input=(throttle,brake)=>({throttle,brake,left:false,right:false,handbrake:false});
const s=newVehicleState(0,0);s.y=.045;
let to100=0,peakLaunchSlip=0;
for(let i=0;i<1800;i++){
  stepVehicle(s,input(true,false),world,evoX,dt);
  peakLaunchSlip=Math.max(peakLaunchSlip,...s.wheelSlipRatio.map(Math.abs));
  if(s.vLong*3.6>=100){to100=i*dt;break}
}
assert(to100>0&&to100<15,'car should accelerate to 100 km/h in a playable time');
const brakeStartZ=s.z;
let brakeTime=0,minWheelRatio=0;
for(let i=0;i<1200;i++){
  stepVehicle(s,input(false,true),world,evoX,dt);
  if(s.vLong>5)minWheelRatio=Math.min(minWheelRatio,...s.wheelSlipRatio);
  if(Math.abs(s.vLong)<.25){brakeTime=i*dt;break}
}
const brakeDistance=s.z-brakeStartZ;
assert(brakeTime>0&&brakeTime<9,'brake should bring car to rest');
assert(brakeDistance>20&&brakeDistance<130,'stopping distance should be bounded');
assert(s.vLong>=-.25,'braking must not snap into reverse before a hold');
for(let i=0;i<90;i++)stepVehicle(s,input(false,true),world,evoX,dt);
assert(s.vLong<-.25,'holding S at rest should allow reverse');
console.log(JSON.stringify({zeroTo100S:to100,brakeTimeS:brakeTime,brakeDistanceM:brakeDistance,minWheelSlipRatio:minWheelRatio,peakLaunchSlipRatio:peakLaunchSlip,reverseAfterHoldMps:s.vLong}));
