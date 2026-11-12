// cars and people: a parked car is solid along its real angle (not a box snapped to 90 degrees); a driven buggy stops
// against a person in front of it; a buggy that ends up on you pushes you out
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,P,karts,kartHits,propBoxes,stepKarts,terrainH,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.props&&T.props.length>1000&&T.karts&&T.karts.length,null,{timeout:180000}); await sleep(1500);
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); }); await sleep(5000);
 const r=await pg.evaluate(()=>{ const cars=T.props.filter(p=>p.kind==='car'&&!p.gone); let inside=0, inMiss=0, side=0, sideHit=0;
   const inB=(bs,x,z)=>bs.some(b=>x>b[0]&&x<b[3]&&z>b[2]&&z<b[5]);
   for(const c of cars){ const bs=T.propBoxes(c), yw=c.g.rotation.y, ux=Math.cos(yw), uz=-Math.sin(yw), vx=-uz, vz=ux;
     for(const a of [-1.6,-0.8,0,0.8,1.6]) for(const w of [-0.55,0,0.55]){ inside++; if(!inB(bs,c.x+ux*a+vx*w,c.z+uz*a+vz*w)) inMiss++; }
     for(const s of [-1,1]) for(const a of [-1,0,1]){ side++; if(inB(bs,c.x+ux*a+vx*s*1.55,c.z+uz*a+vz*s*1.55)) sideHit++; } }
   const k=T.karts.find(k=>!k.boat), fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw);
   T.P.pos.set(k.x+fx*3.2,k.y,k.z+fz*3.2); const blocked=T.kartHits(k,k.x+fx*1.6,k.z+fz*1.6,k.yaw,k.x,k.z);
   T.P.pos.set(k.x+fx*30,k.y,k.z+fz*30); const clear=T.kartHits(k,k.x+fx*1.6,k.z+fz*1.6,k.yaw,k.x,k.z);
   T.P.pos.set(k.x+0.2,k.y,k.z+0.1); for(let i=0;i<5;i++) T.stepKarts(0.016); const out=Math.hypot(T.P.pos.x-k.x,T.P.pos.z-k.z);
   return {cars:cars.length,inside,inMiss,side,sideHit,blocked,clear,pushedOut:+out.toFixed(2)}; });
 console.log(JSON.stringify(r)); const ok=r.cars>10&&r.inMiss===0&&r.sideHit<=r.side*0.1&&r.blocked&&!r.clear&&r.pushedOut>0.9;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();
