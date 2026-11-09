import assert from 'node:assert/strict';
import {newVehicleState,stepVehicle} from '../src/physics.ts';
import evoX from '../src/carSpecs/evo_x.json' with {type:'json'};

const dt=1/120;
const clearWorld={surfaceHeightAt:()=>0,roadDistance:()=>0,surfaceAt:()=>({name:'tarmac',grip:.96,rolling:1,roughness:.01}),resolveVehicle:(x,z)=>({x,z,hit:false,normalX:0,normalZ:0})};
function run(input,world=clearWorld,steps=240){
  const state=newVehicleState(0,0);state.y=.045;
  for(let i=0;i<steps;i++)stepVehicle(state,input,world,evoX,dt);
  return state;
}
const right=run({throttle:true,brake:false,left:false,right:true,handbrake:false});
const left=run({throttle:true,brake:false,left:true,right:false,handbrake:false});
assert(right.yaw<-.1&&right.x<-.5,'D must turn screen-right (-X)');
assert(left.yaw>.1&&left.x>.5,'A must turn screen-left (+X)');
const hill={...clearWorld,surfaceHeightAt:(_x,z)=>Math.max(0,(z-2)*.12)};
const climber=run({throttle:true,brake:false,left:false,right:false,handbrake:false},hill,420);
assert(climber.y>.3,'chassis must climb the hill');
assert(climber.y>=hill.surfaceHeightAt(climber.x,climber.z)+.044,'chassis must stay above terrain');
const wall={...clearWorld,resolveVehicle:(x,z)=>z>7?{x,z:7,hit:true,normalX:0,normalZ:-1}:{x,z,hit:false,normalX:0,normalZ:0}};
const stopped=run({throttle:true,brake:false,left:false,right:false,handbrake:false},wall,420);
assert(stopped.z<=7.001,'object contact must block movement');
const highSpeed=newVehicleState(0,0);highSpeed.y=.045;
const throttle={throttle:true,brake:false,left:false,right:false,handbrake:false};
let peakBodySlip=0;
for(let i=0;i<480;i++)stepVehicle(highSpeed,throttle,clearWorld,evoX,dt);
for(let i=0;i<240;i++){
  stepVehicle(highSpeed,{...throttle,right:true},clearWorld,evoX,dt);
  peakBodySlip=Math.max(peakBodySlip,Math.abs(Math.atan2(highSpeed.vLat,Math.max(Math.abs(highSpeed.vLong),1.5))));
}
const yawBeforeCountersteer=highSpeed.yaw;
for(let i=0;i<240;i++){
  stepVehicle(highSpeed,{...throttle,left:true},clearWorld,evoX,dt);
  peakBodySlip=Math.max(peakBodySlip,Math.abs(Math.atan2(highSpeed.vLat,Math.max(Math.abs(highSpeed.vLong),1.5))));
}
assert(peakBodySlip<.28,'Normal handling should prevent an unrecoverable high-speed 75-degree spin');
assert(Math.abs(highSpeed.yaw)<Math.abs(yawBeforeCountersteer),'countersteer should turn the car back toward the travel direction');
assert(Math.abs(highSpeed.roll)>.04,'high-speed cornering should still produce visible force-driven body roll');
// Rally recovery profile: initiate a loose-surface slide with SPACE, then
// countersteer for 0.75 s while SPACE remains down. A catch must reduce slip
// without throwing the car straight into a large slide the other way.
const gravel={...clearWorld,surfaceAt:()=>({name:'gravel',grip:.55,rolling:1,roughness:.08})};
const rally=newVehicleState(0,0);rally.y=.045;
for(let i=0;i<480;i++)stepVehicle(rally,throttle,gravel,evoX,dt);
for(let i=0;i<120;i++)stepVehicle(rally,{throttle:false,brake:false,left:false,right:true,handbrake:true},gravel,evoX,dt);
const slipDeg=state=>Math.atan2(state.vLat,Math.max(Math.abs(state.vLong),1.5))*180/Math.PI;
const entrySlip=Math.abs(slipDeg(rally));
for(let i=0;i<90;i++)stepVehicle(rally,{throttle:true,brake:false,left:true,right:false,handbrake:true},gravel,evoX,dt);
const caughtSlip=slipDeg(rally);
assert(entrySlip>2,'handbrake entry should create a visible slide on gravel');
assert(Math.abs(caughtSlip)<entrySlip*.5,'opposite lock should substantially catch the initiated slide');
assert(Math.abs(caughtSlip)<3,'countersteer catch should avoid a large snap into the other direction');
const kick=newVehicleState(0,0);kick.y=.045;
for(let i=0;i<480;i++)stepVehicle(kick,throttle,clearWorld,evoX,dt);
for(let i=0;i<24;i++)stepVehicle(kick,{...throttle,clutch:true},clearWorld,evoX,dt);
const rearOmegaBefore=Math.max(kick.wheelOmega[2],kick.wheelOmega[3]);
for(let i=0;i<15;i++)stepVehicle(kick,{...throttle,right:true,clutch:false},clearWorld,evoX,dt);
assert(kick.clutchKick>0,'quick clutch release under throttle should create a brief drive-torque pulse');
assert(Math.max(kick.wheelOmega[2],kick.wheelOmega[3])>rearOmegaBefore*1.3,'clutch kick should increase driven-wheel speed');
console.log(JSON.stringify({steerRightYaw:right.yaw,steerLeftYaw:left.yaw,hillHeight:climber.y,hillGround:hill.surfaceHeightAt(climber.x,climber.z),wallZ:stopped.z,
  highSpeedKmh:Math.hypot(highSpeed.vLong,highSpeed.vLat)*3.6,peakBodySlipDeg:peakBodySlip*180/Math.PI,
  yawBeforeCountersteerDeg:yawBeforeCountersteer*180/Math.PI,yawAfterCountersteerDeg:highSpeed.yaw*180/Math.PI,rollDeg:highSpeed.roll*180/Math.PI,
  rallyEntrySlipDeg:entrySlip,rallyCaughtSlipDeg:caughtSlip,clutchKickRearOmega:Math.max(kick.wheelOmega[2],kick.wheelOmega[3])}));
