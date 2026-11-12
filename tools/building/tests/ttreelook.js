// what the trees look like where players see them: the lobby (behind the menu) and in the world, near / middle / far
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,camera,settings,TOD,terrainH,props,SPAWN'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.renderer.info.render.frame>5,null,{timeout:180000}); await sleep(6000);
 await pg.screenshot({path:'/home/claude/work/look_lobby.png'});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(8000); await pg.evaluate(()=>{ T.TOD.fix=0.3; });
 // stand at the edge of a forest and look across it; then from a hilltop
 const spots=await pg.evaluate(()=>{ const tr=T.props.filter(p=>p.kind==='tree'&&!p.gone); const p=tr[Math.floor(tr.length*0.37)], q=tr[Math.floor(tr.length*0.71)]; return [[p.x+18,p.z+18,p.x,p.z],[q.x-25,q.z+10,q.x,q.z]]; });
 let n=0; for(const [x,z,lx,lz] of spots){ await pg.evaluate(([x,z,lx,lz])=>{ T.P.pos.set(x,T.terrainH(x,z)+0.1,z); T.P.yaw=Math.atan2(-(lx-x),-(lz-z)); T.P.pitch=0.02; },[x,z,lx,lz]); await sleep(6000);
   await pg.screenshot({path:'/home/claude/work/look_world'+(n++)+'.png'}); }
 await pg.evaluate(()=>{ T.P.pitch=-0.25; T.P.pos.y+=0; }); 
 console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();
