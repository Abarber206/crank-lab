// every emote, start to end: no broken joint values, the feet stay on the floor (within a few cm, except hops and kicks),
// and every song beat plays without an error.  node tdances.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,OUTFITS,heroFor,animateRig,EMOTES,emoteBeat,audioInit'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.EMOTES,null,{timeout:180000});
 const r=await pg.evaluate(()=>{ const out={}; try{ T.audioInit(); }catch(e){}
   for(const id of Object.keys(T.EMOTES)){ const E=T.EMOTES[id], h=T.heroFor(T.OUTFITS[0],'steel'), z=new THREE.Vector3(), S={bare:true,pos:z,vel:new THREE.Vector3(),yaw:0,pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:{id,t:0}};
     let bad=0, lo=9, hi=-9, songErr=null; const v=new THREE.Vector3();
     for(let t=0;t<E.dur;t+=1/30){ S.emote.t=t; T.animateRig(h,S,1/30); h.group.updateMatrixWorld(true);
       h.group.traverse(o=>{ if(!isFinite(o.rotation.x+o.rotation.y+o.rotation.z+o.position.x+o.position.y+o.position.z)) bad++; });
       const fy=Math.min(h.rig.legL.foot.getWorldPosition(v).y,h.rig.legR.foot.getWorldPosition(v).y); lo=Math.min(lo,fy); hi=Math.max(hi,fy); }
     if(E.beat){ try{ for(let b=0;b<Math.ceil(E.dur*E.beat);b++) T.emoteBeat(id,b); }catch(e){ songErr=e.message; } }
     out[id]={bad,footLo:+lo.toFixed(3),footHi:+hi.toFixed(3),songErr}; }
   return out; });
 let ok=true; for(const [id,x] of Object.entries(r)){ const f=x.bad===0&&!x.songErr&&x.footLo>-0.06; if(!f) ok=false; console.log(id.padEnd(11),JSON.stringify(x),f?'':'<-- FAIL'); }
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();
