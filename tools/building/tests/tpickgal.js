// every pickaxe in the Locker preview, one picture each (crop of the stage).  node tpickgal.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/pg'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,settings,PICKAXES,get _stage(){return _stage}'),{vp:{width:1100,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(2500);
 await pg.evaluate(()=>document.querySelector('button[data-tab=locker]').click()); await sleep(1000);
 if(process.env.D) await pg.evaluate(d=>{ window.__d=d; },process.env.D);
 await pg.evaluate(()=>{ const S=T._stage, R=S.r.render.bind(S.r); S.r.render=(sc,cam)=>{ if(S.heroes[0]){ const p=S.heroes[0].pos, y=(S.heroes[0].yaw||0)+(window.__a||0.5); const D=+(window.__d||2.2); cam.position.set(p.x-Math.sin(y)*D,p.y+1.35,p.z-Math.cos(y)*D); cam.lookAt(p.x,p.y+1.2,p.z); cam.fov=30; cam.updateProjectionMatrix(); } R(sc,cam); }; });
 const ids=(process.env.IDS||'').split(',').filter(Boolean); const list=ids.length?ids:await pg.evaluate(()=>T.PICKAXES.map(p=>p.id));
 for(const id of list){ await pg.evaluate(id=>{ window._stageLook={pk:id}; window._stagePrev=null; window._stagePickT=performance.now()+60000; },id); await sleep(1800); const el=await pg.$('#stageC'); await el.screenshot({path:pre+'_'+id+'.png',timeout:200000}); }
 console.log(list.join(',')); console.log(errs.join('\n')||'no errors'); await b.close(); })();
