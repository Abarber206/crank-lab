// steep mountainsides: can't walk up them, slide down them (no fall damage from a slide); gentle hills still walkable
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,physStep,moveBody,stepFall,terrainH,terrainUnder,slopeAt,settings,SPAWN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); T.settings.skyDrop=false; });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 const r=await pg.evaluate(()=>{ const P=T.P, S=T.SPAWN, out={};
   // find spots by slope
   const find=(lo,hi,minH)=>{ for(let k=0;k<200000;k++){ const a=k*2.399, d=60+(k%4000)*0.18, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d; const [s]=T.slopeAt(x,z); if(s>lo&&s<hi&&T.terrainH(x,z)>(minH||0)){ const [s2]=T.slopeAt(x+1.5,z), [s3]=T.slopeAt(x,z+1.5); if(s2>lo&&s3>lo&&s2<hi*1.3&&s3<hi*1.3) return [x,z]; } } return null; };
   const steep=find(1.3,2.2,20), gentle=find(0.3,0.6,5); out.found=!!steep&&!!gentle;
   const sim=(x,z,fwUp,secs)=>{ P.pos.set(x,T.terrainUnder(x,z),z); P.vel.set(0,0,0); P.onGround=true; P.fallTop=null; P.hp=100; P.slideT=0;
     const [,gx,gz]=T.slopeAt(x,z); P.yaw=Math.atan2(-gx,-gz); // face uphill
     const y0=P.pos.y, dt=1/120; for(let t=0;t<secs;t+=dt){ T.moveBody(P,fwUp,0,false,dt); T.physStep(dt); T.stepFall(); }
     return {dy:+(P.pos.y-y0).toFixed(2),hp:P.hp,moved:+Math.hypot(P.pos.x-x,P.pos.z-z).toFixed(1)}; };
   out.steepWalkUp=sim(steep[0],steep[1],1,3);   // tries to walk straight up a cliff
   out.steepStand=sim(steep[0],steep[1],0,2.5);  // just stands on it
   out.gentleWalkUp=sim(gentle[0],gentle[1],1,3);
   out.flat=sim(S[0],S[2],1,1);
   return out; });
 console.log(JSON.stringify(r));
 const ok=r.found&&r.steepWalkUp.dy<0.3&&r.steepStand.dy<-1.5&&r.steepStand.hp===100&&r.gentleWalkUp.dy>3&&r.flat.moved>4;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
