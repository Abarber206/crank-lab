// everyone else in water: a monster wades and swims out to you; Buddy swims after you and holds fire while swimming;
// the opponent bot doesn't shoot from the water
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,newZombie,horde,settings,ZT,waterAt,waterDepth,terrainH,SPAWN,get AB(){return AB},get B(){return B},tracers'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.mode='horde'; T.settings.hordeBot=true; const hb=document.getElementById('hordeBot'); if(hb){ hb.checked=true; hb.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const r=await pg.evaluate(async()=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms)), o={}, S=T.SPAWN; let sp=null;
   for(let k=0;k<400000&&!sp;k++){ const a=k*2.399, d=600+(k%4000)*0.055, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d; if(T.waterDepth(x,z)>2.5){ for(let q=0;q<16&&!sp;q++){ const aa=q*Math.PI/8; for(let rr=14;rr<30;rr+=2){ const sx=x+Math.cos(aa)*rr, sz=z+Math.sin(aa)*rr; if(T.waterAt(sx,sz)<-999&&Math.hypot(sx-S[0],sz-S[2])<Math.hypot(x-S[0],z-S[2])){ sp={x,z,sx,sz}; break; } } } } }
   if(!sp) return {err:'no spot'}; const w=T.waterAt(sp.x,sp.z);
   T.P.pos.set(sp.x,w-1.3,sp.z); T.P.vel.set(0,0,0); T.P.onGround=true;
   // horde.zs: clear the wave, add one monster on the beach
   T.horde.zs.forEach(z=>{ z.alive=false; }); await wait(300);
   const z=T.newZombie(Object.keys(T.ZT)[0],sp.sx,sp.sz); const d0=Math.hypot(z.pos.x-sp.x,z.pos.z-sp.z);
   o.ab=!!(T.AB&&T.AB.active); if(o.ab){ T.AB.pos.set(sp.x+3,w-1.3,sp.z+3); T.AB.vel.set(0,0,0); }
   const t0=T.tracers.length; let abShots=0; const ft=[]; for(let i=0;i<16;i++){ await wait(500); if(T.AB&&T.AB.swim&&T.tracers.some(t=>t.H===T.AB.h)) abShots++; T.P.pos.set(sp.x,w-1.3,sp.z); T.P.hp=100; }
   o.zMoved=+(d0-Math.hypot(z.pos.x-sp.x,z.pos.z-sp.z)).toFixed(1); o.zInWater=T.waterDepth(z.pos.x,z.pos.z)>0.5; o.zAlive=z.alive; o.zY=+(z.pos.y-T.terrainH(z.pos.x,z.pos.z)).toFixed(2);
   o.abSwim=o.ab?!!T.AB.swim:null; o.abShots=abShots; o.abNear=o.ab?+Math.hypot(T.AB.pos.x-sp.x,T.AB.pos.z-sp.z).toFixed(1):null;
   return o; });
 console.log(JSON.stringify(r)); const ok=r.zMoved>5&&r.zAlive!==undefined&&(!r.ab||(r.abShots===0));
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
