const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,physStep,moveBody,stepFall,skyDrop,terrainH,settings,fireDown,tryPlace,SPAWN,get mode(){return mode}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 const r=await pg.evaluate(()=>{ const P=T.P, out={}; out.start=P.sky&&P.sky.phase; out.h0=P.pos.y-T.terrainH(P.pos.x,P.pos.z);
   const hp0=P.hp; out.fire=(T.fireDown('mouse'),P.sky!=null); out.place=T.tryPlace('wall');
   let t=0, deployAt=null, maxV=0, landT=null; const dt=1/60; P.pitch=-0.8;
   while(t<120){ T.moveBody(P,1,0,false,dt); T.physStep(dt); T.stepFall(); maxV=Math.max(maxV,-P.vel.y);
     if(P.sky&&P.sky.phase==='glide'&&deployAt==null) deployAt=P.pos.y-T.terrainH(P.pos.x,P.pos.z);
     if(!P.sky){ landT=t; break; } t+=dt; }
   // a few ground steps
   for(let i=0;i<60;i++){ T.moveBody(P,0,0,false,dt); T.physStep(dt); T.stepFall(); }
   out.deployAt=deployAt; out.maxV=maxV; out.landT=landT; out.hp=P.hp+'/'+hp0; out.onGround=P.onGround; out.dist=Math.hypot(P.pos.x-T.SPAWN[0],P.pos.z-T.SPAWN[2]);
   // second drop: no dive, jump to deploy early
   T.skyDrop(T.SPAWN[0],T.SPAWN[2],300); P.pitch=0; let t2=0; for(;t2<2;t2+=dt){ T.moveBody(P,0,0,t2>1.5,dt); T.physStep(dt);} out.earlyDeploy=P.sky&&P.sky.phase; 
   for(let i=0;i<60*120&&P.sky;i++){ T.moveBody(P,0,0,false,dt); T.physStep(dt); T.stepFall(); } out.hp2=P.hp; out.sky2=P.sky;
   return out; });
 console.log(JSON.stringify(r));
 const ok=r.start==='fall'&&r.h0>550&&r.place===false&&r.deployAt>60&&r.deployAt<90&&r.maxV>50&&r.landT&&r.hp.startsWith('100')&&r.onGround&&r.earlyDeploy==='glide'&&r.hp2===100&&r.sky2===null;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
