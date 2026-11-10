const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,physStep,moveBody,stepFall,skyDrop,settings,SPAWN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(()=>{ const P=T.P, dt=1/60, run=(j,n)=>{ for(let i=0;i<n;i++){ T.moveBody(P,0,0,j,dt); T.physStep(dt); T.stepFall(); } };
   T.skyDrop(T.SPAWN[0],T.SPAWN[2],400); run(false,90); run(true,2); run(false,30); const a=P.sky&&P.sky.phase; // jump: glider out
   run(false,60); run(true,2); run(false,10); const b=P.sky&&P.sky.phase; // jump: let go
   run(false,50); run(true,2); run(false,10); const c=P.sky&&P.sky.phase; // jump: out again
   P.pitch=-0.8; for(let i=0;i<60*120&&P.sky;i++) run(false,1); return {a,b,c,landed:!P.sky,hp:P.hp}; });
 console.log(JSON.stringify(r), r.a==='glide'&&r.b==='fall'&&r.c==='glide'&&r.landed&&r.hp===100?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
