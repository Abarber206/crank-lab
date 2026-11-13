// sound upgrades: each rarity of a gun is its own sound; far shots arrive late; near misses whiz; the falls roar near them
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,WEAPONS,GUN_SND,gunTakes,gunSndKey,sfx,sfxAt,whizBy,audioInit,settings,SPAWN,WGEN,OCEAN,terrainH,camera,AUDIO,AC:()=>AC,amb:()=>amb'),{fast:true,norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); T.audioInit(); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const out={};
   const keys=['ar_c','ar','ar_r','ar_e','ar_l'].filter(k=>T.WEAPONS[k]).map(k=>T.gunSndKey(T.WEAPONS[k])); out.keys=keys;
   for(const k of keys){ T.sfx(k); } await new Promise(r=>setTimeout(r,300));
   out.takes=keys.map(k=>{ const t=T.gunTakes[k]; if(!t||!t.length) return null; const d=t[0].getChannelData(0); let e=0, lo=0; for(let i=0;i<d.length;i++) e+=d[i]*d[i]; return [+t[0].duration.toFixed(2),+(Math.sqrt(e/d.length)).toFixed(3)]; });
   // far shot: arrives late
   let played=0; const s0=T.sfx; window.__n=0; const far=T.camera.position.clone().add(new THREE.Vector3(200,0,0)); const t0=performance.now(); T.sfxAt(keys[1],far); out.lateNow=window.__late; 
   // whiz
   const o=T.camera.position.clone().add(new THREE.Vector3(-60,0,1)); T.whizBy(o,new THREE.Vector3(1,0,0),120); out.whizOk=true;
   // stand by the falls
   const S=T.WGEN.sea(), a=Math.atan2(S.nz,S.nx), e=T.WGEN.edgeR(Math.cos(a)*800,Math.sin(a)*800)-30, x=T.SPAWN[0]+Math.cos(a)*e, z=T.SPAWN[2]+Math.sin(a)*e; T.P.pos.set(x,T.terrainH(x,z)+3,z);
   await new Promise(r=>setTimeout(r,2500)); const A=T.amb(); out.fall=A&&A.fall?+A.fall.g.gain.value.toFixed(3):null; out.fallD=A&&+A.fallD.toFixed(0); out.cliff=A&&A.cliff?+A.cliff.g.gain.value.toFixed(3):null;
   T.P.pos.set(T.SPAWN[0],T.terrainH(T.SPAWN[0],T.SPAWN[2])+1,T.SPAWN[2]); await new Promise(r=>setTimeout(r,2500)); out.fallMid=A&&A.fall?+A.fall.g.gain.value.toFixed(3):null; out.cliffMid=A&&A.cliff?+A.cliff.g.gain.value.toFixed(3):null;
   out.ambBus=!!T.AUDIO.amb; return out; });
 console.log(JSON.stringify(r));
 const ok=r.keys.length===5&&new Set(r.keys).size===5&&r.takes.every(x=>x)&&r.fall>0.1&&r.fallMid<0.01&&r.ambBus;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();
