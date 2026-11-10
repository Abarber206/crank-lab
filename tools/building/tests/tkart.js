// the dune buggy: found in garages, get in, drive, steer, stop at walls, get out
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','WORLD,SPAWN,P,scene,renderer,TOWNS,karts,simKart,enterKart,exitKart,findUseTarget,stepKarts,terrainH,settings,pieces,kartHits,get mode(){return mode}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); T.settings.skyDrop=false; });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 const r=await pg.evaluate(()=>{ const out={}, K=T.karts; out.karts=K.length; out.garages=T.TOWNS.reduce((n,t)=>n+t.houses.filter(h=>h.garage).length,0);
   out.towns=T.TOWNS.map(t=>K.filter(k=>Math.hypot(k.x-t.x,k.z-t.z)<t.R+5).length).join(',');
   const k=K[0]; out.home=[+k.x.toFixed(1),+k.y.toFixed(2),+k.z.toFixed(1)];
   // a garage floor under it
   out.onFloor=[...T.pieces.values()].some(p=>p.type==='floor'&&p.skin&&p.skin.garage===1&&Math.abs((p.i+.5)*5-k.x)<2.6&&Math.abs((p.j+.5)*5-k.z)<2.6);
   // walk up to the driver's door: the prompt says Drive
   const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw), rx=Math.cos(k.yaw), rz=-Math.sin(k.yaw);
   T.P.pos.set(k.x-rx*1.4,k.y,k.z-rz*1.4); T.P.yaw=Math.atan2(rx,rz); const tg=T.findUseTarget(); out.prompt=tg&&tg.label;
   T.enterKart(k,0); out.inside=!!T.P.kart; out.prompt2=(T.findUseTarget()||{}).label;
   const dt=1/60, step=(fw,st,hb,n)=>{ for(let i=0;i<n;i++) T.simKart(k,{fw,st,hb},dt); };
   // out of the garage, onto the drive
   const y0=k.yaw; step(1,0,false,90); out.after15=+Math.abs(k.vf).toFixed(1); out.moved=+Math.hypot(k.x-k.home.x,k.z-k.home.z).toFixed(1);
   step(1,0,false,150); out.top=+(Math.abs(k.vf)*3.6).toFixed(0);
   if(out.top<50){ const sx=k.x, sz=k.z, sy=k.y, syaw=k.yaw; // something stands across the street from this garage: take the run on an open road instead
     const rd=T.WORLD.roads.filter(r=>!r.street).sort((a,b)=>b.pts.length-a.pts.length)[0]; for(let q=20;q<rd.pts.length-80&&out.top<50;q+=25){ const p0=rd.pts[q], p1=rd.pts[q+3]; k.x=T.SPAWN[0]+p0[0]; k.z=T.SPAWN[2]+p0[1]; k.y=p0[2]; k.yaw=Math.atan2(-(p1[0]-p0[0]),-(p1[1]-p0[1])); k.vx=k.vz=k.vf=0; step(1,0,false,240); out.top=+(Math.abs(k.vf)*3.6).toFixed(0); out.roadRun=q; } }
   const yb=k.yaw; step(0.6,1,false,40); out.turnRight=angD(k.yaw,yb)<-0.2; // turning right lowers the heading
   function angD(a,b){ return ((a-b+Math.PI*3)%(Math.PI*2))-Math.PI; }
   if(out.roadRun!=null){ const rd=T.WORLD.roads.filter(r=>!r.street).sort((a,b)=>b.pts.length-a.pts.length)[0], p0=rd.pts[out.roadRun+40], p1=rd.pts[out.roadRun+43]; k.x=T.SPAWN[0]+p0[0]; k.z=T.SPAWN[2]+p0[1]; k.y=p0[2]; k.yaw=Math.atan2(-(p1[0]-p0[0]),-(p1[1]-p0[1])); k.vx=k.vz=0; k.vf=6; }
   step(-1,0,false,120); out.stopped=+Math.abs(k.vf).toFixed(2); step(-1,0,false,150); out.reverse=k.vf<-1; out.rv=+k.vf.toFixed(2);
   step(0,0,false,120);
   // back into its garage: it stops at the back wall instead of going through
   Object.assign(k,{x:k.home.x,z:k.home.z,y:k.home.y,yaw:k.home.yaw,vx:0,vz:0}); step(-1,0,false,240); out.backWall=+Math.hypot(k.x-k.home.x,k.z-k.home.z).toFixed(2);
   Object.assign(k,{x:k.home.x,z:k.home.z,y:k.home.y,yaw:k.home.yaw,vx:0,vz:0});
   T.stepKarts(dt); out.seatY=+(T.P.pos.y-k.y).toFixed(2);
   T.exitKart(true); out.out=!T.P.kart; out.free=k.seats[0]===null; out.exitDist=+Math.hypot(T.P.pos.x-k.x,T.P.pos.z-k.z).toFixed(2);
   // no building or edit from the seat
   T.enterKart(k,1); out.passenger=T.P.kart&&T.P.kart.seat===1; T.exitKart(true);
   return out; });
 console.log(JSON.stringify(r));
 const ok=r.karts>=4&&r.onFloor&&r.prompt==='Drive'&&r.inside&&r.prompt2==='Get out'&&r.moved>4&&r.top>=50&&r.top<=66&&r.turnRight&&r.reverse&&r.backWall<1.4&&r.out&&r.free&&r.exitDist>1&&r.passenger;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
