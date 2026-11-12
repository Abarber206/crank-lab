// performance benchmark: for a few scenes, the drawing work per frame (draw calls and triangles, all passes) and where
// the script's time goes (inclusive, by subsystem, from Chrome's profiler; rendering itself excluded with NORENDER=1).
// node tbench.js [scenes: town,river,br]   DRAW=1 for draw counts (slower)
const {sleep,page,launch,open}=require('./h.js');
const SUBS=['brUpdate','brStepBot','brAnim','animateRig','physStep','renderReflection','renderMain','stepForest','stepTerrain','stepGrass','updateHUD','drawMini','hordeUpdate','stepAmbience','updateCamera','stepKarts','stepDrops','stepChests','stepProps','brSees','castShot','placeFarShadow','stepClouds','renderClouds','animateHero','stepPlayers','frame'];
(async()=>{ const b=await launch(); const draw=!!process.env.DRAW; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,SPAWN,camera,BR,BRBUS,WORLD,TOD'),draw?{vp:{width:1000,height:600}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 const scenes=(process.argv[2]||'town,river,br').split(',');
 const cdp=await pg.context().newCDPSession(pg); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval',{interval:400});
 await pg.evaluate(()=>{ const I=T.renderer.info; I.autoReset=false; window.__D={calls:0,tris:0,n:0,rc:0}; const R=T.renderer.render.bind(T.renderer);
   T.renderer.render=(s,c)=>{ const c0=I.render.calls, t0=I.render.triangles; R(s,c); const D=window.__D; D.calls+=I.render.calls-c0; D.tris+=I.render.triangles-t0; if(c===T.camera) D.n++; else if(c.isPerspectiveCamera) D.rc+=I.render.calls-c0; }; });
 const place=async sc=>pg.evaluate(sc=>{ const t=T.TOWNS[0];
   if(sc==='town'){ T.P.pos.set(t.x+6,T.terrainH(t.x+6,t.z+4)+0.05,t.z+4); T.P.yaw=0.6; T.P.pitch=-0.05; }
   if(sc==='river'){ const rv=T.WORLD.rivers.find(r=>r.main)||T.WORLD.rivers[0], p=rv.pts[Math.floor(rv.pts.length*0.45)], n=rv.pts[Math.floor(rv.pts.length*0.45)+6], S=T.SPAWN, x=S[0]+p[0]+p[3]+3, z=S[2]+p[1]; T.P.pos.set(x,T.terrainH(x,z)+0.05,z); T.P.yaw=Math.atan2(-(n[0]-p[0]),-(n[1]-p[1])); T.P.pitch=-0.05; }
   if(sc==='br'){ T.BRBUS.t=T.BRBUS.T; T.P.bus=false; T.P.sky=null; T.P.pos.set(t.x+6,T.terrainH(t.x+6,t.z+4)+0.05,t.z+4); T.P.yaw=0.6; T.P.pitch=-0.05; T.P.hp=1e6; T.BR.over=true; T.BR.overT=1e9;
     T.BR.bots.forEach((b,i)=>{ b.bus=false; b.sky=null; const a=i*0.33, r=15+i*5; const x=t.x+Math.cos(a)*r, z=t.z+Math.sin(a)*r; b.pos.set(x,T.terrainH(x,z)+0.1,z); b.vel.set(0,0,0); b.wpn=null; b.hp=1e6; }); }
   T.P.vel.set(0,0,0); },sc);
 for(const sc of scenes){
   await pg.evaluate(sc=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode='+(sc==='br'?'br':'fight')+']').click(); const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); if(!document.getElementById('menu').hidden) document.getElementById('play').click(); },sc);
   if(sc==='br') await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(1500);
   await place(sc); await sleep(2500); await place(sc);
   await pg.evaluate(()=>Object.assign(window.__D,{calls:0,tris:0,n:0,rc:0}));
   await cdp.send('Profiler.start'); const t0=Date.now(); await sleep(6000); const {profile}=await cdp.send('Profiler.stop'); const ms=Date.now()-t0;
   const D=await pg.evaluate(()=>window.__D), fr=Math.max(1,D.n);
   const byId=new Map(profile.nodes.map(n=>[n.id,n])), parent=new Map(); profile.nodes.forEach(n=>(n.children||[]).forEach(c=>parent.set(c,n.id)));
   const inc=new Map(); let tot=0; profile.samples.forEach((id,i)=>{ const dt=profile.timeDeltas[i]||0; tot+=dt; const seen=new Set(); let x=id; while(x!=null){ const fn=byId.get(x).callFrame.functionName; if(SUBS.includes(fn)&&!seen.has(fn)){ seen.add(fn); inc.set(fn,(inc.get(fn)||0)+dt); } x=parent.get(x); } });
   console.log('== '+sc+': '+fr+' frames in '+ms+' ms ('+(ms/fr).toFixed(1)+' ms/frame)'+(draw?' · draw calls/frame '+Math.round(D.calls/fr)+' (mirror '+Math.round(D.rc/fr)+') · ktris '+Math.round(D.tris/fr/1000):''));
   [...inc.entries()].sort((a,b)=>b[1]-a[1]).forEach(([k,us])=>console.log('  '+(us/1000/fr).toFixed(2).padStart(7)+' ms/frame  '+k)); }
 console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();
