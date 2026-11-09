import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const data=new Map();let counter=0;
const context={
  CacheService:{getScriptCache:()=>({get:key=>data.get(key)||null,put:(key,value)=>data.set(key,value)})},
  LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock:()=>{}})},
  Utilities:{getUuid:()=>`${String(++counter).padStart(6,'0')}abcdef-1234-4567-8901-abcdef123456`},
  HtmlService:{createHtmlOutputFromFile:()=>({setTitle:()=>({})})},Date,Math,JSON,String,Number,Error,isFinite,
};
vm.createContext(context);vm.runInContext(fs.readFileSync(new URL('../apps-script/Code.gs',import.meta.url),'utf8'),context);
const host=context.roomCreate('Driver <script>','evoX');
assert.match(host.room.code,/^[A-Z0-9]{6}$/);
assert.equal(host.room.players.length,1);
assert(!JSON.stringify(host.room).includes(host.token),'public room leaked a player token');
const guest=context.roomJoin(host.room.code,'Guest','sti');
assert.equal(guest.room.players.length,2);
const synced=context.roomSync(host.room.code,guest.token,{x:120,y:2,z:44,yaw:.5,speed:18});
assert.equal(synced.players.find(p=>p.id===guest.room.id).x,120);
assert.equal(synced.players.find(p=>p.id===guest.room.id).speed,18);
assert.throws(()=>context.roomSync(host.room.code,'wrong',{}));
context.roomLeave(host.room.code,guest.token);
assert.equal(context.roomSync(host.room.code,host.token,{}).players.length,1);
console.log(JSON.stringify({room:host.room.code,playersAfterLeave:1,tokenPrivate:true}));
