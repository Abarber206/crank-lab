// knocked down: the whole body lies on the ground and follows the slope. A hero is laid down on flat ground, facing up a slope,
// facing down it and across it, lying still and crawling. Every visible vertex is measured against the terrain:
// nothing may sink in (pen), and the torso must rest on it (gap). node tcrawl.js [shots-prefix]
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,camera,heroFor,OUTFITS,animateRig,terrainH,slopeAt,SPAWN,settings,P'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const shots=process.argv[2]||'';
 const cases=process.env.ONLY?[['flat',0,0],['up',1,0],['down',1,Math.PI],['up-crawl',1,0,1.2]]:[['flat',0,0],['up',1,0],['down',1,Math.PI],['across',1,Math.PI/2],['flat-crawl',0,0,1.2],['up-crawl',1,0,1.2],['down-crawl',1,Math.PI,1.2],['across-crawl',1,-Math.PI/2,1.2]];
 const res=[];
 for(const c of cases){ const r=await pg.evaluate(async([name,slope,rel,spd])=>{ const S0=T.SPAWN; let spot=null;
   for(let k=0;k<200000&&!spot;k++){ const a=k*2.399, d=60+(k%3000)*0.25, x=S0[0]+Math.cos(a)*d, z=S0[2]+Math.sin(a)*d, [s]=T.slopeAt(x,z);
     if(slope?(s>0.45&&s<0.6&&Math.abs(T.slopeAt(x+1.5,z)[0]-s)<0.08&&Math.abs(T.slopeAt(x,z+1.5)[0]-s)<0.08):(s<0.03&&T.slopeAt(x+1.5,z)[0]<0.04&&T.slopeAt(x,z+1.5)[0]<0.04)) spot=[x,z]; }
   const [s,gx,gz]=T.slopeAt(spot[0],spot[1]); const upYaw=Math.atan2(-gx,-gz)+(slope?0:0.7); // yaw that faces uphill (forward is -sin,-cos)
   if(!window.__h){ window.__h=T.heroFor(T.OUTFITS[1]); T.scene.add(window.__h.group); } const h=window.__h; h.group.visible=true;
   const yaw=upYaw+rel, y=T.terrainH(spot[0],spot[1]);
   const st={pos:new THREE.Vector3(spot[0],y,spot[1]),vel:new THREE.Vector3(-Math.sin(yaw)*(spd||0),0,-Math.cos(yaw)*(spd||0)),yaw,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,down:{},ads:0,swingT:0,emote:null};
   h.anim.downT=0; let worstPen=0, worstGap=0, worstAll=0, slp=0;
   for(let f=0;f<150;f++){ if(spd) st.pos.addScaledVector(st.vel,1/60), st.pos.y=T.terrainH(st.pos.x,st.pos.z); T.animateRig(h,st,1/60);
     if(f>=70&&f%8===0){ h.group.updateMatrixWorld(true); let pen=0, torso=1e9, all=1e9; const v=new THREE.Vector3();
       h.group.traverse(o=>{ if(!o.isMesh||!o.geometry||!o.geometry.attributes.position) return; let vis=true; for(let q=o;q;q=q.parent) if(!q.visible){ vis=false; break; } if(!vis) return;
         const pa=o.geometry.attributes.position, step=Math.max(1,Math.floor(pa.count/60)); let inTorso=false; for(let q=o;q;q=q.parent) if(q===h.rig.chest||q===h.rig.spine) { inTorso=true; } 
         let isArm=false; for(let q=o;q;q=q.parent) if(q===h.rig.armL.sh||q===h.rig.armR.sh||q===h.rig.head) isArm=true; if(isArm) inTorso=false;
         for(let i=0;i<pa.count;i+=step){ v.fromBufferAttribute(pa,i).applyMatrix4(o.matrixWorld); const d=v.y-T.terrainH(v.x,v.z); pen=Math.min(pen,d); all=Math.min(all,d); if(inTorso) torso=Math.min(torso,d); } });
       worstPen=Math.min(worstPen,pen); worstGap=Math.max(worstGap,torso); } }
   // how the body lies: the line from the ankles to the neck against the ground under it
   const n=new THREE.Vector3(), a=new THREE.Vector3(); h.rig.neck.getWorldPosition(n); h.rig.hips.getWorldPosition(a); const bodyRise=(n.y-a.y)/Math.hypot(n.x-a.x,n.z-a.z), gRise=(T.terrainH(n.x,n.z)-T.terrainH(a.x,a.z))/Math.hypot(n.x-a.x,n.z-a.z);
   const cx=st.pos.x-Math.sin(yaw)*0.8, cz=st.pos.z-Math.cos(yaw)*0.8, cy=T.terrainH(cx,cz); window.__cam={p:[cx+Math.cos(yaw)*2.4,Math.max(cy+0.45,T.terrainH(cx+Math.cos(yaw)*2.4,cz-Math.sin(yaw)*2.4)+0.35),cz-Math.sin(yaw)*2.4],t:[cx,cy+0.15,cz]};
   return {name,slope:+s.toFixed(2),pen:+worstPen.toFixed(3),gap:+worstGap.toFixed(3),tilt:+(bodyRise-gRise).toFixed(2)}; },c);
  console.log(JSON.stringify(r)); res.push(r);
  if(shots){ await pg.evaluate(()=>{ const c=window.__cam; T.P.pos.set(c.t[0]+70,T.terrainH(c.t[0]+70,c.t[2])+0.1,c.t[2]); T.P.vel.set(0,0,0); T.settings.grassLevel='off'; window.__camHold=c; if(!window.__ch){ window.__ch=1; const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,cam)=>{ if(window.__camHold&&cam===T.camera){ const c=window.__camHold; cam.position.set(...c.p); cam.lookAt(...c.t); cam.updateMatrixWorld(); } R(s,cam); }; } });
    await sleep(1500); await pg.screenshot({path:shots+'_'+r.name+'.png',timeout:150000}); await pg.evaluate(()=>{ window.__camHold=null; }); } }
 const ok=res.every(r=>r.pen>-0.02&&r.gap<(r.name.includes('crawl')?0.18:0.13)&&Math.abs(r.tilt)<(r.name.includes('crawl')?0.35:0.2)); console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
