const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,WORLD,TOWNS,karts,simKart,slopeAt,terrainH,physStep,moveBody,SPAWN,settings,get B(){return B}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:180000});
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(2500); // bot left on (the default)
 const r=await pg.evaluate(()=>{ const out={}; out.botOn=!!(T.B&&T.B.active); out.sky=T.P.sky&&T.P.sky.phase; out.h=Math.round(T.P.pos.y-T.terrainH(T.P.pos.x,T.P.pos.z));
   out.roads=T.WORLD.roads.filter(r=>!r.street).length;
   const near=(rd,t)=>{ const S=T.SPAWN, a=rd.pts[0], b=rd.pts[rd.pts.length-1]; return Math.min(Math.hypot(S[0]+a[0]-t.x,S[2]+a[1]-t.z),Math.hypot(S[0]+b[0]-t.x,S[2]+b[1]-t.z)); };
   const link=(i,j)=>T.WORLD.roads.some(rd=>!rd.street&&near(rd,T.TOWNS[i])<60&&near(rd,T.TOWNS[j])<60);
   out.kettleCopper=link(2,8); out.hollowBramble=link(5,7);
   // steepest grade along the two new roads
   // a buggy on a steep slope slides back instead of climbing
   const S=T.SPAWN; let spot=null; for(let k=0;k<200000&&!spot;k++){ const a=k*2.399, d=100+(k%3000)*0.2, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d; const [s]=T.slopeAt(x,z); if(s>1.0&&s<1.3&&T.slopeAt(x+2,z)[0]>0.95&&T.slopeAt(x,z+2)[0]>0.95) spot=[x,z]; }
   const k=T.karts[0], [,gx,gz]=T.slopeAt(spot[0],spot[1]); Object.assign(k,{x:spot[0],z:spot[1],y:T.terrainH(spot[0],spot[1]),yaw:Math.atan2(-gx,-gz),vx:0,vz:0,air:false});
   const y0=k.y; for(let i=0;i<240;i++) T.simKart(k,{fw:1,st:0,hb:false},1/60); out.kartClimb=+(k.y-y0).toFixed(2);
   // walking past the old circle edge is no longer stopped
   T.P.sky=null; T.P.pos.set(S[0]+805,T.terrainH(S[0]+805,S[2]),S[2]); T.P.vel.set(6,0,0); T.P.onGround=true; for(let i=0;i<60;i++) T.physStep(1/60); out.pastEdge=+(Math.hypot(T.P.pos.x-S[0],T.P.pos.z-S[2])).toFixed(1);
   return out; });
 console.log(JSON.stringify(r)); const ok=r.sky&&r.roads>=0&&r.kettleCopper&&r.hollowBramble&&r.kartClimb<0.3;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
