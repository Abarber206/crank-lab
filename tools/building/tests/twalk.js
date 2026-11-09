const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,TOWNS,onWalk,SIDEWALKS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.props&&T.props.length>1000,null,{timeout:180000}); await sleep(3000);
 const r=await pg.evaluate(()=>{ let bad=0, yard=0; const near=(x,z)=>T.SIDEWALKS.some(([a,b])=>{ const dx=b[0]-a[0], dz=b[1]-a[1], L2=dx*dx+dz*dz||1e-6; let f=((x-a[0])*dx+(z-a[1])*dz)/L2; f=Math.max(0,Math.min(1,f)); return Math.hypot(x-a[0]-dx*f,z-a[1]-dz*f)<1.0+0.5; });
   for(const p of T.props){ if(!p.yard||p.kind==='furn') continue; yard++; if(near(p.x,p.z)) bad++; } return {yard,bad}; });
 console.log(JSON.stringify(r), r.bad===0?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
