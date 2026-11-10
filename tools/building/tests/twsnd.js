// water sounds: wading splashes, dry land does not; the game runs by the sea and by a river with sound on without errors
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,TOWNS,terrainH,WORLD,SPAWN,WGEN,waterAt,stepSound,audioInit,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.WORLD.rivers,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); T.audioInit(); }); await sleep(1200);
 const r=await pg.evaluate(async()=>{ const out={}, S=T.WGEN.sea(), t=T.TOWNS[0]; let d=40; while(d<400&&T.waterAt(t.x+S.nx*d,t.z+S.nz*d)<T.terrainH(t.x+S.nx*d,t.z+S.nz*d)+0.25) d+=1;
   const wx=t.x+S.nx*d, wz=t.z+S.nz*d; out.depth=+(T.waterAt(wx,wz)-T.terrainH(wx,wz)).toFixed(2); out.wade=T.stepSound({pos:{x:wx,y:T.terrainH(wx,wz),z:wz}}); out.dry=T.stepSound({pos:{x:t.x+S.nx*(d-25),y:T.terrainH(t.x+S.nx*(d-25),t.z+S.nz*(d-25)),z:t.z+S.nz*(d-25)}});
   T.P.pos.set(t.x+S.nx*(d-4),T.terrainH(t.x+S.nx*(d-4),t.z+S.nz*(d-4))+0.1,t.z+S.nz*(d-4)); T.P.vel.set(0,0,0); await new Promise(r=>setTimeout(r,1500));
   const rv=T.WORLD.rivers[0], p=rv.pts[Math.floor(rv.pts.length/2)]; out.river=!!p; T.P.pos.set(T.SPAWN[0]+p[0]+6,T.terrainH(T.SPAWN[0]+p[0]+6,T.SPAWN[2]+p[1])+0.1,T.SPAWN[2]+p[1]); T.P.vel.set(0,0,0); await new Promise(r=>setTimeout(r,1500)); return out; });
 console.log(JSON.stringify(r), r.wade==='step_water'&&r.dry!=='step_water'&&r.river?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
