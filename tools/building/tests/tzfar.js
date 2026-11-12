// zombies left far behind come back: in Zombie horde, a zombie moved 300 m away from you returns to within 70 m
// (42-62 m out, on dry ground) after a few seconds.  node tzfar.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,horde,settings,renderer,newZombie,waterAt,terrainUnder'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(3000);
 const r=await pg.evaluate(async()=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms)); T.horde.phase='wave'; T.horde.toSpawn=0; T.P.hp=1e6; T.P.maxHp=1e6;
   const x=T.P.pos.x+300, z=T.P.pos.z; T.newZombie('husk',x,z); const zz=[...T.horde.zs.values()].pop(); zz.pos.set(x,T.terrainUnder(x,z),z);
   const d0=Math.hypot(zz.pos.x-T.P.pos.x,zz.pos.z-T.P.pos.z); await wait(5000); const d1=Math.hypot(zz.pos.x-T.P.pos.x,zz.pos.z-T.P.pos.z);
   return {d0:Math.round(d0),d1:Math.round(d1),wet:T.waterAt(zz.pos.x,zz.pos.z)>-999,alive:zz.alive}; });
 console.log(JSON.stringify(r)); console.log(r.d0>250&&r.d1<70&&r.d1>30&&!r.wet?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
