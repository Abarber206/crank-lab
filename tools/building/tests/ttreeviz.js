const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,props,terrainH'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(800);
 const info=await pg.evaluate(()=>{ let best=null, bd=1e9; const tr=T.props.filter(p=>p.lazy&&p.alive&&!p.gone); for(const a of tr){ if(a.kind!=='tree') continue; const pn=tr.find(q=>q.kind==='pine'&&Math.hypot(q.x-a.x,q.z-a.z)<9&&Math.hypot(q.x-a.x,q.z-a.z)>4.5); if(pn){ const d=Math.hypot(a.x,a.z); if(d<bd){ bd=d; best=[a,pn]; } } }
   const [a,pn]=best, mx=(a.x+pn.x)/2, mz=(a.z+pn.z)/2, dx=pn.x-a.x, dz=pn.z-a.z, l=Math.hypot(dx,dz), nx=-dz/l, nz=dx/l; T.P.pos.set(mx+nx*9,T.terrainH(mx+nx*9,mz+nz*9)+0.2,mz+nz*9); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(-(mx-T.P.pos.x),-(mz-T.P.pos.z)); T.P.pitch=0.22; return T.renderer.info.render.triangles; });
 await sleep(5000); await pg.screenshot({path:'tree_new.png'}); console.log('tris before',info,'after',await pg.evaluate(()=>T.renderer.info.render.triangles), errs.join('\n')||'no errors'); await b.close(); })();
