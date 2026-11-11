// draw calls and triangles of each pass (main, reflection, shadows) at a riverside view: node tperf.js [file]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.argv[2]||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,waterAt,waterDepth,camera,SPAWN,WORLD,PERF'),{vp:{width:800,height:500}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000});
 const sp=await pg.evaluate(()=>{ // a spot on the main river, looking downstream along it
   const rv=T.WORLD.rivers.find(r=>r.main)||T.WORLD.rivers[0], q=Math.floor(rv.pts.length*0.45), p=rv.pts[q], n=rv.pts[q+6], S=T.SPAWN; const x=S[0]+p[0], z=S[2]+p[1], yaw=Math.atan2(-(n[0]-p[0]),-(n[1]-p[1]));
   T.P.pos.set(x,T.terrainH(x,z),z); T.P.vel.set(0,0,0); T.P.yaw=yaw; T.P.pitch=-0.05; window.__hold=[x,z,yaw];
   T.renderer.info.autoReset=false; const R=T.renderer.render.bind(T.renderer); window.__log=[]; T.renderer.render=(s,c)=>{ if(c===T.camera){ T.P.pos.set(window.__hold[0],T.P.pos.y,window.__hold[1]); T.P.yaw=window.__hold[2]; T.P.pitch=-0.05; } const i=T.renderer.info.render, c0=i.calls, t0=i.triangles; R(s,c); window.__log.push([c===T.camera?'main':(T.renderer.getRenderTarget()?'rt':'other'),c.type,i.calls-c0,i.triangles-t0]); };
   return {x,z,w:T.waterAt(x,z)}; });
 await sleep(4000); const r=await pg.evaluate(()=>{ window.__log.length=0; return new Promise(res=>setTimeout(()=>res(window.__log.slice(-12)),1500)); });
 console.log(JSON.stringify(sp)); console.log(JSON.stringify(r)); console.log(JSON.stringify(await pg.evaluate(()=>T.PERF)));
 if(process.argv[3]) await pg.screenshot({path:process.argv[3],timeout:200000});
 console.log(errs.join('\n')||'no errors'); await b.close(); })();
