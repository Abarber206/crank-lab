// where a battle royale frame goes: a JS profile (self time by function) while 99 bots skydive and then play, the player
// standing in Gearworks; plus draw calls and triangles there
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,renderer,TOWNS,terrainH,camera'),{vp:{width:960,height:540}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(1500);
 const phase=process.argv[2]||'drop';
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T*0.55; }); await sleep(2500);
 await pg.evaluate(()=>{ const t=T.TOWNS.find(t=>t.name==='Gearworks'); T.P.sky=null; T.P.bus=false; T.P.pos.set(t.x+8,T.terrainH(t.x+8,t.z+10)+0.1,t.z+10); T.P.hp=1e6; });
 if(phase==='late'){ await sleep(40000); }
 if(process.argv[3]==='nr') await pg.evaluate(()=>{ T.scene.visible=false; });
 await sleep(3000);
 const cdp=await pg.context().newCDPSession(pg); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval',{interval:200}); await cdp.send('Profiler.start');
 const f0=await pg.evaluate(()=>{ window._fr=0; const f=()=>{ window._fr++; requestAnimationFrame(f); }; requestAnimationFrame(f); return performance.now(); });
 await sleep(12000);
 const {profile}=await cdp.send('Profiler.stop'); const fr=await pg.evaluate(()=>window._fr);
 const self=new Map(); const byId=new Map(profile.nodes.map(n=>[n.id,n])); const dt=profile.timeDeltas; let tot=0;
 profile.samples.forEach((id,k)=>{ const n=byId.get(id), key=n.callFrame.functionName+':'+n.callFrame.lineNumber; const d=dt[k]||0; tot+=d; self.set(key,(self.get(key)||0)+d); });
 const top=[...self.entries()].sort((a,b)=>b[1]-a[1]).slice(0,35); console.log('frames',fr,'in 12 s; profiled',(tot/1000).toFixed(0),'ms');
 for(const [k,v] of top) console.log((v/1000).toFixed(0).padStart(6),'ms',(100*v/tot).toFixed(1).padStart(5)+'%',k);
 // inclusive time for some functions
 const parent=new Map(); profile.nodes.forEach(n=>(n.children||[]).forEach(c=>parent.set(c,n.id)));
 const incl=new Map(); profile.samples.forEach((id,k)=>{ const seen=new Set(); let n=id; while(n!=null){ const nn=byId.get(n), key=nn.callFrame.functionName; if(!seen.has(key)){ seen.add(key); incl.set(key,(incl.get(key)||0)+(dt[k]||0)); } n=parent.get(n); } });
 for(const f of ['frame','brUpdate','brBotStep','brBot','renderMain','renderMain0','renderReflection','renderClouds','stepGrass','stepProps','botThink','brThink','updateCamera','stepTerrain','physStep','stepChunks','stepAnims','brView','stepIndoor','stepHarv','stepWeather','animateFigure','brFar']) if(incl.has(f)) console.log('incl',f,(incl.get(f)/1000).toFixed(0),'ms');
 const info=await pg.evaluate(()=>{ const r=T.renderer.info.render; return {calls:r.calls,tri:r.triangles,geo:T.renderer.info.memory.geometries,tex:T.renderer.info.memory.textures,prog:T.renderer.info.programs.length,alive:T.BR.bots.filter(b=>b.alive).length,sky:T.BR.bots.filter(b=>b.sky).length}; });
 console.log(JSON.stringify(info)); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();
