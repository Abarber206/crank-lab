// where the time goes: Chrome's sampling profiler over a few seconds of standing, then of skydiving, grouped by function
// node tprof.js [seconds]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,skyDrop,deployGlider,SPAWN'),process.env.DRAW?{vp:{width:800,height:480}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(4000);
 const cdp=await pg.context().newCDPSession(pg); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval',{interval:500});
 const secs=+(process.argv[2]||6);
 const run=async(label,setup)=>{ await pg.evaluate(setup); await sleep(1500); const f0=await pg.evaluate(()=>T.renderer.info.render.frame); await cdp.send('Profiler.start'); const t0=Date.now(); await sleep(secs*1000); const {profile}=await cdp.send('Profiler.stop'); const fr=await pg.evaluate(()=>T.renderer.info.render.frame)-f0, ms=Date.now()-t0;
   const self=new Map(), byId=new Map(profile.nodes.map(n=>[n.id,n])), dt=profile.timeDeltas; const cnt=new Map(); profile.samples.forEach((id,i)=>cnt.set(id,(cnt.get(id)||0)+(dt[i]||0)));
   for(const [id,us] of cnt){ const n=byId.get(id), fn=n.callFrame.functionName||'(anon)', k=fn+':'+n.callFrame.lineNumber; self.set(k,(self.get(k)||0)+us); }
   const tot=[...self.values()].reduce((a,b)=>a+b,0), top=[...self.entries()].sort((a,b)=>b[1]-a[1]).slice(0,22);
   console.log('== '+label+': '+fr+' frames in '+ms+' ms ('+(ms/Math.max(1,fr)).toFixed(1)+' ms/frame)'); top.forEach(([k,us])=>console.log('  '+(us/1000/Math.max(1,fr)).toFixed(2).padStart(7)+' ms/frame  '+(100*us/tot).toFixed(1).padStart(5)+'%  '+k)); };
 await run('standing',()=>{});
 await run('skydiving',()=>{ const S=T.SPAWN; T.skyDrop(S[0]+80,S[2]-120,560); });
 await run('gliding',()=>{ const S=T.SPAWN; T.skyDrop(S[0]-200,S[2]+90,200); T.deployGlider(T.P); });
 console.log(errs.join('\n')||'no errors'); await b.close(); })();
