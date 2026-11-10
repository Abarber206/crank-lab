// Buddy holds fire when a wall is between it and the creature, and shoots once it's clear
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,horde,settings,renderer,newZombie,chests,addPiece,pieces,removePiece,get AB2(){return AB}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=true; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.AB2&&T.AB2.active,null,{timeout:60000}); await sleep(1000);
 const r=await pg.evaluate(async()=>{ T.horde.t=9999; T.chests.forEach(c=>c.open=true); const A=T.AB2; T.P.pos.set(12.5,0.1,12.5); A.pos.set(12.5,0.1,10.5); A.vel.set(0,0,0); A.wpn='ar'; A.hp=1e6; A.ammo=999;
   // a wall line at z=10 (cells i=1..3), the creature on the far side, pinned in place
   const ws=[]; for(let i=1;i<=3;i++) ws.push(T.addPiece({type:'wall',axis:'z',i,j:2,l:0,key:'wz'+i+'_2_0',mat:'metal',owner:'me',dir:0,instant:true})); ws.forEach(w=>{ w.hp=w.maxHp=1e7; });
   const z=T.newZombie('husk',12.5,6); z.rise=0; z.hp=z.maxHp=1e6; const pin=setInterval(()=>{ z.pos.set(12.5,z.pos.y,6); z.vel.set(0,0,0); A.pos.x=12.5; A.pos.z=Math.max(10.6,A.pos.z); },16);
   let shots=0; const of=A.h.rig; const iv=setInterval(()=>{ if(A.fireT>0.1&&A.los!==false) shots++; },30);
   await new Promise(r=>setTimeout(r,3000)); const hpWall=z.hp, blockedShots=shots, los1=A.los;
   ws.forEach(w=>T.removePiece(w)); await new Promise(r=>setTimeout(r,3000)); clearInterval(pin); clearInterval(iv);
   return {los1,dmgBehindWall:1e6-hpWall,dmgClear:hpWall-z.hp}; });
 console.log(JSON.stringify(r), r.los1===false&&r.dmgBehindWall===0&&r.dmgClear>0?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
